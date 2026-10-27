"""Graphe de connaissances J-DriftX : registre typé, validation et rendu Mermaid.

Le fichier ``site/data/graphe-connaissances.toml`` est la source de vérité : il
décrit les nœuds typés du projet (concepts, hypothèses, niveaux, propriétés,
modules, tests, références, jeux de données) et les arêtes typées qui les
relient. Ce module charge le registre, vérifie sa cohérence avec le dépôt
(liens existants, clés de ``references.bib``, modules de ``src/jdriftx``),
puis génère ``site/projet/_graphes-mermaid.md``, inclus dans la page Carte
des connaissances du site Quarto.

Éditer le registre sans régénérer le rendu casse volontairement la CI :
lancer ``uv run python -m jdriftx.graphe_connaissances`` puis committer
les deux fichiers ensemble.
"""

from __future__ import annotations

import os
import re
import sys
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RACINE = Path(__file__).resolve().parents[2]
CHEMIN_REGISTRE = RACINE / "site" / "data" / "graphe-connaissances.toml"
CHEMIN_PARTIEL = RACINE / "site" / "projet" / "_graphes-mermaid.md"
LIEN_LISTE_MANUELLE = "[liste manuelle](../references.qmd)"
REGEX_CITATION = re.compile(r"@([A-Za-z][A-Za-z0-9_:-]*)")
REGEX_CLE_BIB = re.compile(r"^@\w+\{([^,\s]+),", re.MULTILINE)
MOTIF_LEGENDE = (
    '<span style="display:inline-block;width:0.85em;height:0.85em;'
    "border:1px solid #495057;border-radius:3px;background:{couleur};"
    'vertical-align:baseline"></span> {libelle}'
)
ENTETE = (
    "<!-- Ne pas éditer à la main : fichier généré par -->\n"
    "<!-- src/jdriftx.graphe_connaissances.py depuis "
    "site/data/graphe-connaissances.toml -->"
)


@dataclass(frozen=True)
class TypeNoeud:
    """Un type de nœud, avec son libellé et sa couleur de rendu."""

    cle: str
    libelle: str
    couleur: str


@dataclass(frozen=True)
class Relation:
    """Un type d'arête, avec son libellé lisible."""

    cle: str
    libelle: str


@dataclass(frozen=True)
class Noeud:
    """Un nœud du graphe, avec un lien de destination optionnel."""

    id: str
    type: str
    libelle: str
    lien: str | None = None


@dataclass(frozen=True)
class Arete:
    """Une arête orientée et typée entre deux nœuds."""

    de: str
    vers: str
    relation: str


@dataclass(frozen=True)
class Groupe:
    """Un sous-graphe Mermaid : un regroupement visuel de nœuds."""

    id: str
    titre: str
    noeuds: tuple[str, ...]


@dataclass(frozen=True)
class Graphe:
    """Une vue : un diagramme Mermaid et sa table de destinations."""

    id: str
    titre: str
    description: str
    sens: str
    noeuds: tuple[str, ...]
    groupes: tuple[Groupe, ...]


@dataclass(frozen=True)
class PageCitante:
    """Une page du site qui cite une référence bibliographique."""

    chemin: str
    titre: str


@dataclass(frozen=True)
class Registre:
    """Le registre complet chargé depuis le TOML."""

    types: Mapping[str, TypeNoeud]
    relations: Mapping[str, Relation]
    noeuds: tuple[Noeud, ...]
    aretes: tuple[Arete, ...]
    graphes: tuple[Graphe, ...]
    index: Mapping[str, Noeud]


def charger(chemin: Path) -> Registre:
    """Charge et convertit le registre TOML en structures typées."""
    with chemin.open("rb") as flux:
        brut: dict[str, Any] = tomllib.load(flux)
    types_ = {
        cle: TypeNoeud(cle=cle, libelle=table["libelle"], couleur=table["couleur"])
        for cle, table in brut["types"].items()
    }
    relations = {
        cle: Relation(cle=cle, libelle=table["libelle"]) for cle, table in brut["relations"].items()
    }
    noeuds = tuple(Noeud(**table) for table in brut["noeuds"])
    aretes = tuple(Arete(**table) for table in brut["aretes"])
    graphes: list[Graphe] = []
    for table in brut["graphes"]:
        groupes = tuple(
            Groupe(
                id=groupe["id"],
                titre=groupe["titre"],
                noeuds=tuple(groupe["noeuds"]),
            )
            for groupe in table.get("groupes", [])
        )
        graphes.append(
            Graphe(
                id=table["id"],
                titre=table["titre"],
                description=table["description"],
                sens=table["sens"],
                noeuds=tuple(table["noeuds"]),
                groupes=groupes,
            )
        )
    index = {noeud.id: noeud for noeud in noeuds}
    return Registre(
        types=types_,
        relations=relations,
        noeuds=noeuds,
        aretes=aretes,
        graphes=tuple(graphes),
        index=index,
    )


