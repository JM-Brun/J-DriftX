# 25 — Audit d'harmonisation OOP du package (26 octobre 2026)

## 1. Objet et méthode

Mandat : vérifier si le code Python nécessite d'autres refactorings du même
type que la modélisation objet des classes de stabilité (PR #96), afin d'obtenir
un code plus propre, plus robuste, plus harmonieux et plus orienté objet.

Méthode identique à l'audit docs/22 : **audit documentaire uniquement, aucun
réusinage appliqué dans cette PR** — les arbitrages appartiennent au
propriétaire. Périmètre : l'intégralité de `src/jdriftx` (13 modules, dont
`experiences/` et `figures/`) a été relue, ainsi que les 15 fichiers de
tests. État audité : `main` au 26/10/2026 ; les PR #95 (tests superposition)
et #96 (objets ClasseStabilite/FormeSigmaZ) étaient ouvertes au moment de
l'audit et sont prises en compte comme acquises quand leur apport est cité
(constat P3 n° 2).

## 2. Verdict global

Le noyau est sain. Après la PR #96, il n'existe **plus aucun `dict` interne
porteur de données dans `src/`** : le seul cas restant de l'audit docs/22
(tables Briggs) est traité. Les objets portant un état ou un invariant sont
des dataclasses frozen validées à la construction ; `champ_analytique.py`
(Protocol `ChampPlan`, composition `SuperpositionChamps`) et
`experiences/` (configuration → résultats → manifeste typés, `dict`
confinés à `vers_dict`) sont les exemplars à suivre pour tout nouveau module.

Aucun refactoring « remplacer des tables par des objets » ne reste donc
nécessaire. Les constats ci-dessous sont des opportunités d'harmonisation,
hiérarchisées P1 à P3, avec options et arbitrages explicites.

## 3. Constat P1 — `constraints.linearite` : signature générique faiblement typée

Signature actuelle :

```python
def linearite(
    modele: Callable[..., np.ndarray],
    point: tuple[float, float, float],
    q1: float,
    q2: float,
    **kwargs: float,
) -> bool:
```

Deux défauts réels, vérifiés :

1. **Annotation fausse.** L'unique usage (`tests/test_constraints.py`) passe
   `classe="D"` — une `str` — dans des kwargs annotés `float`. mypy ne le
   détecte pas car la CI type `src/` uniquement, pas les tests : l'appel
   fautif vit hors périmètre. L'écart avait été signalé par docs/22 et n'a
   pas été traité depuis (la PR #82 a traité la fermeture `rhs` et la
   validation partagée, pas ceci).
2. **Kwargs non vérifiés.** Une coquille (`clsse="D"`) traverse
   `linearite` silencieusement et échoue plus profond dans le modèle, avec
   un message moins clair.

Options :

- **Option A (recommandée)** — spécialiser sans casser : ajouter une fonction
  dédiée et intégralement typée
  `linearite_panache(point, q1, q2, *, u, classe, hauteur=0.0)` enveloppant
  `concentration_panache`, et retyper la fonction générique en
  `**kwargs: object` avec une docstring explicite (« passés tels quels au
  modèle, non vérifiés ici »). Aucun appel existant ne casse ; le cas nominal
  devient typé de bout en bout.
- **Option B** — réparer l'annotation seulement : `**kwargs: float | str`
  (la non-vérification demeure).
- **Option C** — rester générique via un `Protocol` de modèle de
  concentration : surdimensionné pour deux modèles.

Estimation : ~20 lignes + 2-3 tests GWT. Décision attendue : A ou B.

## 4. Constat P2 — Vocabulaires clos : `Literal` vs `StrEnum`

Trois vocabulaires clos restent en `Literal` avec branche défensive à
l'exécution :

- `fields.py` : `FieldKind = Literal["uniform", "shear", "radial"]` +
  `raise ValueError("Unknown field kind")` ;
- `terrain.py` : `TerrainKind = Literal["flat", "hill", "valley", "ridge"]`
  + branche analogue ;
- `trajectories.py` : `IntegrationMethod = Literal["euler", "rk4"]`.

La PR #96 a établi le pattern `StrEnum` (`ClasseStabilite`,
`FormeSigmaZ`). Harmoniser ces trois vocabulaires donnerait des membres
autodocumentés, itérables et vérifiables par itération. Nuances honnêtes :

- `Literal` est **déjà sûr côté types** (mypy strict) ; contrairement au cas
  Briggs, **aucune donnée n'est dupliquée** dans des tables : ce n'est pas un
  défaut de correction, seulement une question d'harmonisation.
- Les branches `else` resteraient nécessaires à l'exécution (`Literal`
  n'est pas appliqué au runtime) ; seuls les messages d'erreur seraient à
  garder mot pour mot.
- Les apps passent des chaînes : un `StrEnum` à identifiants stables
  (membre = chaîne, comme `ClasseStabilite`) garantit la compatibilité.

Recommandation : arbitrage propriétaire. Si oui : trois petits `StrEnum`
avec garde de non-régression des messages d'erreur, sur le modèle de #96.

## 5. Constat P2 — Duplication résiduelle entre les deux solveurs périodiques

Depuis la PR #82, la validation des paramètres est partagée
(`_validate_periodic_parameters`). Restent dupliqués entre
`solve_periodic_sine_transport` et `solve_periodic_upwind_euler` :

- la construction de la grille (`dx = length / n_cells` puis
  `x = np.arange(n_cells) * dx`) ;
