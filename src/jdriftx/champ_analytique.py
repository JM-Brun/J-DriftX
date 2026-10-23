"""Champ plan incompressible à fonction de courant (phase 2, Fig. 1).

Un champ défini par une fonction de courant ψ est incompressible par
construction : u = ∂ψ/∂y et v = −∂ψ/∂x donnent ∇·u = 0 pour toute ψ
suffisamment régulière. Ce module fournit le champ cellulaire sinusoïdal
utilisé comme cas analytique pour vérifier l'intégration des trajectoires
(phase 2 du document d'architecture, Fig. 1 du chapitre de 2008). En champ
stationnaire, les trajectoires suivent les lignes de courant : ψ est conservé
le long d'une trajectoire exacte, ce qui fournit la référence de vérification.

Ce champ est un objet mathématique de vérification, pas une reconstruction
météorologique : un champ réel n'est pas déterminé par deux mesures, et ce
module ne simule ni relief, ni turbulence, ni couche limite.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


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
        """Valide l'invariant : amplitude finie non nulle, longueur finie positive."""
        if not math.isfinite(self.amplitude) or self.amplitude == 0.0:
            msg = "L'amplitude de la fonction de courant doit être finie et non nulle."
            raise ValueError(msg)
        if not math.isfinite(self.longueur) or self.longueur <= 0.0:
            msg = "La longueur d'onde doit être finie et strictement positive."
            raise ValueError(msg)

    @property
    def nombre_donde(self) -> float:
        """Nombre d'onde k = 2π/longueur en rad m⁻¹."""
        return 2.0 * math.pi / self.longueur

    def fonction_courant(self, x: float, y: float) -> float:
        """Évalue la fonction de courant ψ(x, y) en m² s⁻¹."""
        k = self.nombre_donde
        return self.amplitude * math.sin(k * x) * math.sin(k * y)

    def vitesse(self, x: float, y: float) -> tuple[float, float]:
        """Évalue (u, v) = (∂ψ/∂y, −∂ψ/∂x) en m s⁻¹, divergence nulle par construction."""
        k = self.nombre_donde
        u = self.amplitude * k * math.sin(k * x) * math.cos(k * y)
        v = -self.amplitude * k * math.cos(k * x) * math.sin(k * y)
        return u, v
