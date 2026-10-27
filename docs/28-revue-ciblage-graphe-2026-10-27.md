# Revue ciblée des pages candidates au graphe — 2026-10-27

## Objet

Cette revue examine les douze pages non associées identifiées comme prioritaires dans le premier diagnostic du graphe, en les confrontant à la [matrice MVP-S de traçabilité définition–hypothèses–démonstration–code–tests–portée](27-matrice-tracabilite-mvp-s.md).

**Décision principale : aucun nouveau nœud sémantique n'est ajouté dans cette revue.** Le registre actuel représente des concepts, hypothèses, propriétés, modules, tests, références et jeux de données candidats ; il ne doit pas devenir un catalogue de pages. Aucune des douze pages ne justifie actuellement un nouveau concept distinct sans risquer de transformer une page de synthèse, un protocole ou une hypothèse non démontrée en objet scientifique autonome. Les liens vers la matrice sont ajoutés aux pages où ils clarifient directement le statut des preuves.

## Décisions par page

| Page | Rapport à la matrice MVP-S | Décision de graphe | Action |
|---|---|---|---|
| [Limites et domaines de validité](../site/hypotheses/limites.qmd) | Complète la portée des modèles ; toutes les limites décrites ne sont ni implémentées ni testées. | **Omission intentionnelle** : catalogue transversal de limites, pas un concept unique. | Ajout d'un lien explicite vers la matrice et avertissement sur la couverture limitée du noyau actuel. |
| [Panorama de l'état de l'art](../site/etat-art/panorama.qmd) | Sert à cadrer les méthodes et les incertitudes, sans prouver les performances du prototype. | **Omission intentionnelle** : revue de littérature, pas nœud conceptuel. | Ajout d'un lien qui sépare constats bibliographiques et preuves propres au prototype. |
| [Positionnement](../site/etat-art/positionnement.qmd) | Présente des hypothèses différenciantes qui restent à tester. | **Omission intentionnelle** : les hypothèses de nouveauté/supériorité ne sont pas des résultats acquis. | Ajout d'un lien vers le périmètre actuellement établi. |
| [Revue mathématique ciblée](../site/etat-art/revue-mathematique.qmd) | Distingue temps de parcours, temps minimal et première arrivée ; analyse les limites des formulations et du code. | **Pas de nouveau nœud** : les objets centraux sont déjà représentés par `c-tau`, `c-pdist` et `c-tpa`. Un nœud supplémentaire de page ferait doublon. | Ajout d'un lien vers la matrice, en complément du bilan MVP-S et de la page travel-time. |
| [Comparaison des complexités](../site/theorie/comparaison-complexites.qmd) | Décrit des profils de coût structurels ; ne présente pas de benchmark complet à précision comparable. | **Omission intentionnelle** : pas de résultat mesuré autonome à représenter. | Ajout d'un lien rappelant la différence entre comparaison qualitative et résultats implémentés/testés. |
| [Métriques non riemanniennes](../site/theorie/metriques-non-riemanniennes.qmd) | Explique le contexte géométrique des coûts orientés et les limites de la définition historique. | **Pas de nouveau nœud** : les concepts centraux sont déjà couverts par `c-tau` et `c-pdist`. | Ajout d'un lien vers la matrice pour borner les propriétés attribuables au code. |
| [Carte d'articulation](../site/projet/carte-articulation.qmd) | Donne une navigation entre niveaux du projet et niveaux de preuve. | **Omission intentionnelle** : page méta-navigation, distincte du contenu sémantique du graphe. | Ajout d'un lien explicite vers la matrice comme complément de preuve, pas comme arête sémantique. |
| [Héritage Drift-X](../site/projet/heritage.qmd) | Apporte de la provenance historique ; ne change pas la portée de preuve du MVP-S. | **Omission intentionnelle** : les sources historiques sont déjà représentées par les nœuds de références et les concepts associés. | Aucun changement : la navigation bibliographique existante suffit pour l'instant. |
| [Modèle jouet](../site/projet/modele-jouet.qmd) | Le candidat de modèle plus général ne doit pas être confondu avec la référence 1D à vitesse constante déjà implémentée. | **Omission intentionnelle, à réexaminer** lorsque le modèle aura une définition et des hypothèses stabilisées, un code et des tests associés. | Ajout d'un lien précisant que le noyau 1D actuel ne valide pas le modèle jouet général. |
| [Qualité et tests](../site/projet/qualite.qmd) | Décrit les vérifications finies et leurs limites. La matrice relie chaque propriété aux tests pertinents. | **Omission intentionnelle** : processus qualité, pas propriété scientifique ; les tests précis sont déjà des nœuds. | Ajout d'un lien direct vers la matrice. |
| [Utilité scientifique](../site/projet/utilite-scientifique.qmd) | Définit les critères à satisfaire pour établir une utilité scientifique, méthodologique ou applicative. | **Omission intentionnelle** : critères de décision, pas preuve de valeur acquise. | Ajout d'un lien vers l'état vérifiable du prototype. |
| [Validation scientifique](../site/projet/validation-scientifique.qmd) | Décrit le protocole futur et les critères de benchmark ; le protocole ne valide pas lui-même le modèle. | **Omission intentionnelle** : protocole méthodologique, pas résultat ou propriété validée. | Ajout d'un lien distinguant critères et preuves actuellement disponibles. |

## Ce qui a changé dans le site

Des liens directs vers la matrice ont été ajoutés aux onze pages où ils améliorent la lecture des affirmations et des limites. La page d'héritage reste inchangée : sa fonction principale est la provenance historique, déjà représentée par les références du graphe.

Ces liens sont de la navigation documentaire ; ils ne sont **pas** de nouvelles arêtes du graphe. Aucun nœud ni aucune relation sémantique n'a été inventé pour faire baisser le nombre de fichiers non mappés.

## Conditions de réexamen

Réouvrir une décision seulement lorsqu'un contenu nouveau justifie un objet sémantique indépendant :

1. **Modèle jouet** : définition mathématique stable, hypothèses explicites, code correspondant et tests de référence. Le nœud éventuel devra pointer vers la définition, et ses relations distingueront ce qui est implémenté de ce qui est seulement visé.
2. **Complexité / performance** : benchmark reproductible avec observable, baseline, précision comparable, coût de préparation/calibration/inférence et incertitude explicités. Une comparaison descriptive seule ne suffit pas.
3. **Limites** : créer un nœud de propriété uniquement si une limite devient une affirmation précise reliée à ses hypothèses, sa preuve ou référence, son code et ses tests — pas pour représenter toute la page.
4. **Validation** : ajouter un nœud de propriété seulement après un résultat validé et reproductible ; un protocole ou une CI verte ne suffisent pas.

## Contrôles de portée à conserver

- Une correspondance de chemin ne démontre pas une relation scientifique.
- Un test fini ne démontre pas une propriété universelle.
- Le code de référence 1D à vitesse constante ne constitue pas un solveur général de champ variable.
- Les propriétés physiques de conservation, de positivité ou de validité atmosphérique ne doivent pas être revendiquées au-delà de leur modèle, hypothèses et tests documentés dans la matrice.
- Le taux de couverture du graphe n'est pas un KPI à maximiser : une omission explicitement justifiée est préférable à un nœud redondant ou trompeur.
