"""Implémentations de champs de vent compatibles avec le contrat commun."""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real

import numpy as np

from jdriftx._protocoles import Vent
from jdriftx.champ_analytique import ChampPlan


def _composantes_reelles_finies(
    resultat: object,
    nombre: int,
    description: str,
) -> tuple[float, ...]:
    """Valide une sortie de vitesse tuple de réels finis et la normalise."""
    if not isinstance(resultat, tuple) or len(resultat) != nombre:
        raise ValueError(description)
    if any(not isinstance(value, Real) or isinstance(value, bool) for value in resultat):
        raise ValueError(description)
    try:
        composantes = tuple(float(value) for value in resultat)
    except (OverflowError, ValueError) as err:
        raise ValueError(description) from err
    if not all(math.isfinite(value) for value in composantes):
        raise ValueError(description)
    return composantes


@dataclass(frozen=True)
class AdaptateurTrajectoire2D:
    """Expose un vent stationnaire horizontal au contrat cinématique 2D.

    Le temps est ignoré et la hauteur est fixée. L'adaptateur refuse tout
    vent avec une composante verticale non nulle : l'intégrateur 2D ne
    pourrait pas représenter ce mouvement sans perte physique.
    """

    vent: Vent
    hauteur: float

    def __post_init__(self) -> None:
        """Valide la hauteur fixe de l'échantillonnage."""
        if not isinstance(self.hauteur, Real) or isinstance(self.hauteur, bool):
            msg = "La hauteur d'échantillonnage doit être un réel fini."
            raise ValueError(msg)
        try:
            hauteur = float(self.hauteur)
        except (OverflowError, ValueError) as err:
            msg = "La hauteur d'échantillonnage doit être un réel fini."
            raise ValueError(msg) from err
        if not math.isfinite(hauteur):
            msg = "La hauteur d'échantillonnage doit être un réel fini."
            raise ValueError(msg)
        if not callable(getattr(self.vent, "vitesse", None)):
            msg = "Le vent doit exposer une méthode vitesse callable."
            raise TypeError(msg)
        object.__setattr__(self, "hauteur", hauteur)

    def __call__(self, _temps: float, x: float, y: float) -> tuple[float, float]:
        """Retourne (u, v) au point (x, y, hauteur), si w est nul."""
        u, v, w = _composantes_reelles_finies(
            self.vent.vitesse(x, y, self.hauteur),
            3,
            "Le champ de vent doit retourner trois composantes réelles finies.",
        )
        if w != 0.0:
            msg = "Un vent vertical ne peut pas être adapté à une trajectoire 2D."
            raise ValueError(msg)
        return float(u), float(v)


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

    def __post_init__(self) -> None:
        """Valide les méthodes requises par le protocole ChampPlan."""
        if not callable(getattr(self.champ, "fonction_courant", None)) or not callable(
            getattr(self.champ, "vitesse", None)
        ):
            msg = "Le champ doit exposer fonction_courant et vitesse callable."
            raise TypeError(msg)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u, v, 0) du champ plan au point (x, y).

        Raises:
            ValueError: si le champ delegue retourne une composante non finie.
        """
        u, v = _composantes_reelles_finies(
            self.champ.vitesse(x, y),
            2,
            "Le champ de vent doit retourner deux composantes réelles finies.",
        )
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
        """Evalue le vent (u(z), 0, 0) au point (x, y, z).

        Raises:
            ValueError: si z est invalide ou si la vitesse calculée n'est pas
                représentable comme une valeur float64 finie et strictement positive.
        """
        if not np.isfinite(z) or z <= 0.0:
            msg = "z doit être strictement positif ; la hauteur doit être finie."
            raise ValueError(msg)
        # Garder le calcul direct dans le domaine usuel pour préserver ses
        # arrondis ; ne passer au domaine logarithmique qu'en cas de perte
        # de représentabilité d'un intermédiaire ou du résultat direct.
        try:
            rapport = z / self.z_reference
            u = self.u_reference * rapport**self.exposant
        except OverflowError:
            # Ceinture de securite a priori inatteignable : avec un exposant
            # valide dans [0, 1] et des entrees finies, rapport ** exposant
            # ne peut pas deborder (la division flottante, elle, renvoie
            # inf sans lever). A reevaluer si le domaine de l exposant change.
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
