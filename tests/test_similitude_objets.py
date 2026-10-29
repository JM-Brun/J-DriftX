"""Tests de l'API objet pour les evaluations ponctuelles de similitude."""

import math

import pytest

from jdriftx.similitude_objets import (
    ParametresPanache,
    ParametresPuff,
    Point3D,
    concentration_panache_au_point,
    concentration_puff_au_point,
)
from jdriftx.stabilite import ClasseStabilite


def test_panache_objet_coherent_avec_api_vectorisee() -> None:
    """L'API objet delegue au noyau numerique sans modifier le resultat."""
    point = Point3D(x=500.0, y=0.0, z=1.5)
    parametres = ParametresPanache(
        debit=2.0, u=3.0, classe=ClasseStabilite.C, hauteur=1.0
    )

    obtenu = concentration_panache_au_point(point, parametres)

    assert math.isfinite(obtenu)
    assert obtenu > 0.0


def test_puff_objet_coherent_avec_api_vectorisee() -> None:
    """L'API objet accepte un point 3D et des parametres immuables."""
    point = Point3D(x=1500.0, y=10.0, z=5.0)
    parametres = ParametresPuff(
        t=500.0, masse=10.0, u=3.0, classe=ClasseStabilite.C
    )

    obtenu = concentration_puff_au_point(point, parametres)

    assert math.isfinite(obtenu)
    assert obtenu > 0.0


@pytest.mark.parametrize(
    ("coords", "message"),
    [
        ((math.nan, 0.0, 0.0), "coordonnees.*finies"),
        ((0.0, math.inf, 0.0), "coordonnees.*finies"),
    ],
)
def test_point3d_refuse_coordonnees_non_finies(
    coords: tuple[float, float, float], message: str
) -> None:
    """Les coordonnées non finies sont rejetées à la frontière de l'API."""
    with pytest.raises(ValueError, match=message):
        Point3D(*coords)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"debit": -1.0, "u": 2.0, "classe": "D"}, "debit"),
        ({"debit": 1.0, "u": 0.0, "classe": "D"}, "vitesse"),
        ({"debit": 1.0, "u": 2.0, "classe": "Z"}, "Classe de stabilite"),
    ],
)
def test_parametres_panache_valident_les_invariants(
    kwargs: dict[str, object], message: str
) -> None:
    """Les paramètres invalides sont refusés avant l'évaluation numérique."""
    with pytest.raises(ValueError, match=message):
        ParametresPanache(**kwargs)  # type: ignore[arg-type]


def test_parametres_normalisent_la_classe_en_enum() -> None:
    """La chaîne historique est normalisée vers l'objet classe unique."""
    parametres = ParametresPanache(debit=1.0, u=2.0, classe="D")

    assert parametres.classe is ClasseStabilite.D


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"t": 0.0, "masse": 1.0, "u": 2.0, "classe": "D"}, "temps"),
        ({"t": 1.0, "masse": -1.0, "u": 2.0, "classe": "D"}, "masse"),
        ({"t": 1.0, "masse": 1.0, "u": 0.0, "classe": "D"}, "vitesse"),
        ({"t": 1.0, "masse": 1.0, "u": 2.0, "classe": "Z"}, "Classe de stabilite"),
    ],
)
def test_parametres_puff_valident_les_invariants(
    kwargs: dict[str, object], message: str
) -> None:
    """Les paramètres du puff valident temps, masse, vent et classe."""
    with pytest.raises(ValueError, match=message):
        ParametresPuff(**kwargs)  # type: ignore[arg-type]
