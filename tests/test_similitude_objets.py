"""Tests de l'API objet pour les evaluations ponctuelles de similitude."""

import math

import hypothesis
import numpy as np
import pytest

from jdriftx.similitude import concentration_panache, concentration_puff
from jdriftx.similitude_objets import (
    ParametresPuff,
    Point3D,
    concentration_panache_au_point,
    concentration_puff_au_point,
)
from jdriftx.source import SourcePanache
from jdriftx.stabilite import ClasseStabilite


def test_panache_objet_coherent_avec_api_vectorisee() -> None:
    """L'API objet delegue au noyau numerique sans modifier le resultat."""
    point = Point3D(x=500.0, y=0.0, z=1.5)
    source = SourcePanache(debit=2.0, u=3.0, classe="C", hauteur=1.0)

    obtenu = concentration_panache_au_point(point, source)

    attendu = concentration_panache(
        point.x,
        point.y,
        point.z,
        debit=source.debit,
        u=source.u,
        classe=ClasseStabilite(source.classe).value,
        hauteur=source.hauteur,
    )
    assert math.isfinite(obtenu)
    assert obtenu == pytest.approx(float(attendu))


def test_puff_objet_coherent_avec_api_vectorisee() -> None:
    """L'API objet accepte un point 3D et des parametres immuables."""
    point = Point3D(x=1500.0, y=10.0, z=5.0)
    parametres = ParametresPuff(t=500.0, masse=10.0, u=3.0, classe=ClasseStabilite.C)

    obtenu = concentration_puff_au_point(point, parametres)

    attendu = concentration_puff(
        point.x,
        point.y,
        point.z,
        t=parametres.t,
        masse=parametres.masse,
        u=parametres.u,
        classe=ClasseStabilite(parametres.classe).value,
        x0=parametres.x0,
    )
    assert math.isfinite(obtenu)
    assert obtenu == pytest.approx(float(attendu))


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
        ({"t": 0.0, "masse": 1.0, "u": 2.0, "classe": "D"}, "temps"),
        ({"t": 1.0, "masse": -1.0, "u": 2.0, "classe": "D"}, "masse"),
        ({"t": 1.0, "masse": 1.0, "u": 0.0, "classe": "D"}, "vitesse"),
        ({"t": 1.0, "masse": 1.0, "u": 2.0, "classe": "Z"}, "Classe de stabilite"),
    ],
)
def test_parametres_puff_valident_les_invariants(kwargs: dict[str, object], message: str) -> None:
    """Les paramètres du puff valident temps, masse, vent et classe."""
    with pytest.raises(ValueError, match=message):
        ParametresPuff(**kwargs)  # type: ignore[arg-type]


