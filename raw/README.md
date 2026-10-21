# raw/ — sources primaires et documents de travail

Ce dossier rassemble les **documents sources** du projet : corpus historique Drift-X, références théoriques et documents contextuels. Chaque source dispose d'une **fiche de lecture** (un markdown par source, dans <code>fiches/</code>) et, quand le texte a pu être extrait, d'une **extraction texte brute** (dans <code>extracts/</code>). Objectif : relecture, extraction d'information et traçabilité, au plus près du dépôt (les revues détaillées du corpus sont dans <code>docs/04-revues-papiers-sources.md</code>).

## Organisation

- un PDF par source, nommé selon la convention <code>AAAA-auteur-sujet.pdf</code> (année de publication d'abord, auteurs, puis sujet court) ;
- une fiche de lecture par source : <code>fiches/AAAA-auteur-sujet.md</code> — référence, revue, informations extraites, valeur pour J-DriftX ;
- <code>extracts/</code> : extractions texte brutes, grep-ables, avec en-tête documentaire (la mise en page, les figures et les équations n'y sont pas conservées : le PDF original reste la référence).

## Fichiers présents et renommage recommandé

Les PDF ont été ajoutés avec leurs noms d'origine (téléchargement, dépôt) ; le tableau ci-dessous donne le renommage recommandé vers la convention du projet. Les binaires ne peuvent pas être renommés par les outils d'intégration (texte seul) : les commandes sont données plus bas.

| Fichier actuel | Renommage recommandé | Source | Fiche de lecture |
|---|---|---|---|
| <code>CRMECA_2006__334_10_634_0.pdf</code> | <code>2006-mohammadi-brun-crmeca.pdf</code> | C. R. Mécanique 334(10), 634–638 — version éditeur, [accès libre (Académie des sciences)](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) | <code>fiches/2006-mohammadi-brun-crmeca.md</code> |
| <code>PDF.js viewer.pdf</code> | <code>2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf</code> | Chapitre Springer CSM 16, chap. 14 — extrait de 2 pages (p. 245–246) | <code>fiches/2008-brun-mohammadi-springer-chap14.md</code> |
| <code>MO2009-PUB00026817.pdf</code> | <code>2009-bozon-sinfort-mohammadi-driftx-hal.pdf</code> | Manuscrit auteur, [HAL hal-00468863](https://hal.science/hal-00468863) | <code>fiches/2009-bozon-sinfort-mohammadi-driftx-hal.md</code> |
| <code>82748_9958-9958-ps.pdf</code> | <code>2009-invs-exposition-aerienne-pesticides-herault.pdf</code> | Rapport InVS / [Santé publique France](https://www.santepubliquefrance.fr/content/download/186474/document_file/82748_9958-9958-ps.pdf), 2009 | <code>fiches/2009-invs-exposition-aerienne-pesticides-herault.md</code> |
| Rapport de l'état de l'art sur la dérive conceptuelle et positionnement de J-DriftX.pdf | <code>2026-rapport-derive-conceptuelle-positionnement-jdriftx.pdf</code> | Document de travail de l'auteur (2026, hors corpus Drift-X) | <code>fiches/2026-rapport-derive-conceptuelle-positionnement-jdriftx.md</code> |

Commandes de renommage (branche de la PR en cours) :

~~~
git checkout feat/images-metriques
git pull
cd raw
git mv CRMECA_2006__334_10_634_0.pdf 2006-mohammadi-brun-crmeca.pdf
git mv "PDF.js viewer.pdf" 2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf
git mv MO2009-PUB00026817.pdf 2009-bozon-sinfort-mohammadi-driftx-hal.pdf
git mv 82748_9958-9958-ps.pdf 2009-invs-exposition-aerienne-pesticides-herault.pdf
git mv Rapport*.pdf 2026-rapport-derive-conceptuelle-positionnement-jdriftx.pdf
cd ..
git commit -m "raw: renomme les PDF selon la convention AAAA-auteur-sujet"
git push origin feat/images-metriques
~~~

## raw/extracts/ — extractions texte

| Fichier | Contenu | Source d'extraction |
|---|---|---|
| <code>extracts/2006-mohammadi-brun-crmeca.txt</code> | Texte intégral du C. R. Mécanique 2006 (5 pages) | [Archive ouverte de l'Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) |
| <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> | Texte intégral du manuscrit auteur Drift-X (17 pages) | [HAL hal-00468863](https://hal.science/hal-00468863) via relais ResearchGate |

À compléter : extraction du rapport InVS 2009 (binaire volumineux, 4 Mo) et du chapitre Springer complet quand il sera ajouté.

## PDF encore attendus

| Fichier attendu | Source | Où le trouver |
|---|---|---|
| <code>2006-these-brun.pdf</code> | Brun, *Modélisation à complexité réduite de la dérive*, thèse Univ. Montpellier II | En possession de l'auteur — puis dépôt HAL (action M0) |
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
