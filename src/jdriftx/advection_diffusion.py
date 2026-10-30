"""Analytical reference case for one-dimensional advection-diffusion."""

from __future__ import annotations

from math import exp, hypot, log, sqrt
from numbers import Real

import numpy as np
from numpy.typing import NDArray


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
    # Compute the standard deviation directly. Squaring initial_sigma or
    # forming 2*K*time can overflow/underflow even when sigma(t) is representable.
    diffusion_sigma = sqrt(2.0) * sqrt(diffusivity) * sqrt(time)
    sigma = hypot(initial_sigma, diffusion_sigma)
    if not np.isfinite(sigma):
        msg = "The effective Gaussian standard deviation is not representable as float64."
        raise ValueError(msg)

    center = initial_center + velocity * time
    if not np.isfinite(center):
        raise ValueError("The advected Gaussian center is not representable as float64.")

    # Evaluate the peak in the log domain: direct division can overflow,
    # while dividing mass by sqrt(2*pi) first can underflow prematurely.
    if mass == 0.0:
        peak = 0.0
    else:
        log_peak = log(mass) - 0.5 * log(2.0 * np.pi) - log(sigma)
        try:
            peak = exp(log_peak)
        except OverflowError as err:
            raise ValueError(
                "The peak Gaussian concentration is not representable as float64."
            ) from err

    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        standardized_distance = (x_arr - center) / sigma
        profile = np.exp(-0.5 * np.square(standardized_distance))
        concentration = peak * profile
    if not np.all(np.isfinite(concentration)):
        raise ValueError("The Gaussian concentration is not representable as finite float64.")
    return np.asarray(concentration, dtype=np.float64)
