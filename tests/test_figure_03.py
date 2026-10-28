"""Tests du rendu SVG déterministe de la figure 3 (modèle réduit vs EDP)."""

from dataclasses import replace
from pathlib import Path

import pytest

from jdriftx.experiences.modele_reduit_edp import SCENARIO_DEFAUT, comparer_scenario
from jdriftx.figures import figure_03
from jdriftx.figures.figure_03 import render_figure_03_svg

CHEMIN_ASSET = (
    Path(__file__).resolve().parents[1] / "site" / "images" / "figure-03-modele-reduit-edp.svg"
)


def test_le_svg_est_bien_forme_et_annote() -> None:
    """La sortie est un document SVG complet avec les étiquettes attendues."""
    svg = render_figure_03_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert "Figure 3" in svg
    for etiquette in ("A", "B", "C", "D", "E", "R1"):
        assert etiquette in svg


def test_les_valeurs_affichees_proviennent_de_la_tranche() -> None:
    """Chaque valeur affichée est recalculée depuis la tranche typée."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    svg = render_figure_03_svg()
    attendu_vent = f"Vent uniforme U = {SCENARIO_DEFAUT.vent:.1f} m/s le long de x."
    assert attendu_vent in svg
    attendu_entree = (
        f"Entrée à {SCENARIO_DEFAUT.x_entree:.0f} m : colonne du panache de similitude."
    )
    assert attendu_entree in svg
    attendu_maillage = f"dy = {SCENARIO_DEFAUT.pas_transverse:.0f} m ; r = 1/3"
    assert attendu_maillage in svg
    l2_txt = f"{resultat.l2_reference:.1e}"
    linf_txt = f"{resultat.linf_reference:.1e}"
    attendu_normes = f"L2 relative : {l2_txt} ; L infinie relative : {linf_txt}."
    assert attendu_normes in svg
    flux_num_txt = f"{resultat.ecart_flux_max:.1e}"
    flux_red_txt = f"{resultat.ecart_flux_reduit:.1e}"
    attendu_flux = f"EDP {flux_num_txt} ; forme fermée {flux_red_txt} (rapporté à Q)."
    assert attendu_flux in svg
    r1_txt = f"{resultat.ratio_grossier:.1f}"
    r2_txt = f"{resultat.ratio_fin:.1f}"
    attendu_convergence = (
        f"Convergence : \u00d7{r1_txt} puis \u00d7{r2_txt} en divisant dy par deux."
    )
    assert attendu_convergence in svg
    for maillage in resultat.maillages:
        assert f"{maillage.l2_relative:.1e}" in svg
        assert f"dy = {maillage.pas_transverse:.0f} m" in svg


def test_les_cartes_sont_denses_et_coherentes() -> None:
    """Les trois cartes et le graphe de convergence portent les mêmes champs."""
    svg = render_figure_03_svg()
    assert svg.count("<rect ") == 806
    assert svg.count("<circle ") == 6


def test_le_rendu_est_deterministe() -> None:
    """Deux appels consécutifs produisent exactement le même SVG."""
    assert render_figure_03_svg() == render_figure_03_svg()


def test_la_copie_versionnee_est_synchronisee() -> None:
    """La copie versionnée du SVG doit être identique au générateur."""
    assert CHEMIN_ASSET.read_text(encoding="utf-8") == render_figure_03_svg()


def test_le_rendu_rejette_une_convergence_hors_ordre_deux(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un rapport de convergence hors de la plage d'ordre deux invalide le rendu."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    faux = replace(resultat, ratio_grossier=2.0)
    monkeypatch.setattr(figure_03, "comparer_scenario", lambda _scenario: faux)
    with pytest.raises(ValueError, match="ordre deux"):
        render_figure_03_svg()


def test_le_rendu_rejette_des_tranches_vides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Des tranches vides vident les cartes de concentration."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    faux = replace(resultat, tranches=())
    monkeypatch.setattr(figure_03, "comparer_scenario", lambda _scenario: faux)
    with pytest.raises(ValueError, match="ne doivent pas être vides"):
        render_figure_03_svg()
