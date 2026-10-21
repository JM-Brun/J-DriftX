# Revue de l'état de l'art — dispersion atmosphérique à complexité réduite (2008 → 2026)

> Revue systémique établie en octobre 2026 pour décider de la reprise du projet Drift-X sous le nom **J-DriftX**.
> Toutes les sources citées sont listées dans [references.md](references.md) ; ce document n'utilise que des sources inspectées (résumés, notices, textes ouverts).

## Question de recherche

Le modèle Drift-X (2006–2009) reposait sur quatre paris : (1) une dispersion prédictible par solutions de similitude **généralisées dans une métrique non symétrique de temps de transport**, (2) sans résoudre d'EDP ni mailler, (3) calibrée par assimilation de données partielles, (4) utile pour la dérive de pesticides et l'identification de source. **Ces paris sont-ils toujours pertinents, concurrencés, dépassés ou confirmés par l'état de l'art de 2026 ? La reprise a-t-elle du sens ?**

## Méthodologie

Angles de recherche : (a) modèles opérationnels et réglementaires de dispersion ; (b) dérive de pulvérisation ; (c) ROM et apprentissage (POD, opérateurs neuronaux, surrogates) ; (d) identification de source / STE ; (e) SIG et open source ; (f) temps réel / jumeaux numériques. Sources privilégiées : textes réglementaires (US EPA, Federal Register), revues à comité de lecture, HAL/Zenodo, dépôts GitHub. Limite : le chapitre Springer 2008 n'est accessible qu'en extraits (paywall) ; l'analyse repose sur le texte fourni par l'auteur (p. 245–246) et le corpus compagnon.

## Résumé exécutif

1. **Aucun modèle concurrent n'a repris l'idée de la métrique travel-time.** Les ROM modernes (POD-GPR, POD-NN, Arnoldi) restent toutes construites *a posteriori* à partir de snapshots CFD/LES coûteux : la niche « réduction a priori par la physique » reste ouverte.
2. **Le besoin applicatif s'est renforcé.** L'extension gaussienne du couple AGDISP (far-field) est officiellement jugée « extrêmement conservatrice » par l'EPA, et le régulateur lui-même lance (2026) une modernisation open source d'AGDISP — une fenêtre d'opportunité directe pour un far-field à complexité réduite.
3. **Les prémisses « assimilation + physique » de Drift-X sont devenues mainstream** (ROM + data assimilation, surrogate physics-informed, STE par méthodes d'adjoint/bayésiennes) : la reprise peut capitaliser sur un écosystème méthodologique mature.
4. **Le contexte données a changé du tout au tout** (ERA5/Copernicus, MNT ouverts, capteurs low-cost, drones) : les verrous de 2006 (données rares) ont disparu, ce qui rend la calibration par assimilation bien plus crédible.
5. **Verdict : oui, la reprise a du sens**, à condition de (i) publier d'abord des benchmarks de validation publics, (ii) livrer un noyau Python/QGIS moderne, (iii) positionner l'article de synthèse sur la niche far-field + réduction a priori, où la concurrence est la plus faible.

## Constats par thème

### 1. Modèles opérationnels et réglementaires : consolidation gaussienne, pas de rupture

- L'EPA a promulgué en novembre 2024 une révision complète de l'Appendix W (Guideline on Air Quality Models), centrée sur les améliorations d'AERMOD, effective janvier 2025 : le paysage réglementaire near-field reste gaussien stationnaire.
- CALPUFF, modèle préféré de 2003 à 2017, est désormais un modèle « alternatif » à justification cas par cas ; les comparatifs AERMOD/CALPUFF montrent des écarts d'un facteur 2 avec les mesures — l'incertitude des modèles opérationnels reste le problème central.
- Les revues récentes d'AERMOD documentent des hybridations (AERMOD + CMAQ pour l'emboîtement local/régional) et un couplage fort avec les SIG et la santé publique. **Aucune remise en cause du paradigme : le besoin de modèles rapides à contraintes physiques demeure.**

### 2. Dérive de pulvérisation : le domaine d'origine de Drift-X, en pleine ébullition

