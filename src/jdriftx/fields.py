"""Synthetic vector fields for interactive exploration.

These fields are mathematical teaching examples, not meteorological simulations.
"""

from __future__ import annotations

from numbers import Real
from typing import Literal

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
        msg = f"{nom} must be a real numeric array (booleans and complex values excluded)."
        raise ValueError(msg)
    try:
        with np.errstate(over="ignore", invalid="ignore"):
            resultat = np.asarray(brut, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} must be representable as float64.") from err
    if not np.all(np.isfinite(resultat)):
        raise ValueError(f"{nom} must contain only finite coordinates.")
    return resultat


FieldKind = Literal["uniform", "shear", "radial"]


def vector_field(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    kind: FieldKind,
    speed: float = 1.0,
    angle_deg: float = 0.0,
    shear: float = 0.0,
    radial_strength: float = 1.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Evaluate a simple 2D vector field on matching finite real coordinate arrays.

    Boolean and complex values, non-finite values and textual coercions are rejected.

    Args:
        x: X coordinates on a grid.
        y: Y coordinates on the same grid.
        kind: Uniform flow, linear shear, or radial source/sink.
        speed: Base speed for uniform and shear fields.
        angle_deg: Direction of the uniform base flow, in degrees.
        shear: Horizontal velocity gradient with respect to y for shear flow.
        radial_strength: Signed radial scaling for the radial field.

    Returns:
        The horizontal and vertical velocity components, with the input shape.

    Raises:
        ValueError: If coordinates have different shapes or parameters are invalid.
    """
    x_arr = _tableau_reel_fini(x, "x")
    y_arr = _tableau_reel_fini(y, "y")
    if x_arr.shape != y_arr.shape:
        msg = "x and y must have identical shapes."
        raise ValueError(msg)
    speed = _reel_fini(speed, "speed")
    angle_deg = _reel_fini(angle_deg, "angle_deg")
    shear = _reel_fini(shear, "shear")
    radial_strength = _reel_fini(radial_strength, "radial_strength")

    angle = np.deg2rad(angle_deg)
    if kind == "uniform":
        u = np.full_like(x_arr, speed * np.cos(angle))
        v = np.full_like(y_arr, speed * np.sin(angle))
    elif kind == "shear":
        u = speed * np.cos(angle) + shear * y_arr
        v = np.full_like(y_arr, speed * np.sin(angle))
    elif kind == "radial":
        u = radial_strength * x_arr
        v = radial_strength * y_arr
    else:
        msg = f"Unknown field kind: {kind!r}."
        raise ValueError(msg)

    return np.asarray(u, dtype=float), np.asarray(v, dtype=float)
