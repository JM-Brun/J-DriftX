"""Synthetic terrain surfaces for interactive teaching examples."""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.typing import NDArray


TerrainKind = Literal["flat", "hill", "valley", "ridge"]


def _scaled_coordinate_difference(
    values: NDArray[np.float64], center: float, width: float
) -> NDArray[np.float64]:
    """Calcule (values - center) / width sans débordement intermédiaire."""
    opposite_signs = np.signbit(values) != np.signbit(center)
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        # La soustraction directe est sûre pour des valeurs de même signe.
        direct = (values - center) / width
        # Pour des signes opposés, diviser avant de soustraire évite l'overflow.
        scaled = values / width - center / width
    return np.where(opposite_signs, scaled, direct)


def terrain_surface(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    kind: TerrainKind,
    height: float = 1.0,
    width: float = 1.5,
    center_x: float = 0.0,
    center_y: float = 0.0,
) -> NDArray[np.float64]:
    """Evaluate dimensionless synthetic terrain on matching finite real coordinates.

    Boolean and complex values, non-finite values and textual coercions are rejected.

    The returned values are teaching examples, not measured topography. No flow
    field or physical effect of terrain is inferred by this function. The grids
    x and y must share the same shape; NumPy broadcasting is not applied.
    """
    x_arr = _tableau_reel_fini(x, "x")
    y_arr = _tableau_reel_fini(y, "y")
    if x_arr.shape != y_arr.shape:
        msg = "x and y must have identical shapes."
        raise ValueError(msg)
    if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
        msg = "x and y must contain only finite coordinates."
        raise ValueError(msg)
    height = _reel_fini(height, "height")
    width = _reel_fini(width, "width")
    center_x = _reel_fini(center_x, "center_x")
    center_y = _reel_fini(center_y, "center_y")
    if width <= 0:
        msg = "width must be strictly positive."
        raise ValueError(msg)

    # Normaliser avant de mettre au carré évite le sous-débordement de width**2.
    # La soustraction est également ordonnée pour éviter un overflow préalable.
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        dx_scaled = _scaled_coordinate_difference(x_arr, center_x, width)
        dy_scaled = _scaled_coordinate_difference(y_arr, center_y, width)
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
