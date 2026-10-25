"""Tests physiques et numeriques des solutions de similitude."""

import numpy as np
import pytest

from jdriftx.similitude import (
    concentration_panache,
    concentration_puff,
    sigma_y,
    sigma_z,
)


@pytest.fixture
def grille() -> tuple[np.ndarray, np.ndarray]:
    """Grille laterale/verticale a x = 500 m."""
    y = np.linspace(-500.0, 500.0, 401)
    z = np.linspace(0.0, 400.0, 201)
    return y, z


def test_classe_invalide() -> None:
    """Une classe de stabilité inconnue est refusée."""
    # Given — une classe hors nomenclature de Pasquill.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="Classe de stabilite inconnue"):
        sigma_y(100.0, "Z")


def test_distance_negative() -> None:
    """Une distance sous le vent négative est refusée."""
    # Given — une distance strictement négative.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="positive ou nulle"):
        sigma_z(-1.0, "D")


def test_sigmas_croissants() -> None:
    """La dispersion ne peut que croitre avec la distance sous le vent."""
    # Given — une grille de distances sous le vent et les six classes.
    x = np.linspace(1.0, 10_000.0, 200)
    # When — les sigma_y et sigma_z sont évalués pour chaque classe.
    # Then — ils croissent strictement avec la distance pour chaque classe.
    for classe in ("A", "B", "C", "D", "E", "F"):
        assert np.all(np.diff(sigma_y(x, classe)) > 0.0)
        assert np.all(np.diff(sigma_z(x, classe)) > 0.0)


def test_positivite_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le panache gaussien est partout strictement positif."""
    # Given — une grille latérale/verticale à x = 500 m.
    y, z = grille
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le panache est évalué.
    c = concentration_panache(500.0, yy, zz, debit=1.0, u=3.0, classe="D")
    # Then — toutes les concentrations sont strictement positives.
    assert np.all(c > 0.0)


def test_symetrie_laterale(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le panache est symétrique par rapport à l'axe y = 0."""
    # Given — une grille latérale et son image miroir.
    y, _ = grille
    # When — le panache est évalué en y et en -y.
    gauche = concentration_panache(300.0, y, 2.0, 1.0, 3.0, "D")
    droite = concentration_panache(300.0, -y, 2.0, 1.0, 3.0, "D")
    # Then — les deux évaluations coïncident.
    assert np.allclose(gauche, droite)


def test_conservation_masse_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le flux integre u*C sur (y, z) doit restituer le debit emis (a 2 %)."""
    # Given — un panache de débit 1,5 dans un vent de 4 m/s.
    y, z = grille
    debit, u = 1.5, 4.0
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux intégré u*C est évalué sur la section (y, z).
    c = concentration_panache(1000.0, yy, zz, debit=debit, u=u, classe="D")
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le flux restitue le débit émis à 2 % relatif.
    assert flux == pytest.approx(debit, rel=0.02)


def test_positivite_puff() -> None:
    """Le puff gaussien est strictement positif au point évalué."""
    # Given / When — un puff est évalué en un point du domaine.
    c = concentration_puff(1500.0, 10.0, 5.0, t=500.0, masse=10.0, u=3.0, classe="C")
    # Then — la concentration est strictement positive.
    assert c > 0.0


def test_puff_temps_invalide() -> None:
    """Un instant nul ou négatif est refusé pour le puff."""
    # Given — un instant t = 0.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="strictement positif"):
        concentration_puff(100.0, 0.0, 0.0, t=0.0, masse=1.0, u=2.0, classe="D")
