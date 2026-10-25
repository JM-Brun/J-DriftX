"""Tests de la figure 1 : deux mesures ne déterminent pas un champ unique."""

from pathlib import Path

from jdriftx.experiences.reconstruction_vent import SCENARIO_DEFAUT, resoudre_scenario
from jdriftx.figures.figure_01 import formate_composante, render_figure_01_svg


def test_figure_01_svg_est_bien_formee() -> None:
    """L'asset généré a une racine SVG stable et ferme ses éléments."""
    # Given — le générateur déterministe.
    # When — la figure est rendue.
    svg = render_figure_01_svg()
    # Then — la racine et la structure SVG sont stables.
    assert svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert svg.rstrip().endswith("</svg>")
    assert svg.count("<text ") == svg.count("</text>")
    assert 'aria-labelledby="title desc"' in svg


def test_figure_01_explique_la_non_unicite_et_le_statut() -> None:
    """Les libellés énoncent la non-unicité et le statut de reconstruction."""
    # Given — la figure rendue.
    svg = render_figure_01_svg()
    # Then — les qualifications scientifiques sont affichées.
    assert "M1" in svg
    assert "M2" in svg
    assert "∇·u" in svg
    assert "Niveau R1" in svg
    assert "pas une reproduction" in svg
    assert "le champ interpolé n&#x27;est pas unique." in svg


def test_figure_01_affiche_les_valeurs_de_la_tranche() -> None:
    """Les valeurs affichées proviennent de la tranche typée, pas de formules dupliquées."""
    # Given — le scénario par défaut résolu par l'implémentation partagée.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    vent_1 = resultat.vent_mesure_1
    vent_2 = resultat.vent_mesure_2
    # When — la figure est rendue.
    svg = render_figure_01_svg()
    # Then — les étiquettes affichent exactement ces valeurs calculées.
    attendu_1 = f"u(M1) = ({formate_composante(vent_1[0])}, {formate_composante(vent_1[1])}) m/s"
    attendu_2 = f"u(M2) = ({formate_composante(vent_2[0])}, {formate_composante(vent_2[1])}) m/s"
    assert attendu_1 in svg
    assert attendu_2 in svg
    trajectoire = f"Trajectoire relevée au sol : {resultat.longueur_trajectoire:.0f} m"
    assert trajectoire in svg


def test_l_asset_svg_versionne_correspond_au_generateur() -> None:
    """L'asset SVG versionné reste exactement reproductible depuis son code source."""
    # Given — l'asset versionné et le générateur.
    asset = Path("site/images/figure-01-reconstruction-vent.svg").read_text(encoding="utf-8")
    # When — la figure est rendue.
    svg = render_figure_01_svg()
    # Then — les deux sont identiques octet par octet.
    assert asset == svg


def test_la_generation_svg_est_deterministe() -> None:
    """Deux rendus consécutifs produisent un SVG identique octet par octet."""
    # Given / When — deux rendus consécutifs.
    # Then — les sorties sont identiques.
    assert render_figure_01_svg() == render_figure_01_svg()
