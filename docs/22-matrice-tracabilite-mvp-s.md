# MVP-S — matrice publique de traçabilité des définitions et des preuves

> **État :** audit documentaire du 26 octobre 2026. Cette matrice relie les définitions, leurs hypothèses, le code et les tests. Elle ne remplace pas les preuves analytiques et ne vaut pas validation physique. Les tests doivent être lus comme des vérifications finies.

## Statuts utilisés

- **Démontré analytiquement** : une dérivation ou une preuve explicite est donnée sous des hypothèses précisées.
- **Testé** : des exemples ou cas limites sont vérifiés par les tests nommés ; cela ne prouve pas une propriété universelle.
- **Implémenté** : le code calcule la quantité annoncée.
- **Non établi / non implémenté** : aucune preuve ou implémentation correspondante n'est revendiquée.

## Matrice

| Objet ou affirmation | Définition et hypothèses | Démonstration ou référence | Code | Tests pertinents | Portée |
|---|---|---|---|---|---|
| **V1 — première arrivée 1D à vitesse constante** | Sur la droite réelle, \(\dot{x}=u\) avec \(u\) constant signé. Temps initial 0 ; cible atteinte exactement. | Solution \(x(t)=a+ut\). Si \(a=b\), le temps vaut 0. Si \(u\ne0\) et le déplacement est dans le sens de \(u\), \(T=|b-a|/|u|\) ; sinon la convention choisie est \(+\infty\). | `temps_premiere_arrivee_1d` dans `src/jdriftx/metric.py`. | `test_1d_first_arrival_constant_velocity`; `test_1d_first_arrival_rejects_non_finite_inputs`; `test_1d_first_arrival_rejects_infinite_displacement`. | Formule fermée démontrée pour le modèle constant, implémentée et testée sur des cas ciblés. Ce n'est pas un solveur de champ variable. |
| **V1 — propriétés générales du temps de première arrivée** | Champ autonome et hypothèses de régularité assurant trajectoires et unicité ; temps étendu avec \(+\infty\) pour l'inaccessibilité. | Voir les preuves des propositions 3.2 et 3.3 dans [l'investigation G0-S](19-investigation-g0s-temps-de-parcours.md). | Ces propriétés générales ne sont pas implémentées comme un solveur général dans le code actuel. | Les tests de V1 portent sur la spécialisation à vitesse constante 1D ; ils ne prouvent pas les propositions générales. | Résultats analytiques sous les hypothèses du document, à ne pas attribuer aux seuls tests de la fonction 1D. |
| **V2 — construction projetée uniforme 2D** | Champ constant \(u\ne0\), projection orthogonale de la cible sur la droite de courant passant par la source ; convention locale \(+\infty\) si la projection est strictement en amont. | Pour \(\Delta=b-a\), \(T_{proj}=\max(0,\Delta\cdot u/\|u\|^2)\) pour la partie finie, et \(+\infty\) si \(\Delta\cdot u<0\). La projection ignore le déplacement transversal. | `pseudo_distance_uniforme`. | `test_uniform_pseudodistance_matches_projection_formula`; `test_uniform_pseudodistance_uses_longitudinal_projection`; tests de translation, rotation, échelle, déplacement transverse et asymétrie. | Référence analytique limitée au champ uniforme. Ce n'est pas l'implémentation générale de la projection historique sur une caractéristique courbe. |
| **V2 — séparation des points** | Même définition V2 uniforme ; déplacement non nul orthogonal au vent. | Si \((b-a)\cdot u=0\), le coût vaut zéro même si \(a\ne b\). C'est un contre-exemple à la séparation métrique. | `pseudo_distance_uniforme`. | `test_uniform_pseudodistance_can_be_zero_for_distinct_points`; `test_uniform_pseudodistance_is_zero_for_upwind_boundary`. | Contre-exemple démontré et testé ; « pseudo-distance » ne signifie pas distance métrique. |
| **V2 — asymétrie directionnelle** | Déplacement longitudinal strictement positif dans le sens du champ uniforme. | L'aller est fini ; au retour, la projection est strictement en amont et la convention donne \(+\infty\). | `pseudo_distance_uniforme`. | `test_uniform_pseudodistance_is_asymmetric_along_the_wind`; `test_uniform_pseudodistance_symmetric_on_transverse_boundary`. | Contre-exemple démontré et testé. La frontière transverse peut toutefois donner zéro dans les deux sens. |
| **Coût de polyligne** | Une polyligne 2D ordonnée ; un vecteur vitesse par segment ; chaque norme de vitesse doit être supérieure ou égale au seuil \(u_{min}>0\). | Définition discrète : \(C=\sum_i \|p_{i+1}-p_i\|/\|u_i\|\). Le seuil est une condition d'acceptation numérique, pas une loi physique. | `temps_transport`. | `test_uniform_speed_time_is_length_over_speed`; `test_polyline_cost_is_invariant_to_path_reversal_and_wind_sign`; `test_longer_path_takes_longer_time_at_same_speed`; tests de formes, seuils et entrées non finies. | Somme discrète implémentée et testée. Elle ignore l'orientation du vent et ne calcule ni caractéristique ni chemin optimal. |
| **Navigation minimale** | Nécessiterait un ensemble de chemins admissibles, un coût, un domaine et des conditions aux limites/obstacles. | Aucun résultat de minimisation ou d'existence d'un minimiseur n'est établi par le code actuel. | Non implémentée dans `metric.py`. | Aucun test de solveur de navigation minimale identifié. | Hors périmètre du MVP-S actuel. Un coût sur un chemin donné n'est pas un optimum sur tous les chemins. |
| **Conservation de masse, positivité de concentration, validité atmosphérique** | Nécessitent une équation physique de transport/dispersion, variables, sources/puits, conditions initiales et de bord et méthode numérique explicites. | Ces propriétés ne découlent pas des définitions de temps de parcours ci-dessus. | Non établi par les primitives de métrique. | Les tests de `test_metric.py` ne valident pas ces propriétés physiques. | Non établi ; aucune revendication physique ne doit être déduite de cette matrice ou d'une CI verte. |

## Limites et lecture correcte

1. **Un test n'est pas une preuve universelle.** Il peut vérifier un exemple, une famille finie de cas ou détecter un contre-exemple.
2. **Une preuve générale et une implémentation particulière ont des portées différentes.** Les propositions générales V1 du document G0-S reposent sur des hypothèses de champ autonome et régulier ; la fonction actuellement codée résout seulement la vitesse constante en 1D.
3. **La V2 codée est une référence uniforme.** La définition historique générale peut rencontrer des caractéristiques courbes et des projections ambiguës, qui ne sont pas traitées par cette fonction.
4. **Le mot « exact » est local au modèle.** Il désigne la formule fermée du cas constant, pas une exactitude numérique absolue ni une validité pour un champ variable.
5. **Le coût de polyligne n'est pas une métrique dirigée.** Il dépend des normes de vitesse et ne tient pas compte de leur orientation.
6. **La CI est une preuve de passage des contrôles exécutés sur un commit donné**, pas une preuve de validité mathématique, de nouveauté ou d'utilité applicative.

## Sources de vérité

- [Investigation G0-S — définitions, dérivations et contre-exemples](19-investigation-g0s-temps-de-parcours.md)
- [Bilan MVP-S 1D](21-bilan-mvp-s-1d.md)
- [Code de référence](../src/jdriftx/metric.py)
- [Tests](../tests/test_metric.py)
