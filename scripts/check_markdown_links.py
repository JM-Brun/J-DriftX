"""Validate local inline Markdown links in source documentation."""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")
_FENCE_RE = re.compile(r"^\s*(\x60{3,}|~{3,}).*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def _without_fenced_code(text: str) -> str:
    """Remove fenced code blocks to avoid treating examples as live links."""
    lines = text.splitlines()
    output: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line in lines:
        match = _FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char, fence_length = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char, fence_length = None, 0
            continue
        if fence_char is None:
            output.append(line)
    return "\n".join(output)


def _slug_heading(heading: str) -> str:
    """Approximate GitHub's heading-anchor slug for ordinary Markdown headings."""
    heading = re.sub(r"\x60([^\x60]*)\x60", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = "".join(
        char
        for char in unicodedata.normalize("NFKD", heading)
        if not unicodedata.combining(char)
    )
    heading = heading.replace("&", "-")
    # GitHub anchors retain a double separator around an em dash while
    # typographic quotes are removed without introducing extra separators.
    heading = re.sub(r"\s*[‐‑‒–—]\s*", "--", heading)  # noqa: RUF001
    heading = re.sub(r"[^\w\-\s]", "", heading, flags=re.UNICODE)
    heading = re.sub(r"\s+", "-", heading.strip().lower())
    return heading.strip("-")


def _heading_anchors(text: str) -> set[str]:
    """Build heading anchors, including GitHub-style suffixes for duplicates."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for heading in _HEADING_RE.findall(_without_fenced_code(text)):
        base = _slug_heading(heading)
        if not base:
            continue
        suffix = counts.get(base, 0)
        counts[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def _target_path(raw_target: str, source: Path, root: Path) -> tuple[Path | None, str]:
    """Resolve a local target and fragment; external and non-HTTP URLs are ignored."""
    parsed = urlsplit(raw_target)
    if parsed.scheme or parsed.netloc:
        return None, ""
    path_text = unquote(parsed.path)
    if not path_text:
        return source, unquote(parsed.fragment)
    target = (
        root / path_text.lstrip("/")
        if path_text.startswith("/")
        else source.parent / path_text
    )
    try:
        target = target.resolve()
        target.relative_to(root.resolve())
    except ValueError:
        return None, unquote(parsed.fragment)
    return target, unquote(parsed.fragment)


def check_markdown_links(root: Path, markdown_files: list[Path]) -> list[str]:
    """Return diagnostics for missing local targets and unresolved Markdown anchors."""
    root = root.resolve()
    diagnostics: list[str] = []
    anchors_cache: dict[Path, set[str]] = {}
    for source_path in markdown_files:
        source = source_path.resolve()
        text = source.read_text(encoding="utf-8")
        for match in _LINK_RE.finditer(_without_fenced_code(text)):
            raw_target = match.group(1).strip("<>")
            target, fragment = _target_path(raw_target, source, root)
            if target is None:
                continue
            if not target.exists():
                diagnostics.append(
                    f"{source.relative_to(root)}: local target not found: {raw_target}"
                )
                continue
            if (
                fragment
                and target.is_file()
                and target.suffix.lower() in {".md", ".markdown"}
            ):
                if target not in anchors_cache:
                    try:
                        anchors_cache[target] = _heading_anchors(
                            target.read_text(encoding="utf-8")
                        )
                    except (OSError, UnicodeDecodeError):
                        diagnostics.append(
                            f"{source.relative_to(root)}: cannot read anchor target: {raw_target}"
                        )
                        continue
                if fragment not in anchors_cache[target]:
                    diagnostics.append(
                        f"{source.relative_to(root)}: anchor #{fragment} not found in "
                        f"{target.relative_to(root)} (from {raw_target})"
                    )
    return diagnostics


def main() -> int:
    """Run the source-Markdown link check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--docs-dir", default="docs")
    args = parser.parse_args()
    root = args.root.resolve()
    docs_dir = (root / args.docs_dir).resolve()
    try:
        docs_dir.relative_to(root)
    except ValueError:
        parser.error(f"documentation directory must be inside repository root: {docs_dir}")
    if not docs_dir.is_dir():
        parser.error(f"documentation directory does not exist: {docs_dir}")

    files = sorted(docs_dir.rglob("*.md"))
    diagnostics = check_markdown_links(root, files)
    if diagnostics:
        print(f"Found {len(diagnostics)} broken local Markdown link(s) or anchor(s):")
        for diagnostic in diagnostics:
            print(f"::error::{diagnostic}")
        return 1
    print(f"Checked local Markdown links and anchors in {len(files)} source document(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
