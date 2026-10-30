"""Regressions de la promotion des booleens aux frontieres des reliefs."""

import numpy as np
import pytest

from jdriftx.reliefs import ReliefMntAscii, ReliefPlat, ReliefSynthetique


@pytest.mark.parametrize("relief", [ReliefPlat(), ReliefSynthetique(kind="flat")])
@pytest.mark.parametrize("axe", ["x", "y"])
def test_reliefs_rejettent_les_booleens_meles_aux_reels(relief, axe: str) -> None:
    """Une sequence reelle/booleen mixte ne passe pas apres promotion NumPy."""
    # Given — un relief et une coordonnee melant un reel et un booleen.
    coordonnees = {"x": [0.0, 1.0], "y": [0.0, 0.0]}
    coordonnees[axe] = [0.0, True]
    # When / Then — l'evaluation est refusee avant toute promotion de type.
    with pytest.raises(ValueError, match="booleens exclus"):
        relief.altitude(**coordonnees)


@pytest.mark.parametrize("axe", ["x", "y"])
def test_mnt_rejette_les_booleens_meles_aux_reels(axe: str) -> None:
    """Le relief de grille ASCII applique le meme contrat strict de coordonnees."""
    # Given — un MNT valide et une coordonnee melant un reel et un booleen.
    relief = ReliefMntAscii(
        altitudes=np.zeros((2, 2), dtype=float),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )
    coordonnees = {"x": [0.0, 1.0], "y": [0.0, 0.0]}
    coordonnees[axe] = [0.0, True]
    # When / Then — l'evaluation est refusee avant toute promotion de type.
    with pytest.raises(ValueError, match="booleens exclus"):
        relief.altitude(**coordonnees)
