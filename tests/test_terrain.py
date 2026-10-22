"""Tests for synthetic terrain functions."""

import numpy as np
import pytest

from jdriftx.terrain import terrain_surface


def test_flat_terrain_is_zero_everywhere() -> None:
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    assert np.allclose(terrain_surface(x, y, "flat"), 0.0)


def test_hill_is_highest_at_its_center_and_symmetric() -> None:
    x, y = np.meshgrid(np.array([-1.0, 0.0, 1.0]), np.array([0.0]))
    z = terrain_surface(x, y, "hill", height=3.0, width=1.0)
    assert z[0, 1] == pytest.approx(3.0)
    assert z[0, 0] == pytest.approx(z[0, 2])
    assert z[0, 1] > z[0, 0]


def test_valley_is_negative_hill() -> None:
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    hill = terrain_surface(x, y, "hill")
    valley = terrain_surface(x, y, "valley")
    assert np.allclose(valley, -hill)


def test_ridge_is_constant_along_x() -> None:
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.array([0.0, 1.0]))
    z = terrain_surface(x, y, "ridge")
    assert np.allclose(z[0], z[0, 0])
    assert np.allclose(z[1], z[1, 0])
    assert z[0, 0] != pytest.approx(z[1, 0])


def test_non_positive_width_is_rejected() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        terrain_surface(np.zeros(2), np.zeros(2), "hill", width=0.0)


def test_mismatched_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="identical shapes"):
        terrain_surface(np.zeros((2, 2)), np.zeros((3, 3)), "flat")
