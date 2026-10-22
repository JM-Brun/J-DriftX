"""Tests for numerical particle trajectory integration."""

import numpy as np
import pytest

from jdriftx.trajectories import integrate_trajectory


def test_constant_velocity_is_integrated_exactly_by_both_methods() -> None:
    velocity = lambda _t, _x, _y: (2.0, -1.0)
    for method in ("euler", "rk4"):
        times, x, y = integrate_trajectory(velocity, 1.0, 3.0, 0.0, 1.0, 0.3, method)
        assert times[-1] == pytest.approx(1.0)
        assert x[-1] == pytest.approx(3.0)
        assert y[-1] == pytest.approx(2.0)


def test_rk4_is_more_accurate_than_euler_for_rotational_field() -> None:
    velocity = lambda _t, x, y: (-y, x)
    _, x_euler, y_euler = integrate_trajectory(velocity, 1.0, 0.0, 0.0, 2.0, 0.1, "euler")
    _, x_rk4, y_rk4 = integrate_trajectory(velocity, 1.0, 0.0, 0.0, 2.0, 0.1, "rk4")
    exact_x, exact_y = np.cos(2.0), np.sin(2.0)
    error_euler = np.hypot(x_euler[-1] - exact_x, y_euler[-1] - exact_y)
    error_rk4 = np.hypot(x_rk4[-1] - exact_x, y_rk4[-1] - exact_y)
    assert error_rk4 < error_euler


def test_invalid_step_is_rejected() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        integrate_trajectory(lambda _t, _x, _y: (1.0, 0.0), 0, 0, 0, 1, 0)


def test_invalid_velocity_output_is_rejected() -> None:
    with pytest.raises(ValueError, match="finite components"):
        integrate_trajectory(lambda _t, _x, _y: (np.nan, 0.0), 0, 0, 0, 1, 0.1)
