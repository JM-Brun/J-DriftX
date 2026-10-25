"""Tests for the independent periodic advection-diffusion solver."""

import numpy as np
import pytest
from numpy.typing import NDArray

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
