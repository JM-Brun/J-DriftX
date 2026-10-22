# Revue structurée de l'état de l'art — dispersion atmosphérique à complexité réduite (2008 → 2026)

> Revue structurée établie en octobre 2026 pour décider de la reprise du projet Drift-X sous le nom **J-DriftX**.
> Toutes les sources citées sont listées dans [references.md](references.md) ; ce document n'utilise que des sources inspectées (résumés, notices, textes ouverts).

> **Avertissement adversarial (22 octobre 2026) :** ce document est une synthèse exploratoire, non une revue systématique reproductible. Plusieurs formulations du résumé exécutif et des constats thématiques ci-dessous (« aucun concurrent », « case vide », « exactement la cible », avantages de généralisation) sont trop affirmatives au regard des preuves consignées. Elles ne doivent pas être reprises comme conclusions établies. Lire en priorité la [revue adversariale G0](10-revue-adversariale-g0.md), qui précise les limites documentées et les objections à tester. Les formulations historiques ci-dessous sont conservées pour traçabilité, pas endossées comme résultats validés.

## Question de recherche

Le modèle Drift-X (2006–2009) reposait sur quatre paris : (1) une dispersion prédictible par solutions de similitude **généralisées dans une métrique non symétrique de temps de transport**, (2) sans résoudre d'EDP ni mailler, (3) calibrée par assimilation de données partielles, (4) utile pour la dérive de pesticides et l'identification de source. **Ces paris sont-ils toujours pertinents, concurrencés, dépassés ou confirmés par l'état de l'art de 2026 ? La reprise a-t-elle du sens ?**

## Méthodologie

Angles de recherche : (a) modèles opérationnels et réglementaires de dispersion ; (b) dérive de pulvérisation ; (c) ROM et apprentissage (POD, opérateurs neuronaux, surrogates) ; (d) identification de source / STE ; (e) SIG et open source ; (f) temps réel / jumeaux numériques. Sources privilégiées : textes réglementaires (US EPA, Federal Register), revues à comité de lecture, HAL/Zenodo, dépôts GitHub. Limite : le chapitre Springer 2008 n'est accessible qu'en extraits (paywall) ; l'analyse repose sur le texte fourni par l'auteur (p. 245–246) et le corpus compagnon.

## Limites de méthode et niveau de preuve\n\nCette version est une revue structurée, mais la méthode n'est pas encore entièrement reproductible : les chaînes de recherche exactes, dates par base, critères d'inclusion/exclusion, décomptes de sélection et évaluation formelle de la qualité des études ne sont pas consignés ici. Il faut compléter ces éléments avant de qualifier le travail de revue systématique. Certaines sources ne sont accessibles que par notice, résumé ou source secondaire ; ces limites doivent être prises en compte dans la force des conclusions. Les affirmations d'absence de concurrents et les avantages annoncés pour J-DriftX sont des hypothèses bornées par le corpus consulté, pas des preuves de nouveauté ou de supériorité. Voir aussi [le plan d'intégration et de validation](05-plan-validation-et-integration.md).\n\n## Résumé exécutif

1. **La recherche effectuée n'établit pas l'absence de travaux concurrents sur le temps de transport dirigé.** Les ROM recensées comprennent plusieurs familles, mais elles ne sont pas toutes équivalentes ni nécessairement fondées sur les mêmes données. La nouveauté de la formulation J-DriftX reste indéterminée tant qu'une recherche systématique des termes mathématiques et des travaux antérieurs n'a pas été menée.
2. **Un problème applicatif est documenté, mais l'avantage de J-DriftX n'en découle pas.** L'EPA décrit des incertitudes et un caractère potentiellement très conservateur pour des scénarios précis de l'extension gaussienne AGDISP. La modernisation AGDISP vise notamment à mieux représenter les conditions spécifiques aux sites, le terrain et les drones ; elle peut donc réduire ou modifier la lacune supposée et doit être suivie comme une alternative concurrente, non comme une validation de l'opportunité J-DriftX.
3. **Des méthodes complémentaires sont désormais bien développées**, notamment la réduction de modèle, l'assimilation et l'identification de source. Cela fournit des baselines et des outils potentiels, mais ne démontre ni l'équivalence avec Drift-X ni la valeur d'une reprise.
4. **La disponibilité de données météorologiques et géographiques s'est améliorée**, mais cela ne signifie pas que les données indépendantes de dépôt/concentration nécessaires à la validation soient abondantes, compatibles ou accessibles. L'identifiabilité et la calibration restent à démontrer pour un observable et un scénario définis.
5. **Conclusion provisoire : seule une investigation scientifique limitée est justifiée à ce stade.** Avant de construire un noyau applicatif ou de revendiquer une niche, il faut choisir un besoin et un observable, confirmer l'accès à des données indépendantes, formaliser les hypothèses et comparer à des baselines pertinentes. Le résultat peut être de poursuivre, de restreindre fortement le domaine, ou d'arrêter.

