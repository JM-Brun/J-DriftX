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

- Éq. (3.1)–(3.3), p. 50 : force de traînée et coefficient $C_D$, avec unités explicites de force, masse volumique et surface de référence.
- Éq. (3.11), p. 52 : densité surfacique foliaire (a_{LAD}(x,y,z)), de dimension (L^{-1}). Le texte avertit que la substitution par l'indice surfacique $a_{LAI}$, sans dimension, peut rendre les unités incohérentes dans les lois de traînée.
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

### 3.1.1 Équations réduites et problème inverse

À l'échelle du rang, l'équation (4.1), p. imprimée 63, représente la traînée végétale :
\[
F_{Dveg}=\frac12\rho\,a_{LAD}\,u^2 C_{Dveg}.
\]
La thèse indique pour \(C_{Dveg}\) une plage bibliographique de 0,1 à 0,5 et souligne que sa détermination est expérimentale. Elle définit \(a_{LAD}\) comme densité foliaire, de dimension \(L^{-1}\).

**Incohérence dimensionnelle relevée sur le fac-similé :** l'équation (4.1) imprime l'unité \([N]\). Avec \([\rho]=\mathrm{kg\,m^{-3}}\), \([a_{LAD}]=\mathrm{m^{-1}}\), \([u]=\mathrm{m\,s^{-1}}\) et \(C_{Dveg}\) sans dimension, le membre droit est en \(\mathrm{kg\,m^{-2}\,s^{-2}}=\mathrm{N\,m^{-3}}\), soit une force par unité de volume. L'étiquette \([N]\) ne correspond donc pas à ces définitions. Le chapitre 3, équation (3.4), p. 51 (PDF p. 60), définit explicitement \(F_D\) comme la force totale de traînée par unité de volume et imprime \(N\,m^{-3}\). La cohérence dimensionnelle et cette définition antérieure indiquent donc que \(F_{Dveg}\) est également une force volumique ; l'étiquette \([N]\) de (4.1) est très probablement une coquille d'unité, et non une force totale à intégrer. L'anomalie est consignée sous **DRX-ERR-021** dans le registre [docs/46](46-registre-erreurs-incoherences-documentaires.md) ; aucune correction de l'équation source n'est imposée. Le fac-similé a été contrôlé visuellement (PDF p. 72, pagination imprimée p. 63).

Le chapitre réduit ensuite l'écoulement dans le rang à une variable de pénétration \(r\). L'équation de vitesse (4.8), p. imprimée 66, est une équation de Burgers visqueuse forcée :
\[
\frac{\partial u}{\partial t}
+\frac12\frac{\partial (u^2)}{\partial r}
-\nu\frac{\partial^2u}{\partial r^2}
=F_u(u,r,t),
\qquad (r,t)\in [r_0,r_1]\times[0,T].
\]
Les conditions imprimées sont \(u(r,0)=u_0(r)=0\) sur \([r_0,r_1]\) et \(u(r_0,t)=u_l(t)=u_l\) sur \([0,T]\). Le texte identifie \(F_u\) comme le terme puits de quantité de mouvement dû à la traînée de la canopée.

L'équation scalaire (4.9), p. 67, est :
\[
\frac{\partial c}{\partial t}
+u(r,t)\frac{\partial c}{\partial r}
-D\frac{\partial^2c}{\partial r^2}
=F_c(u,c,r,t),
\]
avec \(c(r,0)=c_0(r)=c_0\) et \(c(r_0,t)=c_l(t)=c_l\). Le texte interprète \(F_c\) comme le terme puits représentant l'effet de perte de masse dû à la canopée.

**Condition aux limites incomplète dans la spécification imprimée :** pour les équations (4.8) et (4.9), le domaine est borné en \(r\) et les termes \(\nu u_{rr}\) et \(D c_{rr}\) sont d'ordre deux, mais seule la condition au bord \(r_0\) est donnée ; aucune condition en \(r_1\) n'est indiquée à ces équations. La valeur cible \(u_{tar}(r_1)\) de (4.18) décrit un profil cible et ne suffit pas, à elle seule, à établir une condition de bord pour l'état. L'annexe C, équation (C.3), répète l'unique condition à \(r_0\) sans ajouter de condition à \(r_1\). La spécification est donc sous-déterminée telle qu'imprimée pour un problème parabolique sur \([r_0,r_1]\) ; une condition naturelle ou une convention d'outflow peut avoir été implicite, mais elle n'est pas documentée dans ces passages. Voir **DRX-ERR-022** dans docs/46.

