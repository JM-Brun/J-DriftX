# Modèles lagrangiens, turbulence et jeux de validation

> Fiche de synthèse documentaire créée le 2 novembre 2026. Elle distingue les articles scientifiques, les documentations de modèles et les catalogues de données. Les sources ont été contrôlées au niveau des notices éditeur ou institutionnelles et des résumés accessibles ; cela ne signifie pas que tous les textes intégraux ou fichiers expérimentaux ont été téléchargés et audités.

## 1. Modèles de dispersion à comparer

### HYSPLIT — transport lagrangien et dispersion

Stein et al. (2015), *NOAA’s HYSPLIT Atmospheric Transport and Dispersion Modeling System*, **Bulletin of the American Meteorological Society**, 96(12), 2059–2077. DOI [10.1175/BAMS-D-14-00110.1](https://doi.org/10.1175/BAMS-D-14-00110.1).

HYSPLIT est développé par le NOAA Air Resources Laboratory. Il couvre le calcul de trajectoires avant/arrière, la dispersion de particules tridimensionnelles et le fractionnement en puffs, ainsi que des processus de mélange, transformation et dépôt. La documentation NOAA constitue la référence logicielle institutionnelle ; l'article de Stein et al. est la référence de description générale.

**Rapport à J-DriftX :** baseline lagrangienne de premier plan pour comparer le transport sur champs météorologiques variables. Elle permet de formuler une comparaison entre représentation particulaire / puff et temps de transport dirigé. Les différences observées doivent être décomposées entre formulation de transport, turbulence, résolution et champs météorologiques.

### UK-ADMS — modèle gaussien avancé

Carruthers et al. (1994), *UK-ADMS: A new approach to modelling dispersion in the earth's atmospheric boundary layer*, **Journal of Wind Engineering and Industrial Aerodynamics**, 52, 139–153. DOI [10.1016/0167-6105(94)90044-2](https://doi.org/10.1016/0167-6105(94)90044-2).

L'article décrit un système modulaire pour des émissions gazeuses ou particulaires, de durée quelconque, et documente notamment la surélévation du panache, le dépôt sec et humide, la décroissance radioactive, les terrains vallonnés et rugosités variables, les zones côtières, les grands bâtiments ainsi que les fluctuations de concentration à des échelles inférieures à l'heure.

**Rapport à J-DriftX :** comparateur de la famille gaussienne avancée. Il permet de vérifier que les capacités annoncées pour J-DriftX ne sont pas déjà couvertes par un modèle opérationnel plus complet. Ce n'est pas un comparateur direct dans tous les régimes : le protocole doit contrôler les hypothèses et observables.

### GRAL — écoulement microscopique et particules lagrangiennes

Öttl (2015), *Quality assurance of the prognostic, microscale wind-field model GRAL 14.8 using wind-tunnel data provided by the German VDI guideline 3783-9*, **Journal of Wind Engineering and Industrial Aerodynamics**, 142, 104–110. DOI [10.1016/j.jweia.2015.03.014](https://doi.org/10.1016/j.jweia.2015.03.014).

L'étude porte sur la validation en soufflerie du champ d'écoulement microscopique associé à GRAL. L'article décrit un champ calculé par RANS avec fermeture k–ε, couplé au modèle lagrangien de particules.

**Rapport à J-DriftX :** comparateur pour les écoulements microscopiques, obstacles et environnements complexes. Sa chaîne de calcul comprend une modélisation du champ de vent qui dépasse le périmètre du noyau J-DriftX actuel ; l'utiliser comme baseline n'a de sens que si le champ d'entrée et le scénario sont comparables.

### PyAERMOD, AERMOD, FLEXPART et OpenDrift : distinguer les niveaux

Les références ajoutées dans la présente PR complètent les entrées FLEXPART v11, OpenDrift v1.0, PyAERMOD 2.2.0 et la documentation EPA AERMOD déjà introduites dans cette branche.

- **FLEXPART** : modèle lagrangien particulaire de dispersion atmosphérique ; Bakels et al. (2024) décrivent la version 11.
- **OpenDrift** : framework générique de modélisation de trajectoires ; Dagestad et al. (2018). Sa généricité et ses cas d'usage ne le rendent pas automatiquement équivalent à un modèle de concentration atmosphérique.
- **PyAERMOD** : wrapper Python / distribution logicielle pour AERMOD ; Capps (2026). Il facilite l'accès programmatique mais ne constitue pas une formulation physique indépendante d'AERMOD.
- **AERMOD / EPA** : modèle réglementaire et documentation de référence EPA. Distinguer le modèle lui-même, ses documents réglementaires et les wrappers logiciels.

## 2. Fondements des modèles stochastiques lagrangiens

### Thomson (1987) — critère de cohérence

Thomson, D. J. (1987), *Criteria for the selection of stochastic models of particle trajectories in turbulent flows*, **Journal of Fluid Mechanics**, 180, 529–556. DOI [10.1017/S0022112087001940](https://doi.org/10.1017/S0022112087001940).

L'article examine les critères de sélection des modèles stochastiques de trajectoires dans des écoulements turbulents inhomogènes ou instationnaires, et leur relation avec la condition dite *well-mixed*.

**Rapport à J-DriftX :** référence théorique majeure pour distinguer trajectoire moyenne, dispersion turbulente et modèle stochastique de particules. Elle doit servir à préciser les limites d'une représentation déterministe fondée sur un temps de transport, pas à postuler une équivalence entre métrique dirigée et diffusion turbulente.

### Luhar & Britter (1989) — turbulence convective inhomogène

Luhar, A. K. & Britter, R. E. (1989), *A random walk model for dispersion in inhomogeneous turbulence in a convective boundary layer*, **Atmospheric Environment**, 23(9), 1911–1924. DOI [10.1016/0004-6981(89)90516-7](https://doi.org/10.1016/0004-6981(89)90516-7).

L'étude construit un modèle de marche aléatoire pour une couche limite convective inhomogène et dissymétrique, en lien avec l'approche de Thomson et la condition *well-mixed*.

**Rapport à J-DriftX :** utile pour délimiter le régime dans lequel une description déterministe simplifiée pourrait être acceptable et les effets turbulents qu'elle ne représente pas.

### Holmes & Morawska (2006) — revue des familles de modèles

Holmes, N. S. & Morawska, L. (2006), *A review of dispersion modelling and its application to the dispersion of particles: An overview of different dispersion models available*, **Atmospheric Environment**, 40(30), 5902–5928. DOI [10.1016/j.atmosenv.2006.06.003](https://doi.org/10.1016/j.atmosenv.2006.06.003).

Revue des modèles de dispersion de particules et de leurs domaines d'application, qui distingue notamment modèles boîte, gaussiens, lagrangiens/eulériens, CFD et modèles incluant la dynamique des aérosols.

**Rapport à J-DriftX :** source de cadrage taxonomique, non benchmark ni preuve de performance actuelle des logiciels cités.

## 3. Comparaisons inter-modèles sur traceurs contrôlés

### Andrews et al. (2013) — HYSPLIT, STILT et FLEXPART

Andrews et al. (2013), *Evaluation of Lagrangian Particle Dispersion Models with Measurements from Controlled Tracer Releases*, **Journal of Applied Meteorology and Climatology**, 52, 2623–2637. DOI [10.1175/JAMC-D-13-0125.1](https://doi.org/10.1175/JAMC-D-13-0125.1).

HYSPLIT, STILT et FLEXPART sont comparés sur CAPTEX et ANATEX, en utilisant des champs météorologiques communs (NARR et différentes configurations WRF). Les auteurs rapportent des compétences comparables entre les trois modèles lorsque les entrées météorologiques modernes sont identiques, et une sensibilité notable aux configurations météorologiques.

**Conséquence méthodologique :** une comparaison J-DriftX / modèle lagrangien doit maintenir les champs météorologiques et les paramètres comparables. Sinon, les écarts ne peuvent pas être attribués proprement à la formulation de transport.

### Rood (2014) — Winter Validation Tracer Study

Rood, A. S. (2014), *Performance evaluation of AERMOD, CALPUFF, and legacy air dispersion models using the Winter Validation Tracer Study dataset*, **Atmospheric Environment**, 89, 707–720. DOI [10.1016/j.atmosenv.2014.02.054](https://doi.org/10.1016/j.atmosenv.2014.02.054).

Le jeu WVTS comprend 12 essais de 11 heures en février 1991, avec émission continue de SF₆ et mesures horaires sur 140 échantillonneurs disposés en couronnes à 8 et 16 km. L'étude compare AERMOD et ISC2 (régime stationnaire) à CALPUFF et RATCHET (puffs lagrangiens). Les puffs obtiennent globalement une variance plus faible, une corrélation plus élevée et davantage de prédictions dans un facteur deux ; les modèles stationnaires sous-estiment moins souvent les maxima. Le résultat dépend donc de l'objectif d'évaluation : conformité réglementaire ou reconstruction de dose.

**Rapport à J-DriftX :** benchmark comparatif pertinent pour les panaches et les échelles intermédiaires, à condition de récupérer les données et de reconstruire précisément le protocole. Ne pas transformer le résultat d'une campagne en classement universel des familles de modèles.

## 4. Jeux de données expérimentaux candidats

### Prairie Grass (1956) — champ proche sur terrain plat

L'expérience comprend 68 périodes d'échantillonnage de dix minutes, avec émission continue de SO₂ près du sol et mesures sur des arcs à 50, 100, 200, 400 et 800 m. La hauteur d'émission est de 0,46 m pour la plupart des essais ; les essais 65 à 68 utilisent 1,5 m. Les profils météorologiques et paramètres de couche limite sont également documentés dans les ressources associées.

**Intérêt :** premier candidat pour un benchmark de champ proche et pour tester des profils de stabilité variés. Les règles d'exclusion de certains essais à vent très faible doivent être explicites ; elles ne doivent pas être choisies après observation des erreurs du modèle.

Source de données et ressources d'évaluation : [Aarhus University — OML / Prairie Grass](https://envs.au.dk/om-instituttet-1/faglige-omraader/luftforurening-udledninger-og-effekter/overvaagningsprogrammet/luftforureningsmodeller/baggrundsmateriale/oml).

### CAPTEX et ANATEX — transport régional

Ces campagnes de traceurs contrôlés sont documentées dans l'archive DATEM du NOAA ARL et utilisées par Andrews et al. (2013) pour comparer des modèles lagrangiens.

**Intérêt :** évaluer le transport régional et la sensibilité aux champs météorologiques. Les données ne doivent pas être considérées comme indépendantes des publications qui les exploitent sans vérifier les versions, périodes et prétraitements.

Source : [NOAA ARL — DATEM tracer evaluation](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/).

### ETEX (1994) — transport à l'échelle européenne

Le JRC décrit deux rejets de traceur et 168 stations d'échantillonnage réparties de l'Angleterre à l'Ukraine et de la Suisse à la Finlande. Les archives météorologiques et de traceur sont proposées séparément pour chacun des deux rejets.

**Intérêt :** transport à longue distance et évaluation de systèmes de prévision d'urgence. Deux rejets ne constituent pas un grand échantillon statistique ; la complétude des archives, les unités et les conditions de réutilisation doivent être auditées avant benchmark.

Sources : [présentation JRC ETEX](https://remon.jrc.ec.europa.eu/Past-Activities/ETEX) et [archives de données ETEX](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm).

### JU2003 — dispersion urbaine

Le rapport NOAA de Clawson et al. (2005) décrit dix périodes intensives d'observation à Oklahoma City, avec 29 rejets continus et 40 rejets en bouffées de SF₆. Les prélèvements sont effectués à environ 150 emplacements, au niveau de la rue, sur les toits, dans des tunnels piétonniers et sur des arcs à 1, 2 et 4 km. Le rapport décrit également le traitement des mesures et les contrôles qualité.

**Intérêt :** benchmark de domaine urbain et d'effets de rue-canyon, mais pas baseline initiale pour le noyau de champ proche sur terrain plat. Les différences de niveaux de prélèvement et de périodes jour/nuit imposent une stratification du protocole.

Source : [NOAA — Joint Urban 2003 SF₆ atmospheric tracer field tests](https://repository.library.noaa.gov/view/noaa/12573).

### ADMLC — catalogue de corpus, pas un jeu de données

L'Atmospheric Dispersion Modelling Liaison Committee répertorie des jeux expérimentaux et des modalités d'accès ; son Modellers' Data Archive (MDA) rassemble plusieurs dizaines de jeux. Le catalogue avertit que la qualité et l'adéquation de chaque jeu doivent être évaluées par l'utilisateur.

Source : [ADMLC — Atmospheric Dispersion Datasets](https://admlc.com/datasets/).

**MUST :** ne pas l'inscrire comme benchmark sélectionné dans cette PR. La piste est intéressante pour les effets d'obstacles, mais la source primaire précise, les fichiers accessibles et les conditions de réutilisation n'ont pas été suffisamment vérifiés pendant cette passe. À reprendre dans l'audit #207 avant toute intégration.

## 5. Priorisation proposée

1. **Benchmark initial : Prairie Grass**, en raison de sa géométrie relativement simple, de ses mesures à plusieurs distances et de sa documentation.
2. **Baseline lagrangienne : HYSPLIT ou FLEXPART**, avec entrées météorologiques communes et protocole contrôlé.
3. **Baseline gaussienne : AERMOD**, puis ADMS si le domaine de comparaison le justifie.
4. **Benchmark régional : CAPTEX/ANATEX**, pour tester le transport à plus grande échelle et la sensibilité météorologique.
5. **Comparaison stationnaire / puff : WVTS**, après audit des fichiers et reconstruction du protocole.
6. **Extension urbaine : JU2003 et GRAL**, seulement si le périmètre physique de J-DriftX inclut les obstacles et les écoulements urbains.

Cette hiérarchie est une proposition de travail, pas un résultat de validation. Avant tout classement, fixer les observables, les unités, les métriques, la stratification des régimes, les règles d'exclusion et l'indépendance entre calibration et validation.
