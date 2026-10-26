"""Tests des coûts de parcours et de la pseudo-distance uniforme."""

import numpy as np
import pytest

from jdriftx.metric import (
    pseudo_distance_uniforme,
    temps_premiere_arrivee_1d,
    temps_transport,
)


def test_uniform_speed_time_is_length_over_speed() -> None:
    """À vitesse constante, le coût vaut longueur divisée par la vitesse."""
    # Given — un segment de 300 m parcouru à 3 m/s.
    ligne = np.array([[0.0, 0.0], [300.0, 0.0]])
    vent = np.array([[3.0, 0.0]])
    # When — le coût de parcours est évalué.
    cout = temps_transport(ligne, vent)
    # Then — le coût vaut 100 s.
    assert cout == pytest.approx(100.0)


def test_polyline_cost_is_invariant_to_path_reversal_and_wind_sign() -> None:
    """La primitive sur polyligne utilise la norme, pas l'orientation."""
    # Given — un même trajet parcouru dans les deux sens, avec un vent
    # portant puis opposé.
    a_vers_b = np.array([[0.0, 0.0], [100.0, 0.0]])
    b_vers_a = a_vers_b[::-1]
    vent_portant = np.array([[5.0, 0.0]])
    vent_oppose = -vent_portant

    # When — les coûts sont évalués pour les trois combinaisons.
    cout_ab = temps_transport(a_vers_b, vent_portant)
    cout_ba_meme_vecteur = temps_transport(b_vers_a, vent_portant)
    cout_ba_vecteur_oppose = temps_transport(b_vers_a, vent_oppose)

    # Then — les trois coûts sont identiques : seule la norme compte.
    assert cout_ab == pytest.approx(cout_ba_meme_vecteur)
    assert cout_ab == pytest.approx(cout_ba_vecteur_oppose)


def test_longer_path_takes_longer_time_at_same_speed() -> None:
    """À vitesse identique, un détour plus long a un coût plus élevé."""
    # Given — un trajet direct et un détour strictement plus long, à la
    # même vitesse.
    ligne_directe = np.array([[0.0, 0.0], [100.0, 0.0]])
    ligne_detour = np.array([[0.0, 0.0], [50.0, 50.0], [100.0, 0.0]])
    vitesse = np.array([[10.0, 0.0]])
    vitesse_detour = np.array([[10.0, 0.0], [10.0, 0.0]])

    # When — les deux coûts sont évalués.
    cout_direct = temps_transport(ligne_directe, vitesse)
    cout_detour = temps_transport(ligne_detour, vitesse_detour)

    # Then — le détour coûte plus cher.
    assert cout_detour > cout_direct


def test_uniform_pseudodistance_uses_longitudinal_projection() -> None:
    """Le coût uniforme défini ici ignore l'écart transversal."""
    # Given — un vent selon +x et une cible décalée transversalement.
    a = np.array([0.0, 0.0])
    b = np.array([10.0, 5.0])
    # When — la pseudo-distance uniforme est évaluée.
    cout = pseudo_distance_uniforme(a, b, np.array([2.0, 0.0]))
    # Then — seul le déplacement longitudinal (10 m à 2 m/s) compte.
    assert cout == pytest.approx(5.0)


def test_uniform_pseudodistance_can_be_zero_for_distinct_points() -> None:
    """La projection longitudinale nulle donne un coût nul, même pour deux points distincts."""
    # Given — une cible exactement transversale à l'origine.
    a = np.array([0.0, 0.0])
    b = np.array([0.0, 5.0])
    # When / Then — pour des points distincts, le coût est nul.
    assert a.tolist() != b.tolist()
    assert pseudo_distance_uniforme(a, b, np.array([2.0, 0.0])) == pytest.approx(0.0)


def test_uniform_pseudodistance_is_infinite_upwind() -> None:
    """Un point en amont reçoit un coût infini selon la convention explicite de cette fonction."""
    # Given — une cible située en amont de l'origine.
    a = np.array([10.0, 0.0])
    b = np.array([0.0, 3.0])
    # When — la pseudo-distance est évaluée vers l'amont.
    cout = pseudo_distance_uniforme(a, b, np.array([2.0, 0.0]))
    # Then — le coût est infini.
    assert np.isinf(cout)


