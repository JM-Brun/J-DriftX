# Dérive de pulvérisation et modèles opérationnels

## Rapport avec J-DriftX

Ces sources décrivent les modèles établis, les pratiques réglementaires, les cas d'usage et les lacunes de validation du domaine de la dérive de pulvérisation. Elles constituent surtout des **références de contexte et des baselines applicatives** ; elles ne prouvent pas, à elles seules, qu'une méthode est concurrente directe du modèle de similitude de J-DriftX.

### US EPA — *Guidance on the Use of the Linked AGDISP-Gaussian Extension Models for Far-Field Drift*

- **Type :** guide réglementaire/technique, pas article de recherche classique.
- **Lien :** contexte opérationnel et source de contraintes de validation.
- **Idées :** couplage AGDISP et extension gaussienne pour la dérive lointaine ; limites déclarées pour certains contextes.
- **Conséquence :** construire un benchmark far-field documenté avec hypothèses, unités, conditions météorologiques et métriques communes.
- **À vérifier :** formulation exacte des réserves de l'EPA et périmètre des cas couverts.
- [Source EPA](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension)

### NCASI (2007) — Technical Bulletin 808

- **Type :** bulletin technique.
- **Lien :** contexte historique des modèles AGDISP/AgDRIFT et du Spray Drift Task Force.
- **Conséquence :** documenter l'usage historique et les scénarios de référence ; ne pas traiter un bulletin technique comme une validation indépendante sans examiner sa méthode.
- [Document](https://ncasi.org/wp-content/uploads/2011/11/tb808.pdf)

### US EPA (2014) — *Pesticides; Consideration of Spray Drift in Pesticide Risk Assessment*

- **Type :** avis/texte réglementaire.
- **Lien :** cadre d'utilisation des modèles de dérive dans l'évaluation du risque.
- **Conséquence :** préciser l'usage cible de J-DriftX et la différence entre recherche, screening et prédiction réglementaire.
- [Federal Register](https://www.federalregister.gov/documents/2014/01/29/2014-01234/pesticides-consideration-of-spray-drift-in-pesticide-risk-assessment-notice-of-availability-and)

### Études de validation d'AGDISPpro pour les drones (2025) et de dérive par systèmes aériens sans équipage (2024)

- **Type :** articles de recherche dans *Science of the Total Environment*.
- **Lien :** applications proches et jeux de validation potentiels, mais le régime de pulvérisation par drone peut différer de la configuration historique de Drift-X.
- **Conséquence :** utiliser comme pistes de jeux de données/conditions expérimentales seulement après vérification de l'accès aux données, des variables et du protocole.
- [Validation AGDISPpro (2025)](https://www.sciencedirect.com/science/article/pii/S0048969725003596)
- [Évaluation spray drift UASS (2024)](https://www.sciencedirect.com/science/article/abs/pii/S0048969724033606)

### Modèles ML de dérive de pulvérisation (2022–2024)

Références recensées dans le dépôt : ANN/SVR, random forest et analyse de sensibilité par ANN.

- **Lien :** approches statistiques potentiellement concurrentes sur certaines sorties, mais pas nécessairement sur les mêmes régimes, entrées ou contraintes physiques.
- **Intuition commune :** apprendre rapidement une relation entrée-sortie à partir d'observations ou de simulations.
- **Différence à tester :** capacité d'extrapolation, cohérence physique, besoin de données d'entraînement et coût de construction.
- **Conséquence :** ne pas comparer un modèle appris à un modèle analytique sur des jeux de données différents ; utiliser mêmes splits, mêmes observables et mêmes budgets.
- [ANN/SVR (2022)](https://link.springer.com/article/10.1007/s11356-022-23571-y)
- [Analyse de sensibilité par ANN (2023)](https://link.springer.com/article/10.1007/s10668-023-04452-x)
- [Machine learning for spraying factors (2024)](https://doi.org/10.3390/agronomy14091977)

### Bonicelli et al. (2012) — Ongoing research on pesticides air dispersion

- **Type :** actes de conférence (CIGR-AgEng 2012, Valencia, 6 p.), texte intégral libre sur HAL.
- **Lien :** continuation de la lignée pesticides du corpus — C. Sinfort est co-auteure des papiers Drift-X ; état de la recherche en début des années 2010.
- **Conséquence :** vérifier le recouvrement avec les papiers Drift-X avant d'en faire une source d'exigences ; statut de conférence, pas d'article de revue.
- [Document HAL](https://hal.science/hal-00825458/document)

### Defra PS2024 (2011) — exposition des riverains en arboriculture

- **Type :** rapport final Defra (SID 5), littérature grise publique ; contractants The Arable Group / Silsoe Spray Applications Unit (projet 01/06/2010–31/03/2011).
- **Lien :** cas d'usage far-field direct — évaluation de l'exposition bystanders/résidents lors de pulvérisations en verger, houblon et petits fruits ; proposition d'un modèle d'exposition à développer.
- **Conséquence :** source de cadrage du besoin applicatif et des scénarios d'exposition ; à ne pas traiter comme validation d'un modèle. Lecture intégrale requise avant d'en extraire des exigences.
- [Rapport (archive Natural England)](https://naturalengland.contentdm.oclc.org/digital/api/collection/p21006coll3/id/2458/download)


### CAREA (2018) — modèle SIG de dispersion pour l'exposition résidentielle aux pesticides

- **Type :** étude applicative, *Science of the Total Environment*.
- **Lien :** application de dispersion/exposition et intégration spatiale ; possible contexte pour les sorties de J-DriftX.
- **Conséquence :** examiner les sources d'émission, la topographie, la résolution spatiale et la chaîne de calcul avant d'en faire une baseline.
- [Costanzini et al. (2018), *Atmosphere* 9(2), 38 — exposition aux pesticides](https://doi.org/10.3390/atmos9020038)

### AGDISP Modernization Project (2026)

- **Type :** initiative logicielle/industrielle, pas article évalué par les pairs.
- **Lien :** évolution de l'écosystème et opportunité d'interopérabilité, non preuve scientifique.
- **Conséquence :** suivre l'état réel du projet, ses licences, ses benchmarks et son périmètre ; ne pas affirmer que J-DriftX serait une « pièce manquante » sans source primaire.
- [Article de presse sectorielle (à confirmer par sources primaires)](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/)

## Prochaines vérifications

- Lire intégralement les publications de recherche lorsqu'elles sont accessibles.
- Relever les conditions de validation, les données ouvertes, les erreurs et les limites.
- Distinguer modèle réglementaire, étude de terrain, article de méthode et annonce de projet logiciel.
- Définir une baseline avant d'implémenter une nouvelle méthode.

### Modèles de qualité de l'air : AERMOD, CALPUFF et revues d'application

- **US EPA (2024), Appendix W / AERMOD.** Source réglementaire primaire sur le cadre de modélisation de la qualité de l'air aux États-Unis ; utile pour comprendre les exigences et limites du contexte opérationnel, mais pas une baseline automatiquement comparable au spray drift. [Federal Register](https://www.federalregister.gov/documents/2024/11/29/2024-27636/guideline-on-air-quality-models-enhancements-to-the-aermod-dispersion-modeling-system)
- **US EPA — Alternative Models.** Source institutionnelle sur le statut de CALPUFF et d'autres modèles alternatifs. À utiliser pour vérifier le statut réglementaire à jour, pas pour inférer une performance universelle. [EPA](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models)
- **Shafie et al. — revue d'AERMOD en environnement complexe.** Revue secondaire sur les applications, hybridations et liens avec la santé publique. Elle sert au cadrage du paysage des modèles ; les conclusions méthodologiques doivent être remontées aux études primaires citées. [Revue](https://rsisinternational.org/journals/ijriss/articles/aermod-in-air-pollution-modeling-for-complex-environment-a-comprehensive-review-of-global-and-regional-applications-technological-integrations-health-risk-assessments-and-policy-implications/)
