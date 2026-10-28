"""Tests du graphe de connaissances : validation, rendu et synchronisation."""

from __future__ import annotations

from pathlib import Path

import pytest

from jdriftx.graphe_connaissances import (
    CHEMIN_PARTIEL,
    CHEMIN_REGISTRE,
    RACINE,
    Registre,
    charger,
    citations,
    generer_contenu,
    main,
    regenerer,
    valider,
)

REGISTRE_MINIMAL = """
[types.concept]
libelle = "Concept"
couleur = "#c9ecd9"

[types.module]
libelle = "Module de code"
couleur = "#d7f0a1"

[types.reference]
libelle = "Référence bibliographique"
couleur = "#e6dccb"

[relations.contexte]
libelle = "contexte"
signification = "le nœud d'origine fournit un arrière-plan au nœud ciblé"
ne_affirme_pas = "tout appui, fondement ou validation"
type_semantique = "structurelle"

[relations.couvre]
libelle = "couvre"
signification = "le fichier de test exerce les fonctions du module ciblé"
ne_affirme_pas = "une validité physique ou une couverture exhaustive"
type_semantique = "TESTED_BY"

[[noeuds]]
id = "c-demo"
type = "concept"
libelle = "Concept de démonstration"
lien = "site/theorie/page.qmd"

[[noeuds]]
id = "c-nu"
type = "concept"
libelle = "Concept sans lien"

[[noeuds]]
id = "noyau"
type = "module"
libelle = "noyau.py"
lien = "https://example.com/noyau.py"

[[noeuds]]
id = "cle2000"
type = "reference"
libelle = "Auteur 2000 - Démo"
lien = "https://example.com/auteur2000"

[[aretes]]
de = "cle2000"
vers = "c-demo"
relation = "contexte"

[[aretes]]
de = "noyau"
vers = "c-demo"
relation = "couvre"
justification = "fichier de test du module noyau"

[[graphes]]
id = "vue"
titre = "Vue minimale"
description = "Vue de démonstration."
sens = "LR"
noeuds = ["c-demo", "noyau", "cle2000", "c-nu"]

  [[graphes.groupes]]
  id = "objets"
  titre = "Objets"
  noeuds = ["noyau", "c-demo", "cle2000", "c-nu"]
"""


def _depot_minimal(racine: Path) -> Path:
    """Construit un dépôt minimal mais complet pour le graphe."""
    (racine / "site/theorie").mkdir(parents=True)
    (racine / "site/projet").mkdir(parents=True)
    (racine / "site/data").mkdir(parents=True)
    (racine / "src/jdriftx").mkdir(parents=True)
    (racine / "site/data/graphe-connaissances.toml").write_text(
        REGISTRE_MINIMAL.strip() + "\n", encoding="utf-8"
    )
    (racine / "site/theorie/page.qmd").write_text(
        '---\ntitle: "Page"\n---\n\nTexte qui cite [@cle2000] deux fois [@cle2000].\n',
        encoding="utf-8",
    )
    (racine / "site/annexe.qmd").write_text(
        "Sans frontmatter, cite [@cle2000].\n", encoding="utf-8"
    )
    (racine / "site/references.bib").write_text(
        "@article{cle2000,\n  title = {Démo},\n}\n", encoding="utf-8"
    )
    (racine / "src/jdriftx/noyau.py").write_text('"""Module minimal."""\n', encoding="utf-8")
    return racine


def _registre_modifie(racine: Path, remplacement: tuple[str, str]) -> Registre:
    """Charge le registre minimal après une substitution de texte."""
    chemin = racine / "site/data/graphe-connaissances.toml"
    texte = chemin.read_text(encoding="utf-8").replace(*remplacement)
    chemin.write_text(texte, encoding="utf-8")
    return charger(chemin)


def test_registre_reel_valide() -> None:
    """Étant donné le dépôt réel, quand on valide, alors tout est cohérent."""
    registre = charger(CHEMIN_REGISTRE)

    valider(registre, RACINE)

    assert {noeud.type for noeud in registre.noeuds} <= set(registre.types)


def test_depot_minimal_valide(tmp_path: Path) -> None:
    """Étant donné un dépôt minimal, quand on valide, alors aucune erreur."""
    racine = _depot_minimal(tmp_path / "depot")

    registre = charger(racine / "site/data/graphe-connaissances.toml")

    valider(registre, racine)