def test_uniform_pseudodistance_is_rotation_invariant() -> None:
    """La formule utilise la projection sur la direction du vent uniforme."""
    # Given — le cas de référence tourné : même géométrie relative, vent
    # selon +y au lieu de +x.
    a = np.array([0.0, 0.0])
    b = np.array([5.0, 10.0])
    # When — la pseudo-distance est évaluée avec le vent tourné.
    cout = pseudo_distance_uniforme(a, b, np.array([0.0, 2.0]))
    # Then — le coût est identique au cas selon +x (5 s).
    assert cout == pytest.approx(5.0)


def test_uniform_pseudodistance_rejects_zero_wind() -> None:
    """Un vent rigoureusement nul est refusé : le coût n'est pas défini."""
    # Given — un vecteur vitesse nul.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="non nulle"):
        pseudo_distance_uniforme(np.zeros(2), np.ones(2), np.zeros(2))


def test_uniform_pseudodistance_rejects_invalid_shapes() -> None:
    """Des points mal formés sont refusés avant tout calcul."""
    # Given — un point à trois coordonnées.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="forme"):
        pseudo_distance_uniforme(np.zeros(3), np.ones(2), np.array([1.0, 0.0]))


def test_inconsistent_polyline_shapes_raise_value_error() -> None:
    """Une polyligne réduite à un point est refusée."""
    # Given — une « polyligne » d'un seul point et un vent non aligné.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="doit etre un tableau"):
        temps_transport(np.zeros((1, 2)), np.zeros((1, 2)))


def test_polyline_speed_below_minimum_raises_value_error() -> None:
    """Une vitesse sous le seuil umin est refusée."""
    # Given — un segment et un vent sous le seuil umin par défaut.
    ligne = np.array([[0.0, 0.0], [10.0, 0.0]])
    vent = np.array([[0.05, 0.0]])
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="umin"):
        temps_transport(ligne, vent)


@pytest.mark.parametrize("umin", [0.0, -1.0, float("inf"), float("nan")])
def test_polyline_cost_rejects_invalid_speed_threshold(umin: float) -> None:
    """Un seuil umin non fini ou non positif est refusé."""
    # Given — un seuil umin invalide (nul, négatif, infini ou NaN).
    ligne = np.array([[0.0, 0.0], [1.0, 0.0]])
    vent = np.array([[1.0, 0.0]])
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="umin"):
        temps_transport(ligne, vent, umin=umin)


@pytest.mark.parametrize(
    ("ligne", "vent", "message"),
    [
        (
            np.array([[0.0, 0.0], [float("nan"), 1.0]]),
            np.array([[1.0, 0.0]]),
            "coordonnees finies",
        ),
        (
            np.array([[0.0, 0.0], [1.0, 0.0]]),
            np.array([[float("inf"), 0.0]]),
            "vitesses finies",
        ),
    ],
)
def test_polyline_cost_rejects_non_finite_inputs(
    ligne: np.ndarray, vent: np.ndarray, message: str
) -> None:
    """Des coordonnées ou des vitesses non finies sont refusées."""
    # Given — une ligne ou un vent contenant une valeur non finie.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match=message):
        temps_transport(ligne, vent)


@pytest.mark.parametrize(
    ("a", "b", "vent", "message"),
    [
        (
            np.array([float("nan"), 0.0]),
            np.zeros(2),
            np.array([1.0, 0.0]),
            "coordonnees finies",
        ),
        (
            np.zeros(2),
            np.ones(2),
            np.array([1.0, float("inf")]),
            "vitesses finies",
        ),
    ],
)
def test_uniform_pseudodistance_rejects_non_finite_inputs(
    a: np.ndarray, b: np.ndarray, vent: np.ndarray, message: str
) -> None:
    """Des coordonnées ou un vent non finis sont refusés."""
    # Given — une coordonnée ou une composante de vent non finie.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match=message):
        pseudo_distance_uniforme(a, b, vent)


