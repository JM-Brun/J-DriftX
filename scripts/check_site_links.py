"""Check local links and fragments in a rendered Quarto site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class _PageParser(HTMLParser):
    """Collect local-link candidates and fragment identifiers from one HTML page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.identifiers: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        for name in ("id",):
            value = attributes.get(name)
            if value:
                self.identifiers.add(value)
        if tag == "a":
            name = attributes.get("name")
            if name:
                self.identifiers.add(name)
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.links.append((attribute, value))


def _parse_page(path: Path) -> _PageParser:
    parser = _PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def _resolve_target(
    raw_url: str,
    source: Path,
    root: Path,
    site_url: str,
) -> tuple[Path | None, str]:
    """Resolve a local URL to a rendered file and return its decoded fragment."""
    parsed = urlsplit(raw_url)
    site = urlsplit(site_url)
    fragment = unquote(parsed.fragment)

    if parsed.scheme and parsed.scheme.lower() not in {"http", "https"}:
        return None, fragment
    if parsed.netloc:
        if parsed.netloc.lower() != site.netloc.lower():
            return None, fragment
        target_path = unquote(parsed.path)
        base_path = site.path.rstrip("/")
        if base_path and (target_path == base_path or target_path.startswith(base_path + "/")):
            target_path = target_path[len(base_path) :]
        else:
            return None, fragment
    else:
        target_path = unquote(parsed.path)
        base_path = site.path.rstrip("/")
        if target_path.startswith("/") and base_path and (
            target_path == base_path or target_path.startswith(base_path + "/")
        ):
            target_path = target_path[len(base_path) :]

    if not target_path:
        target = source
    elif target_path.startswith("/"):
        target = root / target_path.lstrip("/")
    else:
        target = source.parent / target_path

    try:
        target = target.resolve()
        target.relative_to(root.resolve())
    except ValueError:
        return None, fragment

    candidates = [target]
    if not target.suffix:
        candidates.extend((target.with_suffix(".html"), target / "index.html"))
    for candidate in candidates:
        if candidate.is_dir():
            candidate = candidate / "index.html"
        if candidate.is_file():
            return candidate, fragment
    return target, fragment


def check_site_links(site_dir: Path, site_url: str) -> list[str]:
    """Return diagnostics for broken local files and HTML fragments."""
    root = site_dir.resolve()
    html_pages = sorted(root.rglob("*.html"))
    parsed_pages = {page: _parse_page(page) for page in html_pages}
    diagnostics: list[str] = []

    for source, page in parsed_pages.items():
        for attribute, raw_url in page.links:
            target, fragment = _resolve_target(raw_url, source, root, site_url)
            if target is None:
                continue
            if not target.is_file():
                diagnostics.append(
                    f"{source.relative_to(root)}: {attribute} target not found: {raw_url}"
                )
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                target_page = parsed_pages.get(target)
                if target_page is None:
                    try:
                        target_page = _parse_page(target)
                    except (OSError, UnicodeDecodeError):
                        diagnostics.append(
                            f"{source.relative_to(root)}: cannot read fragment target: {raw_url}"
                        )
                        continue
                if fragment not in target_page.identifiers:
                    known_ids = sorted(target_page.identifiers)
                    nearby_ids = [
                        identifier
                        for identifier in known_ids
                        if identifier.lower().startswith(fragment[:2].lower())
                    ][:12]
                    diagnostics.append(
                        f"{source.relative_to(root)}: fragment #{fragment} not found in "
                        f"{target.relative_to(root)} (from {raw_url}); "
                        f"nearby identifiers: {nearby_ids}"
                    )
    return diagnostics


def main() -> int:
    """Run the rendered-site link check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site/_site"))
    parser.add_argument(
        "--site-url",
        default="https://jm-brun.github.io/J-DriftX/",
        help="Published site URL, used to resolve same-site absolute URLs.",
    )
    args = parser.parse_args()

    if not args.site_dir.is_dir():
        parser.error(f"rendered site directory does not exist: {args.site_dir}")

    diagnostics = check_site_links(args.site_dir, args.site_url)
    if diagnostics:
        print(f"Found {len(diagnostics)} broken local link(s) or fragment(s):")
        for diagnostic in diagnostics:
            print(f"::error::{diagnostic}")
        return 1

    page_count = sum(1 for _ in args.site_dir.rglob("*.html"))
    print(f"Checked local links and fragments in {page_count} rendered HTML page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