## Constats par thème

### 1. Modèles opérationnels et réglementaires : consolidation gaussienne, pas de rupture

- L'EPA a promulgué en novembre 2024 une révision complète de l'Appendix W (Guideline on Air Quality Models), centrée sur les améliorations d'AERMOD, effective janvier 2025 : le paysage réglementaire near-field reste gaussien stationnaire.
- CALPUFF, modèle préféré de 2003 à 2017, est désormais un modèle « alternatif » à justification cas par cas ; les comparatifs AERMOD/CALPUFF montrent des écarts d'un facteur 2 avec les mesures — l'incertitude des modèles opérationnels reste le problème central.
- Les revues récentes d'AERMOD documentent des hybridations (AERMOD + CMAQ pour l'emboîtement local/régional) et un couplage fort avec les SIG et la santé publique. Ces éléments montrent que les modèles opérationnels ont des domaines de validité et des incertitudes documentés ; ils ne démontrent pas à eux seuls que la formulation J-DriftX serait plus appropriée.

### 2. Dérive de pulvérisation : le domaine d'origine de Drift-X, en pleine ébullition

- Le couple réglementaire AgDRIFT/AGDISP (Lagrangien near-field ≤ 800 m + extension gaussienne far-field) domine toujours l'évaluation du risque. L'EPA reconnaît que l'extension gaussienne far-field est « extrêmement conservatrice » et peu validée pour les barrières végétales et la topographie — un scénario qui pourrait être étudié ; aucune preuve ne montre que la métrique travel-time de Drift-X représente correctement ces effets.
- L'**AGDISP Modernization Project** (AMP) lancé par l'industrie et rejoint par Bayer Crop Science (mars 2026) réécrit AGDISP en langage moderne, open source, pour intégrer agriculture de précision et conditions site-spécifiques. Un far-field rapide et réaliste y est une pièce manquante identifiée.
- Les drones (RPAAS/UASS) soulèvent des questions de validation spécifiques ; un article de 2025 évalue AGDISPpro dans ce contexte, et plusieurs travaux recensent des approches ML (random forest, ANN, SVR). Leurs contraintes physiques et leur extrapolation doivent être examinées méthode par méthode. Les sources recensées ne suffisent pas à conclure qu'une « case vide » existe pour un modèle mécaniste rapide.
- Côté européen, la Directive 2009/128/CE encadre l'aérien et les modèles type Costanzini et al. (2018) comparent un modèle de proximité et CAREA pour l'exposition résidentielle aux pesticides ; le modèle CAREA lui-même est décrit séparément par Teggi et al. (2018) — la qualité du modèle change les décisions sanitaires.

### 3. ROM et apprentissage : maturité méthodologique, mais toujours a posteriori

