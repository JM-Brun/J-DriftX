"""Tests for synthetic vector fields used by the interactive lab."""

import numpy as np
import pytest

from jdriftx.fields import vector_field


def test_uniform_field_has_constant_components() -> None:
    """Le champ uniforme a des composantes constantes selon l'angle donné."""
    # Given — une grille carrée et un vent uniforme à 90 degrés.
    x, y = np.meshgrid(np.linspace(-1, 1, 3), np.linspace(-1, 1, 3))
    # When — le champ est évalué.
    u, v = vector_field(x, y, "uniform", speed=2.0, angle_deg=90.0)
    # Then — le vent est purement vertical, de norme 2.
    assert np.allclose(u, 0.0, atol=1e-12)
    assert np.allclose(v, 2.0)


def test_shear_field_changes_horizontal_velocity_with_y() -> None:
    """Le champ de cisaillement varie linéairement avec y."""
    # Given — trois hauteurs y et un cisaillement de 0,5.
    x, y = np.meshgrid(np.array([0.0, 1.0]), np.array([-1.0, 0.0, 1.0]))
    # When — le champ est évalué.
    u, v = vector_field(x, y, "shear", speed=2.0, shear=0.5)
    # Then — u varie linéairement en y autour de la vitesse de 2 et v reste nul.
    assert np.allclose(u[:, 0], np.array([1.5, 2.0, 2.5]))
    assert np.allclose(v, 0.0)


def test_radial_field_is_zero_at_origin_and_scales_linearly() -> None:
    """Le champ radial est nul à l'origine et croît linéairement avec la distance."""
    # Given — quelques points dont l'origine et des points à distance 1 et 2.
    x = np.array([[0.0, 1.0], [0.0, -2.0]])
    y = np.array([[0.0, 0.0], [1.0, 0.0]])
    # When — le champ radial est évalué.
    u, v = vector_field(x, y, "radial", radial_strength=3.0)
    # Then — nul à l'origine et proportionnel à la position.
    assert u[0, 0] == pytest.approx(0.0)
    assert v[0, 0] == pytest.approx(0.0)
    assert u[1, 1] == pytest.approx(-6.0)
    assert v[1, 0] == pytest.approx(3.0)


def test_mismatched_coordinate_shapes_raise() -> None:
    """Des grilles x et y de formes différentes sont refusées."""
    # Given — deux grilles de formes incompatibles.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="identical shapes"):
        vector_field(np.zeros((2, 2)), np.zeros((3, 3)), "uniform")


def test_non_finite_coordinates_raise() -> None:
    """Des coordonnées non finies sont refusées."""
    # Given — une grille contenant un NaN.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="finite"):
        vector_field(np.array([np.nan]), np.array([0.0]), "uniform")


def test_unknown_field_kind_raises() -> None:
    """Un type de champ inconnu est refusé."""
    # Given — un type de champ hors de l'ensemble fermé.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="Unknown field kind"):
        vector_field(np.zeros(2), np.zeros(2), "unknown")  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", np.nan, np.inf])
def test_vector_field_rejects_non_real_or_non_finite_coordinates(bad: object) -> None:
    """Les coordonnées brutes sont réelles, finies et sans coercition booléenne."""
    with pytest.raises(ValueError):
        vector_field(np.array([bad]), np.array([0.0]), "uniform")


@pytest.mark.parametrize("bad", [True, np.bool_(True), 1.0 + 2.0j, "1.0", np.nan, np.inf])
@pytest.mark.parametrize("parameter", ["speed", "angle_deg", "shear", "radial_strength"])
def test_vector_field_rejects_non_real_or_non_finite_parameters(
    parameter: str, bad: object
) -> None:
    """Chaque paramètre scalaire suit le même contrat réel fini."""
    with pytest.raises(ValueError):
        vector_field(
            np.array([0.0]),
            np.array([0.0]),
            "uniform",
            **{parameter: bad},
        )


@pytest.mark.parametrize("coordinates", [[0.0, True], [0.0, 1.0 + 2.0j], ["0.0", "1.0"]])
def test_vector_field_rejects_mixed_or_non_numeric_coordinate_sequences(
    coordinates: list[object],
) -> None:
    """Les promotions NumPy ne masquent pas les booléens ou les complexes."""
    with pytest.raises(ValueError):
        vector_field(coordinates, [0.0, 0.0], "uniform")  # type: ignore[arg-type]


def test_vector_field_preserves_signed_real_parameters() -> None:
    """Les paramètres signés historiquement admis restent valides."""
    u, v = vector_field(
        np.array([1.0, -1.0]),
        np.array([2.0, -2.0]),
        "radial",
        radial_strength=-2.0,
    )
    np.testing.assert_array_equal(u, np.array([-2.0, 2.0]))
    np.testing.assert_array_equal(v, np.array([-4.0, 4.0]))