def valider(registre: Registre, racine: Path) -> None:
    """Vérifie la cohérence du registre avec lui-même et avec le dépôt."""
    erreurs: list[str] = []
    erreurs.extend(_erreurs_noeuds(registre, racine))
    erreurs.extend(_erreurs_aretes(registre))
    erreurs.extend(_erreurs_vues(registre))
    erreurs.extend(_erreurs_groupes(registre))
    erreurs.extend(_erreurs_references(registre, racine))
    erreurs.extend(_erreurs_modules(registre, racine))
    if erreurs:
        raise ValueError("Registre invalide :\n- " + "\n- ".join(erreurs))


def _erreurs_noeuds(registre: Registre, racine: Path) -> list[str]:
    """Identifiants dupliqués, types inconnus, liens morts."""
    resultats: list[str] = []
    identifiants = [noeud.id for noeud in registre.noeuds]
    doublons = sorted({i for i in identifiants if identifiants.count(i) > 1})
    if doublons:
        resultats.append(f"identifiants dupliqués : {', '.join(doublons)}")
    for noeud in registre.noeuds:
        if noeud.type not in registre.types:
            resultats.append(f"nœud {noeud.id} : type inconnu ({noeud.type})")
        if noeud.lien and not _lien_existe(noeud.lien, racine):
            resultats.append(f"nœud {noeud.id} : lien introuvable ({noeud.lien})")
    return resultats


def _erreurs_aretes(registre: Registre) -> list[str]:
    """Relations inconnues et extrémités absentes du registre."""
    resultats: list[str] = []
    for arete in registre.aretes:
        if arete.relation not in registre.relations:
            resultats.append(
                f"arête {arete.de} -> {arete.vers} : relation inconnue ({arete.relation})"
            )
        if arete.de not in registre.index:
            resultats.append(f"arête vers {arete.vers} : origine inconnue ({arete.de})")
        if arete.vers not in registre.index:
            resultats.append(f"arête depuis {arete.de} : cible inconnue ({arete.vers})")
    return resultats


def _erreurs_vues(registre: Registre) -> list[str]:
    """Nœuds orphelins (aucune vue) et arêtes invisibles dans toutes les vues."""
    resultats: list[str] = []
    vues = {graphe.id: set(graphe.noeuds) for graphe in registre.graphes}
    apparitions = dict.fromkeys(registre.index, 0)
    for ensemble in vues.values():
        for identifiant in ensemble:
            if identifiant in apparitions:
                apparitions[identifiant] += 1
    orphelins = sorted(i for i, n in apparitions.items() if n == 0)
    if orphelins:
        resultats.append(f"nœuds absents de toutes les vues : {', '.join(orphelins)}")
    rendues = sum(
        1
        for arete in registre.aretes
        if any(arete.de in ensemble and arete.vers in ensemble for ensemble in vues.values())
    )
    if rendues != len(registre.aretes):
        manquantes = len(registre.aretes) - rendues
        resultats.append(f"{manquantes} arête(s) invisible(s) dans toutes les vues")
    return resultats


def _erreurs_groupes(registre: Registre) -> list[str]:
    """Nœuds de groupe hors graphe, nœuds de vue sans groupe, sens invalide."""
    resultats: list[str] = []
    vues = {graphe.id: set(graphe.noeuds) for graphe in registre.graphes}
    for graphe in registre.graphes:
        ensemble = vues[graphe.id]
        declares: set[str] = set()
        for groupe in graphe.groupes:
            for identifiant in groupe.noeuds:
                if identifiant not in ensemble:
                    resultats.append(
                        f"graphe {graphe.id} : nœud {identifiant} du groupe "
                        f"{groupe.id} hors du graphe"
                    )
                declares.add(identifiant)
        manquants = sorted(ensemble - declares)
        if manquants:
            resultats.append(
                f"graphe {graphe.id} : nœuds absents des groupes : {', '.join(manquants)}"
            )
        if graphe.sens not in {"LR", "TD", "RL", "BT"}:
            resultats.append(f"graphe {graphe.id} : sens invalide ({graphe.sens})")
    return resultats


