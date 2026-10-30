"""Tests for the independent periodic advection-diffusion solver."""

from collections.abc import Callable

import numpy as np
import pytest
from numpy.typing import NDArray

from jdriftx import periodic_transport
from jdriftx.periodic_transport import (
    periodic_sine_solution,
    solve_periodic_sine_transport,
    solve_periodic_upwind_euler,
)


def _solve(
    n_cells: int, dt: float, end_time: float = 0.4
) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Résout le cas de référence commun aux tests du solveur centré/RK4."""
    return solve_periodic_sine_transport(
        n_cells=n_cells,
        length=1.0,
        end_time=end_time,
        dt=dt,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )


def test_numerical_solver_matches_exact_solution_on_refined_grid() -> None:
    """Sur grille raffinée, le schéma centré/RK4 restitue la solution exacte."""
    # Given / When — le cas de référence est résolu sur 128 mailles avec un
    # pas de temps fin, jusqu'à t = 0,4.
    x, actual, _ = _solve(128, 0.0005)
    # Then — l'erreur RMS vis-à-vis de la solution exacte reste sous 2e-3.
    exact = periodic_sine_solution(
        x,
        0.4,
        length=1.0,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )
    assert np.sqrt(np.mean((actual - exact) ** 2)) < 2e-3


def test_periodic_solver_conserves_discrete_mean() -> None:
    """Le schéma centré/RK4 conserve la moyenne discrète à 1e-12 près."""
    # Given / When — le cas de référence est résolu sur 96 mailles.
    _, actual, _ = _solve(96, 0.0005)
    # Then — la moyenne discrète finale vaut la concentration moyenne initiale.
    assert float(np.mean(actual)) == pytest.approx(1.0, abs=1e-12)


def test_spatial_refinement_reduces_error() -> None:
    """L'erreur décroît en raffinant la grille, à l'ordre spatial attendu."""
    # Given — trois grilles de plus en plus fines, au même instant final.
    errors = []
    for n_cells in (24, 48, 96):
        # When — chaque grille est résolue et l'erreur RMS mesurée.
        x, actual, _ = _solve(n_cells, 0.0001)
        exact = periodic_sine_solution(
            x,
            0.4,
            length=1.0,
            mean_concentration=1.0,
            amplitude=0.3,
            velocity=0.4,
            diffusivity=0.01,
        )
        errors.append(float(np.sqrt(np.mean((actual - exact) ** 2))))
    # Then — l'erreur décroît strictement et l'ordre mesuré est entre 1,8 et 2,2.
    assert errors[2] < errors[1] < errors[0]
    observed_order = float(np.polyfit(np.log([1 / 24, 1 / 48, 1 / 96]), np.log(errors), 1)[0])
    assert 1.8 < observed_order < 2.2


def test_temporal_refinement_converges_to_fine_step_reference() -> None:
    """À grille fixée, l'erreur décroît en raffinant le pas, à l'ordre RK4 attendu."""
    # Given — une référence à pas très fin et trois pas de temps plus grossiers.
    n_cells = 48
    _, reference, _ = _solve(n_cells, 0.0003125)
    errors = []
    for dt in (0.02, 0.01, 0.005):
        # When — chaque pas de temps est résolu sur la même grille.
        _, actual, _ = _solve(n_cells, dt)
        errors.append(float(np.sqrt(np.mean((actual - reference) ** 2))))
    # Then — l'erreur décroît strictement et l'ordre mesuré est entre 3,5 et 4,5.
    assert errors[2] < errors[1] < errors[0]
    observed_order = float(np.polyfit(np.log([0.02, 0.01, 0.005]), np.log(errors), 1)[0])
    assert 3.5 < observed_order < 4.5


def test_unstable_time_step_is_rejected() -> None:
    """Un pas de temps hors de la région de stabilité RK4 est refusé."""
    # Given / When / Then — un pas de temps grossier (dt = 1,0) déclenche le
    # refus avant toute intégration.
    with pytest.raises(ValueError, match="stability region"):
        _solve(64, 1.0)


def test_invalid_grid_and_diffusivity_are_rejected() -> None:
    """Une grille trop grossière ou une diffusivité négative est refusée."""
    # Given / When / Then — n_cells = 4 (minimum 8), puis diffusivité négative.
    with pytest.raises(ValueError, match="greater than or equal to 8"):
        solve_periodic_sine_transport(n_cells=4, length=1, end_time=1, dt=0.01)
    with pytest.raises(ValueError, match="non-negative"):
        solve_periodic_sine_transport(
            n_cells=16, length=1, end_time=0.1, dt=0.001, diffusivity=-0.1
        )


def test_independent_upwind_euler_solver_matches_exact_solution() -> None:
    """Le schéma amont/Euler indépendant restitue la solution exacte."""
    # Given — le même cas de référence résolu par le schéma amont/Euler.
    x, actual, _ = solve_periodic_upwind_euler(
        n_cells=128,
        length=1.0,
        end_time=0.4,
        dt=0.0001,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )
    # When — l'erreur amont/Euler et l'erreur centré/RK4 sont mesurées.
    exact = periodic_sine_solution(
        x,
        0.4,
        length=1.0,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )
    assert np.sqrt(np.mean((actual - exact) ** 2)) < 5e-3
    assert float(np.mean(actual)) == pytest.approx(1.0, abs=1e-12)
    _, centered, _ = _solve(128, 0.0001)
    centered_exact = periodic_sine_solution(
        x,
        0.4,
        length=1.0,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )
    centered_error = float(np.sqrt(np.mean((centered - centered_exact) ** 2)))
    upwind_error = float(np.sqrt(np.mean((actual - exact) ** 2)))
    # Then — la validation croisée passe et le schéma d'ordre 1 est moins précis.
    assert centered_error < upwind_error


def test_upwind_euler_rejects_unstable_time_step() -> None:
    """Un pas de temps violant la condition CFL amont/Euler est refusé."""
    # Given / When / Then — un pas de temps grossier (dt = 1,0) déclenche le
    # refus avant toute intégration.
    with pytest.raises(ValueError, match="stability condition"):
        solve_periodic_upwind_euler(n_cells=64, length=1.0, end_time=0.4, dt=1.0)


@pytest.mark.parametrize(
    ("modification", "message"),
    [
        ({"length": 0.0}, "strictly positive"),
        ({"length": float("nan")}, "finite"),
        ({"end_time": -0.1}, "non-negative"),
        ({"dt": 0.0}, "strictly positive"),
        ({"mean_concentration": 0.2, "amplitude": 0.3}, "non-negative"),
        ({"amplitude": -0.1}, "non-negative"),
        ({"n_cells": 16.0}, "greater than or equal to 8"),
    ],
)
def test_shared_validation_rejects_out_of_range_parameters(
    modification: dict[str, float], message: str
) -> None:
    """La validation partagée refuse chaque paramètre hors de son domaine."""
    # Given — le cas de référence et une seule modification invalide.
    parametres: dict[str, float] = {
        "n_cells": 16,
        "length": 1.0,
        "end_time": 0.1,
        "dt": 0.001,
        "mean_concentration": 1.0,
        "amplitude": 0.3,
        "velocity": 0.4,
        "diffusivity": 0.01,
    }
    parametres.update(modification)
    # When / Then — le solveur centré/RK4 refuse la configuration avant tout calcul.
    with pytest.raises(ValueError, match=message):
        solve_periodic_sine_transport(**parametres)


@pytest.mark.parametrize(
    ("modification", "message"),
    [
        ({"time": -0.5}, "non-negative"),
        ({"length": 0.0}, "strictly positive"),
        ({"length": float("inf")}, "finite"),
        ({"mean_concentration": 0.2, "amplitude": 0.3}, "non-negative"),
        ({"diffusivity": -1.0}, "non-negative"),
    ],
)
def test_exact_solution_rejects_invalid_parameters(
    modification: dict[str, float], message: str
) -> None:
    """La solution exacte refuse les paramètres hors de son domaine de définition."""
    # Given — une grille valide et une seule modification invalide.
    grille = np.linspace(0.0, 1.0, 8)
    parametres: dict[str, float] = {
        "time": 0.0,
        "length": 1.0,
        "mean_concentration": 1.0,
        "amplitude": 0.3,
        "velocity": 0.4,
        "diffusivity": 0.01,
    }
    parametres.update(modification)
    # When / Then — l'évaluation de la solution exacte est refusée.
    with pytest.raises(ValueError, match=message):
        periodic_sine_solution(grille, **parametres)


def test_exact_solution_rejects_non_finite_coordinates() -> None:
    """Une coordonnée non finie est refusée avant l'évaluation."""
    # Given — une grille contenant une valeur NaN, des paramètres valides.
    grille = np.array([0.0, 0.25, float("nan"), 0.75])
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="finite"):
        periodic_sine_solution(
            grille,
            0.0,
            length=1.0,
            mean_concentration=1.0,
            amplitude=0.3,
            velocity=0.4,
            diffusivity=0.01,
        )


