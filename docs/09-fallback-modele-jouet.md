# Fallback scientifique : modèle jouet et contribution théorique

> **Règle de décision :** si J-DriftX ne démontre pas d'utilité pratique ou d'avantage face aux méthodes existantes, le projet ne doit ni maquiller ce résultat ni continuer à étendre une architecture applicative sans justification. Il peut être réorienté vers un modèle jouet mathématique, explicitement limité, reproductible et intéressant pour comprendre une idée.

Ce fallback est une stratégie de recherche, pas une preuve anticipée que l'approche actuelle possède une nouveauté théorique. La nouveauté et l'intérêt du modèle jouet devront eux aussi être confrontés à la littérature.

## 1. Pourquoi un modèle jouet est un résultat légitime

Un modèle jouet peut isoler un mécanisme et rendre ses propriétés démontrables. Il peut produire une contribution utile à l'enseignement, à l'intuition mathématique ou à l'étude d'un phénomène limite, même s'il n'est pas un outil prédictif pour une application réelle.

Il faut cependant distinguer :
- **un exemple pédagogique** qui illustre une idée connue ;
- **un résultat théorique** qui établit une propriété sous des hypothèses explicites ;
- **une contribution originale** qui ajoute quelque chose de nouveau à la littérature ;
- **un modèle applicable** dont la pertinence est validée dans un domaine réel.

Le projet ne doit revendiquer que le niveau effectivement atteint.

## 2. Arbre de décision

1. **L'approche répond-elle à un besoin pratique documenté ?**
   - Oui : tester l'avantage contre des baselines, puis valider sur données indépendantes.
   - Incertain : construire le test discriminant le moins coûteux ; ne pas ajouter de fonctionnalités.
   - Non : passer à l'évaluation du potentiel théorique.
2. **Existe-t-il une propriété mathématique précise, non triviale et démontrable ?**
   - Oui : isoler les hypothèses, établir la preuve, chercher contre-exemples et cas limites.
   - Non : simplifier le modèle ou le traiter comme démonstration pédagogique, sans prétention de contribution théorique.
3. **Le résultat est-il nouveau et correctement positionné dans la littérature ?**
   - Oui, après vérification : développer une note théorique ou un article ciblé.
   - Non : documenter l'exemple pédagogique, citer les travaux existants et arrêter la revendication d'originalité.
4. **Le modèle jouet aide-t-il à comprendre ou à tester une idée ?**
   - Oui : le conserver comme banc d'essai minimal et ressource pédagogique.
   - Non : archiver la piste avec la justification de la décision.

## 3. Modèle jouet candidat : transport unidimensionnel à vitesse variable

Un premier candidat, à confirmer après revue des travaux connexes, est un problème de transport 1D dans lequel le temps de parcours dirigé peut être comparé à une distance géométrique symétrique.

Soit un intervalle (x\in[0,L]), une vitesse strictement positive (u(x)>0) et un transport dans le sens croissant de (x). Le temps de parcours dans ce sens est

\[
T_+(a,b)=\int_a^b \frac{1}{u(x)}\,dx,\qquad a\le b.
\]

Pour (b<a), le temps de parcours inverse doit être défini selon une dynamique physique spécifiée ; il ne faut pas simplement inverser les bornes et obtenir un temps négatif. Dans un modèle réversible simplifié, on peut introduire une vitesse de retour (u_-(x)>0) et définir séparément

\[
T_-(b,a)=\int_b^a \frac{1}{u_-(x)}\,dx.
\]

Si l'on choisit (u_-(x)=u(x)), le temps de parcours le long du même chemin est positif dans les deux sens et ne constitue pas à lui seul une asymétrie. Une véritable asymétrie de temps de parcours exige un mécanisme directionnel explicite — par exemple des vitesses advectives différentes, une dynamique non réversible ou une définition orientée du coût. Ce point est une précaution conceptuelle centrale : **une intégrale de vitesse positive le long d'un chemin n'est pas automatiquement une métrique non symétrique**.

