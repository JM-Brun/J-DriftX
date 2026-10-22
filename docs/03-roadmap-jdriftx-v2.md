# Feuille de route — J-DriftX v2

> Adoptée en octobre 2026 après audit du projet historique et revue structurée de l'état de l'art. Les décisions scientifiques restent révisables après examen de la revue systématique finale. Justifications : [audit historique](01-audit-heritage-driftx.md), [revue structurée](02-revue-etat-art-2026.md), [plan d'intégration de la revue](07-plan-integration-revue-systematique.md).

## Vision

**J-DriftX v2** est un projet de recherche visant un moteur de dispersion à complexité réduite : solutions de similitude généralisées dans une métrique non symétrique de temps de transport, évaluation ponctuelle sans maillage, calibration par assimilation de données et contraintes physiques à formaliser et valider. Cible applicative à instruire : far-field de la dérive de pulvérisation, exposition résidentielle et identification de source.

Cette vision est une hypothèse de recherche, pas une validation des performances, de la nouveauté ou de l'aptitude réglementaire du modèle.

## Principes directeurs

1. **Physique d'abord, données ensuite** : conserver un modèle analytique interprétable comme hypothèse centrale ; toute calibration ou approche apprise doit être évaluée face à une baseline et hors domaine.
2. **Benchmarks avant fonctionnalités** : chaque module est livré avec un cas de validation reproductible.
3. **Cœur pur, bindings en aval** : noyau Python sans dépendance SIG ; plugin QGIS et API séparés.
4. **Mesurer le coût total** : distinguer coût de préparation/entraînement, coût d'inférence, mémoire et précision ; l'évaluation ponctuelle à faible coût reste un objectif à mesurer.
5. **Interopérabilité vérifiée** : formats d'entrée météo compatibles AERMOD/AgDRIFT quand c'est possible ; sorties raster/GeoTIFF géoréférencées après validation du noyau.
6. **Revue traçable** : ne pas transformer l'absence de références trouvées en preuve d'absence de concurrents ; les décisions de conception doivent renvoyer aux sources examinées et aux tests.

## Architecture cible

| Module | Rôle | Priorité |
|---|---|---|
| core/similitude | Solutions de similitude jets/panaches/puffs ; formalisation des hypothèses et limites | M1 |
| core/metric | Métrique non symétrique de temps de transport ; propriétés et cas limites | M1 |
| core/constraints | Conservation, positivité et divergence nulle uniquement lorsque justifiées ; tests systématiques | M1 |
| benchmarks/reference | Cas analytique reproductible, métriques d'erreur, coût et cas limites | M1 |
| benchmarks/baselines | Comparaison équitable avec modèle gaussien et, sur cas commun, POD/ROM ou surrogate pertinent | M1–M2 |
| core/levels | Hiérarchie multi-niveaux et estimateur d'erreur | M2, après validation du cas M1 |
| assim/calibration | Moindres carrés (M1) puis régularisation Tikhonov/calibration bayésienne si justifiées | M1–M3 |
| assim/ste | Identification de source et méthodes adjointes, avec baselines documentées | M2 |
| io/ | Météo, MNT, émissions ; sorties ponctuelles, profils et rasters | M1–M2, selon données et validation |
| bindings/qgis | Plugin QGIS modernisé | M3, après validation du noyau |
| benchmarks/ | Cas publiés et comparaisons reproductibles | M1 puis continu |

## Jalons et critères d'acceptation

- **M0 — Ancrage documentaire** : revue structurée existante et traçabilité des sources. La revue systématique finale, ses limites et les décisions qui en découlent seront enregistrées selon [le plan d'intégration](07-plan-integration-revue-systematique.md). La qualification de revue systématique reproductible n'est utilisée que si les recherches, comptes et sélections sont effectivement documentés.
- **M1 — Noyau et preuve** : modules similitude/métrique/contraintes et benchmark analytique ; tests des propriétés dans leur domaine de validité ; mesure de l'erreur, du temps et de la mémoire.
- **M2 — Calibration et multi-niveaux** : données de calibration distinctes de la validation ; comparaison à des baselines sur le même problème ; sensibilité, identifiabilité et incertitude documentées.
- **M3 — Terrains et GIS** : données indépendantes avec provenance/licence vérifiées ; effets du relief et des conditions météo testés séparément ; intégration GIS en aval.
- **M4 — Article de synthèse** : manuscrit fondé sur résultats vérifiables, avec résultats négatifs et limites ; choix de la cible éditoriale après résultats.
- **M5 — Transfert réglementaire/applicationnel** : étude de pertinence et conformité spécifique au contexte avant toute revendication d'usage opérationnel ou réglementaire.

## Hypothèses scientifiques à tester

1. La métrique de temps de transport peut généraliser certaines solutions de similitude à des vents non uniformes tout en respectant la conservation de masse sous des hypothèses explicites.
2. Une calibration hybride peut être plus robuste hors domaine qu'un surrogate ML comparable.
3. Une métrique intégrant certains effets topographiques peut améliorer des cas définis par rapport à une baseline gaussienne pertinente.

Aucune de ces hypothèses ne doit être présentée comme un résultat acquis avant preuve analytique ou validation empirique indépendante.

## Risques et parades

| Risque | Parade |
|---|---|
| Texte intégral ou données de validation inaccessibles | Distinguer clairement résultats vérifiés, résumés et sources secondaires ; documenter les limites |
| Comparaisons entre problèmes non équivalents | Définir un protocole commun et justifier la comparabilité physique |
| Dérive vers le « tout ML » ou rejet a priori du ML | Choisir les méthodes sur preuves et benchmarks, pas sur préférence idéologique |
| Propriétés physiques annoncées sans preuve | Relier chaque propriété à une hypothèse, une démonstration et/ou un test ; borner le domaine garanti |
| Dépendance à une seule campagne ou un cas synthétique | Ajouter analyses de sensibilité et validation indépendante avant généralisation |
| Fonctionnalités applicatives prématurées | Garder QGIS, API et interopérabilité après la validation du noyau |

## Prochaines actions

1. Ajouter le fichier final de revue systématique sous raw/ et référencer son nom exact.
2. Remplir la matrice de décision dans [le plan d'intégration](07-plan-integration-revue-systematique.md), en reliant chaque décision à des sources primaires.
3. Formaliser le problème mathématique et le benchmark M1 le plus discriminant.
4. Ouvrir des issues ciblées par module avec critères d'acceptation.
5. Décider des licences et de l'archivage des sources historiques selon les droits applicables.
