# Protocole de falsification S0–S3 — contrat expérimental proposé

**Statut :** protocole de recherche à spécifier et exécuter. Aucun résultat S1–S3 n'est revendiqué ici. Cette note transforme la revue adversariale du 2 novembre 2026 en plan expérimental, sans dupliquer les contrats S0 déjà suivis par [#232](https://github.com/JM-Brun/J-DriftX/issues/232) et [#244](https://github.com/JM-Brun/J-DriftX/issues/244).

**Illustration :** [protocole-falsification-s0-s3.svg](../site/images/protocole-falsification-s0-s3.svg). Schéma conceptuel, non résultat numérique.

## 1. Question scientifique et hypothèse falsifiable

La question n'est pas de savoir si une formule de temps dirigé peut être calculée, mais si une représentation réduite de la dispersion fournit, pour une observable définie, une approximation suffisamment précise et moins coûteuse qu'une référence indépendante et que des baselines pertinentes.

Hypothèse à tester, sans la tenir pour acquise :

> Pour une classe explicitement bornée de champs de vitesse et de tenseurs de diffusion, une formulation réduite identifiée à l'avance peut prédire le champ de concentration (ou une observable dérivée) avec une erreur et un coût total inférieurs ou comparables aux méthodes de référence.

Le protocole doit pouvoir conclure **conserver**, **restreindre** ou **remplacer** la formulation projetée. Une absence d'avantage est un résultat recevable.

## 2. Objets comparés — nomenclature obligatoire

| Symbole | Définition opérationnelle | Précaution |
|---|---|---|
| $T_{\\mathrm{proj}}$ | Construction historique projetée, avec règle de projection explicitée | Ne pas lui attribuer par défaut l'équation eikonale ou la propriété de temps d'arrivée |
| $T_{\\mathrm{arr}}$ | Temps d'arrivée le long d'une caractéristique issue de la source, calculé par intégration d'EDO et événement | Défini uniquement sur les points atteints par cette caractéristique ; ne résout pas à lui seul la diffusion transverse |
| $T_{\\mathrm{path}}$ | Intégrale $\\int_\\gamma ds/\\lVert u\\rVert$ sur une courbe prescrite | La courbe est une entrée ; ce n'est ni une projection ni une optimisation |
| EDP-FV | Référence indépendante de l'équation conservative d'advection-diffusion, résolue par volumes finis | Le schéma, les flux, les frontières et la convergence doivent être vérifiés séparément |
| Puff | Modèle impulsionnel gaussien advecté et élargi selon une loi explicitée | Le puff Briggs actuellement présent dans le package n'est pas automatiquement un puff lagrangien sur vent variable |

Ne pas confondre le résultat idéal GZ-1, le puff Briggs existant, le cas S0 et un futur solveur Hamilton–Jacobi.

## 3. Équation de référence

Pour le traceur passif, partir de la forme conservative :

$$
\\partial_t c + \\nabla\\cdot(\\mathbf u c)
= \\nabla\\cdot(\\mathbf K\\nabla c)+S,
$$

où $c$ est en kg m$^{-3}$, $\\mathbf u$ en m s$^{-1}$, $\\mathbf K$ en m$^2$ s$^{-1}$ et $S$ en kg m$^{-3}$ s$^{-1}$. Les pertes, dépôts et réactions sont exclus du premier protocole et ne doivent pas être introduits implicitement.

Pour une source impulsionnelle de masse $M$, définir explicitement la condition initiale $c(\\mathbf x,0)=M\\delta(\\mathbf x-\\mathbf x_0)$, ou une régularisation volumique documentée et convergée. La source continue constitue une expérience séparée.

Le bilan attendu sur un domaine $\\Omega$ est :

$$
\\frac{d}{dt}\\int_\\Omega c\\,dV
= -\\int_{\\partial\\Omega}(\\mathbf u c-\\mathbf K\\nabla c)\\cdot\\mathbf n\\,dA
+\\int_\\Omega S\\,dV.
$$

En domaine fermé sans flux, la masse doit rester constante. En domaine tronqué ouvert, le flux sortant doit être comptabilisé ; une masse qui quitte le domaine n'est pas une perte numérique.

## 4. Matrice des scénarios

