"""Time integration for particle trajectories in prescribed velocity fields.

This module integrates kinematics only. It does not model particle inertia,
turbulent dispersion, deposition, or feedback on the flow.
"""

from __future__ import annotations

from collections.abc import Callable
from numbers import Real
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
    Coordinates and time are in user-chosen consistent units. Every accepted
    step must advance representable time and produce finite coordinates. The
    velocity callback must return a tuple of two finite components; other
    sequence types (lists, arrays) are rejected on purpose.

    Raises:
        ValueError: If initial values, step parameters, method, or velocity
            output are invalid.
        FloatingPointError: If a step cannot be represented with finite
            coordinates or cannot advance floating-point time (explicit
            failure instead of silently truncating the trajectory).
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

    def rhs(time: float, px: float, py: float) -> tuple[float, float]:
        result = velocity(time, px, py)
        if not isinstance(result, tuple) or len(result) != 2:
            raise ValueError("velocity must return a pair of finite components.")
        if not all(isinstance(component, Real) and not isinstance(component, bool) for component in result):
            raise ValueError("velocity must return a pair of finite components.")
        components = (float(result[0]), float(result[1]))
        if not all(np.isfinite(component) for component in components):
            raise ValueError("velocity must return a pair of finite components.")
        return components

    times = [float(t0)]
    xs = [float(x0)]
    ys = [float(y0)]
    while times[-1] < t_end:
        time, x, y = times[-1], xs[-1], ys[-1]
        step = min(dt, t_end - time)
        next_time = time + step
        if next_time <= time:
            raise FloatingPointError(
                "dt is too small to advance time at the current floating-point magnitude."
            )

        if method == "euler":
            ux, uy = rhs(time, x, y)
            next_x, next_y = x + step * ux, y + step * uy
        else:
            k1x, k1y = rhs(time, x, y)
            k2x, k2y = rhs(time + step / 2, x + step * k1x / 2, y + step * k1y / 2)
            k3x, k3y = rhs(time + step / 2, x + step * k2x / 2, y + step * k2y / 2)
            k4x, k4y = rhs(time + step, x + step * k3x, y + step * k3y)
            next_x = x + step * (k1x + 2 * k2x + 2 * k3x + k4x) / 6
            next_y = y + step * (k1y + 2 * k2y + 2 * k3y + k4y) / 6

        if not np.isfinite(next_x) or not np.isfinite(next_y):
            raise FloatingPointError("Trajectory coordinates became non-finite during integration.")

        times.append(float(next_time))
        xs.append(float(next_x))
        ys.append(float(next_y))

    return (
        np.asarray(times, dtype=float),
        np.asarray(xs, dtype=float),
        np.asarray(ys, dtype=float),
    )
