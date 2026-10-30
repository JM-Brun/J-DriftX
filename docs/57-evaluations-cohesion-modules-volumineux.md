# 57 — Évaluations de cohésion P2 : modules volumineux (chantier #303, P2)

## Statut

Note d'évaluation portant la tranche **P2** du [chantier qualité #303](https://github.com/JM-Brun/J-DriftX/issues/303) : évaluation de cohésion, de responsabilités et de dépendances des modules > 15 ko listés dans [l'annexe A de la note 56](56-cartographie-architecturale-bounded-contexts.md). **Aucun refactoring n'est appliqué dans cette note** : conformément à la règle du chantier, la taille seule ne justifie pas une extraction. Cette note ne change aucune équation, tolérance, contrat d'exécution ni test.

## 1. Méthode — critères du gabarit transitoire_puff

Le précédent `transitoire_puff` ([docs/54](54-transitoire-puff-edp-transitoire-marginale.md)) est le gabarit de référence : un monolithe de 648 lignes est devenu un package de 5 modules parce que des **frontières métier nettes** existaient (marginale fermée, schéma transitoire, comparaison, manifeste), et l'identité numérique a été prouvée par des tests inchangés. Les critères retenus pour chaque module évalué :

1. une frontière métier ou technique nette existe (pas une découpe par taille) ;
2. l'identité numérique est démontrable (tests inchangés, équivalence byte-exact si un calcul est déplacé) ;
3. le bénéfice est concret : plusieurs consommateurs, point d'extension ou réduction de duplication ;
4. le coût de migration est maîtrisé (imports, CI, tests de synchronisation).

Sources factuelles : squelettes des modules (classes, fonctions, sections), docstrings de module, imports réels vérifiés sur `main` (recherche de code), tailles de l'annexe A de la note 56.

## 2. Verdicts

| Module | Lignes | Verdict |
|---|---|---|
| `experiences/reference_independante.py` | 960 | **Extraction ciblée différée** : `GrilleEdp` et `EchantillonneurBilineaire` ont déjà deux consommateurs (transitoire_puff) ; frontière nette identifiée, à exécuter à la prochaine extension qui touche ces objets (S0-b ou R3). |
| `experiences/identification_source.py` | 633 | **Statu quo** : tranche verticale uniforme, une seule expérience. |
| `experiences/modele_reduit_edp.py` | 502 | **Statu quo** : tranche verticale uniforme (scénario, deux routes, manifeste). |
| `graphe_connaissances.py` | 527 | **Statu quo confirmé** : déjà tranché par la note 56 §7 (déplacement = étiquette sans gain). |
| `figures/wind_field_explorer.py` | 558 | **Statu quo** : rendu pur déléguant le calcul à `fields` (C3), responsabilité unique documentée. |
| `experiences/relief.py` | 498 | **Statu quo** : tranche verticale uniforme. |
| `experiences/superposition_sources.py` | 441 | **Statu quo** : tranche verticale uniforme. |
| `figures/figure_06.py` | 488 | **Statu quo** : rendu pur d'une expérience testée, miroir du gabarit figure_01/figure_02. |

**Bilan : aucune décomposition n'est justifiée aujourd'hui.** La taille des modules d'expériences est structurée par le gabarit vertical commun (validation → scénario typé → résolution → résultat → manifeste) imposé par la charte qualité ; chaque module porte une seule expérience ou une seule figure.

## 3. Le seul signal architectural réel : la grille EDP partagée

`transitoire_puff/marginale.py` importe `EchantillonneurBilineaire` et `GrilleEdp` depuis `experiences/reference_independante.py` (vérifié sur `main`). Ces deux objets forment une frontière technique nette (géométrie et lecture d'un champ sur grille, sans physique propre), et le docstring de `reference_independante.py` les documente déjà comme points d'extension de S0-b et R3.

Recommandation : **différer l'extraction** (par exemple vers un sous-module `experiences/grille_edp.py` ou un package partagé) jusqu'à l'extension S0-b ou R3, qui touchera ces objets de toute façon. Le seuil « deux consommateurs » est atteint, mais migrer maintenant ferait porter le coût de compatibilité (imports, tests, registre du graphe) sans bénéfice immédiat ; l'extension S0-b/R3 offrira le moment naturel, avec le gabarit d'identité numérique de docs/54 (tests inchangés). À l'extraction, la façade historique `reference_independante` conservera les ré-exports pendant une période de compatibilité (règle n°5 de #303).

## 4. Duplications transverses (item P2 n°3 de #303)

Inventaire : `_valide_point` et `_coins` sont dupliqués dans `identification_source.py`, `relief.py` et `superposition_sources.py` (trois exemplaires courts de validation géométrique). Les autres blocs de validation sont propres à chaque expérience.

Recommandation : **statu quo**. Extraire ces helpers créerait une couche générique prématurée, que l'item P2 n°3 demande explicitement d'éviter ; la divergence éventuelle des règles reste détectable en revue. À revisiter si une quatrième expérience les duplique.

## 5. Bande de surveillance 10–15 ko

Aucune action : les modules de la bande (`figure_03/04/05`, `reconstruction_vent`, `figure_01`, `baseline_uniforme`, `evaluation_puff`) suivent les mêmes gabarits verticaux. Recomptage au prochain point P2.

## 6. Suites

- Items P2 n°1 et n°2 du chantier #303 : soldés par cette note (aucune frontière nette ne justifie une décomposition aujourd'hui) ;
- Item P2 n°3 : soldé par l'inventaire §4, recommandation statu quo ;
- Item P2 n°4 : conventions stables (gabarit vertical homogène, langue par module) ;
- Réévaluation : à l'ouverture de S0-b ou R3 (§3) ; recomptage des tailles à ce moment.

## Références

- [Chantier qualité #303](https://github.com/JM-Brun/J-DriftX/issues/303) — plan P0–P3, définition of done par tranche.
- [docs/54](54-transitoire-puff-edp-transitoire-marginale.md) — gabarit de référence de l'extraction (identité numérique par tests inchangés).
- [docs/56](56-cartographie-architecturale-bounded-contexts.md) — annexe A (modules > 15 ko), contextes C1–C8, exception `reliefs → terrain`.
- [docs/25](25-audit-harmonisation-oop-2026.md) et [docs/22](22-audit-package-code.md) — charte qualité et audit du package.
