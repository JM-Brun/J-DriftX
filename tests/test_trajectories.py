"""Tests for numerical particle trajectory integration."""

import numpy as np
import pytest

from jdriftx import trajectories
from jdriftx.trajectories import integrate_trajectory


def test_constant_velocity_is_integrated_exactly_by_both_methods() -> None:
    """À vitesse constante, Euler et RK4 intègrent exactement l'intervalle."""

    # Given — un champ de vitesse constant (2, -1) m/s.
    def velocity(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (2.0, -1.0)

    # When — la trajectoire est intégrée de t = 0 à t = 1 par chaque méthode.
    for method in ("euler", "rk4"):
        times, x, y = integrate_trajectory(velocity, 1.0, 3.0, 0.0, 1.0, 0.3, method)
        # Then — l'intervalle est couvert exactement et la position est exacte.
        assert times[-1] == pytest.approx(1.0)
        assert x[-1] == pytest.approx(3.0)
        assert y[-1] == pytest.approx(2.0)


def test_rk4_is_more_accurate_than_euler_for_rotational_field() -> None:
    """Sur champ rotationnel, RK4 est plus précis qu'Euler."""

    # Given — un champ en rotation solide et les deux méthodes au même pas.
    def velocity(_t: float, x: float, y: float) -> tuple[float, float]:
        return (-y, x)

    # When — deux tours de cercle sont intégrés par chaque méthode.
    _, x_euler, y_euler = integrate_trajectory(velocity, 1.0, 0.0, 0.0, 2.0, 0.1, "euler")
    _, x_rk4, y_rk4 = integrate_trajectory(velocity, 1.0, 0.0, 0.0, 2.0, 0.1, "rk4")
    exact_x, exact_y = np.cos(2.0), np.sin(2.0)
    error_euler = np.hypot(x_euler[-1] - exact_x, y_euler[-1] - exact_y)
    error_rk4 = np.hypot(x_rk4[-1] - exact_x, y_rk4[-1] - exact_y)
    # Then — l'erreur RK4 est strictement inférieure à l'erreur Euler.
    assert error_rk4 < error_euler


def test_invalid_step_is_rejected() -> None:
    """Un pas de temps nul est refusé."""
    # Given — un pas de temps nul.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="strictly positive"):
        integrate_trajectory(lambda _t, _x, _y: (1.0, 0.0), 0, 0, 0, 1, 0)


def test_invalid_velocity_output_is_rejected() -> None:
    """Une composante de vitesse non finie est refusée pendant l'intégration."""
    # Given — un champ de vitesse retournant une composante NaN.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="finite components"):
        integrate_trajectory(lambda _t, _x, _y: (np.nan, 0.0), 0, 0, 0, 1, 0.1)


def test_time_step_that_cannot_advance_float_time_is_rejected() -> None:
    """Un pas de temps sous la résolution flottante ne doit pas boucler indéfiniment."""
    # Given — un temps initial dont l'ULP dépasse le pas demandé.
    initial_time = 1.0e16
    end_time = initial_time + 2.0

    # When / Then — le premier pas non représentable est rejeté.
    with pytest.raises(FloatingPointError, match="too small to advance time"):
        integrate_trajectory(
            lambda _t, _x, _y: (1.0, 0.0),
            0.0,
            0.0,
            initial_time,
            end_time,
            0.1,
        )


def test_non_finite_position_after_step_is_rejected() -> None:
    """Un débordement de coordonnées ne doit pas être retourné silencieusement."""
    # Given — une vitesse finie et un pas dont le produit déborde en float64.
    maximum_float = np.finfo(float).max

    # When / Then — l'intégration signale explicitement le dépassement.
    with pytest.raises(FloatingPointError, match="coordinates became non-finite"):
        integrate_trajectory(
            lambda _t, _x, _y: (maximum_float, 0.0),
            0.0,
            0.0,
            0.0,
            2.0,
            2.0,
            "euler",
        )


def test_velocity_callback_must_return_a_pair() -> None:
    """Une sortie qui ne respecte pas le contrat (ux, uy) est rejetée."""
    # Given — un callback qui retourne une seule composante.
    # When / Then — l'appel échoue avec une erreur de contrat explicite.
    with pytest.raises(ValueError, match="pair of finite components"):
        integrate_trajectory(
            lambda _t, _x, _y: (1.0,),
            0.0,
            0.0,
            0.0,
            1.0,
            0.1,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_component", ["bad", 1.0 + 2.0j, None])
def test_velocity_callback_rejects_non_real_components(invalid_component: object) -> None:
    """Les composantes non réelles ou non numériques donnent une ValueError stable."""

    def velocity(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return 1.0, invalid_component  # type: ignore[return-value]

    with pytest.raises(ValueError, match="pair of finite components"):
        integrate_trajectory(velocity, 0.0, 0.0, 0.0, 1.0, 0.1)


def test_excessive_step_count_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """Une intégration qui dépasserait la garde de pas est refusée explicitement."""
    # Given — une garde abaissée à trois pas et un champ de vitesse constant.
    monkeypatch.setattr(trajectories, "_MAXIMUM_STEPS", 3)
    # When / Then — l'intégration refuse de boucler sans borne.
    with pytest.raises(ValueError, match="maximum"):
        integrate_trajectory(lambda _t, _x, _y: (1.0, 0.0), 0.0, 0.0, 0.0, 10.0, 0.1)
