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

import math
from dataclasses import dataclass
from numbers import Real

from jdriftx.stabilite import ClasseStabilite

__all__ = [
    "SourcePanache",
]


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
        debit = _reel_fini(self.debit, "Le debit d emission")
        u = _reel_fini(self.u, "La vitesse du vent")
        hauteur = _reel_fini(self.hauteur, "La hauteur de source")
        if debit <= 0.0:
            raise ValueError("Le debit d emission doit etre strictement positif.")
        if u <= 0.0:
            raise ValueError("La vitesse du vent doit etre strictement positive.")
        if hauteur < 0.0:
            raise ValueError("La hauteur de source doit etre positive ou nulle.")
        try:
            ClasseStabilite(self.classe)
        except (TypeError, ValueError) as err:
            raise ValueError(f"Classe de stabilite invalide : {self.classe!r}.") from err
        object.__setattr__(self, "debit", debit)
        object.__setattr__(self, "u", u)
        object.__setattr__(self, "hauteur", hauteur)