@pytest.mark.parametrize(
    ("a", "b", "vent"),
    [
        ((0.0, 0.0), (12.0, 7.0), (3.0, 4.0)),
        ((-5.0, 2.0), (8.0, -1.0), (0.0, 2.5)),
        ((1.0, -9.0), (4.0, 6.0), (-2.0, 1.0)),
    ],
)
def test_uniform_pseudodistance_matches_projection_formula(
    a: tuple[float, float],
    b: tuple[float, float],
    vent: tuple[float, float],
) -> None:
    """Le résultat coïncide avec la formule fermée, ou +inf si b est en amont."""
    # Given — le déplacement et le vent, et la formule fermée indépendante :
    # projection longitudinale sur le vent divisée par le carré de sa norme,
    # avec la convention +inf pour une cible en amont.
    deplacement = np.asarray(b) - np.asarray(a)
    vitesse = np.asarray(vent, dtype=float)
    projection_longitudinale = float(np.dot(deplacement, vitesse))
    if projection_longitudinale < 0.0:
        attendu = float("inf")
    else:
        attendu = projection_longitudinale / float(np.dot(vitesse, vitesse))
    # When — la pseudo-distance uniforme est évaluée par l'implémentation.
    obtenu = pseudo_distance_uniforme(a, b, vent)
    # Then — l'implémentation restitue la formule fermée.
    assert obtenu == pytest.approx(attendu)


def test_uniform_pseudodistance_is_translation_invariant() -> None:
    """Translater les deux points ensemble préserve le déplacement et le coût."""
    # Given — un couple de points, une translation quelconque et un vent.
    a = np.array([-3.0, 2.0])
    b = np.array([9.0, 8.0])
    translation = np.array([100.0, -45.0])
    vent = np.array([4.0, 3.0])
    # When — le coût est évalué avant et après translation des deux points.
    original = pseudo_distance_uniforme(a, b, vent)
    translate = pseudo_distance_uniforme(a + translation, b + translation, vent)
    # Then — le coût est inchangé.
    assert translate == pytest.approx(original)


def test_uniform_pseudodistance_scales_inversely_with_wind_magnitude() -> None:
    """Pour un facteur positif, le coût décroît comme l'inverse du facteur."""
    # Given — un couple de points en aval et un vent non nul, avec un
    # facteur d'échelle strictement positif (hypothèse : l'amont/aval est
    # préservé, un facteur négatif inverserait la convention +inf).
    a = np.array([0.0, 0.0])
    b = np.array([12.0, 9.0])
    vent = np.array([4.0, 3.0])
    facteur = 2.5
    # When — le coût est évalué pour le vent et pour le vent renforcé.
    original = pseudo_distance_uniforme(a, b, vent)
    vent_renforce = pseudo_distance_uniforme(a, b, facteur * vent)
    # Then — le coût est divisé par le facteur.
    assert vent_renforce == pytest.approx(original / facteur)


def test_uniform_pseudodistance_is_invariant_to_transverse_displacement() -> None:
    """Un déplacement orthogonal au vent ne change pas le coût longitudinal."""
    # Given — une cible en aval et un déplacement transversal exactement
    # orthogonal au vent.
    a = np.array([0.0, 0.0])
    vent = np.array([3.0, 4.0])
    aval = np.array([6.0, 8.0])
    transversal = np.array([-8.0, 6.0])
    # When — le coût est évalué pour la cible et pour la cible décalée.
    reference = pseudo_distance_uniforme(a, aval, vent)
    decalee = pseudo_distance_uniforme(a, aval + transversal, vent)
    # Then — le coût est inchangé.
    assert decalee == pytest.approx(reference)


def test_uniform_pseudodistance_is_zero_for_upwind_boundary() -> None:
    """Un déplacement purement transversal reçoit le coût nul (borne amont)."""
    # Given — un point et un déplacement transversal exactement orthogonal
    # au vent (avance longitudinale nulle, pas strictement négative).
    a = np.array([2.0, -1.0])
    vent = np.array([3.0, 4.0])
    transversal = np.array([-4.0, 3.0])
    # When — la pseudo-distance est évaluée sur la borne amont.
    obtenu = pseudo_distance_uniforme(a, a + transversal, vent)
    # Then — le coût est nul selon la convention documentée.
    assert obtenu == pytest.approx(0.0)


def test_uniform_pseudodistance_is_asymmetric_along_the_wind() -> None:
    """La référence uniforme n'est pas symétrique : finie vers l'aval, infinie vers l'amont."""
    # Given — deux points alignés avec le vent, b en aval de a, dans un
    # repère quelconque (vent non aligné sur un axe).
    a = np.array([0.0, 0.0])
    b = np.array([12.0, 9.0])
    vent = np.array([4.0, 3.0])
    # When — la pseudo-distance est évaluée dans les deux sens.
    aller = pseudo_distance_uniforme(a, b, vent)
    retour = pseudo_distance_uniforme(b, a, vent)
    # Then — l'aller est fini (15 m de projection à 5 m/s) et le retour est
    # infini selon la convention documentée : la référence n'est pas symétrique.
    assert aller == pytest.approx(3.0)
    assert np.isinf(retour)


