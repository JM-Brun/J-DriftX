"""Régressions P0 : métriques, trajectoires et explorateur excluent les booléens."""

import numpy as np
import pytest

from jdriftx import metric, trajectories
from jdriftx.figures.wind_field_explorer import WindFieldExplorerConfig


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["a", "b", "vitesse"])
def test_temps_premiere_arrivee_refuse_les_scalaires_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les positions et la vitesse de la métrique 1D excluent les booléens."""
    # Given — un scalaire de l'arrivée 1D remplacé par un booléen.
    valeurs: dict[str, object] = {"a": 0.0, "b": 10.0, "vitesse": 2.0}
    valeurs[champ] = booleen
    # When / Then — le calcul du temps refuse l'entrée avant l'arithmétique.
    with pytest.raises(ValueError, match="booleens exclus"):
        metric.temps_premiere_arrivee_1d(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([[True, False], [False, True]]),
        [[0.0, 0.0], [1.0, True]],
        np.array([[0.0, 0.0], [1.0, True]], dtype=object),
    ],
)
@pytest.mark.parametrize("champ", ["ligne", "vent"])
def test_temps_transport_refuse_les_tableaux_booleens(valeur: object, champ: str) -> None:
    """La polyligne et le vent excluent les booléens avant coercition."""
    # Given — une polyligne ou un tableau de vents contenant un booléen.
    ligne: object = np.array([[0.0, 0.0], [1.0, 0.0]])
    vent: object = np.array([[1.0, 0.0]])
    if champ == "ligne":
        ligne = valeur
    else:
        vent = valeur
    # When / Then — le coût de transport refuse l'entrée.
    with pytest.raises(ValueError, match="booleens exclus"):
        metric.temps_transport(ligne, vent)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_temps_transport_refuse_umin_booleen(booleen: bool | np.bool_) -> None:
    """Le seuil minimal de vitesse exclut les booléens."""
    # Given — une ligne et un vent valides avec un seuil booléen.
    ligne = np.array([[0.0, 0.0], [1.0, 0.0]])
    vent = np.array([[2.0, 0.0]])
    # When / Then — le seuil est refusé avant la comparaison.
    with pytest.raises(ValueError, match="booleens exclus"):
        metric.temps_transport(ligne, vent, umin=booleen)


@pytest.mark.parametrize(
    "valeur",
    [
        np.array([True, False]),
        [0.0, True],
        np.array([0.0, True], dtype=object),
    ],
)
@pytest.mark.parametrize("champ", ["a", "b", "vent"])
def test_pseudo_distance_uniforme_refuse_les_tableaux_booleens(valeur: object, champ: str) -> None:
    """Les deux points et le vent uniforme excluent les booléens avant coercition."""
    # Given — un point ou un vecteur de vent contenant un booléen.
    a: object = np.zeros(2)
    b: object = np.array([1.0, 0.0])
    vent: object = np.array([2.0, 0.0])
    if champ == "a":
        a = valeur
    elif champ == "b":
        b = valeur
    else:
        vent = valeur
    # When / Then — la pseudo-distance refuse l'entrée.
    with pytest.raises(ValueError, match="booleens exclus"):
        metric.pseudo_distance_uniforme(a, b, vent)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["x0", "y0", "t0", "t_end", "dt"])
def test_integrateur_refuse_les_conditions_initiales_booleennes(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les coordonnées initiales et paramètres de temps excluent les booléens."""
    # Given — une condition initiale ou un pas remplacé par un booléen.
    valeurs: dict[str, object] = {
        "x0": 0.0,
        "y0": 0.0,
        "t0": 0.0,
        "t_end": 1.0,
        "dt": 0.1,
    }
    valeurs[champ] = booleen
    # When / Then — l'intégrateur refuse l'entrée avant le premier appel de vitesse.
    with pytest.raises(ValueError, match="booleans excluded"):
        trajectories.integrate_trajectory(lambda _t, _x, _y: (1.0, 0.0), **valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    ["speed", "angle_deg", "shear", "radial_strength", "probe_x", "probe_y"],
)
def test_explorateur_refuse_les_parametres_booleens(booleen: bool | np.bool_, champ: str) -> None:
    """Les paramètres et coordonnées de lecture de l'explorateur excluent les booléens."""
    # Given — un champ de la configuration remplacé par un booléen.
    valeurs: dict[str, object] = {
        "family": "Uniforme",
        "speed": 1.0,
        "angle_deg": 0.0,
        "shear": 0.0,
        "radial_strength": 1.0,
        "probe_x": 0.0,
        "probe_y": 0.0,
    }
    valeurs[champ] = booleen
    # When / Then — la configuration est refusée avant le rendu SVG.
    with pytest.raises(ValueError, match="booléens exclus"):
        WindFieldExplorerConfig(**valeurs)  # type: ignore[arg-type]
