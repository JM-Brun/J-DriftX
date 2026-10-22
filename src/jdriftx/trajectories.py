"""Time integration for particle trajectories in prescribed velocity fields.

This module integrates kinematics only. It does not model particle inertia,
turbulent dispersion, deposition, or feedback on the flow.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

import numpy as np
from numpy.typing import NDArray

Velocity = Callable[[float, float, float], tuple[float, float]]
IntegrationMethod = Literal["euler", "rk4"]


def integrate_trajectory(
    velocity: Velocity,
    x0: float,
    y0: float,
    t0: float,
    t_end: float,
    dt: float,
    method: IntegrationMethod = "rk4",
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Integrate dx/dt=u(x,y,t), dy/dt=v(x,y,t) with Euler or classical RK4.

    The final step is shortened when the interval is not divisible by dt.
    Coordinates and time are in user-chosen consistent units.

    Raises:
        ValueError: If initial values or step parameters are invalid.
    """
    values = (x0, y0, t0, t_end, dt)
    if not all(np.isfinite(value) for value in values):
        raise ValueError("Initial values and time parameters must be finite.")
    if dt <= 0:
        raise ValueError("dt must be strictly positive.")
    if t_end < t0:
        raise ValueError("t_end must be greater than or equal to t0.")
    if method not in ("euler", "rk4"):
        raise ValueError(f"Unknown integration method: {method!r}.")

    times = [float(t0)]
    xs = [float(x0)]
    ys = [float(y0)]
    while times[-1] < t_end:
        t, x, y = times[-1], xs[-1], ys[-1]
        step = min(dt, t_end - t)

        def rhs(time: float, px: float, py: float) -> tuple[float, float]:
            result = velocity(time, px, py)
            if len(result) != 2 or not all(np.isfinite(value) for value in result):
                raise ValueError("velocity must return two finite components.")
            return float(result[0]), float(result[1])

        if method == "euler":
            ux, uy = rhs(t, x, y)
            next_x, next_y = x + step * ux, y + step * uy
        else:
            k1x, k1y = rhs(t, x, y)
            k2x, k2y = rhs(t + step / 2, x + step * k1x / 2, y + step * k1y / 2)
            k3x, k3y = rhs(t + step / 2, x + step * k2x / 2, y + step * k2y / 2)
            k4x, k4y = rhs(t + step, x + step * k3x, y + step * k3y)
            next_x = x + step * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
            next_y = y + step * (k1y + 2 * k2y + 2 * k3y + k4y) / 6

        times.append(float(t + step))
        xs.append(float(next_x))
        ys.append(float(next_y))

    return (
        np.asarray(times, dtype=float),
        np.asarray(xs, dtype=float),
        np.asarray(ys, dtype=float),
    )
