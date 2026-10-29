"""Squelette de benchmark de reference : cas analytique S0.

Cas S0 (docs/21, famille des cas synthetiques) : panache gaussien exact en
vent uniforme, la verite etant la solution de similitude du package
(jdriftx.similitude.concentration_panache). Ce squelette fournit :

1. une configuration typee et validee du cas (CasS0) ;
2. la grille de prelevements (arcs sous le vent x positions laterales) ;
3. la verite analytique exacte aux points de mesure ;
4. les metriques pre-enregistrees par l issue #43 (FAC2, NMSE), avec la
   convention choisie explicitee dans les docstrings ;
5. une evaluation reproductible de n importe quelle prediction contre la
   verite (evaluer_prediction), sans anticipation de resultat ;
6. une commande reproductible : uv run python -m jdriftx.benchmarks.reference,
   dont le passage a vide (prediction = verite) est un controle de coherence,
   PAS un resultat scientifique.

Garde-fous (issues #17 et #43) : le cas S0 n est pas une validation physique ;
aucun benchmark applicatif ne demarre tant que la porte G1 (inspection des
fichiers, issue #204) n est pas franchie ; les metriques et seuils de succes
G2/G3 sont pre-enregistres dans #43 et ne sont pas modifies ici.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.similitude import concentration_panache
from jdriftx.stabilite import ClasseStabilite

__all__ = [
    "CAS_S0_DEFAUT",
    "CasS0",
    "PointMesure",
    "ResultatS0",
    "evaluer_prediction",
    "fac2",
    "grille_mesures",
    "main",
    "mesurer_cout_inference",
    "nmse",
    "verite_s0",
]


@dataclass(frozen=True)
class CasS0:
    """Configuration validee du cas analytique S0.

    Attributs :
        debit : debit massique d emission (kg s^-1), strictement positif.
        u : vitesse du vent uniforme (m s^-1), strictement positive.
        classe : classe de stabilite de Pasquill (A a F).
        hauteur : hauteur effective de la source (m), positive ou nulle.
        arcs : distances sous le vent des arcs de mesure (m), toutes
            strictement positives, en ordre croissant strict.
        positions_laterales : coordonnees y des prelevements (m), non vide.
        z_mesure : altitude des prelevements (m), positive ou nulle.
    """

    debit: float
    u: float
    classe: str
    hauteur: float
    arcs: tuple[float, ...]
    positions_laterales: tuple[float, ...]
    z_mesure: float

    def __post_init__(self) -> None:
        """Valide les invariants du cas, sinon leve une ValueError."""
        if self.u <= 0.0:
            msg = "La vitesse du vent doit etre strictement positive."
            raise ValueError(msg)
        if self.debit <= 0.0:
            msg = "Le debit d emission doit etre strictement positif."
            raise ValueError(msg)
        if self.hauteur < 0.0:
            msg = "La hauteur de source doit etre positive ou nulle."
            raise ValueError(msg)
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
        ClasseStabilite(self.classe)


@dataclass(frozen=True)
class PointMesure:
    """Point de mesure (m) : distance sous le vent, laterale, altitude."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class ResultatS0:
    """Metriques d une prediction contre la verite S0 (sans unite).

    Attributs :
        fac2 : fraction des points avec 0.5 <= prediction/verite <= 2.
        nmse : erreur quadratique normalisee, voir la fonction nmse.
        effectif : nombre de points de mesure evalues.
    """

    fac2: float
    nmse: float
    effectif: int

    def vers_dict(self) -> dict[str, float | int]:
        """Export JSON aux frontieres du package (convention de la charte)."""
        return {"fac2": self.fac2, "nmse": self.nmse, "effectif": self.effectif}


def _cas_defaut() -> CasS0:
    """Cas S0 par defaut : vent 3 m/s, debit 2 kg/s, classe C, 4 arcs, 3 y."""
    return CasS0(
        debit=2.0,
        u=3.0,
        classe="C",
        hauteur=1.0,
        arcs=(100.0, 200.0, 400.0, 800.0),
        positions_laterales=(-50.0, 0.0, 50.0),
        z_mesure=1.5,
    )


CAS_S0_DEFAUT: CasS0 = _cas_defaut()


