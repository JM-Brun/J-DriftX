"""Regression tests for boolean promotion at public relief boundaries."""

import numpy as np
import pytest

from jdriftx.reliefs import ReliefMntAscii, ReliefPlat, ReliefSynthetique


@pytest.mark.parametrize("relief", [ReliefPlat(), ReliefSynthetique(kind="flat")])
@pytest.mark.parametrize("axe", ["x", "y"])
def test_reliefs_rejettent_les_booleens_meles_aux_reels(relief, axe: str) -> None:
    """Mixed real/bool coordinate sequences must not pass after NumPy promotion."""
    coordonnees = {"x": [0.0, 1.0], "y": [0.0, 0.0]}
    coordonnees[axe] = [0.0, True]
    with pytest.raises(ValueError, match="booleens exclus"):
        relief.altitude(**coordonnees)


@pytest.mark.parametrize("axe", ["x", "y"])
def test_mnt_rejette_les_booleens_meles_aux_reels(axe: str) -> None:
    """The ASCII-grid relief applies the same strict coordinate contract."""
    relief = ReliefMntAscii(
        altitudes=np.zeros((2, 2), dtype=float),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )
    coordonnees = {"x": [0.0, 1.0], "y": [0.0, 0.0]}
    coordonnees[axe] = [0.0, True]
    with pytest.raises(ValueError, match="booleens exclus"):
        relief.altitude(**coordonnees)
