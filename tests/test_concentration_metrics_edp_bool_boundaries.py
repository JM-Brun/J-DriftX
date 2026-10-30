"""Régressions P0 : champs de concentration, métriques et grille EDP excluent les booléens."""

import numpy as np
import pytest

from jdriftx.benchmarks.metriques import calculer_metriques, fac2, nmse
from jdriftx.benchmarks.reference import evaluer_prediction
from jdriftx.constraints import positivite
from jdriftx.experiences.reference_independante import (
    CoefficientsDiffusion,
    DiffusionBriggs,
    GrilleEdp,
    ParametresEdp,
    SolutionEdp,
    TrancheEdp,
    derivee_sigma_carre,
)


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


@pytest.mark.parametrize("champ", ["verite", "prediction"])
def test_evaluer_prediction_refuse_les_vecteurs_booleens(champ: str) -> None:
    """La façade de benchmark conserve le dtype jusqu'à la validation des métriques."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = np.array([True, False])
    else:
        prediction = np.array([True, False])
    with pytest.raises(ValueError, match="booleens exclus"):
        evaluer_prediction(verite, prediction)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_tranche_edp_refuse_une_abscisse_booleenne(booleen: bool | np.bool_) -> None:
    """L'abscisse de tranche est un scalaire réel, pas un booléen."""
    with pytest.raises(ValueError, match="booléen exclu"):
        TrancheEdp(x=booleen, champ=np.ones((2, 2)))


@pytest.mark.parametrize("champ", ["x_entree", "pas_longitudinal"])
@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_solution_edp_refuse_les_scalaires_booleens(champ: str, booleen: bool | np.bool_) -> None:
    """L'entrée et le pas de la solution EDP excluent les booléens."""
    valeurs: dict[str, object] = {
        "x_entree": 100.0,
        "pas_longitudinal": 0.5,
        "abscisses_y": np.array([-1.0, 0.0, 1.0]),
        "abscisses_z": np.array([0.0, 1.0]),
        "tranches": (TrancheEdp(x=100.0, champ=np.ones((3, 2))),),
    }
    valeurs[champ] = booleen
    with pytest.raises(ValueError, match="booléens exclus"):
        SolutionEdp(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["x", "coefficient", "d"])
@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_derivee_sigma_carre_refuse_les_scalaires_booleens(
    champ: str, booleen: bool | np.bool_
) -> None:
    """Les trois arguments de la dérivée analytique excluent les booléens."""
    valeurs: dict[str, float | bool | np.bool_] = {"x": 100.0, "coefficient": 0.08, "d": 0.0002}
    valeurs[champ] = booleen
    with pytest.raises(ValueError, match="booléens exclus"):
        derivee_sigma_carre(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["a_y", "d_y", "b_z", "d_z"])
