"""Tests du rendu SVG déterministe de la figure 6 (identification de source)."""

import math
from dataclasses import replace
from pathlib import Path

import pytest

from jdriftx.experiences.identification_source import SCENARIO_DEFAUT, resoudre_scenario
from jdriftx.figures import figure_06
from jdriftx.figures.figure_06 import render_figure_06_svg

CHEMIN_ASSET = (
    Path(__file__).resolve().parents[1] / "site" / "images" / "figure-06-identification-source.svg"
)


def test_le_svg_est_bien_forme_et_annote() -> None:
    """La sortie est un document SVG complet avec les étiquettes attendues."""
    svg = render_figure_06_svg()
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert "Figure 6" in svg
    for etiquette in ("A", "B", "C", "R1"):
        assert etiquette in svg
    assert "probabilité de source" in svg


def test_les_valeurs_affichees_proviennent_du_resultat() -> None:
    """Chaque valeur affichée est recalculée depuis le résultat typé."""
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    svg = render_figure_06_svg()
    u0, u1 = scenario.vent
    vitesse = math.sqrt(u0 * u0 + u1 * u1)
    attendu_vent = f"Vent uniforme U = {vitesse:.1f} m/s vers le sud-ouest."
    assert attendu_vent in svg
    attendu_seuil = f"Cinq capteurs au sol ; seuil de détection {scenario.seuil_detection:.1e}."
    assert attendu_seuil in svg
    nombre = int(scenario.fenetre.largeur / scenario.pas_candidats) + 1
    attendu_candidats = (
        f"Candidats : grille {nombre} fois {nombre}, pas {scenario.pas_candidats:.0f} m."
    )
    assert attendu_candidats in svg
    attendu_cout_nul = f"Coût nul J0 = {resultat.cout_nul:.1e} (absence de source)."
    assert attendu_cout_nul in svg
    attendu_detection = (
        f"Concentration au coin détecté : {resultat.concentration_detection:.1e} kg/m² ;"
    )
    assert attendu_detection in svg
    attendu_cellules = f"{resultat.cellules_detectees} cellules au-dessus du seuil (carte A)."
    assert attendu_cellules in svg
    attendu_minimum = (
        f"Minimum exact J = 0 à la source vraie, Q* = {resultat.debit_etoile:.2f} kg/s."
    )
    assert attendu_minimum in svg
    attendu_vallee_1 = (
        f"Vallée (J/J0 sous 1e-2) : {resultat.nombre_cellules_vallee} cellules, "
        f"{resultat.etendue_vallee:.0f} m le long"
    )
    assert attendu_vallee_1 in svg
    facteur = resultat.etendue_vallee / resultat.largeur_vallee
    attendu_vallee_2 = (
        f"du vent, {resultat.largeur_vallee:.0f} m en travers (facteur {facteur:.1f})."
    )
    assert attendu_vallee_2 in svg
    attendu_decale_1 = (
        f"Candidat décalé de {resultat.decalage_vent:.0f} m au vent : "
        f"Q* = {resultat.debit_etoile_decale:.2f} kg/s,"
    )
    assert attendu_decale_1 in svg
    attendu_decale_2 = (
        f"coût {resultat.cout_relatif_decale:.1e} de J0 : position et débit restent couplés."
    )
    assert attendu_decale_2 in svg


def test_les_cartes_sont_denses_et_coherentes() -> None:
    """Les deux cartes et la coupe portent les mêmes champs et le même coût."""
    svg = render_figure_06_svg()
    assert svg.count("<rect ") == 471
    assert svg.count("<circle ") == 20


def test_le_rendu_est_deterministe() -> None:
    """Deux appels consécutifs produisent exactement le même SVG."""
    assert render_figure_06_svg() == render_figure_06_svg()


def test_la_copie_versionnee_est_synchronisee() -> None:
    """La copie versionnée du SVG doit être identique au générateur."""
    assert CHEMIN_ASSET.read_text(encoding="utf-8") == render_figure_06_svg()


def test_le_rendu_rejette_un_minimum_non_nul(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un minimum non nul invalide l'identification sans bruit."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    faux = replace(resultat, cout_minimum=1e-9)
    monkeypatch.setattr(figure_06, "resoudre_scenario", lambda _scenario: faux)
    with pytest.raises(ValueError, match="exactement nul"):
        render_figure_06_svg()


def test_le_rendu_rejette_une_vallee_quasi_ronde(monkeypatch: pytest.MonkeyPatch) -> None:
    """Une vallée à peine plus longue que large invalide la lecture."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    faux = replace(resultat, etendue_vallee=200.0)
    monkeypatch.setattr(figure_06, "resoudre_scenario", lambda _scenario: faux)
    with pytest.raises(ValueError, match="plus longue que large"):
        render_figure_06_svg()


def test_le_rendu_rejette_une_ambiguite_absente(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un candidat décalé nettement plus coûteux invalide la carte."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    faux = replace(resultat, cout_relatif_decale=5e-2)
    monkeypatch.setattr(figure_06, "resoudre_scenario", lambda _scenario: faux)
    with pytest.raises(ValueError, match="ambiguïté"):
        render_figure_06_svg()