| Scénario | Champ de vitesse | Diffusion | Rôle |
|---|---|---|---|
| S0 | $\\mathbf u=(U_0,0,0)$, $U_0>0$ | constante ou loi analytique figée dans le contrat S0 | Contrôle positif ; poursuivre #244, ne pas dupliquer |
| S1 | cisaillement $u_x(z)=U_0+\\gamma(z-z_0)$, positif sur tout le domaine ; autres composantes nulles | tenseur constant, éventuellement anisotrope mais fixé | Isoler l'effet du cisaillement |
| S2 | vent uniforme strictement positif | $K_z(z)>0$ lisse, borné et explicitement paramétré ; autres composantes fixées | Isoler l'effet d'une diffusivité variable |
| S2b | cisaillement S1 | $K_z(z)$ variable | Interaction cisaillement–diffusion, après validation séparée S1 et S2 |
| S3 | champ 2D/3D non uniforme, divergence nulle pour le premier cas, puis cas avec divergence contrôlée si pertinent | tenseur positif défini, d'abord constant | Tester courbure des trajectoires, convergence/divergence des tubes, zones stagnantes et ambiguïtés de projection |

Les paramètres doivent être sans dimension autant que possible (par exemple rapport de cisaillement $\\gamma H/U_0$ et nombre de Péclet). Éviter les champs dont la vitesse s'annule avant d'avoir défini le traitement de $1/\\lVert u\\rVert$.

## 5. Protocole numérique de référence

1. Définir domaine, géométrie, unités SI, source, conditions initiales et aux limites.
2. Définir un champ $\\mathbf u$ et un tenseur $\\mathbf K$ analytiques, échantillonnables sans ambiguïté.
3. Implémenter un schéma volumes finis conservatif ; publier les flux numériques et le traitement des frontières.
4. Vérifier le solveur sur des solutions analytiques indépendantes (advection uniforme, diffusion pure, advection-diffusion uniforme) avant S1.
5. Effectuer une étude de convergence en espace et en temps ; comparer au moins trois résolutions et documenter l'ordre observé lorsque celui-ci est théoriquement attendu.
6. Vérifier le bilan massique à chaque pas ou à des instants préenregistrés.
7. Vérifier l'indépendance de la référence : aucun appel au code, aux paramètres calculés ou à la chaîne d'évaluation du modèle candidat, hors entrées physiques communes inévitables.
8. Si possible, confronter un cas à un second solveur indépendant ou à une solution de référence publiée.

Le schéma FV n'est pas une vérité exacte par définition. La référence est une solution numérique vérifiée, avec une incertitude de discrétisation rapportée.

## 6. Traitement de $T_{\\mathrm{arr}}$ et des récepteurs hors caractéristique

Un récepteur hors de la caractéristique déterministe issue de la source n'a pas de temps d'arrivée advectif défini par cette caractéristique. La diffusion peut néanmoins lui apporter une concentration non nulle.

Il est donc interdit de remplacer mécaniquement $T_{\\mathrm{proj}}$ par $T_{\\mathrm{arr}}$ pour tous les récepteurs. Le protocole doit séparer :

- le temps d'arrivée sur la caractéristique ;
- la distance/dispersion transverse ;
- la concentration au récepteur, qui dépend de l'EDP ou d'un noyau de puff ;
- les cas où aucune caractéristique ne relie la source au récepteur.

Toute règle d'interpolation, de projection, de sélection de caractéristique ou de traitement des zones multi-valuées doit être spécifiée avant le calcul.

## 7. Méthodes candidates et comparaison puff

Comparer, sur les mêmes champs, sources, récepteurs et observables :

1. formulation projetée historique, si elle est définie dans le scénario ;
2. formulation par caractéristiques / temps d'arrivée, uniquement sur son domaine de définition ;
3. référence EDP-FV ;
4. puff gaussien actuel du package dans son domaine réel de validité ;
5. puff lagrangien sur trajectoire, seulement après définition d'une méthode d'advection, de déformation du puff et d'évolution du tenseur de covariance.

Le code actuel `jdriftx.similitude.concentration_puff` utilise les paramétrisations Briggs/Pasquill et une approximation longitudinale. Il ne doit pas être décrit comme une implémentation CALPUFF/SCIPUFF/RIMPUFF ni comme un modèle de puff advecté en champ variable sans audit de code dédié.

## 8. Observables et métriques

Observable principale du premier benchmark : concentration aérienne $c(\\mathbf x,t)$ sur une grille spatio-temporelle fixée. Pour une source impulsionnelle, rapporter aussi la masse intégrée et les moments spatiaux (centre de masse, covariance) lorsque le domaine et les frontières rendent ces quantités interprétables.

Rapporter au minimum :

