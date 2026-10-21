"""Tests des contraintes physiques."""

import numpy as np

from jdriftx.constraints import linearite, positivite
from jdriftx.similitude import concentration_panache


def test_positivite_ok() -> None:
    champ = np.linspace(0.0, 1.0, 10)
    assert positivite(champ)


def test_positivite_echouee() -> None:
    champ = np.linspace(-1.0, 1.0, 10)
    assert not positivite(champ)


def test_superposition_panache() -> None:
    """Le panache gaussien est lineaire en debit : multi-sources garanti."""
    point = (500.0, 25.0, 2.0)
    assert linearite(
        concentration_panache,
        point,
        q1=1.0,
        q2=2.5,
        u=3.0,
        classe="D",
        hauteur=10.0,
    )
