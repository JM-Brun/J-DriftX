"""Tests physiques et numeriques des solutions de similitude."""

import numpy as np
import pytest

from jdriftx.similitude import (
    concentration_panache,
    concentration_puff,
    sigma_y,
    sigma_z,
)


@pytest.fixture()
def grille() -> tuple[np.ndarray, np.ndarray]:
    """Grille laterale/verticale a x = 500 m."""
    y = np.linspace(-500.0, 500.0, 401)
    z = np.linspace(0.0, 400.0, 201)
    return y, z


def test_classe_invalide() -> None:
    with pytest.raises(ValueError, match="Classe de stabilite inconnue"):
        sigma_y(100.0, "Z")


def test_distance_negative() -> None:
    with pytest.raises(ValueError, match="positive ou nulle"):
        sigma_z(-1.0, "D")


def test_sigmas_croissants() -> None:
    """La dispersion ne peut que croitre avec la distance sous le vent."""
    x = np.linspace(1.0, 10_000.0, 200)
    for classe in ("A", "B", "C", "D", "E", "F"):
        assert np.all(np.diff(sigma_y(x, classe)) > 0.0)
        assert np.all(np.diff(sigma_z(x, classe)) > 0.0)


def test_positivite_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    y, z = grille
    yy, zz = np.meshgrid(y, z, indexing="ij")
    c = concentration_panache(500.0, yy, zz, debit=1.0, u=3.0, classe="D")
    assert np.all(c > 0.0)


def test_symetrie_laterale(grille: tuple[np.ndarray, np.ndarray]) -> None:
    y, _ = grille
    gauche = concentration_panache(300.0, y, 2.0, 1.0, 3.0, "D")
    droite = concentration_panache(300.0, -y, 2.0, 1.0, 3.0, "D")
    assert np.allclose(gauche, droite)


def test_conservation_masse_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le flux integre u*C sur (y, z) doit restituer le debit emis (a 2 %)."""
    y, z = grille
    debit, u = 1.5, 4.0
    yy, zz = np.meshgrid(y, z, indexing="ij")
    c = concentration_panache(1000.0, yy, zz, debit=debit, u=u, classe="D")
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    assert flux == pytest.approx(debit, rel=0.02)


def test_positivite_puff() -> None:
    c = concentration_puff(1500.0, 10.0, 5.0, t=500.0, masse=10.0, u=3.0, classe="C")
    assert c > 0.0


def test_puff_temps_invalide() -> None:
    with pytest.raises(ValueError, match="strictement positif"):
        concentration_puff(100.0, 0.0, 0.0, t=0.0, masse=1.0, u=2.0, classe="D")
