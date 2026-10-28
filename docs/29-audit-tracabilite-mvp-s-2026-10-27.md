# Audit de traçabilité du MVP-S — 2026-10-27

## Objet et méthode

Cet audit croise la matrice publique `docs/27-matrice-tracabilite-mvp-s.md` avec les fonctions et tests effectivement présents dans `src/jdriftx/metric.py` et `tests/test_metric.py`. Il vérifie la cohérence de la chaîne :

**définition → hypothèses → démonstration ou référence → code → tests → portée**.

Cet audit documentaire ne constitue ni une exécution locale des tests, ni une revue mathématique indépendante de toutes les preuves de `docs/19-investigation-g0s-temps-de-parcours.md`.

## Résultats du contrôle croisé

| Objet | Définition / hypothèses | Code et tests vérifiés dans les sources | Conclusion / limite |
|---|---|---|---|
| V1 — temps de première arrivée, cas constant 1D | `dx/dt = vitesse` constante signée ; temps initial nul ; cible exacte ; convention (+infty) si inaccessible | `temps_premiere_arrivee_1d`; `test_1d_first_arrival_constant_velocity`; tests d'entrées non finies et de débordement du déplacement | Cohérent pour la spécialisation constante 1D. Aucun solveur de champ variable n'est fourni. |
| V1 — propriétés générales | Champ stationnaire (C^1), trajectoire maximale et hypothèses précisées dans l'investigation G0-S | Pas de fonction générale correspondante ; les tests de la fonction constante ne couvrent pas ces propositions | La portée est correctement restreinte dans la matrice. Les propositions générales restent des résultats documentaires à relire indépendamment ; elles ne sont pas « validées par les tests ». |
| V2 — temps après projection, cas uniforme 2D | Champ constant non nul ; coût longitudinal ; coût nul sur la frontière transverse ; (+infty) seulement pour une projection strictement en amont selon la convention locale | `pseudo_distance_uniforme`; tests de formule, translation, rotation, échelle de vitesse, déplacement transverse, asymétrie et vent nul | Cohérent avec la définition locale implémentée. La convention transverse dégénérée est explicite. Cela ne reproduit pas la projection historique générale sur une caractéristique courbe. |
| Coût de polyligne | Polyligne ordonnée et vitesse par segment ; norme de vitesse au-dessus de (u_{min}>0) | `temps_transport`; tests longueur/vitesse, inversion du chemin et du signe du vent, détour, formes, seuils et entrées non finies | Cohérent comme somme discrète longueur/norme. Ce n'est ni un temps dirigé physiquement validé, ni un solveur de trajectoire, ni une minimisation. |
| Navigation minimale | Ensemble admissible de chemins, coût, domaine et contraintes nécessaires | Pas de solveur ni de test de minimisation identifié | Explicitement hors périmètre ; ne pas assimiler le coût d'une polyligne donnée à un optimum. |
| Conservation, positivité et validité atmosphérique | Équation de transport, données, conditions aux limites et méthode numérique nécessaires | Non établies par les fonctions de `metric.py` ni par `tests/test_metric.py` | Explicitement hors preuve du MVP-S. Aucun changement de code ne se justifie sans un modèle physique et un protocole distincts. |

## Points de vigilance qui restent ouverts

1. **Relecture mathématique indépendante.** La matrice référence les propositions 3.2 et 3.3 de l'investigation G0-S pour les propriétés générales de V1. Une seconde revue indépendante des preuves, hypothèses et cas limites reste nécessaire avant d'élever leur statut au-delà de « démontré dans le document ».
2. **Reproduction locale propre.** Le bilan `docs/21-bilan-mvp-s-1d.md` indique que les commandes complètes doivent être exécutées dans un environnement propre et les versions/sorties archivées. La CI seule ne ferme pas ce critère.
3. **Décision de sortie.** Le statut global MVP-S reste ouvert jusqu'à une décision explicite : clôture limitée au noyau démontré, restriction, ou arrêt. G0-A reste une décision séparée et non franchie.
4. **État de l'art / nouveauté.** La conclusion « nouveauté non établie » doit rester en place tant que la comparaison aux antécédents n'est pas conclue et documentée selon les critères du document de définition du MVP.

## Décisions

- **Aucun nouveau nœud sémantique n'est justifié par cet audit.** Les lacunes identifiées sont des limites de portée ou des tâches de validation, pas des concepts manquants à ajouter au graphe.
- **Aucun nouveau test logiciel n'est requis pour prétendre à un solveur général** : celui-ci n'est pas implémenté. Il faut soit maintenir cette limite, soit spécifier un nouveau modèle avant d'écrire du code.
- **La matrice actuelle est cohérente avec les fonctions et tests inspectés**, sous réserve des tâches ouvertes ci-dessus. La cohérence documentaire ne remplace pas la reproduction ni la revue indépendante.

## Sources de vérité

- [Matrice MVP-S](27-matrice-tracabilite-mvp-s.md)
- [Investigation G0-S](19-investigation-g0s-temps-de-parcours.md)
- [Bilan MVP-S 1D](21-bilan-mvp-s-1d.md)
- [Définition du MVP et critères de sortie](https://github.com/JM-Brun/career-knowledge/blob/main/jdriftx/notes/11-mvp-definition-of-done.md)
