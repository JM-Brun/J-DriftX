# Revue structurée de l'état de l'art — dispersion atmosphérique à complexité réduite (2008 → 2026)

> Revue structurée établie en octobre 2026 pour décider de la reprise du projet Drift-X sous le nom **J-DriftX**.
> Toutes les sources citées sont listées dans [references.md](references.md) ; ce document n'utilise que des sources inspectées (résumés, notices, textes ouverts).

> **Avertissement adversarial (22 octobre 2026) :** ce document est une synthèse exploratoire, non une revue systématique reproductible. Plusieurs formulations du résumé exécutif et des constats thématiques ci-dessous (« aucun concurrent », « case vide », « exactement la cible », avantages de généralisation) sont trop affirmatives au regard des preuves consignées. Elles ne doivent pas être reprises comme conclusions établies. Lire en priorité la page publique sur les [limites et domaines de validité](../site/hypotheses/limites.qmd) et consulter les [issues scientifiques ouvertes](https://github.com/JM-Brun/J-DriftX/issues), qui recensent les questions restant à tester. Les formulations historiques ci-dessous sont conservées pour traçabilité, pas endossées comme résultats validés.

## Question de recherche

Le modèle Drift-X (2006–2009) reposait sur quatre paris : (1) une dispersion prédictible par solutions de similitude **généralisées dans une métrique non symétrique de temps de transport**, (2) sans résoudre d'EDP ni mailler, (3) calibrée par assimilation de données partielles, (4) utile pour la dérive de pesticides et l'identification de source. **Ces paris sont-ils toujours pertinents, concurrencés, dépassés ou confirmés par l'état de l'art de 2026 ? La reprise a-t-elle du sens ?**

## Méthodologie

Angles de recherche : (a) modèles opérationnels et réglementaires de dispersion ; (b) dérive de pulvérisation ; (c) ROM et apprentissage (POD, opérateurs neuronaux, surrogates) ; (d) identification de source / STE ; (e) SIG et open source ; (f) temps réel / jumeaux numériques. Sources privilégiées : textes réglementaires (US EPA, Federal Register), revues à comité de lecture, HAL/Zenodo, dépôts GitHub. Limite : le chapitre Springer 2008 n'est accessible qu'en extraits (paywall) ; l'analyse repose sur le texte fourni par l'auteur (p. 245–246) et le corpus compagnon.

## Limites de méthode et niveau de preuve

Cette version est une revue structurée, mais la méthode n'est pas encore entièrement reproductible : les chaînes de recherche exactes, dates par base, critères d'inclusion/exclusion, décomptes de sélection et évaluation formelle de la qualité des études ne sont pas consignés ici. Il faut compléter ces éléments avant de qualifier le travail de revue systématique. Certaines sources ne sont accessibles que par notice, résumé ou source secondaire ; ces limites doivent être prises en compte dans la force des conclusions. Les affirmations d'absence de concurrents et les avantages annoncés pour J-DriftX sont des hypothèses bornées par le corpus consulté, pas des preuves de nouveauté ou de supériorité. Voir aussi [le protocole public de validation](05-plan-validation-et-integration.md).

## Résumé exécutif

1. **La recherche effectuée n'établit pas l'absence de travaux concurrents sur le temps de transport dirigé.** Les ROM recensées comprennent plusieurs familles, mais elles ne sont pas toutes équivalentes ni nécessairement fondées sur les mêmes données. La nouveauté de la formulation J-DriftX reste indéterminée tant qu'une recherche systématique des termes mathématiques et des travaux antérieurs n'a pas été menée.
2. **Un problème applicatif est documenté, mais l'avantage de J-DriftX n'en découle pas.** L'EPA décrit des incertitudes et un caractère potentiellement très conservateur pour des scénarios précis de l'extension gaussienne AGDISP. La modernisation AGDISP vise notamment à mieux représenter les conditions spécifiques aux sites, le terrain et les drones ; elle peut donc réduire ou modifier la lacune supposée et doit être suivie comme une alternative concurrente, non comme une validation de l'opportunité J-DriftX.
3. **Des méthodes complémentaires sont désormais bien développées**, notamment la réduction de modèle, l'assimilation et l'identification de source. Cela fournit des baselines et des outils potentiels, mais ne démontre ni l'équivalence avec Drift-X ni la valeur d'une reprise.
4. **La disponibilité de données météorologiques et géographiques s'est améliorée**, mais cela ne signifie pas que les données indépendantes de dépôt/concentration nécessaires à la validation soient abondantes, compatibles ou accessibles. L'identifiabilité et la calibration restent à démontrer pour un observable et un scénario définis.
5. **Conclusion provisoire : seule une investigation scientifique limitée est justifiée à ce stade.** Avant de construire un noyau applicatif ou de revendiquer une niche, il faut choisir un besoin et un observable, confirmer l'accès à des données indépendantes, formaliser les hypothèses et comparer à des baselines pertinentes. Le résultat peut être de poursuivre, de restreindre fortement le domaine, ou d'arrêter.

## Constats par thème

### 1. Modèles opérationnels et réglementaires : consolidation gaussienne, pas de rupture

- L'EPA a promulgué en novembre 2024 une révision complète de l'Appendix W (Guideline on Air Quality Models), centrée sur les améliorations d'AERMOD, effective janvier 2025 : le paysage réglementaire near-field reste gaussien stationnaire.
- L'EPA classe désormais CALPUFF parmi les modèles « alternatifs », dont l'emploi doit être justifié au cas par cas. Dans une comparaison AERMOD/CALPUFF en environnement bâti (bâtiments d'élevage, validation par soufflerie), les deux modèles peuvent sur- ou sous-estimer les concentrations près des bâtiments d'un facteur deux ou davantage, alors que les résultats moyens plus en aval sont jugés adéquats. Ce constat est propre à cette configuration, pas un classement général des modèles ([étude de 2012](https://doi.org/10.1016/j.buildenv.2012.02.017)).
- Des travaux sur l'exposition humaine combinent CMAQ (fond régional/chimie) et AERMOD (gradient local), puis relient les concentrations à des modèles d'exposition ; un exemple publié en 2009 décrit cette approche hybride. Il s'agit d'une lignée méthodologique précise, pas d'une « revue récente d'AERMOD » ni d'une preuve générale de couplage SIG/santé publique. Les modèles opérationnels ont des domaines de validité et des incertitudes documentés, mais cela ne démontre pas que J-DriftX serait plus approprié ([Isakov et al., 2009](https://doi.org/10.3155/1047-3289.59.4.461)).

### 2. Dérive de pulvérisation : le domaine d'origine de Drift-X, en pleine ébullition

- Le couple AgDRIFT/AGDISP relie un modèle lagrangien de near-field (jusqu'à 800 m) à une extension gaussienne pouvant aller jusqu'à 20 km. Dans ses recommandations FIFRA de 2010, l'EPA qualifie l'estimation de far-field d'« extrêmement conservatrice » **dans le cadre d'hypothèses précises** : absence de barrières sur le trajet jusqu'à 20 km et absence de prise en compte de variables météorologiques au-delà du site d'application. La recommandation vise des cas de pulvérisation aérienne définis (adulticides anti-moustiques ou spectre de gouttelettes très fines à fines, hauteur minimale de 50 ft au-dessus du sol et 10 ft au-dessus de la canopée) ; elle signale un manque de validation au-delà de 2 miles. Ce constat ne doit pas être généralisé à toutes les pulvérisations ni interprété comme une validation de J-DriftX ([guidance EPA, sections Background/Guidance/Validation](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension)).
- L'**AGDISP Modernization Project** (AMP), établi par la National Agricultural Aviation Association et rejoint par Bayer Crop Science (mars 2026), vise à moderniser le code et à mieux intégrer conditions site/environnement spécifiques, techniques de réduction de dérive et évaluations par scénario. La source consultée ne suffit pas à établir qu'un module far-field rapide et réaliste est explicitement désigné comme « pièce manquante » ; l'AMP constitue une voie de développement concurrente à suivre, pas une validation de J-DriftX ([annonce de mars 2026](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/)).
- Les drones (RPAAS/UASS) soulèvent des questions de validation spécifiques ; un article de 2025 évalue AGDISPpro dans ce contexte, et plusieurs travaux recensent des approches ML (random forest, ANN, SVR). Leurs contraintes physiques et leur extrapolation doivent être examinées méthode par méthode. Les sources recensées ne suffisent pas à conclure qu'une « case vide » existe pour un modèle mécaniste rapide.
- Côté européen, la Directive 2009/128/CE encadre l'aérien et les modèles type Costanzini et al. (2018) comparent un modèle de proximité et CAREA pour l'exposition résidentielle aux pesticides ; le modèle CAREA lui-même est décrit séparément par Teggi et al. (2018) — la qualité du modèle change les décisions sanitaires.

### 3. ROM et apprentissage : maturité méthodologique, mais toujours a posteriori

- Les ROM de dispersion urbaine comprennent plusieurs familles : Arnoldi (2015, facteur ~2500 vs CFD rapporté après initialisation dans le cas étudié, avec champ de vitesse de fond pré-calculé), ROM physique POD-NN (Bologne, 2024), POD-GPR (nombre de snapshots et protocole à vérifier dans la source primaire), ROM avec assimilation de données (2023), et ROM POD + interpolation RBF appliqué au vent urbain et à la dispersion de gaz dans un canyon de rue (Ding & Yang, 2021, Pékin, domaine de 144 km²). Pour ce dernier, le résumé éditeur rapporte une réduction du temps CPU supérieure à 99 % et une perte d'information de 0,1 % par rapport au calcul CFD traditionnel ; ces chiffres sont des résultats annoncés par les auteurs, pas des résultats reproduits indépendamment ici. Le facteur 2500 de l'étude Arnoldi ne doit pas être confondu avec ses autres ratios (25× le temps réel ; coût annoncé 10⁵ fois inférieur), dont les périmètres diffèrent. Ces travaux sont des comparateurs de familles ROM, pas une validation directe de Drift-X/J-DriftX.
- Les surrogate neuronaux montent en gamme : FNO pour panaches radioactifs (2024), architectures masquage/correction 3D (CEA, 2024, priors physiques + opérateurs neuronaux), surrogates ML d'émissions industrielles, et prévision d'accidents de type Seveso (publication en ligne en 2022, volume 2023).
- Certaines approches recensées utilisent des simulations haute-fidélité et des snapshots ; ce n'est pas une propriété universelle de toutes les ROM et méthodes de substitution. Leurs performances d'interpolation et d'extrapolation dépendent de la méthode, des données et du régime étudié. Le coût, la généralisation et le besoin d'entraînement de J-DriftX doivent être mesurés et comparés ; une extrapolation correcte n'est pas garantie par la seule construction analytique. Une architecture hybride reste une hypothèse à évaluer, pas un positionnement déjà justifié.

### 4. Identification de source (STE) : un champ qui s'est structuré

- La revue de référence (Information Fusion, 2017) classe les méthodes STE (optimisation, adjoint, bayésien, renormalisation) ; NARAC opérationalise le STE à toutes échelles ; la technique de renormalisation (JAMES, 2014) fournit le formalisme d'opérateur inverse généralisé.
- La ressource Zenodo de Shafiyev et al. publiée en 2026 synthétise des méthodes STE et mentionne des problèmes ouverts. Elle ne suffit pas, à elle seule, à établir l'état de l'art ni à justifier un modèle physique comme garde-fou ; les affirmations sur la régularisation sous données rares/bruitées et la détection hors domaine doivent être corroborées par les articles primaires cités.
- Les documents historiques mentionnent une analyse de sensibilité du modèle direct. La disponibilité, l'exactitude et l'utilité d'un adjoint pour la formulation actuelle ne sont pas démontrées par le seul caractère analytique du modèle ; elles doivent être dérivées et vérifiées.

### 5. SIG et open source : plusieurs exemples actuels, nouveauté non établie

- Le corpus ciblé repère plusieurs plugins QGIS gaussiens (modèle GP QGIS intercompared 2026, plugin éducatif GitHub 2025, screening environnemental 2017). Cela suffit à montrer que l'intégration SIG n'établit pas, à elle seule, la nouveauté de J-DriftX ; cette sélection ne prouve toutefois ni l'exhaustivité de la recherche ni que le SIG est un standard uniforme dans tous les domaines. Le différenciateur scientifique doit être établi par comparaison des modèles, pas supposé à partir du couplage.
- Conséquence pour J-DriftX : architecture cœur Python pur (sans dépendance QGIS) + bindings/plugin QGIS en aval ; les sorties raster/vecteur géoréférencées sont attendues par défaut.

### 6. Tendances transverses : temps réel, jumeaux numériques, gouvernance

- Les travaux sur les jumeaux numériques urbains (feu/fumée, 2025) et la session SICC/CBRNe 2026 documentent des applications ou propositions associant simulation, données et aide à la décision dans des contextes particuliers. Ils ne suffisent pas à établir un consensus général ni une exigence EU AI Act uniforme pour toutes ces applications. Pour J-DriftX, l'auditabilité d'un modèle contraint par la physique est un avantage potentiel à démontrer, pas un résultat acquis.
- Des chaînes combinant prévisions ECMWF et dispersion CBRN sont documentées, par exemple CbrnAlert dans l'European Weather Cloud, qui utilise FLEXPART et des prévisions ECMWF récentes. Cela établit la faisabilité d'une intégration de ce type, pas que « données météo ouvertes → modèle rapide → tableau de bord » serait universellement le meilleur format ([présentation du cas CbrnAlert](https://www.europeanweather.cloud/use-cases/cbrnalert-web-application-near-real-time-dispersion-modelling-cbrn-releases)).

### 7. Modèles lagrangiens, turbulence et baselines complémentaires

La comparaison des modèles doit distinguer les **formulations physiques**, les **logiciels**, les **wrappers** et les **cadres génériques**. Les références ajoutées dans cette passe complètent les entrées FLEXPART v11, OpenDrift v1.0, PyAERMOD et la documentation EPA AERMOD déjà présentes dans la branche.

#### Modèles et familles

- **HYSPLIT** (Stein et al., 2015, [DOI 10.1175/BAMS-D-14-00110.1](https://doi.org/10.1175/BAMS-D-14-00110.1)) est une baseline lagrangienne majeure : trajectoires avant/arrière, dispersion particulaire 3D et puffs, transport, mélange, transformation et dépôt. Il complète FLEXPART pour la comparaison de formulations lagrangiennes sur des champs météorologiques communs.
- **UK-ADMS** (Carruthers et al., 1994, [DOI 10.1016/0167-6105(94)90044-2](https://doi.org/10.1016/0167-6105(94)90044-2)) est une baseline gaussienne avancée intégrant notamment couche limite, dépôt, terrain vallonné, zones côtières et bâtiments. Sa présence empêche d'assimiler « modèle gaussien » à une formulation simpliste.
- **GRAMM–GRAL** est une référence de microscale : GRAL couple un champ d'écoulement microscopique (RANS k–ε dans l'étude examinée) à un transport lagrangien particulaire. Öttl (2015), [DOI 10.1016/j.jweia.2015.03.014](https://doi.org/10.1016/j.jweia.2015.03.014), documente une validation du champ de vent par soufflerie. C'est un comparateur de domaine urbain/obstacles, pas une baseline immédiate si le champ de vent J-DriftX est imposé.
- **PyAERMOD** est un wrapper Python d'AERMOD, non une nouvelle formulation physique ; **OpenDrift** est un framework générique de trajectoires, pas nécessairement un modèle de concentration atmosphérique directement comparable ; **FLEXPART** est un modèle lagrangien particulaire. Il faut éviter de compter ces quatre objets comme quatre familles indépendantes.

La revue de Holmes & Morawska (2006), [DOI 10.1016/j.atmosenv.2006.06.003](https://doi.org/10.1016/j.atmosenv.2006.06.003), fournit une taxonomie historique des modèles boîte, gaussiens, lagrangiens/eulériens, CFD et modèles de dynamique des aérosols. Elle sert au cadrage, pas à classer les versions actuelles des logiciels.

#### Cohérence physique des modèles stochastiques

Thomson (1987), [DOI 10.1017/S0022112087001940](https://doi.org/10.1017/S0022112087001940), formalise des critères de cohérence pour les modèles stochastiques de trajectoires en turbulence inhomogène ou instationnaire, dont la condition *well-mixed*. Luhar & Britter (1989), [DOI 10.1016/0004-6981(89)90516-7](https://doi.org/10.1016/0004-6981(89)90516-7), construisent un modèle de marche aléatoire adapté à une couche limite convective inhomogène et dissymétrique.

Ces références sont centrales pour ne pas confondre :
1. une trajectoire moyenne ou une caractéristique déterministe ;
2. un transport de particules ;
3. une dispersion turbulente stochastique ;
4. une concentration moyenne résultant d'un ensemble de trajectoires.

Elles ne réfutent pas une formulation par temps de transport, mais imposent de décrire explicitement ce que cette formulation approxime et les effets qu'elle ne représente pas.

#### Comparaisons sur traceurs contrôlés

- Andrews et al. (2013), [DOI 10.1175/JAMC-D-13-0125.1](https://doi.org/10.1175/JAMC-D-13-0125.1), comparent HYSPLIT, STILT et FLEXPART sur CAPTEX et ANATEX avec des entrées météorologiques communes (NARR et configurations WRF). Les auteurs rapportent des performances comparables lorsque les champs météorologiques modernes sont identiques et une sensibilité importante aux configurations de ces champs. **Conséquence :** une comparaison de formulations doit contrôler les entrées météo avant d'interpréter les écarts.
- Rood (2014), [DOI 10.1016/j.atmosenv.2014.02.054](https://doi.org/10.1016/j.atmosenv.2014.02.054), évalue AERMOD, CALPUFF, ISC2 et RATCHET sur le Winter Validation Tracer Study : 12 essais de 11 h, SF₆, 140 échantillonneurs en couronnes à 8 et 16 km. Les puffs ont globalement une variance plus faible et une corrélation plus élevée ; les modèles stationnaires sous-estiment moins souvent les maxima. Les performances dépendent de l'objectif (conformité réglementaire ou reconstruction de dose), donc ce résultat n'établit aucun classement universel.

#### Jeux expérimentaux candidats

- **Prairie Grass (1956)** : 68 périodes de dix minutes, émissions de SO₂ proches du sol, mesures à 50, 100, 200, 400 et 800 m. La hauteur d'émission est de 0,46 m pour la plupart des essais ; les quatre derniers utilisent 1,5 m. Source et données associées : [Aarhus University / OML](https://envs.au.dk/om-instituttet-1/faglige-omraader/luftforurening-udledninger-og-effekter/overvaagningsprogrammet/luftforureningsmodeller/baggrundsmateriale/oml). Candidat prioritaire pour le champ proche ; les exclusions de périodes à vent très faible doivent être préspécifiées.
- **CAPTEX / ANATEX** : campagnes de traceurs contrôlés utilisées pour évaluer HYSPLIT, STILT et FLEXPART. L'archive NOAA DATEM donne les expériences et périodes ; elle doit être rapprochée des fichiers réellement récupérés et des prétraitements. Candidat pour le transport régional.
- **ETEX (1994)** : deux rejets et 168 stations selon le JRC ; les archives météo et traceur sont proposées séparément pour chaque rejet. Candidat pour le transport continental, mais le faible nombre de rejets et la complétude des fichiers limitent les conclusions statistiques.
- **JU2003** : rapport NOAA décrivant dix périodes intensives, 29 rejets continus et 40 rejets en bouffées de SF₆, environ 150 emplacements de mesure à Oklahoma City (rue, toiture, tunnels et arcs à 1, 2 et 4 km). Candidat pour une extension urbaine, non pour la première baseline sur terrain plat.
- **ADMLC** : catalogue de jeux expérimentaux et modalités d'accès, incluant le Modellers' Data Archive. Ce catalogue n'est pas lui-même un jeu de données et n'atteste pas la qualité ou l'adéquation de chaque corpus.
- **MUST** : piste non intégrée à la sélection validée de cette PR. La source primaire précise, les fichiers et les conditions de réutilisation restent à vérifier dans le cadre de l'audit #207.

Les notices, DOI, descriptions de contenu et limites d'accès sont consignés dans la [fiche détaillée modèles lagrangiens et benchmarks](bibliographie/modeles-lagrangiens-et-benchmarks.md). L'audit des données existant reste la source de vérité sur les fichiers effectivement inspectés, licences et unités d'indépendance ; l'ajout d'une référence ne signifie pas que les données sont téléchargées ou prêtes à servir de benchmark.

#### Séquence de comparaison proposée

1. Prairie Grass comme premier cas de champ proche et de complexité contrôlée.
2. AERMOD comme baseline gaussienne et HYSPLIT ou FLEXPART comme baseline lagrangienne, avec entrées météorologiques communes.
3. CAPTEX/ANATEX pour examiner la sensibilité météorologique et le transport régional.
4. WVTS pour comparer plume stationnaire et puff, après récupération et audit des fichiers.
5. JU2003 et GRAL uniquement si le périmètre J-DriftX s'étend aux obstacles et aux écoulements urbains.

Avant tout classement, fixer les observables, unités, métriques, stratification des régimes, règles d'exclusion, indépendance calibration/validation et coûts de préparation/calcul. Cette séquence est un plan d'investigation, pas un résultat de validation.

## Synthèse : positionnement de J-DriftX en 2026

| Dimension | État de l'art 2026 | Apport de J-DriftX |
|---|---|---|
| Réduction | Familles hétérogènes : ROM, surrogates, modèles analytiques et apprentissage | Hypothèse de réduction a priori par similitude, à formaliser et comparer |
| Coût | Coûts variables selon méthode, préparation, calibration et inférence | Coût complet et précision de J-DriftX non mesurés |
| Far-field dérive | L'EPA documente des limites dans des scénarios précis ; AGDISP est en cours de modernisation | Hypothèse de traitement du terrain et du transport dirigé à tester |
| Calibration | Assimilation/ML matures | Assimilation de données partielles (déjà dans Drift-X) à moderniser (bayésien) |
| STE | Plusieurs familles de méthodes inverses existent ; le choix dépend du problème | Applicabilité et calcul d'un adjoint pour J-DriftX à démontrer |
| SIG | Plugins QGIS gaussiens multiples | Cœur Python + plugin QGIS, standard attendu |

**Conclusion provisoire : les résultats de cette revue ciblée justifient de poursuivre l'investigation, mais la nouveauté, la robustesse et la valeur prédictive de J-DriftX restent à démontrer par des benchmarks reproductibles.** Dans les sources examinées, cette passe n'a pas établi si l'idée exacte a été reprise ou réfutée ; l'absence de résultat identifié ne prouve ni l'une ni l'autre. Les domaines applicatifs et l'écosystème méthodologique (assimilation, STE, benchmarks) offrent des pistes de validation, mais ne garantissent ni la nouveauté ni l'utilité du modèle.

## Notes de sources

| Source | Type de source / limite de lecture | Année de publication ou version |
|---|---|---|
| [Federal Register — Appendix W / AERMOD (US EPA)](https://www.federalregister.gov/documents/2024/11/29/2024-27636/guideline-on-air-quality-models-enhancements-to-the-aermod-dispersion-modeling-system) | Texte réglementaire officiel ; source primaire pour la règle publiée | 2024 |
| [US EPA — Alternative Models (statut CALPUFF)](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models) | Page institutionnelle officielle ; vérifier la version/date en cas de citation de statut historique | — |
| [US EPA — Guidance AGDISP-Gaussian Extension](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) | Guidance institutionnelle primaire de 2010 ; conclusions bornées aux scénarios indiqués | 2010 (page mise à jour 2026) |
| [AgAir Update — modernisation AGDISP / AMP](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/) | Presse professionnelle / annonce de projet ; recouper les résultats techniques avec les livrables AMP | 2026 |
| [Sci. Total Environ. — validation AGDISPpro drones](https://www.sciencedirect.com/science/article/pii/S0048969725003596) | Article scientifique éditeur ; conclusions limitées au protocole étudié | 2025 |
| [NCASI TB808 — historique AGDISP/AgDRIFT](https://ncasi.org/wp-content/uploads/2011/11/tb808.pdf) | Rapport technique secondaire ; contrôler les affirmations historiques contre les sources citées | 2007 |
| [HAL — ROM POD-GPR dispersion micro-échelle](https://hal.science/hal-04310899/document) | Dépôt institutionnel annoncé ; texte et nombre de snapshots non contrôlés dans cette passe | 2024 |
| [CMAME — ROM physique pollution urbaine](https://www.sciencedirect.com/science/article/abs/pii/S0045782523005406) | Notice éditeur ; contenu méthodologique à vérifier dans le texte intégral | 2024 |
| [ResearchGate — ROM Arnoldi built environment](https://www.researchgate.net/publication/277338242_Stable_reduced-order_models_for_pollutant_dispersion_in_the_built_environment) | Copie/notice secondaire ; les métadonnées sont recoupées avec DOI et source institutionnelle | 2015 |
| [SERRA — surrogate FNO panache radioactif](https://link.springer.com/article/10.1007/s00477-024-02738-8) | Article évalué par les pairs ; chiffres de performance bornés au protocole et aux simulations WSPEEDI | 2024 |
| [CEA/HAL — MCxM 3D deep learning dispersion](https://cea.hal.science/cea-04810109/document) | Dépôt institutionnel ; statut éditorial et détails à vérifier dans le document | 2024 |
| [SERRA — surrogate accidents Seveso](https://link.springer.com/article/10.1007/s00477-022-02288-x) | Article éditeur ; publication en ligne et année du volume distinguées | 2023 (en ligne 2022) |
| [Information Fusion — revue STE](https://www.sciencedirect.com/science/article/pii/S156625351630152X) | Article de revue évalué par les pairs ; revue de littérature, non preuve indépendante de chaque méthode citée | 2017 |
| [JAMES — renormalisation / STE](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014MS000385) | Article évalué par les pairs ; référence bibliographique corrigée en 2014 | 2014 |
| [NARAC / LLNL — STE opérationnel](https://narac.llnl.gov/research-and-development/source-term-estimation) | Page institutionnelle ; description de capacité opérationnelle, pas comparaison indépendante | — |
| [Shafiyev et al. — Source Term Estimation for Atmospheric Pollutant Releases](https://zenodo.org/records/22914336) | Ressource Zenodo ; évaluation par les pairs non établie ici, à corroborer par les sources primaires | 2026-09-22 |
| [Appl. Sci. — modèle QGIS gaussien 2026](https://www.mdpi.com/2076-3417/16/4/1833) | Article éditeur ; conclusions limitées à l'étude décrite | 2026 |
| [GitHub — plugin QGIS éducatif gaussien](https://github.com/Sebapac90/qgis-educational-gaussian-plume) | Dépôt logiciel communautaire ; utile comme preuve d'existence d'un outil, pas comme validation scientifique | 2025 |
| [Teggi et al. — modèle CAREA pour sources complexes](https://doi.org/10.1016/j.scitotenv.2017.07.196) | Article évalué par les pairs ; modèle CAREA pour sources complexes | 2018 |
| [Costanzini et al. — exposition aux pesticides avec CAREA](https://doi.org/10.3390/atmos9020038) | Article évalué par les pairs ; étude applicative distincte de la description du modèle CAREA | 2018 |
| [PMC — digital twin urbain feu/fumée](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/) | Article accessible via PMC ; statut éditorial et portée de l'exemple à vérifier au texte | 2025 |
| [SICC 2026 — session IA/Digital Twins CBRNe](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/) | Programme de conférence ; preuve d'une session, pas d'un consensus scientifique | 2026 |
| [European Weather Cloud — CbrnAlert (FLEXPART + prévisions ECMWF)](https://www.europeanweather.cloud/use-cases/cbrnalert-web-application-near-real-time-dispersion-modelling-cbrn-releases) | Cas d'usage institutionnel ; atteste une architecture déployée, pas sa supériorité générale | — |
| [EM-Consulte — CR Mécanique 334 (Mohammadi & Brun)](https://www.em-consulte.com/article/69927) | Notice éditeur de l'article primaire de 2006 | 2006 |
| [HAL — Drift-X / GIS-based model](https://hal.science/hal-00468863) | Manuscrit auteur en archive ouverte ; version et article de revue à distinguer | 2009 (version JESA 2010) |
| [Springer — chapitre Brun & Mohammadi 2008](https://link.springer.com/chapter/10.1007/978-1-4020-8758-5_14) | Notice éditeur confirmée ; seuls résumé et extrait p. 245–246 consultés dans cette passe | 2008 |

**Conflits et réserves** : les évaluations de CALPUFF vs AERMOD divergent selon les études (meilleure corrélation CALPUFF sur les tracer studies, mais facteurs 2 d'écart résiduels) ; les sources presse spécialisée (AgAir Update) sont à reconfirmer par les publications de l'AMP ; la ressource Zenodo publiée en 2026 n'est pas présentée ici comme revue évaluée par les pairs.


## Questions ouvertes

1. La métrique travel-time a-t-elle déjà été formalisée de façon autonome (thèse citée comme 2007 par l'article primaire ; année officielle à confirmer) ? Le document original doit être numérisé/déposé sur HAL pour servir de référence — action M0 de la roadmap.
2. Quel niveau d'accord (facteur 2 ? erreur L2 ?) viser sur les benchmarks far-field pour convaincre la communauté spray drift, sachant que les modèles réglementaires eux-mêmes vivent avec des facteurs 2 ?
3. Faut-il viser la conformité aux standards d'entrée AERMOD/AgDRIFT (météo au format météorologique réglementaire) pour l'interopérabilité ?
4. La calibration bayésienne (au lieu des moindres carrés) vaut-elle le coût en complexité au stade M1, ou est-ce un M2/M3 ?

## Recommandations

1. **Poursuivre uniquement l'investigation critique** — la niche scientifique n'est pas établie et le besoin applicatif doit être précisé.
2. Prioriser M1 : noyau Python + benchmark gaussien classique (reproductibilité) avant toute extension.
3. Suivre la modernisation d'AGDISP et évaluer objectivement si un besoin distinct subsiste ; aucune proposition d'extension ne devrait précéder une validation comparative.
4. Retrouver et vérifier les documents historiques avant de les déposer ou de revendiquer une antériorité ; vérifier les droits de diffusion des documents coécrits/édités.
5. Cibler une revue type *Atmospheric Environment* / *Environmental Modelling & Software* pour l'article de synthèse v2.
