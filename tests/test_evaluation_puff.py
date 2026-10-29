"""Tests de l'évaluation dirigée d'une source impulsionnelle (puff).

Couverture (étape 6, issue #232) : source impulsionnelle calibrée et figée,
temps dirigé par pseudo-distance uniforme (rejet amont), grille du cas S0
couverte, écarts et retards calibrés sous seuil, symétrie latérale exacte,
pic au passage sur les arcs proches, manifeste étiqueté, export JSON-natif.
"""

from __future__ import annotations

import json
import math

import pytest
from pydantic import ValidationError

import jdriftx.experiences.evaluation_puff as module_puff
from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, PointMesure
from jdriftx.experiences.evaluation_puff import (
    PUFF_DEFAUT,
    EvaluationPuff,
    ManifestePuff,
    SourceImpulsionnelle,
    construire_manifeste,
    evaluer_grille,
    evaluer_point,
    temps_dirige,
)


@pytest.fixture(scope="module")
def grille() -> tuple[PointMesure, ...]:
    """Grille de prélèvements du cas S0 figé (12 points, docs/48 §2.2)."""
    return CAS_S0_DEFAUT.points()


@pytest.fixture(scope="module")
def evaluations(grille: tuple[PointMesure, ...]) -> tuple[EvaluationPuff, ...]:
    """Évaluations dirigées du puff par défaut sur la grille (calcul unique)."""
    return evaluer_grille(PUFF_DEFAUT, grille)


@pytest.fixture(scope="module")
def manifeste(evaluations: tuple[EvaluationPuff, ...]) -> ManifestePuff:
    """Manifeste étiqueté de l'évaluation (calcul unique)."""
    return construire_manifeste(evaluations)


def test_la_source_par_defaut_est_calibree() -> None:
    """Le puff par défaut porte la calibration de l'étape 6."""
    # Given — le puff par défaut du module.
    # When — ses attributs sont lus.
    # Then — masse, vent, classe et position de l'étape 6 sont exacts.
    assert PUFF_DEFAUT.masse == 1.0
    assert PUFF_DEFAUT.u == 3.0
    assert PUFF_DEFAUT.classe == "C"
    assert PUFF_DEFAUT.x0 == 0.0


def test_une_classe_inconnue_est_rejetee() -> None:
    """Une classe hors registre partagé est rejetée à la construction."""
    # Given — une classe absente du registre jdriftx.stabilite.
    # When — la source est construite.
    # Then — la validation Pydantic rejette la classe inconnue.
    with pytest.raises(ValidationError, match="Classe de stabilité inconnue"):
        SourceImpulsionnelle(masse=1.0, u=3.0, classe="Z")


def test_la_source_est_immuable() -> None:
    """La source par défaut est gelée : l'affectation lève une ValidationError."""
    # Given — le puff par défaut, figé à la construction.
    # When / Then — toute affectation lève une ValidationError Pydantic.
    with pytest.raises(ValidationError):
        PUFF_DEFAUT.masse = 2.0


def test_le_temps_dirige_est_exact_aux_arcs(
    grille: tuple[PointMesure, ...],
) -> None:
    """Le temps dirigé vaut la distance sous le vent divisée par le vent."""
    # Given — le puff par défaut et la grille du cas S0 (docs/48 §2.5).
    # When — les temps dirigés sont évalués.
    # Then — chaque tau vaut arc/u, sans pénalité latérale.
    for point in grille:
        tau = temps_dirige(PUFF_DEFAUT, point)
        assert math.isclose(tau, point.x / PUFF_DEFAUT.u, rel_tol=1e-12)


def test_un_point_amont_est_rejete() -> None:
    """Un point strictement en amont de l'émission est rejeté (convention +inf)."""
    # Given — un point en amont de l'émission (x < x0).
    amont = PointMesure(x=-10.0, y=0.0, z=1.5)
    # When — le point est évalué.
    # Then — l'évaluation refuse le temps dirigé infini.
    with pytest.raises(ValueError, match="strictement à l'aval"):
        evaluer_point(PUFF_DEFAUT, amont)


