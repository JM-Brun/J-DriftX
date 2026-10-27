"""Tests de la famille de cas synthétiques S0 (docs/21)."""

import json
from dataclasses import FrozenInstanceError

import numpy as np
import pytest

from jdriftx.experiences import (
    CasSynthetiqueS0,
    construire_partition,
    generer_dataset_s0,
)
from jdriftx.experiences.cas_synthetiques import (
    CAS_S0_DEFAUT,
    CLAUSE_NON_VALIDATION,
    VERSION_GENERATEUR,
)


def _configuration_valide() -> dict[str, object]:
    """Retourne une configuration de cas S0 valide, à modifier dans les rejets."""
    return {
        "identifiant": "jdriftx-s0-test",
        "classe": "D",
        "debit": 1.0,
        "u": 3.0,
        "hauteur": 10.0,
        "altitude": 2.0,
        "graine": 42,
        "nombre_points": 20,
        "x_min": 50.0,
        "x_max": 5000.0,
        "y_max": 200.0,
    }


def test_generation_deterministe() -> None:
    """Deux générations avec la même graine produisent des jeux identiques."""
    # Given — le cas S0 par défaut, généré deux fois.
    premier = generer_dataset_s0(CAS_S0_DEFAUT)
    second = generer_dataset_s0(CAS_S0_DEFAUT)
    # When / Then — points, vérités et partition sont identiques bit à bit.
    assert np.array_equal(premier.points_x, second.points_x)
    assert np.array_equal(premier.points_y, second.points_y)
    assert np.array_equal(premier.concentrations, second.concentrations)
    assert premier.partition == second.partition


def test_partition_disjointe_et_couvrante() -> None:
    """La partition figée sépare calibration et évaluation sans trou ni doublon."""
    # Given — un jeu généré à partir du cas par défaut (200 points).
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    # When — on réunit les deux parties d'indices.
    reunion = sorted(jeu.partition.calibration + jeu.partition.evaluation)
    # Then — la réunion couvre tous les indices, en proportions 70/30.
    assert reunion == list(range(CAS_S0_DEFAUT.nombre_points))
    assert len(jeu.partition.calibration) == 140
    assert len(jeu.partition.evaluation) == 60


def test_partition_deterministe_et_sensible_a_la_graine() -> None:
    """Même graine : partition identique ; graine différente : partition changée."""
    # Given — trois partitions construites avec deux graines différentes.
    premiere = construire_partition(50, 1)
    meme_graine = construire_partition(50, 1)
    autre_graine = construire_partition(50, 2)
    # When / Then — la graine fixe la partition et la change lorsqu'elle change.
    assert premiere == meme_graine
    assert premiere != autre_graine


def test_concentrations_positives_et_finies() -> None:
    """Les vérités S0 du panache gaussien sont positives et finies."""
    # Given — un jeu généré à partir du cas par défaut.
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    # When / Then — toutes les concentrations sont finies et strictement positives.
    assert np.all(np.isfinite(jeu.concentrations))
    assert np.all(jeu.concentrations > 0.0)


def test_manifeste_exploitable_en_json() -> None:
    """Le manifeste porte la version du générateur et la clause de non-validation."""
    # Given — un jeu généré à partir du cas par défaut.
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    # When — on exporte le manifeste.
    manifeste = jeu.vers_dict()
    # Then — identifiant, version et clause sont présents et sérialisables.
    assert manifeste["identifiant"] == CAS_S0_DEFAUT.identifiant
    assert manifeste["version_generateur"] == VERSION_GENERATEUR
    assert manifeste["clause"] == CLAUSE_NON_VALIDATION
    json.dumps(manifeste)


def test_cas_immuable() -> None:
    """La configuration d'un cas S0 ne peut pas être modifiée après construction."""
    # Given — le cas par défaut.
    # When / Then — toute mutation est refusée (dataclass figée).
    with pytest.raises(FrozenInstanceError):
        CAS_S0_DEFAUT.debit = 2.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("modifications", "message_attendu"),
    [
        ({"identifiant": ""}, "non vide"),
        ({"debit": 0.0}, "débit"),
        ({"u": 0.0}, "vent"),
        ({"hauteur": -1.0}, "hauteur"),
        ({"nombre_points": 1}, "2 points"),
        ({"x_min": 0.0}, "x_min"),
        ({"y_max": 0.0}, "y_max"),
    ],
)
def test_rejets_de_configurations_invalides(modifications, message_attendu) -> None:
    """Une configuration invalide est rejetée à la construction du cas."""
    # Given — une configuration de référence valide.
    parametres = _configuration_valide()
    # When — un paramètre est rendu invalide.
    # Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        CasSynthetiqueS0(**{**parametres, **modifications})
