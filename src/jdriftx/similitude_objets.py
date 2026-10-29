"""API orientee objet pour les evaluations ponctuelles des modeles de similitude.

Les fonctions vectorisees de :mod:`jdriftx.similitude` restent le noyau numerique.
Ce module ajoute une couche de valeurs immuables et validees pour les appels
ponctuels, sans dupliquer les equations ni casser l'API historique.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from numpy.typing import NDArray
import numpy as np

from jdriftx.similitude import concentration_panache, concentration_puff
from jdriftx.stabilite import ClasseStabilite


@dataclass(frozen=True, slots=True)
class Point3D:
    """Point cartesien (x, y, z), en metres.

    Les coordonnees doivent etre finies. Aucune contrainte z >= 0 n'est imposee :
    les puffs gaussiens actuels sont definis sur R^3, tandis que le panache avec
    reflexion au sol est interprete physiquement pour z >= 0.
    """

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(value) for value in (self.x, self.y, self.z)):
            raise ValueError("Les coordonnees du point doivent etre finies.")


@dataclass(frozen=True, slots=True)
class ParametresPanache:
    """Parametres physiques d'un panache stationnaire gaussien.

    debit en kg/s, u en m/s, hauteur effective en m. Le debit nul est admis
    afin de representer explicitement une source eteinte.
    """

    debit: float
    u: float
    classe: ClasseStabilite | str
    hauteur: float = 0.0

    def __post_init__(self) -> None:
        if not math.isfinite(self.debit) or self.debit < 0.0:
            raise ValueError("Le debit doit etre fini et positif ou nul.")
        if not math.isfinite(self.u) or self.u <= 0.0:
            raise ValueError("La vitesse du vent doit etre finie et strictement positive.")
        if not math.isfinite(self.hauteur) or self.hauteur < 0.0:
            raise ValueError("La hauteur de source doit etre finie et positive ou nulle.")
        try:
            classe = ClasseStabilite(self.classe)
        except ValueError as err:
            raise ValueError(f"Classe de stabilite inconnue : {self.classe!r}") from err
        object.__setattr__(self, "classe", classe)


@dataclass(frozen=True, slots=True)
class ParametresPuff:
    """Parametres d'un puff gaussien : temps (s), masse (kg), vent (m/s)."""

    t: float
    masse: float
    u: float
    classe: ClasseStabilite | str
    x0: float = 0.0

    def __post_init__(self) -> None:
        if not math.isfinite(self.t) or self.t <= 0.0:
            raise ValueError("Le temps doit etre fini et strictement positif.")
        if not math.isfinite(self.masse) or self.masse < 0.0:
            raise ValueError("La masse doit etre finie et positive ou nulle.")
        if not math.isfinite(self.u) or self.u <= 0.0:
            raise ValueError("La vitesse du vent doit etre finie et strictement positive.")
        if not math.isfinite(self.x0):
            raise ValueError("La position initiale x0 doit etre finie.")
        try:
            classe = ClasseStabilite(self.classe)
        except ValueError as err:
            raise ValueError(f"Classe de stabilite inconnue : {self.classe!r}") from err
        object.__setattr__(self, "classe", classe)


def concentration_panache_au_point(
    point: Point3D, parametres: ParametresPanache
) -> float:
    """Evalue le panache en un point et retourne une concentration en kg/m^3.

    Le point est exprime dans le repere sous le vent du modele de similitude.
    Les distances x <= 0 sont refusees par le noyau numerique.
    """
    valeur = concentration_panache(
        x=point.x,
        y=point.y,
        z=point.z,
        debit=parametres.debit,
        u=parametres.u,
        classe=ClasseStabilite(parametres.classe).value,
        hauteur=parametres.hauteur,
    )
    return float(np.asarray(valeur).item())


def concentration_puff_au_point(
    point: Point3D, parametres: ParametresPuff
) -> float:
    """Evalue le puff en un point et retourne une concentration en kg/m^3."""
    valeur: NDArray[np.float64] = np.asarray(
        concentration_puff(
            x=point.x,
            y=point.y,
            z=point.z,
            t=parametres.t,
            masse=parametres.masse,
            u=parametres.u,
            classe=ClasseStabilite(parametres.classe).value,
            x0=parametres.x0,
        ),
        dtype=np.float64,
    )
    return float(valeur.item())


__all__ = [
    "Point3D",
    "ParametresPanache",
    "ParametresPuff",
    "concentration_panache_au_point",
    "concentration_puff_au_point",
]
