# raw/ — sources primaires et documents de travail

Ce dossier rassemble les **documents sources** du projet : corpus historique Drift-X, références théoriques et documents contextuels. Chaque source dispose d'une **fiche de lecture** (un markdown par source, dans <code>fiches/</code>) et, quand le texte a pu être extrait, d'une **extraction texte brute** (dans <code>extracts/</code>). Objectif : relecture, extraction d'information et traçabilité, au plus près du dépôt (les revues détaillées du corpus sont dans <code>docs/04-revues-papiers-sources.md</code>).

## Organisation

- un PDF par source, nommé selon la convention <code>AAAA-auteur-sujet.pdf</code> (année de publication d'abord, auteurs, puis sujet court) ;
- une fiche de lecture par source : <code>fiches/AAAA-auteur-sujet.md</code> — référence, revue, informations extraites, valeur pour J-DriftX ;
- <code>extracts/</code> : extractions texte brutes, grep-ables, avec en-tête documentaire (la mise en page, les figures et les équations n'y sont pas conservées : le PDF original reste la référence).

## Sources PDF présentes

Les fichiers du corpus historique utilisent déjà la convention `AAAA-auteur-sujet.pdf`. La table ci-dessous documente les sources conservées dans `raw/`.

| Fichier | Source | Fiche / état |
|---|---|---|
| `2006-mohammadi-brun-crmeca.pdf` | Mohammadi & Brun, *C. R. Mécanique* (2006), DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007) | Texte intégral et extraction texte disponibles |
| `2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf` | Brun & Mohammadi, chapitre Springer (2008), extrait p. 245–246 | Extrait seulement ; chapitre complet à retrouver |
| `2009-bozon-sinfort-mohammadi-driftx-hal.pdf` | Bozon, Sinfort & Mohammadi, manuscrit Drift-X (2009), [HAL hal-00468863](https://hal.science/hal-00468863) | Manuscrit auteur et extraction texte disponibles |
| `2009-invs-exposition-aerienne-pesticides-herault.pdf` | InVS / Santé publique France (2009), mesures d'exposition aux pesticides dans l'Hérault | Rapport d'agence ; données détaillées à vérifier |
| `2026-rapport-derive-conceptuelle-positionnement-jdriftx.pdf` | Rapport de travail sur la dérive conceptuelle et le positionnement (2026) | Document de travail, pas une source primaire scientifique |
| `reviews/2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf` | Résumé exécutif de la revue, partie 1 | Synthèse PDF ; voir la cartographie éditable |
| `reviews/2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf` | Résumé exécutif de la revue, partie 2 | Synthèse PDF ; voir la cartographie éditable |

Les fiches Markdown décrivant les liens scientifiques entre les références et le projet sont centralisées dans [la bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md). Cette cartographie distingue les sources fondatrices, les baselines concurrentes, les méthodes complémentaires, les analogies conceptuelles et les références de contexte applicatif.

## raw/extracts/ — extractions texte

| Fichier | Contenu | Source d'extraction |
|---|---|---|
| <code>extracts/2006-mohammadi-brun-crmeca.txt</code> | Texte intégral du C. R. Mécanique 2006 (5 pages) | [Archive ouverte de l'Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) |
| <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> | Texte intégral du manuscrit auteur Drift-X (17 pages) | [HAL hal-00468863](https://hal.science/hal-00468863) via relais ResearchGate |

À compléter : extraction du rapport InVS 2009 (binaire volumineux, 4 Mo) et du chapitre Springer complet quand il sera ajouté.

## PDF encore attendus

| Fichier attendu | Source | Où le trouver |
|---|---|---|
| <code>2007-these-brun.pdf</code> | Brun, *Modélisation à complexité réduite de la dérive*, thèse Univ. Montpellier II (citée comme 2007 dans l'article primaire de 2006 ; année exacte à vérifier) | Indiquée comme en possession de l'auteur — vérifier page de titre, métadonnées et droits avant tout dépôt HAL (action M0) |
| <code>2006-mohammadi-brun-pironneau-springer.pdf</code> | Chapitre Springer 2006 (avec Pironneau) | Recueil introuvable en ligne à ce jour |
| <code>2008-bozon-mohammadi-sinfort-esta.pdf</code> | e-sta vol. 5, STIC & Environnement'07 | Archives SEE introuvables en ligne à ce jour |
| <code>2008-brun-mohammadi-springer-chap14.pdf</code> | Chapitre complet (seul un extrait de 2 pages est présent) | En possession de l'auteur ; [page ResearchGate](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion) |
| <code>2009-mohammadi-bozon-applied-geomatics.pdf</code> | Applied Geomatics 1, 33–39 | Abonnement Springer / tiré-à-part auteur |
| <code>2010-bozon-sinfort-mohammadi-jesa.pdf</code> | JESA 44(4-5), 445–461 | Abonnement Lavoisier ; DOI 10.3166/jesa.44.445-461 |
| <code>1979-muller-espace-geographique.pdf</code> | Muller, *La cartographie d'une métrique non euclidienne : les distances-temps*, L'Espace géographique 8(3), 215–227 | [Persée](https://www.persee.fr/doc/spgeo_0046-2497_1979_num_8_3_1915) — référence théorique (métriques non riemanniennes), hors corpus Drift-X |

## Comment ajouter d'autres PDF

En local (les outils d'intégration du projet ne versionnent pas les binaires automatiquement) :

~~~
git checkout feat/images-metriques
git pull
cp /chemin/vers/le.pdf raw/
git add raw/*.pdf
git commit -m "raw: ajoute ..."
git push origin feat/images-metriques
~~~

Ou via l'interface GitHub : onglet **Add file → Upload files** sur ce dossier, en sélectionnant la branche de la PR en cours.

## Note de prudence (copyright)

- Les **manuscrits auteurs** (thèse, HAL, tirés-à-part acceptés) peuvent être versionnés et déposés sur HAL sans difficulté : c'est la voie propre pour l'archivage public (action M0).
- Les **versions éditeurs** (Académie des sciences/Elsevier, Springer, Lavoisier, Persée) restent sous le copyright de l'éditeur même quand elles sont librement téléchargeables : ce dossier est une archive de travail du projet ; en cas de doute, ne versionner que les manuscrits auteurs et laisser les liens ci-dessus faire le travail d'accès.
- Le **rapport InVS / Santé publique France** est un document public d'agence sanitaire : diffusion libre avec citation de la source.
- Les extractions texte de <code>extracts/</code> sont des extraits attribués destinés à l'analyse (recherche/text mining), avec mention complète du copyright dans leur en-tête.


## Revue de l'état de l'art et traçabilité

Les deux résumés exécutifs de la revue sont conservés dans `raw/reviews/`. Ils ne remplacent pas les articles scientifiques primaires qu'ils citent. Leurs références sont organisées en Markdown éditable dans [la bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md), avec une fiche par famille de méthodes.

Les décisions qui découlent de la revue doivent être synthétisées dans [`docs/07-plan-integration-revue-systematique.md`](../docs/07-plan-integration-revue-systematique.md), en reliant chaque décision aux sections de la revue, aux sources vérifiées, aux limites de preuve et aux critères d'acceptation associés. Les PDF bruts sont conservés sans modification de contenu.

Ne pas confondre une synthèse de revue avec une source primaire ni compter comme indépendantes deux versions d'un même travail sans vérifier leurs différences.


Le rapport final de revue systématique sera ajouté par le mainteneur dans ce dossier. Son fichier exact sera indiqué ici après dépôt. Le rapport est une source de travail ; les décisions qui en découlent doivent être synthétisées séparément dans docs/07-plan-integration-revue-systematique.md, avec les références vérifiées, les limites de preuve et les critères d'acceptation associés.

Ne pas remplacer les PDF historiques ni confondre le rapport de revue avec les sources primaires qu'il cite. Si le rapport contient des exports bibliographiques ou des données de sélection, les conserver avec leur provenance et leur format d'origine.