@pytest.mark.parametrize(
    ("avant", "apres", "motif"),
    [
        ('relation = "couvre"', 'relation = "inconnue"', "relation inconnue"),
        ('vers = "c-demo"', 'vers = "fantome"', "cible inconnue"),
        ('type = "reference"', 'type = "reverence"', "type inconnu"),
        ('id = "c-demo"', 'id = "noyau"', "dupliqués"),
        (
            'noeuds = ["c-demo", "noyau", "cle2000", "c-nu"]',
            'noeuds = ["noyau", "cle2000", "c-nu"]',
            "absents de toutes les vues",
        ),
        (
            'noeuds = ["c-demo", "noyau", "cle2000", "c-nu"]',
            'noeuds = ["c-demo", "noyau", "c-nu"]',
            "invisible",
        ),
        (
            'lien = "site/theorie/page.qmd"',
            'lien = "site/theorie/fantome.qmd"',
            "lien introuvable",
        ),
        ('id = "cle2000"', 'id = "cle9999"', "clé bib absente du registre"),
        ('id = "noyau"', 'id = "noyau2"', "module absent du registre"),
        ('sens = "LR"', 'sens = "XX"', "sens invalide"),
        (
            'noeuds = ["noyau", "c-demo", "cle2000", "c-nu"]',
            'noeuds = ["noyau", "c-demo", "cle2000"]',
            "absents des groupes",
        ),
        (
            'type_semantique = "TESTED_BY"',
            'type_semantique = "INCONNU"',
            "type sémantique inconnu",
        ),
        (
            'justification = "fichier de test du module noyau"',
            'justification = ""',
            "justification manquante",
        ),
    ],
)
def test_erreurs_de_validation(tmp_path: Path, avant: str, apres: str, motif: str) -> None:
    """Étant donné un registre modifié de façon invalide, quand on valide,
    alors l'erreur mentionne le motif attendu."""
    racine = _depot_minimal(tmp_path / "depot")

    registre = _registre_modifie(racine, (avant, apres))

    with pytest.raises(ValueError, match=motif):
        valider(registre, racine)


def test_rendu_contient_la_structure(tmp_path: Path) -> None:
    """Étant donné un registre minimal, quand on génère le rendu, alors
    légende, groupes, arêtes, classDef et tables cliquables sont présents."""
    racine = _depot_minimal(tmp_path / "depot")
    registre = charger(racine / "site/data/graphe-connaissances.toml")

    contenu = generer_contenu(registre, citations(registre, racine))

    assert contenu.startswith("<!-- Ne pas éditer à la main")
    assert "```{mermaid}\ngraph LR" in contenu
    assert 'subgraph objets["Objets"]' in contenu
    assert 'noyau["noyau.py"]::module' in contenu
    assert 'cle2000 -->|"contexte"| c_demo' in contenu
    assert "classDef module fill:#d7f0a1,stroke:#495057,color:#212529;" in contenu
    assert "| Nœud | Type | Où approfondir |" in contenu
    assert "[theorie/page.qmd](../theorie/page.qmd)" in contenu
    assert "| Concept sans lien | Concept | Concept sans lien |" in contenu
    assert "[Auteur 2000 - Démo](https://example.com/auteur2000)" in contenu


def test_citations_pages_titres_et_doublons(tmp_path: Path) -> None:
    """Étant donné deux pages citant la même clé, quand on extrait, alors
    chaque page apparaît une fois, avec son titre ou son nom de fichier."""
    racine = _depot_minimal(tmp_path / "depot")
    registre = charger(racine / "site/data/graphe-connaissances.toml")

    pages = citations(registre, racine)

    assert [(page.titre, page.chemin) for page in pages["cle2000"]] == [
        ("annexe", "annexe.qmd"),
        ("Page", "theorie/page.qmd"),
    ]


def test_rendu_contient_les_citations(tmp_path: Path) -> None:
    """Étant donné des pages citantes, quand on génère, alors la table
    finale lie chaque référence à ses pages, relatifs au partiel."""
    racine = _depot_minimal(tmp_path / "depot")
    registre = charger(racine / "site/data/graphe-connaissances.toml")

    contenu = generer_contenu(registre, citations(registre, racine))

    assert "## Où chaque référence est citée" in contenu
    assert "[annexe](../annexe.qmd)" in contenu
    assert "[Page](../theorie/page.qmd)" in contenu


def test_regenerer_est_deterministe(tmp_path: Path) -> None:
    """Étant donné un rendu régénéré deux fois, quand on compare, alors
    le contenu est identique octet par octet."""
    racine = _depot_minimal(tmp_path / "depot")
    registre = racine / "site/data/graphe-connaissances.toml"
    partiel = racine / "site/projet/_graphes-mermaid.md"

    regenerer(registre, partiel)
    premier = partiel.read_text(encoding="utf-8")
    regenerer(registre, partiel)

    assert partiel.read_text(encoding="utf-8") == premier
    assert premier.startswith("<!-- Ne pas éditer à la main")


def test_rendu_commute_est_synchronise() -> None:
    """Étant donné le registre réel, quand on régénère, alors le partiel
    committé est identique octet par octet."""
    registre = charger(CHEMIN_REGISTRE)

    valider(registre, RACINE)
    attendu = generer_contenu(registre, citations(registre, RACINE))

    assert CHEMIN_PARTIEL.read_text(encoding="utf-8") == attendu


def test_main_verifier_retourne_zero() -> None:
    """Étant donné le dépôt réel synchronisé, quand on appelle main avec
    --verifier, alors le code de sortie est 0."""
    assert main(["--verifier"]) == 0