def test_solvers_at_end_time_zero_return_the_initial_state() -> None:
    """À instant final nul, chaque solveur restitue l'état initial sans intégrer."""
    # Given — le cas de référence arrêté à t = 0.
    parametres = {
        "n_cells": 16,
        "length": 1.0,
        "end_time": 0.0,
        "dt": 0.001,
        "mean_concentration": 1.0,
        "amplitude": 0.3,
        "velocity": 0.4,
        "diffusivity": 0.01,
    }
    # When — les deux solveurs indépendants sont appelés.
    x_centre, c_centre, dt_centre = solve_periodic_sine_transport(**parametres)
    x_amont, c_amont, dt_amont = solve_periodic_upwind_euler(**parametres)
    initial = periodic_sine_solution(
        x_centre,
        0.0,
        length=1.0,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=0.4,
        diffusivity=0.01,
    )
    # Then — l'état initial est restitué à l'identique et le pas effectif est nul.
    assert dt_centre == 0.0
    assert dt_amont == 0.0
    assert np.array_equal(c_centre, initial)
    assert np.array_equal(c_amont, initial)
    assert np.array_equal(x_centre, x_amont)


def test_upwind_euler_handles_negative_velocity() -> None:
    """Le schéma amont/Euler traite aussi un vent négatif (advection selon -x)."""
    # Given — le cas de référence avec une vitesse négative.
    x, actual, _ = solve_periodic_upwind_euler(
        n_cells=128,
        length=1.0,
        end_time=0.4,
        dt=0.0001,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=-0.4,
        diffusivity=0.01,
    )
    # When — l'erreur RMS est mesurée contre la solution exacte correspondante.
    exact = periodic_sine_solution(
        x,
        0.4,
        length=1.0,
        mean_concentration=1.0,
        amplitude=0.3,
        velocity=-0.4,
        diffusivity=0.01,
    )
    erreur = float(np.sqrt(np.mean((actual - exact) ** 2)))
    # Then — l'erreur reste du même ordre que le cas de référence à vent positif.
    assert erreur < 5e-3
    assert float(np.mean(actual)) == pytest.approx(1.0, abs=1e-12)


