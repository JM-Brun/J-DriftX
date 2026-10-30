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
    field or physical effect of terrain is inferred by this function. The grids
    x and y must share the same shape; NumPy broadcasting is not applied.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.shape != y_arr.shape:
        msg = "x and y must have identical shapes."
        raise ValueError(msg)
    if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
        msg = "x and y must contain only finite coordinates."
        raise ValueError(msg)
    parameters = (height, width, center_x, center_y)
    if not all(np.isfinite(value) for value in parameters):
        msg = "Terrain parameters must be finite."
        raise ValueError(msg)
    if width <= 0:
        msg = "width must be strictly positive."
        raise ValueError(msg)

    # Normaliser avant de mettre au carré évite le sous-débordement de width**2.
    # Les distances très grandes peuvent devenir infinies après normalisation ;
    # exp(-inf) vaut zéro, ce qui correspond à la limite du profil gaussien.
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        dx_scaled = (x_arr - center_x) / width
        dy_scaled = (y_arr - center_y) / width
        radius_squared = 0.5 * (dx_scaled**2 + dy_scaled**2)

    if kind == "flat":
        z = np.zeros_like(x_arr)
    elif kind == "hill":
        z = height * np.exp(-radius_squared)
    elif kind == "valley":
        z = -height * np.exp(-radius_squared)
    elif kind == "ridge":
        z = height * np.exp(-0.5 * dy_scaled**2)
    else:
        msg = f"Unknown terrain kind: {kind!r}."
        raise ValueError(msg)
    return np.asarray(z, dtype=float)
