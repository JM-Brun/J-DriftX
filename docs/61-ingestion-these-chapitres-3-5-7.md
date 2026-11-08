# 61 — Ingestion complémentaire de la thèse Brun : canopée, champ proche et transport lointain

**Statut :** première tranche d'ingestion transversale à partir du PDF de thèse déjà présent dans le projet. Elle complète [docs/43 — audit de conservation](43-audit-these-brun-conservation-g0s.md) sans le remplacer et ne prétend pas achever les 204 pages. Aucune acquisition de source n'a été relancée.

**Source primaire :** J.-M. Brun, *Modèles à complexité réduite de transport pour applications environnementales*, thèse de doctorat, Université Montpellier II, 2007, HAL tel-02589999. Les pages ci-dessous sont les numéros imprimés dans le manuscrit ; ils ne coïncident pas nécessairement avec la pagination PDF.

## 1. Architecture scientifique de la thèse

La thèse décrit une chaîne de modèles emboîtés :
1. théorie du transport atmosphérique et limites des modèles usuels (chap. 1) ;
2. météorologie et couche limite atmosphérique (chap. 2) ;
3. écoulement dans la canopée, notamment comme milieu poreux (chap. 3) ;
4. modèle réduit de champ dans la canopée (chap. 4) ;
5. jets turbulents et estimation de la dérive en champ proche (chap. 5) ;
6. échelles et familles de modèles de dispersion (chap. 6) ;
7. transport lointain par similitude généralisée dans une géométrie non symétrique fondée sur les temps de migration (chap. 7).

La dépendance centrale est **canopée/écoulement → émission et transport local → quantité candidate au transport lointain → champ atmosphérique et temps de migration → profil de similitude**. L'introduction du chapitre 7 (pp. imprimées 124–125) explicite cette dépendance entre niveaux.

## 2. Chapitre 3 — Canopée et écoulement

### 2.1 Phénomènes et choix de modèle

Le chapitre 3 souligne que la végétation est constituée d'éléments discrets et irréguliers (feuilles, tiges, branches) dont la représentation 3D explicite est impraticable pour l'objectif visé. La canopée agit par absorption de quantité de mouvement via la traînée, échanges de scalaires, transport vertical et génération de sillages turbulents.

Le chapitre distingue plusieurs approches qui ne doivent pas être amalgamées : diffusion locale, paramétrisation de rugosité, approche poreuse et moyennisation spatiale/volumique.

### 2.2 Équations et unités relevées

- Éq. (3.1)–(3.3), p. 50 : force de traînée et coefficient (C_D), avec unités explicites de force, masse volumique et surface de référence.
- Éq. (3.11), p. 52 : densité surfacique foliaire (a_{LAD}(x,y,z)), de dimension (L^{-1}). Le texte avertit que la substitution par l'indice surfacique (a_{LAI}), sans dimension, peut rendre les unités incohérentes dans les lois de traînée.
- Éq. (3.12), p. 52 : fermeture diffusive locale (Q_S=-\rho K_S\,\partial s/\partial z). La thèse rappelle que les hypothèses de cette approche sont contestées.
- Éq. (3.16)–(3.19), pp. 54–55 : formulation poreuse, perte de pression et traînée volumique. La relation (3.19) est donnée pour des nombres de Reynolds élevés, lorsque le terme inertiel quadratique domine.
- Éq. (3.20), p. 55 : équation de Navier–Stokes servant de point de départ à la moyennisation.
- Éq. (3.21)–(3.23), pp. 56–57 : conservation de masse, quantité de mouvement et transport d'une propriété passive dans la couche de rugosité, avec contraintes de Reynolds et flux turbulent.

### 2.3 Hypothèses de moyennisation

La méthode de moyennisation volumique est présentée sous quatre hypothèses explicites : (i) homogénéité macroscopique du milieu, (ii) matrice solide rigide, (iii) absence de réaction chimique entre matrice et fluide, (iv) conditions isothermes. La moyenne horizontale suppose également une canopée suffisamment homogène sur la région moyennée (espacements, hauteurs et densité foliaire approximativement constants).

