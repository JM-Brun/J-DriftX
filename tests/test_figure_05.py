"""Tests du rendu SVG déterministe de la figure 5 (relief)."""

from dataclasses import replace
from pathlib import Path

import pytest

from jdriftx.experiences.relief import SCENARIO_DEFAUT, resoudre_scenario
from jdriftx.figures import figure_05
from jdriftx.figures.figure_05 import formate_composante, render_figure_05_svg

CHEMIN_ASSET = (
    Path(__file__).resolve().parents[1] / "site" / "images" / "figure-05-relief.svg"
)


def test_le_svg_est_bien_forme_et_annote() -> None:
    """La sortie est un document SVG complet avec les étiquettes attendues."""
    svg = render_figure_05_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert "Figure 5" in svg
    for etiquette in ("A", "B", "S", "R1"):
        assert etiquette in svg


def test_les_valeurs_affichees_proviennent_de_la_tranche() -> None:
    """Chaque valeur affichée est recalculée depuis la tranche typée."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    svg = render_figure_05_svg()
    u = formate_composante(SCENARIO_DEFAUT.vent[0])
    v = formate_composante(SCENARIO_DEFAUT.vent[1])
    attendu_vent = f"u = ({u}, {v}) m/s, identique dans les deux calculs."
    assert attendu_vent in svg
    assert f"Seuil : {SCENARIO_DEFAUT.seuil:.1e} kg m⁻³" in svg
    surface_sans = f"{int(resultat.surface_region_sans):,}".replace(",", " ")
    attendu_sans = f"Région sans : {surface_sans} m² ({resultat.cellules_sans} cellules)"
    assert attendu_sans in svg
    surface_avec = f"{int(resultat.surface_region_avec):,}".replace(",", " ")
    attendu_avec = f"Région avec : {surface_avec} m² ({resultat.cellules_avec} cellules)"
    assert attendu_avec in svg
    attendu_cmax_sans = f"c max sans : {resultat.concentration_max_sans:.1e} kg m⁻³"
    assert attendu_cmax_sans in svg
    attendu_cmax_avec = f"c max avec : {resultat.concentration_max_avec:.1e} kg m⁻³"
    assert attendu_cmax_avec in svg
    assert f"Ratio au sommet A : ×{resultat.ratio_sommet_1:.2f}" in svg
    assert f"Ratio au sommet B : ×{resultat.ratio_sommet_2:.2f}" in svg
    attendu_axe = f"h = {SCENARIO_DEFAUT.hauteur_source:.0f} m ; axe à {resultat.altitude_axe:.1f} m"
    assert attendu_axe in svg
    assert "Réflexion au sol du modèle référée à z = 0." in svg


def test_le_rendu_est_deterministe() -> None:
    """Deux appels consécutifs produisent exactement le même SVG."""
    assert render_figure_05_svg() == render_figure_05_svg()


def test_la_copie_versionnee_est_synchronisee() -> None:
    """La copie versionnée du SVG doit être identique au générateur."""
    assert CHEMIN_ASSET.read_text(encoding="utf-8") == render_figure_05_svg()


def test_le_rendu_rejette_un_seuil_trop_grand(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un seuil au-dessus des concentrations maximales vide les régions."""
    scenario = replace(SCENARIO_DEFAUT, seuil=1e-3)
    monkeypatch.setattr(figure_05, "SCENARIO_DEFAUT", scenario)
    with pytest.raises(ValueError, match="ne doivent pas être vides"):
        render_figure_05_svg()