L'annexe C apporte une seconde réserve de reproductibilité : (C.1) inclut la viscosité physique \(\nu u_{rr}\), tandis que les formes (C.2) et (C.4) l'omettent ; le schéma explicite (C.9) réintroduit \(\nu\), alors que le schéma JST (C.20) utilise une viscosité numérique \(\mu_j^{n,p}\) définie en (C.22), sans expliquer si elle remplace ou complète \(\nu\). Ces formulations ne doivent pas être assimilées sans reconstituer précisément la branche numérique effectivement utilisée.

Le problème inverse cherche le terme de contrôle/puits \(F\) qui rapproche l'état \(u_F\) d'un profil cible. Les équations (4.14) et (4.16), p. imprimée 68, présentent deux critères :
\[
J_{LC}(F)=\sum_{i=1}^{n}\alpha^{(i)}
\left\|u_F-u_{tar}^{(i)}\right\|_{L_2},
\qquad
J_{WCE}(F)=\max_i\left\{
\alpha^{(i)}\left\|u_F-u_{tar}^{(i)}\right\|_{L_2}
\right\}.
\]
Le premier minimise une somme pondérée des erreurs (coût moyen) ; le second minimise la pire erreur pondérée (minimax). Le texte les présente comme formulations multi-critères complémentaires pour la robustesse, mais précise que l'application simple de paramétrage qui suit n'emploie pas encore l'approche multi-critères.

Le profil cible (4.17)–(4.18), p. 68, est exponentiel entre les vitesses d'entrée et de sortie du rang, avec \(u_r^{(i)}=\beta_{veg}u_l^{(i)}\) et \(\beta_{veg}\in[0,1]\). Le contrôle est ensuite discrétisé par morceaux sur \(m\) sous-intervalles, équations (4.20)–(4.24), sous la forme de valeurs constantes du produit \(a_{LAD}C_{Dveg}\), de dimension \(m^{-1}\). La figure 4.2 compare les profils cibles et optimisés ; la figure 4.3 rapporte les paramètres optimaux correspondants. Il s'agit d'une identification de paramétrisation à partir de profils cibles, pas d'une estimation indépendante de \(a_{LAD}\) et \(C_{Dveg}\) séparément.

### 3.2 Chapitre 5 — jets turbulents et application viticole

Le chapitre 5 utilise un jet turbulent rond axisymétrique comme modèle simplifié de l'émission par une buse, puis l'applique au pulvérisateur dans une rangée de vigne assimilée à un milieu poreux homogène. Les paramètres cités comprennent notamment $a_{LAD}$, $C_D$ et les paramètres de perte/efficacité du filet de canopée.

### 3.2.1 Similitude du jet et profil de concentration

Les équations (5.32)–(5.40), pp. imprimées 94–95, partent de l'équation de transport moyennée du scalaire dans un jet axisymétrique turbulent. La diffusion moléculaire est négligée à grand nombre de Reynolds. Le profil de concentration est posé sous forme auto-similaire, avec une échelle de concentration axiale, une échelle de fluctuation turbulente et une coordonnée radiale réduite. La conservation du flux de concentration (5.37) impose que l'échelle radiale de concentration soit prise égale à celle du jet ; elle implique aussi que le produit de la concentration d'axe par la largeur du jet soit constant. Les relations (5.38)–(5.40) relient ensuite le profil moyen et le flux turbulent.

La thèse discute explicitement la non-universalité possible du jet : l'hypothèse \(u_L^x=U_{turb}\) conduirait à une vitesse d'étalement universelle, mais cette hypothèse est contestée dans la littérature citée. Les conditions initiales de la buse peuvent donc affecter les paramètres de similitude. Il ne faut pas transformer la famille de profils en loi universelle indépendante de la buse.

Les équations (5.44)–(5.45), p. imprimée 101 (PDF p. 110), donnent la concentration tridimensionnelle d'un jet :
\[
c_{jet}(x,r,\theta)=c_{centerline}(x)f_{rad}\!\left(\frac{r}{x}\right),
\qquad
f_{rad}\!\left(\frac{r}{x}\right)
=\exp\!\left[-\alpha_{Jet}\left(\frac{r}{x}\right)^2\right].
\]
Le profil radial est gaussien, tandis que le comportement axial est modifié dans la canopée. La thèse suppose que la canopée modifie le profil axial mais pas le profil radial, à l'intérieur comme à l'extérieur du rang ; elle qualifie explicitement cette hypothèse de forte et demande une vérification expérimentale. La figure 5.8 montre une sensibilité du profil axial à \(a_{LAD}\).