def test_step_count_above_the_real_limit_is_rejected() -> None:
    """Une demande de plus de dix millions de pas est refusée sans intégrer."""
    # Given — end_time / dt exige plus de dix millions de pas.
    # When / Then — la garde réelle refuse la configuration immédiatement.
    with pytest.raises(ValueError, match="maximum"):
        solve_periodic_sine_transport(n_cells=16, length=1.0, end_time=1.0, dt=9e-8)


@pytest.mark.parametrize(
    "solveur",
    [solve_periodic_sine_transport, solve_periodic_upwind_euler],
)
def test_excessive_step_count_is_rejected_for_both_solvers(
    solveur: Callable[..., object], monkeypatch: pytest.MonkeyPatch
) -> None:
    """La garde partagée sur le nombre de pas protège les deux solveurs."""
    # Given — une garde abaissée à quatre pas et une demande de dix pas.
    monkeypatch.setattr(periodic_transport, "_MAXIMUM_STEPS", 4)
    # When / Then — chaque solveur refuse la configuration avant toute intégration.
    with pytest.raises(ValueError, match="maximum"):
        solveur(n_cells=16, length=1.0, end_time=1.0, dt=0.1)


@pytest.mark.parametrize(
    "solveur",
    [solve_periodic_sine_transport, solve_periodic_upwind_euler],
)
def test_step_ratio_overflow_is_rejected_as_value_error(solveur: Callable[..., object]) -> None:
    """Un rapport end_time/dt qui déborde devient une ValueError explicite."""
    # Given — un rapport end_time / dt hors de tout domaine représentable.
    # When / Then — la garde refuse avant que math.ceil ne déborde.
    with pytest.raises(ValueError, match="maximum"):
        solveur(n_cells=16, length=1.0, end_time=1e308, dt=1e-308)