- l'évaluation de la condition initiale
  (`periodic_sine_solution(x, 0.0, ...)`) ;
- la garde `end_time == 0` (retour de l'état initial, pas effectif nul).

Soit environ dix lignes par solveur. Options :

- **Helper privé** `_etat_initial_periodique(...)` retournant
  `(x, initial, actual_dt)` — non cassant, recommandé si on y touche ;
- en profiter, ou non, pour un objet résultat (voir ci-dessous).

Second volet : les deux solveurs retournent le tuple
`(x, concentration, actual_dt)`. Une dataclass frozen
`ResultatPeriodique` serait plus harmonieuse avec `ResultatDirige` et
`ResultatReconstruction`, mais **cassante** pour tous les tests qui
déballent le tuple. Arbitrage : le changement de signature est-il accepté ?

## 6. Constat P2 — Langues mixtes dans `src/`

Deux conventions coexistent : docstrings et messages **en français**
(`metric`, `similitude`, `stabilite`, `experiences`,
`champ_analytique`, `figures`) contre **en anglais** (`trajectories`,
`fields`, `terrain`, `periodic_transport`, `advection_diffusion` ;
`constraints` est mixte : docstrings FR, identifiants EN). Une
harmonisation totale représenterait un remaniement important (messages
d'erreur testés mot pour mot, figures comprises). Recommandation : **ne pas
migrer rétroactivement** ; statuer la convention dans CONTRIBUTING (le
nouveau code du projet est déjà majoritairement FR : PR #71, #73, #80, #96)
et laisser les modules EN converger à l'occasion de modifications
ultérieures. Arbitrage propriétaire.

## 7. Constats P3 — Micro-harmonisations

1. `integrate_trajectory` retourne `(times, xs, ys)` : une dataclass frozen
   `Trajectoire` est candidate, même arbitrage que le tuple périodique
   (changement cassant).
2. Après fusion de la PR #96 : élargir les annotations `classe: str` en
   `str | ClasseStabilite` dans `concentration_panache`,
   `concentration_puff`, `sigma_y` et `sigma_z`, pour documenter le
   contrat réellement accepté (les deux formes sont déjà validées par
   `_valide_classe`).
3. Exports racine `__init__.py` : `trajectories`, `fields`, `terrain`,
   `periodic_transport` et `advection_diffusion` ne sont pas exportés
   (modules d'enseignement ?). Si c'est volontaire, une phrase dans la
   docstring du `__init__` évite toute confusion ; sinon, harmoniser.
4. Constantes de disposition de `figures/figure_01.py` (`PANEL_*`,
   `ECHELLE_*`) : un groupement en dataclass est possible, mais il n'y a
   **aucun invariant réel** à protéger et le test de synchronisation SVG
   byte-exact couvre déjà le sujet. Recommandation : ne rien faire.

## 8. Points conformes (aucune action requise)

- Plus aucun `dict` interne dans `src/` (charte satisfaite après #96) ;
  `dict` confinés aux frontières (`vers_dict`, apps).
- `champ_analytique.py` (Protocol + dataclasses frozen, divergence nulle
  par construction) et `experiences/` : exemplars à suivre.
- mypy --strict homogène, validation d'entrée systématique, suite de tests
  intégralement au format Given/When/Then, couverture 94 % (seuil 91).
- Noyau NumPy-only ; streamlit/plotly confinés aux apps ; solveurs
  périodiques numériquement indépendants (validation croisée).

## 9. Invariants à préserver (toute exécution des recommandations)

1. Noyau NumPy-only ; `dict`/JSON aux frontières uniquement.
2. Assets SVG byte-exact (tests de synchronisation) : ne pas régénérer les
   figures sans re-vérification.
3. Messages d'erreur historiques testés mot pour mot (sigma_*, validation
   périodique partagée).
4. Solveurs périodiques indépendants : pas de factorisation du schéma
   numérique lui-même, seulement de la préparation d'état.
5. TDD Given/When/Then, docstrings FR pour le nouveau code, ruff
   line-length 100, deux lignes vides entre définitions de premier niveau,
   tri RUF022 du `__all__`.

## 10. Table des recommandations

| N° | Priorité | Constat | Recommandation | Décision |
|----|----------|---------|---------------|----------|
| 1 | P1 | `linearite` : kwargs non vérifiés, annotation fausse (`classe` est un `str`) | Spécialiser + retyper (option A) | propriétaire |
| 2 | P2 | `Literal` vs `StrEnum` (fields, terrain, trajectories) | Harmonisation optionnelle, pattern #96 | propriétaire |
| 3 | P2 | Duplication grille / CI / garde `end_time == 0` entre solveurs | Helper privé non cassant | propriétaire |
| 4 | P2 | Tuples de résultats (solveurs périodiques, trajectoires) | Dataclasses si le remaniement des tests est accepté | propriétaire |
| 5 | P2 | Langues mixtes FR/EN dans `src/` | Statuer la convention, convergence progressive | propriétaire |
| 6 | P3 | `classe: str` → `str | ClasseStabilite` (après fusion de #96) | À l'occasion d'une PR sur `similitude` | faible risque |
| 7 | P3 | Exports racine incohérents | Documenter l'intention | propriétaire |
| 8 | P3 | Constantes de disposition `figure_01` | Ne rien faire (aucun invariant) | — |

Cet audit ne dépend d'aucune fusion (files disjoints des PR #95 et #96) ; la
recommandation n° 6 suppose la fusion de la PR #96.
