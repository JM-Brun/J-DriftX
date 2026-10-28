# MVP-S 1D — bilan de reproductibilité et état des preuves

**État au 26 octobre 2026.** Cette note est un état des lieux technique et scientifique, pas une déclaration de clôture du MVP-S. La portée des résultats analytiques doit être lue au regard des hypothèses de chaque section : le cadre général stationnaire \(C^1\) est distinct des exemples 1D élargis aux champs non lipschitziens et aux endpoints.

## 1. Périmètre réellement implémenté

Le noyau de référence contient trois objets qui ne doivent pas être confondus :

- `temps_premiere_arrivee_1d(a, b, vitesse)` : temps exact de première arrivée pour l'EDO stationnaire \\(dx/dt = u\\), où \\(u\\) est une vitesse signée constante. Une cible dans le sens opposé au mouvement est inaccessible (`+inf`), comme toute cible distincte lorsque \\(u=0\\).
- `pseudo_distance_uniforme(a, b, vent)` : référence analytique projetée dans un champ uniforme 2D ; le coût transversal est nul et la convention locale pour une cible en amont est `+inf`.
- `temps_transport(ligne, vent)` : somme discrète longueur/norme de vitesse sur une polyligne fournie ; cette fonction ignore le signe du vent et n'est pas un solveur de caractéristiques.

La première primitive rend le cas constant 1D du temps de première arrivée (V1) exécutable. Aucune de ces primitives ne constitue un solveur général de champ variable, une implémentation complète de la projection historique en 2D, ni une validation physique du modèle de dispersion.

## 2. Reproduction locale

Prérequis : Python compatible avec `requires-python` dans `pyproject.toml`, `uv` et Quarto si le rendu documentaire complet est souhaité.

Depuis la racine du dépôt :

```bash
uv sync --group dev
uv run pytest tests/test_metric.py
uv run ruff check src/jdriftx/metric.py tests/test_metric.py
uv run ruff format --check src/jdriftx/metric.py tests/test_metric.py
uv run mypy src/jdriftx
```

Pour la suite des contrôles automatisés du dépôt, exécuter également :

```bash
uv run pytest --cov=jdriftx
uv run ruff check .
uv run ruff format --check .
uv run pre-commit run --all-files
```

Le rendu Quarto et la construction du paquet Pyodide requièrent l'environnement correspondant au workflow CI du dépôt. La CI ne remplace pas la reproduction locale : elle établit seulement que les étapes listées dans le workflow ont réussi sur le commit testé.

## 3. État des preuves

| Élément | Statut au 26/10/2026 | Portée exacte |
|---|---|---|
| Cas V1 constant 1D | **Implémenté** | Primitive analytique exacte pour une vitesse constante signée |
| Cas 1D et cas uniformes ciblés | **Testé en CI** | Tests déterministes du dépôt ; pas une validation de tous les champs possibles |
| Construction projetée uniforme 2D | **Implémentée et testée** | Convention locale documentée ; fidélité historique complète non établie |
| Coût de polyligne | **Implémenté et testé** | Somme longueur/norme, sans directionnalité physique |
| Limites mathématiques et contre-exemples de la définition V2 (temps après projection) | **Démontrés dans le périmètre analytique documenté** | Ne pas transférer ces résultats à un solveur de champ variable inexistant |
| Exécution du workflow qualité | **Reproduite en CI** | Run [#440](https://github.com/JM-Brun/J-DriftX/actions/runs/40239614200), succès sur le head synchronisé de la PR #81 |
| Comparaison exhaustive aux antécédents | **Non achevée** | Pas de revendication de nouveauté |
| Utilité applicative / performance prédictive | **Inconnue, G0-A non franchi** | Aucun benchmark applicatif autorisé par ce bilan |
| Validation atmosphérique indépendante | **Non réalisée** | Aucun résultat de validité physique ne découle des tests |

## 4. Limites et décision de suite

Les cas analytiques et la CI justifient de conserver ce noyau comme **prototype pédagogique et de vérification mathématique restreint**. Ils ne justifient pas d'étendre maintenant le modèle à un solveur 2D, à un benchmark applicatif ou à une revendication de nouveauté.

**Décision proposée, à ratifier dans le suivi de projet :** considérer la tranche de code MVP-S constant 1D comme implémentée et couverte par CI, mais garder le jalon global MVP-S ouvert jusqu'à ce que (a) la reproduction locale soit effectivement exécutée et son environnement consigné, (b) la comparaison aux antécédents soit conclue, et (c) une décision explicite soit prise sur l'arrêt ou la poursuite. G0-A reste séparé et non franchi.

## 5. Traçabilité des affirmations

La [matrice publique de traçabilité](27-matrice-tracabilite-mvp-s.md) relie les définitions MVP-S à leurs hypothèses, démonstrations ou contre-exemples, fonctions et tests nommés. Elle distingue les résultats démontrés analytiquement des vérifications finies par tests. En particulier, les tests de la fonction V1 constante 1D ne démontrent pas les propriétés générales du temps de première arrivée présentées dans l'investigation G0-S.

La reproduction locale est un contrôle de portabilité de l'environnement ; elle ne constitue pas une preuve mathématique. La CI documente le passage des contrôles automatisés sur le commit effectivement testé. Ni l'une ni l'autre ne valide à elle seule la nouveauté, l'utilité applicative ou la physique du modèle.

## 6. Sources de vérité

- [Matrice de traçabilité : définitions, hypothèses, preuves et tests](27-matrice-tracabilite-mvp-s.md)
- [Investigation G0-S — définitions, dérivations et contre-exemples](19-investigation-g0s-temps-de-parcours.md)
- [Code de référence](../src/jdriftx/metric.py)
- [Tests](../tests/test_metric.py)
- [Définition du MVP et critères de sortie](https://github.com/JM-Brun/career-knowledge/blob/main/jdriftx/notes/11-mvp-definition-of-done.md)
- [PR #81 — primitive 1D](https://github.com/JM-Brun/J-DriftX/pull/81)
