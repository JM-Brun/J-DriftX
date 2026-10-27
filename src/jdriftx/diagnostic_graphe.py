"""Diagnostics déterministes entre l'inventaire extrait et le registre revu.

Le rapprochement porte uniquement sur les localisateurs de fichiers. Une
correspondance indique qu'un fichier extrait est référencé par un nœud du
registre ; elle ne valide ni le contenu du nœud ni une relation scientifique.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import urlsplit

from jdriftx.extraction_graphe import extraire_faits
from jdriftx.graphe_connaissances import charger

KINDS_FICHIER = {"python_module", "test_file", "quarto_page"}
PREFIXES_EXTRACTES = ("src/jdriftx/", "tests/", "site/")


def _chemin_local(lien: str | None) -> str | None:
    """Retourne un localisateur repo-relatif pour un lien local."""
    if not lien:
        return None
    parsed = urlsplit(lien)
    if parsed.scheme or parsed.netloc:
        return None
    chemin = parsed.path.removeprefix("./").lstrip("/")
    return chemin or None


def diagnostiquer(racine: Path) -> dict[str, object]:
    """Compare les fichiers extraits aux localisateurs du registre sémantique."""
    racine = racine.resolve()
    registre = charger(racine / "site/data/graphe-connaissances.toml")
    faits = extraire_faits(racine)
    fichiers = {
        fait.path: fait
        for fait in faits
        if fait.kind in KINDS_FICHIER
    }

    liens_registre: dict[str, list[str]] = {}
    localisateurs_non_extraits: list[dict[str, str]] = []
    for noeud in registre.noeuds:
        chemin = _chemin_local(noeud.lien)
        if chemin is None:
            continue
        liens_registre.setdefault(chemin, []).append(noeud.id)
        if not chemin.startswith(PREFIXES_EXTRACTES):
            continue
        if chemin not in fichiers:
            localisateurs_non_extraits.append(
                {"node_id": noeud.id, "path": chemin, "reason": "not_in_extracted_inventory"}
            )

    mapped = [
        {
            "path": chemin,
            "node_ids": sorted(liens_registre[chemin]),
        }
        for chemin in sorted(fichiers.keys() & liens_registre.keys())
    ]
    unmapped = [
        {"path": chemin, "kind": fichiers[chemin].kind, "label": fichiers[chemin].label}
        for chemin in sorted(fichiers.keys() - liens_registre.keys())
    ]
    return {
        "schema_version": 1,
        "semantics": (
            "Locator reconciliation only; matches do not establish scientific support, "
            "validity, dependency, or causality. Unmapped items are diagnostics, not errors."
        ),
        "summary": {
            "extracted_file_count": len(fichiers),
            "mapped_file_count": len(mapped),
            "unmapped_file_count": len(unmapped),
            "registry_locator_without_extracted_fact_count": len(localisateurs_non_extraits),
        },
        "mapped_files": mapped,
        "unmapped_files": unmapped,
        "registry_locators_without_extracted_facts": sorted(
            localisateurs_non_extraits, key=lambda item: (item["path"], item["node_id"])
        ),
    }


def serialiser_diagnostic(racine: Path) -> str:
    """Produit un JSON stable pour inspection locale ou CI."""
    return json.dumps(
        diagnostiquer(racine),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """Écrit le diagnostic JSON sur stdout ou dans un fichier."""
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument(
        "--racine",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Racine du dépôt à analyser (par défaut : ce dépôt).",
    )
    parseur.add_argument("--sortie", type=Path, help="Fichier JSON de sortie.")
    arguments = parseur.parse_args(argv)
    contenu = serialiser_diagnostic(arguments.racine)
    if arguments.sortie is None:
        print(contenu, end="")
    else:
        arguments.sortie.parent.mkdir(parents=True, exist_ok=True)
        arguments.sortie.write_text(contenu, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