- Le couple réglementaire AgDRIFT/AGDISP (Lagrangien near-field ≤ 800 m + extension gaussienne far-field) domine toujours l'évaluation du risque. L'EPA reconnaît que l'extension gaussienne far-field est « extrêmement conservatrice » et peu validée pour les barrières végétales et la topographie — **exactement la cible de la métrique travel-time de Drift-X**.
- L'**AGDISP Modernization Project** (AMP) lancé par l'industrie et rejoint par Bayer Crop Science (mars 2026) réécrit AGDISP en langage moderne, open source, pour intégrer agriculture de précision et conditions site-spécifiques. Un far-field rapide et réaliste y est une pièce manquante identifiée.
- L'arrivée des drones (RPAAS/UASS) crée un besoin nouveau de modèles de dérive validés : AGDISPpro est en cours de validation pour les drones (2025), et les approches ML (random forest, ANN, SVR) se multiplient pour la dérive — toutes statistiques, sans contraintes physiques, donc fragiles en extrapolation. **La dérive « mécaniste rapide » reste une case vide.**
- Côté européen, la Directive 2009/128/CE encadre l'aérien et les modèles type CAREA (2018) couplent dispersion gaussienne et SIG pour l'exposition résidentielle aux pesticides, avec des écarts d'exposition très importants selon le modèle utilisé — la qualité du modèle change les décisions sanitaires.

### 3. ROM et apprentissage : maturité méthodologique, mais toujours a posteriori

- Les ROM de dispersion urbaine se sont standardisées : Arnoldi (2015, facteur ~2500 vs CFD), POD+RBF sur 144 km² (Pékin, 2021), ROM physique POD-NN (Bologne, 2024, avec vent réel pour le monitoring temps réel), POD-GPR avec ~50 snapshots LES (2024), ROM + assimilation de données (2023).
- Les surrogate neuronaux montent en gamme : FNO pour panaches radioactifs (2024), architectures masquage/correction 3D (CEA, 2024, priors physiques + opérateurs neuronaux), surrogates ML d'émissions industrielles, prévision d'accidents Seveso (2022).
- **Point commun à toutes ces approches : elles exigent un modèle haute-fidélité (CFD/LES) et des snapshots pour exister.** Elles excellent en interpolation dans leur domaine d'entraînement mais leur faiblesse déclarée est la généralisation hors domaine (identifiée comme problème ouvert dans la revue STE 2025). La réduction a priori de Drift-X est précisément complémentaire : coût indépendant du domaine, extrapolation par construction, pas d'entraînement requis. **Positionnement naturel : hybride — Drift-X comme prior physique et modèle d'évaluation ponctuelle, ML pour la calibration.**

### 4. Identification de source (STE) : un champ qui s'est structuré

- La revue de référence (Information Fusion, 2017) classe les méthodes STE (optimisation, adjoint, bayésien, renormalisation) ; NARAC opérationalise le STE à toutes échelles ; la technique de renormalisation (JAMES, 2016) fournit le formalisme d'opérateur inverse généralisé.
- La revue 2025 (Zenodo) confirme deux problèmes ouverts : la régularisation automatique sous données rares et bruitées, et **la détection du fonctionnement hors domaine d'un surrogate ML** — argument supplémentaire pour un modèle physique rapide servant de garde-fou.
- Drift-X avait intégré l'identification de source via analyse de sensibilité du modèle direct ; la reprise peut s'aligner sur les standards STE (adjoint du modèle de transport travel-time = naturellement disponible, puisque le modèle est analytique).

### 5. SIG et open source : l'avenant de Drift-X est devenu banal — d'où l'exigence

- Des plugins QGIS gaussiens existent désormais (modèle GP QGIS intercompared 2026, plugin éducatif GitHub 2025, screening environnemental 2017) : l'intégration GIS n'est plus un différenciateur en soi, c'est un standard d'usage. Le différenciateur doit être **le modèle**, pas le couplage.
- Conséquence pour J-DriftX : architecture cœur Python pur (sans dépendance QGIS) + bindings/plugin QGIS en aval ; les sorties raster/vecteur géoréférencées sont attendues par défaut.

### 6. Tendances transverses : temps réel, jumeaux numériques, gouvernance

- Les jumeaux numériques de résilience urbaine (feu/fumée, 2025) et les sessions CBRNe 2026 plébiscitent la fusion capteurs + simulation + DSS temps réel, avec exigences explicites d'interprétabilité et de conformité (EU AI Act) : un modèle analytique contraint par la physique est un atout d'auditabilité face aux boîtes noires.
- Les prévisions météo temps réel (ECMWF) alimentent déjà la réponse CBRN opérationnelle : la chaîne « données météo ouvertes → modèle rapide → tableau de bord » est le format gagnant.

## Synthèse : positionnement de J-DriftX en 2026