def test_la_grille_du_cas_est_couverte(
    grille: tuple[PointMesure, ...],
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """L'évaluation couvre les 12 points du cas S0, dans l'ordre de la grille."""
    # Given — la grille du cas S0 et les évaluations associées.
    # When — les points évalués sont confrontés à la grille.
    # Then — chaque point est couvert une fois, dans l'ordre.
    assert len(evaluations) == len(grille)
    for evaluation, point in zip(evaluations, grille, strict=True):
        assert evaluation.point == point


def test_l_ecart_relatif_reste_dans_la_bande(
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """Chaque écart C(τ)/C(pic) - 1 reste dans la bande calibrée [-5 %, 0]."""
    # Given — les évaluations de la grille (12 points).
    # When — les écarts relatifs sont observés.
    # Then — l'évaluation dirigée capture au moins 95 % du pic, sans dépassement.
    for evaluation in evaluations:
        assert -0.05 <= evaluation.ecart_relatif <= 0.0


def test_le_retard_du_pic_reste_sous_le_seuil(
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """Le retard du pic (τ - t_pic)/τ reste sous 5 % sur la grille."""
    # Given — les évaluations de la grille (12 points).
    # When — les retards sont observés.
    # Then — aucun retard ne dépasse le seuil calibré (pire cas : 3,30 %).
    for evaluation in evaluations:
        retard = (evaluation.tau - evaluation.t_pic) / evaluation.tau
        assert retard <= 0.05


def test_la_symetrie_laterale_est_bit_a_bit(
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """Les paires latérales ±50 ont des évaluations identiques bit à bit."""
    # Given — les évaluations de la grille du cas S0.
    # When — les paires ±50 sont confrontées.
    # Then — tau, t_pic, concentrations et écart sont identiques (==).
    for gauche, droite in zip(evaluations[::3], evaluations[2::3], strict=True):
        assert gauche.tau == droite.tau
        assert gauche.t_pic == droite.t_pic
        assert gauche.concentration_tau == droite.concentration_tau
        assert gauche.concentration_pic == droite.concentration_pic
        assert gauche.ecart_relatif == droite.ecart_relatif


def test_le_pic_est_au_passage_sur_les_arcs_proches(
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """|y| = 50 m : le pic tombe au passage sur les arcs 100 et 200 m."""
    # Given — les évaluations des points latéraux (indices 0, 3, 6, 9).
    lateraux = evaluations[0::3]
    # When — les arcs 100 et 200 m sont observés.
    proches = lateraux[:2]
    # Then — le maximum de grille est atteint au passage, sans écart.
    for evaluation in proches:
        assert evaluation.t_pic == evaluation.tau
        assert evaluation.ecart_relatif == 0.0


def test_le_pire_ecart_est_sur_l_axe_du_premier_arc(
    evaluations: tuple[EvaluationPuff, ...],
) -> None:
    """Le pire écart de la grille est sur l'axe au premier arc (-4,90 %)."""
    # Given — les évaluations de la grille (12 points).
    # When — le pire écart est recherché.
    # Then — il se situe à l'arc 100 m sur l'axe, capture ≥ 95,1 % du pic.
    pire = min(evaluations, key=lambda evaluation: evaluation.ecart_relatif)
    assert pire.point.x == 100.0
    assert pire.point.y == 0.0
    assert math.isclose(pire.ecart_relatif, -0.049, abs_tol=0.001)


def test_le_manifeste_est_etiquete(manifeste: ManifestePuff) -> None:
    """Le manifeste porte l'étiquetage complet et les limites de l'étape 6."""
    # Given — le manifeste de l'évaluation dirigée.
    # When — ses champs d'étiquetage sont observés.
    # Then — héritage, extension et limites sont explicites (docs/47).
    assert manifeste.identifiant == "jdriftx-evaluation-puff-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "docs/47" in manifeste.heritage_documentaire
    assert manifeste.extension.startswith("Source impulsionnelle")
    limites = " ".join(manifeste.limites)
    assert "pas une validation physique" in limites
    assert "pas le maximum temporel exact" in limites


def test_le_manifeste_s_exporte_en_json_natif(manifeste: ManifestePuff) -> None:
    """Le manifeste s'exporte en JSON natif : types prêts à la sérialisation."""
    # Given — le manifeste et sa frontière d'export vers_dict.
    # When — le dictionnaire exporté est sérialisé puis rechargé.
    # Then — le JSON est valide et l'identifiant survit à l'aller-retour.
    exporte = manifeste.vers_dict()
    charge = json.loads(json.dumps(exporte))
    assert charge["identifiant"] == "jdriftx-evaluation-puff-001"
    assert charge["niveau_fidelite"] == "R1"
    assert len(charge["evaluations"]) == 12


def test_la_version_non_installee_est_supportee(
    evaluations: tuple[EvaluationPuff, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Le manifeste reste constructible quand le package n'est pas installé."""
    # Given — l'évaluation de la grille et un environnement non installé.
    def _introuvable(nom: str) -> str:
        raise module_puff.metadata.PackageNotFoundError(nom)

    monkeypatch.setattr(module_puff.metadata, "version", _introuvable)
    # When — le manifeste est construit malgré l'absence de métadonnées.
    manifeste = module_puff.construire_manifeste(evaluations)
    # Then — la version est explicitement rapportée comme non installée.
    assert manifeste.version_code == "non-installe"
