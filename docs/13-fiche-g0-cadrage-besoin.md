# Fiche G0 — Cadrage du besoin indépendant de la solution

> **Statut : proposition à ratifier.** Cette fiche formalise le cadrage exigé par le [cadre de décision et de preuve](08-decision-utilite-et-preuve.md) avant tout benchmark applicatif. Les champs marqués **[à ratifier]** sont des choix que l'auteur du projet doit confirmer ; les autres sont documentés et sourcés. G0 ne sera déclaré franchi que lorsque les critères (a)–(g) ci-dessous seront renseignés, sourcés et ratifiés.

Rédigée le 22 octobre 2026. Documents liés : [revue adversariale G0](10-revue-adversariale-g0.md), [preuves externes](11-g0-evidence-externe.md), [catalogue de données](12-catalogue-donnees-transport-dispersion.md). Suit le plan de fiche en neuf points du document 08.

## Matrice de sortie G0 (critères a–g)

| Champ | Valeur retenue ou proposée | Statut |
|---|---|---|
| (a) Utilisateur et décision | Primaire : chercheur en dispersion — obtenir rapidement une estimation ponctuelle défendable, sans maillage. Candidat pratique : évaluateur de risque (exposition hors site). Horizon *in fine* : instruction de ZNT / distances tampons | **[à ratifier]** |
| (b) Observable primaire | Concentration aérienne d'un scalaire passif aux points de mesure ; dépôt au sol et exposition comme observables dérivés | **[à ratifier]** |
| (c) Régime physique et hypothèses | Scalaire passif turbulent ; deux pistes instruites en parallèle : champ proche contrôlé (traceur) et far-field (pulvérisation) ; tranchées après l'audit des données | Tranché : deux pistes |
| (d) Baseline | Multi-baselines : panache gaussien simple (toujours) + modèle état de l'art du corpus retenu (AGDISP/AgDRIFT pour la pulvérisation, extension gaussienne/AERMOD pour le far-field, panache gaussien calibré pour les traceurs) | Retenu |
| (e) Données de validation indépendantes | Candidats : DIFLU (champ proche contrôlé), DATEM/ETEX (longue distance) ; audit en cours (issue #13). CAPRIV limité au champ proche | En cours |
| (f) Seuil de succès | Voir §7 | **[proposé, à ratifier avant tout benchmark]** |
| (g) Critère d'arrêt | Voir §7 | **[proposé, à ratifier]** |

## 1. Problème physique et décision visée

Le problème physique est la prédiction, en un point quelconque de l'espace, du transport turbulent d'un scalaire passif émis dans l'atmosphère, sans construction de maillage ni résolution d'une EDP. La décision scientifique première est la capacité de cette représentation à prédire l'observable visée mieux qu'une baseline simple sur des essais indépendants. Les décisions appliquées candidates (évaluation d'exposition hors site, dimensionnement de distances tampons) sont documentées comme existantes ([Ministère de l'Agriculture](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques), [EPA](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/models-pesticide-risk-assessment)) mais restent des cibles conditionnelles : aucune n'est retenue avant la preuve de valeur différentielle (G2).

## 2. Utilisateurs et contraintes — un ordre hiérarchique, pas trois pistes en parallèle

Trois utilisateurs candidats ont été identifiés. Les instruire simultanément fragmenterait l'observable, les baselines et les standards de preuve exigés. La fiche retient donc un ordre :

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

Audit en cours (issue #13) sur les candidats identifiés par le [catalogue](12-catalogue-donnees-transport-dispersion.md) : **DATEM/ETEX** (longue distance), **DIFLU** (lâchers d'hélium contrôlés en champ proche avec météo), **ERIES** (dispersion urbaine en soufflerie). CAPRIV reste limité au champ proche (1–25 m) avec risque de fuite entre collecteurs d'un même essai. Règle de partition : par essai/scénario, jamais par collecteur isolé ([preuves externes, §2](11-g0-evidence-externe.md)). Lacune connue : aucun corpus ouvert de dépôt far-field de pulvérisation n'est identifié à ce jour ; si l'audit le confirme, la piste far-field pulvérisation est requalifiée en analogie méthodologique, pas en validation.

## 7. Critères de succès, seuils et conditions d'arrêt

**Seuil de succès proposé (à ratifier avant tout benchmark) :**

- Métriques : FAC2 (fraction de points dans un facteur 2) et NMSE, évaluées par essai indépendant, sur la concentration aérienne.
- Succès G2 (corpus unique) : FAC2 de J-DriftX ≥ FAC2 du panache gaussien simple sur au moins 60 % des essais indépendants, **et** pour au moins un sous-ensemble documenté : erreur ≤ baseline état de l'art, ou erreur comparable à coût total inférieur d'un facteur ≥ 10.
- Succès G3 (généralisation) : gain maintenu sur au moins un second corpus ou sous-ensemble disjoint non utilisé pour le calibrage.

**Critère d'arrêt proposé :** restreindre ou arrêter la piste applicative si :

1. l'audit conclut qu'aucun corpus ne permet de reconstruire les entrées et d'isoler des essais indépendants pour l'observable choisie ;
2. ou J-DriftX ne bat pas la baseline gaussienne simple sur le test discriminant (§8), à coût total comparable ;
3. ou le gain subsiste uniquement dans des régimes déjà bien servis par des modèles simples.

Dans ces cas, le projet se replie sur le [fallback théorique](09-fallback-modele-jouet.md) et documente le résultat négatif.

## 8. Test discriminant le moins coûteux

Après l'audit, sur **un seul** corpus (DIFLU si la piste champ proche est retenue, DATEM/ETEX pour le far-field) : comparer J-DriftX au panache gaussien simple sur les essais indépendants identifiés, observable concentration. Ce test peut réfuter l'hypothèse centrale — qu'un temps de transport dirigé apporte une information prédictive au-delà de la seule distance — sans développement applicatif ni calibrage lourd.

## 9. Sources et niveau de preuve

| Affirmation | Source | Niveau de preuve |
|---|---|---|
| Décisions réglementaires concrètes liées à la dérive (ZNT, matériels) | [Ministère de l'Agriculture](https://agriculture.gouv.fr/materiels-permettant-la-limitation-de-la-derive-de-pulverisation-des-produits-phytopharmaceutiques) | Officiel, contexte français |
| Incertitudes et limites AGDISP-Gaussian (far-field) | [EPA 2010](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) | Officiel, périmètre restreint |
| Accords variables AgDRIFT / AGDISPpro | [Bird et al. 2002](https://doi.org/10.1002/etc.5620210328), [Castro-Tanzi et al. 2025](https://doi.org/10.1016/j.scitotenv.2025.178725) | Évaluations publiées |
| CAPRIV limité au champ proche | [Perriot et al. 2024](https://doi.org/10.1016/j.dib.2024.110366) | Article de données |
| Candidats de validation (DATEM/ETEX, DIFLU, ERIES) | [Catalogue](12-catalogue-donnees-transport-dispersion.md) | Pré-tri documentaire, non audité |
| Aucune niche vacante établie | [Revue adversariale](10-revue-adversariale-g0.md) | Objections à instruire |