def test_uniform_pseudodistance_symmetric_on_transverse_boundary() -> None:
    """La non-symétrie n'est pas globale : la borne transversale coûte zéro dans les deux sens."""
    # Given — un déplacement exactement orthogonal au vent. Le vent selon +y
    # donne une direction exacte en virgule flottante : la projection est
    # nulle des deux côtés, sans bruit d'arrondi à la borne.
    a = np.array([2.0, -1.0])
    vent = np.array([0.0, 5.0])
    transversal = np.array([4.0, 0.0])
    b = a + transversal
    # When — la pseudo-distance est évaluée dans les deux sens.
    aller = pseudo_distance_uniforme(a, b, vent)
    retour = pseudo_distance_uniforme(b, a, vent)
    # Then — les deux directions reçoivent le coût nul de la borne amont :
    # l'asymétrie de la convention +inf ne s'étend pas à cette dégénérescence.
    assert aller == pytest.approx(0.0)
    assert retour == pytest.approx(0.0)


@pytest.mark.parametrize(
    ("a", "b", "vitesse", "attendu"),
    [
        (0.0, 10.0, 2.0, 5.0),
        (10.0, 0.0, -2.0, 5.0),
        (3.0, 3.0, 2.0, 0.0),
        (3.0, 3.0, 0.0, 0.0),
        (0.0, 10.0, -2.0, float("inf")),
        (10.0, 0.0, 2.0, float("inf")),
        (0.0, 10.0, 0.0, float("inf")),
    ],
)
def test_1d_first_arrival_constant_velocity(
    a: float, b: float, vitesse: float, attendu: float
) -> None:
    """Le temps de première arrivée suit le sens du champ constant 1D."""
    assert temps_premiere_arrivee_1d(a, b, vitesse) == pytest.approx(attendu)


@pytest.mark.parametrize(
    ("a", "b", "vitesse"),
    [
        (float("nan"), 1.0, 1.0),
        (0.0, float("inf"), 1.0),
        (0.0, 1.0, float("-inf")),
    ],
)
def test_1d_first_arrival_rejects_non_finite_inputs(a: float, b: float, vitesse: float) -> None:
    """Les entrées non finies sont rejetées explicitement."""
    with pytest.raises(ValueError, match="finis"):
        temps_premiere_arrivee_1d(a, b, vitesse)


def test_1d_first_arrival_rejects_infinite_displacement() -> None:
    """Un déplacement b - a non fini (débordement flottant) est refusé explicitement."""
    # Given — deux positions finies dont la différence déborde le format flottant.
    a = -1.0e308
    b = 1.0e308
    # When / Then — l'évaluation est refusée avant tout calcul de temps.
    with pytest.raises(ValueError, match="deplacement"):
        temps_premiere_arrivee_1d(a, b, 1.0)


