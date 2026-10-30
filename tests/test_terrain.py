"""Tests for synthetic terrain functions."""

from typing import Literal

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


def test_non_finite_coordinates_are_rejected() -> None:
    """Non-finite grid coordinates are rejected."""
    # Given — grids containing NaN or an infinity.
    x_mauvais = np.array([0.0, float("nan")])
    y_mauvais = np.array([0.0, float("inf")])
    # When / Then — the call is rejected instead of returning NaN.
    with pytest.raises(ValueError, match="finite coordinates"):
        terrain_surface(x_mauvais, np.zeros(2), "flat")
    with pytest.raises(ValueError, match="finite coordinates"):
        terrain_surface(np.zeros(2), y_mauvais, "flat")


@pytest.mark.parametrize("kind", ["hill", "valley", "ridge"])
def test_scaled_formulas_preserve_standard_terrain_profiles(
    kind: Literal["hill", "valley", "ridge"],
) -> None:
    """La normalisation conserve les profils analytiques aux échelles usuelles."""
    # Given — une grille et des paramètres loin des limites de représentation.
    x, y = np.meshgrid(np.array([-2.0, 0.5, 3.0]), np.array([-1.0, 1.5]))
    height, width = 2.5, 1.7
    center_x, center_y = 0.25, -0.5
    dx = x - center_x
    dy = y - center_y

    # When — le profil est calculé par la fonction et par sa formule directe.
    actual = terrain_surface(
        x,
        y,
        kind,
        height=height,
        width=width,
        center_x=center_x,
        center_y=center_y,
    )
    if kind == "ridge":
        expected = height * np.exp(-(dy**2) / (2.0 * width**2))
    else:
        radial_exponent = -(dx**2 + dy**2) / (2.0 * width**2)
        expected = height * np.exp(radial_exponent)
        if kind == "valley":
            expected = -expected

    # Then — la réécriture numérique conserve la formule de référence.
    np.testing.assert_allclose(actual, expected, rtol=1e-14, atol=1e-14)


@pytest.mark.parametrize(
    ("kind", "expected"),
    [("hill", 2.0), ("valley", -2.0), ("ridge", 2.0)],
)
def test_tiny_positive_width_remains_finite_at_terrain_center(
    kind: Literal["hill", "valley", "ridge"], expected: float
) -> None:
    """Une largeur très petite ne doit pas créer de NaN au centre du relief."""
    # Given — une largeur positive dont le carré sous-déborde en float64.
    coordinates = np.zeros((1, 1))
    width = 1.0e-200

    # When — le relief est évalué exactement en son centre.
    elevation = terrain_surface(
        coordinates,
        coordinates,
        kind,
        height=2.0,
        width=width,
    )

    # Then — la valeur au centre reste égale à la hauteur analytique.
    assert np.isfinite(elevation).all()
    assert elevation[0, 0] == pytest.approx(expected)


@pytest.mark.parametrize(
    ("kind", "x_value", "y_value", "expected"),
    [
        ("hill", 1.0e308, -1.0e308, 2.0 * np.exp(-2.0)),
        ("valley", 1.0e308, -1.0e308, -2.0 * np.exp(-2.0)),
        ("ridge", 0.0, 1.0e308, 2.0 * np.exp(-2.0)),
    ],
)
def test_opposite_extreme_coordinates_do_not_overflow_before_scaling(
    kind: Literal["hill", "valley", "ridge"],
    x_value: float,
    y_value: float,
    expected: float,
) -> None:
    """Les coordonnées de signes opposés sont normalisées avant leur soustraction."""
    # Given — des coordonnées finies dont la différence brute déborde en float64.
    x = np.array([[x_value]])
    y = np.array([[y_value]])

    # When — le centre est à l'opposé, avec une largeur de 1e308.
    elevation = terrain_surface(
        x,
        y,
        kind,
        height=2.0,
        width=1.0e308,
        center_x=-1.0e308,
        center_y=-1.0e308,
    )

    # Then — le quotient analytique vaut 2 et le profil reste fini.
    assert np.isfinite(elevation).all()
    assert elevation[0, 0] == pytest.approx(expected)


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", np.nan, np.inf])
def test_terrain_surface_rejects_non_real_or_non_finite_coordinates(bad: object) -> None:
    """Les coordonnées brutes sont réelles, finies et sans coercition booléenne."""
    with pytest.raises(ValueError):
        terrain_surface(np.array([bad]), np.array([0.0]), "hill")


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", np.nan, np.inf])
@pytest.mark.parametrize("parameter", ["height", "width", "center_x", "center_y"])
def test_terrain_surface_rejects_non_real_or_non_finite_parameters(
    parameter: str, bad: object
) -> None:
    """Chaque paramètre scalaire suit le même contrat réel fini."""
    with pytest.raises(ValueError):
        terrain_surface(
            np.array([0.0]),
            np.array([0.0]),
            "hill",
            **{parameter: bad},
        )


@pytest.mark.parametrize("coordinates", [[0.0, True], [0.0, 1.0 + 2.0j], ["0.0", "1.0"]])
def test_terrain_surface_rejects_mixed_or_non_numeric_coordinate_sequences(
    coordinates: list[object],
) -> None:
    """Les promotions NumPy ne masquent pas les booléens ou les complexes."""
    with pytest.raises(ValueError):
        terrain_surface(coordinates, [0.0, 0.0], "hill")  # type: ignore[arg-type]


def test_terrain_surface_preserves_signed_height_and_centers() -> None:
    """Les signes de hauteur et de coordonnées centrales restent libres."""
    result = terrain_surface(
        np.array([-1.0, 1.0]),
        np.array([0.0, 0.0]),
        "hill",
        height=-2.0,
        center_x=-1.0,
        center_y=-3.0,
    )
    assert result[0] == pytest.approx(-2.0)
