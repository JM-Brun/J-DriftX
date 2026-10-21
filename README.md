# J-DriftX

**Modélisation à complexité réduite de la dispersion atmosphérique de scalaires passifs** — reprise et modernisation open-source du projet **Drift-X** (J.-M. Brun & B. Mohammadi, 2006–2009).

J-DriftX prédit la dispersion (panaches, puffs, dérive de pulvérisation) via des **solutions de similitude généralisées dans une métrique non symétrique basée sur les temps de transport** — sans résoudre d'EDP ni construire de maillage — avec calibration par **assimilation de données partielles**, évaluation ponctuelle directe, analyse de sensibilité et identification de source.

## Héritage (2006–2009)

| Année | Référence | Support |
|---|---|---|
| 2006 | Thèse : *Modélisation à complexité réduite de la dérive* (J.-M. Brun, Univ. Montpellier II) | — |
| 2006 | *Similitude généralisée et modélisation géométrique à complexité réduite* (Mohammadi & Brun) | C. R. Mécanique 334 |
| 2006 | *Reduced order modelling of dispersion* (Mohammadi, Brun & Pironneau) | Springer |
| 2008 | *Reduced-Order Modelling of Dispersion* (Brun & Mohammadi) | Springer, CSM vol. 16, p. 245 |
| 2008 | *Similitude and non symmetric geometry for dispersion modelling* (Bozon, Mohammadi & Sinfort) | e-sta vol. 5 |
| 2009 | *A GIS-based atmospheric dispersion model* — plateforme Drift-X (QGIS) | HAL hal-00468863 |
| 2009 | *GIS-based atmospheric dispersion modelling* (Mohammadi & Bozon) | Applied Geomatics 1 |

Détails complets : [docs/references.md](docs/references.md)

## Pourquoi reprendre ce projet en 2026 ?

- L'idée fondatrice (**réduction a priori** par information physique, sans snapshots CFD coûteux) n'a pas été démentie : elle préfigure les approches modernes *physics + data*, et reste différenciante face aux ROM-POD et aux surrogate ML actuels.
- Le besoin métier s'est renforcé : far-field de la dérive de pesticides (l'extension gaussienne d'AGDISP est reconnue très conservatrice), réponse d'urgence temps réel, exposition résidentielle aux pesticides.
- Les briques qui manquaient en 2008 existent aujourd'hui : données ouvertes (ERA5, Copernicus, MNT), calcul embarqué, apprentissage pour la calibration, écosystème QGIS mature.

Analyse détaillée : [docs/01-audit-heritage-driftx.md](docs/01-audit-heritage-driftx.md) · [docs/02-revue-etat-art-2026.md](docs/02-revue-etat-art-2026.md) · [docs/03-roadmap-jdriftx-v2.md](docs/03-roadmap-jdriftx-v2.md)

## Structure du dépôt

```
docs/
  01-audit-heritage-driftx.md   # Audit du projet historique Drift-X
  02-revue-etat-art-2026.md     # Revue systémique de l'état de l'art (2008→2026)
  03-roadmap-jdriftx-v2.md      # Orientations futures et feuille de route
  references.md                 # Bibliographie complète (corpus historique + moderne)
```

## Statut

🚧 Reprise en cours — phase 0 (documentation, audit, revue, roadmap). Le noyau Python v2 est spécifié dans la feuille de route ; les contributions seront bienvenues dès la publication du M1.

## Licence

À définir (proposition : GPLv3 ou MIT pour le cœur, données ouvertes sous ODbL). Voir roadmap.