@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_coefficients_diffusion_refusent_les_booleens(champ: str, booleen: bool | np.bool_) -> None:
    """Les coefficients de diffusion typés réels excluent les booléens."""
    valeurs: dict[str, float | bool | np.bool_] = {
        "a_y": 0.08,
        "d_y": 0.0002,
        "b_z": 0.06,
        "d_z": 0.0003,
    }
    valeurs[champ] = booleen
    with pytest.raises(ValueError, match="booléens exclus"):
        CoefficientsDiffusion(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_pas_longitudinal_refuse_un_debut_booleen(booleen: bool | np.bool_) -> None:
    """La distance initiale du pas longitudinal exclut les booléens."""
    coefficients = CoefficientsDiffusion(a_y=0.08, d_y=0.0002, b_z=0.06, d_z=0.0003)
    parametres = ParametresEdp(2.5, 2.0, 340.0, 240.0)
    with pytest.raises(ValueError, match="booléen exclu"):
        coefficients.pas_longitudinal(booleen, 800.0, parametres)


@pytest.mark.parametrize(
    ("pas_y", "pas_z", "demi_largeur", "hauteur"),
    [
        (1e-308, 2.0, 1e308, 240.0),
        (2.5, 1e-308, 340.0, 1e308),
        (1e308, 2.0, 1e-308, 240.0),
        (2.5, 1e308, 340.0, 1e-308),
    ],
)
def test_parametres_edp_refusent_les_rapports_de_grille_non_representables(
    pas_y: float, pas_z: float, demi_largeur: float, hauteur: float
) -> None:
    """Les rapports de multiplicité ne débordent ni ne sous-débordent silencieusement."""
    with pytest.raises(ValueError, match="rapport de discrétisation"):
        ParametresEdp(pas_y, pas_z, demi_largeur, hauteur)


@pytest.mark.parametrize(
    ("x", "coefficient", "d"),
    [
        (1e308, 1.0, 0.0),
        (1e-308, 1e-308, 0.0),
        (np.float64(np.inf), 1.0, 0.0),
        (100.0, 1.0, np.float64(np.nan)),
    ],
)
def test_derivee_sigma_carre_refuse_les_calculs_non_representables(
    x: float | np.float64, coefficient: float, d: float | np.float64
) -> None:
    """Les entrées non finies et les intermédiaires non représentables sont explicites."""
    with pytest.raises(ValueError, match="représentable"):
        derivee_sigma_carre(x, coefficient, d)


@pytest.mark.parametrize(
    "valeur",
    [np.array([1.0 + 2.0j]), [1.0, 1.0 + 2.0j], np.array([1.0 + 2.0j], dtype=object)],
)
def test_positivite_refuse_les_concentrations_complexes(valeur: object) -> None:
    """Un champ complexe ne peut pas être ramené silencieusement à sa partie réelle."""
    with pytest.raises(ValueError, match="complexes exclus"):
        positivite(valeur)  # type: ignore[arg-type]


@pytest.mark.parametrize("metrique", [fac2, nmse])
@pytest.mark.parametrize("champ", ["verite", "prediction"])
@pytest.mark.parametrize(
    "valeur",
    [np.array([1.0 + 2.0j]), [1.0, 1.0 + 2.0j], np.array([1.0 + 2.0j], dtype=object)],
)
def test_metriques_refusent_les_vecteurs_complexes(metrique, champ: str, valeur: object) -> None:
    """FAC2 et NMSE refusent les vecteurs complexes avant toute conversion float64."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = valeur
    else:
        prediction = valeur
    with pytest.raises(ValueError, match="complexes exclus"):
        metrique(verite, prediction)


@pytest.mark.parametrize("champ", ["verite", "prediction"])
def test_calculer_metriques_refuse_les_vecteurs_complexes(champ: str) -> None:
    """La façade d'évaluation refuse les complexes avant sa coercition float64."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = np.array([1.0 + 2.0j])
    else:
        prediction = np.array([1.0 + 2.0j])
    with pytest.raises(ValueError, match="complexes exclus"):
        calculer_metriques(verite, prediction)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["verite", "prediction"])
def test_evaluer_prediction_refuse_les_vecteurs_complexes(champ: str) -> None:
    """La façade de benchmark ne doit pas masquer la partie imaginaire."""
    verite: object = [1.0, 2.0]
    prediction: object = [1.0, 2.0]
    if champ == "verite":
        verite = np.array([1.0 + 2.0j])
    else:
        prediction = np.array([1.0 + 2.0j])
    with pytest.raises(ValueError, match="complexes exclus"):
        evaluer_prediction(verite, prediction)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["abscisses_y", "abscisses_z"])
def test_grille_edp_refuse_les_axes_complexes(champ: str) -> None:
    """Les axes d'une grille EDP sont réels et ne perdent pas leur partie imaginaire."""
    axes: dict[str, object] = {
        "abscisses_y": np.array([-1.0, 0.0, 1.0]),
        "abscisses_z": np.array([0.0, 1.0]),
    }
    axes[champ] = np.array([0.0 + 1.0j, 1.0 + 1.0j])
    with pytest.raises(ValueError, match="complexes exclus"):
        GrilleEdp(**axes)  # type: ignore[arg-type]


