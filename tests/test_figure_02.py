"""Tests for the original chapter-figure-2 schematic."""

import math
from pathlib import Path

import pytest

from jdriftx.experiences.uniforme import (
    SCENARIO_DEFAUT,
    ChampUniforme,
    ScenarioUniforme,
    resoudre_scenario,
)
from jdriftx.figures import figure_02
from jdriftx.figures.figure_02 import render_figure_02_svg


def test_figure_02_svg_is_well_formed_enough_for_a_static_asset() -> None:
    """The generated asset has a stable SVG root and closes its elements."""
    # Given — the deterministic generator.
    # When — the figure is rendered.
    svg = render_figure_02_svg()
    # Then — the SVG root and structure are stable.
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert svg.count("<text ") == svg.count("</text>")
    assert 'aria-labelledby="title desc"' in svg


def test_figure_02_explains_both_geometries_and_scope() -> None:
    """Labels state the key mathematical distinction and schematic status."""
    # Given — the rendered figure.
    svg = render_figure_02_svg()
    # Then — the scientific qualifications are displayed.
    assert "Distance euclidienne" in svg
    assert "Coût de migration dirigé" in svg
    assert "Symétrique" in svg
    assert "cible en amont" in svg
    assert "pas une métrique au sens strict" in svg


def test_figure_02_displayed_costs_come_from_the_typed_experiment() -> None:
    """Displayed values come from the vertical slice, not a duplicated formula."""
    # Given — the default scenario resolved by the shared implementation.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # When — the figure is rendered.
    svg = render_figure_02_svg()
    # Then — the figure displays exactly those computed values.
    assert math.isinf(resultat.tau_cible_origine)
    assert f"τ(A, B) = {resultat.tau_origine_cible:.0f} s (aval) ; τ(B, A) = +∞ (amont)" in svg
    assert f"dE(A, B) = dE(B, A) = {resultat.distance_euclidienne:.0f} m" in svg


def test_versioned_svg_matches_the_generator() -> None:
    """The committed SVG stays exactly reproducible from its source code."""
    # Given — the versioned asset and the generator.
    asset = Path("site/images/figure-02-geometries.svg").read_text(encoding="utf-8")
    # When — the figure is rendered.
    svg = render_figure_02_svg()
    # Then — both are byte-identical.
    assert asset == svg


def test_figure_02_svg_generation_is_deterministic() -> None:
    """Re-running the generator produces byte-identical SVG text."""
    # Given / When — two consecutive renders.
    # Then — the outputs are identical.
    assert render_figure_02_svg() == render_figure_02_svg()


def test_figure_02_rejects_a_scenario_without_upstream_return(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The generator refuses a scenario whose reverse directed cost is finite."""
    # Given — a scenario with coincident origin and target: the reverse
    # cost is 0 (finite), which violates the figure's upstream assumption.
    scenario = ScenarioUniforme(
        champ=ChampUniforme(vent=(2.0, 0.0)),
        origine=(0.0, 0.0),
        cible=(0.0, 0.0),
    )
    monkeypatch.setattr(figure_02, "SCENARIO_DEFAUT", scenario)
    # When / Then — the render is refused before any output is produced.
    with pytest.raises(ValueError, match="amont"):
        render_figure_02_svg()
