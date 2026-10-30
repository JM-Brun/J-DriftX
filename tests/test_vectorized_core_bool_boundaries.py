"""Régressions P0 : les noyaux vectorisés excluent les booléens des entrées réelles."""

import numpy as np
import pytest

from jdriftx import advection_diffusion, fields, periodic_transport, terrain


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([True, False]),
        [1.0, True],
        np.array([1.0, True], dtype=object),
    ],
)
@pytest.mark.parametrize("axe", ["x", "y"])
def test_vector_field_refuse_les_coordonnees_booleennes(valeur: object, axe: str) -> None:
    """Les coordonnées booléennes sont rejetées avant la conversion en float."""
    # Given — une coordonnée booléenne, homogène ou mélangée à un réel.
    x, y = np.zeros(2), np.zeros(2)
    if axe == "x":
        x = valeur  # type: ignore[assignment]
    else:
        y = valeur  # type: ignore[assignment]
    # When / Then — le champ refuse la coordonnée avant le calcul vectorisé.
    with pytest.raises(ValueError, match="booleans excluded"):
        fields.vector_field(x, y, "uniform")  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["speed", "angle_deg", "shear", "radial_strength"])
def test_vector_field_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les quatre paramètres numériques du champ excluent les booléens."""
    # Given — un paramètre du champ remplacé par un booléen.
    parametres: dict[str, object] = {
        "speed": 1.0,
        "angle_deg": 0.0,
        "shear": 0.0,
        "radial_strength": 1.0,
    }
    parametres[champ] = booleen
    # When / Then — le champ refuse le paramètre avant toute opération trigonométrique.
    with pytest.raises(ValueError, match="booleans excluded"):
        fields.vector_field(
            np.zeros(2), np.zeros(2), "uniform", **parametres
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([True, False]),
        [1.0, True],
        np.array([1.0, True], dtype=object),
    ],
)
@pytest.mark.parametrize("axe", ["x", "y"])
def test_terrain_surface_refuse_les_coordonnees_booleennes(valeur: object, axe: str) -> None:
    """Les grilles de terrain excluent les booléens avant conversion numérique."""
    # Given — une grille contenant une coordonnée booléenne.
    x, y = np.zeros(2), np.zeros(2)
    if axe == "x":
        x = valeur  # type: ignore[assignment]
    else:
        y = valeur  # type: ignore[assignment]
    # When / Then — le terrain refuse la grille avant le calcul du relief.
    with pytest.raises(ValueError, match="booleans excluded"):
        terrain.terrain_surface(x, y, "flat")  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["height", "width", "center_x", "center_y"])
def test_terrain_surface_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les paramètres géométriques du terrain excluent les booléens."""
    # Given — un paramètre du relief remplacé par un booléen.
    parametres: dict[str, object] = {
        "height": 1.0,
        "width": 1.5,
        "center_x": 0.0,
        "center_y": 0.0,
    }
    parametres[champ] = booleen
    # When / Then — le terrain refuse le paramètre avant l'évaluation.
    with pytest.raises(ValueError, match="booleans excluded"):
        terrain.terrain_surface(
            np.zeros(2), np.zeros(2), "hill", **parametres
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([True, False]),
        [1.0, True],
        np.array([1.0, True], dtype=object),
    ],
)
def test_gaussian_advection_diffusion_refuse_les_coordonnees_booleennes(
    valeur: object,
) -> None:
    """Les coordonnées de la solution gaussienne excluent les booléens."""
    # Given — un vecteur de coordonnées booléennes ou mixte.
    # When / Then — la solution refuse l'entrée avant la conversion en float.
    with pytest.raises(ValueError, match="booleans excluded"):
        advection_diffusion.gaussian_advection_diffusion(valeur, 1.0)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    ["time", "mass", "initial_center", "velocity", "diffusivity", "initial_sigma"],
)
def test_gaussian_advection_diffusion_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les paramètres scalaires de la solution gaussienne excluent les booléens."""
    # Given — un paramètre physique remplacé par un booléen.
    parametres: dict[str, object] = {
        "mass": 1.0,
        "initial_center": 0.0,
        "velocity": 1.0,
        "diffusivity": 0.1,
        "initial_sigma": 1.0,
    }
    if champ == "time":
        temps = booleen
    else:
        parametres[champ] = booleen
        temps = 1.0
    # When / Then — la solution refuse le paramètre avant le calcul de variance.
    with pytest.raises(ValueError, match="booleans excluded"):
        advection_diffusion.gaussian_advection_diffusion(
            np.zeros(2), temps, **parametres
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([True, False]),
        [1.0, True],
        np.array([1.0, True], dtype=object),
    ],
)
def test_periodic_sine_solution_refuse_les_coordonnees_booleennes(
    valeur: object,
) -> None:
    """La solution périodique exacte exclut les coordonnées booléennes."""
    # Given — un vecteur de coordonnées booléennes ou mixte.
    # When / Then — la solution refuse la conversion numérique.
    with pytest.raises(ValueError, match="booleans excluded"):
        periodic_transport.periodic_sine_solution(
            valeur,
            0.1,
            length=1.0,
            mean_concentration=1.0,
            amplitude=0.5,
            velocity=0.4,
            diffusivity=0.01,
        )  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    ["time", "length", "mean_concentration", "amplitude", "velocity", "diffusivity"],
)
def test_periodic_sine_solution_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les paramètres de la solution périodique exacte excluent les booléens."""
    # Given — un paramètre de la solution exacte remplacé par un booléen.
    parametres: dict[str, object] = {
        "length": 1.0,
        "mean_concentration": 1.0,
        "amplitude": 0.5,
        "velocity": 0.4,
        "diffusivity": 0.01,
    }
    if champ == "time":
        temps = booleen
    else:
        parametres[champ] = booleen
        temps = 0.1
    # When / Then — la solution refuse le paramètre avant le calcul de phase.
    with pytest.raises(ValueError, match="booleans excluded"):
        periodic_transport.periodic_sine_solution(
            np.zeros(2), temps, **parametres
        )  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    ["length", "end_time", "dt", "mean_concentration", "amplitude", "velocity", "diffusivity"],
)
def test_periodic_solver_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les paramètres du solveur périodique excluent les booléens."""
    # Given — un paramètre du solveur remplacé par un booléen.
    parametres: dict[str, object] = {
        "n_cells": 16,
        "length": 1.0,
        "end_time": 0.1,
        "dt": 0.001,
        "mean_concentration": 1.0,
        "amplitude": 0.3,
        "velocity": 0.4,
        "diffusivity": 0.01,
    }
    parametres[champ] = booleen
    # When / Then — le solveur refuse l'entrée avant la création de la grille.
    with pytest.raises(ValueError, match="booleans excluded"):
        periodic_transport.solve_periodic_sine_transport(**parametres)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_periodic_solver_refuse_un_nombre_de_cellules_booleen(booleen: bool | np.bool_) -> None:
    """Le nombre de cellules exclut explicitement les booléens."""
    # Given — un nombre de cellules booléen.
    # When / Then — le solveur refuse la dimension de grille.
    with pytest.raises(ValueError, match="integer"):
        periodic_transport.solve_periodic_sine_transport(
            n_cells=booleen, length=1.0, end_time=0.1, dt=0.001
        )  # type: ignore[arg-type]
