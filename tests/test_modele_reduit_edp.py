"""Tests de la comparaison modèle réduit / EDP (tranche typée)."""

import dataclasses
import json
import math

import pytest

from jdriftx.experiences.modele_reduit_edp import (
    SCENARIO_DEFAUT,
    comparer_scenario,
    construire_manifeste,
    resoudre_edp,
)


def test_le_scenario_par_defaut_est_coherent() -> None:
    """Le scénario par défaut expose des maillages et des pas exacts."""
    assert SCENARIO_DEFAUT.nombre_tranches() == 18
    assert SCENARIO_DEFAUT.maillages() == (20.0, 10.0, 5.0)
    assert SCENARIO_DEFAUT.pas_longitudinal(10.0) == pytest.approx(25.0)
    assert SCENARIO_DEFAUT.pas_longitudinal(20.0) == pytest.approx(100.0)
    assert SCENARIO_DEFAUT.pas_longitudinal(5.0) == pytest.approx(6.25)


def test_les_parametres_doivent_etre_positifs() -> None:
    """Un paramètre nul ou négatif invalide le scénario."""
    champs = (
        "vent",
        "diffusivite",
        "debit",
        "x_entree",
        "x_fin",
        "demi_largeur",
        "pas_transverse",
        "pas_tranche",
    )
    for champ in champs:
        with pytest.raises(ValueError, match="strictement positif"):
            dataclasses.replace(SCENARIO_DEFAUT, **{champ: 0.0})


def test_x_fin_doit_etre_au_dela_de_l_entree() -> None:
    """Une fin confondue avec l'entrée invalide le scénario."""
    with pytest.raises(ValueError, match="au-delà"):
        dataclasses.replace(SCENARIO_DEFAUT, x_fin=300.0)


def test_les_distances_doivent_etre_multiples_du_pas_de_tranche() -> None:
    """Une distance hors grille de tranches invalide le scénario."""
    with pytest.raises(ValueError, match="x_entree doit être un multiple"):
        dataclasses.replace(SCENARIO_DEFAUT, x_entree=350.0)


def test_la_demi_largeur_doit_etre_multiple_du_pas_grossier() -> None:
    """Une fenêtre hors grille transversale invalide le scénario."""
    with pytest.raises(ValueError, match="multiple exact du pas grossier"):
        dataclasses.replace(SCENARIO_DEFAUT, demi_largeur=310.0)


def test_la_fenetre_doit_couvrir_quatre_ecarts_types() -> None:
    """Une fenêtre trop étroite tronquerait la queue du panache."""
    with pytest.raises(ValueError, match="quatre écarts-types"):
        dataclasses.replace(SCENARIO_DEFAUT, demi_largeur=100.0)


def test_le_pas_de_tranche_doit_diviser_le_pas_longitudinal() -> None:
    """Chaque maillage doit aligner ses pas pour marcher exactement."""
    with pytest.raises(ValueError, match="multiple exact du pas longitudinal"):
        dataclasses.replace(SCENARIO_DEFAUT, pas_transverse=15.0)


def test_la_forme_fermee_est_analytique() -> None:
    """Le pic transversal vaut Q sur sqrt(2 pi) U sigma."""
    x = 300.0
    sigma = SCENARIO_DEFAUT.ecart_type(x)
    pic = SCENARIO_DEFAUT.concentration_reduite(x, 0.0)
    denominateur = math.sqrt(2.0 * math.pi) * SCENARIO_DEFAUT.vent * sigma
    assert pic == pytest.approx(SCENARIO_DEFAUT.debit / denominateur, rel=1e-12)
    lateral = SCENARIO_DEFAUT.concentration_reduite(x, sigma)
    assert lateral == pytest.approx(pic * math.exp(-0.5), rel=1e-12)
    assert SCENARIO_DEFAUT.concentration_reduite(0.0, 0.0) == 0.0


