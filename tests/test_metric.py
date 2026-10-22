"""Tests des coûts de parcours et de la pseudo-distance uniforme."""

import numpy as np
import pytest

from jdriftx.metric import pseudo_distance_uniforme, temps_transport


def test_uniform_speed_time_is_length_over_speed() -> None:
    """À vitesse constante, le coût vaut longueur divisée par la vitesse."""
    ligne = np.array([[0.0, 0.0], [300.0, 0.0]])
    vent = np.array([[3.0, 0.0]])
    assert temps_transport(ligne, vent) == pytest.approx(100.0)


def test_polyline_cost_is_invariant_to_path_reversal_and_wind_sign() -> None:
    """La primitive sur polyligne utilise la norme, pas l'orientation."""
    a_vers_b = np.array([[0.0, 0.0], [100.0, 0.0]])
    b_vers_a = a_vers_b[::-1]
    vent_portant = np.array([[5.0, 0.0]])
    vent_oppose = -vent_portant

    cout_ab = temps_transport(a_vers_b, vent_portant)
    cout_ba_meme_vecteur = temps_transport(b_vers_a, vent_portant)
    cout_ba_vecteur_oppose = temps_transport(b_vers_a, vent_oppose)

    assert cout_ab == pytest.approx(cout_ba_meme_vecteur)
    assert cout_ab == pytest.approx(cout_ba_vecteur_oppose)


def test_longer_path_takes_longer_time_at_same_speed() -> None:
    """À vitesse identique, un détour plus long a un coût plus élevé."""
    ligne_directe = np.array([[0.0, 0.0], [100.0, 0.0]])
    ligne_detour = np.array([[0.0, 0.0], [50.0, 50.0], [100.0, 0.0]])
    vitesse = np.array([[10.0, 0.0]])
    vitesse_detour = np.array([[10.0, 0.0], [10.0, 0.0]])

    cout_direct = temps_transport(ligne_directe, vitesse)
    cout_detour = temps_transport(ligne_detour, vitesse_detour)

    assert cout_detour > cout_direct


def test_historical_uniform_pseudodistance_uses_longitudinal_projection() -> None:
    """Le coût historique uniforme ignore l'écart transversal."""
    a = np.array([0.0, 0.0])
    b = np.array([10.0, 5.0])
    assert pseudo_distance_uniforme(a, b, np.array([2.0, 0.0])) == pytest.approx(5.0)


def test_historical_uniform_pseudodistance_can_be_zero_for_distinct_points() -> None:
    """Même abscisse : la projection du point cible tombe sur le point de départ."""
    a = np.array([0.0, 0.0])
    b = np.array([0.0, 5.0])
    assert a.tolist() != b.tolist()
    assert pseudo_distance_uniforme(a, b, np.array([2.0, 0.0])) == pytest.approx(0.0)


def test_historical_uniform_pseudodistance_is_infinite_upwind() -> None:
    """Un point en amont reçoit un coût infini selon la convention historique."""
    a = np.array([10.0, 0.0])
    b = np.array([0.0, 3.0])
    assert np.isinf(pseudo_distance_uniforme(a, b, np.array([2.0, 0.0])))


def test_historical_uniform_pseudodistance_is_rotation_invariant() -> None:
    """La formule utilise la projection sur la direction du vent uniforme."""
    a = np.array([0.0, 0.0])
    b = np.array([5.0, 10.0])
    assert pseudo_distance_uniforme(a, b, np.array([0.0, 2.0])) == pytest.approx(5.0)


def test_historical_uniform_pseudodistance_rejects_zero_wind() -> None:
    with pytest.raises(ValueError, match="non nulle"):
        pseudo_distance_uniforme(np.zeros(2), np.ones(2), np.zeros(2))


def test_historical_uniform_pseudodistance_rejects_invalid_shapes() -> None:
    with pytest.raises(ValueError, match="forme"):
        pseudo_distance_uniforme(np.zeros(3), np.ones(2), np.array([1.0, 0.0]))


def test_inconsistent_polyline_shapes_raise_value_error() -> None:
    with pytest.raises(ValueError, match="doit etre un tableau"):
        temps_transport(np.zeros((1, 2)), np.zeros((1, 2)))


def test_polyline_speed_below_minimum_raises_value_error() -> None:
    ligne = np.array([[0.0, 0.0], [10.0, 0.0]])
    vent = np.array([[0.05, 0.0]])
    with pytest.raises(ValueError, match="umin"):
        temps_transport(ligne, vent)


@pytest.mark.parametrize("umin", [0.0, -1.0, float("inf"), float("nan")])
def test_polyline_cost_rejects_invalid_speed_threshold(umin: float) -> None:
    ligne = np.array([[0.0, 0.0], [1.0, 0.0]])
    vent = np.array([[1.0, 0.0]])
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
    with pytest.raises(ValueError, match=message):
        pseudo_distance_uniforme(a, b, vent)