@pytest.mark.parametrize(
    ("a", "b", "vent"),
    [
        ((0.0, 0.0), (12.0, 9.0), (4.0, 3.0)),
        ((0.0, 0.0), (300.0, 65.0), (2.0, 0.0)),
        ((10.0, 20.0), (310.0, 85.0), (1.5, 2.5)),
    ],
)
def test_uniform_pseudodistance_is_adjoint_vector_dot_displacement(
    a: tuple[float, float], b: tuple[float, float], vent: tuple[float, float]
) -> None:
    """Le cout dirige uniforme est le produit scalaire de l'adjoint et du deplacement."""
    # Given — le vecteur adjoint exact du champ uniforme, dérivé
    # indépendamment : lambda = u/(u.u), et l'identité tau = lambda.(b - a).
    vitesse = np.asarray(vent, dtype=float)
    adjoint = vitesse / float(np.dot(vitesse, vitesse))
    identite = float(np.dot(adjoint, np.asarray(b, dtype=float) - np.asarray(a, dtype=float)))
    # When — la pseudo-distance uniforme est évaluée par l'implémentation.
    obtenu = pseudo_distance_uniforme(a, b, vent)
    # Then — l'identité adjointe est restituée à la précision machine près.
    assert obtenu == pytest.approx(identite, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    ("a", "b", "vent"),
    [
        ((0.0, 0.0), (12.0, 9.0), (4.0, 3.0)),
        ((0.0, 0.0), (300.0, 65.0), (2.0, 0.0)),
        ((10.0, 20.0), (310.0, 85.0), (1.5, 2.5)),
    ],
)
def test_uniform_pseudodistance_gradient_wrt_wind_matches_analytic(
    a: tuple[float, float], b: tuple[float, float], vent: tuple[float, float]
) -> None:
    """Le gradient du coût dirigé par rapport au vent est analytiquement exact."""
    # Given — la dérivée fermée indépendante :
    # d(tau)/du = d/(u.u) - 2 (d.u) u / (u.u)^2.
    deplacement = np.asarray(b, dtype=float) - np.asarray(a, dtype=float)
    vitesse = np.asarray(vent, dtype=float)
    uu = float(np.dot(vitesse, vitesse))
    du = float(np.dot(deplacement, vitesse))
    attendu = deplacement / uu - 2.0 * du * vitesse / (uu * uu)
    # When — le gradient est estimé par différences finies centrées.
    pas = 1e-5
    gradient = np.zeros(2)
    for axe in range(2):
        perturbation = np.zeros(2)
        perturbation[axe] = pas
        plus = pseudo_distance_uniforme(a, b, vitesse + perturbation)
        moins = pseudo_distance_uniforme(a, b, vitesse - perturbation)
        gradient[axe] = (plus - moins) / (2.0 * pas)
    # Then — l'estimation coïncide avec la formule analytique.
    np.testing.assert_allclose(gradient, attendu, rtol=1e-6, atol=1e-6)


def test_uniform_pseudodistance_gradient_wrt_points_is_adjoint_vector() -> None:
    """Le gradient par rapport aux extrémités vaut plus ou moins le vecteur adjoint."""
    # Given — une configuration aval quelconque et l'adjoint exact
    # lambda = u/(u.u) : le coût est linéaire en la position.
    a = np.array([10.0, 20.0])
    b = np.array([310.0, 85.0])
    vitesse = np.array([1.5, 2.5])
    adjoint = vitesse / float(np.dot(vitesse, vitesse))
    pas = 1e-5
    gradient_b = np.zeros(2)
    gradient_a = np.zeros(2)
    # When — les gradients par rapport à b puis à a sont estimés par
    # différences finies centrées.
    for axe in range(2):
        decalage = np.zeros(2)
        decalage[axe] = pas
        plus = pseudo_distance_uniforme(a, b + decalage, vitesse)
        moins = pseudo_distance_uniforme(a, b - decalage, vitesse)
        gradient_b[axe] = (plus - moins) / (2.0 * pas)
        plus = pseudo_distance_uniforme(a + decalage, b, vitesse)
        moins = pseudo_distance_uniforme(a - decalage, b, vitesse)
        gradient_a[axe] = (plus - moins) / (2.0 * pas)
    # Then — d(tau)/db = lambda et d(tau)/da = -lambda, à la précision des
    # différences finies près.
    np.testing.assert_allclose(gradient_b, adjoint, rtol=1e-6, atol=1e-6)
    np.testing.assert_allclose(gradient_a, -adjoint, rtol=1e-6, atol=1e-6)


def test_1d_first_arrival_gradient_matches_closed_form() -> None:
    """Le gradient du cas 1D exact vaut -tau/v pour la vitesse et 1/v pour la cible."""
    # Given — un cas aval 1D (b > a, vitesse positive) et les dérivées
    # fermées d(tau)/dv = -tau/v et d(tau)/db = 1/v.
    a = 0.0
    b = 10.0
    vitesse = 2.0
    tau = temps_premiere_arrivee_1d(a, b, vitesse)
    pas = 1e-5
    # When — les gradients sont estimés par différences finies centrées.
    plus_v = temps_premiere_arrivee_1d(a, b, vitesse + pas)
    moins_v = temps_premiere_arrivee_1d(a, b, vitesse - pas)
    derivee_v = (plus_v - moins_v) / (2.0 * pas)
    plus_b = temps_premiere_arrivee_1d(a, b + pas, vitesse)
    moins_b = temps_premiere_arrivee_1d(a, b - pas, vitesse)
    derivee_b = (plus_b - moins_b) / (2.0 * pas)
    # Then — les estimations coïncident avec les formules fermées.
    assert derivee_v == pytest.approx(-tau / vitesse, rel=1e-6)
    assert derivee_b == pytest.approx(1.0 / vitesse, rel=1e-6)