def _erreurs_references(registre: Registre, racine: Path) -> list[str]:
    """Correspondance exacte entre clés bib et nœuds référence."""
    resultats: list[str] = []
    cles_bib = _cles_bib(racine / "site" / "references.bib")
    references = {n.id for n in registre.noeuds if n.type == "reference"}
    for cle in sorted(cles_bib - references):
        resultats.append(f"clé bib absente du registre : {cle}")
    for cle in sorted(references - cles_bib):
        resultats.append(f"référence absente de site/references.bib : {cle}")
    return resultats


def _erreurs_modules(registre: Registre, racine: Path) -> list[str]:
    """Correspondance exacte entre modules du paquet et nœuds module."""
    resultats: list[str] = []
    modules = _modules(racine / "src" / "jdriftx")
    declares = {n.id for n in registre.noeuds if n.type == "module"}
    for module in sorted(modules - declares):
        resultats.append(f"module absent du registre : {module}")
    for module in sorted(declares - modules):
        resultats.append(f"nœud module sans fichier : {module}")
    return resultats


def _lien_existe(lien: str, racine: Path) -> bool:
    """URL absolue : acceptée ; chemin relatif : le fichier doit exister."""
    if lien.startswith(("http://", "https://")):
        return True
    return (racine / lien).exists()


def _cles_bib(chemin: Path) -> set[str]:
    """Extrait les clés BibTeX de site/references.bib."""
    if not chemin.exists():
        return set()
    return set(REGEX_CLE_BIB.findall(chemin.read_text(encoding="utf-8")))


def _modules(racine_paquet: Path) -> set[str]:
    """Liste les modules de src/jdriftx, chemins sans suffixe ni __init__."""
    if not racine_paquet.exists():
        return set()
    resultats: set[str] = set()
    for chemin in racine_paquet.rglob("*.py"):
        if chemin.name == "__init__.py":
            continue
        relatif = chemin.relative_to(racine_paquet).with_suffix("")
        resultats.add(relatif.as_posix())
    return resultats


def citations(registre: Registre, racine: Path) -> dict[str, list[PageCitante]]:
    """Extrait, pour chaque référence, les pages du site qui la citent."""
    par_cle = {noeud.id: [] for noeud in registre.noeuds if noeud.type == "reference"}
    racine_site = racine / "site"
    if not racine_site.exists():
        return par_cle
    for page in sorted(racine_site.rglob("*.qmd")):
        texte = page.read_text(encoding="utf-8")
        chemin = page.relative_to(racine_site).as_posix()
        titre = _titre_page(texte, page.stem)
        for cle in dict.fromkeys(REGEX_CITATION.findall(texte)):
            if cle in par_cle:
                par_cle[cle].append(PageCitante(chemin=chemin, titre=titre))
    return par_cle


def _titre_page(texte: str, nom: str) -> str:
    """Titre du frontmatter Quarto, ou nom de fichier en secours."""
    correspondance = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', texte, re.MULTILINE)
    if correspondance is None:
        return nom
    return correspondance.group(1).strip()


def generer_contenu(
    registre: Registre, pages: Mapping[str, list[PageCitante]] | None = None
) -> str:
    """Assemble le partiel Markdown complet (légende, vues, citations)."""
    if pages is None:
        pages = citations(registre, RACINE)
    parties = [ENTETE, _legende(registre)]
    for graphe in registre.graphes:
        parties.append(_section_vue(graphe, registre))
    parties.append(_section_citations(registre, pages))
    return "\n\n".join(parties) + "\n"


def _legende(registre: Registre) -> str:
    """Rend la légende des couleurs, une pastille par type de nœud."""
    morceaux = [
        MOTIF_LEGENDE.format(couleur=t.couleur, libelle=t.libelle) for t in registre.types.values()
    ]
    return "## Légende\n\n" + " \u00b7 ".join(morceaux)


def _section_vue(graphe: Graphe, registre: Registre) -> str:
    """Rend une vue : diagramme Mermaid puis table des destinations."""
    lignes = [
        f"## {graphe.titre}",
        "",
        graphe.description,
        "",
        "```{mermaid}",
        f"graph {graphe.sens}",
    ]
    for groupe in graphe.groupes:
        lignes.append(f'  subgraph {_identifiant(groupe.id)}["{groupe.titre}"]')
        for identifiant in groupe.noeuds:
            lignes.append(_ligne_noeud(registre.index[identifiant]))
        lignes.append("  end")
    vus = set(graphe.noeuds)
    for arete in registre.aretes:
        if arete.de in vus and arete.vers in vus:
            libelle = registre.relations[arete.relation].libelle
            lignes.append(f'  {_identifiant(arete.de)} -->|"{libelle}"| {_identifiant(arete.vers)}')
    types_vus = {registre.index[i].type for i in graphe.noeuds}
    for cle, type_noeud in registre.types.items():
        if cle in types_vus:
            lignes.append(
                f"  classDef {cle} fill:{type_noeud.couleur},stroke:#495057,color:#212529;"
            )
    lignes.append("```")
    lignes.append("")
    lignes.append("**Nœuds et destinations**")
    lignes.append("")
    lignes.append("| Nœud | Type | Où approfondir |")
    lignes.append("|---|---|---|")
    for identifiant in graphe.noeuds:
        lignes.append(_ligne_table(registre.index[identifiant], registre))
    return "\n".join(lignes)


