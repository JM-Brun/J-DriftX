"""Tests de stabilité numérique de la marginale gaussienne du puff."""

from __future__ import annotations

import numpy as np
import pytest

from jdriftx.experiences.evaluation_puff import PUFF_DEFAUT, SourceImpulsionnelle
from jdriftx.experiences.reference_independante import GrilleEdp
from jdriftx.experiences.transitoire_puff.marginale import MarginaleFermee
from jdriftx.similitude import sigma_y, sigma_z


def test_marginale_fermee_preserves_representable_peak_at_extreme_widths() -> None:
    """Le pic fini reste calculable malgré le sous-débordement de sy*sz."""
    source = SourceImpulsionnelle(masse=1e-300, u=3.0, classe="C")
    grille = GrilleEdp(
        abscisses_y=np.array([-1.0, 0.0, 1.0]),
        abscisses_z=np.array([0.0, 1.0]),
    )
    actual = MarginaleFermee(source=source, grille=grille).champ(1e-300)
    distance = source.u * 1e-300
    sy = float(sigma_y(distance, source.classe))
    sz = float(sigma_z(distance, source.classe))
    expected_peak = np.exp(
        np.log(source.masse) - np.log(2.0 * np.pi) - np.log(sy) - np.log(sz)
    )
    assert np.isfinite(actual[1, 0])
    assert actual[1, 0] == pytest.approx(expected_peak, rel=2e-14)


def test_marginale_fermee_matches_direct_formula_at_moderate_scales() -> None:
    """La formulation logarithmique est équivalente à la formule directe usuelle."""
    grille = GrilleEdp(
        abscisses_y=np.array([-50.0, 0.0, 50.0]),
        abscisses_z=np.array([0.0, 1.0, 2.0]),
    )
    source = PUFF_DEFAUT
    instant = 100.0
    sy = float(sigma_y(source.u * instant, source.classe))
    sz = float(sigma_z(source.u * instant, source.classe))
    mailles_y, mailles_z = grille.mailles()
    expected = (
        source.masse
        / (2.0 * np.pi * sy * sz)
        * np.exp(-(mailles_y**2) / (2.0 * sy**2))
        * np.exp(-(mailles_z**2) / (2.0 * sz**2))
    )
    actual = MarginaleFermee(source=source, grille=grille).champ(instant)
    np.testing.assert_allclose(actual, expected, rtol=2e-14, atol=0.0)


def test_marginale_fermee_rejects_unrepresentable_positive_peak() -> None:
    """Une concentration théorique hors float64 est refusée explicitement."""
    source = SourceImpulsionnelle(masse=1e308, u=3.0, classe="C")
    grille = GrilleEdp(
        abscisses_y=np.array([-1.0, 0.0, 1.0]),
        abscisses_z=np.array([0.0, 1.0]),
    )
    marginale = MarginaleFermee(source=source, grille=grille)
    with pytest.raises(ValueError, match="not representable"):
        marginale.champ(1e-300)
