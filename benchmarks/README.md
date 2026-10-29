# Benchmarks

Instrument de mesure de coût livré dans le cadre de l'issue [#17](https://github.com/JM-Brun/J-DriftX/issues/17), désormais close pour ce livrable. Il pose un instrument pour mesurer certains moments de coût aux jalons G1 et suivants. **Aucune revendication de gain n'est faite ici** : les chiffres produits par ces scripts sont indicatifs et dépendants de la machine.

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
  ce squelette ; voir `docs/20` et `docs/21`, puis les issues opérationnelles
  [#204–#207](https://github.com/JM-Brun/J-DriftX/issues/204). L'ancienne
  issue #13 est close comme remplacée.
- Ce squelette n'établit aucune propriété physique ni aucun gain prédictif.
