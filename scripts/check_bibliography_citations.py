"""Validate Quarto citation keys against the site's BibTeX bibliography."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

_BIB_ENTRY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
_CITATION = re.compile(r"(?<![\w@])-?@([A-Za-z][A-Za-z0-9_:+-]*)")
_CROSS_REFERENCE_PREFIXES = (
    "fig-",
    "tbl-",
    "sec-",
    "eq-",
    "lst-",
    "thm-",
    "exm-",
    "def-",
    "prp-",
    "cor-",
    "lem-",
    "cnj-",
    "nte-",
    "sol-",
    "rem-",
    "app-",
)


def _bib_keys(bibliography: Path) -> set[str]:
    """Return citation keys declared in a BibTeX file."""
    content = bibliography.read_text(encoding="utf-8")
    return {match.group(1) for match in _BIB_ENTRY.finditer(content)}


def _prose_lines(path: Path) -> list[tuple[int, str]]:
    """Return source lines with fenced and inline code removed."""
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            continue
        line = re.sub(r"`[^`]*`", "", raw_line)
        result.append((number, line))
    return result


def check_citation_keys(site_dir: Path, bibliography: Path) -> list[str]:
    """Return diagnostics for citation keys missing from the bibliography."""
    keys = _bib_keys(bibliography)
    diagnostics: list[str] = []
    for source in sorted(site_dir.rglob("*.qmd")):
        if "_extensions" in source.parts or "_site" in source.parts:
            continue
        for line_number, line in _prose_lines(source):
            for match in _CITATION.finditer(line):
                key = match.group(1)
                if key.startswith(_CROSS_REFERENCE_PREFIXES) or key in keys:
                    continue
                diagnostics.append(
                    f"{source.relative_to(site_dir)}:{line_number}: "
                    f"citation key @{key} not found in {bibliography}"
                )
    return diagnostics


def main() -> int:
    """Run the citation-key validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--bibliography", type=Path, default=Path("site/references.bib"))
    args = parser.parse_args()
    diagnostics = check_citation_keys(args.site_dir, args.bibliography)
    if diagnostics:
        print("\n".join(diagnostics))
        print(f"Found {len(diagnostics)} unresolved citation(s).")
        return 1
    print(f"All citation keys resolve against {args.bibliography}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
