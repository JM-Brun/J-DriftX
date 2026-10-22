# G0 — Compléter le cadrage à partir de preuves externes

> **État au 22 octobre 2026.** Recherche documentaire ciblée, non revue systématique. Les sources établissent l'existence de problèmes de mesure et d'évaluation de la dérive ; elles ne démontrent pas que J-DriftX y apporte une solution.

**Extension de la recherche de données :** un [catalogue détaillé de jeux de données de transport et dispersion](12-catalogue-donnees-transport-dispersion.md) a été ajouté. Les candidats les plus proches de l'hypothèse atmosphérique sont NOAA DATEM/ETEX (longue distance), DIFLU (traceur hélium contrôlé en champ proche) et ERIES (dispersion urbaine en soufflerie). Des données routières, industrielles, marines, fluviales et radiologiques sont aussi recensées, avec distinction explicite entre validation physique directe, analogie méthodologique et simple surveillance. Ce catalogue est un pré-tri documentaire; aucun des fichiers bruts de ces nouveaux jeux n'a encore été audité.

## Décision provisoire

**G0 n'est pas franchi.** Ne pas commencer un benchmark applicatif ni présenter le far-field comme cas d'usage retenu. Deux éléments sont maintenant plus clairs :

1. Il existe des décisions concrètes liées à la dérive de pulvérisation (évaluation d'exposition, distances tampons, évaluation de matériels de réduction de dérive).
2. CAPRIV est principalement adapté à l'étude de dérive de proximité, pas à la validation du far-field à plusieurs kilomètres. Le décalage entre le phénomène mesuré et les hypothèses physiques du modèle reste à résoudre.

La question de recherche doit donc être formulée indépendamment de la méthode : **quelle grandeur, pour quelle décision, dans quel régime physique, n'est-elle pas suffisamment prédite par une méthode existante, et quelles données permettent de tester cette lacune ?**

## 1. Besoin et décision utilisateur : ce que les sources soutiennent

### Évaluation réglementaire et exposition

L'EPA utilise des modèles atmosphériques pour estimer les dépôts hors site de pesticides. Sa page de modèles décrit AgDRIFT (v2.1.1) pour différentes applications agricoles et AGDISP (v8.26) pour la dérive depuis des sites d'application, notamment en aérien et en rampe au sol. [EPA — Models for Pesticide Risk Assessment](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment).

L'EPA a documenté des incertitudes spécifiques à l'extension gaussienne d'AGDISP au-delà de 0,5 mile, une validation limitée au-delà de 2 miles et des limites relatives aux barrières et à la météorologie. Son guide restreint toutefois l'usage discuté à certains scénarios de pulvérisation aérienne. [EPA — Guidance on the linked AGDISP-Gaussian Extension Models](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension).

Ces sources justifient une question ciblée sur certains scénarios d'exposition lointaine. Elles ne démontrent pas que les décisions réglementaires gagneraient à des estimations moins conservatrices, que le cas s'applique à tous les modes d'application, ou qu'une méthode à temps de transport dirigé reproduirait les mécanismes physiques manquants.

### Décision en France

Le ministère français indique que les zones non traitées (ZNT) et certaines distances de sécurité sont encadrées par l'arrêté du 4 mai 2017 ; les réductions de certaines ZNT reposent notamment sur l'utilisation de matériels figurant sur une liste officielle et sur des conditions d'efficacité définies. [Ministère de l'Agriculture — matériels permettant de limiter la dérive](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques).

**Implication :** il existe un besoin décisionnel réel autour de la dérive, mais ce n'est pas une preuve que le modèle de dispersion J-DriftX est le bon outil. Pour viser cette décision, il faudrait déterminer si le livrable attendu est une courbe de dépôt, un facteur de réduction, une distance tampon ou une exposition.

## 2. Données CAPRIV : intérêt limité au champ proche

