# 50 — Étape 5 : oracle indépendant et protocole de coûts pour S0 uniforme

**Statut :** protocole et outillage implémentés ; les mesures de performance ne sont pas encore exécutées sur un environnement de référence ni interprétées. Voir l'issue [#244](https://github.com/JM-Brun/J-DriftX/issues/244).

## 1. Objet et portée

Comparer l'évaluation dirigée implémentée à l'étape 4 ([PR #241](https://github.com/JM-Brun/J-DriftX/pull/241)) à une formule scalaire indépendante du chemin d'exécution, sur les 12 points du cas S0 uniforme de [la note 48](48-cas-reference-autonome-ecoulement-uniforme.md).

L'oracle recalcule directement la solution gaussienne pour la classe C avec les coefficients explicites de la note 48. Il n'appelle ni `pseudo_distance_uniforme`, ni `PanacheGaussien`, ni `concentration_panache`, ni les fonctions de coefficients de production. Il partage toutefois le même modèle analytique et les mêmes paramètres physiques : **il vérifie indépendamment le chemin de calcul, pas la validité du modèle physique ou des sources historiques**.

## 2. Protocole pré-enregistré

- **Cas :** vent uniforme `U = 3.0 m/s`, débit `Q = 2.0 kg/s`, classe C, hauteur effective `H = 1.0 m`, altitude de mesure `z = 1.5 m`.
- **Grille :** `x = {100, 200, 400, 800} m`, `y = {-50, 0, 50} m`, soit 12 points ; grille inchangée.
- **Formules indépendantes :** `sigma_y = 0.11 x / sqrt(1 + 0.0001 x)` et `sigma_z = 0.08 x / sqrt(1 + 0.0002 x)`, puis formule gaussienne avec réflexion au sol.
- **Tolérance :** `abs_error <= 1e-15 kg/m^3 + 1e-12 * abs(C_oracle)`. L'erreur relative utilise `max(abs(C_oracle), 1e-15 kg/m^3)` au dénominateur ; le plancher est explicite.
- **Répétitions :** au moins 5 ; défaut 1000. Une invocation d'échauffement est exclue des mesures. Toutes les durées brutes et statistiques médiane, moyenne, écart-type, minimum et maximum sont émises.
- **Coûts :** préparation (construction de la source et de la grille), inférence sur un point (médiane du coût grille / 12), coût total d'une charge de 12 requêtes et pic d'allocations Python suivies par `tracemalloc`. Aucun calibrage n'existe dans ce cas : il ne faut pas présenter la préparation comme un coût de calibration.
- **Environnement :** version Python, plateforme, NumPy, Pydantic et version du package consignées dans le JSON.

## 3. Reproduction

Depuis la racine du dépôt :

```bash
uv run python scripts/benchmark_baseline_uniforme.py --repetitions 1000 --output artifacts/baseline-uniforme-step5.json
uv run pytest tests/test_baseline_oracle.py tests/test_baseline_uniforme.py
```

Le JSON produit contient les valeurs par point, les erreurs, toutes les répétitions chronométrées, les statistiques et les métadonnées d'environnement. Il doit être versionné après exécution dans un environnement déclaré ; ne pas inventer ni recopier des mesures issues de la CI comme si elles représentaient un benchmark stable.

## 4. Limites d'interprétation

1. L'oracle est indépendant de l'implémentation et du chemin d'exécution, mais pas du modèle analytique ni des hypothèses/paramètres communs.
2. L'égalité numérique sur 12 points établit une cohérence entre deux implémentations de la formule, pas une validation météorologique, expérimentale ou applicative.
3. `tracemalloc` rapporte le pic d'allocations Python tracées, pas la mémoire résidente du processus ni toutes les allocations natives de NumPy.
4. Les durées dépendent de la machine, de la charge et du runtime ; elles sont descriptives, non un résultat universel.
5. Aucun facteur d'accélération historique `10^3–10^4` n'est validé : le coût de préparation et la comparaison avec un solveur maillé historiquement comparable ne sont pas établis.
6. Le contre-exemple de cisaillement reste séparé ([note 33](33-test-contre-exemple-cisaillement.md)). Rien ici ne permet d'extrapoler à un champ variable, au multi-niveaux, à des données terrain ou à DIFLU.
