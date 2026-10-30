"""Tests de cohérence : les booléens ne sont pas des scalaires physiques."""

from dataclasses import replace

import numpy as np
import pytest

from jdriftx.benchmarks.cas import CasS0, PointMesure
from jdriftx.experiences.cas_synthetiques import (
    CAS_S0_DEFAUT,
    DatasetS0,
    generer_dataset_s0,
)
from jdriftx.similitude_objets import ParametresPuff, Point3D
from jdriftx.stabilite import ClasseStabilite


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("coord", ["x", "y", "z"])
def test_point3d_refuse_les_coordonnees_booleennes(booleen: bool, coord: str) -> None:
    valeurs = {"x": 1.0, "y": 2.0, "z": 3.0}
    valeurs[coord] = booleen
    with pytest.raises(ValueError, match="booleens exclus"):
        Point3D(**valeurs)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["t", "masse", "u", "x0"])
def test_parametres_puff_refusent_les_booleens(booleen: bool, champ: str) -> None:
    valeurs: dict[str, object] = {
        "t": 1.0,
        "masse": 1.0,
        "u": 2.0,
        "classe": ClasseStabilite.D,
        "x0": 0.0,
    }
    valeurs[champ] = booleen
    with pytest.raises(ValueError, match="booleens exclus"):
        ParametresPuff(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("coord", ["x", "y", "z"])
def test_point_mesure_refuse_les_coordonnees_booleennes(booleen: bool, coord: str) -> None:
    valeurs = {"x": 100.0, "y": 0.0, "z": 1.0}
    valeurs[coord] = booleen
    with pytest.raises(ValueError, match="booleens exclus"):
        PointMesure(**valeurs)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["z_mesure", "arcs", "positions_laterales"])
def test_cas_s0_refuse_les_parametres_booleens(booleen: bool, champ: str) -> None:
    cas = CasS0(
        source=CAS_S0_DEFAUT.source,
        arcs=(100.0, 200.0),
        positions_laterales=(-10.0, 10.0),
        z_mesure=1.0,
    )
    valeur: object
    if champ == "arcs":
        valeur = (100.0, booleen)
    elif champ == "positions_laterales":
        valeur = (booleen,)
    else:
        valeur = booleen
    with pytest.raises(ValueError, match="booleens exclus"):
        replace(cas, **{champ: valeur})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["altitude", "x_min", "x_max", "y_max"])
def test_cas_synthetique_s0_refuse_les_parametres_booleens(
    booleen: bool, champ: str
) -> None:
    with pytest.raises(ValueError, match="booleens exclus"):
        replace(CAS_S0_DEFAUT, **{champ: booleen})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["graine", "nombre_points"])
def test_cas_synthetique_s0_refuse_les_entiers_booleens(
    booleen: bool, champ: str
) -> None:
    with pytest.raises(ValueError, match="entier"):
        replace(CAS_S0_DEFAUT, **{champ: booleen})


def test_cas_synthetique_s0_refuse_un_nombre_de_points_non_entier() -> None:
    with pytest.raises(ValueError, match="entier"):
        replace(CAS_S0_DEFAUT, nombre_points=2.5)


@pytest.mark.parametrize(
    "valeurs",
    [
        np.array([True, False]),
        [1.0, True],
        np.array([1.0, True], dtype=object),
    ],
)
def test_dataset_s0_refuse_les_tableaux_booleens_avant_conversion(valeurs: object) -> None:
    jeu = generer_dataset_s0(CAS_S0_DEFAUT)
    with pytest.raises(ValueError, match="booleens exclus"):
        DatasetS0(
            cas=jeu.cas,
            points_x=valeurs,  # type: ignore[arg-type]
            points_y=jeu.points_y,
            concentrations=jeu.concentrations,
            partition=jeu.partition,
        )
