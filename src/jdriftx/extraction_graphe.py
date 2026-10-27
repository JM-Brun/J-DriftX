"""Extraction mécanique de faits structurels pour le graphe de connaissances.

Cette étape ne crée aucune relation scientifique. Elle extrait des faits observables
(fichiers, symboles Python, tests, titres, titres de sections, citations et liens)
avec leurs localisateurs afin qu'une couche de résolution puisse ensuite les
comparer au registre sémantique maintenu dans site/data/graphe-connaissances.toml.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from collections.abc import Sequence
from pathlib import Path

REGEX_TITRE = re.compile(r'^title:\s*["\']?([^"\'\n]+)["\']?\s*$')
REGEX_TITRE_MARKDOWN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
REGEX_CITATION = re.compile(r"(?<!\w)@([A-Za-z][A-Za-z0-9_:-]*)")
REGEX_LIEN = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
REGEX_SLUG = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True, order=True)
class FaitExtrait:
    """Fait structurel observé, avec son origine et son localisateur."""

    id: str
    kind: str
    label: str
    path: str
    line: int | None
    origin_kind: str = "extracted"


def extraire_faits(racine: Path) -> list[FaitExtrait]:
    """Extrait des faits structurels depuis le code et les sources documentaires."""
    faits: list[FaitExtrait] = []
    faits.extend(_extraire_python(racine))
    faits.extend(_extraire_quarto(racine))
    return sorted(faits)


def _extraire_python(racine: Path) -> list[FaitExtrait]:
    """Extrait les modules, classes, fonctions et fonctions de test Python."""
    faits: list[FaitExtrait] = []
    racine_python = racine / "src" / "jdriftx"
    racine_tests = racine / "tests"
    chemins = sorted(racine_python.rglob("*.py")) + sorted(racine_tests.rglob("test_*.py"))
    for chemin in chemins:
        relatif = chemin.relative_to(racine).as_posix()
        if chemin.name == "__init__.py":
            continue
        est_test = chemin.is_relative_to(racine_tests)
        type_fichier = "test_file" if est_test else "python_module"
        faits.append(
            FaitExtrait(
                id=f"{type_fichier}:{relatif}",
                kind=type_fichier,
                label=chemin.name,
                path=relatif,
                line=1,
            )
        )
        arbre = ast.parse(chemin.read_text(encoding="utf-8"), filename=relatif)
        faits.extend(_faits_symboles(arbre, relatif, est_test))
    return faits


def _faits_symboles(
    arbre: ast.Module, chemin: str, est_test: bool
) -> list[FaitExtrait]:
    """Extrait récursivement les symboles Python en conservant leur nom qualifié."""
    faits: list[FaitExtrait] = []

    def visiter(noeuds: list[ast.stmt], prefixe: str = "") -> None:
        for noeud in noeuds:
            if not isinstance(noeud, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            qualifie = f"{prefixe}.{noeud.name}" if prefixe else noeud.name
            if isinstance(noeud, ast.ClassDef):
                kind = "python_class"
            elif est_test and noeud.name.startswith("test_"):
                kind = "test_function"
            elif isinstance(noeud, ast.AsyncFunctionDef):
                kind = "python_async_function"
            else:
                kind = "python_function"
            faits.append(
                FaitExtrait(
                    id=f"{kind}:{chemin}::{qualifie}",
                    kind=kind,
                    label=qualifie,
                    path=chemin,
                    line=noeud.lineno,
                )
            )
            visiter(noeud.body, qualifie)

    visiter(arbre.body)
    return faits


def _extraire_quarto(racine: Path) -> list[FaitExtrait]:
    """Extrait les pages Quarto, titres, titres Markdown, citations et liens."""
    faits: list[FaitExtrait] = []
    racine_site = racine / "site"
    for chemin in sorted(racine_site.rglob("*.qmd")):
        relatif = chemin.relative_to(racine).as_posix()
        lignes = chemin.read_text(encoding="utf-8").splitlines()
        titre_page = chemin.stem
        for numero, ligne in enumerate(lignes, start=1):
            correspondance = REGEX_TITRE.match(ligne)
            if correspondance and numero <= 30:
                titre_page = correspondance.group(1).strip()
                break
        faits.append(
            FaitExtrait(
                id=f"quarto_page:{relatif}",
                kind="quarto_page",
                label=titre_page,
                path=relatif,
                line=1,
            )
        )
        dans_bloc_code = False
        for numero, ligne in enumerate(lignes, start=1):
            if ligne.lstrip().startswith(("\x60\x60\x60", "~~~")):
                dans_bloc_code = not dans_bloc_code
                continue
            if dans_bloc_code:
                continue
            titre = REGEX_TITRE_MARKDOWN.match(ligne)
            if titre:
                libelle = titre.group(1).strip()
                slug = _slug(libelle)
                faits.append(
                    FaitExtrait(
                        id=f"quarto_heading:{relatif}#{slug}:{numero}",
                        kind="quarto_heading",
                        label=libelle,
                        path=relatif,
                        line=numero,
                    )
                )
            for cle in dict.fromkeys(REGEX_CITATION.findall(ligne)):
                faits.append(
                    FaitExtrait(
                        id=f"citation:{relatif}:{numero}:{cle}",
                        kind="citation_occurrence",
                        label=cle,
                        path=relatif,
                        line=numero,
                    )
                )
            for lien in REGEX_LIEN.finditer(ligne):
                destination = lien.group(2).strip()
                faits.append(
                    FaitExtrait(
                        id=f"markdown_link:{relatif}:{numero}:{lien.start()}",
                        kind="markdown_link",
                        label=f"{lien.group(1).strip()} -> {destination}",
                        path=relatif,
                        line=numero,
                    )
                )
    return faits


def _slug(texte: str) -> str:
    """Produit un identifiant stable et lisible, y compris pour les accents."""
    normalise = unicodedata.normalize("NFKD", texte)
    ascii_texte = normalise.encode("ascii", "ignore").decode("ascii").lower()
    return REGEX_SLUG.sub("-", ascii_texte).strip("-") or "section"


def serialiser(faits: list[FaitExtrait]) -> str:
    """Sérialise les faits en JSON stable, prêt pour une couche de résolution."""
    return json.dumps(
        {
            "schema_version": 1,
            "semantics": (
                "Observed structure only; extracted facts do not imply scientific "
                "support, validity, dependency, or causality."
            ),
            "facts": [asdict(fait) for fait in sorted(faits)],
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    """Écrit l'inventaire JSON sur stdout ou dans un fichier demandé."""
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument(
        "--racine",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Racine du dépôt à analyser (par défaut : ce dépôt).",
    )
    parseur.add_argument(
        "--sortie",
        type=Path,
        help="Fichier JSON de sortie ; sans cette option, écrit sur stdout.",
    )
    arguments = parseur.parse_args(argv)
    contenu = serialiser(extraire_faits(arguments.racine.resolve()))
    if arguments.sortie is None:
        print(contenu, end="")
    else:
        arguments.sortie.parent.mkdir(parents=True, exist_ok=True)
        arguments.sortie.write_text(contenu, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