Le texte souligne que la moyenne spatiale fait apparaître des flux dispersifs, analogues spatiaux des contraintes de Reynolds. Ils ne doivent pas être omis dans une synthèse de la fermeture.

**Limite :** les équations (3.21)–(3.23) sont relevées, mais la dérivation complète des termes de fermeture après moyennisation et leur correspondance avec le code restent à auditer. Le chapitre 3 n'est donc pas encore une spécification complète du module de canopée.

## 3. Chapitres 4–5 — Champ proche et terme source

### 3.1 Rôle du chapitre 4

Le chapitre 4 est intitulé *DriftX Module 1: Canopy Flow Model*. Il décrit un modèle à complexité réduite obtenu par réduction dimensionnelle des équations de Navier–Stokes et de transport, visant le champ de vitesse, la distribution des quantités pulvérisées dans la canopée et la quantité capturée par le feuillage. Le chapitre 3 en constitue le socle physique.

Le modèle local ne se réduit donc pas à un profil gaussien : il représente l'interaction entre écoulement, structure végétale et transport/dépôt dans la parcelle.

### 3.2 Chapitre 5 — jets turbulents et application viticole

Le chapitre 5 utilise un jet turbulent rond axisymétrique comme modèle simplifié de l'émission par une buse, puis l'applique au pulvérisateur dans une rangée de vigne assimilée à un milieu poreux homogène. Les paramètres cités comprennent notamment (a_{LAD}), (C_D) et les paramètres de perte/efficacité du filet de canopée.

La section 5.6.1 (p. 97) applique l'équation du jet à une buse et ajoute le comportement dans le rang de vigne. La section 5.6.3 (pp. 101–102) attribue à la concentration locale (c_{loc}) l'unité kg·m⁻³ et au coefficient de calibration associé l'unité s⁻¹. Ces unités sont déjà mobilisées dans [docs/43](43-audit-these-brun-conservation-g0s.md) pour l'audit de (7.12).

Les sections expérimentales 5.7.1–5.7.2 (pp. 104–105) décrivent les conditions microclimatiques et l'estimation du flux de pulvérisation par des lignes collectrices installées dans un plan horizontal à 2,5 m du sol. Le liquide contient un traceur fluorescent BSF ; le volume capturé est estimé par fluorométrie, puis converti en flux spécifique et en quantité traversant le plan.

La discussion 5.8.3 (p. 107) énumère des simplifications : certains effets du vent et des oscillations de canopée, interactions de jets, spectre de gouttelettes (gravité et traînée), densité, température et évaporation ne sont pas pris en compte ; vitesse d'avancement et vent dans les rangs sont considérés constants et supposés ne pas modifier la vitesse d'éjection. La thèse souligne qu'un modèle plus complexe n'est pas nécessairement plus prédictif si les entrées sont incertaines.

**Résultats rapportés, limités au dispositif étudié :** autour de la figure 5.12, la simulation estime environ 30 % de capture par le feuillage et environ 12 % de la masse pulvérisée perdue sous forme de dérive. Ces valeurs ne sont pas des constantes universelles ni une validation générale.

## 4. Chapitre 7 — transport lointain

### 4.1 Séparation des échelles

Le chapitre 7 (pp. 124–125) pose une séparation d'échelles : près de la buse, le mouvement des gouttelettes dépend du pulvérisateur ; suffisamment loin, il est supposé dominé par les conditions météorologiques. La concentration est alors considérée assez faible pour que l'influence des gouttelettes sur la turbulence atmosphérique soit négligeable.

La figure 7.2 précise que le champ local instantané sert à déterminer la part du polluant quittant la couche proche du sol ; il n'est pas supposé modifier la circulation atmosphérique globale. L'état transmis au niveau lointain est une quantité candidate au transport, pas l'intégralité de l'état local.