### 3.2.2 Du champ local à la masse candidate au transport lointain

Les équations (5.50)–(5.55), p. imprimée 102, normalisent la forme spatiale du flux de concentration de chaque buse par son intégrale volumique, puis la multiplient par le débit massique de la buse \(Q_0^i\). Le coefficient de calibration \(coef\,f^i\) a l'unité \(s^{-1}\). La concentration locale cumulée est mise à jour par (5.56)–(5.60) en sommant, sur les buses, les contributions de taux \(c_{\Delta t^j}^i\) multipliées par le pas de temps. La concentration \(c_{loc}\) est en \(\mathrm{kg\,m^{-3}}\), tandis que le taux de contribution est en \(\mathrm{kg\,m^{-3}\,s^{-1}}\).

Les équations (5.61)–(5.63), p. 102, calculent les pertes par intégration de \(c_{loc}\) au-dessus de la hauteur \(z_0\), puis sur l'espace et à la fin du traitement \(T_{spray}\). La thèse identifie explicitement cette masse comme le terme source du niveau 3 de DriftX, c'est-à-dire du modèle de dispersion atmosphérique à méso-échelle.

Les équations (5.64)–(5.67), p. 103, présentent une formulation par flux vertical à travers le plan horizontal \(x-y\) juste au-dessus de \(z_0\) :
\[
M_{loss}(\Delta t^j)
=\int_{\Delta t^j}\!\int_S(wc_{loc})\,dS\,dt.
\]
Sous l'hypothèse que le pulvérisateur et l'écoulement sont stationnaires pendant l'intervalle considéré, (5.65)–(5.67) relient ce flux à l'intégrale volumique des contributions des buses. La dernière relation (5.67) est imprimée avec le signe approximatif \(\approx\), et doit rester une relation approchée, non une identité générale. Les hypothèses invoquées sont la stationnarité sur \(\Delta t^j\), la localisation spatiale de la source et la représentation par le champ \(c_{loc}\).

L'implémentation historique décrite en 5.6.3 est en FORTRAN77 ; chaque buse produit un jet turbulent indépendant selon (5.44), sans interaction entre jets, et le domaine est discrétisé sur une grille uniforme prescrite par l'utilisateur. Cette hypothèse d'indépendance est une limite explicite du modèle.

La section 5.6.1 (p. 97) applique l'équation du jet à une buse et ajoute le comportement dans le rang de vigne. La section 5.6.3 (pp. 101–102) attribue à la concentration locale $c_{loc}$ l'unité kg·m⁻³ et au coefficient de calibration associé l'unité s⁻¹. Ces unités sont déjà mobilisées dans [docs/43](43-audit-these-brun-conservation-g0s.md) pour l'audit de (7.12).

Les sections expérimentales 5.7.1–5.7.2 (pp. 104–105) décrivent les conditions microclimatiques et l'estimation du flux de pulvérisation par des lignes collectrices installées dans un plan horizontal à 2,5 m du sol. Le liquide contient un traceur fluorescent BSF ; le volume capturé est estimé par fluorométrie, puis converti en flux spécifique et en quantité traversant le plan.

La discussion 5.8.3 (p. 107) énumère des simplifications : certains effets du vent et des oscillations de canopée, interactions de jets, spectre de gouttelettes (gravité et traînée), densité, température et évaporation ne sont pas pris en compte ; vitesse d'avancement et vent dans les rangs sont considérés constants et supposés ne pas modifier la vitesse d'éjection. La thèse souligne qu'un modèle plus complexe n'est pas nécessairement plus prédictif si les entrées sont incertaines.

**Résultats rapportés, limités au dispositif étudié :** autour de la figure 5.12, la simulation estime environ 30 % de capture par le feuillage et environ 12 % de la masse pulvérisée perdue sous forme de dérive. Ces valeurs ne sont pas des constantes universelles ni une validation générale.

## 4. Chapitre 7 — transport lointain

### 4.1 Séparation des échelles

