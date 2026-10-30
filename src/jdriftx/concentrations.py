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
        """Valide la collection et les implémentations du protocole."""
        if not isinstance(self.panaches, tuple):
            msg = "Les panaches doivent être fournis sous forme de tuple."
            raise TypeError(msg)
        if not self.panaches:
            msg = "La superposition exige au moins un panache."
            raise ValueError(msg)
        for index, panache in enumerate(self.panaches):
            if not isinstance(panache, ModeleConcentration) or not callable(
                getattr(panache, "concentration", None)
            ):
                msg = f"Le panache d'indice {index} ne satisfait pas ModeleConcentration."
                raise TypeError(msg)

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Somme les concentrations sur la forme broadcast des entrées.

        Chaque modèle doit renvoyer un ndarray de forme exactement égale à
        celle du broadcasting de x, y et z. Cette égalité évite qu'une
        addition NumPy masque une incohérence par broadcasting implicite.

        Raises:
            TypeError: si un modèle ne renvoie pas un ndarray flottant réel.
            ValueError: si les entrées ne sont pas broadcastables, si une
                sortie a une forme inattendue ou si la somme n'est pas finie.
        """
        try:
            forme_attendue = np.broadcast_shapes(np.shape(x), np.shape(y), np.shape(z))
        except ValueError as exc:
            msg = "Les formes de x, y et z doivent être broadcastables."
            raise ValueError(msg) from exc

        total: np.ndarray | None = None
        for index, panache in enumerate(self.panaches):
            concentration = panache.concentration(x, y, z)
            if not isinstance(concentration, np.ndarray):
                msg = f"Le panache d'indice {index} doit renvoyer un ndarray."
                raise TypeError(msg)
            if not np.issubdtype(concentration.dtype, np.floating):
                msg = (
                    f"La concentration du panache d'indice {index} doit être "
                    "un tableau flottant réel."
                )
                raise TypeError(msg)
            if concentration.shape != forme_attendue:
                msg = (
                    f"La concentration du panache d'indice {index} a la forme "
                    f"{concentration.shape}, attendue {forme_attendue}."
                )
                raise ValueError(msg)
            if total is None:
                total = concentration
            else:
                with np.errstate(over="ignore", invalid="ignore"):
                    total = total + concentration

        if total is None or not np.all(np.isfinite(total)):
            msg = "La superposition doit rester finie."
            raise ValueError(msg)
        return total


__all__ = [
    "PanacheGaussien",
    "SuperpositionPanaches",
]
