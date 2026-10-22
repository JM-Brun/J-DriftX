"""Synthetic terrain surfaces for interactive teaching examples."""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.typing import NDArray

TerrainKind = Literal["flat", "hill", "valley", "ridge"]


def terrain_surface(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    kind: TerrainKind,
    height: float = 1.0,
    width: float = 1.5,
    center_x: float = 0.0,
    center_y: float = 0.0,
) -> NDArray[np.float64]:
    """Evaluate a dimensionless synthetic terrain elevation on a coordinate grid.

    The returned values are teaching examples, not measured topography. No flow
    field or physical effect of terrain is inferred by this function.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.shape != y_arr.shape:
        msg = "x and y must have identical shapes."
        raise ValueError(msg)
    parameters = (height, width, center_x, center_y)
    if not all(np.isfinite(value) for value in parameters):
        msg = "Terrain parameters must be finite."
        raise ValueError(msg)
    if width <= 0:
        msg = "width must be strictly positive."
        raise ValueError(msg)

    dx = x_arr - center_x
    dy = y_arr - center_y
    radius_squared = (dx**2 + dy**2) / (2.0 * width**2)
    if kind == "flat":
        z = np.zeros_like(x_arr)
    elif kind == "hill":
        z = height * np.exp(-radius_squared)
    elif kind == "valley":
        z = -height * np.exp(-radius_squared)
    elif kind == "ridge":
        z = height * np.exp(-(dy**2) / (2.0 * width**2))
    else:
        msg = f"Unknown terrain kind: {kind!r}."
        raise ValueError(msg)
    return np.asarray(z, dtype=float)
