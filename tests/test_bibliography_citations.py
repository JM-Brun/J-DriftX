"""Tests for citation-key validation against the BibTeX bibliography."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_checker_path = (
    Path(__file__).resolve().parents[1] / "scripts" / "check_bibliography_citations.py"
)
_checker_spec = importlib.util.spec_from_file_location(
    "check_bibliography_citations", _checker_path
)
if _checker_spec is None or _checker_spec.loader is None:
    raise ImportError(f"Cannot load citation checker from {_checker_path}")
_checker_module = importlib.util.module_from_spec(_checker_spec)
_checker_spec.loader.exec_module(_checker_module)
check_citation_keys = _checker_module.check_citation_keys


def test_check_citation_keys_accepts_bib_entries_and_quarto_crossrefs(
    tmp_path: Path,
) -> None:
    """Known bibliography keys and Quarto cross-reference labels are accepted."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "references.bib").write_text(
        "@article{known2024,\n  title = {Example}\n}\n", encoding="utf-8"
    )
    (site / "page.qmd").write_text(
        "Cite @known2024 and [@known2024].\n"
        "See @fig-example and @sec-methods.\n"
        "`@not-a-citation`\n"
        "```text\n@also-not-a-citation\n```\n",
        encoding="utf-8",
    )

    assert check_citation_keys(site, site / "references.bib") == []


def test_check_citation_keys_reports_unknown_keys_with_line_numbers(
    tmp_path: Path,
) -> None:
    """Unknown citation keys produce source-relative diagnostics."""
    site = tmp_path / "site"
    site.mkdir()
    bibliography = site / "references.bib"
    bibliography.write_text("@article{known2024, title = {Example}}\n", encoding="utf-8")
    (site / "page.qmd").write_text(
        "Known: @known2024.\nUnknown: [@missing2025].\n", encoding="utf-8"
    )

    diagnostics = check_citation_keys(site, bibliography)

    assert len(diagnostics) == 1
    assert diagnostics[0].startswith("page.qmd:2:")
    assert "@missing2025" in diagnostics[0]
