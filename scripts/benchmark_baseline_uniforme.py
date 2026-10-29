"""Benchmark reproducible de l'oracle indépendant pour la baseline uniforme.

Usage:
    uv run python scripts/benchmark_baseline_uniforme.py --repetitions 1000 \
        --output artifacts/baseline-uniforme-step5.json

Le benchmark compare deux chemins de calcul sur le cas analytique S0, classe C :
la reconstruction de production (temps dirigé, objet Pydantic, adaptateur de
concentration) et une formule scalaire explicite écrite indépendamment des
fonctions de production. L'oracle partage les paramètres physiques et la
famille gaussienne ; il n'est donc pas une validation indépendante du modèle
physique ni une source historique authentifiée.

Les durées sont des mesures exploratoires dépendantes de la machine. Le script
conserve chaque répétition brute, les statistiques descriptives, les erreurs,
l'environnement et le pic d'allocations Python tracées. Ce dernier n'est pas
la mémoire résidente totale du processus.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import statistics
import sys
import time
import tracemalloc
from collections.abc import Callable
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np

from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, CasS0, PointMesure
from jdriftx.experiences.baseline_uniforme import evaluer_point
from jdriftx.source import SourcePanache

TOLERANCE_ABSOLUE = 1e-15
TOLERANCE_RELATIVE = 1e-12
SEUIL_RELATIF = 1e-15


def oracle_concentration(point: PointMesure, source: SourcePanache) -> float:
    """Solution gaussienne scalaire explicite pour la classe C du cas S0.

    Les coefficients sont repris explicitement du contrat scientifique docs/48
    (Briggs rural, classe C), pas lus depuis jdriftx.stabilite ou similitude.
    Ce chemin indépendant peut détecter des erreurs d'assemblage et de calcul
    dans le pipeline, mais pas une erreur commune dans le choix des équations
    ou des coefficients.
    """
    if source.classe != "C":
        raise ValueError("L'oracle scalaire est limité à la classe C.")
    if point.x <= 0.0:
        raise ValueError("L'oracle exige un point strictement sous le vent.")

    sigma_y = 0.11 * point.x / math.sqrt(1.0 + 0.0001 * point.x)
    sigma_z = 0.08 * point.x / math.sqrt(1.0 + 0.0002 * point.x)
    lateral = math.exp(-(point.y**2) / (2.0 * sigma_y**2))
    vertical = math.exp(-((point.z - source.hauteur) ** 2) / (2.0 * sigma_z**2))
    vertical += math.exp(-((point.z + source.hauteur) ** 2) / (2.0 * sigma_z**2))
    return (
        source.debit
        / (2.0 * math.pi * source.u * sigma_y * sigma_z)
        * lateral
        * vertical
    )


def preparer_cas() -> tuple[CasS0, tuple[PointMesure, ...]]:
    """Construit les paramètres et la grille avant la mesure d'inférence."""
    source = SourcePanache(
        debit=CAS_S0_DEFAUT.source.debit,
        u=CAS_S0_DEFAUT.source.u,
        classe=CAS_S0_DEFAUT.source.classe,
        hauteur=CAS_S0_DEFAUT.source.hauteur,
    )
    cas = CasS0(
        source=source,
        arcs=CAS_S0_DEFAUT.arcs,
        positions_laterales=CAS_S0_DEFAUT.positions_laterales,
        z_mesure=CAS_S0_DEFAUT.z_mesure,
    )
    return cas, cas.points()


def statistiques(valeurs_ms: list[float]) -> dict[str, float]:
    """Résume des mesures brutes en millisecondes."""
    return {
        "median_ms": statistics.median(valeurs_ms),
        "mean_ms": statistics.fmean(valeurs_ms),
        "stdev_ms": statistics.stdev(valeurs_ms) if len(valeurs_ms) > 1 else 0.0,
        "min_ms": min(valeurs_ms),
        "max_ms": max(valeurs_ms),
    }


def mesurer(
    operation: Callable[[], Any],
    repetitions: int,
) -> dict[str, Any]:
    """Exécute une opération répétée et conserve toutes les durées brutes."""
    brutes: list[float] = []
    operation()  # échauffement hors mesure
    for _ in range(repetitions):
        debut = time.perf_counter_ns()
        operation()
        brutes.append((time.perf_counter_ns() - debut) / 1_000_000)
    return {"raw_ms": brutes, **statistiques(brutes)}


def mesurer_pic_allocations(operation: Callable[[], Any]) -> int:
    """Mesure le pic d'allocations suivies par tracemalloc pour une opération."""
    tracemalloc.start()
    try:
        operation()
        _, pic = tracemalloc.get_traced_memory()
        return pic
    finally:
        tracemalloc.stop()


