"""Diagnostics déterministes entre l'inventaire extrait et le registre revu.

Le rapprochement porte uniquement sur les localisateurs de fichiers. Une
correspondance indique qu'un fichier extrait est référencé par un nœud du
registre ; elle ne valide ni le contenu du nœud ni une relation scientifique.
"""

from __future__ import annotations

import argparse
import configparser
import json
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jdriftx.extraction_graphe import extraire_faits
from jdriftx.graphe_connaissances import charger

KINDS_FICHIER = {"python_module", "test_file", "quarto_page"}


def _identite_github(racine: Path) -> tuple[str, str] | None:
    """Lit le propriétaire et le dépôt depuis le remote GitHub origin."""
    configuration = configparser.ConfigParser()
    chemin_configuration = racine / ".git" / "config"
    if not chemin_configuration.is_file():
        return None
    configuration.read(chemin_configuration, encoding="utf-8")
    url = configuration.get('remote "origin"', "url", fallback="").strip()
    if not url:
        return None

    if url.startswith("git@github.com:"):
        chemin = url.removeprefix("git@github.com:")
    else:
        parsed = urlsplit(url)
        if parsed.hostname is None or parsed.hostname.lower() != "github.com":
            return None
        chemin = parsed.path.lstrip("/")

    chemin = chemin.removesuffix(".git").strip("/")
    morceaux = chemin.split("/")
    if len(morceaux) < 2 or not morceaux[0] or not morceaux[1]:
        return None
    return morceaux[0].casefold(), morceaux[1].casefold()


def _chemin_local(lien: str | None, identite_github: tuple[str, str] | None = None) -> str | None:
    """Retourne un chemin repo-relatif pour un lien local ou GitHub du même dépôt."""
    if not lien:
        return None
    parsed = urlsplit(lien)
    if not parsed.scheme and not parsed.netloc:
        chemin = parsed.path.removeprefix("./").lstrip("/")
        return unquote(chemin) or None

    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname is None
        or parsed.hostname.lower() != "github.com"
        or identite_github is None
    ):
        return None

    morceaux = parsed.path.strip("/").split("/")
    if len(morceaux) < 5 or tuple(part.casefold() for part in morceaux[:2]) != identite_github:
        return None
    if morceaux[2] not in {"blob", "tree"}:
        return None

    # Le segment suivant est une branche ou un tag ; le reste est le chemin du dépôt.
    chemin = unquote("/".join(morceaux[4:]))
    return chemin or None


def _est_extractible(chemin: str) -> bool:
    """Indique si le chemin appartient à une catégorie couverte par l'extracteur."""
    return (
        (
            chemin.startswith("src/jdriftx/")
            and chemin.endswith(".py")
            and not chemin.endswith("/__init__.py")
        )
        or (
            chemin.startswith("tests/")
            and Path(chemin).name.startswith("test_")
            and chemin.endswith(".py")
        )
        or (
            chemin.startswith("site/")
            and not chemin.startswith("site/_extensions/")
            and chemin.endswith(".qmd")
        )
    )


def diagnostiquer(racine: Path) -> dict[str, object]:
    """Compare les fichiers extraits aux localisateurs du registre sémantique."""
    racine = racine.resolve()
    identite_github = _identite_github(racine)
    registre = charger(racine / "site/data/graphe-connaissances.toml")
    faits = extraire_faits(racine)
    fichiers = {fait.path: fait for fait in faits if fait.kind in KINDS_FICHIER}

    liens_registre: dict[str, list[str]] = {}
    localisateurs_non_extraits: list[dict[str, str]] = []
    for noeud in registre.noeuds:
        chemin = _chemin_local(noeud.lien, identite_github)
        if chemin is None:
            continue
        liens_registre.setdefault(chemin, []).append(noeud.id)
        if not _est_extractible(chemin):
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
    return (
        json.dumps(
            diagnostiquer(racine),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


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
