# Fiche G0 — Cadrage du besoin indépendant de la solution

> **Statut : cadrage ratifié le 22 octobre 2026 sur les champs (a), (b), (f) et (g)** (priorité : la question scientifique, physique et mathématique, d'abord ; la visée pratique restant un horizon *in fine*). Le champ (e) a été renseigné le même jour par l'audit documentaire des corpus ([résultats](15-audit-corpus-g0-resultats.md)) : verdicts **V** pour DIFLU, DATEM et ETEX. **Décision : G0 est franchi le 22 octobre 2026.** La vérification au niveau des fichiers bruts (licence DIFLU, unités, limites de détection, sommes de contrôle) est un prérequis G1 avant le test discriminant, pas une condition de G0.

Rédigée et ratifiée le 22 octobre 2026. Documents liés : [revue adversariale G0](10-revue-adversariale-g0.md), [preuves externes](11-g0-evidence-externe.md), [catalogue de données](12-catalogue-donnees-transport-dispersion.md), [protocole d'audit des corpus](14-protocole-audit-corpus-g0.md), [résultats de l'audit](15-audit-corpus-g0-resultats.md). Suit le plan de fiche en neuf points du document 08.

## Matrice de sortie G0 (critères a–g)

| Champ | Valeur retenue | Statut |
|---|---|---|
| (a) Utilisateur et décision | Primaire : chercheur en dispersion — obtenir rapidement une estimation ponctuelle défendable, sans maillage. Candidat pratique : évaluateur de risque (exposition hors site). Horizon *in fine* : instruction de ZNT / distances tampons | **Ratifié le 22/10/2026** |
| (b) Observable primaire | Concentration aérienne d'un scalaire passif aux points de mesure ; dépôt au sol et exposition comme observables dérivés | **Ratifié le 22/10/2026** |
| (c) Régime physique et hypothèses | Scalaire passif turbulent ; deux pistes instruites : champ proche contrôlé (traceur) et far-field (traceur continental) ; tranchées après l'audit des données | Tranché : deux pistes |
| (d) Baseline | Multi-baselines : panache gaussien simple (toujours) + modèle état de l'art du corpus retenu (AGDISP/AgDRIFT pour la pulvérisation, extension gaussienne/AERMOD pour le far-field, panache gaussien calibré pour les traceurs) | Retenu |
| (e) Données de validation indépendantes | DIFLU (V, champ proche, lâchers d'hélium contrôlés, météo co-localisée), NOAA DATEM (V, cinq expériences longue distance), ETEX (V, deux lâchers, 168 stations, météo ECMWF) — [audit](15-audit-corpus-g0-resultats.md). CAPRIV limité au champ proche | **Renseigné et sourcé le 22/10/2026 — verdicts V, réserves explicites dans l'audit** |
| (f) Seuil de succès | Voir §7 | **Ratifié le 22/10/2026** |
| (g) Critère d'arrêt | Voir §7 | **Ratifié le 22/10/2026** |

## 1. Problème physique et décision visée

Le problème physique est la prédiction, en un point quelconque de l'espace, du transport turbulent d'un scalaire passif émis dans l'atmosphère, sans construction de maillage ni résolution d'une EDP. La décision scientifique première est la capacité de cette représentation à prédire l'observable visée mieux qu'une baseline simple sur des essais indépendants. Les décisions appliquées candidates (évaluation d'exposition hors site, dimensionnement de distances tampons) sont documentées comme existantes ([Ministère de l'Agriculture](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques), [EPA](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment)) mais restent des cibles conditionnelles : aucune n'est retenue avant la preuve de valeur différentielle (G2).

## 2. Utilisateurs et contraintes — un ordre hiérarchique, pas trois pistes en parallèle

Trois utilisateurs candidats ont été identifiés. Les instruire simultanément fragmenterait l'observable, les baselines et les standards de preuve exigés. La fiche retient donc un ordre, ratifié le 22 octobre 2026 avec la priorité explicite : **la question scientifique (physique et mathématique) d'abord**.

1. **Chercheur en dispersion (utilisateur primaire).** Le plus atteignable : les corpus traceurs (DIFLU, DATEM/ETEX) fournissent des essais contrôlés avec observable directe, et l'hypothèse centrale de J-DriftX (information prédictive d'une métrique de temps de transport) est une affirmation scientifique testable indépendamment de tout usage réglementaire.
2. **Évaluateur de risque (premier utilisateur pratique candidat).** Il exigera exactement ce que la piste scientifique doit produire : un gain de précision ou de coût démontré sur essais indépendants, et une méthode transparente. Cette piste devient instruisable dès G2.
3. **Autorité / instruction des ZNT (horizon *in fine*).** La décision réglementaire impose en plus une aptitude au cadre réglementaire (G4) : standard hors de portée avant G2–G3 ; viser ce jalon d'emblée prématurerait l'arrêt du projet sur un critère non encore instruit.