### 4.2 Champ de vent et topographie

- Éq. (7.8)–(7.9), p. 127 : construction du champ proche du sol à partir d'observations, sous forme de potentiel (ec u=\nabla\phi) et d'un problème de Poisson ajustant le potentiel aux vitesses observées ((n_{obs}) points).
- Éq. (7.10), p. 127 : complétion verticale par des fonctions de paroi généralisées ; la direction tangentielle au sol est définie à partir du champ horizontal. Le texte suppose une composante normale nulle au sol et déduit la troisième composante via la divergence nulle et sa valeur au sol.
- Éq. (7.11), p. 128 : correction des temps de migration liée à la topographie, par une fonction positive monotone décroissante valant 1 pour une pente nulle ; la variable (phi_{topo}) dépend du gradient du terrain et du champ horizontal construit.

La thèse reconnaît que les observations météo sont très clairsemées et que la complétion du champ/topographie est une approximation adaptée au niveau de précision visé, non une reconstruction CFD détaillée.

### 4.3 Condition d'entrée et conservation

Les équations (7.12)–(7.13), p. 129, sont le périmètre propriétaire de [docs/43](43-audit-these-brun-conservation-g0s.md) et de l'issue [#123](https://github.com/JM-Brun/J-DriftX). Cette note n'en duplique pas l'analyse dimensionnelle.

La lecture distingue (a) la quantité locale candidate au transport lointain (c^+(x,y)), définie selon l'une des deux alternatives imprimées, et (b) l'inventaire (M_C=\int_{\mathbb R^2}c^+\,d\sigma), que la thèse indique devoir être conservé. La revendication est explicite mais sa démonstration ne l'est pas dans ce passage. L'ambiguïté dimensionnelle reste documentée dans docs/43. La reconstruction J-DriftX retient un inventaire de masse par intégration verticale, sans prétendre avoir établi l'intention historique.

### 4.4 Profil de similitude et géométrie dirigée

Les équations (7.14)–(7.15), pp. 129–130, donnent pour un écoulement plan uniforme :
[
c_{glob}(x,y,z)=c_{axis}(x)f_{rad}(r,\delta(x)),\qquad r=\sqrt{y^2+z^2},
]
avec décroissance axiale exponentielle et profil radial exponentiel. (delta(x)) caractérise l'épaisseur du panache ; le texte indique une évolution parabolique pour un jet laminaire et linéaire dans les cas turbulents considérés. (a(U)) est positif et monotone décroissant ; (b(U,\delta)) est positif, croissant en (U) et décroissant en (delta).

La généralisation proposée remplace la distance cartésienne par une géométrie non symétrique fondée sur les temps de migration. Les équations (7.6)–(7.7), p. 127, définissent le temps le long d'une caractéristique issue de A jusqu'à la projection (B^\perp) de B. La caractéristique est supposée unique ; sources et points d'attraction sont écartés. Si la projection n'est pas unique, le texte propose un choix satisfaisant au mieux une contrainte de transport au point B.

La construction des caractéristiques est ensuite approchée par des polynômes satisfaisant des conditions aux extrémités et sur les dérivées, équations (7.16)–(7.19), p. 130. Le passage retrouvé indique que l'ordre polynomial est augmenté lorsque la dérivée de la courbe candidate ne correspond pas au champ local. Cette prescription est un algorithme approché ; elle ne démontre ni existence, ni unicité, ni convergence de la caractéristique.

### 4.5 Propriétés annoncées et statut

Le chapitre 7 énonce que les solutions doivent satisfaire la divergence nulle du vent, la conservation, la positivité et la linéarité. Ce sont des objectifs/contraintes de construction déclarés par l'auteur. Pour la conservation, docs/43 et #123 montrent qu'une preuve exige de préciser la grandeur, la transformation, le jacobien, les sources/puits et les frontières ; elle ne découle pas de la seule condition (
abla\cdot\vec u=0).

## 5. Résultats et figures du chapitre 7

