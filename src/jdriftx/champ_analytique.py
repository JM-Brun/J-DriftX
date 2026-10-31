"""Champ plan incompressible à fonction de courant (phase 2, Fig. 1).

Un champ défini par une fonction de courant ψ est incompressible par
construction : u = ∂ψ/∂y et v = -∂ψ/∂x donnent ∇·u = 0 pour toute ψ
suffisamment régulière. Ce module fournit le champ cellulaire sinusoïdal
utilisé comme cas analytique pour vérifier l'intégration des trajectoires
(phase 2 du document d'architecture, Fig. 1 du chapitre de 2008). En champ
stationnaire, les trajectoires suivent les lignes de courant : ψ est conservé
le long d'une trajectoire exacte, ce qui fournit la référence de vérification.

La superposition de tels champs (classe ``SuperpositionChamps``) fournit un
second champ incompressible : deux champs très différents peuvent coïncider
en des points choisis, ce qui est le coeur de la reconstruction du vent à
deux mesures. Ce champ est un objet mathématique de vérification, pas une
reconstruction météorologique : un champ réel n'est pas déterminé par deux
mesures, et ce module ne simule ni relief, ni turbulence, ni couche limite.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol

import numpy as np


class ChampPlan(Protocol):
    """Interface structurelle d'un champ plan stationnaire à fonction de courant.

    Tout objet fournissant ``fonction_courant`` et ``vitesse`` avec ces
    signatures satisfait le protocole (typage structurel) : c'est le contrat
    partagé par les champs simples et leurs superpositions.
    """

    def fonction_courant(self, x: float, y: float) -> float:
        """Évalue ψ(x, y) en m² s⁻¹ pour deux coordonnées réelles finies."""
        ...

    def vitesse(self, x: float, y: float) -> tuple[float, float]:
        """Évalue (u, v) en m s⁻¹ pour deux coordonnées réelles finies."""
        ...


def _phase_periodique(coord: float, longueur: float) -> float:
    """Reduit une coordonnee modulo la longueur avant le calcul de phase."""
    return 2.0 * math.pi * (math.remainder(coord, longueur) / longueur)


def _produit_float64(*facteurs: float, sujet: str = "La vitesse du champ") -> float:
    """Multiplie des facteurs finis sans overflow intermediaire."""
    mantisse = 1.0
    exposant = 0
    for facteur in facteurs:
        if facteur == 0.0:
            return 0.0
        mantisse_facteur, exposant_facteur = math.frexp(facteur)
        mantisse *= mantisse_facteur
        exposant += exposant_facteur
        mantisse, correction = math.frexp(mantisse)
        exposant += correction
    try:
        resultat = math.ldexp(mantisse, exposant)
    except OverflowError as err:
        raise ValueError(f"{sujet} doit rester finie.") from err
    if not math.isfinite(resultat):
        raise ValueError(f"{sujet} doit rester finie.")
    if resultat == 0.0:
        raise ValueError(f"{sujet} est sous-representable en float64.")
    return resultat


def _verifie_coordonnees(x: float, y: float) -> None:
    """Refuse les coordonnées non finies avant toute évaluation du champ."""
    if any(isinstance(valeur, (bool, np.bool_)) for valeur in (x, y)):
        msg = "Les coordonnées doivent être numériques (booléens exclus)."
        raise ValueError(msg)
    if not (math.isfinite(x) and math.isfinite(y)):
        msg = "Les coordonnées doivent être finies."
        raise ValueError(msg)


@dataclass(frozen=True)
class ChampFonctionCourant:
    """Champ plan stationnaire incompressible à fonction de courant sinusoïdale.

    La fonction de courant est ψ(x, y) = amplitude · sin(k·x) · sin(k·y) avec
    k = 2π/longueur ; les cellules de recirculation sont périodiques de
    période ``longueur`` et les trajectoires suivent les lignes ψ = constante.

    Attributes:
        amplitude: amplitude de la fonction de courant (m² s⁻¹), finie et non nulle.
        longueur: longueur d'onde des cellules (m), finie et strictement positive.
    """

    amplitude: float
    longueur: float

    def __post_init__(self) -> None:
        """Valide l'invariant : amplitude finie non nulle, longueur finie positive.

        Raises:
            ValueError: si un parametre est non fini, nul, ou si le nombre
                d'onde deborde vers l'infini.
        """
        parametres = (self.amplitude, self.longueur)
        if any(isinstance(valeur, (bool, np.bool_)) for valeur in parametres):
            msg = "L'amplitude et la longueur doivent être numériques (booléens exclus)."
            raise ValueError(msg)
        if not math.isfinite(self.amplitude) or self.amplitude == 0.0:
            msg = "L'amplitude de la fonction de courant doit être finie et non nulle."
            raise ValueError(msg)
        if not math.isfinite(self.longueur) or self.longueur <= 0.0:
            msg = "La longueur d'onde doit être finie et strictement positive."
            raise ValueError(msg)
        if not math.isfinite(self.nombre_donde):
            msg = "Le nombre d'onde doit rester fini."
            raise ValueError(msg)

    @property
    def nombre_donde(self) -> float:
        """Nombre d'onde k = 2π/longueur en rad m⁻¹."""
        return 2.0 * math.pi / self.longueur

    def fonction_courant(self, x: float, y: float) -> float:
        """Évalue la fonction de courant ψ(x, y) en m² s⁻¹.

        Un facteur trigonométrique nul (bord ou centre de cellule) donne un
        zéro mathématique exact ; en revanche, un produit de facteurs non
        nuls sous-representable en float64 est refusé, comme pour la vitesse.

        Raises:
            ValueError: si les coordonnées ne sont pas finies ou si la valeur
                est sous-representable en float64.
        """
        _verifie_coordonnees(x, y)
        phase_x = _phase_periodique(x, self.longueur)
        phase_y = _phase_periodique(y, self.longueur)
        return _produit_float64(
            self.amplitude, math.sin(phase_x), math.sin(phase_y), sujet="La fonction de courant"
        )

    def vitesse(self, x: float, y: float) -> tuple[float, float]:
        """Évalue (u, v) = (∂ψ/∂y, -∂ψ/∂x) en m s⁻¹, divergence nulle par construction.

        Raises:
            ValueError: si les coordonnées ne sont pas finies ou si une
                composante de vitesse n'est pas representable en float64.
        """
        _verifie_coordonnees(x, y)
        k = self.nombre_donde
        phase_x = _phase_periodique(x, self.longueur)
        phase_y = _phase_periodique(y, self.longueur)
        sin_x, cos_x = math.sin(phase_x), math.cos(phase_x)
        sin_y, cos_y = math.sin(phase_y), math.cos(phase_y)
        u = _produit_float64(self.amplitude, k, sin_x, cos_y)
        v = -_produit_float64(self.amplitude, k, cos_x, sin_y)
        if not (math.isfinite(u) and math.isfinite(v)):
            msg = "La vitesse du champ doit rester finie."
            raise ValueError(msg)
        return u, v