Le chapitre 7 (pp. 124–125) pose une séparation d'échelles : près de la buse, le mouvement des gouttelettes dépend du pulvérisateur ; suffisamment loin, il est supposé dominé par les conditions météorologiques. La concentration est alors considérée assez faible pour que l'influence des gouttelettes sur la turbulence atmosphérique soit négligeable.

La figure 7.2 précise que le champ local instantané sert à déterminer la part du polluant quittant la couche proche du sol ; il n'est pas supposé modifier la circulation atmosphérique globale. L'état transmis au niveau lointain est une quantité candidate au transport, pas l'intégralité de l'état local.

### 4.2 Champ de vent et topographie

- Éq. (7.8)–(7.9), p. 127 : construction du champ proche du sol à partir d'observations, sous forme de potentiel ($\vec{u}=\nabla\phi$) et d'un problème de Poisson ajustant le potentiel aux vitesses observées $n_{obs}$ points.
- Éq. (7.10), p. 127 : complétion verticale par des fonctions de paroi généralisées ; la direction tangentielle au sol est définie à partir du champ horizontal. Le texte suppose une composante normale nulle au sol et déduit la troisième composante via la divergence nulle et sa valeur au sol.
- Éq. (7.11), p. 128 : correction des temps de migration liée à la topographie, par une fonction positive monotone décroissante valant 1 pour une pente nulle ; la variable $\phi_{topo}$ dépend du gradient du terrain et du champ horizontal construit.

La thèse reconnaît que les observations météo sont très clairsemées et que la complétion du champ/topographie est une approximation adaptée au niveau de précision visé, non une reconstruction CFD détaillée.

### 4.3 Condition d'entrée et conservation

Les équations (7.12)–(7.13), p. 129, sont le périmètre propriétaire de [docs/43](43-audit-these-brun-conservation-g0s.md) et de l'issue [#123](https://github.com/JM-Brun/J-DriftX). Cette note n'en duplique pas l'analyse dimensionnelle.

La lecture distingue (a) la quantité locale candidate au transport lointain (c^+(x,y)), définie selon l'une des deux alternatives imprimées, et (b) l'inventaire $M_C=\int_{\mathbb R^2}c^+\,d\sigma$, que la thèse indique devoir être conservé. La revendication est explicite mais sa démonstration ne l'est pas dans ce passage. L'ambiguïté dimensionnelle reste documentée dans docs/43. La reconstruction J-DriftX retient un inventaire de masse par intégration verticale, sans prétendre avoir établi l'intention historique.

### 4.4 Profil de similitude et géométrie dirigée

Les équations (7.14)–(7.15), pp. 129–130, donnent pour un écoulement plan uniforme :
\[
c_{glob}(x,y,z)=c_{axis}(x)f_{rad}(r,\delta(x)),\qquad r=\sqrt{y^2+z^2}
\]
avec décroissance axiale exponentielle et profil radial exponentiel. $\delta(x)$ caractérise l'épaisseur du panache ; le texte indique une évolution parabolique pour un jet laminaire et linéaire dans les cas turbulents considérés. $a(U)$ est positif et monotone décroissant ; $b(U,\delta)$ est positif, croissant en $U$ et décroissant en $\delta$.

La généralisation proposée remplace la distance cartésienne par une géométrie non symétrique fondée sur les temps de migration. Les équations (7.6)–(7.7), p. 127, définissent le temps le long d'une caractéristique issue de A jusqu'à la projection (B^\perp) de B. La caractéristique est supposée unique ; sources et points d'attraction sont écartés. Si la projection n'est pas unique, le texte propose un choix satisfaisant au mieux une contrainte de transport au point B.

La construction des caractéristiques est ensuite approchée par des polynômes satisfaisant des conditions aux extrémités et sur les dérivées, équations (7.16)–(7.19), p. 130. Le passage retrouvé indique que l'ordre polynomial est augmenté lorsque la dérivée de la courbe candidate ne correspond pas au champ local. Cette prescription est un algorithme approché ; elle ne démontre ni existence, ni unicité, ni convergence de la caractéristique.

### 4.5 Propriétés annoncées et statut

Le chapitre 7 énonce que les solutions doivent satisfaire la divergence nulle du vent, la conservation, la positivité et la linéarité. Ce sont des objectifs/contraintes de construction déclarés par l'auteur. Pour la conservation, docs/43 et #123 montrent qu'une preuve exige de préciser la grandeur, la transformation, le jacobien, les sources/puits et les frontières ; elle ne découle pas de la seule condition $\nabla\cdot\vec u=0$.

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
