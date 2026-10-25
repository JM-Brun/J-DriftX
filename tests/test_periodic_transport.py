"""Tests for the independent periodic advection-diffusion solver."""

import numpy as np
from numpy.typing import NDArray
import pytest

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
    x, actual, _ = _solve(128, 0.0005)
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
    _, actual, _ = _solve(96, 0.0005)
    assert float(np.mean(actual)) == pytest.approx(1.0, abs=1e-12)


def test_spatial_refinement_reduces_error() -> None:
    errors = []
    for n_cells in (24, 48, 96):
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
    assert errors[2] < errors[1] < errors[0]
    observed_order = float(np.polyfit(np.log([1 / 24, 1 / 48, 1 / 96]), np.log(errors), 1)[0])
    assert 1.8 < observed_order < 2.2


def test_temporal_refinement_converges_to_fine_step_reference() -> None:
    n_cells = 48
    _, reference, _ = _solve(n_cells, 0.0003125)
    errors = []
    for dt in (0.02, 0.01, 0.005):
        _, actual, _ = _solve(n_cells, dt)
        errors.append(float(np.sqrt(np.mean((actual - reference) ** 2))))
    assert errors[2] < errors[1] < errors[0]
    observed_order = float(np.polyfit(np.log([0.02, 0.01, 0.005]), np.log(errors), 1)[0])
    assert 3.5 < observed_order < 4.5


def test_unstable_time_step_is_rejected() -> None:
    with pytest.raises(ValueError, match="stability region"):
        _solve(64, 1.0)


def test_invalid_grid_and_diffusivity_are_rejected() -> None:
    with pytest.raises(ValueError, match="greater than or equal to 8"):
        solve_periodic_sine_transport(n_cells=4, length=1, end_time=1, dt=0.01)
    with pytest.raises(ValueError, match="non-negative"):
        solve_periodic_sine_transport(
            n_cells=16, length=1, end_time=0.1, dt=0.001, diffusivity=-0.1
        )


def test_independent_upwind_euler_solver_matches_exact_solution() -> None:
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
    assert centered_error < upwind_error


def test_upwind_euler_rejects_unstable_time_step() -> None:
    with pytest.raises(ValueError, match="stability condition"):
        solve_periodic_upwind_euler(n_cells=64, length=1.0, end_time=0.4, dt=1.0)
