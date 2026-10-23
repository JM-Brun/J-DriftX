"""Tests for the original chapter-figure-2 schematic."""

from pathlib import Path

from jdriftx.figures.figure_02 import render_figure_02_svg


def test_figure_02_svg_is_well_formed_enough_for_a_static_asset() -> None:
    """The generated asset has a stable SVG root and closes its elements."""
    svg = render_figure_02_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert svg.count("<text ") == svg.count("</text>")
    assert "aria-labelledby=\"title desc\"" in svg


def test_figure_02_explains_both_geometries_and_scope() -> None:
    """Labels state the key mathematical distinction and schematic status."""
    svg = render_figure_02_svg()
    assert "Distance euclidienne" in svg
    assert "Coût de migration dirigé" in svg
    assert "Symétrique" in svg
    assert "cible en amont" in svg
    assert "pas une métrique au sens strict" in svg


def test_versioned_svg_matches_the_generator() -> None:
    """The committed SVG stays exactly reproducible from its source code."""
    asset = Path("site/images/figure-02-geometries.svg").read_text(encoding="utf-8")
    assert asset == render_figure_02_svg()


def test_figure_02_svg_generation_is_deterministic() -> None:
    """Re-running the generator produces byte-identical SVG text."""
    assert render_figure_02_svg() == render_figure_02_svg()
