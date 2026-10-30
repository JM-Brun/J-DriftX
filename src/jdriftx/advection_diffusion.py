"""Analytical reference case for one-dimensional advection-diffusion."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _contient_booleen(valeur: object) -> bool:
    """Détecte les booléens avant une éventuelle promotion numérique NumPy."""
    if isinstance(valeur, np.ndarray):
        if valeur.dtype.kind == "b":
            return True
        if valeur.dtype.kind != "O":
            return False
        valeurs = valeur
    else:
        valeurs = np.asarray(valeur, dtype=object)
    return any(isinstance(element, (bool, np.bool_)) for element in valeurs.flat)


def gaussian_advection_diffusion(
    x: NDArray[np.floating],
    time: float,
    *,
    mass: float = 1.0,
    initial_center: float = 0.0,
    velocity: float = 1.0,
    diffusivity: float = 0.1,
    initial_sigma: float = 0.5,
) -> NDArray[np.float64]:
    r"""Return the infinite-domain Gaussian solution of 1D advection-diffusion.

    Solves dc/dt + u dc/dx = K d²c/dx² for constant u and K >= 0,
    with initial concentration mass times Normal(initial_center, initial_sigma²).
    The integral over the real line remains mass and the variance is
    initial_sigma² + 2 K time.

    This is a mathematical reference case, not a complete atmospheric-dispersion
    model. The finite plotted domain may omit part of the Gaussian tail.
    """
    parameters = (time, mass, initial_center, velocity, diffusivity, initial_sigma)
    if any(isinstance(value, (bool, np.bool_)) for value in parameters):
        raise ValueError("Parameters must be numeric (booleans excluded).")
    if not all(np.isfinite(value) for value in parameters):
        raise ValueError("Parameters must be finite.")
    if time < 0:
        raise ValueError("time must be non-negative.")
    if mass < 0:
        raise ValueError("mass must be non-negative.")
    if diffusivity < 0:
        raise ValueError("diffusivity must be non-negative.")
    if initial_sigma <= 0:
        raise ValueError("initial_sigma must be strictly positive.")

    if _contient_booleen(x):
        raise ValueError("Coordinates must be numeric (booleans excluded).")
    x_arr = np.asarray(x, dtype=float)
    if not np.all(np.isfinite(x_arr)):
        raise ValueError("Coordinates must be finite.")
    variance = initial_sigma**2 + 2.0 * diffusivity * time
    center = initial_center + velocity * time
    return np.asarray(
        mass / np.sqrt(2.0 * np.pi * variance) * np.exp(-0.5 * (x_arr - center) ** 2 / variance),
        dtype=float,
    )
