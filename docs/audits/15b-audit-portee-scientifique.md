# Audit adversarial — portée scientifique, hypothèses et affirmations

> **Périmètre :** examiner la portée réelle des revendications scientifiques, des hypothèses physiques, des gains de coût, des propriétés mathématiques et des conclusions applicatives. Une référence correcte ne valide pas à elle seule une affirmation scientifique.

> Le registre d'entrée est [`docs/15-audit-adversarial-hallucinations.md`](../15-audit-adversarial-hallucinations.md). Les erreurs de métadonnées et de versions sont dans [l'audit bibliographique](15a-audit-bibliographique.md), et les incohérences de méthode/statut documentaire dans [l'audit méthodologique](15c-audit-methodologie-et-coherence.md).

### A-06 — Facteur de gain de coût 10³–10⁴ : résultat historique, pas promesse actuelle

- **Statut :** affirmation publiée à contextualiser ; pas une performance vérifiée de J-DriftX.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, fiches 2006, roadmap et éventuelles pages de présentation.
- **Constat :** l'article Mohammadi & Brun (2006) rapporte un gain d'environ 10³–10⁴ par point dans ses exemples, comparé à une simulation de référence donnée par les auteurs. Ce chiffre dépend du cas, de l'implémentation, du nombre de points et du périmètre du coût mesuré. Il ne peut pas être transposé au code Python actuel, à un autre domaine ou au coût total (calibration, préparation du champ, assimilation et validation) sans nouveau benchmark.
- **Source :** [article primaire de 2006](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf).
- **Correction sûre :** toujours écrire « les auteurs rapportent, pour les exemples de leur article… » et fournir la comparaison exacte ; présenter toute performance J-DriftX comme « non mesurée » jusqu'à un benchmark reproductible à précision comparable.


### A-07 — « Sans résolution d'EDP », « sans maillage » : portée historique à circonscrire

- **Statut :** description d'une approche historique, pas preuve d'absence de toute résolution PDE dans la chaîne complète.
- **Emplacement :** README, pages de positionnement et revue.
- **Constat :** les résumés de 2006 et 2008 présentent une évaluation à faible coût ne nécessitant pas de résoudre directement l'EDP sur le domaine pour chaque évaluation. L'article de 2006 compare toutefois la méthode à un modèle de référence résolvant une équation de transport-diffusion-dépôt par éléments finis. La formulation ne doit pas laisser entendre que la méthode a été validée sans modèle de référence, ni que toute préparation/calibration est sans calcul numérique.
- **Correction sûre :** préciser « l'évaluation réduite décrite par les auteurs ne résout pas l'EDP complète à chaque point d'évaluation » ; décrire séparément les calculs de construction, assimilation et référence.


### A-08 — Revue systématique : méthode de reporting ≠ preuve d'exhaustivité

- **Statut :** risque méthodologique connu, déjà partiellement reconnu dans le dépôt.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, `docs/05-plan-validation-et-integration.md`, `docs/06-choix-methode-revue-systematique.md`, pages Quarto et résumés exécutifs dans `raw/reviews/`.
- **Constat :** PRISMA 2020 est une ligne directrice de reporting. Sa mention ne prouve pas à elle seule que la recherche documentaire est exhaustive, reproductible ou évaluée sur le risque de biais. Il faut des sources et dates de recherche, requêtes exactes, critères d'éligibilité, nombres réellement observés aux étapes de sélection, raisons d'exclusion et méthode d'évaluation critique.
- **Source de méthode :** [PRISMA 2020 — site officiel](https://www.prisma-statement.org/prisma-2020) ; [article explicatif en accès libre](https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/).
- **Correction sûre :** ne pas appeler la revue « exhaustive » ou « entièrement reproductible » avant d'avoir produit et vérifié les éléments ci-dessus. Les documents de synthèse stockés dans `raw/reviews/` ne sont pas des sources primaires et ne peuvent pas confirmer eux-mêmes les affirmations qu'ils rapportent.


### A-09 — Hypothèses de conservation, divergence et propriétés de la pseudo-distance

- **Statut :** point mathématique à contrôler proposition par proposition, sans généralisation.
- **Emplacement :** documentation scientifique et implémentation.
- **Constat :** les sources historiques imposent certaines contraintes physiques et décrivent une pseudo-distance non symétrique qui peut ne pas séparer les points et violer l'inégalité triangulaire. Cela ne suffit pas à démontrer que toute construction J-DriftX conserve exactement la masse sur toute surface iso-temps, pour tout champ de vitesse ou en présence de sources, puits, stagnations et caractéristiques non uniques.
- **Correction sûre :** pour chaque affirmation de conservation, donner l'équation, les hypothèses (régularité, stationnarité, divergence, conditions aux limites, source/puits, unicité de caractéristique/projection) et une preuve ou un contre-exemple. Séparer les propriétés citées de la source historique des propriétés démontrées pour le modèle actuel.


### A-12 — Conclusions de la revue d'état de l'art plus fortes que les preuves consignées

- **Statut :** extrapolations non démontrées ; formulation corrigée dans cette PR.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`.
- **Constat :** le résumé exécutif et les tableaux comparatifs affirmaient notamment qu'aucun concurrent n'avait repris la métrique travel-time, que la niche restait ouverte, que la dérive mécaniste rapide était une « case vide », que les ROM exigeaient toutes des snapshots CFD/LES, que J-DriftX extrapolerait « par construction » et qu'un adjoint serait « disponible par construction ». La revue elle-même reconnaissait que les requêtes, les critères et les décomptes n'étaient pas entièrement reproductibles.
- **Pourquoi c'est problématique :** une recherche ciblée ne prouve pas l'absence de travaux ; les familles de ROM sont hétérogènes ; une formule analytique ne garantit ni extrapolation prédictive ni disponibilité d'un adjoint utile ; un besoin réglementaire non couvert ne prouve pas qu'une méthode proposée le couvre.
- **Correction effectuée dans cette PR :** réécriture des conclusions exécutives et de plusieurs affirmations thématiques en hypothèses bornées ; correction du tableau de positionnement et des recommandations pour ne pas présenter la nouveauté, la supériorité ou le besoin d'une extension AGDISP comme acquis.
- **Preuve de clôture :** chaque comparaison restante doit pointer vers le passage précis de la source primaire, expliciter le régime et l'observable, et être classée comme fait, hypothèse ou question ouverte.


### B-13 — Facteur ×4000 du surrogate U-FNO : périmètre de comparaison et validation

- **Statut :** chiffre primaire vérifié ; toute généralisation au coût total ou à la validation terrain serait non étayée.
- **Emplacement :** `docs/bibliographie/rom-et-apprentissage.md` ; à contrôler dans tout résumé comparatif des méthodes rapides.
- **Constat :** Ayoub et al. (2024) rapportent un surrogate U-FNO entraîné sur un corpus de 616 simulations WSPEEDI, avec une séparation 85/15. Le facteur annoncé d'environ 4000 compare environ 82 minutes pour une simulation WSPEEDI de six heures à environ 1,26 seconde pour une inférence du modèle entraîné. Il n'inclut donc pas, à lui seul, la génération des simulations d'apprentissage, la préparation des données ni l'entraînement. La cible évaluée est le simulateur numérique, pas une mesure indépendante du monde réel.
- **Source primaire :** [texte intégral éditeur, sections 2, 4–6](https://link.springer.com/article/10.1007/s00477-024-02738-8).
- **Correction effectuée :** la fiche bibliographique précise le périmètre du speed-up, les limites du corpus fini, la sous-estimation signalée lors de dépôts humides et le besoin de validation sur données réelles reconnu par les auteurs. Le facteur ×4000 n'est pas traité comme benchmark transférable à J-DriftX.
- **Preuve de clôture :** toute comparaison J-DriftX/ML doit mesurer séparément coût de préparation, entraînement, inférence, erreur sur test indépendant, extrapolation et validation terrain.


### B-14 — Vervecken et al. (2015) : méthode et accélérations à contextualiser

- **Statut :** métadonnées et résumé éditeur vérifiés ; portée des chiffres explicitée dans la fiche, texte intégral non audité ligne à ligne.
- **Emplacement :** `docs/bibliographie/rom-et-apprentissage.md`, entrée BibTeX `vervecken2015rom`.
- **Constat :** la notice éditeur confirme trois auteurs (Vervecken, Camps et Meyers), *Building and Environment* 92, 360–367, DOI 10.1016/j.buildenv.2015.05.008. Le résumé décrit une projection Krylov/Arnoldi d'un modèle CFD d'advection-diffusion instationnaire sur un champ de vitesse de fond stationnaire, pour un rejet temporel de gaz neutre à la centrale de Doel. Les ratios rapportés — environ 2500× par rapport au CFD après initialisation, 25× plus rapide que le temps réel et un coût calculatoire annoncé 10⁵ fois inférieur — ont des périmètres distincts et sont spécifiques aux cas étudiés.
- **Source primaire de contrôle :** [notice éditeur et résumé](https://doi.org/10.1016/j.buildenv.2015.05.008).
- **Correction effectuée :** la fiche distingue le coût de construction initial, le champ CFD pré-calculé, les hypothèses de régime et les ratios de performance ; elle interdit de les transférer directement à J-DriftX ou à la dérive de pulvérisation.
- **Preuve de clôture :** lire les sections méthodologiques et résultats du texte intégral, relever précisément les cas, métriques et périmètres de coût, puis comparer seulement sur un protocole commun.


### B-17 — Comparaisons réglementaires : portée des conclusions EPA et AERMOD/CALPUFF

- **Statut :** sur-généralisation identifiée et formulation corrigée.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, sections sur modèles opérationnels, dérive de pulvérisation et AGDISP.
- **Constat :** la guidance EPA de 2010 décrit l'extension gaussienne AGDISP comme « extremely conservative » dans un cadre FIFRA défini, en supposant notamment l'absence de barrières sur la trajectoire et en ne représentant pas certaines variables météorologiques au-delà du site d'application. Elle limite les usages recommandés à certains cas de pulvérisation aérienne et note le manque de validation au-delà de 2 miles. La formule générale « extrêmement conservatrice » sans ces conditions aurait pu être lue comme une propriété de toutes les applications. De même, un résultat d'une comparaison AERMOD/CALPUFF en environnement bâti ne permet pas de classer globalement ces modèles.
- **Sources primaires :** [guidance EPA de 2010, sections Background/Guidance/Validation](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) ; [étude de comparaison en environnement bâti](https://doi.org/10.1016/j.buildenv.2012.02.017) ; [annonce AMP du 9 mars 2026](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/).
- **Correction effectuée :** les conditions d'application et la portée de validation EPA sont explicitées ; le résultat AERMOD/CALPUFF est attribué à un cas précis ; l'AMP est présenté comme une voie de modernisation concurrente, sans inventer un besoin de module explicitement annoncé par la source.
- **Preuve de clôture :** les autres affirmations comparatives de la revue doivent, de même, identifier le cas, l'observable, le protocole et la portée de validité de chaque source.


### B-18 — Tendances CBRN / jumeaux numériques : consensus et « format gagnant » non démontrés

- **Statut :** formulations de tendance trop fortes, corrigées.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, section « Tendances transverses » et tableau des sources.
- **Constat :** les sources sur les jumeaux numériques urbains, une session SICC/CBRNe et les prévisions ECMWF attestent des applications et initiatives spécifiques, mais ne démontrent ni un consensus universel en faveur d'une architecture donnée, ni que la conformité EU AI Act est explicitement exigée dans tous les cas, ni qu'une chaîne « données météo ouvertes → modèle rapide → tableau de bord » est un « format gagnant ». En revanche, la page CbrnAlert de l'European Weather Cloud décrit concrètement une plateforme utilisant FLEXPART et des prévisions ECMWF récentes.
- **Sources :** [CbrnAlert / European Weather Cloud](https://www.europeanweather.cloud/use-cases/cbrnalert-web-application-near-real-time-dispersion-modelling-cbrn-releases) ; [session SICC/CBRNe 2026](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/) ; [étude sur jumeau numérique feu/fumée](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/).
- **Correction effectuée :** les sources sont décrites comme exemples contextualisés, l'existence d'une intégration ECMWF–FLEXPART est citée directement et les superlatifs/conclusions de consensus sont retirés.
- **Preuve de clôture :** les conclusions transverses restantes doivent être distinguées des constats source par source et ne pas transformer un exemple de déploiement en preuve de supériorité générale.


### B-19 — Affirmations négatives (« aucun code », « jamais publié », idée non reprise) non démontrées

- **Statut :** formulations absolues non soutenues par une recherche d'absence exhaustive ; corrigées.
- **Emplacement :** `docs/01-audit-heritage-driftx.md` et conclusion/positionnement de `docs/02-revue-etat-art-2026.md`.
- **Constat :** des formulations telles que « aucun dépôt de code n'a accompagné les publications », « l'ensemble n'a jamais été consolidé en un article de revue » ou « l'idée n'a été ni reprise ni démentie » transforment l'absence de résultat dans le corpus consulté en affirmation générale sur la littérature ou l'historique du projet. La recherche effectuée n'étant pas exhaustive et reproductible, ces propositions ne sont pas démontrées.
- **Correction effectuée :** les formulations précisent désormais « aucune ressource identifiée dans le corpus/recherches consignées » et explicitent que cela ne prouve pas une absence générale ; la conclusion de l'état de l'art ne prétend plus établir la non-reprise ou la non-réfutation de l'idée.
- **Preuve de clôture :** si une conclusion d'absence doit être maintenue, documenter les bases consultées, requêtes exactes, dates, langues, critères, décomptes et recherche de citation/rétrospective ; sinon conserver le statut « non identifié dans cette passe ».


### B-21 — Hybridation CMAQ/AERMOD : temporalité et portée mal décrites

- **Statut :** source et formulation recontextualisées.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, section « Modèles opérationnels et réglementaires ».
- **Constat :** le texte parlait de « revues récentes d'AERMOD » pour soutenir l'hybridation CMAQ+AERMOD et un couplage SIG/santé publique. Une source primaire pertinente est plutôt l'étude d'Isakov et al. (2009), qui combine un modèle régional chimique CMAQ, le modèle local AERMOD et des modèles d'exposition humaine. La référence démontre l'existence d'une approche hybride dans ce contexte, pas une revue récente ni une supériorité universelle.
- **Source :** [Isakov et al. (2009), DOI 10.3155/1047-3289.59.4.461](https://doi.org/10.3155/1047-3289.59.4.461).
- **Correction effectuée :** la phrase est attribuée à cette lignée précise et ne présente plus le travail comme une revue récente d'AERMOD.
- **Preuve de clôture :** si une autre source est destinée à soutenir une tendance plus récente, l'ajouter explicitement et vérifier le passage exact.


### B-22 — Verdict global de validité/originalité et garanties physiques trop catégoriques

- **Statut :** formulations trop fortes, corrigées dans les documents de synthèse et de lecture.
- **Emplacements :** `docs/01-audit-heritage-driftx.md`, `site/projet/audit.qmd`, `docs/04-revues-papiers-sources.md`, `raw/fiches/2009-bozon-sinfort-mohammadi-driftx-hal.md`.
- **Constat 1 — verdict scientifique :** la conclusion « cœur scientifique sain, original et toujours différenciant » dépassait les preuves disponibles. Une revue ciblée, quelques articles historiques et l'absence de benchmarks modernes indépendants ne suffisent pas à établir la validité mathématique, la nouveauté exhaustive ou l'avantage actuel. Les lacunes portent donc aussi sur la formalisation et la validation, pas seulement sur le code.
- **Constat 2 — invariants :** le manuscrit Bozon, Sinfort & Mohammadi (2009) affirme que sa restriction multi-niveaux préserve la divergence nulle **si** le champ précédent vérifie cette propriété, et que la restriction de concentration satisfait le bilan de masse entrant. Les fiches résumaient cela comme des garanties inconditionnelles et transférables à une réimplémentation. Le texte source rapporte une propriété sous construction/hypothèses ; il ne valide pas automatiquement les calculs numériques, les données, ni un nouveau code.
- **Sources internes primaires :** extraction du manuscrit HAL `raw/extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt`, autour des équations [2]–[4] (notamment les lignes extraites autour de 461–505) ; fiche documentaire [HAL hal-00468863](https://hal.science/hal-00468863).
- **Corrections effectuées :** le verdict global est remplacé par une hypothèse méthodologique à tester ; les propriétés multi-niveaux sont explicitement attribuées aux auteurs et conditionnées à leurs hypothèses ; les fiches demandent une dérivation et des tests avant de les traiter comme garanties d'une implémentation moderne. Les absences de publication de synthèse sont également formulées comme « non identifiée dans les recherches consignées ».
- **Tests requis avant clôture :** (1) écrire les hypothèses et la définition précise de la divergence pour le champ utilisé ; (2) vérifier symboliquement que l'interpolation par fonctions de forme conserve les conditions aux limites revendiquées ; (3) vérifier le bilan de masse par intégration de flux sur des cas analytiques ; (4) tester les erreurs discrètes sur plusieurs grilles, géométries et niveaux ; (5) distinguer propriété continue, propriété de l'algorithme discret et résultat observé dans le prototype historique.


### B-23 — Page « Contraintes physiques » : couverture CI exagérée et garanties non implémentées

- **Statut :** affirmation directement contredite par le code et les tests actuels ; corrigée.
- **Emplacements :** `site/theorie/contraintes-physiques.qmd`, docstring de `src/jdriftx/constraints.py`.
- **Constat :** l'ancienne page affirmait que quatre contraintes (conservation, positivité, linéarité et divergence nulle) étaient « vérifiées en continu par la CI ». Or le module de contraintes ne contient que des helpers de positivité et de superposition ; il n'implémente pas de vérification de divergence. La conservation est testée séparément sur un seul panache gaussien, avec une grille finie et une tolérance de 2 %. Les tests de positivité et de linéarité couvrent eux aussi des configurations ciblées, pas toutes les extensions possibles. La page appelait en outre la concentration une « densité de probabilité », ce qui confond deux grandeurs différentes, et affirmait sans comparaison sourcée que les surrogates ML ne garantissent aucune propriété physique.
- **Preuves de code :** `src/jdriftx/constraints.py` (seuls les helpers `positivite` et `linearite`) ; `tests/test_constraints.py` ; `tests/test_similitude.py::test_conservation_masse_panache` (grille `y ∈ [-500,500]`, `z ∈ [0,400]`, cas unique, tolérance relative 2 %).
- **Correction effectuée :** la page expose maintenant un tableau propriété/test/limite, précise que la divergence n'est pas testée, borne le résultat de conservation au cas numérique testé, corrige la distinction concentration/probabilité et remplace l'opposition générale aux modèles ML par une comparaison empirique des garanties et erreurs.
- **Preuve de clôture :** ajouter séparément les tests/proofs nécessaires à chaque invariant et préciser leur domaine de validité ; tant que le champ de vent historique n'est pas implémenté, ne pas revendiquer la vérification de sa divergence.


### B-24 — Pages théoriques : garanties, complexités et gradients présentés comme acquis

- **Statut :** plusieurs généralisations et avantages non démontrés corrigés.
- **Emplacements :** `site/theorie/reduction-a-priori.qmd`, `assimilation-identification.qmd`, `modele-direct.qmd`, `comparaison-complexites.qmd`.
- **Constats :** les pages présentaient la consistance physique comme « garantie par contraintes » alors que le champ de vent historique n'est pas implémenté ; les méthodes POD étaient décrites comme exigeant toutes des snapshots CFD/LES et comme fragiles hors domaine ; l'optimisation était dite triviale grâce à un coût d'évaluation quasi nul ; les gradients/adjoints J-DriftX étaient dits exacts, gratuits et disponibles par construction ; la comparaison affirmait que les surrogates ML ne respectent pas les contraintes physiques et que les modèles CFD repartent toujours de zéro pour chaque scénario. Ces propositions sont trop générales ou contredites par l'état du code.
- **Correction effectuée :** les pages distinguent les objectifs historiques des capacités du prototype actuel ; elles conditionnent les propriétés aux formulations et aux tests, séparent coût d'évaluation et coût total de calibration, décrivent les gradients comme non établis pour la métrique complète et reconnaissent que certaines méthodes ROM/ML peuvent intégrer des contraintes physiques. Les coûts CFD et particulaires sont décrits comme dépendants du workflow et de l'observable. Une clé bibliographique périmée `renormalization2016` a aussi été remplacée par `renormalization2014`.
- **Preuve de clôture :** toute comparaison quantitative devra utiliser un protocole commun (observable, précision, régime, coûts de préparation/calibration/inférence, mémoire et incertitude) ; toute affirmation de gradient/adjoint devra être rattachée à une dérivation ou à une implémentation testée.


### B-25 — Page d'utilité scientifique en contradiction avec le statut G0 courant

- **Statut :** contradiction documentaire confirmée et corrigée.
- **Emplacements :** `site/projet/utilite-scientifique.qmd` et `site/projet/preuves-g0.qmd`, conclusions de page.
- **Constat :** la page affirmait encore « G0 non franchi », alors que `docs/13-fiche-g0-cadrage-besoin.md` et `docs/15-audit-corpus-g0-resultats.md` enregistrent une décision G0 franchie le 22 octobre 2026 sur la base du cadrage et d'un audit documentaire des corpus. La contradiction risquait de faire confondre le statut du jalon documentaire et l'absence de validation scientifique/applicative.
- **Correction effectuée :** les deux pages indiquent désormais que G0 est franchi au niveau documentaire, mais que G1, la validation des fichiers bruts et le benchmark restent en attente ; elles rappellent que ce statut ne prouve ni l'utilité prédictive ni l'adéquation scientifique du modèle.
- **Preuve de clôture :** maintenir un statut unique et cohérent entre fiche G0, audit de corpus, page publique et roadmap ; ne faire évoluer G1 qu'après contrôle des fichiers et licences.


### B-26 — Page qualité : tests inexistants cités et portée de la CI exagérée

- **Statut :** erreurs de documentation directement vérifiables, corrigées.
- **Emplacement :** `site/projet/qualite.qmd`.
- **Constat :** la page citait `test_non_symetrie_champ_non_uniforme`, absent de la suite de tests, et présentait plusieurs tests comme s'ils validaient simultanément plusieurs propriétés (par exemple la superposition et la positivité). Elle annonçait aussi « pytest + coverage », alors que la commande CI exécute pytest sans rapport de couverture. Le slogan « l'oracle des tests est la physique elle-même » et l'idée que chaque test indique nécessairement une propriété physique violée étaient trop catégoriques.
- **Preuves :** `tests/test_metric.py`, `tests/test_constraints.py`, `tests/test_similitude.py`, `.github/workflows/ci.yml` et `pyproject.toml`.
- **Correction effectuée :** la page énumère les tests existants par nom, explique ce qu'ils testent et ce qu'ils ne testent pas, retire le test fictif et la mention de couverture non exécutée, et distingue tests ciblés, preuve mathématique et validation physique. Elle précise que la divergence n'est pas testée parce que le champ de vent multi-niveaux n'est pas implémenté.
- **Preuve de clôture :** garder cette page synchronisée avec les fichiers de tests et le workflow CI ; toute nouvelle affirmation de couverture doit pointer vers un test existant et décrire sa portée.


### B-27 — Synthèse publique de l'héritage : coût nul, transférabilité et disponibilité des données sur-généralisés

- **Statut :** formulations trop fortes, corrigées dans la synthèse web et la note de fond.
- **Emplacements :** `site/projet/audit.qmd` et `docs/01-audit-heritage-driftx.md`.
- **Constats :** l'ancienne synthèse décrivait la métrique comme « originale et transposable », le coût comme indépendant du domaine ou nul par évaluation, et les données modernes comme ayant remplacé la rareté de 2006. Elle présentait également l'absence de comparaison STE comme un fait général. Ces affirmations dépassaient les éléments documentés : une évaluation ponctuelle ne supprime pas les coûts de préparation, de caractéristique et de calibration ; l'accès aux données reste soumis à la couverture, à la résolution, à la qualité et aux droits ; une revue ciblée ne suffit pas à conclure à la nouveauté ou à l'absence exhaustive de comparateurs.
- **Correction effectuée :** les deux synthèses parlent désormais d'hypothèses historiques et de contexte ayant évolué, sans affirmer que les coûts sont nuls, que la nouveauté est établie ou que les contraintes d'accès aux données ont disparu.
- **Preuve de clôture :** comparer les coûts complets et la transférabilité sur un protocole reproductible ; documenter la couverture et les licences des données réellement utilisées ; formaliser le protocole de recherche bibliographique avant toute conclusion d'originalité.


### B-30 — Filiation historique non établie entre la pseudo-distance travel-time et les métriques d'adaptation de maillage

- **Statut :** affirmation historique trop catégorique, corrigée.
- **Emplacement :** `site/theorie/metrique-travel-time.qmd`, section « Généalogie ».
- **Constat :** le texte affirmait que la métrique travel-time « descend » de la métrique utilisée pour l'adaptation de maillage anisotrope et que Drift-X transfère cette technologie au contrôle de la géométrie du panache. La référence Borouchaki et al. sur la génération de maillages ne suffit pas, à elle seule, à prouver une filiation historique ou une équivalence mathématique avec la pseudo-distance définie dans les sources Drift-X.
- **Correction effectuée :** le rapprochement est présenté comme une analogie conceptuelle entre deux usages de géométries dépendantes du problème. La filiation directe reste non établie faute de source explicite.
- **Preuve de clôture :** retrouver une source historique primaire décrivant ce transfert, ou conserver la formulation en termes d'analogie et non de généalogie.


### B-31 — Domaine d'entrée incomplet des primitives travel-time

- **Statut :** défaut de validation d'entrée confirmé et corrigé dans cette PR.
- **Emplacements :** `src/jdriftx/metric.py`, `tests/test_metric.py`.
- **Constat :** les fonctions convertissaient les entrées en tableaux numériques et contrôlaient leur forme, mais ne rejetaient pas systématiquement les coordonnées/vitesses non finies (`NaN`, (+\infty), (-\infty)). Dans `temps_transport`, une valeur `umin` nulle ou négative pouvait également neutraliser le garde-fou sur la vitesse; les calculs pouvaient alors retourner `NaN` ou `inf` au lieu d'un rejet explicite.
- **Correction effectuée :** les primitives rejettent maintenant les coordonnées et vitesses non finies; `temps_transport` exige en outre un seuil `umin` fini et strictement positif. Des tests paramétrés couvrent ces cas.
- **Limite :** ces contrôles améliorent la robustesse numérique des API; ils ne valident ni la définition historique complète de la pseudo-distance, ni la physique du modèle.
- **Preuve de clôture :** suite de tests et CI sur le HEAD de la PR; conserver une distinction explicite entre validité des entrées, propriétés mathématiques et validation physique.



### B-34 — Conservation de flux : débit volumique et flux de polluant confondus dans le raisonnement potentiel

- **Statut :** risque d'inférence scientifique identifié; formulation clarifiée, revendication historique exacte toujours à vérifier.
- **Emplacement :** `docs/14-revue-mathematique-ciblee.md`, §3.4.1.
- **Constat :** `\nabla\cdot\mathbf u=0` permet, sous régularité et géométrie de tube de courant, de conclure à la conservation du débit volumique signé entre sections transverses. Cela ne suffit pas à conclure que le flux advectif d'un scalaire `c\mathbf u` vaut le débit source `Q`; ce second résultat dépend de l'équation de bilan, des sources et des autres termes de transport.
- **Correction effectuée :** la note donne une dérivation conditionnelle par le théorème de la divergence et distingue le flux du fluide de celui du polluant. Elle n'affirme pas que cette dérivation prouve la revendication historique des surfaces iso-\tau.
- **Limite :** le sens précis de `Q`, le domaine d'intégration et les hypothèses de la formule historique doivent encore être vérifiés dans les sources accessibles, sans examiner la thèse.
- **Preuve de clôture :** relier la revendication à une équation de bilan explicitement sourcée et vérifier les conditions de frontière, l'émission et les termes négligés.



### B-35 — Hypothèses de la dérivation gaussienne et portée du test de conservation

- **Statut :** hypothèses implicites et portée du contrôle CI clarifiées.
- **Emplacement :** `site/theorie/similitude.qmd`, étapes 1 et 5 de la dérivation du panache gaussien.
- **Constat :** l'équation parabolique écrite dans la dérivation omet la diffusion longitudinale et suppose un vent uniforme positif ainsi que des diffusivités transversales constantes. Ces conditions doivent être énoncées avant de présenter la réduction en temps de transport. En outre, la normalisation de la gaussienne sans source image intègre sur tout l'axe vertical; elle ne représente pas encore le demi-espace physique au-dessus du sol.
- **Correction effectuée :** les hypothèses incluent désormais explicitement l'absence de diffusion longitudinale, de réaction et de dépôt, la source en `x = 0`, `U > 0`, et le domaine `x > 0`. La normalisation analytique est séparée de l'ajout ultérieur de la condition de sol par méthode des images.
- **Portée du test :** le test existant vérifie numériquement un cas du panache implémenté à `x = 1000 m`, sur une grille finie et avec une tolérance relative de 2 %. Il s'agit d'un contrôle de régression ciblé, non d'une preuve de conservation exacte pour tout `x` ni d'une validation de la dérivation à diffusivités constantes.
- **Preuve de clôture :** rendu Quarto, suite de tests et CI sur le HEAD de cette PR. Ces contrôles vérifient la documentation et l'implémentation, pas la validité de toutes les hypothèses physiques possibles.
