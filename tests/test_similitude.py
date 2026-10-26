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


@pytest.mark.parametrize(
    ("classe", "x"),
    [
        ("A", 1000.0),
        ("B", 1000.0),
        ("C", 1000.0),
        ("D", 1000.0),
        ("E", 1000.0),
        ("F", 1000.0),
        ("D", 200.0),
        ("D", 5000.0),
    ],
)
def test_conservation_masse_panache_toutes_classes(classe: str, x: float) -> None:
    """Le flux integre restitue le debit emis pour six classes et plusieurs distances."""
    # Given — un panache de debit 1,5 kg/s dans un vent de 4 m/s, grille adaptee a 4 sigma.
    debit, u = 1.5, 4.0
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, 4.0 * sz, 121)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux u*C est integre sur la section transversale.
    c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le debit emis est restitue a 0,1 % relatif.
    assert flux == pytest.approx(debit, rel=1e-3)


def test_conservation_masse_panache_hauteur_non_nulle() -> None:
    """Une source en hauteur avec reflexion au sol conserve le debit emis."""
    # Given — un panache de classe D emis a 30 m de hauteur, x = 1000 m.
    debit, u, h = 2.0, 4.0, 30.0
    x, classe = 1000.0, "D"
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, h + 4.0 * sz, 161)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux est integre sur la section avec le terme de reflexion.
    c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe, hauteur=h)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le debit emis est restitue a 0,1 % relatif.
    assert flux == pytest.approx(debit, rel=1e-3)


def test_conservation_masse_puff() -> None:
    """L'integrale volumique du puff restitue la masse emise."""
    # Given — un puff de 10 kg apres 500 s de transport (classe C, vent 3 m/s).
    masse, u, t, classe = 10.0, 3.0, 500.0, "C"
    distance = u * t
    s = float(sigma_y(distance, classe))
    sz = float(sigma_z(distance, classe))
    n = 81
    x = np.linspace(distance - 4.0 * s, distance + 4.0 * s, n)
    y = np.linspace(-4.0 * s, 4.0 * s, n)
    z = np.linspace(-4.0 * sz, 4.0 * sz, n)
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")
    # When — la concentration est integree sur le volume.
    c = concentration_puff(xx, yy, zz, t=t, masse=masse, u=u, classe=classe)
    integrale = np.trapezoid(np.trapezoid(np.trapezoid(c, x, axis=0), y, axis=0), z)
    # Then — la masse emise est restituee a 0,1 % relatif.
    assert integrale == pytest.approx(masse, rel=1e-3)


def test_conservation_masse_superposition_deux_panaches() -> None:
    """Le flux d'une superposition de deux panaches est la somme des debits."""
    # Given — deux panaches de classe D, debits et hauteurs differents.
    debit1, debit2, u, x, classe = 1.2, 0.8, 4.0, 1000.0, "D"
    h1, h2 = 0.0, 30.0
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, h2 + 4.0 * sz, 161)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — la superposition des deux panaches est integree sur la section.
    c = concentration_panache(x, yy, zz, debit=debit1, u=u, classe=classe, hauteur=h1)
    c += concentration_panache(x, yy, zz, debit=debit2, u=u, classe=classe, hauteur=h2)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — la somme des debits emis est restituee a 0,1 % relatif.
    assert flux == pytest.approx(debit1 + debit2, rel=1e-3)


def test_convergence_elargissement_grille() -> None:
    """L'erreur relative du bilan de masse decroit quand la grille s'elargit."""
    # Given — un panache de classe D a x = 1000 m et trois etendues de grille.
    debit, u, x, classe = 1.5, 4.0, 1000.0, "D"
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    erreurs = []
    for k in (2.0, 3.0, 4.0):
        y = np.linspace(-k * sy, k * sy, 241)
        z = np.linspace(0.0, k * sz, 121)
        yy, zz = np.meshgrid(y, z, indexing="ij")
        # When — le flux est integre pour chaque etendue k * sigma.
        c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe)
        flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
        erreurs.append(abs(flux - debit) / debit)
    # Then — l'erreur decroit strictement avec l'elargissement et reste sous
    # 0,1 % a quatre sigma : elle est dominee par la troncature du domaine,
    # pas par le pas de discretisation.
    assert erreurs[0] > erreurs[1] > erreurs[2]
    assert erreurs[2] < 1e-3


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
