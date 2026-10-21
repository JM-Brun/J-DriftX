# Feuille de route — J-DriftX v2

> Adoptée en octobre 2026 après audit du projet historique et revue de l'état de l'art. Toutes les justifications sont dans [01-audit-heritage-driftx.md](01-audit-heritage-driftx.md) et [02-revue-etat-art-2026.md](02-revue-etat-art-2026.md).

## Vision

**J-DriftX v2** est un moteur open source de dispersion à complexité réduite : solutions de similitude généralisées dans une métrique non symétrique de temps de transport, évaluation ponctuelle sans maillage, calibration par assimilation de données, contraintes physiques à formaliser et à valider (conservation, positivité, divergence nulle). Cible applicative : far-field de la dérive de pulvérisation (dont drones), exposition résidentielle, analyse de risque et identification de source.

## Principes directeurs

1. **Physique d'abord, données ensuite** : le modèle analytique reste la source de vérité ; l'apprentissage ne sert qu'à calibrer (garde-fou contre l'extrapolation, exigence d'interprétabilité).
2. **Benchmarks avant fonctionnalités** : chaque module est livré avec son jeu de validation public.
3. **Cœur pur, bindings en aval** : noyau Python sans dépendance SIG ; plugin QGIS et API séparés.
4. **Coût nul par évaluation** : préserver la propriété d'évaluation ponctuelle (objectif : Monte Carlo million d'échantillons sur laptop).
5. **Conformité d'interopérabilité** : formats d'entrée météo compatibles AERMOD/AgDRIFT quand c'est possible ; sorties raster/GeoTIFF géoréférencées.

## Architecture cible

| Module | Rôle | Priorité |
|---|---|---|
| core/similitude | Solutions de similitude jets/panaches/puffs (métrique cartésienne) — portage du chapitre 2008 | M1 |
| core/metric | Métrique non symétrique travel-time (vents non uniformes, topographie) | M1 |
| core/constraints | Conservation, positivité, divergence nulle — tests systématiques | M1 |
| core/levels | Hiérarchie multi-niveaux + estimateur d'erreur entre niveaux (nouveau vs 2008) | M2 |
| assim/calibration | Moindres carrés (M1) → régularisation Tikhonov et calibration bayésienne (M3) | M1→M3 |
| assim/ste | Identification de source (adjoint analytique, suivi des standards STE) | M2 |
| io/ | Météo (CSV/ERA5), MNT (GeoTIFF), émissions ; sorties ponctuelles, profils, rasters | M1–M2 |
| bindings/qgis | Plugin QGIS (équivalent Drift-X 2009, modernisé) | M3 |
| benchmarks/ | Gaussien de référence, comparaisons POD/ROM, cas spray drift publiés | M1 puis continu |

## Jalons

- **M0 — Ancrage documentaire (revue structurée disponible ; reproductibilité à compléter)** : audit, revue d'état de l'art, bibliographie (ce dépôt) ; numérisation et dépôt HAL de la thèse 2006 et du chapitre 2008 ; choix de licence (proposition : GPLv3 pour le code, CC BY 4.0 pour les docs).
- **M1 — Cœur et preuve (T+2 mois)** : modules similitude/metric/constraints + benchmark gaussien classique (cas flat terrain, classes Pasquill) ; CI avec tests physiques (conservation/positivité) ; publication v0.1.
- **M2 — Calibration et multi-niveaux (T+6 mois)** : assimilation de données partielles ; hiérarchie multi-niveaux avec estimateur d'erreur ; identification de source simple ; comparaison publique contre un POD-ML sur un cas académique (article de blog + note technique).
- **M3 — Terrains et GIS (T+12 mois)** : topographie réelle via MNT, cas dérive viticole/drones, plugin QGIS ; validation sur données de campagne publiées.
- **M4 — Article de synthèse (T+15 mois)** : soumission *Environmental Modelling & Software* ou *Atmospheric Environment* : « a priori reduced-order dispersion via travel-time metrics : theory, validation, applications ».
- **M5 — Impact réglementaire (T+24 mois)** : proposition d'extension far-field à l'AGDISP Modernization Project ; dossier de conformité interprétabilité (EU AI Act) pour usage réponse d'urgence.

## Positionnement scientifique (hypothèses d'article)

1. **Hypothèse à tester :** la métrique travel-time généralise les solutions de similitude aux vents non uniformes tout en respectant la conservation de masse dans les conditions précisées — preuve théorique et benchmark requis.
2. **Hypothèse à tester :** la calibration hybride peut être plus robuste hors domaine qu'un surrogate ML comparable — protocole de comparaison et validation indépendante requis.
3. **Hypothèse à tester :** le far-field topographique via métrique peut améliorer la représentation de certains cas par rapport à l'extension gaussienne AGDISP — validation croisée sur campagnes publiées requise.

## Risques et parades

| Risque | Gravité | Parade |
|---|---|---|
| Difficulté d'accès à des données de validation terrain | Élevée | Prioriser les campagnes publiées (tracer studies, essais dérive ouverts) ; générer des cas synthétiques CFD pour la cohérence |
| Concurrence d'un acteur majeur (AMP) | Moyenne | L'AMP réécrit le near-field ; le far-field analytique reste la case vide — viser la complémentarité, pas la confrontation |
| Dérive vers le « tout ML » (facile à démontrer, dur à publier) | Moyenne | Principe 1 gravé dans la roadmap ; benchmarks hors-domaine systématiques |
| Charge de formalisation mathématique de la métrique | Moyenne | Consolider depuis la thèse 2006 ; demander relecture à B. Mohammadi / O. Pironneau (co-auteurs historiques) |

## Critères de sortie des jalons\n\n- **M0 :** requêtes et dates de recherche, critères de sélection, décompte du corpus et limites d'accès consignés ; références vérifiées.\n- **M1 :** benchmark gaussien reproductible, tests physiques automatisés, métriques d'erreur et coût documentés.\n- **M2 :** calibration évaluée sur données distinctes de celles utilisées pour l'ajustement ; comparaison avec une baseline.\n- **M3 :** validation indépendante sur données de terrain et analyse d'incertitude.\n- **M4 :** manuscrit fondé sur les résultats vérifiables, avec limites et résultats négatifs.\n\n## Prochaines actions immédiates

1. Valider cette feuille de route et la licence proposée.
2. Déposer thèse (2006) et chapitre (2008) en archive ouverte.
3. Ouvrir les issues M1 (un issue par module, avec critères d'acceptation).
4. Contact informel avec l'équipe AMP / CREAM (sensibilisation far-field).
