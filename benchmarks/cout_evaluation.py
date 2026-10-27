"""Squelette de benchmark : évaluation ponctuelle vs champ complet.

Instrument de mesure pour le premier moment de coût identifié par
l'investigation « espaces de solutions, sensibilité, coût » : combien coûte
une évaluation ponctuelle de la concentration par rapport à la construction
d'un champ complet ? Ce script est un squelette (issue #17) : les chiffres
produits sont indicatifs, dépendants de la machine, et ne constituent ni un
résultat scientifique ni une revendication de gain. Les moments restants
(construction de la métrique, recalibration) ne sont pas couverts.

Usage :
    uv run python benchmarks/cout_evaluation.py
    uv run python benchmarks/cout_evaluation.py --repetitions 7
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from jdriftx.similitude import concentration_panache

TAILLES_GRILLE: tuple[int, ...] = (50, 100, 200, 400)
NOMBRE_POINTS: int = 100
DEBIT: float = 1.0
VENT: float = 3.0
GRAINE: int = 20261027


@dataclass(frozen=True)
class MesureCas:
    """Mesures indicatives pour une taille de grille donnée."""

    taille_grille: int
    temps_grille_s: float
    temps_ponctuel_s: float

    @property
    def nombre_cellules(self) -> int:
        """Nombre de cellules du champ complet."""
        return self.taille_grille * self.taille_grille

    @property
    def cout_par_point_ponctuel_s(self) -> float:
        """Coût moyen (s) d'une évaluation ponctuelle."""
        return self.temps_ponctuel_s / NOMBRE_POINTS


def _temps_median(appel: Callable[[], object], repetitions: int) -> float:
    """Retourne le temps médian (s) d'un appel répété."""
    durees: list[float] = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        appel()
        durees.append(time.perf_counter() - debut)
    durees.sort()
    return durees[len(durees) // 2]


def _mesurer_cas(taille: int, repetitions: int) -> MesureCas:
    """Mesure le champ complet et les évaluations ponctuelles pour une taille."""
    x = np.linspace(1.0, 5000.0, taille)
    y = np.linspace(-200.0, 200.0, taille)
    grille_x, grille_y = np.meshgrid(x, y)

    def evalue_grille() -> None:
        concentration_panache(grille_x, grille_y, 2.0, DEBIT, VENT, "D")

    temps_grille = _temps_median(evalue_grille, repetitions)

    generateur = np.random.default_rng(GRAINE)
    points_x = generateur.uniform(1.0, 5000.0, NOMBRE_POINTS)
    points_y = generateur.uniform(-200.0, 200.0, NOMBRE_POINTS)

    def evalue_points() -> None:
        for px, py in zip(points_x, points_y, strict=True):
            concentration_panache(px, py, 2.0, DEBIT, VENT, "D")

    temps_ponctuel = _temps_median(evalue_points, repetitions)
    return MesureCas(taille, temps_grille, temps_ponctuel)


def _afficher(mesures: list[MesureCas]) -> None:
    """Affiche le tableau indicatif des mesures."""
    print(f"{'grille':>8} {'cellules':>10} {'champ (s)':>13} {'ponctuel (s)':>14} {'s/point':>11}")
    for mesure in mesures:
        print(
            f"{mesure.taille_grille:>8} {mesure.nombre_cellules:>10} "
            f"{mesure.temps_grille_s:>13.3e} {mesure.temps_ponctuel_s:>14.3e} "
            f"{mesure.cout_par_point_ponctuel_s:>11.3e}"
        )


def main() -> None:
    """Mesure et affiche les cas du squelette."""
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument("--repetitions", type=int, default=5, help="répétitions par cas")
    args = analyseur.parse_args()
    mesures = [_mesurer_cas(taille, args.repetitions) for taille in TAILLES_GRILLE]
    _afficher(mesures)


if __name__ == "__main__":
    main()
