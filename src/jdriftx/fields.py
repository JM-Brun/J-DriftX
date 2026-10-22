"""Synthetic vector fields for interactive exploration.

These fields are mathematical teaching examples, not meteorological simulations.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.typing import NDArray

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
    """Evaluate a simple 2D vector field on matching coordinate arrays.

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
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.shape != y_arr.shape:
        msg = "x and y must have identical shapes."
        raise ValueError(msg)
    if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
        msg = "Coordinates must be finite."
        raise ValueError(msg)
    if not np.isfinite(speed) or not np.isfinite(angle_deg) or not np.isfinite(shear):
        msg = "Field parameters must be finite."
        raise ValueError(msg)
    if not np.isfinite(radial_strength):
        msg = "radial_strength must be finite."
        raise ValueError(msg)

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
