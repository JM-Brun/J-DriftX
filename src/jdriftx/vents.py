"""Implémentations de champs de vent compatibles avec le contrat commun."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from jdriftx.champ_analytique import ChampPlan


@dataclass(frozen=True)
class VentUniforme:
    """Vent plan uniforme : composantes constantes, w nul.

    Attributes:
        u: composante sous le vent (m s^-1), finie.
        v: composante laterale (m s^-1), finie.
    """

    u: float
    v: float

    def __post_init__(self) -> None:
        """Valide la finitude des composantes, sinon leve une ValueError."""
        if not np.isfinite(self.u) or not np.isfinite(self.v):
            msg = "Les composantes du vent doivent etre finies."
            raise ValueError(msg)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Retourne le vent uniforme (u, v, 0) au point (x, y, z)."""
        return self.u, self.v, 0.0


@dataclass(frozen=True)
class VentDeChampPlan:
    """Adaptateur : un champ plan existant devient un vent du contrat.

    Tout objet satisfaisant le protocole ChampPlan (fonction_courant,
    vitesse) est adapte sans modification : la composante verticale est
    nulle. Les champs 2D et 3D s echangent derriere le meme contrat.

    Attributes:
        champ: champ plan stationnaire a adapter.
    """

    champ: ChampPlan

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u, v, 0) du champ plan au point (x, y)."""
        u, v = self.champ.vitesse(x, y)
        return u, v, 0.0


@dataclass(frozen=True)
class VentProfilPuissance:
    """Vent unidirectionnel en loi de puissance, standard de couche de surface.

    u(z) = u_reference * (z / z_reference) ** exposant : profil de vent
    standard des modeles de dispersion pour la couche de surface. La
    composante verticale est nulle ; le profil est defini pour z
    strictement positif.

    Attributes:
        u_reference: vitesse (m s^-1) a la hauteur de reference, positive.
        z_reference: hauteur de reference (m), strictement positive.
        exposant: exposant de la loi de puissance, entre 0 et 1.
    """

    u_reference: float
    z_reference: float
    exposant: float

    def __post_init__(self) -> None:
        """Valide les invariants du profil, sinon leve une ValueError."""
        if not np.isfinite(self.u_reference) or self.u_reference <= 0.0:
            msg = "La vitesse de reference doit etre finie strictement positive."
            raise ValueError(msg)
        if not np.isfinite(self.z_reference) or self.z_reference <= 0.0:
            msg = "La hauteur de reference doit etre finie strictement positive."
            raise ValueError(msg)
        if not 0.0 <= self.exposant <= 1.0:
            msg = "L exposant de la loi de puissance doit etre entre 0 et 1."
            raise ValueError(msg)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u(z), 0, 0) au point (x, y, z)."""
        if z <= 0.0:
            msg = "Le profil de puissance est defini pour z strictement positif."
            raise ValueError(msg)
        u = self.u_reference * (z / self.z_reference) ** self.exposant
        return u, 0.0, 0.0

__all__ = ["VentDeChampPlan", "VentProfilPuissance", "VentUniforme"]
