"""Tests de la primitive de coût de parcours sur une polyligne."""

import numpy as np
import pytest

from jdriftx.metric import temps_transport


def test_uniform_speed_time_is_length_over_speed() -> None:
    """À vitesse constante, le coût vaut longueur divisée par la vitesse."""
    ligne = np.array([[0.0, 0.0], [300.0, 0.0]])
    vent = np.array([[3.0, 0.0]])
    assert temps_transport(ligne, vent) == pytest.approx(100.0)


def test_path_reversal_and_wind_sign_do_not_change_cost() -> None:
    """La primitive utilise la norme de vitesse, pas son orientation."""
    a_vers_b = np.array([[0.0, 0.0], [100.0, 0.0]])
    b_vers_a = a_vers_b[::-1]
    vent_portant = np.array([[5.0, 0.0]])
    vent_oppose = -vent_portant

    tau_ab = temps_transport(a_vers_b, vent_portant)
    tau_ba_same_vector = temps_transport(b_vers_a, vent_portant)
    tau_ba_opposite_vector = temps_transport(b_vers_a, vent_oppose)

    assert tau_ab == pytest.approx(tau_ba_same_vector)
    assert tau_ab == pytest.approx(tau_ba_opposite_vector)


def test_longer_path_takes_longer_time_at_same_speed() -> None:
    """À vitesse identique, un détour plus long a un coût plus élevé."""
    ligne_directe = np.array([[0.0, 0.0], [100.0, 0.0]])
    ligne_detour = np.array([[0.0, 0.0], [50.0, 50.0], [100.0, 0.0]])
    vitesse = np.array([[10.0, 0.0]])
    vitesse_detour = np.array([[10.0, 0.0], [10.0, 0.0]])

    cout_direct = temps_transport(ligne_directe, vitesse)
    cout_detour = temps_transport(ligne_detour, vitesse_detour)

    assert cout_detour > cout_direct


def test_inconsistent_shapes_raise_value_error() -> None:
    with pytest.raises(ValueError, match="doit etre un tableau"):
        temps_transport(np.zeros((1, 2)), np.zeros((1, 2)))


def test_speed_below_minimum_raises_value_error() -> None:
    ligne = np.array([[0.0, 0.0], [10.0, 0.0]])
    vent = np.array([[0.05, 0.0]])
    with pytest.raises(ValueError, match="umin"):
        temps_transport(ligne, vent)
