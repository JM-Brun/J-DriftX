"""Tests for synthetic vector fields used by the interactive lab."""

import numpy as np
import pytest

from jdriftx.fields import vector_field


def test_uniform_field_has_constant_components() -> None:
    x, y = np.meshgrid(np.linspace(-1, 1, 3), np.linspace(-1, 1, 3))
    u, v = vector_field(x, y, "uniform", speed=2.0, angle_deg=90.0)
    assert np.allclose(u, 0.0, atol=1e-12)
    assert np.allclose(v, 2.0)


def test_shear_field_changes_horizontal_velocity_with_y() -> None:
    x, y = np.meshgrid(np.array([0.0, 1.0]), np.array([-1.0, 0.0, 1.0]))
    u, v = vector_field(x, y, "shear", speed=2.0, shear=0.5)
    assert np.allclose(u[:, 0], np.array([1.5, 2.0, 2.5]))
    assert np.allclose(v, 0.0)


def test_radial_field_is_zero_at_origin_and_scales_linearly() -> None:
    x = np.array([[0.0, 1.0], [0.0, -2.0]])
    y = np.array([[0.0, 0.0], [1.0, 0.0]])
    u, v = vector_field(x, y, "radial", radial_strength=3.0)
    assert u[0, 0] == pytest.approx(0.0)
    assert v[0, 0] == pytest.approx(0.0)
    assert u[1, 1] == pytest.approx(-6.0)
    assert v[1, 0] == pytest.approx(3.0)


def test_mismatched_coordinate_shapes_raise() -> None:
    with pytest.raises(ValueError, match="identical shapes"):
        vector_field(np.zeros((2, 2)), np.zeros((3, 3)), "uniform")


def test_non_finite_coordinates_raise() -> None:
    with pytest.raises(ValueError, match="finite"):
        vector_field(np.array([np.nan]), np.array([0.0]), "uniform")


def test_unknown_field_kind_raises() -> None:
    with pytest.raises(ValueError, match="Unknown field kind"):
        vector_field(np.zeros(2), np.zeros(2), "unknown")  # type: ignore[arg-type]
