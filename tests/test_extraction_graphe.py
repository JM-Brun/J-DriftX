"""Tests de l'extraction structurelle destinée au graphe de connaissances."""

from __future__ import annotations

import json
from pathlib import Path

from jdriftx.extraction_graphe import extraire_faits, main, serialiser


def _depot_minimal(racine: Path) -> Path:
    """Construit un mini-dépôt local pour tester les formats pris en charge."""
    (racine / "src/jdriftx").mkdir(parents=True)
    (racine / "tests").mkdir()
    (racine / "site/theorie").mkdir(parents=True)
    (racine / "src/jdriftx/noyau.py").write_text(
        "class Modele:\n"
        "    def calculer(self) -> int:\n"
        "        def interne() -> int:\n"
        "            return 1\n"
        "        return interne()\n"
        "\n"
        "async def charger() -> None:\n"
        "    return None\n",
        encoding="utf-8",
    )
    (racine / "tests/test_noyau.py").write_text(
        "def test_resultat() -> None:\n    assert True\n\ndef helper() -> None:\n    pass\n",
        encoding="utf-8",
    )
    (racine / "site/theorie/modele.qmd").write_text(
        "---\n"
        'title: "Modèle de transport"\n'
        "---\n"
        "# Cadre général\n"
        "Une affirmation [documentée](../references.qmd) cite [@Auteur2026].\n"
        "## Limites\n"
        "```python\n"
        "# Fausse section\n"
        "citation [@FausseCle] [lien](faux.qmd)\n"
        "```\n",
        encoding="utf-8",
    )
    (racine / "site/sans-titre.qmd").write_text(
        "# Page sans titre\nTexte simple.\n",
        encoding="utf-8",
    )
    (racine / "site/_extensions/live").mkdir(parents=True)
    (racine / "site/_extensions/live/_knitr.qmd").write_text(
        '---\ntitle: "Extension interne"\n---\n# Ne pas indexer\n[@ExtensionInterne]\n',
        encoding="utf-8",
    )
    return racine


def test_extrait_symboles_python_et_tests(tmp_path: Path) -> None:
    """Les symboles Python et les fonctions test_* ont un localisateur source."""
    racine = _depot_minimal(tmp_path / "depot")

    faits = extraire_faits(racine)
    par_id = {fait.id: fait for fait in faits}

    assert par_id["python_module:src/jdriftx/noyau.py"].line == 1
    assert par_id["python_class:src/jdriftx/noyau.py::Modele"].line == 1
    assert par_id["python_function:src/jdriftx/noyau.py::Modele.calculer"].line == 2
    assert par_id["python_function:src/jdriftx/noyau.py::Modele.calculer.interne"].line == 3
    assert par_id["python_async_function:src/jdriftx/noyau.py::charger"].line == 7
    assert par_id["test_function:tests/test_noyau.py::test_resultat"].line == 1
    assert "python_function:tests/test_noyau.py::helper" in par_id
    assert "test_file:tests/test_noyau.py" in par_id


def test_symboles_dans_if_et_try_au_niveau_module(tmp_path: Path) -> None:
    """Étant donné des définitions dans des blocs if et try au niveau module,
    quand on extrait, alors elles sont observées sans évaluer les conditions."""
    racine = _depot_minimal(tmp_path / "depot")
    (racine / "src/jdriftx/conditionnel.py").write_text(
        "import sys\n"
        "\n"
        "if sys.version_info >= (3, 10):\n"
        "    def moderne() -> int:\n"
        "        return 1\n"
        "else:\n"
        "    def ancienne() -> int:\n"
        "        return 2\n"
        "\n"
        "try:\n"
        "    def ordinaire() -> int:\n"
        "        return 3\n"
        "except ImportError:\n"
        "    def repli() -> int:\n"
        "        return 4\n"
        "\n"
        'with open("f"):\n'
        "    def ignoree() -> int:\n"
        "        return 5\n",
        encoding="utf-8",
    )

    faits = extraire_faits(racine)
    identifiants = {fait.id for fait in faits}
    par_id = {fait.id: fait for fait in faits}

    assert "python_function:src/jdriftx/conditionnel.py::moderne" in identifiants
    assert "python_function:src/jdriftx/conditionnel.py::ancienne" in identifiants
    assert "python_function:src/jdriftx/conditionnel.py::ordinaire" in identifiants
    assert "python_function:src/jdriftx/conditionnel.py::repli" in identifiants
    assert "python_function:src/jdriftx/conditionnel.py::ignoree" not in identifiants
    assert par_id["python_function:src/jdriftx/conditionnel.py::moderne"].line == 4


