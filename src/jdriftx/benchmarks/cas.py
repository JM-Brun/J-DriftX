"""Cas synthetiques a verite exacte : contrat commun, cas S0 et registre.

Famille des cas synthetiques de docs/21 (S0 a S3). Un cas fournit une
grille de prelevements et une verite exacte STRICTEMENT POSITIVE a ces
points. Le contrat (CasSynthetique) isole ce qui est general, le cas S0
(panache gaussien en vent uniforme, docs/21 S0-a) est la premiere
instance, et le registre (enregistrer_cas, lister_cas, construire_cas,
retirer_cas) permet d ajouter les cas suivants (S0-b a S0-d, S1, S2, S3)
sans toucher au pipeline d evaluation ni a la commande.

Garde-fous (issues #17 et #43) : un cas synthetique n est pas une
validation physique ; la verite du cas S0 est la solution de similitude
du package (jdriftx.similitude.concentration_panache) : aucun
developpement mathematique n est duplique.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar

import numpy as np

from jdriftx.similitude import concentration_panache
from jdriftx.source import SourcePanache

__all__ = [
    "CAS_S0_DEFAUT",
    "CasS0",
    "CasSynthetique",
    "PointMesure",
    "construire_cas",
    "enregistrer_cas",
    "lister_cas",
    "retirer_cas",
]


@dataclass(frozen=True)
class PointMesure:
    """Point de mesure (m) : distance sous le vent, laterale, altitude."""

    x: float
    y: float
    z: float


class CasSynthetique(ABC):
    """Contrat d un cas synthetique a verite exacte (docs/21, S0 a S3).

    Un cas expose un identifiant stable (commande, rapports), une grille
    de prelevements ordonnee et non vide, et une verite exacte
    strictement positive aux points de la grille (garantie exigee par
    les metriques pre-enregistrees de l issue #43). L enregistrement au
    registre verifie ces invariants : un cas invalide ne peut pas
    devenir silencieusement disponible.
    """

    identifiant: ClassVar[str]
    libelle: ClassVar[str]

    @abstractmethod
    def points(self) -> tuple[PointMesure, ...]:
        """Grille de prelevements du cas, ordonnee et non vide."""

    @abstractmethod
    def verite(self, points: tuple[PointMesure, ...]) -> np.ndarray:
        """Concentrations exactes (kg m^-3) aux points, strictement positives."""


@dataclass(frozen=True)
class CasS0(CasSynthetique):
    """Cas analytique S0 (docs/21, S0-a) : panache gaussien en vent uniforme.

    Attributs :
        source : valeur source du panache (debit, vent, classe, hauteur),
            dont les invariants sont portes par SourcePanache (docs/41).
        arcs : distances sous le vent des arcs de mesure (m), toutes
            strictement positives, en ordre croissant strict.
        positions_laterales : coordonnees y des prelevements (m), non vide.
        z_mesure : altitude des prelevements (m), positive ou nulle.
    """

    identifiant: ClassVar[str] = "S0"
    libelle: ClassVar[str] = "Panache gaussien en vent uniforme (docs/21, S0-a)"

    source: SourcePanache
    arcs: tuple[float, ...]
    positions_laterales: tuple[float, ...]
    z_mesure: float

    def __post_init__(self) -> None:
        """Valide les invariants du cas, sinon leve une ValueError.

        Les invariants de la source (debit, vent, classe, hauteur) sont
        portes par SourcePanache : le cas ne revalide pas ce que la
        valeur partagee garantit deja (docs/41).
        """
        if self.z_mesure < 0.0:
            msg = "L altitude de mesure doit etre positive ou nulle."
            raise ValueError(msg)
        if not self.arcs:
            msg = "Au moins un arc de mesure est requis."
            raise ValueError(msg)
        if any(a <= 0.0 for a in self.arcs):
            msg = "Les distances sous le vent doivent etre strictement positives."
            raise ValueError(msg)
        if any(self.arcs[i] >= self.arcs[i + 1] for i in range(len(self.arcs) - 1)):
            msg = "Les distances sous le vent doivent etre en ordre croissant strict."
            raise ValueError(msg)
        if not self.positions_laterales:
            msg = "Au moins une position laterale est requise."
            raise ValueError(msg)

    def points(self) -> tuple[PointMesure, ...]:
        """Grille croisee arcs x positions laterales a z_mesure."""
        return tuple(
            PointMesure(x=x, y=y, z=self.z_mesure)
            for x in self.arcs
            for y in self.positions_laterales
        )

    def verite(self, points: tuple[PointMesure, ...]) -> np.ndarray:
        """Concentrations exactes (kg m^-3) de la solution de similitude.

        La verite S0 est la solution analytique du package elle-meme :
        aucun developpement mathematique n est duplique ici.
        """
        if not points:
            msg = "Au moins un point de mesure est requis."
            raise ValueError(msg)
        xs = np.asarray([p.x for p in points], dtype=float)
        ys = np.asarray([p.y for p in points], dtype=float)
        zs = np.asarray([p.z for p in points], dtype=float)
        return concentration_panache(
            x=xs,
            y=ys,
            z=zs,
            debit=self.source.debit,
            u=self.source.u,
            classe=self.source.classe,
            hauteur=self.source.hauteur,
        )


_USINES: dict[str, Callable[[], CasSynthetique]] = {}


def enregistrer_cas(usine: Callable[[], CasSynthetique]) -> Callable[[], CasSynthetique]:
    """Enregistre une usine de cas apres verification des invariants.

    Verifications a l enregistrement : identifiant unique, grille non
    vide, verite strictement positive sur la grille. Une usine invalide
    leve une ValueError et ne modifie pas le registre.
    """
    cas = usine()
    if cas.identifiant in _USINES:
        msg = f"Le cas {cas.identifiant} est deja enregistre."
        raise ValueError(msg)
    points = cas.points()
    if not points:
        msg = f"Le cas {cas.identifiant} expose une grille vide."
        raise ValueError(msg)
    if np.any(cas.verite(points) <= 0.0):
        msg = f"Le cas {cas.identifiant} expose une verite non strictement positive."
        raise ValueError(msg)
    _USINES[cas.identifiant] = usine
    return usine


def lister_cas() -> tuple[str, ...]:
    """Identifiants des cas enregistres, en ordre alphabetique."""
    return tuple(sorted(_USINES))


def construire_cas(identifiant: str) -> CasSynthetique:
    """Construit le cas enregistre sous cet identifiant, sinon ValueError."""
    if identifiant not in _USINES:
        msg = f"Cas inconnu : {identifiant}. Cas enregistres : {', '.join(lister_cas())}."
        raise ValueError(msg)
    return _USINES[identifiant]()


def retirer_cas(identifiant: str) -> None:
    """Retire le cas enregistre sous cet identifiant, sinon ValueError."""
    if identifiant not in _USINES:
        msg = f"Le cas {identifiant} est absent du registre."
        raise ValueError(msg)
    del _USINES[identifiant]


CAS_S0_DEFAUT: CasS0 = CasS0(
    source=SourcePanache(debit=2.0, u=3.0, classe="C", hauteur=1.0),
    arcs=(100.0, 200.0, 400.0, 800.0),
    positions_laterales=(-50.0, 0.0, 50.0),
    z_mesure=1.5,
)

enregistrer_cas(lambda: CAS_S0_DEFAUT)
