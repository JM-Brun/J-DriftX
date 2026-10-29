"""Source du panache : valeur partagee par toutes les familles de cas S0.

Le concept de source etait duplique entre benchmarks/cas.py (CasS0) et
experiences/cas_synthetiques.py (CasSynthetiqueS0) : quatre champs
identiques (debit, vent, classe de stabilite, hauteur) valides deux
fois, avec un ecart de comportement (la classe n etait validee que du
cote des benchmarks). Le module isole le concept (docs/41) : chaque
famille compose sa configuration avec le meme objet SourcePanache, qui
porte seul les invariants de la source.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from jdriftx.stabilite import ClasseStabilite

__all__ = [
    "SourcePanache",
]


@dataclass(frozen=True)
class SourcePanache:
    """Valeur source d un panache gaussien (docs/41) : debit, vent, classe, hauteur.

    Attributs :
        debit : debit massique d emission (kg s^-1), strictement positif.
        u : vitesse du vent uniforme (m s^-1), strictement positive.
        classe : classe de stabilite de Pasquill (A a F).
        hauteur : hauteur effective de la source (m), positive ou nulle.
    """

    debit: float
    u: float
    classe: str
    hauteur: float

    def __post_init__(self) -> None:
        """Valide les invariants de la source, sinon leve une ValueError."""
        if not math.isfinite(self.debit) or self.debit <= 0.0:
            msg = "Le debit d emission doit etre fini et strictement positif."
            raise ValueError(msg)
        if not math.isfinite(self.u) or self.u <= 0.0:
            msg = "La vitesse du vent doit etre finie et strictement positive."
            raise ValueError(msg)
        if not math.isfinite(self.hauteur) or self.hauteur < 0.0:
            msg = "La hauteur de source doit etre finie et positive ou nulle."
            raise ValueError(msg)
        ClasseStabilite(self.classe)
