# Audit du package `jdriftx` — code, tests et applications au regard de la charte qualité

> **Statut : audit exécuté le 23 octobre 2026**, suite à l’adoption de la [charte qualité](../CONTRIBUTING.md) (PR #65). Périmètre : intégralité du package `src/jdriftx` (huit modules + `figures/figure_02.py` + `__init__.py`), les neuf fichiers de tests, les trois applications Streamlit de `apps/`, `pyproject.toml` et le workflow CI.
> **Méthode et limites explicites.** Audit documentaire par lecture intégrale du code source, **sans exécution instrumentée** : la couverture de tests exacte n’a pas été mesurée depuis l’environnement d’audit (la CI la mesure déjà via `--cov-report=term-missing` mais sans seuil, cf. [issue #16](https://github.com/JM-Brun/J-DriftX/issues/16)). Conformément à la charte, **aucune modification de code n’est proposée ni appliquée dans cette PR** : les recommandations sont hiérarchisées pour les itérations suivantes.

## Synthèse

| Axe de la charte | État constaté | Verdict |
|---|---|---|
| OOP, responsabilités séparées, modules identifiés | API 100 % fonctionnelle ; huit modules à responsabilité unique, bien nommés, docstrings avec limites scientifiques explicites | Conforme au noyau actuel ; vigilance sur la saturation des signatures physiques |
| Typage strict | `mypy --strict` sur `src/` en CI ; `NDArray`/`ArrayLike`, docstrings complètes, validation d’entrée systématique avec `ValueError` | Bon ; un point faible (`**kwargs` non vérifiés dans `constraints.linearite`) |
| Structures typées vs `dict`/DataFrame | Aucun pandas ; `dict` confinés aux tables de constantes Briggs et aux frontières UI | Conforme ; un sélecteur de forme par chaîne candidat `Enum` |
| Séparation calcul / rendu / IO | `src/` importe uniquement numpy ; rendu confiné aux apps (plotly) et figures (stdlib) | Excellent, invariant à préserver |
| Ne pas réinventer la roue | numpy seule dépendance runtime ; solveurs maison = validation croisée justifiée | Conforme |
| TDD Given/When/Then | Environ 50 tests comportementaux solides (cas analytiques, ordres de convergence mesurés, conservation, rejets) ; **aucun au format Given/When/Then** | Partiel — convergence progressive à planifier |
| Couverture mesurée avec seuil | Couverture affichée en CI sans `--cov-fail-under` | À figer ([issue #16](https://github.com/JM-Brun/J-DriftX/issues/16)) |

## 0. Périmètre audité

- **Noyau `src/jdriftx`** : `advection_diffusion`, `constraints`, `fields`, `metric`, `periodic_transport`, `similitude`, `terrain`, `trajectories`, plus `figures/figure_02.py` (rendu SVG stdlib) et `__init__.py` (ré-export des fonctions publiques).
- **Tests `tests/`** : neuf fichiers, environ 50 tests.
- **Applications `apps/`** : `convergence_lab.py`, `interactive_lab.py`, `scientific_validation.py` (Streamlit + plotly).
- **Configuration** : `pyproject.toml` (ruff ligne 100, mypy strict sur `src/`, per-file-ignores pour `tests/**`) et `.github/workflows/ci.yml` (job « qualite » : build, ruff, mypy, pytest avec couverture).

## 1. Architecture et responsabilités

**Constat.** Le noyau est entièrement fonctionnel : aucune classe, uniquement des fonctions à arguments scalaires ou tableaux. Chaque module a une responsabilité unique claire :

- `similitude` : solutions de similitude gaussiennes (panache, puff, écarts-types de Briggs) ;
- `advection_diffusion` : cas analytique de référence 1D ;
- `periodic_transport` : deux solveurs numériques indépendants (centré/RK4, amont/Euler) et leur solution exacte ;
- `trajectories` : intégration de particules dans un champ prescrit ;
- `fields` / `terrain` : objets synthétiques pédagogiques ;
- `constraints` : vérifications génériques (positivité, superposition) ;
- `metric` : primitives géométriques provisoires, honnêtement documentées comme telles.

**Appréciation.** C’est conforme à la charte : une classe ne se justifie que si elle porte un état ou un invariant utile, ce qui n’est le cas d’aucun module actuel (fonctions pures sans état partagé). Les docstrings énoncent systématiquement les limites scientifiques (ex. `metric.py` : « approximation géométrique provisoire », pas une métrique non symétrique validée) — cette rigueur déclarative est un point fort à maintenir.

**Vigilance identifiée.** La « signature physique » des fonctions croît : `solve_periodic_sine_transport` et `solve_periodic_upwind_euler` prennent sept paramètres nommés, `concentration_panache` six arguments positionnels. `pyproject.toml` ignore déjà PLR0913/PLR0917 pour ces signatures ; c’est un signal de saturation qui deviendra contraignant lors de la tranche verticale « champ uniforme » (action 5 du document d’architecture), où la même physique sera évaluée sur des configurations composites.

## 2. Typage

**Constat positif.** Typage homogène et strict : `NDArray[np.floating]` / `ArrayLike` selon la nature de l’argument, `Literal` pour les sélecteurs fermés (`FieldKind`, `TerrainKind`, `IntegrationMethod`), `Final` pour les constantes, docstrings complètes au format Google avec unités, messages d’erreur pré-construits (`msg = ...; raise ValueError(msg)`), validation d’entrée systématique (finitude, signes, formes) dans chaque fonction publique. `mypy --strict` passe sur `src/` en CI.

**Point faible unique.** `constraints.linearite` accepte `**kwargs: float` non vérifiés : ni les noms ni l’exhaustivité des arguments attendus par le modèle ne sont contrôlés à l’appel (une faute de frappe remonte en `TypeError` au lieu d’un `ValueError` explicite). Gravité faible (module de vérification pédagogique), à typer davantage si le module se généralise.

## 3. Structures typées vs `dict`/DataFrame

**Constat.** Aucun pandas, aucun DataFrame nulle part. Les `dict` sont confinés à deux usages légitimes :

- tables de constantes `_BRIGGS_SY` / `_BRIGGS_SZ` dans `similitude.py` : données pures indexées par classe de Pasquill — acceptable en l’état (ensemble fermé, couvert par les tests) ;
- tables de correspondance libellés→identifiants dans les apps Streamlit : frontière UI, conforme à la règle « `dict` aux frontières ».

**Candidat d’amélioration (non urgent).** Dans `_BRIGGS_SZ`, la forme verticale est encodée par une chaîne `"lin"`/`"sqrt"`/`"inv"` dans un tuple `tuple[str, float, float]`, puis dispatchée par des `if forme == ...`. Un petit `Enum` (ou une donnée structurée) rendrait le sélecteur fermé et typé au même titre que `FieldKind`. À faire lors d’une prochaine modification du module, pas en réusinage isolé.

## 4. Séparation calcul / rendu / IO

**Constat.** Excellente et vérifiable dans les imports : `src/jdriftx` n’importe que numpy (plus `typing`/`collections.abc` de la stdlib) ; streamlit et plotly n’apparaissent que dans `apps/` ; `figures/figure_02.py` produit du SVG avec la stdlib seule ; aucune écriture de fichier dans le noyau. Les apps importent le cœur sans le dupliquer et affichent systématiquement des avertissements de portée scientifique. Cette frontière est l’invariant le plus précieux du package : **aucune future fonctionnalité de rendu ou d’IO ne doit entrer dans `src/`**.

## 5. Dépendances — ne pas réinventer la roue

**Constat.** Dépendance runtime unique : numpy. Outils de développement légers (pytest, pytest-cov, ruff, mypy, pre-commit) ; groupe `app` séparé (plotly, streamlit). Les solveurs périodiques maison (RK4, Euler amont, différences centrées) ne sont pas une réinvention contestable : ce sont des **schémas de validation croisée volontairement indépendants** de la solution analytique, requis pour éprouver l’implémentation sans dépendre d’un solveur externe. Aucune dépendance lourde n’est justifiée aujourd’hui ; l’arrivée éventuelle de scipy devra être documentée besoin par besoin.

## 6. Tests et TDD

**Constats positifs.** La suite est comportementalement solide pour un noyau de cette taille :

- cas analytiques exacts (gaussienne : masse et variance ; sinusoïde périodique ; cercle en rotation) ;
- **ordres de convergence mesurés et bornés** : spatial 1.8–2.2, temporel 3.5–4.5 pour centré/RK4, comparaison croisée centré-RK4 < amont-Euler ;
- conservation de la moyenne périodique à 1e-12 près, flux intégré du panache restituant le débit (2 %) ;
- rejets systématiques des entrées invalides (paramètres non finis, pas nuls, classes inconnues, instabilité détectée avant intégration).

**Écarts à la charte.**

1. **Aucun test ne suit le découpage Given/When/Then** : les tests actuels sont des séquences d’assertions correctes mais sans structure explicite. La charte impose ce format pour la qualité et la relecture.
2. **Couverture sans seuil** : `pytest --cov=jdriftx --cov-report=term-missing` s’affiche en CI mais n’échoue jamais ; le pourcentage exact est donc suivi nulle part ([issue #16](https://github.com/JM-Brun/J-DriftX/issues/16)).
3. Détail : le helper `_solve` de `test_periodic_transport.py` n’est pas typé (couvert par les `per-file-ignores` de `tests/**`), alors que la fixture `grille` de `test_similitude.py` montre la voie correcte.

## 7. Points techniques secondaires (constatés, sans urgence)

- `trajectories.integrate_trajectory` définit la fermeture `rhs` **à l’intérieur de la boucle `while`** : elle est recréée à chaque pas de temps. La remonter au-dessus de la boucle est un micro-nettoyage sans changement de comportement (à faire au prochain passage sur le module, avec les tests existants comme garde).
- Les deux solveurs périodiques dupliquent **environ vingt lignes de validation d’entrée identiques** : candidate à une fonction privée commune au prochain passage sur `periodic_transport.py`.
- `metric.py` documente explicitement son statut provisoire (temps de parcours sur polyligne ≠ pseudo-distance historique) : à conserver tel quel jusqu’à la décision prévue avant le jalon M1.

## 8. Recommandations hiérarchisées (aucune appliquée dans cet audit)

| Priorité | Action | Référence |
|---|---|---|
| P1 | Mesurer la couverture sur `main`, puis activer `--cov-fail-under` dans la CI (seuil initial prudent, relevé ensuite) | [issue #16](https://github.com/JM-Brun/J-DriftX/issues/16) |
| P1 | Adopter Given/When/Then pour **tout nouveau test** (commentaires `# Given` / `# When` / `# Then` ou sections équivalentes), puis converger progressivement les tests existants — sans réécrire massivement d’un coup | [charte qualité](../CONTRIBUTING.md) |
| P2 | Lors de la tranche verticale « champ uniforme » (action 5), introduire des **dataclasses de configuration** (grille, pas de temps, paramètres physiques) pour les nouvelles signatures, sans réusinage rétroactif du noyau existant | charte, OOP |
| P2 | Extraire la validation commune des deux solveurs périodiques en une fonction privée partagée | §7 |
| P3 | Typer le helper `_solve` de test ; remonter `rhs` hors de la boucle ; envisager un `Enum` pour le sélecteur de forme Briggs | §6, §7 |

**Aucune recommandation ne demande une classe aujourd’hui** : aucun module n’a d’état partagé ni d’invariant qui la justifierait. La charte (composition > hiérarchies, classes seulement si état/invariant utile) est respectée par l’absence même de classes.

## 9. Invariants à préserver dans les itérations suivantes

1. **Noyau numpy-only** : aucune dépendance streamlit/plotly/pandas dans `src/`.
2. **`dict`/JSON confinés aux frontières** : tables de constantes fermées et UI uniquement.
3. **Solveurs périodiques indépendants du modèle de similitude** : la validation croisée exige l’absence de couplage.
4. **Docstrings avec limites scientifiques explicites** pour tout nouveau module (le standard étant celui de `metric.py` et `constraints.py`).
5. **Toute modification de comportement passe par TDD** : test exprimant d’abord le comportement attendu, puis implémentation minimale.

## Sources de l’audit (lecture intégrale, 23 octobre 2026)

- `src/jdriftx/` : `advection_diffusion.py`, `constraints.py`, `fields.py`, `metric.py`, `periodic_transport.py`, `similitude.py`, `terrain.py`, `trajectories.py`, `figures/figure_02.py`, `__init__.py`.
- `tests/` : les neuf fichiers de tests, en particulier `test_periodic_transport.py` et `test_similitude.py`.
- `apps/` : `convergence_lab.py`, `interactive_lab.py`, `scientific_validation.py`.
- `pyproject.toml` (ruff, mypy strict sur `src/`, per-file-ignores), `.github/workflows/ci.yml` (job « qualite »).
- [CONTRIBUTING.md](../CONTRIBUTING.md) — charte qualité (PR #65, décision du propriétaire du 23 octobre 2026).
- [Issue #16](https://github.com/JM-Brun/J-DriftX/issues/16) — couverture et seuil CI ; document d’architecture (action 2 : audit avant figement des interfaces, action 5 : tranche verticale champ uniforme).
