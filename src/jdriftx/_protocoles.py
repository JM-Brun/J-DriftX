"""Protocoles structurels partagés par les composants du modèle.

Les interfaces sont séparées des implémentations afin de limiter le couplage
entre domaines et de rendre les dépendances explicites.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import ArrayLike, NDArray

@runtime_checkable
class Relief(Protocol):
    """Contrat d un relief : altitude du sol evaluee sur des grilles.

    Le contrat est vectorise (grilles de points, comme le rendu) : tout
    objet fournissant altitude avec cette signature satisfait le
    protocole, sans heritage.
    """

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Altitude du sol (m) aux points (x, y), formes identiques."""
        ...


@runtime_checkable
class Vent(Protocol):
    """Contrat d un champ de vent stationnaire, plan ou tridimensionnel.

    Le contrat est ponctuel (un point a la fois, comme l integration des
    trajectoires) : un champ plan renvoie w = 0, un champ 3D renseigne la
    composante verticale. Changer de modele de vent ne change pas les
    appelants.
    """

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Composantes (u, v, w) du vent (m s^-1) au point (x, y, z) (m)."""
        ...


@runtime_checkable
class ModeleConcentration(Protocol):
    """Contrat d un modele de concentration evaluable sur une grille."""

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Concentrations (kg m^-3) aux points (x, y, z)."""
        ...