Le jeu [Drift data from French CAPRIV project](https://doi.org/10.57745/Z8OJ3A) est disponible sur Recherche Data Gouv. La table de cultures de plein champ contient 3 792 observations/collecteurs et 38 variables ; le dépôt comprend aussi des données de viticulture et d'arboriculture. [Dépôt de données](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FZ8OJ3A).

Le papier de données décrit des essais en France en 2021–2022 sur blé, avec boîtes de Petri pour le dépôt, fils PVC pour la dérive aérienne et vêtements sur mannequins pour l'exposition cutanée potentielle. Les distances rapportées pour le dépôt au sol sont de l'ordre de 1–25 m et les fils PVC de mesure aérienne sont localisés à 5 m. [Perriot et al. (2024)](https://doi.org/10.1016/j.dib.2024.110366).

| Question | Évaluation actuelle | Motif |
|---|---|---|
| Données accessibles ? | Oui, en principe | Dépôt public; fichiers bruts, unités, droits et complétude à vérifier |
| Dépôt au sol ? | Oui | Collecteurs de dépôt avec indicateur normalisé |
| Dérive aérienne ? | Oui, dispositif localisé | Fils PVC à 5 m; ce n'est pas une mesure de concentration continue |
| Validation far-field ? | Non démontrée | Distances de l'ordre de quelques dizaines de mètres |
| Observations indépendantes ? | Pas établi | Plusieurs milliers de collecteurs ne signifient pas plusieurs milliers d'essais indépendants |
| Scalaire passif ? | Incertain | Le dépôt de gouttelettes dépend de la taille, de la sédimentation, de l'évaporation et de la collecte |

CAPRIV peut aider à caractériser un cas proche, mais ne constitue pas une validation du far-field. Une séparation aléatoire par collecteur risquerait une fuite entre mesures d'un même essai; les groupes doivent être identifiés avant toute évaluation.

## 3. Pourquoi les modèles existants et leurs données comptent

L'évaluation d'AgDRIFT par Bird et al. compare 161 essais de terrain et rapporte des résultats différents selon les variables et les régimes. [Bird et al. (2002), DOI 10.1002/etc.5620210328](https://doi.org/10.1002/etc.5620210328).

L'évaluation d'AGDISPpro publiée en 2025 porte sur 18 applications de drones et rapporte un accord variable selon les buses et scénarios. [Castro-Tanzi et al. (2025), DOI 10.1016/j.scitotenv.2025.178725](https://doi.org/10.1016/j.scitotenv.2025.178725).

Pour un inventaire plus large, consulter le [catalogue ADMLC](https://admlc.com/datasets/) et les [jeux classiques HARMO](https://harmo.org/classic.php). Le [catalogue J-DriftX des données ouvertes](12-catalogue-donnees-transport-dispersion.md) hiérarchise les candidats atmosphériques, routiers, industriels, marins, fluviaux et radiologiques, et précise lesquels sont des analogies seulement.

## 4. Fiche G0 mise à jour

| Champ G0 | État actuel | Preuve manquante / prochaine action |
|---|---|---|
| Phénomène | Dérive de pulvérisation et transport atmosphérique | Délimiter gouttelettes vs phase vapeur/scalaires passifs |
| Observable primaire | **Non choisi** | Choisir dépôt, concentration/flux aérien ou autre cible |
| Utilisateur | **Non identifié** | Distinguer évaluateur de risque, autorité, chercheur ou développeur |
| Décision | Exposition et zones tampons sont des exemples documentés | Identifier une décision précise et le coût des erreurs |
| Scénario | Far-field proposé, non confirmé | Définir mode d'application, distance, météo, terrain, végétation et tailles |
| Baseline | AgDRIFT/AGDISP selon le scénario; DATEM/ETEX comme corpus d'évaluation potentiel | Vérifier la même physique et les mêmes observables |
| Données | CAPRIV ouvert mais proche; DATEM/ETEX, DIFLU, ERIES et jeux routiers prometteurs sur le papier | Auditer accès, fichiers, métadonnées, licence et unités |
| Indépendance | Non établie | Partitionner par essais/scénarios et isoler un test final |
| Seuil de succès | **Non défini** | Fixer métriques, tolérance et gain décisionnel avant benchmark |
| Critère d'arrêt | À préciser | Arrêter si observable, besoin, données ou baseline ne peuvent être justifiés |

## 5. Décision et prochaines étapes

**Ne pas lancer le benchmark far-field sur la base de CAPRIV.** La suite raisonnable est un audit des fichiers, sans entraînement de modèle, sur trois candidats :

1. **DATEM/ETEX** si le far-field atmosphérique reste l'hypothèse;
2. **DIFLU** pour la dispersion contrôlée en champ proche avec météorologie;
3. **ERIES ou EPA near-road barriers** selon que l'on privilégie la dispersion urbaine ou routière.

Pour chaque candidat, vérifier licence, terme source, coordonnées et temps, météo, observable/unité, limites de détection, données manquantes, nombre d'expériences indépendantes et possibilité de reproduire les entrées. Si les équations ne correspondent pas à l'observable, ou si les conditions ne sont pas reconstructibles, le classer comme référence bibliographique uniquement.

### Critère de sortie G0

G0 ne peut être déclaré franchi que lorsque sont renseignés et sourcés : (a) utilisateur et décision, (b) observable primaire, (c) régime physique et hypothèses, (d) baseline, (e) données de validation indépendantes, (f) seuil de succès et (g) critère d'arrêt.

## Mise à jour — sortie de G0 (22 octobre 2026, en soirée)

**G0 est franchi.** La décision provisoire ci-dessus est remplacée par deux documents :

- la [fiche de cadrage du besoin](13-fiche-g0-cadrage-besoin.md), dont les critères (a)–(g) sont renseignés, sourcés et ratifiés ;
- les [résultats de l'audit des corpus](15-audit-corpus-g0-resultats.md) : verdicts **V** pour DIFLU (champ proche, licence à confirmer), NOAA DATEM (far-field) et ETEX (far-field, deux lâchers), avec réserves explicites.

CAPRIV reste classé champ proche, sans changement. La vérification au niveau des fichiers bruts (licence DIFLU, unités, limites de détection, sommes de contrôle) est un prérequis G1 avant tout benchmark.

## Références externes

- US EPA, [AGDISP-Gaussian Extension guidance](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension), 2010.
- US EPA, [Models for Pesticide Risk Assessment](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment).
- Ministère de l'Agriculture, [limitation de la dérive](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques).
- Perriot et al., [CAPRIV data article](https://doi.org/10.1016/j.dib.2024.110366), 2024.
- Perriot et al., [CAPRIV dataset](https://doi.org/10.57745/Z8OJ3A).
- Bird et al., [AgDRIFT evaluation](https://doi.org/10.1002/etc.5620210328), 2002.
- Castro-Tanzi et al., [AGDISPpro drone evaluation](https://doi.org/10.1016/j.scitotenv.2025.178725), 2025.
- Catalogue additionnel : [docs/12-catalogue-donnees-transport-dispersion.md](12-catalogue-donnees-transport-dispersion.md).
