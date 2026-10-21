# raw/ — sources primaires du corpus Drift-X

Ce dossier rassemble les **documents primaires** du corpus historique : les PDF des papiers sources et leurs extractions texte brutes. Objectif : relecture, extraction d'information et traçabilité, au plus près du dépôt (voir <code>docs/04-revues-papiers-sources.md</code> pour les fiches de lecture).

## raw/extracts/ — extractions texte

Extractions automatiques (octobre 2026), grep-ables, avec en-tête documentaire. La mise en page, les figures et les équations n'y sont pas conservées : le PDF original reste la référence.

| Fichier | Contenu | Source d'extraction |
|---|---|---|
| <code>extracts/2006-mohammadi-brun-crmeca.txt</code> | Texte intégral du C. R. Mécanique 2006 (5 pages) | [Archive ouverte de l'Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) |
| <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> | Texte intégral du manuscrit auteur Drift-X (17 pages) | [HAL hal-00468863](https://hal.science/hal-00468863) via relais ResearchGate |

## PDF originaux — inventaire et où les trouver

| Fichier attendu | Source | Où le trouver | Statut |
|---|---|---|---|
| <code>2006-these-brun.pdf</code> | Brun, *Modélisation à complexité réduite de la dérive*, thèse Univ. Montpellier II | En possession de l'auteur | **À ajouter** — puis dépôt HAL (action M0) |
| <code>2006-mohammadi-brun-crmeca.pdf</code> | C. R. Mécanique 334(10), 634–638 | [PDF en accès libre — Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) | **À ajouter** (version éditeur © Académie des sciences/Elsevier — voir note ci-dessous) |
| <code>2006-mohammadi-brun-pironneau-springer.pdf</code> | Chapitre Springer 2006 (avec Pironneau) | Recueil introuvable en ligne | Introuvable à ce jour |
| <code>2008-bozon-mohammadi-sinfort-esta.pdf</code> | e-sta vol. 5, STIC & Environnement'07 | Archives SEE introuvables en ligne | Introuvable à ce jour |
| <code>2008-brun-mohammadi-springer-chap14.pdf</code> | Chapitre Springer CSM 16, chap. 14, p. 245 et s. | En possession de l'auteur ; [page ResearchGate](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion) | **À ajouter** |
| <code>2009-bozon-sinfort-mohammadi-driftx-hal.pdf</code> | Actes STIC & Environnement 2009 | [PDF HAL](https://hal.science/hal-00468863/file/MO2009-PUB00026817.pdf) — manuscrit auteur, dépôt ouvert | **À ajouter** |
| <code>2009-mohammadi-bozon-applied-geomatics.pdf</code> | Applied Geomatics 1, 33–39 | Abonnement Springer / tiré-à-part auteur | **À ajouter** |
| <code>2010-bozon-sinfort-mohammadi-jesa.pdf</code> | JESA 44(4-5), 445–461 | Abonnement Lavoisier ; DOI 10.3166/jesa.44.445-461 | **À ajouter** |

## Comment ajouter les PDF

En local (les outils d'intégration du projet ne versionnent pas les binaires automatiquement) :

~~~
git checkout main
git pull
cp /chemin/vers/les/pdf/*.pdf raw/
git add raw/*.pdf
git commit -m "raw: ajoute les PDF sources du corpus Drift-X"
git push origin main
~~~

Ou via l'interface GitHub : onglet **Add file → Upload files** sur ce dossier.

## Note de prudence (copyright)

- Les **manuscrits auteurs** (thèse, HAL, tirés-à-part acceptés) peuvent être versionnés et déposés sur HAL sans difficulté : c'est la voie propre pour l'archivage public (action M0).
- Les **versions éditeurs** (Académie des sciences/Elsevier, Springer, Lavoisier) restent sous le copyright de l'éditeur même quand elles sont librement téléchargeables : ce dossier est une archive de travail privée du projet ; en cas de doute, ne versionner que les manuscrits auteurs et laisser les liens ci-dessus faire le travail d'accès.
- Les extractions texte de <code>raw/extracts/</code> sont des extraits attribués destinés à l'analyse (recherche/text mining), avec mention complète du copyright dans leur en-tête.
