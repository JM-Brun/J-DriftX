"Tests de l'oracle scalaire indépendant pour l'étape 5."""

import math

import pytest

from jdriftx.benchmarks.cas import CAS_S0_DEFAUT
from jdriftx.source import SourcePanache
from scripts.benchmark_baseline_uniforme import (
    TOLERANCE_ABSOLUE,
    TOLERANCE_RELATIVE,
    executer,
    oracle_concentration,
)


def test_oracle_est_positif_sur_les_12_points_s0() -> None:
    """L'oracle est défini et positif sur la grille S0 figée."""
    cas = CAS_S0_DEFAUT
    valeurs = [oracle_concentration(point, cas.source) for point in cas.points()]
    assert len(valeurs) == 12
    assert all(math.isfinite(valeur) and valeur > 0.0 for valeur in valeurs)


def test_oracle_refuse_les_classes_non_specifiees() -> None:
    """L'oracle n'étend pas silencieusement sa formule au-delà de la classe C."""
    source = SourcePanache(debit=2.0, u=3.0, classe="D", hauteur=1.0)
    with pytest.raises(ValueError, match="classe C"):
        oracle_concentration(CAS_S0_DEFAUT.points()[0], source)


def test_comparaison_reproductible_rejoint_la_tolerance_numerique() -> None:
    """La formule indépendante rejoint le pipeline dans la tolérance préfixée."""
    rapport = executer(repetitions=5)
    precision = rapport["accuracy"]
    assert precision["all_within_tolerance"]
    assert precision["max_absolute_error_kg_m3"] <= (
        TOLERANCE_ABSOLUE
        + TOLERANCE_RELATIVE
        * max(point["oracle_kg_m3"] for point in precision["points"])
    )
    assert rapport["cost"]["per_query_median_ms_baseline"] > 0.0
    assert rapport["cost"]["per_query_median_ms_oracle"] > 0.0
