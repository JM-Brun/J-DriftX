# Contribuer à J-DriftX

Ce dépôt est un projet de recherche : **la rigueur scientifique et la qualité du code priment sur l'ajout de fonctionnalités**. Les règles suivantes s'appliquent à toute contribution de code.

## Flux de travail

1. Créer une branche courte depuis `main`.
2. Faire **un** changement cohérent par pull request, avec un objectif clair.
3. Ouvrir une PR vers `main` ; ne jamais committer directement sur `main`.
4. Expliquer dans la PR l'objectif, la validation effectuée et les incertitudes.
5. La CI doit être verte avant fusion : `ruff check` + `ruff format --check`, `mypy --strict`, `pytest --cov=jdriftx`, rendu du site Quarto.

## Qualité du code

- **Orienté objet, responsabilités séparées.** Chaque module a un rôle identifié (`metric`, `fields`, `trajectories`, `similitude`, `terrain`…). Une classe n'existe que si elle porte un état ou un invariant utile ; privilégier la composition et des protocoles/interfaces explicites aux hiérarchies de classes profondes ; pas de classe « manager » fourre-tout, pas de couche qui ne fait que relayer des appels.
- **Typage strict partout.** `mypy --strict` doit passer sur `src/` ; toute signature est annotée ; pas de `Any` implicite ni de type de retour omis.
- **Structures typées plutôt que `dict` ou DataFrame.** Les objets du domaine (points, champs, sources, configurations, résultats) sont des dataclasses/classes ou des tableaux NumPy ; on évite les `dict` et les DataFrame pandas comme porteurs de données internes quand une structure typée est possible. Les `dict`/JSON restent confinés aux frontières (fichiers de configuration, exports) et sont convertis tôt vers des objets typés validés.
- **Séparation calcul / rendu / IO.** Le cœur (`src/jdriftx`) ne dépend ni de Matplotlib, ni de QGIS, ni de formats de fichiers ; les figures et pages consomment des résultats calculés par le cœur, elles ne réimplémentent pas la physique (cf. `figure_02.py`, qui appelle `pseudo_distance_uniforme` au lieu de dupliquer la formule).
- **Ne pas réinventer la roue.** Préférer une bibliothèque existante, efficace et raisonnablement légère (NumPy, SciPy) à du code maison ; toute nouvelle dépendance est justifiée dans la PR (besoin réel, licence, maintenance, coût d'installation) et idéalement appuyée par un mini-benchmark comparatif.

## Tests — TDD

- **TDD** : écrire d'abord le test (cas analytique, propriété mathématique, cas limite), puis l'implémentation, puis refactorer. Une figure seule ne valide rien.
- **Structure Given / When / Then** : chaque test sépare visiblement la donnée d'entrée (`# Given`), l'action testée (`# When`) et l'assertion (`# Then`). Les tests existants convergent progressivement vers ce format ; tout nouveau test le suit.
- **Couverture** : la CI mesure la couverture (`pytest --cov=jdriftx --cov-report=term-missing`). Viser une couverture élevée sur le cœur, sans écrire de tests creux pour le score ; un seuil `--cov-fail-under` sera fixé (issue #16) une fois la ligne de base mesurée.
- **Régression** : conserver des sorties de référence légères (tableaux numériques versionnés, tolérances documentées) ; comparer des champs et des métriques, jamais des captures d'écran.
- Les tests de propriétés mathématiques et physiques ne valident que **sous les hypothèses qui les garantissent** (cf. README) ; un test de propriété ne démontre ni l'exactitude empirique ni l'utilité applicative du modèle.

## Contributions scientifiques

- Toute affirmation est sourcée et traçable ; ne jamais présenter une reconstruction synthétique comme une reproduction quantitative des papiers historiques.
- Séparer explicitement, dans la PR, ce qui est transcription vérifiée d'une source de ce qui est hypothèse nouvelle.
- Les figures portent leur statut de fidélité (schéma explicatif / reconstruction conceptuelle / reproduction numérique) et un manifeste de régénération.
