# Squelette benchmarks/reference : cas analytique S0

> **Statut — squelette reproductible, aucun résultat anticipé.** Ce document répond à l'issue [#17](https://github.com/JM-Brun/J-DriftX/issues/17) : définir le cas analytique minimal, choisir les métriques et mesures de coût, préparer une commande reproductible et documenter la baseline — **sans anticiper aucun résultat**. Le cas S0 n'est pas une validation physique ; aucun benchmark applicatif ne démarre avant la porte G1 (inspection des fichiers, [#204](https://github.com/JM-Brun/J-DriftX/issues/204), déléguée).

## 1. Cas analytique reproductible S0

- **Source** : émission continue de débit massique Q (kg s⁻¹) à hauteur effective H.
- **Champ de vitesse** : vent uniforme U (m s⁻¹) selon +x, classe de stabilité de Pasquill fixée (défaut : C, site rural).
- **Vérité** : la solution de similitude du package elle-même (module jdriftx.similitude, fonction concentration_panache, tables de Briggs/Pasquill, réflexion au sol incluse) — aucun développement mathématique dupliqué.
- **Observable** : concentration aérienne (kg m⁻³), conformément à [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
- **Grille de prélèvements** : arcs sous le vent (défaut : 100, 200, 400, 800 m) × positions latérales (défaut : −50, 0, +50 m) à altitude de mesure fixée (défaut : 1,5 m).
- **Cas par défaut** : constante CAS_S0_DEFAUT (vent 3 m/s, débit 2 kg/s, classe C, hauteur 1 m).

Conformément à docs/21 (famille S0) : générateur déterministe, aucune donnée observée, clause « pas une validation physique ».

## 2. Métriques d'erreur et mesures de coût

Métriques **préenregistrées par [#43](https://github.com/JM-Brun/J-DriftX/issues/43), inchangées** :

- **FAC2** : fraction des points avec 0,5 ≤ prediction/vérité ≤ 2, bornes incluses, ratio point à point.
- **NMSE** : Σ(prediction − vérité)² / Σ(vérité)². **Convention explicite** : d'autres usages prennent Σ(vérité × prediction) au dénominateur ; le choix est documenté dans les docstrings pour lever toute ambiguïté avant tout benchmark.
- Évaluation **par essai/scénario indépendant** (jamais par point isolé), conformément à #43.

Mesures de coût (issue #17 : préparation et inférence) : la fonction mesurer_cout_inference mesure le temps d'un appel d'inférence ; la mesure est **non déterministe** et n'entre dans aucune assertion. Les seuils de succès G2 (au moins 60 % des essais indépendants ; coût total au moins 10× inférieur pour erreur comparable) restent ceux de #43.

## 3. Commande reproductible

~~~bash
uv run python -m jdriftx.benchmarks.reference
~~~

Le passage à vide évalue la prédiction contre elle-même : FAC2 = 1 et NMSE = 0 sont des **contrôles d'auto-cohérence du pipeline** (grille → vérité → métriques), pas un résultat scientifique. Toute évaluation future d'un candidat contre la vérité S0 passe par evaluer_prediction(vérité, prédiction).

## 4. Baseline et hypothèses communes

- **Baseline** (préenregistrée par #43) : panache gaussien simple, mêmes entrées, même observable. Dans le cas S0, la vérité analytique **est** la baseline gaussienne : le squelette vérifie donc le pipeline, et n'établit aucune supériorité.
- **Hypothèses communes** : linéarité (H1), stationnarité sur la fenêtre (H3), homogénéité du segment (H5), vent uniforme non nul ; garde-fou de #43 : le cas S0 teste une hypothèse de méthode sur un scalaire, pas la dérive de pulvérisation.
- **Ce que le squelette ne fait pas** : aucune comparaison de modèle, aucun résultat rapporté, aucun seuil modifié, aucune donnée observée (G1) chargée.

## 5. Périmètre et suivi

| Élément de #17 | Statut |
|---|---|
| Cas analytique reproductible (source, champ, observable) | **Fait** (section 1, classe CasS0) |
| Métriques d'erreur et mesures de coût | **Fait** (section 2, conventions explicites) |
| Squelette + commande reproductible sans résultat | **Fait** (section 3, commande reproductible) |
| Baseline et hypothèses communes documentées | **Fait** (section 4) |
| Benchmark applicatif sur données observées | **Non commencé — bloqué** par G1 (#204, DIFLU déléguée) et la décision G0-A du propriétaire |

L'issue #17 reste ouverte tant que le benchmark applicatif n'a pas de donnée inspectée ; le squelette S0 est la première brique, réutilisable telle quelle pour la famille S1 (vérités bruitées, docs/21) quand la porte G1 sera franchie.

## Références

- Squelette : [src/jdriftx/benchmarks/reference.py](../src/jdriftx/benchmarks/reference.py) ; tests GWT : [tests/test_benchmarks_reference.py](../tests/test_benchmarks_reference.py).
- Critères préenregistrés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43) ; cas synthétiques S0–S3 : [docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md).
