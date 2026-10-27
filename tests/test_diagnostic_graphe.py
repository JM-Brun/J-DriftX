"""Tests des diagnostics de rapprochement du graphe."""

from __future__ import annotations

import json
from pathlib import Path

from jdriftx.diagnostic_graphe import _chemin_local, _identite_github, diagnostiquer, main


def _depot_minimal(racine: Path) -> Path:
    """Construit un dépôt minimal pour tester le rapprochement de localisateurs."""
    (racine / "src/jdriftx").mkdir(parents=True)
    (racine / "tests").mkdir()
    (racine / "site/data").mkdir(parents=True)
    (racine / "site/theorie").mkdir()
    (racine / ".git").mkdir()
    (racine / ".git/config").write_text(
        '[remote "origin"]\n\turl = https://github.com/JM-Brun/J-DriftX.git\n',
        encoding="utf-8",
    )
    (racine / "src/jdriftx/noyau.py").write_text(
        "def calculer() -> int:\n    return 1\n", encoding="utf-8"
    )
    (racine / "tests/test_noyau.py").write_text(
        "def test_calculer() -> None:\n    assert True\n", encoding="utf-8"
    )
    (racine / "site/theorie/modele.qmd").write_text(
        '---\ntitle: "Modèle"\n---\n# Hypothèses\n', encoding="utf-8"
    )
    (racine / "site/theorie/orphelin.qmd").write_text("# Page non référencée\n", encoding="utf-8")
    (racine / "site/_extensions/live").mkdir(parents=True)
    (racine / "site/_extensions/live/_knitr.qmd").write_text(
        '---\\ntitle: "Extension interne"\\n---\\n', encoding="utf-8"
    )
    (racine / "site/references.bib").write_text(
        "@article{demo,\n title = {Démo},\n}\n", encoding="utf-8"
    )
    (racine / "site/data/graphe-connaissances.toml").write_text(
        """
[types.concept]
libelle = "Concept"
couleur = "#c9ecd9"

[types.module]
libelle = "Module"
couleur = "#d7f0a1"

[types.test]
libelle = "Test"
couleur = "#e9ecef"

[relations.couvre]
libelle = "couvre"

[[noeuds]]
id = "modele"
type = "concept"
libelle = "Modèle"
lien = "site/theorie/modele.qmd"

[[noeuds]]
id = "noyau"
type = "module"
libelle = "Noyau"
lien = "https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/noyau.py"

[[noeuds]]
id = "test-noyau"
type = "test"
libelle = "Test noyau"
lien = "tests/test_noyau.py"

[[noeuds]]
id = "helper-extension"
type = "concept"
libelle = "Extension interne"
lien = "site/_extensions/live/_knitr.qmd"

[[noeuds]]
id = "page-perimee"
type = "concept"
libelle = "Page périmée"
lien = "site/theorie/disparue.qmd"

[[aretes]]
de = "noyau"
vers = "modele"
relation = "couvre"

[[graphes]]
id = "vue"
titre = "Vue"
description = "Vue de test"
sens = "LR"
noeuds = ["modele", "noyau", "test-noyau", "page-perimee"]

  [[graphes.groupes]]
  id = "tous"
  titre = "Tous"
  noeuds = ["modele", "noyau", "test-noyau", "page-perimee"]
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return racine


def test_diagnostic_distingue_fichiers_mappes_non_mappes_et_localisateurs_perimes(
    tmp_path: Path,
) -> None:
    """Le diagnostic rapproche les chemins sans inférer de relations sémantiques."""
    racine = _depot_minimal(tmp_path / "depot")

    rapport = diagnostiquer(racine)

    assert rapport["summary"] == {
        "extracted_file_count": 4,
        "mapped_file_count": 3,
        "unmapped_file_count": 1,
        "registry_locator_without_extracted_fact_count": 1,
    }
    assert rapport["mapped_files"] == [
        {"path": "site/theorie/modele.qmd", "node_ids": ["modele"]},
        {"path": "src/jdriftx/noyau.py", "node_ids": ["noyau"]},
        {"path": "tests/test_noyau.py", "node_ids": ["test-noyau"]},
    ]
    assert rapport["unmapped_files"] == [
        {"path": "site/theorie/orphelin.qmd", "kind": "quarto_page", "label": "orphelin"}
    ]
    assert rapport["registry_locators_without_extracted_facts"] == [
        {
            "node_id": "page-perimee",
            "path": "site/theorie/disparue.qmd",
            "reason": "not_in_extracted_inventory",
        }
    ]
    assert "do not establish scientific support" in rapport["semantics"]


def test_url_externe_et_url_dun_autre_depot_sont_ignorees(tmp_path: Path) -> None:
    """Seules les URL de fichiers du dépôt analysé deviennent des chemins locaux."""
    racine = _depot_minimal(tmp_path / "depot")
    identite = _identite_github(racine)

    assert identite == ("jm-brun", "j-driftx")
    assert (
        _chemin_local(
            "https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/noyau.py",
            identite,
        )
        == "src/jdriftx/noyau.py"
    )
    assert _chemin_local("https://example.com/src/jdriftx/noyau.py", identite) is None
    assert (
        _chemin_local("https://github.com/other/project/blob/main/src/jdriftx/noyau.py", identite)
        is None
    )


def test_diagnostic_json_et_commande_sont_deterministes(tmp_path: Path, capsys: object) -> None:
    """Le JSON reste stable et la CLI expose le rapport."""
    racine = _depot_minimal(tmp_path / "depot")

    premier = json.dumps(diagnostiquer(racine), sort_keys=True)
    second = json.dumps(diagnostiquer(racine), sort_keys=True)
    assert premier == second
    assert main(["--racine", str(racine)]) == 0
    sortie = capsys.readouterr()  # type: ignore[attr-defined]
    assert json.loads(sortie.out)["schema_version"] == 1
