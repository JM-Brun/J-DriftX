"""Periodic 1D advection-diffusion solved with an independent numerical scheme.

The solver uses centered finite differences in space and classical RK4 in time.
The sinusoidal exact solution is a verification target, not part of the solver.
"""

from __future__ import annotations

from fractions import Fraction
from math import ceil, exp, log
from numbers import Integral, Real
from typing import Final

import numpy as np
from numpy.typing import NDArray

_FLOAT_EPS: Final[float] = 1e-10
_MAXIMUM_STEPS: Final[int] = 10_000_000


def _reel_fini(valeur: object, nom: str) -> float:
    """Valide un scalaire réel fini et représentable en float64."""
    if isinstance(valeur, (bool, np.bool_)) or not isinstance(valeur, Real):
        msg = f"{nom} must be a finite real scalar (booleans excluded; complex values excluded)."
        raise ValueError(msg)
    try:
        resultat = float(valeur)
    except (OverflowError, TypeError, ValueError) as err:
        raise ValueError(f"{nom} must be representable as finite float64.") from err
    if not np.isfinite(resultat):
        raise ValueError(f"{nom} must be finite.")
    return resultat


def _tableau_reel_fini(valeur: object, nom: str) -> NDArray[np.float64]:
    """Convertit un tableau réel en float64 sans coercition booléenne ou textuelle."""
    try:
        brut = np.asarray(valeur)
        valeurs_brutes = (
            np.asarray(valeur, dtype=object)
            if not isinstance(valeur, np.ndarray) or brut.dtype.kind == "O"
            else None
        )
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} must be a real numeric array.") from err
    if brut.dtype.kind == "b" or (
        valeurs_brutes is not None
        and any(isinstance(element, (bool, np.bool_)) for element in valeurs_brutes.flat)
    ):
        raise ValueError(f"{nom} must be a real numeric array (booleans excluded).")
    if brut.dtype.kind not in "iuf":
        msg = f"{nom} must be a real numeric array (booleans excluded; complex values excluded)."
        raise ValueError(msg)
    try:
        with np.errstate(over="ignore", invalid="ignore"):
            resultat = np.asarray(brut, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} must be representable as float64.") from err
    if not np.all(np.isfinite(resultat)):
        raise ValueError(f"{nom} must contain only finite coordinates.")
    return resultat


def _entier_cellules(valeur: object) -> int:
    """Valide un nombre entier de cellules représentable comme dimension NumPy."""
    if isinstance(valeur, (bool, np.bool_)) or not isinstance(valeur, Integral):
        raise ValueError("n_cells must be an integer greater than or equal to 8.")
    resultat = int(valeur)
    if resultat < 8:
        raise ValueError("n_cells must be an integer greater than or equal to 8.")
    if resultat > int(np.iinfo(np.intp).max):
        raise ValueError("n_cells must be representable as a NumPy array dimension.")
    return resultat


def _validate_periodic_parameters(
    n_cells: int,
    length: float,
    end_time: float,
    dt: float,
    mean_concentration: float,
    amplitude: float,
    velocity: float,
    diffusivity: float,
) -> tuple[int, float, float, float, float, float, float, float]:
    """Validate and normalize the parameters shared by both periodic solvers.

    The checks and error messages are common to the centered/RK4 and
    upwind/Euler schemes; the scheme-specific stability conditions remain
    in each solver.

    Raises:
        ValueError: If a parameter is non-real, non-finite, unrepresentable,
            or outside its existing domain, the grid is too coarse, or the
            requested number of time steps exceeds the safety limit.
    """
    n_cells = _entier_cellules(n_cells)
    length = _reel_fini(length, "length")
    end_time = _reel_fini(end_time, "end_time")
    dt = _reel_fini(dt, "dt")
    mean_concentration = _reel_fini(mean_concentration, "mean_concentration")
    amplitude = _reel_fini(amplitude, "amplitude")
    velocity = _reel_fini(velocity, "velocity")
    diffusivity = _reel_fini(diffusivity, "diffusivity")
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
    if end_time > 0.0:
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            step_ratio = np.float64(end_time) / np.float64(dt)
        if not np.isfinite(step_ratio) or ceil(float(step_ratio)) > _MAXIMUM_STEPS:
            raise ValueError(
                "The requested number of time steps exceeds the maximum of "
                f"{_MAXIMUM_STEPS}; reduce end_time or increase dt."
            )
    return (
        n_cells,
        length,
        end_time,
        dt,
        mean_concentration,
        amplitude,
        velocity,
        diffusivity,
    )


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