def test_l_ecart_type_croit_en_racine_carree() -> None:
    """Doubler la distance multiplie l'écart-type par racine de deux."""
    attendu = math.sqrt(2.0) * SCENARIO_DEFAUT.ecart_type(300.0)
    assert SCENARIO_DEFAUT.ecart_type(600.0) == pytest.approx(attendu, rel=1e-12)


def test_les_deux_routes_coincident_exactement_a_l_entree() -> None:
    """Au premier pas, le champ numérique est la colonne d'entrée, bit à bit."""
    tranches = resoudre_edp(SCENARIO_DEFAUT, 10.0)
    assert tranches[0].numerique == tranches[0].reduite
    assert tranches[0].x == pytest.approx(300.0)


def test_le_champ_numerique_est_symetrique() -> None:
    """Entrée symétrique et Dirichlet symétrique donnent un champ symétrique."""
    tranches = resoudre_edp(SCENARIO_DEFAUT, 10.0)
    for tranche in tranches:
        nombre = len(tranche.numerique)
        for i in range(nombre // 2 + 1):
            assert tranche.numerique[i] == tranche.numerique[nombre - 1 - i]
            assert tranche.reduite[i] == tranche.reduite[nombre - 1 - i]


def test_les_bords_sont_au_dirichlet_nul() -> None:
    """Après le premier pas, les bords latéraux restent exactement nuls."""
    tranches = resoudre_edp(SCENARIO_DEFAUT, 10.0)
    for tranche in tranches[1:]:
        assert tranche.numerique[0] == 0.0
        assert tranche.numerique[-1] == 0.0


def test_les_normes_du_scenario_par_defaut_sont_reproductibles() -> None:
    """Les valeurs affichées sont recalculées depuis la tranche."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    grossier, reference, fin = resultat.maillages
    assert grossier.l2_relative == pytest.approx(1.1004e-2, rel=1e-3)
    assert reference.l2_relative == pytest.approx(2.5655e-3, rel=1e-3)
    assert fin.l2_relative == pytest.approx(6.3252e-4, rel=1e-3)
    assert resultat.l2_reference == pytest.approx(2.5655e-3, rel=1e-3)
    assert resultat.linf_reference == pytest.approx(3.0029e-3, rel=1e-3)
    assert resultat.ecart_flux_max == pytest.approx(6.928e-5, rel=1e-3)
    assert resultat.ecart_flux_reduit == pytest.approx(4.103e-5, rel=1e-3)
    assert resultat.concentration_max == pytest.approx(9.4032e-3, rel=1e-3)
    assert resultat.nombre_tranches == 18
    assert len(resultat.tranches) == 18
    assert reference.nombre_noeuds == 61


def test_la_convergence_est_d_ordre_deux() -> None:
    """Diviser le pas transversal par deux divise l'erreur par environ quatre."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    grossier, reference, fin = resultat.maillages
    assert 3.5 < resultat.ratio_grossier < 4.7
    assert 3.5 < resultat.ratio_fin < 4.7
    assert grossier.l2_relative > reference.l2_relative > fin.l2_relative


def test_le_manifeste_est_complet() -> None:
    """Le manifeste relie l'expérience à sa source et à ses limites."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resultat)
    assert manifeste.identifiant == "jdriftx-modele-reduit-edp-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert manifeste.hypothese
    assert manifeste.limites
    assert "uv run" in manifeste.commande
    export = manifeste.vers_dict()
    assert export["identifiant"] == "jdriftx-modele-reduit-edp-001"
    assert export["parametres"]["vent"] == SCENARIO_DEFAUT.vent
    assert export["resultats"]["l2_reference"] == pytest.approx(2.5655e-3, rel=1e-3)
    assert json.dumps(export)


def test_les_objets_sont_immuables() -> None:
    """Scénario, tranches et résultats refusent la mutation."""
    resultat = comparer_scenario(SCENARIO_DEFAUT)
    with pytest.raises(dataclasses.FrozenInstanceError):
        SCENARIO_DEFAUT.vent = 5.0  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        resultat.l2_reference = 0.0  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        resultat.tranches[0].x = 0.0  # type: ignore[misc]
