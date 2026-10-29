"""Squelette de benchmark : evaluation contre une verite exacte.

Pipeline : cas enregistre -> grille de points -> verite exacte ->
metriques pre-enregistrees (#43) -> ResultatEvaluation exportable en
JSON. La commande uv run python -m jdriftx.benchmarks.reference
[identifiant] fait tourner le passage a vide (prediction = verite) du
cas demande : FAC2 = 1 et NMSE = 0 sont des controles d auto-coherence
du pipeline, PAS un resultat scientifique.

Garde-fous (issues #17 et #43) : aucun benchmark applicatif ne demarre
tant que la porte G1 (inspection des fichiers, issue #204) n est pas
franchie ; les seuils de succes G2/G3 sont pre-enregistres dans #43 et
ne sont pas modifies ici.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.benchmarks.cas import construire_cas
from jdriftx.benchmarks.metriques import METRIQUES_DEFAUT, Metrique, calculer_metriques

__all__ = [
    "ResultatEvaluation",
    "evaluer_prediction",
    "main",
    "mesurer_cout_inference",
]


@dataclass(frozen=True)
class ResultatEvaluation:
    """Metriques d une prediction contre la verite d un cas (sans unite).

    Attributs :
        metriques : dictionnaire nom -> valeur (cles pre-enregistrees).
        effectif : nombre de points de mesure evalues.
    """

    metriques: dict[str, float]
    effectif: int

    def vers_dict(self) -> dict[str, float | int]:
        """Export JSON aux frontieres du package (convention de la charte)."""
        return {**self.metriques, "effectif": self.effectif}


def evaluer_prediction(
    verite: ArrayLike,
    prediction: ArrayLike,
    metriques: Sequence[Metrique] = METRIQUES_DEFAUT,
) -> ResultatEvaluation:
    """Evalue une prediction contre une verite strictement positive."""
    vrais = np.asarray(verite, dtype=float)
    return ResultatEvaluation(
        metriques=calculer_metriques(vrais, prediction, metriques),
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


def main(identifiant: str = "S0") -> dict[str, float | int]:
    """Controle de coherence du squelette : pas un resultat scientifique.

    Commande : uv run python -m jdriftx.benchmarks.reference [identifiant].
    La prediction evaluee EST la verite du cas demande : les metriques
    parfaites sont des controles d auto-coherence du pipeline.
    """
    cas = construire_cas(identifiant)
    points = cas.points()
    vrais = cas.verite(points)
    resultat = evaluer_prediction(vrais, vrais)
    return resultat.vers_dict()


if __name__ == "__main__":
    print(main(sys.argv[1] if len(sys.argv) > 1 else "S0"))