**Contraintes transverses :** coût total mesuré (préparation + inférence, pas seulement l'inférence), transparence et reproductibilité des hypothèses, distinction systématique entre propriété démontrée et conjecture.

## 3. Limites documentées des solutions existantes

- L'extension gaussienne d'AGDISP a des incertitudes documentées au-delà de 0,5 mile et une validation limitée au-delà de 2 miles, dans le cadre précis de certains scénarios de pulvérisation aérienne ([EPA 2010](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension)).
- Les évaluations d'AgDRIFT (161 essais de terrain) et d'AGDISPpro (18 applications de drones) rapportent des accords variables selon les variables, buses et régimes ([Bird et al. 2002](https://doi.org/10.1002/etc.5620210328), [Castro-Tanzi et al. 2025](https://doi.org/10.1016/j.scitotenv.2025.178725)).
- Les modèles complets (CFD, lagrangiens) exigent une préparation coûteuse (maillage, météo haute résolution), ce qui limite leur usage pour l'évaluation ponctuelle rapide.

Ces limites établissent l'existence d'un espace de problème, pas celle d'une niche vacante ([revue adversariale](10-revue-adversariale-g0.md)).

## 4. Valeur ajoutée supposée de J-DriftX

Évaluation ponctuelle sans maillage, coût d'inférence faible, interprétabilité physique (temps de transport dirigés), calibration possible sur de rares observations. Cette valeur est **supposée** : elle reste l'hypothèse à tester, pas un acquis ([README](https://github.com/JM-Brun/J-DriftX#readme)).

## 5. Baselines et justification

Comparaison multi-baselines, équitable (mêmes entrées, mêmes observables, coût total mesuré) :

1. **Panache/puff gaussien simple** — baseline minimale sur tous les corpus ; tout gain doit d'abord être établi face à elle.
2. **Modèle état de l'art du corpus retenu** — AGDISP/AgDRIFT (pulvérisation), extension gaussienne/AERMOD (far-field), panache gaussien calibré (traceurs DIFLU/DATEM). La comparaison à plusieurs baselines répond au risque qu'un seul modèle de référence masque des gains ou des pertes sélectifs.

## 6. Données accessibles et lacunes

L'audit documentaire du 22 octobre 2026 ([résultats](15-audit-corpus-g0-resultats.md)) a vérifié l'accès, le terme source, la météo et la structure d'indépendance des candidats du [catalogue](12-catalogue-donnees-transport-dispersion.md) : **DIFLU** (champ proche, hélium, 2019), **DATEM** (cinq expériences longue distance), **ETEX** (deux lâchers continentaux, JRC). CAPRIV reste limité au champ proche (1–25 m) avec risque de fuite entre collecteurs d'un même essai. Règle de partition : par essai/scénario, jamais par point de mesure isolé. Lacune confirmée par l'audit : aucun corpus ouvert de dépôt far-field de pulvérisation n'a été identifié ; la piste far-field rejoint donc la voie traceur (DATEM/ETEX), la pulvérisation restant une analogie méthodologique en far-field et un cas de champ proche documenté par CAPRIV.

## 7. Critères de succès, seuils et conditions d'arrêt

**Seuil de succès (ratifié le 22 octobre 2026, avant tout benchmark) :**

- Métriques : FAC2 (fraction de points dans un facteur 2) et NMSE, évaluées par essai indépendant, sur la concentration aérienne.
- Succès G2 (corpus unique) : FAC2 de J-DriftX ≥ FAC2 du panache gaussien simple sur au moins 60 % des essais indépendants, **et** pour au moins un sous-ensemble documenté : erreur ≤ baseline état de l'art, ou erreur comparable à coût total inférieur d'un facteur ≥ 10.
- Succès G3 (généralisation) : gain maintenu sur au moins un second corpus ou sous-ensemble disjoint non utilisé pour le calibrage.

**Critère d'arrêt (ratifié le 22 octobre 2026) :** restreindre ou arrêter la piste applicative si :

1. l'audit conclut qu'aucun corpus ne permet de reconstruire les entrées et d'isoler des essais indépendants pour l'observable choisie ;
2. ou J-DriftX ne bat pas la baseline gaussienne simple sur le test discriminant (§8), à coût total comparable ;
3. ou le gain subsiste uniquement dans des régimes déjà bien servis par des modèles simples.

Dans ces cas, le projet se replie sur le [fallback théorique](09-fallback-modele-jouet.md) et documente le résultat négatif. *Note : la condition 1 n'est pas activée — l'audit a établi le contraire ([docs/15](15-audit-corpus-g0-resultats.md)).*

## 8. Test discriminant le moins coûteux

Corpus principal retenu par l'audit : **DIFLU** (champ proche, terme source contrôlé, météo co-localisée, observable conforme). Comparer J-DriftX au panache gaussien simple sur les lâchers indépendants identifiés, observable concentration. Ce test peut réfuter l'hypothèse centrale — qu'un temps de transport dirigé apporte une information prédictive au-delà de la seule distance — sans développement applicatif ni calibrage lourd. DATEM/ETEX restent en réserve pour la généralisation (G3).

## 9. Sources et niveau de preuve

| Affirmation | Source | Niveau de preuve |
|---|---|---|
| Décisions réglementaires concrètes liées à la dérive (ZNT, matériels) | [Ministère de l'Agriculture](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques) | Officiel, contexte français |
| Incertitudes et limites AGDISP-Gaussian (far-field) | [EPA 2010](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) | Officiel, périmètre restreint |
| Accords variables AgDRIFT / AGDISPpro | [Bird et al. 2002](https://doi.org/10.1002/etc.5620210328), [Castro-Tanzi et al. 2025](https://doi.org/10.1016/j.scitotenv.2025.178725) | Évaluations publiées |
| CAPRIV limité au champ proche | [Perriot et al. 2024](https://doi.org/10.1016/j.dib.2024.110366) | Article de données |
| DIFLU, DATEM, ETEX : accès, terme source, indépendance | [Audit des corpus](15-audit-corpus-g0-resultats.md) | Audit documentaire du 22/10/2026 |
| Aucune niche vacante établie | [Revue adversariale](10-revue-adversariale-g0.md) | Objections à instruire |