- Les ROM de dispersion urbaine comprennent plusieurs familles : Arnoldi (2015, facteur ~2500 vs CFD selon l'étude), ROM physique POD-NN (Bologne, 2024), POD-GPR (~50 snapshots LES selon la source), et ROM avec assimilation de données (2023). Une référence auparavant attribuée à un ROM POD+RBF sur 144 km² à Pékin (PII S2666449621000372) n'a pas encore été confirmée et n'est donc pas utilisée ici comme preuve.
- Les surrogate neuronaux montent en gamme : FNO pour panaches radioactifs (2024), architectures masquage/correction 3D (CEA, 2024, priors physiques + opérateurs neuronaux), surrogates ML d'émissions industrielles, et prévision d'accidents de type Seveso (publication en ligne en 2022, volume 2023).
- Certaines approches recensées utilisent des simulations haute-fidélité et des snapshots ; ce n'est pas une propriété universelle de toutes les ROM et méthodes de substitution. Leurs performances d'interpolation et d'extrapolation dépendent de la méthode, des données et du régime étudié. Le coût, la généralisation et le besoin d'entraînement de J-DriftX doivent être mesurés et comparés ; une extrapolation correcte n'est pas garantie par la seule construction analytique. Une architecture hybride reste une hypothèse à évaluer, pas un positionnement déjà justifié.

### 4. Identification de source (STE) : un champ qui s'est structuré

- La revue de référence (Information Fusion, 2017) classe les méthodes STE (optimisation, adjoint, bayésien, renormalisation) ; NARAC opérationalise le STE à toutes échelles ; la technique de renormalisation (JAMES, 2014) fournit le formalisme d'opérateur inverse généralisé.
- La ressource Zenodo de Shafiyev et al. publiée en 2026 synthétise des méthodes STE et mentionne des problèmes ouverts. Elle ne suffit pas, à elle seule, à établir l'état de l'art ni à justifier un modèle physique comme garde-fou ; les affirmations sur la régularisation sous données rares/bruitées et la détection hors domaine doivent être corroborées par les articles primaires cités.
- Les documents historiques mentionnent une analyse de sensibilité du modèle direct. La disponibilité, l'exactitude et l'utilité d'un adjoint pour la formulation actuelle ne sont pas démontrées par le seul caractère analytique du modèle ; elles doivent être dérivées et vérifiées.

### 5. SIG et open source : l'avenant de Drift-X est devenu banal — d'où l'exigence

- Des plugins QGIS gaussiens existent désormais (modèle GP QGIS intercompared 2026, plugin éducatif GitHub 2025, screening environnemental 2017) : l'intégration GIS n'est plus un différenciateur en soi, c'est un standard d'usage. Le différenciateur doit être **le modèle**, pas le couplage.
- Conséquence pour J-DriftX : architecture cœur Python pur (sans dépendance QGIS) + bindings/plugin QGIS en aval ; les sorties raster/vecteur géoréférencées sont attendues par défaut.

### 6. Tendances transverses : temps réel, jumeaux numériques, gouvernance

- Les jumeaux numériques de résilience urbaine (feu/fumée, 2025) et les sessions CBRNe 2026 plébiscitent la fusion capteurs + simulation + DSS temps réel, avec exigences explicites d'interprétabilité et de conformité (EU AI Act) : un modèle analytique contraint par la physique est un atout d'auditabilité face aux boîtes noires.
- Les prévisions météo temps réel (ECMWF) alimentent déjà la réponse CBRN opérationnelle : la chaîne « données météo ouvertes → modèle rapide → tableau de bord » est le format gagnant.

## Synthèse : positionnement de J-DriftX en 2026

| Dimension | État de l'art 2026 | Apport de J-DriftX |
|---|---|---|
| Réduction | Familles hétérogènes : ROM, surrogates, modèles analytiques et apprentissage | Hypothèse de réduction a priori par similitude, à formaliser et comparer |
| Coût | Coûts variables selon méthode, préparation, calibration et inférence | Coût complet et précision de J-DriftX non mesurés |
| Far-field dérive | L'EPA documente des limites dans des scénarios précis ; AGDISP est en cours de modernisation | Hypothèse de traitement du terrain et du transport dirigé à tester |
| Calibration | Assimilation/ML matures | Assimilation de données partielles (déjà dans Drift-X) à moderniser (bayésien) |
| STE | Plusieurs familles de méthodes inverses existent ; le choix dépend du problème | Applicabilité et calcul d'un adjoint pour J-DriftX à démontrer |
| SIG | Plugins QGIS gaussiens multiples | Cœur Python + plugin QGIS, standard attendu |

**Conclusion provisoire : les résultats de la revue justifient de poursuivre l'investigation, mais la nouveauté, la robustesse et la valeur prédictive de J-DriftX restent à démontrer par des benchmarks reproductibles.** L'idée n'a été ni reprise ni démentie ; le contexte applicatif (dérive far-field, drones, exposition résidentielle, réponse d'urgence auditable) s'est amélioré ; l'écosystème méthodologique (assimilation, STE, benchmarks) offre maintenant tout ce qui manquait en 2008 pour valider et publier proprement.

