# Contribuer à J-DriftX

Ce dépôt est un projet de recherche : **la rigueur scientifique et la qualité du code priment sur l'ajout de fonctionnalités**. Chaque PR doit annoncer son mode de contribution, sa question précise et le type de preuve qu'elle apporte. Une contribution documentaire, mathématique, logicielle ou expérimentale n'est pas évaluée avec les mêmes critères. Le Wiki canonique est actuellement privé : les pages publiques de J-DriftX ne doivent pas envoyer les lecteurs vers des URLs Wiki inaccessibles. Citer des sources publiques accessibles et inclure uniquement la définition concise nécessaire à comprendre l'application locale ; ne pas recopier un chapitre général complet.

## Modes de contribution

Choisir un ou plusieurs modes et les indiquer dans la PR.

1. **Revue de sources et état de l'art** — ajouter une source primaire, compléter une fiche de lecture ou confronter des affirmations historiques. Fournir une référence vérifiable, séparer transcription, interprétation et hypothèse, et signaler les incertitudes bibliographiques.
2. **Définition ou formulation mathématique** — préciser une définition, ses domaines, hypothèses, conventions, unités et cas limites. Donner une dérivation ou une source, des exemples analytiques et des contre-exemples lorsque c'est utile. Relier les changements aux conséquences attendues dans le code et les tests.
3. **Méthode numérique ou implémentation** — modifier le cœur Python, un algorithme, une interface de domaine ou une dépendance. Fournir un contrat explicite, des tests analytiques/de propriétés/de régression adaptés et expliquer les écarts avec les formulations de référence.
4. **Tests et diagnostic de preuve** — ajouter un cas de référence, une propriété, une tolérance, un test de régression ou un diagnostic du graphe. Indiquer exactement ce que le test établit et sous quelles hypothèses ; ne pas confondre test logiciel, preuve mathématique et validation empirique.
5. **Expérience numérique ou benchmark** — annoncer la question et l'hypothèse, les cas comparés, les paramètres, les données/champs, les versions, les métriques, les tolérances et le protocole de reproduction. Rapporter les résultats négatifs et les limites ; ne pas extrapoler au-delà du domaine testé.
6. **Documentation scientifique, figures et site** — améliorer l'articulation, le glossaire, les schémas ou les pages Quarto. Identifier le statut de chaque figure (schéma explicatif, reconstruction conceptuelle ou reproduction numérique), ses sources et son mode de régénération. Le rendu seul ne valide pas une affirmation scientifique.
7. **Graphe et traçabilité théorie–code–tests** — modifier le registre sémantique ou l'extraction structurelle. Garder le registre TOML comme source des relations revues et les faits extraits comme inventaire, sans inférer automatiquement une relation scientifique depuis un nom ou un lien.

## Flux de travail

1. Créer une branche courte depuis `main`.
2. Faire un changement cohérent et ouvrir une PR vers `main` ; ne jamais committer directement sur `main`.
3. Décrire la question, le mode de contribution, les hypothèses affectées, les preuves ajoutées et ce qui reste non démontré.
4. Relier les changements mathématiques à leurs implémentations et tests, et inversement lorsque c'est pertinent.
5. La CI doit être verte avant fusion : `ruff check` + `ruff format --check`, `mypy --strict`, `pytest --cov=jdriftx --cov-fail-under=91`, rendu du site Quarto.

## Qualité du code

- **Orienté objet, responsabilités séparées.** Chaque module a un rôle identifié (`metric`, `fields`, `trajectories`, `similitude`, `terrain`…). Une classe n'existe que si elle porte un état ou un invariant utile ; privilégier la composition et des protocoles/interfaces explicites aux hiérarchies de classes profondes ; pas de classe « manager » fourre-tout, pas de couche qui ne fait que relayer des appels.
- **Typage strict partout.** `mypy --strict` doit passer sur `src/` ; toute signature est annotée ; pas de `Any` implicite ni de type de retour omis.
- **Structures typées plutôt que `dict` ou DataFrame.** Les objets du domaine sont des dataclasses/classes ou des tableaux NumPy ; éviter les `dict` et DataFrame pandas comme porteurs internes quand une structure typée convient. Les `dict`/JSON restent aux frontières et sont convertis tôt vers des objets typés validés.
- **Séparation calcul / rendu / IO.** Le cœur (`src/jdriftx`) ne dépend ni de Matplotlib, ni de QGIS, ni de formats de fichiers ; figures et pages consomment les résultats du cœur et ne réimplémentent pas la physique.
- **Ne pas réinventer la roue.** Justifier toute nouvelle dépendance (besoin, licence, maintenance, coût d'installation), idéalement avec un mini-benchmark.
- **Langue du code.** Les docstrings et messages des nouveaux modules sont
  rédigés en français. Les modules d'enseignement existants en anglais
  (`trajectories`, `fields`, `terrain`, `periodic_transport`,
  `advection_diffusion`) ne sont pas migrés rétroactivement : un ajout
  ponctuel y suit la langue du module, et ils convergent à l'occasion d'une
  modification substantielle (audit docs/25, recommandation 5).

## Tests — TDD

- Écrire d'abord le test (cas analytique, propriété mathématique, cas limite), puis l'implémentation, puis refactorer.
- Chaque nouveau test sépare visiblement donnée d'entrée (`# Given`), action (`# When`) et assertion (`# Then`).
- La CI applique un seuil de couverture `--cov-fail-under=91`. Viser une couverture élevée sur le cœur sans écrire de tests creux.
- Conserver des sorties de référence légères et tolérances documentées ; comparer des champs et métriques, jamais des captures d'écran.
- Les tests de propriétés générées (Hypothesis) énoncent la propriété sous ses hypothèses exactes, avec des stratégies bornées (coût de CI maîtrisé) et `@settings(deadline=None)` ; un contre-exemple généré est un bogue, une absence de contre-exemple n'est ni une preuve mathématique ni une validation physique (règles détaillées : docs/40).
- Les tests de propriétés mathématiques et physiques ne valident que **sous les hypothèses qui les garantissent** ; un test ne démontre ni exactitude empirique ni utilité applicative.

## Contributions scientifiques

- Toute affirmation est sourcée et traçable ; ne jamais présenter une reconstruction synthétique comme une reproduction quantitative des papiers historiques.
- Séparer dans la PR transcription vérifiée d'une source et hypothèse nouvelle.
- Les figures portent leur statut de fidélité et un manifeste de régénération.

## Carte des connaissances

Le graphe est généré depuis `site/data/graphe-connaissances.toml` par `src/jdriftx/graphe_connaissances.py`, et le rendu `site/projet/_graphes-mermaid.md` est committé. Pour ajouter/modifier un nœud, une arête ou une vue : éditer le registre, exécuter `uv run python -m jdriftx.graphe_connaissances`, puis committer ensemble le registre et le rendu.

Le registre TOML reste la source de vérité des **relations sémantiques revues**. L'extracteur structurel recense des faits observables sans leur attribuer de sens scientifique. Un lien Markdown ne prouve pas une affirmation ; une proximité de nom ne prouve pas qu'une fonction implémente un concept. Les diagnostics sont à examiner, pas des erreurs automatiques.

## Validation et limites des preuves

Écrire dans la PR les commandes réellement exécutées et leurs résultats. Si un contrôle est impossible, expliquer pourquoi. Une CI verte vérifie les contrôles configurés ; elle ne constitue ni une preuve mathématique générale, ni une validation scientifique empirique, ni une démonstration d'utilité applicative.
