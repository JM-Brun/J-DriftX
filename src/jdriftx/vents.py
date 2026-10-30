"""Implémentations de champs de vent compatibles avec le contrat commun."""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Literal, overload

import numpy as np

from jdriftx._protocoles import Vent
from jdriftx.champ_analytique import ChampPlan


def _reel_fini(valeur: object, nom: str) -> float:
    """Convertit un scalaire reel en float fini, sinon leve ValueError."""
    if isinstance(valeur, bool) or not isinstance(valeur, Real):
        raise ValueError(f"{nom} doit etre un nombre reel (booleen exclu).")
    try:
        resultat = float(valeur)
    except (OverflowError, TypeError, ValueError) as err:
        raise ValueError(f"{nom} doit etre representable comme float fini.") from err
    if not math.isfinite(resultat):
        raise ValueError(f"{nom} doit etre fini.")
    return resultat


@overload
def _composantes_finies(
    valeurs: object, nombre: Literal[2], contexte: str
) -> tuple[float, float]: ...


@overload
def _composantes_finies(
    valeurs: object, nombre: Literal[3], contexte: str
) -> tuple[float, float, float]: ...


def _composantes_finies(
    valeurs: object, nombre: int, contexte: str
) -> tuple[float, ...]:
    """Valide un tuple de composantes reelles et finies, puis le normalise."""
    if not isinstance(valeurs, tuple) or len(valeurs) != nombre:
        raise ValueError(f"{contexte} doit retourner un tuple de {nombre} composantes.")
    return tuple(_reel_fini(valeur, f"{contexte} : composante") for valeur in valeurs)


@dataclass(frozen=True)
class AdaptateurTrajectoire2D:
    """Expose un vent stationnaire horizontal au contrat cinématique 2D.

    Le temps est ignore et la hauteur est fixee. L'adaptateur refuse tout
    vent avec une composante verticale non nulle : l'integrateur 2D ne
    pourrait pas representer ce mouvement sans perte physique.
    """

    vent: Vent
    hauteur: float

    def __post_init__(self) -> None:
        """Valide et normalise la hauteur fixe de l'echantillonnage."""
        object.__setattr__(self, "hauteur", _reel_fini(self.hauteur, "La hauteur d echantillonnage"))

    def __call__(self, _temps: float, x: float, y: float) -> tuple[float, float]:
        """Retourne (u, v) au point (x, y, hauteur), si w est nul."""
        u, v, w = _composantes_finies(
            self.vent.vitesse(x, y, self.hauteur), 3, "Le champ de vent"
        )
        if w != 0.0:
            msg = "Un vent vertical ne peut pas etre adapte a une trajectoire 2D."
            raise ValueError(msg)
        return u, v


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
        """Valide et normalise les composantes, sinon leve ValueError."""
        object.__setattr__(self, "u", _reel_fini(self.u, "La composante u du vent"))
        object.__setattr__(self, "v", _reel_fini(self.v, "La composante v du vent"))

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
        """Evalue le vent (u, v, 0) du champ plan au point (x, y).

        Raises:
            ValueError: si le champ delegue ne retourne pas deux composantes
                reelles finies.
        """
        u, v = _composantes_finies(self.champ.vitesse(x, y), 2, "Le champ plan")
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
        """Valide et normalise les parametres du profil."""
        u_reference = _reel_fini(self.u_reference, "La vitesse de reference")
        z_reference = _reel_fini(self.z_reference, "La hauteur de reference")
        exposant = _reel_fini(self.exposant, "L exposant")
        if u_reference <= 0.0:
            raise ValueError("La vitesse de reference doit etre strictement positive.")
        if z_reference <= 0.0:
            raise ValueError("La hauteur de reference doit etre strictement positive.")
        if not 0.0 <= exposant <= 1.0:
            raise ValueError("L exposant de la loi de puissance doit etre entre 0 et 1.")
        object.__setattr__(self, "u_reference", u_reference)
        object.__setattr__(self, "z_reference", z_reference)
        object.__setattr__(self, "exposant", exposant)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u(z), 0, 0) au point (x, y, z).

        Raises:
            ValueError: si z est invalide ou si la vitesse calculee n'est pas
                representable comme une valeur float64 finie et strictement positive.
        """
        z = _reel_fini(z, "La hauteur z")
        if z <= 0.0:
            raise ValueError("z doit etre strictement positif.")
        # Garder le calcul direct dans le domaine usuel pour preserver ses
        # arrondis ; ne passer au domaine logarithmique qu'en cas de perte
        # de representabilite d'un intermediaire ou du resultat direct.
        try:
            rapport = z / self.z_reference
            u = self.u_reference * rapport**self.exposant
        except OverflowError:
            u = math.inf
        if not np.isfinite(u) or u <= 0.0:
            log_u = math.log(self.u_reference) + self.exposant * (
                math.log(z) - math.log(self.z_reference)
            )
            try:
                u = math.exp(log_u)
            except OverflowError as err:
                msg = "Le profil de vent doit rester fini et strictement positif."
                raise ValueError(msg) from err
        if not np.isfinite(u) or u <= 0.0:
            msg = "Le profil de vent doit rester fini et strictement positif."
            raise ValueError(msg)
        return u, 0.0, 0.0


__all__ = [
    "AdaptateurTrajectoire2D",
    "VentDeChampPlan",
    "VentProfilPuissance",
    "VentUniforme",
]