Le modèle jouet devrait donc comparer explicitement :
- distance euclidienne ou coût géométrique symétrique ;
- temps de parcours orienté induit par un champ de vitesse et des règles de propagation ;
- prédiction ou noyau de transport construit à partir de chacun ;
- comportement en présence d'un champ uniforme, d'un champ variable, d'un obstacle ou d'une inversion de direction, selon la définition retenue.

Ne pas appeler automatiquement (T) une métrique : vérifier les axiomes pertinents. Une fonction de coût dirigée peut être une quasi-distance ou une distance asymétrique si elle satisfait les propriétés correspondantes ; le vocabulaire doit suivre la définition mathématique.

### Résultats à chercher

1. Une définition sans ambiguïté des objets et de leur domaine.
2. Des propriétés élémentaires démontrées (positivité, séparation éventuelle, inégalité triangulaire dirigée, conditions d'asymétrie).
3. Des exemples calculables à la main.
4. Des contre-exemples montrant ce que la construction ne garantit pas.
5. Une expérience numérique minimale qui compare les quantités calculées aux expressions analytiques.
6. Une recherche bibliographique ciblée pour établir si la construction ou le résultat est déjà connu.

Ce modèle ne prétend pas représenter à lui seul la dispersion atmosphérique, les turbulences ou la dérive de pulvérisation. Il sert d'abord à tester une idée mathématique isolée.

## 4. Autres options de fallback

| Option | Question scientifique | Livrable possible | Limite |
|---|---|---|---|
| Cas analytique de transport | Quelles propriétés découlent réellement de la définition du temps de parcours ? | Note avec propositions, preuves et contre-exemples | Peut être connu dans la littérature |
| Noyau anisotrope minimal | Comment une géométrie dirigée change-t-elle une fonction de propagation ? | Visualisation, étude de paramètres, cas limites | Illustration seule, pas nécessairement originale |
| Comparaison pédagogique des modèles | Quand une représentation simple échoue-t-elle par rapport à une référence ? | Notebook reproductible et guide d'interprétation | Valeur principalement pédagogique |
| Contre-exemples de conservation/positivité | Quelles constructions naïves violent les contraintes physiques ? | Tests et note technique sur les limites | Ne constitue pas à elle seule un nouveau modèle |
| Problème inverse minimal | Quelles observations suffisent à identifier un paramètre dans un modèle jouet ? | Analyse d'identifiabilité et exemples non identifiables | Ne garantit pas le passage aux données réelles |

## 5. Critères d'acceptation du fallback

Le fallback est réussi s'il produit :
- une définition mathématique sans ambiguïté ;
- au moins une proposition non triviale ou une démonstration pédagogique rigoureuse ;
- une preuve vérifiée et des contre-exemples pertinents ;
- un code ou notebook minimal reproductible, si le calcul numérique est utile ;
- une section explicite « ce que ce modèle ne démontre pas » ;
- des références pertinentes et une formulation prudente de la nouveauté ;
- une décision documentée : contribution théorique, ressource pédagogique, ou arrêt.

Il n'est pas nécessaire de développer une API, un plugin SIG, un système de calibration général ou une interface graphique pour satisfaire ces critères.

## 6. Plan d'exécution si G0 ou G2 échoue

1. Conserver les résultats négatifs et la raison de la décision dans le dépôt.
2. Identifier quelle hypothèse a échoué : importance du besoin, cohérence théorique, précision, coût ou généralisation.
3. Réduire le problème à la plus petite construction mathématique qui conserve la question intéressante.
4. Vérifier la littérature sur cette construction et ses propriétés.
5. Formaliser les définitions et rechercher des preuves et contre-exemples.
6. Créer un test analytique et une illustration numérique reproductible.
7. Décider entre note théorique, ressource pédagogique, nouvelle hypothèse applicative ou arrêt.

**Principe :** l'échec de l'objectif applicatif ne transforme pas automatiquement une idée en contribution théorique originale. Le fallback doit passer son propre test de valeur, de rigueur et de positionnement dans l'état de l'art.

## Documents liés

- [Décider de l'utilité de J-DriftX et construire une preuve](08-decision-utilite-et-preuve.md)
- [Feuille de route J-DriftX v2](03-roadmap-jdriftx-v2.md)