def grille_mesures(cas: CasS0) -> tuple[PointMesure, ...]:
    """Construit la grille croisee arcs x positions laterales a z_mesure."""
    return tuple(
        PointMesure(x=x, y=y, z=cas.z_mesure) for x in cas.arcs for y in cas.positions_laterales
    )


def verite_s0(cas: CasS0, points: tuple[PointMesure, ...]) -> np.ndarray:
    """Concentrations exactes (kg m^-3) de la solution de similitude.

    La verite S0 est la solution analytique du package elle-meme : aucun
    developpement mathematique n est duplique ici.
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
        debit=cas.debit,
        u=cas.u,
        classe=cas.classe,
        hauteur=cas.hauteur,
    )


def fac2(verite: ArrayLike, prediction: ArrayLike) -> float:
    """FAC2 : fraction des points avec 0.5 <= prediction/verite <= 2.

    Convention pre-enregistree (issue #43) : ratio point a point, bornes
    incluses ; toutes les valeurs de verite doivent etre strictement
    positives (le cas S0 le garantit).
    """
    vrais = np.asarray(verite, dtype=float)
    predits = np.asarray(prediction, dtype=float)
    if vrais.shape != predits.shape or vrais.ndim != 1:
        msg = "verite et prediction doivent etre des vecteurs 1D de meme taille."
        raise ValueError(msg)
    if vrais.size == 0:
        msg = "Au moins un point est requis pour FAC2."
        raise ValueError(msg)
    if np.any(vrais <= 0.0):
        msg = "FAC2 requiert des valeurs de verite strictement positives."
        raise ValueError(msg)
    ratios = predits / vrais
    return float(np.count_nonzero((ratios >= 0.5) & (ratios <= 2.0)) / vrais.size)


def nmse(verite: ArrayLike, prediction: ArrayLike) -> float:
    """NMSE = somme((prediction - verite)^2) / somme(verite^2).

    Convention explicite : d autres usages prennent somme(verite x prediction)
    au denominateur ; ce choix est documente pour eviter toute ambiguite.
    Toutes les valeurs de verite doivent etre strictement positives.
    """
    vrais = np.asarray(verite, dtype=float)
    predits = np.asarray(prediction, dtype=float)
    if vrais.shape != predits.shape or vrais.ndim != 1:
        msg = "verite et prediction doivent etre des vecteurs 1D de meme taille."
        raise ValueError(msg)
    if vrais.size == 0:
        msg = "Au moins un point est requis pour NMSE."
        raise ValueError(msg)
    if np.any(vrais <= 0.0):
        msg = "NMSE requiert des valeurs de verite strictement positives."
        raise ValueError(msg)
    return float(np.sum((predits - vrais) ** 2) / np.sum(vrais**2))


def evaluer_prediction(verite: ArrayLike, prediction: ArrayLike) -> ResultatS0:
    """Evalue une prediction contre la verite S0 (FAC2 et NMSE ensemble)."""
    vrais = np.asarray(verite, dtype=float)
    return ResultatS0(
        fac2=fac2(vrais, prediction),
        nmse=nmse(vrais, prediction),
        effectif=int(vrais.size),
    )


def mesurer_cout_inference(fonction: Callable[..., object], *args: object) -> float:
    """Mesure (s) le cout d un appel d inference ; mesure non deterministe.

    Le cout documente par l issue #17 distingue preparation et inference ;
    cette mesure n entre dans aucune assertion de test.
    """
    debut = time.perf_counter()
    fonction(*args)
    return float(time.perf_counter() - debut)


def main() -> dict[str, float | int]:
    """Controle de coherence du squelette : pas un resultat scientifique.

    Commande : uv run python -m jdriftx.benchmarks.reference.
    La prediction evaluee EST la verite : FAC2 = 1 et NMSE = 0 sont des
    controles d auto-coherence du pipeline, pas un resultat scientifique.
    """
    cas = _cas_defaut()
    points = grille_mesures(cas)
    vrais = verite_s0(cas, points)
    resultat = evaluer_prediction(vrais, vrais)
    return resultat.vers_dict()


if __name__ == "__main__":
    print(main())
