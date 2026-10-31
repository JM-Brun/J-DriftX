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


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", np.nan, np.inf, 10**400])
@pytest.mark.parametrize("parameter", ["x0", "y0", "t0", "t_end", "dt"])
def test_integrator_rejects_non_real_or_non_finite_scalar_inputs(
    parameter: str, bad: object
) -> None:
    """Les paramètres d'entrée sont des scalaires réels finis représentables en float64."""
    values: dict[str, object] = {
        "x0": 0.0,
        "y0": 0.0,
        "t0": 0.0,
        "t_end": 1.0,
        "dt": 0.1,
    }
    values[parameter] = bad
    with pytest.raises(ValueError, match="must be"):
        integrate_trajectory(
            lambda _t, _x, _y: (1.0, 0.0),
            values["x0"],
            values["y0"],
            values["t0"],
            values["t_end"],
            values["dt"],
        )  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", 10**400])
def test_integrator_rejects_unrepresentable_or_non_real_callback_components(
    bad: object,
) -> None:
    """Les composantes du callback suivent le même contrat scalaire réel fini."""
    with pytest.raises(ValueError, match="finite components"):
        integrate_trajectory(
            lambda _t, _x, _y: (bad, 0.0),  # type: ignore[return-value]
            0.0,
            0.0,
            0.0,
            1.0,
            0.1,
        )


def test_final_step_lands_exactly_on_t_end_when_the_remainder_is_one_ulp() -> None:
    """Un reste final d'un ulp atterrit exactement sur t_end, pour chaque methode."""

    # Given — deux temps float64 consecutifs : le reste final vaut exactement un ulp.
    def vitesse(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (1.0, 0.0)

    t0 = 1.0
    t_end = float(np.nextafter(t0, np.inf))

    # When — la trajectoire est integree jusqu'au reste d'un ulp par chaque methode.
    for method in ("euler", "rk4"):
        times, _, _ = integrate_trajectory(vitesse, 0.0, 0.0, t0, t_end, 1.0, method)

        # Then — le dernier pas raccourci atterrit exactement sur t_end, sans erreur.
        assert list(times) == [t0, t_end]


def test_final_step_lands_exactly_on_t_end_across_a_binade_boundary() -> None:
    """Un reste final egal a un demi-ulp de t_end atterrit exactement sur t_end."""

    # Given — le temps initial est le plus grand float64 sous 1.0 : le reste
    # final vaut exactement un demi-ulp de t_end (un ulp du temps initial).
    def vitesse(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (1.0, 0.0)

    t0 = float(np.nextafter(1.0, -np.inf))
    t_end = 1.0

    # When — la trajectoire est integree jusqu'a la frontiere de binade.
    for method in ("euler", "rk4"):
        times, _, _ = integrate_trajectory(vitesse, 0.0, 0.0, t0, t_end, 1.0, method)

        # Then — la somme exacte atterrit sur t_end, sans erreur de dernier pas.
        assert list(times) == [t0, t_end]


def test_final_step_lands_exactly_on_t_end_at_subnormal_scale() -> None:
    """Le dernier pas reste exact a l'echelle sous-normale la plus fine."""

    # Given — le plus petit float64 positif comme cible, depuis t = 0.
    def vitesse(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (1.0, 0.0)

    t_end = 5e-324

    # When — l'intervalle est couvert d'un seul pas raccourci.
    for method in ("euler", "rk4"):
        times, _, _ = integrate_trajectory(vitesse, 0.0, 0.0, 0.0, t_end, t_end, method)

        # Then — le pas raccourci atterrit exactement sur le plus petit subnormal.
        assert list(times) == [0.0, t_end]


def test_final_step_of_one_ulp_succeeds_at_large_time_magnitude() -> None:
    """A magnitude elevee, un reste d'un ulp franchit le dernier pas sans erreur."""

    # Given — un temps initial dont l'ulp vaut 2 : le reste final est exactement
    # un ulp, alors qu'un pas dt plus fin que l'ulp serait refuse par la garde.
    def vitesse(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (1.0, 0.0)

    t0 = 1.0e16
    t_end = float(np.nextafter(t0, np.inf))

    # When — le dernier pas raccourci (un ulp) est franchi par RK4.
    times, _, _ = integrate_trajectory(vitesse, 0.0, 0.0, t0, t_end, 4.0, "rk4")

    # Then — la trajectoire se termine exactement sur t_end, en un seul pas.
    assert list(times) == [t0, t_end]


def test_half_ulp_dt_is_rejected_as_an_unrepresentable_step() -> None:
    """Un dt d'un demi-ulp est refuse : la garde ne concerne que dt, jamais le reste."""

    # Given — un dt egal au demi-ulp de t0 : l'arrondi ties-to-even ramene le
    # temps calcule au temps courant (mantisse paire) — echec explicite documente.
    def vitesse(_t: float, _x: float, _y: float) -> tuple[float, float]:
        return (1.0, 0.0)

    # When / Then — seul un dt sous la resolution flottante est refuse.
    with pytest.raises(FloatingPointError, match="too small to advance time"):
        integrate_trajectory(vitesse, 0.0, 0.0, 1.0, 2.0, 2.0**-53)