def test_tranche_edp_refuse_un_champ_complexe() -> None:
    """Le champ EDP est réel ; sa partie imaginaire ne doit pas être supprimée."""
    with pytest.raises(ValueError, match="complexes exclus"):
        TrancheEdp(x=100.0, champ=np.ones((2, 2), dtype=complex))


@pytest.mark.parametrize(
    "champ", ["pas_transverse_y", "pas_transverse_z", "demi_largeur_y", "hauteur_max"]
)
def test_parametres_edp_refusent_les_scalaires_complexes(champ: str) -> None:
    """Les paramètres géométriques EDP sont des scalaires réels."""
    valeurs: dict[str, object] = {
        "pas_transverse_y": 2.5,
        "pas_transverse_z": 2.0,
        "demi_largeur_y": 340.0,
        "hauteur_max": 240.0,
    }
    valeurs[champ] = 1.0 + 2.0j
    with pytest.raises(ValueError, match="complexes exclus"):
        ParametresEdp(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["x_entree", "pas_longitudinal"])
def test_solution_edp_refuse_les_scalaires_complexes(champ: str) -> None:
    """Les paramètres longitudinaux de la solution sont des scalaires réels."""
    valeurs: dict[str, object] = {
        "x_entree": 100.0,
        "pas_longitudinal": 0.5,
        "abscisses_y": np.array([-1.0, 0.0, 1.0]),
        "abscisses_z": np.array([0.0, 1.0]),
        "tranches": (TrancheEdp(x=100.0, champ=np.ones((3, 2))),),
    }
    valeurs[champ] = 1.0 + 2.0j
    with pytest.raises(ValueError, match="complexes exclus"):
        SolutionEdp(**valeurs)  # type: ignore[arg-type]


def test_tranche_edp_refuse_une_abscisse_complexe() -> None:
    """L'abscisse d'une tranche EDP est un scalaire réel."""
    with pytest.raises(ValueError, match="complexe exclu"):
        TrancheEdp(x=100.0 + 1.0j, champ=np.ones((2, 2)))  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["x", "coefficient", "d"])
def test_derivee_sigma_carre_refuse_les_scalaires_complexes(champ: str) -> None:
    """Les trois paramètres de la dérivée analytique sont réels."""
    valeurs: dict[str, object] = {"x": 100.0, "coefficient": 0.08, "d": 0.0002}
    valeurs[champ] = 1.0 + 2.0j
    with pytest.raises(ValueError, match="complexes exclus"):
        derivee_sigma_carre(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["a_y", "d_y", "b_z", "d_z"])
def test_coefficients_diffusion_refusent_les_complexes(champ: str) -> None:
    """Les coefficients de diffusion sont des scalaires réels."""
    valeurs: dict[str, object] = {
        "a_y": 0.08, "d_y": 0.0002, "b_z": 0.06, "d_z": 0.0003
    }
    valeurs[champ] = 1.0 + 2.0j
    with pytest.raises(ValueError, match="complexes exclus"):
        CoefficientsDiffusion(**valeurs)  # type: ignore[arg-type]


def test_pas_longitudinal_refuse_un_debut_complexe() -> None:
    """La distance de début du pas longitudinal est un scalaire réel."""
    coefficients = CoefficientsDiffusion(a_y=0.08, d_y=0.0002, b_z=0.06, d_z=0.0003)
    parametres = ParametresEdp(2.5, 2.0, 340.0, 240.0)
    with pytest.raises(ValueError, match="complexe exclu"):
        coefficients.pas_longitudinal(100.0 + 1.0j, 800.0, parametres)  # type: ignore[arg-type]


def test_diffusion_briggs_refuse_une_distance_complexe() -> None:
    """Le point d'évaluation de la loi de diffusion est une distance réelle."""
    with pytest.raises(ValueError, match="complexe exclu"):
        DiffusionBriggs().coefficients("D", 100.0 + 1.0j)  # type: ignore[arg-type]