- erreurs relatives et absolues $L^1$, $L^2$ et $L^\\infty$ sur une grille commune ;
- erreur sur les pics (amplitude, position et temps) ;
- erreur sur le centre de masse et la covariance du panache ;
- bilan de masse et flux aux frontières ;
- FAC2/NMSE uniquement lorsque la convention, les valeurs nulles et l'unité d'échantillonnage sont compatibles avec ces métriques ;
- coût de préparation, coût de champ/trajectoires/projection, coût par requête, coût total pour une charge $N$ déclarée et mémoire maximale.

Les points d'une même simulation ne sont pas des essais indépendants. Toute évaluation statistique sur données observées doit partitionner par essai/scénario, pas par point.

## 9. Pré-enregistrement et critères de décision

Avant de lancer les expériences, versionner :

- paramètres et plages des scénarios ;
- grilles et instants d'observation ;
- tolérances du solveur et étude de convergence ;
- métriques, seuils et règles de traitement des zéros ;
- charge de requêtes et environnement de mesure ;
- critères de succès, d'échec et d'exclusion.

Ne pas fixer ici de seuil numérique arbitraire : reprendre les seuils déjà préenregistrés dans #43 lorsqu'ils s'appliquent réellement, et créer une décision explicite avant tout nouveau benchmark S1–S3. Aucun seuil ne doit être ajusté après observation des résultats.

Verdict par scénario et observable :

- **Conserver** : erreur sous le seuil préenregistré, bilan respecté et coût total avantageux à précision comparable.
- **Restreindre** : critères satisfaits uniquement sur un sous-domaine paramétrique explicite.
- **Remplacer** : baseline puff ou autre méthode au moins aussi précise et moins coûteuse, ou échec de précision/conservation.

## 10. Baselines externes : ne pas confondre comparaison de famille et reproduction

L'état de l'art doit examiner CALPUFF, SCIPUFF, RIMPUFF et AERMOD, mais une comparaison logicielle n'est recevable qu'après fixation d'une version, d'une configuration, des entrées disponibles, de l'observable, des options physiques et des conditions d'évaluation.

- CALPUFF, SCIPUFF et RIMPUFF : modèles de dispersion à puffs, avec différences de formulation et de domaine d'application.
- AERMOD : modèle réglementaire gaussien de couche limite, pertinent comme baseline stationnaire adaptée à son domaine, pas comme substitut universel d'un modèle non stationnaire.
- AGDISP : pertinent si l'application reste la dérive de pulvérisation ; l'observable dépôt hors cible exige une physique de gouttelettes et ne peut être remplacée par la seule concentration d'un traceur passif.

Ne pas annoncer qu'un concurrent « fait déjà la même chose » sans comparer algorithme, hypothèses, entrées, observables et version. Ne pas annoncer non plus un avantage J-DriftX à partir d'une différence de vocabulaire mathématique.

## 11. Portée et non-objectifs

Ce protocole ne valide pas la dérive de pesticides, les dépôts, la volatilisation, la chimie atmosphérique, les écoulements turbulents instationnaires, ni les performances sur terrain réel. Ces sujets nécessitent des équations, données et baselines supplémentaires.

GZ-1 reste un résultat mathématique conditionnel de navigation/contrôlabilité ; il ne constitue pas une validation du puff Briggs ni de la dispersion en champ variable.

## 12. Dépendances et suivi

- [#232 — reconstruction de la baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
- [#244 — comparaison S0 à oracle indépendant et mesure des coûts](https://github.com/JM-Brun/J-DriftX/issues/244)
- [#123 — conservation et coordonnées travel-time](https://github.com/JM-Brun/J-DriftX/issues/123)
- [#211 — contre-exemple analytique de cisaillement](https://github.com/JM-Brun/J-DriftX/issues/211)
- [#448 — oracle analytique GZ-1](https://github.com/JM-Brun/J-DriftX/issues/448)
- [#43 — critères d'évaluation et seuils préenregistrés](https://github.com/JM-Brun/J-DriftX/issues/43)

Les issues S1, S2 et S3 doivent être des sous-tâches expérimentales distinctes, avec dépendances explicites. La comparaison aux logiciels externes et l'étude d'admissibilité d'une application pesticide restent séparées du benchmark synthétique.


### Issues dédiées créées le 2 novembre 2026

- [#466 — triage de la revue adversariale](https://github.com/JM-Brun/J-DriftX/issues/466)
- [#467 — S1, cisaillement vertical](https://github.com/JM-Brun/J-DriftX/issues/467)
- [#468 — S2, diffusivité variable](https://github.com/JM-Brun/J-DriftX/issues/468)
- [#469 — S3, champ 2D non uniforme](https://github.com/JM-Brun/J-DriftX/issues/469)
- [#470 — audit du puff et baselines externes](https://github.com/JM-Brun/J-DriftX/issues/470)