def _ligne_noeud(noeud: Noeud) -> str:
    """Rend la déclaration Mermaid d'un nœud avec sa classe de couleur."""
    return f'    {_identifiant(noeud.id)}["{_texte(noeud.libelle)}"]::{noeud.type}'


def _ligne_table(noeud: Noeud, registre: Registre) -> str:
    """Rend la ligne de table « Nœud | Type | Où approfondir »."""
    type_libelle = registre.types[noeud.type].libelle
    if noeud.lien is None:
        destination = _texte(noeud.libelle)
    else:
        destination = f"[{_texte_lien(noeud.lien)}]({_lien(noeud.lien)}))"
    return f"| {_texte(noeud.libelle)} | {type_libelle} | {destination} |"


def _section_citations(registre: Registre, pages: Mapping[str, list[PageCitante]]) -> str:
    """Rend la table des pages du site qui citent chaque référence."""
    lignes = [
        "## Où chaque référence est citée",
        "",
        "| Référence | Citée dans les pages du site |",
        "|---|---|",
    ]
    for noeud in registre.noeuds:
        if noeud.type != "reference":
            continue
        if noeud.lien is None:
            reference = _texte(noeud.libelle)
        else:
            reference = f"[{_texte(noeud.libelle)}]({_lien(noeud.lien)})"
        citantes = pages.get(noeud.id, [])
        if citantes:
            cellule = " \u00b7 ".join(
                f"[{page.titre}]({_lien_page(page.chemin)})" for page in citantes
            )
        else:
            cellule = LIEN_LISTE_MANUELLE
        lignes.append(f"| {reference} | {cellule} |")
    return "\n".join(lignes)


def _texte_lien(lien: str) -> str:
    """Texte d'ancre : dernier segment pour une URL, chemin sans site/."""
    if lien.startswith("http"):
        return lien.rstrip("/").rsplit("/", 1)[-1]
    if lien.startswith("site/"):
        return lien[len("site/") :]
    return lien


def _lien(lien: str) -> str:
    """URL cible : liens absolus inchangés, chemins relatifs au partiel."""
    if lien.startswith("http"):
        return lien
    return os.path.relpath(RACINE / lien, CHEMIN_PARTIEL.parent)


def _lien_page(chemin: str) -> str:
    """URL d'une page du site, relative au partiel site/projet/."""
    if chemin.startswith("projet/"):
        return chemin[len("projet/") :]
    return f"../{chemin}"


def _texte(libelle: str) -> str:
    """Rend un libellé sûr pour Mermaid et les tables Markdown."""
    return libelle.replace('"', "'")


def _identifiant(identifiant: str) -> str:
    """Rend un identifiant sûr pour Mermaid (lettres, chiffres, tirets bas)."""
    return re.sub(r"[^A-Za-z0-9_]", "_", identifiant)


def regenerer(chemin_registre: Path, chemin_partiel: Path) -> None:
    """Valide le registre puis réécrit le partiel Mermaid synchronisé."""
    registre = charger(chemin_registre)
    racine = chemin_registre.parents[2]
    valider(registre, racine)
    contenu = generer_contenu(registre, citations(registre, racine))
    chemin_partiel.parent.mkdir(parents=True, exist_ok=True)
    chemin_partiel.write_text(contenu, encoding="utf-8", newline="\n")


def main(argv: Sequence[str] | None = None) -> int:
    """Point d'entrée : régénère le rendu, ou le vérifie avec --verifier."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if "--verifier" in arguments:
        registre = charger(CHEMIN_REGISTRE)
        valider(registre, RACINE)
        attendu = generer_contenu(registre, citations(registre, RACINE))
        if CHEMIN_PARTIEL.read_text(encoding="utf-8") != attendu:
            print("Le partiel Mermaid n'est pas synchronisé avec le registre.")
            print("Relancer : uv run python -m jdriftx.graphe_connaissances")
            return 1
        print("Graphe de connaissances : registre et rendu synchronisés.")
        return 0
    regenerer(CHEMIN_REGISTRE, CHEMIN_PARTIEL)
    print(f"Rendu régénéré : {CHEMIN_PARTIEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
