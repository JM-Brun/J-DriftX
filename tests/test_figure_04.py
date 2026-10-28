"""Tests du rendu SVG déterministe de la figure 4 (superposition)."""

from dataclasses import replace
from pathlib import Path

import pytest

from jdriftx.experiences.superposition_sources import SCENARIO_DEFAUT, resoudre_scenario
from jdriftx.figures import figure_04
from jdriftx.figures.figure_04 import formate_composante, render_figure_04_svg

CHEMIN_ASSET = (
    Path(__file__).resolve().parents[1] / "site" / "images" / "figure-04-superposition-sources.svg"
)


def test_le_svg_est_bien_forme_et_annote() -> None:
    """La sortie est un document SVG complet avec les étiquettes attendues."""
    svg = render_figure_04_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert "Figure 4" in svg
    for etiquette in ("S1", "S2", "M1", "M2", "M3", "R1"):
        assert etiquette in svg


def test_les_valeurs_affichees_proviennent_de_la_tranche() -> None:
    """Chaque valeur affichée est recalculée depuis la tranche typée."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    svg = render_figure_04_svg()
    vents = (resultat.vent_mesure_1, resultat.vent_mesure_2, resultat.vent_mesure_3)
    for etiquette, vent in zip(("M1", "M2", "M3"), vents, strict=True):
        attendu = (
            f"u({etiquette}) = ({formate_composante(vent[0])}, "
            f"{formate_composante(vent[1])}) m/s"
        )
        assert attendu in svg
    assert f"Seuil : {SCENARIO_DEFAUT.seuil:.1f} (concentration relative)" in svg
    assert f"r1 = r2 = {resultat.rayon_affecte_1:.1f} m" in svg
    surface = f"{int(resultat.surface_affectee_1):,}".replace(",", " ")
    assert f"S1 = S2 = {surface} m²" in svg
    totale = f"{int(resultat.surface_affectee_totale):,}".replace(",", " ")
    assert f"Région totale (grille 100 m) : {totale} m²" in svg
    assert f"Contribution de S2 en S1 : {resultat.contribution_croisee_1:.4f}" in svg
    attendu_max = f"Concentration max (somme, grille) : {resultat.concentration_max_totale:.3f}"
    assert attendu_max in svg
    assert "Région totale > S1 + S2" in svg
    assert "∇·u < 1e-12 s⁻¹" in svg


def test_le_rendu_est_deterministe() -> None:
    """Deux appels consécutifs produisent exactement le même SVG."""
    assert render_figure_04_svg() == render_figure_04_svg()


def test_la_copie_versionnee_est_synchronisee() -> None:
    """La copie versionnée du SVG doit être identique au générateur."""
    assert CHEMIN_ASSET.read_text(encoding="utf-8") == render_figure_04_svg()


def test_le_rendu_rejette_les_mesures_trop_faibles(monkeypatch: pytest.MonkeyPatch) -> None:
    """Une mesure dans une zone de vent quasi nul fait échouer le rendu."""
    mesures = ((400.0, 400.0), (1000.0, 1000.0), (1600.0, 400.0))
    scenario = replace(SCENARIO_DEFAUT, mesures=mesures)
    monkeypatch.setattr(figure_04, "SCENARIO_DEFAUT", scenario)
    with pytest.raises(ValueError, match="assez fortes"):
        render_figure_04_svg()
