# Benchmarks

Squelette de mesure de coût (issue #17). Objectif : poser l'instrument qui
mesurera les moments de coût du modèle aux jalons G1 et suivants. **Aucune
revendication de gain n'est faite ici** : les chiffres produits par ces
scripts sont indicatifs et dépendants de la machine.

## Moments de coût identifiés

1. **Évaluation ponctuelle** — couvert par `cout_evaluation.py` : coût d'une
   concentration en un point, découplé de la taille du domaine, comparé à la
   construction d'un champ complet sur grille.
2. **Construction de la métrique** — non couvert : coût de construction de τ
   (polylignes, caractéristiques) ; à mesurer quand la métrique généralisée
   existera.
3. **Recalibration** — non couvert : coût d'une recalibration par assimilation ;
   conditionné par le jalon M3.

## Usage

~~~bash
uv run python benchmarks/cout_evaluation.py
uv run python benchmarks/cout_evaluation.py --repetitions 7
~~~

## Limites

- Le panache gaussien vectorisé sur grille **n'est pas** un solveur EDP : la
  comparaison actuelle mesure l'instrument de mesure, pas un gain face à un
  CFD. La référence « EDP/maillage » des jalons G1+ reste à instancier.
- Les protocoles G1 (jeux de données réels, baselines) sont hors périmètre de
  ce squelette ; voir `docs/20`, `docs/21` et l'issue #13.
- Ce squelette n'établit aucune propriété physique ni aucun gain prédictif.
