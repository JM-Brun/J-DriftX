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
| `2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf` | Brun & Mohammadi, chapitre Springer (2008), extrait p. 245–246 | Extrait seulement ; chapitre complet désormais couvert par le recueil ci-dessous |
| — | Glowinski, R. & Neittaanmäki (eds) (2008), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, DOI [10.1007/978-1-4020-8758-5](https://doi.org/10.1007/978-1-4020-8758-5) | Recueil complet non distribué dans ce dépôt ; accès via DOI/publisher. Les notes et l'extrait autorisé du chapitre 14 restent référencés séparément |
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

À compléter : extraction du rapport InVS 2009 (binaire volumineux, 4 Mo). Pour le chapitre 14 du recueil Glowinski & Neittaanmäki, une extraction analytique est disponible dans `extracts/2008-brun-mohammadi-springer-chap14-notes.txt`. Elle ne remplace pas une transcription OCR intégrale vérifiée ; les équations, légendes et figures doivent être contrôlées sur le PDF original.

## PDF encore attendus

| Fichier attendu | Source | Où le trouver |
|---|---|---|
| <code>2007-these-brun.pdf</code> | Brun, *Modélisation à complexité réduite de la dérive*, thèse Univ. Montpellier II (citée comme 2007 dans l'article primaire de 2006 ; année exacte à vérifier) | Indiquée comme en possession de l'auteur — vérifier page de titre, métadonnées et droits avant tout dépôt HAL (action M0) |
| <code>2006-mohammadi-brun-pironneau-reference.pdf</code> | Fichier éventuel pour la référence attribuée à Mohammadi, Brun & Pironneau (2006) | Référence citée secondairement ; recueil et statut éditorial à confirmer, ne pas traiter comme un chapitre Springer établi |
| <code>2008-bozon-mohammadi-sinfort-esta.pdf</code> | e-sta vol. 5, STIC & Environnement’07 | Archives SEE introuvables en ligne à ce jour |
| ~~<code>2008-brun-mohammadi-springer-chap14.pdf</code>~~ | Chapitre complet — désormais couvert par le recueil Glowinski & Neittaanmäki présent dans <code>raw/</code> (23 octobre 2026) ; un fichier chapitre séparé n'est plus nécessaire | Recueil présent ; extraction à poursuivre |
| <code>2009-bozon-mohammadi-applied-geomatics.pdf</code> | Applied Geomatics 1, 59–74 | Abonnement Springer / tiré-à-part auteur |
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

## Politique de réutilisation et copyright

- Ne versionner que les documents dont la licence ou les droits de redistribution sont établis. Un téléchargement libre ne signifie pas que le dépôt public est autorisé.
- Pour les versions éditeurs, conserver la référence bibliographique et le DOI/lien éditeur plutôt que le PDF intégral, sauf autorisation explicite de redistribution.
- Préférer les manuscrits auteurs déposés légalement en archive ouverte, en vérifiant la version et les conditions applicables.
- Vérifier la licence et la provenance des jeux de données, figures et extractions avant de les redistribuer ou de les utiliser dans un benchmark public.
- Le recueil Glowinski & Neittaanmäki (2008) n'est pas distribué dans ce dépôt ; accès via le DOI ci-dessus. L'extrait et les notes du chapitre 14 ne remplacent pas le texte original.
- Les extractions texte de <code>extracts/</code> restent des matériaux attribués destinés à l'analyse ; leur redistribution doit être évaluée au cas par cas, sans supposer qu'une mention du copyright suffit à autoriser la republication.


## Revue de l'état de l'art et traçabilité

Les deux résumés exécutifs de la revue sont conservés dans `raw/reviews/`. Ils ne remplacent pas les articles scientifiques primaires qu'ils citent. Leurs références sont organisées en Markdown éditable dans [la bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md), avec une fiche par famille de méthodes.

Les décisions qui découlent de la revue doivent être synthétisées dans [`docs/07-plan-integration-revue-systematique.md`](../docs/07-plan-integration-revue-systematique.md), en reliant chaque décision aux sections de la revue, aux sources vérifiées, aux limites de preuve et aux critères d'acceptation associés. Les PDF bruts sont conservés sans modification de contenu.

Ne pas confondre une synthèse de revue avec une source primaire ni compter comme indépendantes deux versions d'un même travail sans vérifier leurs différences.


Le rapport final de revue systématique sera ajouté par le mainteneur dans ce dossier. Son fichier exact sera indiqué ici après dépôt. Le rapport est une source de travail ; les décisions qui en découlent doivent être synthétisées séparément dans docs/07-plan-integration-revue-systematique.md, avec les références vérifiées, les limites de preuve et les critères d'acceptation associés.

Ne pas remplacer les PDF historiques ni confondre le rapport de revue avec les sources primaires qu'il cite. Si le rapport contient des exports bibliographiques ou des données de sélection, les conserver avec leur provenance et leur format d'origine.
