# G0 — Compléter le cadrage à partir de preuves externes

> **État au 22 octobre 2026.** Recherche documentaire ciblée, non revue systématique. Les sources établissent l'existence de problèmes de mesure et d'évaluation de la dérive ; elles ne démontrent pas que J-DriftX y apporte une solution.

## Décision provisoire

**G0 n'est pas franchi.** Ne pas commencer un benchmark applicatif ni présenter le far-field comme cas d'usage retenu. Deux éléments sont maintenant plus clairs :

1. Il existe des décisions concrètes liées à la dérive de pulvérisation (évaluation d'exposition, distances tampons, évaluation de matériels de réduction de dérive).
2. Le jeu de données ouvert identifié est principalement adapté à l'étude de dérive de proximité, pas à la validation du far-field à plusieurs kilomètres. Le décalage entre le phénomène mesuré et les hypothèses physiques du modèle reste à résoudre.

La question de recherche doit donc être formulée indépendamment de la méthode : **quelle grandeur, pour quelle décision, dans quel régime physique, n'est-elle pas suffisamment prédite par une méthode existante, et quelles données permettent de tester cette lacune ?**

## 1. Besoin et décision utilisateur : ce que les sources soutiennent

### Évaluation réglementaire et exposition

L'EPA utilise des modèles atmosphériques pour estimer les dépôts hors site de pesticides. Sa page de modèles décrit AgDRIFT (v2.1.1) pour différentes applications agricoles et AGDISP (v8.26) pour la dérive depuis des sites d'application, notamment en aérien et en rampe au sol. [EPA — Models for Pesticide Risk Assessment](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment).

L'EPA a documenté des incertitudes spécifiques à l'extension gaussienne d'AGDISP au-delà de 0,5 mile, une validation limitée au-delà de 2 miles et des limites relatives aux barrières et à la météorologie. Son guide restreint toutefois l'usage discuté à certains scénarios de pulvérisation aérienne. [EPA — Guidance on the linked AGDISP-Gaussian Extension Models](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension).

Ces sources justifient une question ciblée sur certains scénarios d'exposition lointaine. Elles ne montrent pas que :
- les décisions réglementaires concernées gagneraient à des estimations moins conservatrices ;
- le cas s'applique aux pulvérisations terrestres, aux drones ou à tous les produits ;
- une méthode à temps de transport dirigé reproduirait les mécanismes physiques manquants ;
- un nouvel outil pourrait être utilisé réglementairement sans validation dédiée.

### Décision en France

Le ministère français indique que les zones non traitées (ZNT) et certaines distances de sécurité sont encadrées par l'arrêté du 4 mai 2017 ; les réductions de certaines ZNT reposent notamment sur l'utilisation de matériels figurant sur une liste officielle et sur des conditions d'efficacité définies. Le dossier d'inscription de matériel inclut des résultats d'essais ou des justificatifs d'analogie. [Ministère de l'Agriculture — matériels permettant de limiter la dérive](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques).

**Implication :** il existe un besoin décisionnel réel autour de la dérive, mais ce n'est pas une preuve que le modèle de dispersion J-DriftX est le bon outil. Pour viser cette décision, il faudrait d'abord déterminer si le livrable attendu est une courbe de dépôt, un facteur de réduction, une distance tampon ou une exposition, et quelles exigences de preuve s'appliquent. La conformité réglementaire n'est pas un objectif raisonnable pour le premier benchmark.

## 2. Données ouvertes identifiées : CAPRIV

Le jeu [Drift data from French CAPRIV project](https://doi.org/10.57745/Z8OJ3A) est disponible sur Recherche Data Gouv. La table de cultures de plein champ contient 3 792 observations/collecteurs et 38 variables ; le dépôt comprend aussi des données de viticulture et d'arboriculture. [Dépôt de données](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FZ8OJ3A).

Le papier de données décrit :
- des essais en France en 2021–2022 ;
- des applications sur blé, avec et sans haie selon l'année ;
- trois types de collecteurs : boîtes de Petri pour le dépôt sédimentaire, fils PVC pour la dérive aérienne, et vêtements sur mannequins pour l'exposition cutanée potentielle ;
- pour les boîtes de Petri, des distances de 1, 2, 3, 5, 10 et 20 m sans haie et de 1, 5, 10, 15, 20 et 25 m avec haie ; les fils PVC de mesure de dérive aérienne sont situés à 5 m ;
- des paramètres d'application, des indicateurs météorologiques et des fichiers de données météo brutes.

Source : Perriot et al. (2024), [*Spray drift in field crops*](https://doi.org/10.1016/j.dib.2024.110366), article en accès ouvert ; les données sont accessibles depuis le dépôt cité ci-dessus.

### Adéquation des données au projet

| Question | Évaluation actuelle | Motif |
|---|---|---|
| Données accessibles pour un test reproductible ? | **Oui, en principe** | Dépôt public, tables et documentation ; vérifier les fichiers, unités, droits et complétude avant analyse. |
| Données de dépôt au sol ? | **Oui** | Collecteurs de dépôt avec indicateur normalisé. |
| Données de dérive aérienne ? | **Oui, mais dispositif localisé** | Fils PVC à 5 m ; ne pas confondre cette mesure avec une concentration atmosphérique continue. |
| Validation far-field à plusieurs kilomètres ? | **Non démontrée** | Les distances décrites sont de l'ordre de quelques dizaines de mètres. |
| Validation indépendante suffisante ? | **Pas établie** | Plusieurs milliers de collecteurs ne signifient pas plusieurs milliers d'essais indépendants : les mesures sont regroupées par essai, site, date et conditions d'application. |
| Adéquation à un modèle de scalaire passif ? | **Incertaine** | Le dépôt de gouttelettes dépend de leur taille, de la sédimentation, de l'évaporation, de l'écoulement induit et de la collecte ; il ne s'identifie pas automatiquement au transport d'un scalaire passif. |

CAPRIV est donc une **source utile pour caractériser un cas proche et analyser la disponibilité réelle des variables**, mais pas une preuve que J-DriftX peut prédire la dérive far-field. Un test sur CAPRIV pourrait servir à examiner un cas adjacent uniquement après avoir justifié la correspondance entre les équations du modèle et les observables.

### Risque de fuite et unité statistique

Il serait incorrect de répartir aléatoirement les collecteurs individuels entre entraînement et test : des collecteurs du même essai partageraient les conditions météo, les réglages et la configuration. Toute évaluation doit grouper les partitions par essai (et, si le nombre d'essais le permet, par date/site/scénario). Les variables disponibles et les identifiants de groupes doivent être inspectés avant de définir le protocole. Le nombre de collecteurs ne doit pas être présenté comme la taille effective de l'échantillon indépendant.

## 3. Pourquoi les validations publiées des modèles existants comptent

L'évaluation d'AgDRIFT par Bird et al. compare 161 essais de terrain ; elle rapporte une réponse conforme aux observations pour plusieurs variables d'application, une surestimation dans certains cas far-field, et un bon accord pour certaines zones tampons de proximité. [Bird et al. (2002), DOI 10.1002/etc.5620210328](https://doi.org/10.1002/etc.5620210328).

L'évaluation d'AGDISPpro publiée en 2025 porte sur 18 applications de drones et rapporte un accord variable selon les buses et scénarios ; les données sont disponibles sur demande, selon l'article. [Castro-Tanzi et al. (2025), DOI 10.1016/j.scitotenv.2025.178725](https://doi.org/10.1016/j.scitotenv.2025.178725).

Ces résultats n'établissent pas que les modèles existants sont suffisants partout. Ils montrent qu'une comparaison utile doit :
- préciser le régime d'application et la version du modèle ;
- comparer les mêmes observables et informations d'entrée ;
- distinguer calibration, validation et test final ;
- expliquer en quoi un écart améliore une décision plutôt que de simplement produire une courbe différente.

## 4. Fiche G0 mise à jour

| Champ G0 | État actuel | Preuve manquante / prochaine action |
|---|---|---|
| Phénomène | Dérive de pulvérisation et transport atmosphérique | Délimiter gouttelettes vs phase vapeur/scalaires passifs. |
| Observable primaire | **Non choisi** | Choisir une seule cible : dépôt au sol, concentration/flux aérien, ou autre. |
| Utilisateur | **Non identifié** | Distinguer évaluateur de risque, autorité réglementaire, chercheur ou développeur de modèle. |
| Décision | Exposition et zones tampons sont des exemples documentés | Identifier une décision précise et le coût des faux positifs/faux négatifs. |
| Scénario | Far-field proposé, non confirmé | Définir mode d'application, distance, météo, terrain, végétation et taille de gouttelettes. |
| Baseline | AgDRIFT/AGDISP sont des candidats selon le scénario | Choisir la version et vérifier qu'elle traite le même régime. Inclure une baseline simple si pertinente, mais pas seule. |
| Données | CAPRIV accessible ; pertinence limitée au near-field | Trouver des données correspondant au scénario choisi et documenter les modalités d'accès. |
| Indépendance | Non établie | Partitionner par essais/scénarios ; rechercher des données d'évaluation non utilisées pour la formulation ou calibration. |
| Seuil de succès | **Non défini** | Fixer métrique, tolérance d'erreur, coût complet et gain décisionnel avant le benchmark. |
| Critère d'arrêt | À préciser | Arrêter le cas pratique si observable, utilisateur, données ou baseline ne peuvent être justifiés. |

## 5. Décision et prochaines étapes

### Décision provisoire

**Ne pas lancer le benchmark far-field sur la base de CAPRIV.** Le jeu est ouvert et pertinent pour la dérive proche, mais ses distances et son dispositif ne couvrent pas le far-field décrit par l'EPA. Il y a en plus une question de compatibilité physique entre la modélisation de scalaire passif et le dépôt de gouttelettes.

### Actions minimales, dans l'ordre

1. **Audit des données CAPRIV sans entraîner de modèle :** télécharger le dépôt, lire le dictionnaire des variables, identifier les essais indépendants, les distances, les cibles et les métadonnées météo ; vérifier les droits de réutilisation. Produire un rapport de qualité des données.
2. **Décision sur la correspondance physique :** expliciter si J-DriftX modélise une concentration de scalaire passif, une phase vapeur ou le transport/dépôt de gouttelettes. Si cette distinction ne peut pas être formulée, CAPRIV ne doit pas être utilisé comme benchmark prédictif.
3. **Choix du problème avec l'utilisateur :** obtenir un cas d'usage précis et une décision documentée ; ne pas déduire l'utilisateur du seul fait que les données sont disponibles.
4. **Données adaptées au régime retenu :** si le far-field est maintenu, trouver des observations indépendantes au-delà des distances couvertes par CAPRIV, avec métadonnées permettant de reproduire les entrées.
5. **Protocole préenregistré :** définir observable, baseline, partition par essais, métriques, seuil de succès et conditions d'arrêt avant toute comparaison.
6. **Repli :** si les données et le besoin pratique ne peuvent être établis, suspendre le développement applicatif et évaluer séparément le fallback théorique.

### Critère de sortie G0

G0 ne peut être déclaré franchi que lorsque les éléments suivants sont tous renseignés et sourcés : (a) utilisateur et décision, (b) observable primaire, (c) régime physique et hypothèses, (d) baseline disponible, (e) données de validation indépendantes adéquates, (f) seuil de succès justifié et (g) critère d'arrêt.

## Références externes consultées

1. US EPA, [Guidance on the Use of the Linked AGDISP-Gaussian Extension Models](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension), 2010.
2. US EPA, [Models for Pesticide Risk Assessment](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment), page consultée le 22 octobre 2026.
3. Ministère français de l'Agriculture, [Matériels permettant la limitation de la dérive](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques), mise à jour 16 juillet 2026.
4. Perriot et al., [Spray drift in field crops: a dataset...](https://doi.org/10.1016/j.dib.2024.110366), 2024.
5. Perriot et al., [Drift data from French CAPRIV project](https://doi.org/10.57745/Z8OJ3A), Recherche Data Gouv, version 3.0.
6. Bird et al., [Evaluation of the AgDISP aerial spray algorithms in the AgDRIFT model](https://doi.org/10.1002/etc.5620210328), 2002.
7. Castro-Tanzi et al., [Validation of AGDISPpro ... drone applications](https://doi.org/10.1016/j.scitotenv.2025.178725), 2025.
