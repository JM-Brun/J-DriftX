# SIG, exposition et applications de la dispersion

## Rapport avec J-DriftX

Ces références décrivent les contextes d'application, l'exposition environnementale, les outils SIG et les usages en temps réel. Elles sont utiles pour choisir les sorties et les validations aval, mais **l'intégration SIG n'est pas en soi une preuve de nouveauté du modèle**.

### InVS / Santé publique France (2009) — exposition aérienne aux pesticides dans l'Hérault

- **Type :** rapport d'agence sanitaire, étude de mesures de terrain.
- **Relation :** source de contexte empirique proche du domaine d'origine de Drift-X ; potentiellement pertinente pour concevoir un protocole de calibration/validation si les données détaillées sont accessibles et compatibles.
- **Conséquence :** vérifier la granularité spatiale et temporelle, les métadonnées, les unités et les conditions météorologiques ; ne pas supposer que les données agrégées suffisent à valider le modèle.
- [Rapport PDF](https://www.santepubliquefrance.fr/content/download/186474/document_file/82748_9958-9958-ps.pdf)

### CAREA (2018) — dispersion et exposition résidentielle aux pesticides

- **Relation :** application proche par le thème de l'exposition et la modélisation spatiale.
- **Intuition commune :** transformer une source d'émission en distribution de concentration/exposition sur un territoire.
- **Différence à examiner :** modèles physiques, représentation des sources, hypothèses météorologiques et validation.
- [Article](https://www.sciencedirect.com/science/article/abs/pii/S0048969717318995)

### Modèle de panache gaussien dans QGIS (2026)

- **Type :** article recensé dans *Applied Sciences*.
- **Relation :** baseline de visualisation/intégration pour un cas simple de source ponctuelle ; concurrent seulement sur les configurations et sorties effectivement communes.
- **Conséquence :** comparer les prédictions du noyau avant d'évaluer l'interface SIG.
- [Article](https://www.mdpi.com/2076-3417/16/4/1833)

### Plugin QGIS éducatif de panache gaussien (2025)

- **Type :** dépôt logiciel pédagogique, pas article évalué par les pairs.
- **Relation :** référence d'architecture et d'ergonomie potentielle, non validation scientifique.
- [Dépôt GitHub](https://github.com/Sebapac90/qgis-educational-gaussian-plume)

### Plugin SIG pour le screening environnemental (ISPRS, 2017)

- **Type :** publication d'application SIG.
- **Relation :** analogue sur l'intégration géospatiale et le screening ; les milieux et processus modélisés peuvent différer.
- **Conséquence :** s'en inspirer pour la traçabilité des couches et des unités, sans extrapoler les résultats physiques.
- [Article/PDF](https://iris.unitn.it/retrieve/handle/11572/184964/151989/isprs-archives-XLII-4-W2-79-2017.pdf)

### Muller (1979) — distances-temps en géographie

- **Type :** article théorique/appliqué dans *L'Espace géographique*.
- **Relation :** analogie conceptuelle pour une métrique non euclidienne ou une représentation de l'espace par temps de déplacement ; domaine distinct de la mécanique des fluides.
- **Intuition commune :** la notion de proximité peut être définie par le temps de trajet plutôt que par la distance euclidienne.
- **Limite :** analogie mathématique, pas validation de la pseudo-distance de Drift-X ni preuve d'équivalence.
- [Article](https://www.persee.fr/doc/spgeo_0046-2497_1979_num_8_3_1915)

### Jumeaux numériques et réponse aux incidents (2025–2026)

- **Références :** FireCom, digital risk twins et session SICC CBRNe recensés dans [la bibliographie générale](../references.md).
- **Relation :** contexte d'usage pour la simulation rapide, la fusion de données et l'aide à la décision ; méthodes et domaines parfois différents.
- **Conséquence :** ne retenir ces références que pour des exigences opérationnelles explicitement liées au cas d'usage ; elles ne démontrent pas la précision du noyau J-DriftX.

### Jumeaux numériques et réponse aux incidents

- **FireCom (2025) — jumeau numérique urbain feu/fumée.** Analogie d'application autour de la simulation rapide, des données et du contexte urbain ; le phénomène physique n'est pas la dérive de pulvérisation. [Article PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/)
- **Digital risk twin for disaster risk management (2025).** Référence de contexte sur les jumeaux numériques, l'IoT, la télédétection et l'aide à la décision. À retenir pour les exigences de chaîne de données, pas comme preuve pour le modèle physique. [Article](https://www.nature.com/articles/s44304-025-00135-x)
- **ECMWF — prévisions en temps réel pour la dispersion CBRN.** Ressource institutionnelle sur l'intégration de prévisions météo à une chaîne de modélisation opérationnelle ; utile pour cadrer les dépendances d'entrée et les contraintes de latence. [Document](https://events.ecmwf.int/event/211/contributions/1871/attachments/989/1737/Cloud-WS_Carion.pdf)
- **SICC (2026) — IA, jumeaux numériques et aide à la décision CBRNe.** Programme de conférence, pas article scientifique évalué par les pairs ; à utiliser comme signal de contexte seulement. [Session](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/)
