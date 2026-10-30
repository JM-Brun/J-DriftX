"""Garde-fous statiques pour les frontières architecturales documentées dans docs/56."""

import ast
from collections import defaultdict
from pathlib import Path

RACINE_PACKAGE = Path(__file__).parents[1] / "src" / "jdriftx"
DEPENDANCES_RENDU_INTERDITES = {"matplotlib", "pandas", "plotly", "streamlit"}

CONTEXTES: dict[str, str] = {
    "jdriftx.metric": "C1",
    "jdriftx.similitude": "C1",
    "jdriftx.similitude_objets": "C1",
    "jdriftx.stabilite": "C1",
    "jdriftx.source": "C1",
    "jdriftx.champ_analytique": "C1",
    "jdriftx.constraints": "C1",
    "jdriftx._protocoles": "C2",
    "jdriftx.reliefs": "C2",
    "jdriftx.vents": "C2",
    "jdriftx.concentrations": "C2",
    "jdriftx.contrats": "C2",
    "jdriftx.periodic_transport": "C3",
    "jdriftx.advection_diffusion": "C3",
    "jdriftx.trajectories": "C3",
    "jdriftx.fields": "C3",
    "jdriftx.terrain": "C3",
    "jdriftx.experiences": "C4",
    "jdriftx.benchmarks": "C5",
    "jdriftx.figures": "C6",
    "jdriftx.graphe_connaissances": "C7",
    "jdriftx.extraction_graphe": "C7",
    "jdriftx.diagnostic_graphe": "C7",
}
DEPENDANCES_AUTORISEES = {
    "C1": {"C1"},
    "C2": {"C1", "C2", "C3"},
    "C3": {"C3"},
    "C4": {"C1", "C2", "C3", "C4", "C5"},
    "C5": {"C1", "C5"},
    "C6": {"C1", "C3", "C4", "C6"},
    "C7": {"C7"},
}
EXCEPTION_C2_C3 = {("jdriftx.reliefs", "jdriftx.terrain")}


def _nom_module(chemin: Path) -> str:
    """Convertit un chemin Python du package en nom de module importable."""
    relatif = chemin.relative_to(RACINE_PACKAGE).with_suffix("")
    parties = list(relatif.parts)
    if parties[-1] == "__init__":
        parties.pop()
    return ".".join(("jdriftx", *parties))


def _imports_internes(chemin: Path, module: str) -> set[str]:
    """Extrait les dépendances statiques vers les modules du package."""
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    est_package = chemin.name == "__init__.py"
    package = module if est_package else module.rpartition(".")[0]
    dependances: set[str] = set()

    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            dependances.update(
                alias.name
                for alias in noeud.names
                if alias.name == "jdriftx" or alias.name.startswith("jdriftx.")
            )
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.level:
                parties = package.split(".")
                base = ".".join(parties[: len(parties) - noeud.level + 1])
                cible = f"{base}.{noeud.module}" if noeud.module else base
                if noeud.module:
                    dependances.add(cible)
                else:
                    dependances.update(f"{cible}.{alias.name}" for alias in noeud.names)
            elif noeud.module == "jdriftx" or (
                noeud.module is not None and noeud.module.startswith("jdriftx.")
            ):
                dependances.add(noeud.module)

    return dependances


def _graphe_imports() -> dict[str, set[str]]:
    """Construit le graphe des imports statiques internes à jdriftx."""
    chemins = sorted(RACINE_PACKAGE.rglob("*.py"))
    modules = {_nom_module(chemin): chemin for chemin in chemins}
    graphe: dict[str, set[str]] = defaultdict(set)
    for module, chemin in modules.items():
        graphe[module].update(_imports_internes(chemin, module) & modules.keys())
    return graphe


def _cycles(graphe: dict[str, set[str]]) -> list[list[str]]:
    """Retourne les cycles détectés par parcours en profondeur."""
    visites: set[str] = set()
    pile: list[str] = []
    dans_pile: set[str] = set()
    trouves: list[list[str]] = []

    def visiter(module: str) -> None:
        if module in dans_pile:
            debut = pile.index(module)
            trouves.append([*pile[debut:], module])
            return
        if module in visites:
            return
        visites.add(module)
        pile.append(module)
        dans_pile.add(module)
        for dependance in sorted(graphe[module]):
            visiter(dependance)
        pile.pop()
        dans_pile.remove(module)

    for module in sorted(graphe):
        visiter(module)
    return trouves


def test_modules_du_package_sont_tous_classes_dans_un_contexte() -> None:
    """La cartographie couvre chaque module Python, hors façade racine."""
    modules = set(_graphe_imports()) - {"jdriftx"}
    modules_classes = {
        module
        for module in modules
        if module in CONTEXTES or any(module.startswith(f"{prefix}.") for prefix in CONTEXTES)
    }
    assert modules_classes == modules


def test_dependances_entre_contextes_respectent_la_cartographie() -> None:
    """Les imports réels ne franchissent pas les frontières interdites."""
    graphe = _graphe_imports()
    violations: list[str] = []

    for origine, dependances in graphe.items():
        contexte_origine = CONTEXTES.get(origine)
        if contexte_origine is None:
            continue
        for cible in dependances:
            contexte_cible = CONTEXTES.get(cible)
            if contexte_cible is None:
                contexte_cible = next(
                    (
                        contexte
                        for prefixe, contexte in CONTEXTES.items()
                        if cible.startswith(f"{prefixe}.")
                    ),
                    None,
                )
            if contexte_cible is None:
                continue
            autorise = contexte_cible in DEPENDANCES_AUTORISEES[contexte_origine]
            exception_documentee = (origine, cible) in EXCEPTION_C2_C3
            if not autorise or (
                contexte_origine == "C2" and contexte_cible == "C3" and not exception_documentee
            ):
                violations.append(f"{origine} ({contexte_origine}) -> {cible} ({contexte_cible})")

    assert not violations, "\n".join(violations)


def test_package_nimporte_pas_de_rendu_ou_dinterface() -> None:
    """Le package reste indépendant des bibliothèques de rendu et d'interface."""
    imports_interdits: list[str] = []

    for chemin in sorted(RACINE_PACKAGE.rglob("*.py")):
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                noms = [alias.name.split(".")[0] for alias in noeud.names]
            elif isinstance(noeud, ast.ImportFrom) and noeud.module:
                noms = [noeud.module.split(".")[0]]
            else:
                continue
            for nom in noms:
                if nom in DEPENDANCES_RENDU_INTERDITES:
                    imports_interdits.append(f"{chemin.relative_to(RACINE_PACKAGE)}: {nom}")

    assert not imports_interdits, "\n".join(imports_interdits)


def test_graphe_des_imports_statiques_est_acyclique() -> None:
    """Les imports directs entre modules ne forment pas de cycle."""
    cycles = _cycles(_graphe_imports())
    assert not cycles, "\n".join(" -> ".join(cycle) for cycle in cycles)
