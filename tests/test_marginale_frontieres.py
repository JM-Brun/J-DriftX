"""Tests ciblés des frontières numériques de la marginale fermée du puff."""

from __future__ import annotations

import numpy as np
import pytest

from jdriftx.experiences.evaluation_puff import PUFF_DEFAUT
from jdriftx.experiences.reference_independante import PARAMETRES_EDP_DEFAUT, GrilleEdp
from jdriftx.experiences.transitoire_puff.marginale import MarginaleFermee


@pytest.mark.parametrize(
    "instant",
    [True, np.bool_(True), 0.0, -1.0, float("nan"), float("inf"), 1.0 + 2.0j, "1.0"],
)
def test_marginale_fermee_rejects_invalid_time(instant: object) -> None:
    """La marginale exige un instant réel fini strictement positif."""
    grille = GrilleEdp.depuis_parametres(PARAMETRES_EDP_DEFAUT)
    marginale = MarginaleFermee(source=PUFF_DEFAUT, grille=grille)
    with pytest.raises(ValueError, match=r"t must|strictly positive"):
        marginale.champ(instant)  # type: ignore[arg-type]


def test_marginale_fermee_rejects_unrepresentable_travel_distance() -> None:
    """Le produit u*t est contrôlé avant le calcul des écarts-types."""
    grille = GrilleEdp.depuis_parametres(PARAMETRES_EDP_DEFAUT)
    marginale = MarginaleFermee(source=PUFF_DEFAUT, grille=grille)
    with pytest.raises(ValueError, match="travel distance"):
        marginale.champ(1e308)
