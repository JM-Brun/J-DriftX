"""Tests de l'API Python qui alimente l'explorateur Quarto des champs 2D."""

from __future__ import annotations

import pytest

from jdriftx.figures.wind_field_explorer import (
    WindFieldExplorerConfig,
    default_wind_field_scenarios,
    render_wind_field_explorer_html,
    render_wind_field_scenario_gallery_html,
)


@pytest.mark.parametrize(
    ("family", "expected_vector", "expected_description"),
    [
        ("Uniforme", "(2.00, 0.00)", "mêmes vecteurs"),
        ("Cisaillement linéaire", "(2.25, 0.00)", "varie linéairement"),
        ("Radial (source / puits)", "(0.70, 0.35)", "divergent de l'origine"),
    ],
)
def test_explorer_renders_each_python_field_family(
    family: str,
    expected_vector: str,
    expected_description: str,
) -> None:
    """Chaque famille rend le vecteur calculé par le noyau partagé."""
    config = WindFieldExplorerConfig(
        family=family,
        speed=2.0,
        angle_deg=0.0,
        shear=0.25,
        radial_strength=0.35,
        probe_x=2.0,
        probe_y=1.0,
    )

    html = render_wind_field_explorer_html(config)

    assert html.startswith("\n<style>")
    assert '<svg viewBox="0 0 760 520" class="vector-field-svg"' in html
    assert expected_vector in html
    assert expected_description in html
    assert "Divergence moyenne estimée" in html


def test_explorer_refuses_unknown_family() -> None:
    """Une étiquette de champ hors contrat est refusée avant le rendu."""
    with pytest.raises(ValueError, match="inconnue"):
        WindFieldExplorerConfig(
            family="Inconnu",
            speed=2.0,
            angle_deg=0.0,
            shear=0.0,
            radial_strength=1.0,
            probe_x=0.0,
            probe_y=0.0,
        )


def test_explorer_refuses_non_finite_parameter() -> None:
    """Un paramètre non fini ne peut pas produire un SVG ambigu."""
    with pytest.raises(ValueError, match="finis"):
        WindFieldExplorerConfig(
            family="Uniforme",
            speed=float("nan"),
            angle_deg=0.0,
            shear=0.0,
            radial_strength=1.0,
            probe_x=0.0,
            probe_y=0.0,
        )


def test_default_scenarios_are_python_rendered_in_native_details() -> None:
    """La galerie évite un moteur Python WebAssembly à télécharger par le lecteur."""
    scenarios = default_wind_field_scenarios()

    html = render_wind_field_scenario_gallery_html(scenarios)

    assert len(scenarios) == 4
    assert html.count("<svg") == 4
    assert html.count('class="wind-field-scenario"') == 4
    assert html.count("<details") == 4
    assert "Référence uniforme" in html
    assert "Source radiale" in html
    assert "Puits radial" in html


def test_gallery_refuses_an_empty_scenario_set() -> None:
    """Une page sans expérience est invalide plutôt que silencieusement vide."""
    with pytest.raises(ValueError, match="Au moins un"):
        render_wind_field_scenario_gallery_html(())
