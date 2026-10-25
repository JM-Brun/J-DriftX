"""Tests for synthetic terrain functions."""

import numpy as np
import pytest

from jdriftx.terrain import terrain_surface


def test_flat_terrain_is_zero_everywhere() -> None:
    """Le terrain plat est nul partout."""
    # Given — une grille carrée.
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    # When / Then — le terrain plat est identiquement nul.
    assert np.allclose(terrain_surface(x, y, "flat"), 0.0)


def test_hill_is_highest_at_its_center_and_symmetric() -> None:
    """La colline est maximale en son centre et symétrique."""
    # Given — une coupe de la colline par son centre.
    x, y = np.meshgrid(np.array([-1.0, 0.0, 1.0]), np.array([0.0]))
    # When — la colline est évaluée (hauteur 3, largeur 1).
    z = terrain_surface(x, y, "hill", height=3.0, width=1.0)
    # Then — le maximum est au centre, les flancs sont symétriques.
    assert z[0, 1] == pytest.approx(3.0)
    assert z[0, 0] == pytest.approx(z[0, 2])
    assert z[0, 1] > z[0, 0]


def test_valley_is_negative_hill() -> None:
    """La vallée est l'opposée exacte de la colline."""
    # Given — une grille carrée et les deux types de terrain.
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    # When — la colline et la vallée sont évaluées aux mêmes points.
    hill = terrain_surface(x, y, "hill")
    valley = terrain_surface(x, y, "valley")
    # Then — la vallée est le négatif exact de la colline.
    assert np.allclose(valley, -hill)


def test_ridge_is_constant_along_x() -> None:
    """La crête est constante le long de x."""
    # Given — une grille à deux lignes.
    x, y = np.meshgrid(np.linspace(-2, 2, 5), np.array([0.0, 1.0]))
    # When — la crête est évaluée.
    z = terrain_surface(x, y, "ridge")
    # Then — chaque ligne est constante en x et les deux lignes diffèrent.
    assert np.allclose(z[0], z[0, 0])
    assert np.allclose(z[1], z[1, 0])
    assert z[0, 0] != pytest.approx(z[1, 0])


def test_non_positive_width_is_rejected() -> None:
    """Une largeur non positive est refusée."""
    # Given — une largeur nulle pour une colline.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="strictly positive"):
        terrain_surface(np.zeros(2), np.zeros(2), "hill", width=0.0)


def test_mismatched_shapes_are_rejected() -> None:
    """Des grilles de formes différentes sont refusées."""
    # Given — deux grilles de formes incompatibles.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="identical shapes"):
        terrain_surface(np.zeros((2, 2)), np.zeros((3, 3)), "flat")
