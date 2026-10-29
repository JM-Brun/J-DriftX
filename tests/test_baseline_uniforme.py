"""Tests de la reconstruction baseline uniforme (étape 4 de l'issue #232)."""

import math
from dataclasses import FrozenInstanceError
from importlib import metadata

import pytest

import jdriftx.experiences.baseline_uniforme as module_baseline
from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, PointMesure
from jdriftx.experiences.baseline_uniforme import (
    CAS_REFERENCE_DEFAUT,
    EvaluationDirigee,
    construire_manifeste,
    evaluer_grille,
    evaluer_point,
    temps_dirige,
)


def test_le_cas_de_reference_est_le_cas_s0_fige() -> None:
    """CAS_REFERENCE_DEFAUT est le cas S0 figé de docs/48 §2.2, sans divergence."""
    # Given — le cas de référence autonome (docs/48 §6).
    cas = CAS_REFERENCE_DEFAUT
    # When / Then — il est le cas S0 figé, paramètre pour paramètre.
    assert cas is CAS_S0_DEFAUT
    assert cas.source.u == pytest.approx(3.0)
    assert cas.source.debit == pytest.approx(2.0)
    assert cas.source.classe == "C"
    assert cas.source.hauteur == pytest.approx(1.0)
    assert cas.arcs == (100.0, 200.0, 400.0, 800.0)
    assert cas.positions_laterales == (-50.0, 0.0, 50.0)
    assert cas.z_mesure == pytest.approx(1.5)


def test_le_temps_dirige_vaut_x_sur_u_sur_la_grille() -> None:
    """Le temps dirigé reconstruit vaut τ = x/U (docs/48 §2.6) sur les 12 points."""
    # Given — le cas de référence et sa grille de prélèvements.
    cas = CAS_REFERENCE_DEFAUT
    points = cas.points()
    # When — le temps dirigé est évalué point par point.
    taus = [temps_dirige(cas, point) for point in points]
    # Then — τ = x/U à la précision machine, sur toute la grille.
    assert len(points) == 12
    for point, tau in zip(points, taus, strict=True):
        assert tau == pytest.approx(point.x / cas.source.u, rel=1e-12)


def test_le_temps_dirige_est_inchange_par_l_ecart_lateral() -> None:
    """L'écart transversal n'est pas facturé : τ ne dépend que de x (docs/48 §2.6)."""
    # Given — trois points du même arc, d'écart latéral différent.
    cas = CAS_REFERENCE_DEFAUT
    # When — le temps dirigé est évalué sur l'arc.
    tau_centre = temps_dirige(cas, PointMesure(x=400.0, y=0.0, z=1.5))
    # Then — le temps dirigé est identique sur tout l'arc.
    for y in (-50.0, 50.0):
        assert temps_dirige(cas, PointMesure(x=400.0, y=y, z=1.5)) == pytest.approx(tau_centre)


def test_le_temps_dirige_rejete_l_amont() -> None:
    """Un point en amont reçoit le coût dirigé +inf (convention docs/48 §2.6)."""
    # Given — une cible en amont de la source.
    cas = CAS_REFERENCE_DEFAUT
    point = PointMesure(x=-100.0, y=0.0, z=1.5)
    # When — le temps dirigé est évalué.
    tau = temps_dirige(cas, point)
    # Then — le coût est infini : la cible n'est pas atteignable.
    assert math.isinf(tau)
    assert tau > 0.0


def test_l_evaluation_dirigee_rejoint_la_verite_du_cas() -> None:
    """L'évaluation via τ coïncide avec la vérité S0 (cas uniforme, note 37)."""
    # Given — le cas de référence, sa grille et sa vérité exacte.
    cas = CAS_REFERENCE_DEFAUT
    points = cas.points()
    verite = cas.verite(points)
    # When — la reconstruction évalue la grille via le temps dirigé.
    evaluations = evaluer_grille(cas)
    # Then — chaque évaluation rejoint la vérité et reste strictement positive.
    assert len(evaluations) == len(points)
    for evaluation, attendu in zip(evaluations, verite, strict=True):
        assert evaluation.x_aval == pytest.approx(evaluation.point.x, rel=1e-12)
        assert evaluation.concentration == pytest.approx(attendu, rel=1e-12)
        assert evaluation.concentration > 0.0


def test_evaluer_point_rejete_un_point_amont() -> None:
    """L'évaluation refuse une cible amont : le mécanisme dirigé ne l'atteint pas."""
    # Given — une cible en amont de la source.
    cas = CAS_REFERENCE_DEFAUT
    point = PointMesure(x=-100.0, y=0.0, z=1.5)
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="amont"):
        evaluer_point(cas, point)


def test_les_evaluations_sont_immuables() -> None:
    """Les évaluations dirigées ne peuvent pas être modifiées après construction."""
    # Given — une évaluation sur la grille.
    evaluation = evaluer_grille(CAS_REFERENCE_DEFAUT)[0]
    # When / Then — toute mutation est refusée.
    with pytest.raises(FrozenInstanceError):
        evaluation.tau = 1.0


def test_le_manifeste_etiquette_heritage_reconstruction_extension() -> None:
    """Le manifeste sépare l'héritage documentaire, la reconstruction et l'extension."""
    # Given — une reconstruction complète du cas de référence.
    cas = CAS_REFERENCE_DEFAUT
    manifeste = construire_manifeste(cas, evaluer_grille(cas))
    # Then — les trois étiquettes sont explicites et documentées.
    assert manifeste.identifiant == "jdriftx-baseline-uniforme-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert "annoncée seulement" in manifeste.heritage_documentaire
    assert "pseudo_distance_uniforme" in manifeste.reconstruction
    assert "concentration_panache" in manifeste.reconstruction
    assert manifeste.extension.startswith("Aucune")
    assert manifeste.hypothese
    assert manifeste.limites
    assert manifeste.cas is cas
    assert manifeste.version_code != ""
    assert "uv run" in manifeste.commande


def test_le_manifeste_exporte_un_dict_pour_la_frontiere_json() -> None:
    """vers_dict produit un export plat, sans objet du domaine imbriqué."""
    # Given — un manifeste construit.
    cas = CAS_REFERENCE_DEFAUT
    manifeste = construire_manifeste(cas, evaluer_grille(cas))
    # When — l'export frontière est produit.
    export = manifeste.vers_dict()
    # Then — clés, paramètres figés et 12 résultats sont présents.
    assert export["identifiant"] == "jdriftx-baseline-uniforme-001"
    assert export["parametres"]["classe"] == "C"
    assert export["parametres"]["arcs"] == [100.0, 200.0, 400.0, 800.0]
    assert len(export["resultats"]) == 12
    assert isinstance(export["limites"], list)
    for valeur in export.values():
        assert not isinstance(valeur, (EvaluationDirigee,))


def test_le_manifeste_signale_une_version_non_installee(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Si le paquet n'est pas installé, le manifeste le dit au lieu d'échouer."""
    # Given — un environnement où importlib.metadata ne trouve pas « jdriftx ».

    def _version_introuvable(nom: str) -> str:
        raise metadata.PackageNotFoundError(nom)

    monkeypatch.setattr(module_baseline.metadata, "version", _version_introuvable)
    # When — le manifeste est construit dans cet environnement.
    cas = CAS_REFERENCE_DEFAUT
    manifeste = construire_manifeste(cas, evaluer_grille(cas))
    # Then — la version est explicitement marquée « non-installe ».
    assert manifeste.version_code == "non-installe"