@hypothesis.given(
    x=hypothesis.strategies.floats(
        min_value=-10_000.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    y=hypothesis.strategies.floats(
        min_value=-10_000.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    z=hypothesis.strategies.floats(
        min_value=-1_000.0, max_value=1_000.0, allow_nan=False, allow_infinity=False
    ),
)
def test_point3d_accepte_toutes_coordonnees_finies_dans_le_domaine(
    x: float, y: float, z: float
) -> None:
    """Given des coordonnées finies, when le point est construit, then il les conserve."""
    point = Point3D(x=x, y=y, z=z)

    assert (point.x, point.y, point.z) == (x, y, z)


@hypothesis.given(
    x=hypothesis.strategies.floats(
        min_value=-10_000.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    y=hypothesis.strategies.floats(
        min_value=-10_000.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    z=hypothesis.strategies.floats(
        min_value=-1_000.0, max_value=1_000.0, allow_nan=False, allow_infinity=False
    ),
    t=hypothesis.strategies.floats(
        min_value=1.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    masse=hypothesis.strategies.floats(
        min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
    ),
    u=hypothesis.strategies.floats(
        min_value=0.1, max_value=20.0, allow_nan=False, allow_infinity=False
    ),
    classe=hypothesis.strategies.sampled_from(list(ClasseStabilite)),
    x0=hypothesis.strategies.floats(
        min_value=-1_000.0, max_value=1_000.0, allow_nan=False, allow_infinity=False
    ),
)
def test_puff_objet_equivaut_au_noyau_pour_entrees_valides(
    x: float,
    y: float,
    z: float,
    t: float,
    masse: float,
    u: float,
    classe: ClasseStabilite,
    x0: float,
) -> None:
    """Given un puff valide, when les deux API calculent, then elles concordent."""
    point = Point3D(x=x, y=y, z=z)
    parametres = ParametresPuff(t=t, masse=masse, u=u, classe=classe, x0=x0)

    obtenu = concentration_puff_au_point(point, parametres)
    attendu = concentration_puff(
        x=x,
        y=y,
        z=z,
        t=t,
        masse=masse,
        u=u,
        classe=classe.value,
        x0=x0,
    )

    assert math.isfinite(obtenu)
    assert obtenu == pytest.approx(float(attendu), rel=1e-12, abs=0.0)


@hypothesis.given(
    t=hypothesis.strategies.floats(
        min_value=1.0, max_value=10_000.0, allow_nan=False, allow_infinity=False
    ),
    u=hypothesis.strategies.floats(
        min_value=0.1, max_value=20.0, allow_nan=False, allow_infinity=False
    ),
    masse=hypothesis.strategies.floats(
        min_value=0.01, max_value=100.0, allow_nan=False, allow_infinity=False
    ),
    facteur=hypothesis.strategies.floats(
        min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False
    ),
    classe=hypothesis.strategies.sampled_from(list(ClasseStabilite)),
)
def test_puff_est_lineaire_en_masse(
    t: float, u: float, masse: float, facteur: float, classe: ClasseStabilite
) -> None:
    """Given deux masses proportionnelles, when calculées, then C est proportionnelle."""
    point = Point3D(x=u * t, y=0.0, z=0.0)
    initial = ParametresPuff(t=t, masse=masse, u=u, classe=classe)
    multiplie = ParametresPuff(t=t, masse=masse * facteur, u=u, classe=classe)

    c_initiale = concentration_puff_au_point(point, initial)
    c_multipliee = concentration_puff_au_point(point, multiplie)

    assert c_multipliee == pytest.approx(c_initiale * facteur, rel=1e-12, abs=0.0)


@pytest.mark.parametrize(
    ("champ", "valeur"),
    [
        ("t", math.nan),
        ("t", math.inf),
        ("masse", math.inf),
        ("u", math.nan),
        ("x0", math.inf),
    ],
)
def test_parametres_puff_refusent_les_valeurs_non_finies(champ: str, valeur: float) -> None:
    """Given un paramètre non fini, when construit, then l'objet le refuse."""
    valeurs: dict[str, object] = {
        "t": 1.0,
        "masse": 1.0,
        "u": 2.0,
        "classe": ClasseStabilite.D,
        "x0": 0.0,
    }
    valeurs[champ] = valeur

    with pytest.raises(ValueError, match=r"fini|finie|strictement"):
        ParametresPuff(**valeurs)  # type: ignore[arg-type]


def test_parametres_puff_normalisent_la_classe_et_sont_immuables() -> None:
    """Given une classe textuelle valide, when construite, then enum et immutabilité."""
    parametres = ParametresPuff(t=1.0, masse=1.0, u=2.0, classe="D")

    assert parametres.classe is ClasseStabilite.D
    with pytest.raises(AttributeError):
        parametres.t = 2.0  # type: ignore[misc]


def test_puff_objet_rejete_la_distance_parcourue_non_finie() -> None:
    """Given t et u finis dont le produit u*t deborde, when le noyau evalue, then refus."""
    point = Point3D(x=1.0, y=0.0, z=0.0)
    parametres = ParametresPuff(t=1.0e200, masse=1.0, u=1.0e200, classe=ClasseStabilite.D)

    with pytest.raises(ValueError, match="distance parcourue doit rester finie"):
        concentration_puff_au_point(point, parametres)


def test_objets_et_noyau_gardent_chacune_leur_frontiere_non_finie() -> None:
    """L'API objet refuse les scalaires non finis ; le noyau refuse les grilles."""
    # Given — un point non fini pour la couche objet, une grille non finie
    # pour le noyau vectorise.
    # When / Then — chaque couche leve son propre message de refus.
    with pytest.raises(ValueError, match="coordonnees.*finies"):
        Point3D(x=float("nan"), y=0.0, z=0.0)
    with pytest.raises(ValueError, match="coordonnees finies"):
        concentration_panache(
            500.0,
            np.array([float("inf")]),
            1.0,
            debit=1.0,
            u=3.0,
            classe=ClasseStabilite.D,
        )