| Dimension | État de l'art 2026 | Apport de J-DriftX |
|---|---|---|
| Réduction | POD/ML a posteriori, dépendantes de snapshots CFD | Réduction a priori par similitude, sans EDP ni entraînement |
| Coût | ROM: évaluation rapide après entraînement coûteux | Évaluation ponctuelle à coût quasi nul, Monte Carlo massif |
| Far-field dérive | Extension gaussienne AGDISP très conservatrice, AMP en cours | Similitude généralisée + topographie via métrique travel-time |
| Calibration | Assimilation/ML matures | Assimilation de données partielles (déjà dans Drift-X) à moderniser (bayésien) |
| STE | Méthodes standardisées (adjoint/bayésien) | Adjoint analytique disponible par construction |
| SIG | Plugins QGIS gaussiens multiples | Cœur Python + plugin QGIS, standard attendu |

**Conclusion de la revue : la reprise est scientifiquement justifiée.** L'idée n'a été ni reprise ni démentie ; le contexte applicatif (dérive far-field, drones, exposition résidentielle, réponse d'urgence auditable) s'est amélioré ; l'écosystème méthodologique (assimilation, STE, benchmarks) offre maintenant tout ce qui manquait en 2008 pour valider et publier proprement.

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
| [SERRA — surrogate accidents Seveso](https://link.springer.com/article/10.1007/s00477-022-02288-x) | 4/5 | 2022 |
| [Information Fusion — revue STE](https://www.sciencedirect.com/science/article/pii/S156625351630152X) | 5/5 | 2017 |
| [JAMES — renormalisation / STE](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014MS000385) | 4/5 | 2016 |
| [NARAC / LLNL — STE opérationnel](https://narac.llnl.gov/research-and-development/source-term-estimation) | 4/5 | - |
| [Zenodo — revue STE 2025 (adjoint, Tikhonov, PINN)](https://zenodo.org/records/22914336) | 3/5 | 2025 |
| [Appl. Sci. — modèle QGIS gaussien 2026](https://www.mdpi.com/2076-3417/16/4/1833) | 3/5 | 2026 |
| [GitHub — plugin QGIS éducatif gaussien](https://github.com/Sebapac90/qgis-educational-gaussian-plume) | 2/5 | 2025 |
| [Sci. Total Environ. — CAREA, exposition pesticides](https://www.sciencedirect.com/science/article/abs/pii/S0048969717318995) | 4/5 | 2018 |
| [PMC — digital twin urbain feu/fumée](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/) | 3/5 | 2025 |
| [SICC 2026 — session IA/Digital Twins CBRNe](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/) | 3/5 | 2026 |
| [EM-Consulte — CR Mécanique 334 (Mohammadi & Brun)](https://www.em-consulte.com/article/69927) | 5/5 | 2006 |
| [HAL — Drift-X / GIS-based model](https://hal.science/hal-00468863) | 4/5 | 2009 |
| [Springer — chapitre Brun & Mohammadi 2008](https://link.springer.com/chapter/10.1007/978-1-4020-8758-5_14) | 5/5 | 2008 |

**Conflits et réserves** : les évaluations de CALPUFF vs AERMOD divergent selon les études (meilleure corrélation CALPUFF sur les tracer studies, mais facteurs 2 d'écart résiduels) ; les sources presse spécialisée (AgAir Update) sont à reconfirmer par les publications de l'AMP ; la revue Zenodo 2025 n'a pas été évaluée par comité de lecture à notre connaissance.

## Questions ouvertes

1. La métrique travel-time a-t-elle déjà été formalisée de façon autonome (thèse 2006) ? Le document original doit être numérisé/déposé sur HAL pour servir de référence — action M0 de la roadmap.
2. Quel niveau d'accord (facteur 2 ? erreur L2 ?) viser sur les benchmarks far-field pour convaincre la communauté spray drift, sachant que les modèles réglementaires eux-mêmes vivent avec des facteurs 2 ?
3. Faut-il viser la conformité aux standards d'entrée AERMOD/AgDRIFT (météo au format météorologique réglementaire) pour l'interopérabilité ?
4. La calibration bayésienne (au lieu des moindres carrés) vaut-elle le coût en complexité au stade M1, ou est-ce un M2/M3 ?

## Recommandations

1. **Reprendre le projet** — la niche scientifique est intacte et le contexte applicatif favorable.
2. Prioriser M1 : noyau Python + benchmark gaussien classique (reproductibilité) avant toute extension.
3. Suivre l'AGDISP Modernization Project et proposer, à terme, le far-field J-DriftX comme extension — c'est le chemin d'impact maximal.
4. Déposer les documents historiques (thèse, chapitre) en archive ouverte pour ancrer l'antériorité.
5. Cibler une revue type *Atmospheric Environment* / *Environmental Modelling & Software* pour l'article de synthèse v2.
