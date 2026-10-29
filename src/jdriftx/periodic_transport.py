"""Periodic 1D advection-diffusion solved with an independent numerical scheme.

The solver uses centered finite differences in space and classical RK4 in time.
The sinusoidal exact solution is a verification target, not part of the solver.
"""

from __future__ import annotations

from math import ceil
from typing import Final

import numpy as np
from numpy.typing import NDArray

_FLOAT_EPS: Final[float] = 1e-10


def _validate_periodic_parameters(
    n_cells: int,
    length: float,
    end_time: float,
    dt: float,
    mean_concentration: float,
    amplitude: float,
    velocity: float,
    diffusivity: float,
) -> None:
    """Validate the parameters shared by both periodic solvers.

    The checks and error messages are common to the centered/RK4 and
    upwind/Euler schemes; the scheme-specific stability conditions remain
    in each solver.

    Raises:
        ValueError: If any parameter is non-finite or out of range, the grid
            is too coarse, or the concentration profile would be negative.
    """
    parameters = (length, end_time, dt, mean_concentration, amplitude, velocity, diffusivity)
    if not all(np.isfinite(value) for value in parameters):
        raise ValueError("Parameters must be finite.")
    if not isinstance(n_cells, int) or n_cells < 8:
        raise ValueError("n_cells must be an integer greater than or equal to 8.")
    if length <= 0:
        raise ValueError("length must be strictly positive.")
    if end_time < 0:
        raise ValueError("end_time must be non-negative.")
    if dt <= 0:
        raise ValueError("dt must be strictly positive.")
    if mean_concentration < 0 or amplitude < 0 or mean_concentration < amplitude:
        raise ValueError("Concentration must remain non-negative: mean >= amplitude >= 0.")
    if diffusivity < 0:
        raise ValueError("diffusivity must be non-negative.")


