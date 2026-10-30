"""Tests de la famille de cas synthétiques S0 (docs/21)."""

import json
from dataclasses import FrozenInstanceError, replace

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
    DatasetS0,
    VERSION_GENERATEUR,
)
from jdriftx.source import SourcePanache


def _cas_valide() -> CasSynthetiqueS0:
    """Retourne un cas S0 valide, à modifier dans les rejets."""
    return CasSynthetiqueS0(
        identifiant="jdriftx-s0-test",
        source=SourcePanache(classe="D", debit=1.0, u=3.0, hauteur=10.0),
        altitude=2.0,
        graine=42,
        nombre_points=20,
        x_min=50.0,
        x_max=5000.0,
        y_max=200.0,
    )


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
    # Then — identifiant, version, clause et source sont présents et sérialisables.
    assert manifeste["identifiant"] == CAS_S0_DEFAUT.identifiant
    assert manifeste["version_generateur"] == VERSION_GENERATEUR
    assert manifeste["clause"] == CLAUSE_NON_VALIDATION
    assert manifeste["cas"]["classe"] == CAS_S0_DEFAUT.source.classe
    assert manifeste["cas"]["debit"] == CAS_S0_DEFAUT.source.debit
    assert manifeste["cas"]["u"] == CAS_S0_DEFAUT.source.u
    assert manifeste["cas"]["hauteur"] == CAS_S0_DEFAUT.source.hauteur
    json.dumps(manifeste)


def test_cas_immuable() -> None:
    """La configuration d'un cas S0 ne peut pas être modifiée après construction."""
    # Given — le cas par défaut.
    # When / Then — toute mutation est refusée (dataclass figée).
    with pytest.raises(FrozenInstanceError):
        CAS_S0_DEFAUT.graine = 43  # type: ignore[misc]


@pytest.mark.parametrize(
    ("champ", "valeur", "message_attendu"),
    [
        ("identifiant", "", "non vide"),
        ("nombre_points", 1, "2 points"),
        ("x_min", 0.0, "x_min"),
        ("y_max", 0.0, "y_max"),
    ],
)
def test_refuse_configurations_de_cas_invalides(champ, valeur, message_attendu) -> None:
    """Un paramètre propre au cas invalide est refusé à la construction."""
    # Given — un cas de référence valide.
    cas = _cas_valide()
    # When — un paramètre du cas est rendu invalide.
    # Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        replace(cas, **{champ: valeur})


@pytest.mark.parametrize(
    ("champ", "valeur", "message_attendu"),
    [
        ("debit", 0.0, "debit"),
        ("u", 0.0, "vent"),
        ("hauteur", -1.0, "hauteur"),
        ("classe", "Z", "Z"),
    ],
)
def test_refuse_sources_invalides(champ, valeur, message_attendu) -> None:
    """Une source invalide est refusée à la construction du cas (docs/41).

    Le partage de la valeur source valide désormais la classe de stabilité
    à la construction : l'écart documenté en docs/41 est comblé.
    """
    # Given — un cas de référence valide.
    cas = _cas_valide()
    # When — un champ de la source est rendu invalide.
    # Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        replace(cas, source=replace(cas.source, **{champ: valeur}))



def test_dataset_copie_et_fige_ses_tableaux() -> None:
    """Un DatasetS0 ne partage pas de tableaux mutables avec son appelant."""
    # Given — un jeu S0 et un tableau d'abscisses fourni par l'appelant.
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    points_x = jeu.points_x.copy()
    valeur_initiale = float(points_x[0])
    # When — un nouveau dataset est construit puis le tableau source est modifié.
    copie = DatasetS0(
        cas=jeu.cas,
        points_x=points_x,
        points_y=jeu.points_y,
        concentrations=jeu.concentrations,
        partition=jeu.partition,
    )
    points_x[0] = points_x[0] + 1.0
    # Then — le dataset conserve sa valeur initiale et ses tableaux sont réellement immuables.
    assert copie.points_x[0] == valeur_initiale
    with pytest.raises(ValueError, match="read-only"):
        copie.points_x[0] = 0.0
    with pytest.raises(ValueError, match="WRITEABLE"):
        copie.points_x.setflags(write=True)


def test_dataset_refuse_des_tableaux_de_formes_differentes() -> None:
    """Les trois vecteurs d'un dataset doivent être alignés point à point."""
    # Given — un jeu valide.
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    # When / Then — une coordonnée amputée d'un point est refusée.
    with pytest.raises(ValueError, match="même forme"):
        DatasetS0(
            cas=jeu.cas,
            points_x=jeu.points_x,
            points_y=jeu.points_y[:-1],
            concentrations=jeu.concentrations,
            partition=jeu.partition,
        )


def test_configuration_s0_refuse_les_scalaires_non_finis() -> None:
    """Les paramètres physiques finis sont exigés dès la construction."""
    # Given — des configurations contenant NaN ou infini.
    # When / Then — chaque paramètre scalaire non fini est refusé.
    with pytest.raises(ValueError, match="finis"):
        replace(_cas_valide(), altitude=float("nan"))
    with pytest.raises(ValueError, match="finis"):
        replace(_cas_valide(), y_max=float("inf"))