def test_extrait_pages_titres_citations_et_liens(tmp_path: Path) -> None:
    """Les pages Quarto et éléments documentaires sont extraits sans arêtes."""
    racine = _depot_minimal(tmp_path / "depot")

    faits = extraire_faits(racine)
    par_id = {fait.id: fait for fait in faits}

    assert par_id["quarto_page:site/theorie/modele.qmd"].label == "Modèle de transport"
    assert par_id["quarto_heading:site/theorie/modele.qmd#cadre-general:4"].label == (
        "Cadre général"
    )
    assert par_id["citation:site/theorie/modele.qmd:5:Auteur2026"].kind == "citation_occurrence"
    lien = par_id["markdown_link:site/theorie/modele.qmd:5:16"]
    assert lien.label == "documentée -> ../references.qmd"
    assert par_id["quarto_page:site/sans-titre.qmd"].label == "sans-titre"
    assert "quarto_page:site/_extensions/live/_knitr.qmd" not in par_id
    assert not any(fait.path == "site/_extensions/live/_knitr.qmd" for fait in faits)
    assert "citation:site/theorie/modele.qmd:9:FausseCle" not in par_id
    assert all(fait.label != "Fausse section" for fait in faits)
    assert all(fait.origin_kind == "extracted" for fait in faits)


def test_titre_au_dela_de_trente_lignes_est_lu(tmp_path: Path) -> None:
    """Étant donné un frontmatter de plus de trente lignes, quand on extrait,
    alors le titre déclaré reste lu, pas le nom du fichier."""
    racine = _depot_minimal(tmp_path / "depot")
    lignes = ["---", *['option: "x"'] * 32, 'title: "Titre tardif"', "---", "# Section"]
    (racine / "site/tardif.qmd").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    faits = extraire_faits(racine)

    par_id = {fait.id: fait for fait in faits}
    assert par_id["quarto_page:site/tardif.qmd"].label == "Titre tardif"


def test_titre_dans_le_corps_non_compte(tmp_path: Path) -> None:
    """Étant donné une ligne title: dans le corps d'une page sans frontmatter,
    quand on extrait, alors le titre reste le nom du fichier."""
    racine = _depot_minimal(tmp_path / "depot")
    (racine / "site/corps.qmd").write_text('# Page\ntitle: "Titre du corps"\n', encoding="utf-8")

    faits = extraire_faits(racine)

    par_id = {fait.id: fait for fait in faits}
    assert par_id["quarto_page:site/corps.qmd"].label == "corps"


def test_serialisation_est_deterministe_et_ne_deduit_pas_de_semantique(
    tmp_path: Path,
) -> None:
    """Le JSON est stable et rappelle que les faits extraits ne sont pas des preuves."""
    racine = _depot_minimal(tmp_path / "depot")

    faits = extraire_faits(racine)
    premier = serialiser(faits)
    second = serialiser(list(reversed(faits)))
    donnees = json.loads(premier)

    assert premier == second
    assert donnees["schema_version"] == 1
    assert "do not imply scientific support" in donnees["semantics"]
    assert donnees["facts"]


def test_main_ecrit_sur_stdout_et_dans_un_fichier(tmp_path: Path, capsys: object) -> None:
    """La commande peut alimenter un pipeline ou produire un artefact JSON."""
    racine = _depot_minimal(tmp_path / "depot")

    assert main(["--racine", str(racine)]) == 0
    sortie = capsys.readouterr()  # type: ignore[attr-defined]
    assert json.loads(sortie.out)["schema_version"] == 1

    destination = tmp_path / "exports" / "faits.json"
    assert main(["--racine", str(racine), "--sortie", str(destination)]) == 0
    assert json.loads(destination.read_text(encoding="utf-8"))["schema_version"] == 1


def test_extraction_reelle_reproductible_et_reliee_au_graphe() -> None:
    """L'inventaire réel inclut les modules, les tests et les pages du dépôt."""
    racine = Path(__file__).resolve().parents[1]

    faits = extraire_faits(racine)
    identifiants = {fait.id for fait in faits}
    json_1 = serialiser(faits)
    json_2 = serialiser(extraire_faits(racine))

    assert json_1 == json_2
    assert "python_module:src/jdriftx/graphe_connaissances.py" in identifiants
    assert "python_module:src/jdriftx/extraction_graphe.py" in identifiants
    assert "test_file:tests/test_graphe_connaissances.py" in identifiants
    assert "test_file:tests/test_extraction_graphe.py" in identifiants
    assert "quarto_page:site/projet/carte-connaissances.qmd" in identifiants
    assert "quarto_page:site/_extensions/live/_knitr.qmd" not in identifiants
