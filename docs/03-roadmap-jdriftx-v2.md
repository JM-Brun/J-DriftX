# Feuille de route — J-DriftX v2

> Adoptée en octobre 2026 après audit du projet historique et revue structurée de l'état de l'art. Les décisions scientifiques restent révisables après examen de la revue systématique finale. Justifications : [audit historique](01-audit-heritage-driftx.md), [revue structurée](02-revue-etat-art-2026.md), [plan d'intégration de la revue](07-plan-integration-revue-systematique.md). Le premier jalon opérationnel est désormais **G0 — établir le besoin et l'utilité potentielle**, détaillé dans [le cadre de décision et de preuve](08-decision-utilite-et-preuve.md).

## Vision

**J-DriftX v2** est un projet de recherche visant un moteur de dispersion à complexité réduite : solutions de similitude généralisées dans une métrique non symétrique de temps de transport, évaluation ponctuelle sans maillage, calibration par assimilation de données et contraintes physiques à formaliser et valider. Cibles candidates à instruire : far-field de la dérive de pulvérisation, exposition résidentielle et identification de source.

Cette vision est une hypothèse de recherche, pas une validation des performances, de la nouveauté ou de l'aptitude réglementaire du modèle. La priorité est de vérifier si l'approche répond à un besoin important mieux que les solutions disponibles, avant de développer l'architecture cible dans son ensemble.

## Principes directeurs

1. **Utilité avant implémentation** : identifier le besoin, l'utilisateur, la décision et le bénéfice attendu ; documenter les alternatives et les critères d'abandon.
2. **Physique d'abord, données ensuite** : conserver un modèle analytique interprétable comme hypothèse centrale ; toute calibration ou approche apprise doit être évaluée face à une baseline et hors domaine.
3. **Benchmarks avant fonctionnalités** : chaque module est justifié par une question testable et livré avec un cas de validation reproductible.
4. **Cœur pur, bindings en aval** : noyau Python sans dépendance SIG ; plugin QGIS et API séparés.
5. **Mesurer le coût total** : distinguer coût de préparation/entraînement, coût d'inférence, mémoire et précision ; l'évaluation ponctuelle à faible coût reste un objectif à mesurer.
6. **Interopérabilité vérifiée** : formats d'entrée météo compatibles AERMOD/AgDRIFT quand c'est possible ; sorties raster/GeoTIFF géoréférencées après validation du noyau.
7. **Revue traçable** : ne pas transformer l'absence de références trouvées en preuve d'absence de concurrents ; les décisions de conception doivent renvoyer aux sources examinées et aux tests.

## Portes de décision scientifiques

Ces portes précèdent ou conditionnent les jalons techniques. Elles peuvent conduire à poursuivre, restreindre, réviser ou arrêter une piste.

- **G0 — Besoin et utilité potentielle (priorité immédiate)** : fiche de problème indépendante de la solution ; utilisateur et décision visés ; limites documentées des alternatives ; bénéfice mesurable attendu ; critères de succès et d'abandon fixés avant le benchmark. Ne pas présumer que le far-field de pulvérisation est le meilleur cas d'usage sans justification comparative.
- **G1 — Cohérence et faisabilité théoriques** : variables, unités, hypothèses et conditions aux limites explicites ; propriétés démontrées séparées des conjectures ; cas analytique minimal reproductible.
- **G2 — Valeur différentielle en environnement contrôlé** : ablations, baselines équitables, précision, coût, robustesse et résultats négatifs ; attribution des gains aux composants effectivement testés.
- **G3 — Validation indépendante** : données ou simulations non utilisées pour concevoir ou calibrer la méthode ; provenance, incertitude, échecs et domaine de validité documentés.
- **G4 — Pertinence applicative** : établir si le bénéfice change une décision ou ouvre une capacité scientifique utile ; publication ou transfert uniquement si les preuves le justifient.

Les détails opérationnels et les critères expérimentaux sont décrits dans [docs/08-decision-utilite-et-preuve.md](08-decision-utilite-et-preuve.md).

## Architecture cible conditionnelle

L'architecture est une cible de conception, non une liste de fonctionnalités à implémenter sans condition. La priorité d'un module dépend de sa contribution à une hypothèse et à une expérience.

| Module | Rôle | Priorité conditionnelle |
|---|---|---|
| core/similitude | Solutions de similitude jets/panaches/puffs ; formalisation des hypothèses et limites | G1, uniquement pour le problème retenu |
| core/metric | Métrique non symétrique de temps de transport ; propriétés et cas limites | G1–G2, si elle teste une valeur différentielle |
| core/constraints | Conservation, positivité et divergence nulle uniquement lorsque justifiées ; tests systématiques | G1–G2 |
| benchmarks/reference | Cas analytique reproductible, métriques d'erreur, coût et cas limites | Prioritaire dès G1 |
| benchmarks/baselines | Comparaison équitable avec modèle gaussien et, sur cas commun, POD/ROM ou surrogate pertinent | Prioritaire dès G2 |
| core/levels | Hiérarchie multi-niveaux et estimateur d'erreur | Après preuve de valeur du cas de base |
| assim/calibration | Calibration et analyse d'identifiabilité | Après définition d'un cas direct crédible |
| assim/ste | Identification de source et méthodes adjointes, avec baselines documentées | Seulement si le besoin G0 le justifie |
| io/ | Météo, MNT, émissions ; sorties ponctuelles, profils et rasters | Selon les données et la validation requises |
| bindings/qgis | Plugin QGIS modernisé | Après validation d'un noyau utile |
| benchmarks/ | Cas publiés et comparaisons reproductibles | Continu, partie intégrante de la preuve |

## Jalons techniques et critères d'acceptation

- **M0 — Ancrage documentaire** : revue structurée existante et traçabilité des sources. La revue systématique finale, ses limites et les décisions qui en découlent seront enregistrées selon [le plan d'intégration](07-plan-integration-revue-systematique.md). La qualification de revue systématique reproductible n'est utilisée que si les recherches, comptes et sélections sont effectivement documentés.
- **M1 — Noyau et preuve** : uniquement après cadrage G0, formaliser le noyau minimal utile et le benchmark analytique ; tests des propriétés dans leur domaine de validité ; mesure de l'erreur, du temps et de la mémoire.
- **M2 — Calibration et multi-niveaux** : données de calibration distinctes de la validation ; comparaison à des baselines sur le même problème ; sensibilité, identifiabilité et incertitude documentées.
- **M3 — Terrains et GIS** : données indépendantes avec provenance/licence vérifiées ; effets du relief et des conditions météo testés séparément ; intégration GIS en aval.
- **M4 — Article de synthèse** : manuscrit fondé sur résultats vérifiables, avec résultats négatifs et limites ; choix de la cible éditoriale après résultats.
- **M5 — Transfert réglementaire/applicationnel** : étude de pertinence et conformité spécifique au contexte avant toute revendication d'usage opérationnel ou réglementaire.

## Hypothèses scientifiques à tester

1. La métrique de temps de transport peut généraliser certaines solutions de similitude à des vents non uniformes tout en respectant la conservation de masse sous des hypothèses explicites.
2. Une calibration hybride peut être plus robuste hors domaine qu'un surrogate ML comparable.
3. Une métrique intégrant certains effets topographiques peut améliorer des cas définis par rapport à une baseline gaussienne pertinente.

Aucune de ces hypothèses ne doit être présentée comme un résultat acquis avant preuve analytique ou validation empirique indépendante. La priorité et la formulation de chaque hypothèse peuvent être révisées à l'issue de G0.

## Risques et parades

| Risque | Parade |
|---|---|
| Le besoin est supposé plutôt que documenté | Porte G0 avant investissement technique |
| Texte intégral ou données de validation inaccessibles | Distinguer clairement résultats vérifiés, résumés et sources secondaires ; documenter les limites |
| Comparaisons entre problèmes non équivalents | Définir un protocole commun et justifier la comparabilité physique |
| Dérive vers le « tout ML » ou rejet a priori du ML | Choisir les méthodes sur preuves et benchmarks, pas sur préférence idéologique |
| Propriétés physiques annoncées sans preuve | Relier chaque propriété à une hypothèse, une démonstration et/ou un test ; borner le domaine garanti |
| Dépendance à une seule campagne ou un cas synthétique | Ajouter analyses de sensibilité et validation indépendante avant généralisation |
| Fonctionnalités applicatives prématurées | Garder QGIS, API et interopérabilité après la validation du noyau |

## Fallback si l'utilité pratique n'est pas démontrée

Un résultat négatif sur l'utilité applicative ne justifie ni de masquer les résultats ni de prolonger l'architecture cible sans motif. Si une question mathématique précise subsiste, le projet peut se réduire à un **modèle jouet** : définitions, propriétés démontrées, contre-exemples, cas analytiques et code minimal reproductible. Le candidat initial est un transport unidimensionnel avec temps de parcours dirigé, sous réserve de vérifier les définitions et l'état de l'art. Ce fallback ne doit pas être présenté comme une contribution originale avant d'avoir établi la nouveauté.

Le protocole et les critères d'acceptation sont décrits dans [docs/09-fallback-modele-jouet.md](09-fallback-modele-jouet.md), avec une [page de synthèse publique](../site/projet/modele-jouet.qmd).

## Prochaines actions

1. **G0 — Rédiger la fiche de décision d'utilité** pour le far-field de dérive de pulvérisation : problème, utilisateur, décision, contraintes, limites documentées des alternatives, bénéfice supposé, baselines, données accessibles et critères d'abandon.
2. Vérifier si la revue de l'état de l'art suggère un autre cas d'usage plus important ou plus testable ; comparer les options sur des critères explicites.
3. Choisir le test discriminant le moins coûteux et définir ses métriques et seuils avant d'observer les résultats.
4. Seulement après cette décision, formaliser le problème mathématique minimal et le benchmark correspondant.
5. Continuer l'intégration de la revue systématique et consigner les décisions en reliant les affirmations aux sources.
6. Décider des licences et de l'archivage des sources historiques selon les droits applicables.

## Références de travail

- [Cadre de décision : utilité et preuve](08-decision-utilite-et-preuve.md)
- [Plan d'intégration scientifique et de validation](05-plan-validation-et-integration.md)
- [Revue de l'état de l'art 2026](02-revue-etat-art-2026.md)
