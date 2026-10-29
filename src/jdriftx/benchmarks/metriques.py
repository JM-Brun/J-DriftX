"""Metriques d erreur pre-enregistrees (FAC2, NMSE) et registre extensible.

Les deux metriques exigees par l issue #43 (FAC2, NMSE) sont definies
avec des conventions explicites et documentees, puis exposees par un
registre (METRIQUES, METRIQUES_DEFAUT) que le pipeline d evaluation
consomme. Ajouter une metrique suppose de pre-enregistrer son seuil de
succes (G2/G3) AVANT tout benchmark : le registre rend l ajout possible,
pas automatique.

Alignement documentaire : FAC2 et NMSE sont les metriques usuelles de
l evaluation des modeles de dispersion (Model Validation Kit de
l initiative Harmonisation, logiciel BOOT ; guide ASTM D6589).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

__all__ = [
    "FAC2",
    "METRIQUES",
    "METRIQUES_DEFAUT",
    "NMSE",
    "Metrique",
    "calculer_metriques",
    "enregistrer_metrique",
    "fac2",
    "nmse",
    "retirer_metrique",
]


def _vecteurs_verifies(
    verite: ArrayLike, prediction: ArrayLike, nom: str
) -> tuple[np.ndarray, np.ndarray]:
    """Convertit et valide : 1D, meme taille, non vides, verite > 0."""
    vrais = np.asarray(verite, dtype=float)
    predits = np.asarray(prediction, dtype=float)
    if vrais.shape != predits.shape or vrais.ndim != 1:
        msg = f"{nom} : verite et prediction doivent etre des vecteurs 1D de meme taille."
        raise ValueError(msg)
    if vrais.size == 0:
        msg = f"{nom} : au moins un point est requis."
        raise ValueError(msg)
    if np.any(vrais <= 0.0):
        msg = f"{nom} : la verite doit etre strictement positive."
        raise ValueError(msg)
    return vrais, predits


def fac2(verite: ArrayLike, prediction: ArrayLike) -> float:
    """FAC2 : fraction des points avec 0.5 <= prediction/verite <= 2.

    Convention pre-enregistree (issue #43) : ratio point a point, bornes
    incluses ; la verite doit etre strictement positive (les cas du
    registre le garantissent a l enregistrement).
    """
    vrais, predits = _vecteurs_verifies(verite, prediction, "FAC2")
    ratios = predits / vrais
    return float(np.count_nonzero((ratios >= 0.5) & (ratios <= 2.0)) / vrais.size)


def nmse(verite: ArrayLike, prediction: ArrayLike) -> float:
    """NMSE = somme((prediction - verite)^2) / somme(verite^2).

    Convention explicite : d autres usages prennent somme(verite x
    prediction) au denominateur ; ce choix est documente pour eviter
    toute ambiguite. La verite doit etre strictement positive.
    """
    vrais, predits = _vecteurs_verifies(verite, prediction, "NMSE")
    return float(np.sum((predits - vrais) ** 2) / np.sum(vrais**2))


@dataclass(frozen=True)
class Metrique:
    """Definition d une metrique : nom stable, calcul, ancrage documentaire.

    Attributs :
        nom : cle stable dans les resultats et les exports JSON.
        libelle : nom lisible pour les rapports.
        ancrage : reference du pre-enregistrement (issue, document).
        calcul : fonction (verite, prediction) -> float.
    """

    nom: str
    libelle: str
    ancrage: str
    calcul: Callable[[np.ndarray, np.ndarray], float]


FAC2: Metrique = Metrique(
    nom="fac2",
    libelle="FAC2",
    ancrage="issue #43 ; metrique usuelle du Model Validation Kit (Harmonisation)",
    calcul=fac2,
)

NMSE: Metrique = Metrique(
    nom="nmse",
    libelle="NMSE",
    ancrage="issue #43 ; metrique usuelle du Model Validation Kit (Harmonisation)",
    calcul=nmse,
)

METRIQUES: dict[str, Metrique] = {"fac2": FAC2, "nmse": NMSE}
METRIQUES_DEFAUT: tuple[Metrique, ...] = (FAC2, NMSE)


def enregistrer_metrique(metrique: Metrique) -> None:
    """Ajoute une metrique au registre ; nom deja pris sinon ValueError.

    Garde-fou : une metrique sans seuil de succes pre-enregistre
    (G2/G3, issue #43) ne doit pas rejoindre METRIQUES_DEFAUT ; ce
    registre sert aux extensions futures, pre-enregistrement fait.
    """
    if metrique.nom in METRIQUES:
        msg = f"La metrique {metrique.nom} est deja enregistree."
        raise ValueError(msg)
    METRIQUES[metrique.nom] = metrique


def retirer_metrique(nom: str) -> None:
    """Retire la metrique enregistree sous ce nom, sinon ValueError."""
    if nom not in METRIQUES:
        msg = f"La metrique {nom} est absente du registre."
        raise ValueError(msg)
    del METRIQUES[nom]


def calculer_metriques(
    verite: ArrayLike,
    prediction: ArrayLike,
    metriques: Sequence[Metrique] = METRIQUES_DEFAUT,
) -> dict[str, float]:
    """Calcule les metriques demandees sur une prediction ; noms uniques.

    La validation (1D, meme taille, verite strictement positive) est
    faite par chaque metrique elle-meme : une metrique enregistree ne
    peut pas contourner les conventions de ses donnees.
    """
    if not metriques:
        msg = "Au moins une metrique est requise."
        raise ValueError(msg)
    if len({m.nom for m in metriques}) != len(metriques):
        msg = "Chaque metrique ne peut etre demandee qu une seule fois."
        raise ValueError(msg)
    vrais = np.asarray(verite, dtype=float)
    predits = np.asarray(prediction, dtype=float)
    return {m.nom: float(m.calcul(vrais, predits)) for m in metriques}