def _etat_initial_periodique(
    n_cells: int,
    length: float,
    *,
    mean_concentration: float,
    amplitude: float,
    velocity: float,
    diffusivity: float,
) -> tuple[NDArray[np.float64], float, NDArray[np.float64]]:
    """Build the periodic grid and the exact initial condition shared by both solvers.

    Returns (grid without duplicated endpoint, cell width, initial sine
    profile), i.e. the exact solution evaluated at t = 0. Shared preparation
    only: each solver keeps its own stability checks and time stepping.
    """
    dx = length / n_cells
    x = np.arange(n_cells, dtype=float) * dx
    initial = periodic_sine_solution(
        x,
        0.0,
        length=length,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    return x, dx, initial

def periodic_sine_solution(
    x: NDArray[np.floating],
    time: float,
    *,
    length: float,
    mean_concentration: float,
    amplitude: float,
    velocity: float,
    diffusivity: float,
) -> NDArray[np.float64]:
    """Evaluate the exact periodic sine solution for constant velocity/diffusivity.

    For k = 2*pi/length, the solution is
    mean + amplitude*exp(-K*k**2*t)*sin(k*(x-u*t)).
    """
    parameters = (time, length, mean_concentration, amplitude, velocity, diffusivity)
    if not all(np.isfinite(value) for value in parameters):
        raise ValueError("Parameters must be finite.")
    if time < 0:
        raise ValueError("time must be non-negative.")
    if length <= 0:
        raise ValueError("length must be strictly positive.")
    if mean_concentration < 0 or amplitude < 0 or mean_concentration < amplitude:
        raise ValueError("Concentration must remain non-negative: mean >= amplitude >= 0.")
    if diffusivity < 0:
        raise ValueError("diffusivity must be non-negative.")
    coordinates = np.asarray(x, dtype=float)
    if not np.all(np.isfinite(coordinates)):
        raise ValueError("Coordinates must be finite.")
    wave_number = 2.0 * np.pi / length
    decay = np.exp(-diffusivity * wave_number**2 * time)
    return np.asarray(
        mean_concentration
        + amplitude * decay * np.sin(wave_number * (coordinates - velocity * time)),
        dtype=float,
    )


def solve_periodic_sine_transport(
    *,
    n_cells: int,
    length: float,
    end_time: float,
    dt: float,
    mean_concentration: float = 1.0,
    amplitude: float = 0.5,
    velocity: float = 1.0,
    diffusivity: float = 0.02,
) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Solve periodic advection-diffusion using centered differences and RK4.

    Returns (periodic grid without a duplicated endpoint, final concentration,
    actual time step). The requested dt is an upper bound; the final step is
    adjusted so that the integration ends exactly at end_time.

    Raises:
        ValueError: For invalid parameters or a time step outside the RK4
            stability region for the discrete spatial operator.
    """
    _validate_periodic_parameters(
        n_cells=n_cells,
        length=length,
        end_time=end_time,
        dt=dt,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )

    x, dx, initial = _etat_initial_periodique(
        n_cells,
        length,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    if end_time == 0:
        return x, initial, 0.0

    n_steps = ceil(end_time / dt)
    actual_dt = end_time / n_steps

    # Eigenvalues of the periodic centered-difference advection-diffusion operator.
    theta = 2.0 * np.pi * np.arange(n_cells, dtype=float) / n_cells
    eigenvalues = (
        -1j * velocity * np.sin(theta) / dx - 4.0 * diffusivity * np.sin(theta / 2.0) ** 2 / dx**2
    )
    z = actual_dt * eigenvalues
    amplification = 1.0 + z + z**2 / 2.0 + z**3 / 6.0 + z**4 / 24.0
    if np.max(np.abs(amplification)) > 1.0 + _FLOAT_EPS:
        raise ValueError(
            "Requested dt is outside the RK4 stability region for this grid and parameters."
        )

    def rhs(concentration: NDArray[np.float64]) -> NDArray[np.float64]:
        right = np.roll(concentration, -1)
        left = np.roll(concentration, 1)
        first_derivative = (right - left) / (2.0 * dx)
        second_derivative = (right - 2.0 * concentration + left) / dx**2
        return -velocity * first_derivative + diffusivity * second_derivative

    concentration = initial.copy()
    for _ in range(n_steps):
        k1 = rhs(concentration)
        k2 = rhs(concentration + 0.5 * actual_dt * k1)
        k3 = rhs(concentration + 0.5 * actual_dt * k2)
        k4 = rhs(concentration + actual_dt * k3)
        concentration += actual_dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0

    return x, concentration, actual_dt


def solve_periodic_upwind_euler(
    *,
    n_cells: int,
    length: float,
    end_time: float,
    dt: float,
    mean_concentration: float = 1.0,
    amplitude: float = 0.5,
    velocity: float = 1.0,
    diffusivity: float = 0.02,
) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
    """Solve the same periodic problem with upwind advection and forward Euler.

    This first-order conservative scheme is an independent cross-check against
    the centered-space/RK4 solver. It requires |u|*dt/dx + 2*K*dt/dx**2 <= 1.
    """
    _validate_periodic_parameters(
        n_cells=n_cells,
        length=length,
        end_time=end_time,
        dt=dt,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )

    x, dx, concentration = _etat_initial_periodique(
        n_cells,
        length,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    if end_time == 0:
        return x, concentration, 0.0

    n_steps = ceil(end_time / dt)
    actual_dt = end_time / n_steps
    cfl = abs(velocity) * actual_dt / dx
    diffusion_number = diffusivity * actual_dt / dx**2
    if cfl + 2.0 * diffusion_number > 1.0 + _FLOAT_EPS:
        raise ValueError(
            "Requested dt violates the upwind-Euler stability condition "
            "|u|*dt/dx + 2*K*dt/dx**2 <= 1."
        )

    for _ in range(n_steps):
        right = np.roll(concentration, -1)
        left = np.roll(concentration, 1)
        if velocity >= 0:
            advection_gradient = (concentration - left) / dx
        else:
            advection_gradient = (right - concentration) / dx
        diffusion_laplacian = (right - 2.0 * concentration + left) / dx**2
        concentration -= actual_dt * velocity * advection_gradient
        concentration += actual_dt * diffusivity * diffusion_laplacian

    return x, concentration, actual_dt
