"""Tests for rendered-site local link and fragment validation."""

from __future__ import annotations

from pathlib import Path

from scripts.check_site_links import check_site_links


def test_check_site_links_accepts_existing_files_and_fragments(tmp_path: Path) -> None:
    """Relative links, assets, fragments, and the published base path resolve."""
    root = tmp_path / "_site"
    (root / "guide").mkdir(parents=True)
    (root / "assets").mkdir()
    (root / "index.html").write_text(
        '<a href="guide/page.html#details">Guide</a>'
        '<a href="#top">Top</a>'
        '<img src="assets/figure.svg">'
        '<a href="https://example.test/external">External</a>'
        '<a href="https://jm-brun.github.io/J-DriftX/guide/page.html#details">Absolute</a>'
        '<a href="/J-DriftX/guide/page.html#details">Root-relative</a>',
        encoding="utf-8",
    )
    (root / "guide/page.html").write_text(
        '<main id="details"><a name="legacy-anchor"></a></main>',
        encoding="utf-8",
    )
    (root / "assets/figure.svg").write_text("<svg></svg>", encoding="utf-8")

    assert check_site_links(root, "https://jm-brun.github.io/J-DriftX/") == []


def test_check_site_links_reports_missing_file_and_fragment(tmp_path: Path) -> None:
    """Missing local targets and missing HTML fragments are reported."""
    root = tmp_path / "_site"
    root.mkdir()
    (root / "index.html").write_text(
        '<a href="missing.html">Missing page</a>'
        '<a href="index.html#not-here">Missing fragment</a>',
        encoding="utf-8",
    )

    diagnostics = check_site_links(root, "https://jm-brun.github.io/J-DriftX/")

    assert len(diagnostics) == 2
    assert any("missing.html" in diagnostic for diagnostic in diagnostics)
    assert any("not-here" in diagnostic for diagnostic in diagnostics)