def _facteur_decroissance_periodique(diffusivity: float, length: float, time: float) -> float:
    """Évalue exp(-4*pi²*K*t/L²) sans former les produits ou carrés extrêmes."""
    if diffusivity == 0.0 or time == 0.0:
        return 1.0

    log_rate = (
        log(4.0 * np.pi**2)
        + log(diffusivity)
        + log(time)
        - 2.0 * log(length)
    )
    # exp(-rate) rounds to zero once rate is above this conservative threshold.
    if log_rate >= log(746.0):
        return 0.0
    rate = exp(log_rate)
    return exp(-rate)



def _phase_periodique(
    coordinates: NDArray[np.float64], velocity: float, time: float, length: float
) -> NDArray[np.float64]:
    """Réduit x-u*t modulo L avant de calculer la phase, sans former k*(x-u*t)."""
    displacement = velocity * time
    if np.isfinite(displacement):
        displacement_modulo = float(np.remainder(displacement, length))
    else:
        # Exact fallback: finite float inputs can have a non-representable product,
        # while its remainder modulo the finite period remains representable.
        exact_remainder = (
            Fraction.from_float(velocity) * Fraction.from_float(time)
        ) % Fraction.from_float(length)
        displacement_modulo = float(exact_remainder)

    with np.errstate(over="ignore", invalid="ignore"):
        coordinates_modulo = np.remainder(coordinates, length)
        relative_modulo = np.remainder(coordinates_modulo - displacement_modulo, length)
        phase = 2.0 * np.pi * (relative_modulo / length)
    return np.asarray(phase, dtype=np.float64)


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
    time = _reel_fini(time, "time")
    length = _reel_fini(length, "length")
    mean_concentration = _reel_fini(mean_concentration, "mean_concentration")
    amplitude = _reel_fini(amplitude, "amplitude")
    velocity = _reel_fini(velocity, "velocity")
    diffusivity = _reel_fini(diffusivity, "diffusivity")
    if time < 0:
        raise ValueError("time must be non-negative.")
    if length <= 0:
        raise ValueError("length must be strictly positive.")
    if mean_concentration < 0 or amplitude < 0 or mean_concentration < amplitude:
        raise ValueError("Concentration must remain non-negative: mean >= amplitude >= 0.")
    if diffusivity < 0:
        raise ValueError("diffusivity must be non-negative.")
    coordinates = _tableau_reel_fini(x, "Coordinates")
    decay = _facteur_decroissance_periodique(diffusivity, length, time)
    phase = _phase_periodique(coordinates, velocity, time, length)
    return np.asarray(
        mean_concentration + amplitude * decay * np.sin(phase),
        dtype=np.float64,
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
        ValueError: For invalid parameters, a time step outside the RK4
            stability region for the discrete spatial operator, or a step
            count above the safety limit.
    """
    (
        n_cells,
        length,
        end_time,
        dt,
        mean_concentration,
        amplitude,
        velocity,
        diffusivity,
    ) = _validate_periodic_parameters(
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
    The shared validation rejects a step count above the safety limit.
    """
    (
        n_cells,
        length,
        end_time,
        dt,
        mean_concentration,
        amplitude,
        velocity,
        diffusivity,
    ) = _validate_periodic_parameters(
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