def executer(repetitions: int) -> dict[str, Any]:
    """Exécute la comparaison et retourne un rapport JSON-natif."""
    cas, points = preparer_cas()
    source = cas.source

    def evaluer_baseline() -> list[float]:
        return [evaluer_point(cas, point).concentration for point in points]

    def evaluer_oracle() -> list[float]:
        return [oracle_concentration(point, source) for point in points]

    baseline = evaluer_baseline()
    oracle = evaluer_oracle()
    erreurs = [
        {
            "point": {"x_m": p.x, "y_m": p.y, "z_m": p.z},
            "baseline_kg_m3": b,
            "oracle_kg_m3": o,
            "absolute_error_kg_m3": abs(b - o),
            "relative_error": abs(b - o) / max(abs(o), SEUIL_RELATIF),
            "within_tolerance": abs(b - o)
            <= TOLERANCE_ABSOLUE + TOLERANCE_RELATIVE * abs(o),
        }
        for p, b, o in zip(points, baseline, oracle, strict=True)
    ]

    def preparer_baseline() -> None:
        preparer_cas()

    def preparer_oracle() -> None:
        # L'oracle est sans calibration : seule la source et la grille sont préparées.
        preparer_cas()

    baseline_workload = lambda: [evaluer_point(cas, p).concentration for p in points]
    oracle_workload = lambda: [oracle_concentration(p, source) for p in points]

    baseline_times = mesurer(baseline_workload, repetitions)
    oracle_times = mesurer(oracle_workload, repetitions)
    baseline_setup = mesurer(preparer_baseline, repetitions)
    oracle_setup = mesurer(preparer_oracle, repetitions)
    baseline_memory = mesurer_pic_allocations(baseline_workload)
    oracle_memory = mesurer_pic_allocations(oracle_workload)

    return {
        "schema_version": 1,
        "experiment": "jdriftx-baseline-uniforme-step5",
        "scope": {
            "case": "S0 uniforme, classe C, 12 points",
            "oracle": "formule gaussienne scalaire indépendante du chemin d'exécution",
            "not_claimed": [
                "validation physique",
                "validation sur données terrain",
                "indépendance de la formulation physique ou des coefficients",
                "reproduction du gain historique 10^3-10^4",
            ],
        },
        "protocol": {
            "repetitions": repetitions,
            "warmup_calls_per_operation": 1,
            "absolute_tolerance_kg_m3": TOLERANCE_ABSOLUE,
            "relative_tolerance": TOLERANCE_RELATIVE,
            "relative_error_denominator_floor_kg_m3": SEUIL_RELATIF,
            "timing_unit": "ms",
            "memory_measure": "tracemalloc_peak_bytes_for_one_full_grid",
        },
        "environment": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pydantic": metadata.version("pydantic"),
            "package_version": _version_package(),
        },
        "accuracy": {
            "point_count": len(points),
            "all_within_tolerance": all(item["within_tolerance"] for item in erreurs),
            "max_absolute_error_kg_m3": max(item["absolute_error_kg_m3"] for item in erreurs),
            "max_relative_error": max(item["relative_error"] for item in erreurs),
            "points": erreurs,
        },
        "cost": {
            "preparation_baseline": baseline_setup,
            "preparation_oracle": oracle_setup,
            "full_grid_baseline": baseline_times,
            "full_grid_oracle": oracle_times,
            "per_query_median_ms_baseline": baseline_times["median_ms"] / len(points),
            "per_query_median_ms_oracle": oracle_times["median_ms"] / len(points),
            "preparation_cost_interpretation": (
                "Construction du cas et de la grille uniquement ; aucun calibrage "
                "n'existe dans cette reconstruction ni dans l'oracle."
            ),
            "peak_traced_allocations_bytes_baseline": baseline_memory,
            "peak_traced_allocations_bytes_oracle": oracle_memory,
        },
    }


def _version_package() -> str:
    """Retourne la version installée ou un libellé explicite en environnement source."""
    try:
        return metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        return "non-installe"


def main() -> None:
    """Point d'entrée CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--output", type=Path, help="Chemin JSON de sortie (stdout sinon).")
    args = parser.parse_args()
    if args.repetitions < 5:
        parser.error("--repetitions doit être >= 5 pour rapporter une variabilité.")

    rapport = executer(args.repetitions)
    texte = json.dumps(rapport, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output is None:
        print(texte, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(texte, encoding="utf-8")


if __name__ == "__main__":
    main()