## Notes de sources

| Source | Crédibilité | Dernière mise à jour |
|---|---|---|
| [Federal Register — Appendix W / AERMOD (US EPA)](https://www.federalregister.gov/documents/2024/11/29/2024-27636/guideline-on-air-quality-models-enhancements-to-the-aermod-dispersion-modeling-system) | 5/5 | 2024-11-29 |
| [US EPA — Alternative Models (statut CALPUFF)](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models) | 5/5 | - |
| [US EPA — Guidance AGDISP-Gaussian Extension](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) | 5/5 | - |
| [AgAir Update — modernisation AGDISP / AMP](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/) | 3/5 | 2026-03-09 |
| [Sci. Total Environ. — validation AGDISPpro drones](https://www.sciencedirect.com/science/article/pii/S0048969725003596) | 4/5 | 2025 |
| [NCASI TB808 — historique AGDISP/AgDRIFT](https://ncasi.org/wp-content/uploads/2011/11/tb808.pdf) | 4/5 | 2007 |
| [HAL — ROM POD-GPR dispersion micro-échelle](https://hal.science/hal-04310899/document) | 4/5 | 2024 |
| [CMAME — ROM physique pollution urbaine](https://www.sciencedirect.com/science/article/abs/pii/S0045782523005406) | 4/5 | 2024 |
| [ResearchGate — ROM Arnoldi built environment](https://www.researchgate.net/publication/277338242_Stable_reduced-order_models_for_pollutant_dispersion_in_the_built_environment) | 3/5 | 2015 |
| [SERRA — surrogate FNO panache radioactif](https://link.springer.com/article/10.1007/s00477-024-02738-8) | 4/5 | 2024 |
| [CEA/HAL — MCxM 3D deep learning dispersion](https://cea.hal.science/cea-04810109/document) | 4/5 | 2024 |
| [SERRA — surrogate accidents Seveso](https://link.springer.com/article/10.1007/s00477-022-02288-x) | 4/5 | 2023 (en ligne 2022) |
| [Information Fusion — revue STE](https://www.sciencedirect.com/science/article/pii/S156625351630152X) | 5/5 | 2017 |
| [JAMES — renormalisation / STE](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014MS000385) | 4/5 | 2016 |
| [NARAC / LLNL — STE opérationnel](https://narac.llnl.gov/research-and-development/source-term-estimation) | 4/5 | - |
| [Shafiyev et al. — Source Term Estimation for Atmospheric Pollutant Releases](https://zenodo.org/records/22914336) | Ressource Zenodo ; évaluation par les pairs non établie ici | 2026-09-22 |
| [Appl. Sci. — modèle QGIS gaussien 2026](https://www.mdpi.com/2076-3417/16/4/1833) | 3/5 | 2026 |
| [GitHub — plugin QGIS éducatif gaussien](https://github.com/Sebapac90/qgis-educational-gaussian-plume) | 2/5 | 2025 |
| [Teggi et al. — modèle CAREA pour sources complexes](https://doi.org/10.1016/j.scitotenv.2017.07.196) | 4/5 | 2018 |
| [Costanzini et al. — exposition aux pesticides avec CAREA](https://doi.org/10.3390/atmos9020038) | 4/5 | 2018 |
| [PMC — digital twin urbain feu/fumée](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/) | 3/5 | 2025 |
| [SICC 2026 — session IA/Digital Twins CBRNe](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/) | 3/5 | 2026 |
| [EM-Consulte — CR Mécanique 334 (Mohammadi & Brun)](https://www.em-consulte.com/article/69927) | 5/5 | 2006 |
| [HAL — Drift-X / GIS-based model](https://hal.science/hal-00468863) | 4/5 | 2009 |
| [Springer — chapitre Brun & Mohammadi 2008](https://link.springer.com/chapter/10.1007/978-1-4020-8758-5_14) | 5/5 | 2008 |

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
