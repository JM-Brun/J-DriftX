"""Tests for the original chapter-figure-2 schematic."""

import math
from pathlib import Path

from jdriftx.figures.figure_02 import (
    POINT_A,
    POINT_B,
    VENT_UNIFORME,
    render_figure_02_svg,
)
from jdriftx.metric import pseudo_distance_uniforme


def test_figure_02_svg_is_well_formed_enough_for_a_static_asset() -> None:
    """The generated asset has a stable SVG root and closes its elements."""
    svg = render_figure_02_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert svg.count("<text ") == svg.count("</text>")
    assert 'aria-labelledby="title desc"' in svg


def test_figure_02_explains_both_geometries_and_scope() -> None:
    """Labels state the key mathematical distinction and schematic status."""
    svg = render_figure_02_svg()
    assert "Distance euclidienne" in svg
    assert "Coût de migration dirigé" in svg
    assert "Symétrique" in svg
    assert "cible en amont" in svg
    assert "pas une métrique au sens strict" in svg


def test_figure_02_displayed_costs_come_from_the_shared_implementation() -> None:
    """Displayed values are computed by pseudo_distance_uniforme, not duplicated."""
    svg = render_figure_02_svg()
    tau_ab = pseudo_distance_uniforme(POINT_A, POINT_B, VENT_UNIFORME)
    tau_ba = pseudo_distance_uniforme(POINT_B, POINT_A, VENT_UNIFORME)
    distance_euclidienne = math.hypot(POINT_B[0] - POINT_A[0], POINT_B[1] - POINT_A[1])
    assert math.isinf(tau_ba)
    assert f"τ(A, B) = {tau_ab:.0f} s (aval) ; τ(B, A) = +∞ (amont)" in svg
    assert f"dE(A, B) = dE(B, A) = {distance_euclidienne:.0f} m" in svg


def test_versioned_svg_matches_the_generator() -> None:
    """The committed SVG stays exactly reproducible from its source code."""
    asset = Path("site/images/figure-02-geometries.svg").read_text(encoding="utf-8")
    assert asset == render_figure_02_svg()


def test_figure_02_svg_generation_is_deterministic() -> None:
    """Re-running the generator produces byte-identical SVG text."""
    assert render_figure_02_svg() == render_figure_02_svg()
