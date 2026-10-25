"""Tests des contraintes physiques."""

import numpy as np

from jdriftx.constraints import linearite, positivite
from jdriftx.similitude import concentration_panache


def test_positivite_ok() -> None:
    """Un champ partout positif satisfait la contrainte de positivité."""
    # Given — un champ de concentration partout positif.
    champ = np.linspace(0.0, 1.0, 10)
    # When / Then — la contrainte est satisfaite.
    assert positivite(champ)


def test_positivite_echouee() -> None:
    """Un champ prenant des valeurs négatives viole la contrainte."""
    # Given — un champ prenant des valeurs négatives.
    champ = np.linspace(-1.0, 1.0, 10)
    # When / Then — la contrainte est violée.
    assert not positivite(champ)


def test_superposition_panache() -> None:
    """Le panache gaussien est lineaire en debit : multi-sources garanti."""
    # Given — un point du domaine et deux débits d'émission différents.
    point = (500.0, 25.0, 2.0)
    # When / Then — la linéarité en débit est vérifiée au point donné.
    assert linearite(
        concentration_panache,
        point,
        q1=1.0,
        q2=2.5,
        u=3.0,
        classe="D",
        hauteur=10.0,
    )