@dataclass(frozen=True)
class SuperpositionChamps:
    """Superposition linéaire immuable de champs à fonction de courant.

    La superposition de champs incompressibles reste incompressible : les
    fonctions de courant s'additionnent, tout comme les composantes de
    vitesse. L'invariant est simplement la présence d'au moins un champ.

    Attributes:
        champs: tuple non vide de champs superposés, chacun satisfaisant le
            protocole ``ChampPlan`` : superpositions imbriquées et
            implémentations structurelles substituables.
    """

    champs: tuple[ChampPlan, ...]

    def __post_init__(self) -> None:
        """Valide l'invariant : au moins un champ, chacun exposant le protocole."""
        if not self.champs:
            msg = "La superposition exige au moins un champ."
            raise ValueError(msg)
        for champ in self.champs:
            if not callable(getattr(champ, "fonction_courant", None)) or not callable(
                getattr(champ, "vitesse", None)
            ):
                msg = "Chaque champ doit exposer fonction_courant et vitesse callable."
                raise TypeError(msg)

    def fonction_courant(self, x: float, y: float) -> float:
        """Évalue la somme des fonctions de courant au point (x, y).

        Raises:
            ValueError: si la somme deborde vers une valeur non finie.
        """
        total = 0.0
        for champ in self.champs:
            total += champ.fonction_courant(x, y)
        if not math.isfinite(total):
            msg = "La superposition doit rester finie."
            raise ValueError(msg)
        return total

    def vitesse(self, x: float, y: float) -> tuple[float, float]:
        """Évalue la somme des composantes de vitesse au point (x, y).

        Raises:
            ValueError: si une somme deborde vers une valeur non finie.
        """
        u = 0.0
        v = 0.0
        for champ in self.champs:
            du, dv = champ.vitesse(x, y)
            u += du
            v += dv
        if not (math.isfinite(u) and math.isfinite(v)):
            msg = "La superposition doit rester finie."
            raise ValueError(msg)
        return u, v
