"""Analytical reference case for one-dimensional advection-diffusion."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray




def _reel_fini(valeur: object, nom: str) -> float:
    """Valide un scalaire réel fini et représentable en float64."""
    if isinstance(valeur, (bool, np.bool_)) or not isinstance(valeur, Real):
        raise ValueError(f"{nom} must be a finite real scalar (booleans and complex values excluded).")
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
    if valeurs_brutes is not None and any(
        isinstance(element, (bool, np.bool_)) for element in valeurs_brutes.flat
    ):
        raise ValueError(f"{nom} must be a real numeric array (booleans excluded).")
    if brut.dtype.kind not in "iuf":
        raise ValueError(f"{nom} must be a real numeric array (complex and non-numeric values excluded).")
    try:
        with np.errstate(over="ignore", invalid="ignore"):
            resultat = np.asarray(brut, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} must be representable as float64.") from err
    if not np.all(np.isfinite(resultat)):
        raise ValueError(f"{nom} must contain only finite values.")
    return resultat


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
    time = _reel_fini(time, "time")
    mass = _reel_fini(mass, "mass")
    initial_center = _reel_fini(initial_center, "initial_center")
    velocity = _reel_fini(velocity, "velocity")
    diffusivity = _reel_fini(diffusivity, "diffusivity")
    initial_sigma = _reel_fini(initial_sigma, "initial_sigma")
    if time < 0:
        raise ValueError("time must be non-negative.")
    if mass < 0:
        raise ValueError("mass must be non-negative.")
    if diffusivity < 0:
        raise ValueError("diffusivity must be non-negative.")
    if initial_sigma <= 0:
        raise ValueError("initial_sigma must be strictly positive.")

    x_arr = _tableau_reel_fini(x, "Coordinates")
    variance = initial_sigma**2 + 2.0 * diffusivity * time
    center = initial_center + velocity * time
    return np.asarray(
        mass / np.sqrt(2.0 * np.pi * variance) * np.exp(-0.5 * (x_arr - center) ** 2 / variance),
        dtype=float,
    )