La liste des figures (pp. 191–192) identifie :
- fig. 7.3 : transport dans un repère euclidien sous vent uniforme stationnaire ;
- fig. 7.4 : solution dans la géométrie généralisée fondée sur les temps de transport ;
- fig. 7.5 : comparaison avec une simulation EDP éléments finis transport–diffusion–dépôt pour le même champ interpolé ; la quantité transportée est indiquée en kg ;
- fig. 7.6 : trajectoire du véhicule et champ construit à partir de deux mesures de vent ;
- fig. 7.7 : comparaison des distances euclidienne et non symétrique ;
- fig. 7.8 : configuration à deux sources ;
- fig. 7.9 : effet de la topographie ;
- fig. 7.10 : champ construit, dispersion et sensibilité pour rechercher des origines possibles d'une pollution.

La comparaison de la fig. 7.5 est un résultat de cas numérique, pas une preuve générale d'équivalence à l'EDP. La fig. 7.10 illustre une analyse de sensibilité/inversion dans la configuration étudiée, pas une garantie générale d'identifiabilité.

## 6. Articulation avec les sources de vérité existantes

- [docs/43 — audit de conservation de la thèse](43-audit-these-brun-conservation-g0s.md) : propriétaire de l'analyse dimensionnelle de (7.12), (M_C) et des limites de conservation.
- [docs/45 — audit de l'article de 2006](45-audit-article-mohammadi-brun-2006.md) : antécédent de la similitude généralisée et de la pseudo-distance orientée.
- [docs/49 — matrice des revendications historiques](49-matrice-revendications-baseline.md) : statuts de définition et de reproductibilité.
- [docs/55 — relevé du manuscrit 2009](55-releve-equations-manuscrit-2009-comparaison-jesa.md) : source distincte pour SIG, topographie et multi-niveaux.
- [#123 — conservation en coordonnées travel-time](https://github.com/JM-Brun/J-DriftX/issues/123) : question mathématique propriétaire.
- [#232 — baseline historique](https://github.com/JM-Brun/J-DriftX/issues/232) : programme de reconstruction/qualification des capacités.

## 7. Travail restant pour achever l'ingestion

1. **Chapitre 4 :** relever le modèle de canopée, variables d'état, équations réduites, conditions aux limites, paramètres et couplage au chapitre 3 ; confronter au code historique sans présumer une correspondance.
2. **Chapitre 5 :** relever systématiquement les équations du jet et hypothèses de similitude (notamment autour de (5.16), (5.33)–(5.42)), puis les confronter aux unités et aux données expérimentales 5.6–5.8.
3. **Chapitre 7 :** poursuivre après (7.19), notamment évaluation du temps de migration, construction effective de la géométrie, assimilation/calibration et exemples ; contrôler les symboles ambigus sur le fac-similé.
4. **Annexes E et F :** qualifier les conditions météorologiques de l'exemple et la formulation Finsler/métrique de vent ; distinguer cette annexe de la construction réellement utilisée au chapitre 7.
5. **Provenance :** consulter la fiche existante du PDF versionné et consigner le contrôle d'identité binaire avec la copie HAL déjà obtenue, sans réacquisition. Vérifier les droits séparément.

### Critère de clôture

Chaque bloc doit disposer d'une fiche avec pages imprimées/PDF, équations transcrites depuis le fac-similé, variables/unités, hypothèses, domaine, conditions initiales/aux limites, sources/puits, résultats, limites, reproductibilité et liens vers les anomalies/implémentations propriétaires. L'OCR seul ne certifie pas une équation.

**Conclusion :** la thèse documente une chaîne physique plus riche que le seul modèle lointain : interaction canopée–écoulement, estimation expérimentale de l'émission, puis transport lointain réduit. Les chapitres 3 et 5 sont nécessaires pour comprendre le sens physique et les unités de l'entrée du chapitre 7. La conservation revendiquée au chapitre 7 reste non démontrée dans le texte examiné et demeure instruite par #123.
