"""Modèles de concentration et composition par superposition linéaire."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from jdriftx._protocoles import ModeleConcentration
from jdriftx.similitude import concentration_panache
from jdriftx.source import SourcePanache


@dataclass(frozen=True)
class PanacheGaussien:
    """Panache gaussien compose : la source porte les parametres (docs/41).

    Attributes:
        source: valeur source du panache (debit, vent, classe, hauteur).
    """

    source: SourcePanache

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Evalue les concentrations (kg m^-3) par delegation a la similitude."""
        return concentration_panache(
            x,
            y,
            z,
            debit=self.source.debit,
            u=self.source.u,
            classe=self.source.classe,
            hauteur=self.source.hauteur,
        )


@dataclass(frozen=True)
class SuperpositionPanaches:
    """Superposition lineaire (hypothese H8) de modeles de concentration.

    La concentration totale est la somme des concentrations : tout objet
    satisfaisant le contrat ModeleConcentration se combine, sans que les
    modeles se connaissent entre eux.

    Attributes:
        panaches: tuple non vide de modeles de concentration.
    """

    panaches: tuple[ModeleConcentration, ...]

    def __post_init__(self) -> None:
        """Valide l invariant : au moins un panache, sinon ValueError."""
        if not self.panaches:
            msg = "La superposition exige au moins un panache."
            raise ValueError(msg)

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Somme les concentrations (kg m^-3) des panaches superposes."""
        total = self.panaches[0].concentration(x, y, z)
        for panache in self.panaches[1:]:
            total = total + panache.concentration(x, y, z)
        return total

__all__ = [
    "PanacheGaussien",
    "SuperpositionPanaches",
]
