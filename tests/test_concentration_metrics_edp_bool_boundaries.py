"""Régressions P0 : champs de concentration, métriques et grille EDP excluent les booléens."""

import numpy as np
import pytest

from jdriftx.benchmarks.metriques import calculer_metriques, fac2, nmse
from jdriftx.constraints import positivite
from jdriftx.experiences.reference_independante import GrilleEdp, ParametresEdp, TrancheEdp


@pytest.mark.parametrize(
    "valeur",
    [np.array([True, False]), [0.0, True], np.array([0.0, True], dtype=object)],
)
def test_positivite_refuse_les_concentrations_booleennes(valeur: object) -> None:
    """Un champ booléen ne constitue pas un tableau de concentrations réelles."""
    with pytest.raises(ValueError, match="booleens exclus"):
        positivite(valeur)  # type: ignore[arg-type]


@pytest.mark.parametrize("metrique", [fac2, nmse])
@pytest.mark.parametrize("champ", ["verite", "prediction"])
@pytest.mark.parametrize(
    "valeur",
    [np.array([True, False]), [1.0, True], np.array([1.0, True], dtype=object)],
)
def test_metriques_refusent_les_vecteurs_booleens(metrique, champ: str, valeur: object) -> None:
    """FAC2 et NMSE refusent les booléens avant coercition des observations."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = valeur
    else:
        prediction = valeur
    with pytest.raises(ValueError, match="booleens exclus"):
        metrique(verite, prediction)


@pytest.mark.parametrize("champ", ["verite", "prediction"])
def test_calculer_metriques_refuse_les_vecteurs_booleens(champ: str) -> None:
    """La façade d'évaluation valide avant sa propre conversion en float64."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = np.array([True, False])
    else:
        prediction = np.array([True, False])
    with pytest.raises(ValueError, match="booleens exclus"):
        calculer_metriques(verite, prediction)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["abscisses_y", "abscisses_z"])
@pytest.mark.parametrize("valeur", [np.array([True, False]), np.array([0.0, True], dtype=object)])
def test_grille_edp_refuse_les_axes_booleens(champ: str, valeur: np.ndarray) -> None:
    """Les axes EDP excluent les tableaux booléens avant leur normalisation."""
    axes: dict[str, object] = {
        "abscisses_y": np.array([-1.0, 0.0, 1.0]),
        "abscisses_z": np.array([0.0, 1.0]),
    }
    axes[champ] = valeur
    with pytest.raises(ValueError, match="booleens exclus"):
        GrilleEdp(**axes)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "valeur",
    [np.array([[True, False], [False, True]]), np.array([[0.0, True]], dtype=object)],
)
def test_tranche_edp_refuse_un_champ_booleen(valeur: np.ndarray) -> None:
    """Le champ d'une tranche EDP exclut les booléens avant copie immuable."""
    with pytest.raises(ValueError, match="booleens exclus"):
        TrancheEdp(x=100.0, champ=valeur)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ", ["pas_transverse_y", "pas_transverse_z", "demi_largeur_y", "hauteur_max"]
)
def test_parametres_edp_refusent_les_scalaires_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les quatre paramètres géométriques EDP excluent les booléens."""
    valeurs: dict[str, float | bool | np.bool_] = {
        "pas_transverse_y": 2.5,
        "pas_transverse_z": 2.0,
        "demi_largeur_y": 340.0,
        "hauteur_max": 240.0,
    }
    if champ == "demi_largeur_y":
        valeurs["pas_transverse_y"] = 2.0
    if champ == "hauteur_max":
        valeurs["pas_transverse_z"] = 1.0
    valeurs[champ] = booleen
    with pytest.raises(ValueError, match="booléens exclus"):
        ParametresEdp(**valeurs)  # type: ignore[arg-type]
