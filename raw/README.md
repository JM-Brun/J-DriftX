# raw/ — sources primaires et documents de travail

Ce dossier rassemble les **documents sources** du projet : corpus historique Drift-X, références théoriques et documents contextuels. Chaque source dispose d'une **fiche de lecture** (un markdown par source, dans <code>fiches/</code>) et, quand le texte a pu être extrait, d'une **extraction texte brute** (dans <code>extracts/</code>). Objectif : relecture, extraction d'information et traçabilité, au plus près du dépôt (les revues détaillées du corpus sont dans <code>docs/04-revues-papiers-sources.md</code>).

## Organisation

- un PDF par source, nommé selon la convention <code>AAAA-auteur-sujet.pdf</code> (année de publication d'abord, auteurs, puis sujet court) ;
- une fiche de lecture par source : <code>fiches/AAAA-auteur-sujet.md</code> — référence, revue, informations extraites, valeur pour J-DriftX ;
- <code>extracts/</code> : extractions texte brutes, grep-ables, avec en-tête documentaire (la mise en page, les figures et les équations n'y sont pas conservées : le PDF original reste la référence).

## Provenance obligatoire par fichier

**Chaque fichier doit indiquer d'où il vient.** Pour chaque PDF binaire conservé dans `raw/` ou `raw/reviews/`, une fiche sidecar correspondante est maintenue dans `raw/provenance/`. Elle donne la notice et le site source, l'URL exacte disponible, les pages conservées, le nom initial, la méthode d'obtention connue, les fichiers dérivés et les limites de preuve. Pour les fichiers textuels, l'en-tête doit inclure l'URL/page source, la méthode d'extraction et les pages concernées ; pour les notes analytiques, distinguer clairement la source bibliographique officielle du fichier effectivement consulté. Les inconnues sont marquées comme telles, jamais devinées.

## Sources PDF présentes

Les fichiers du corpus historique utilisent déjà la convention `AAAA-auteur-sujet.pdf`. La table ci-dessous documente les sources conservées dans `raw/`.

| Fichier | Source | Fiche / état |
|---|---|---|
| `2006-mohammadi-brun-crmeca.pdf` | Mohammadi & Brun, *C. R. Mécanique* (2006), DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007) | PDF éditeur de 5 pages et extraction automatique disponibles ; la revue publique qualifie désormais la lecture de partielle (PR #143), car l'accès direct au PDF n'a pas pu être vérifié dans l'environnement de relecture |
| `2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf` | Brun & Mohammadi, chapitre Springer (2008), extrait p. 245–246 | Extrait de deux pages seulement ; les pages restantes nécessitent une source légalement accessible |
| Référence bibliographique du recueil Springer 2008 (PDF intégral non distribué) | Glowinski, R. & Neittaanmäki (eds) (2008), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, Dordrecht, DOI [10.1007/978-1-4020-8758-5](https://doi.org/10.1007/978-1-4020-8758-5) — chapitre 14, Brun & Mohammadi, pp. 245–256, DOI [10.1007/978-1-4020-8758-5_14](https://doi.org/10.1007/978-1-4020-8758-5_14) | Référence et provenance historique conservées ; le recueil complet a été retiré par la PR #67. Le PDF local restant ne couvre que les pages 245–246 ; les notes analytiques ne sont pas un OCR intégral |
| `2009-bozon-sinfort-mohammadi-driftx-hal.pdf` | Bozon, Sinfort & Mohammadi, manuscrit Drift-X (2009), [HAL hal-00468863](https://hal.science/hal-00468863) | Manuscrit auteur et extraction texte disponibles |
| `2009-invs-exposition-aerienne-pesticides-herault.pdf` | InVS / Santé publique France (2009), mesures d'exposition aux pesticides dans l'Hérault | Rapport d'agence ; lecture ciblée documentée, extraction intégrale reproductible encore à produire |
| `reviews/2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf` | Résumé exécutif de la revue, partie 1 | Synthèse PDF ; voir la cartographie éditable |
| `reviews/2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf` | Résumé exécutif de la revue, partie 2 | Synthèse PDF ; voir la cartographie éditable |

Les fiches Markdown décrivant les liens scientifiques entre les références et le projet sont centralisées dans [la bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md). Cette cartographie distingue les sources fondatrices, les baselines concurrentes, les méthodes complémentaires, les analogies conceptuelles et les références de contexte applicatif.

## raw/extracts/ — extractions texte

| Fichier | Contenu | Source d'extraction |
|---|---|---|
| <code>extracts/2006-mohammadi-brun-crmeca.txt</code> | Texte intégral du C. R. Mécanique 2006 (5 pages) | [Archive ouverte de l'Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) |
| <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> | Texte intégral du manuscrit auteur Drift-X (17 pages) | [HAL hal-00468863](https://hal.science/hal-00468863) via relais ResearchGate |

Pour le rapport InVS 2009, une lecture ciblée paraphrasée est disponible dans `extracts/2009-invs-exposition-aerienne-pesticides-herault-lecture-ciblee.md`. Elle documente les tableaux de concentrations consultés et leurs limites ; ce n'est ni un OCR intégral ni une transcription exhaustive. Une extraction complète reproductible reste à produire, après vérification de l'identité du PDF local avec la version officielle. Pour le chapitre 14 du recueil Glowinski & Neittaanmäki, `extracts/2008-brun-mohammadi-springer-chap14-notes.txt` est une note analytique, pas un OCR verbatim ; les équations, légendes et figures doivent être contrôlées sur le PDF original.

## PDF encore attendus

| Fichier attendu | Source | Où le trouver |
|---|---|---|
| <code>2007-these-brun.pdf</code> | Brun, *Modélisation à complexité réduite de la dérive*, thèse Univ. Montpellier II (citée comme 2007 dans l'article primaire de 2006 ; année exacte à vérifier) | Indiquée comme en possession de l'auteur — vérifier page de titre, métadonnées et droits avant tout dépôt HAL (action M0) |
| <code>2006-mohammadi-brun-pironneau-reference.pdf</code> | Fichier éventuel pour la référence attribuée à Mohammadi, Brun & Pironneau (2006) | Référence citée secondairement ; recueil et statut éditorial à confirmer, ne pas traiter comme un chapitre Springer établi |
| <code>2008-bozon-mohammadi-sinfort-esta.pdf</code> | e-sta vol. 5, STIC & Environnement’07 | Archives SEE introuvables en ligne à ce jour |
| ~~<code>2008-brun-mohammadi-springer-chap14.pdf</code>~~ | Chapitre complet non versionné faute d'autorisation de redistribution établie | Utiliser une source légalement accessible ; l'extrait local ne couvre que les pages 245–246 |
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

## Note de prudence (copyright)

- Les **manuscrits auteurs** (thèse, HAL, tirés-à-part acceptés) peuvent être versionnés et déposés sur HAL sans difficulté : c'est la voie propre pour l'archivage public (action M0).
- Les **versions éditeurs** (Académie des sciences/Elsevier, Springer, Lavoisier, Persée) restent soumises aux droits applicables même quand elles sont librement téléchargeables : l'accès en ligne ne vaut pas autorisation de redistribution. En cas de doute, privilégier les manuscrits auteurs autorisés et les liens DOI plutôt que le versionnement du PDF éditeur.
- Le **recueil Glowinski & Neittaanmäki (2008)** n'est plus versionné dans ce dépôt après la PR #67. Sa référence bibliographique, ses DOI et la fiche de provenance historique sont conservés ; le binaire complet n'est pas redistribué. Les notes analytiques proviennent d'une copie historiquement consultée sur un miroir tiers.
- Le **rapport InVS / Santé publique France** est un document public d'agence sanitaire : diffusion libre avec citation de la source.
- Les extractions texte de <code>extracts/</code> sont des extraits attribués destinés à l'analyse (recherche/text mining), avec mention complète du copyright dans leur en-tête.


## Revue de l'état de l'art et traçabilité

Les deux résumés exécutifs de la revue sont conservés dans `raw/reviews/`. Ils ne remplacent pas les articles scientifiques primaires qu'ils citent. Leurs références sont organisées en Markdown éditable dans [la bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md), avec une fiche par famille de méthodes.

Les synthèses publiques des résultats de la revue se trouvent dans `docs/02-revue-etat-art-2026.md`, `docs/04-revues-papiers-sources.md` et la [bibliographie annotée](../docs/bibliographie-annotee-jdriftx.md). Le plan d'intégration détaillé est conservé dans les notes privées associées au projet. Les PDF sources sont conservés sans modification de contenu.

Ne pas confondre une synthèse de revue avec une source primaire ni compter comme indépendantes deux versions d'un même travail sans vérifier leurs différences.


Le rapport final de revue systématique sera ajouté par le mainteneur dans ce dossier. Son fichier exact sera indiqué ici après dépôt. Le rapport est une source de travail ; les résultats utiles à la compréhension publique doivent être synthétisés dans les documents scientifiques publics, avec les références vérifiées et les limites de preuve. Le suivi opérationnel des décisions reste dans les notes privées associées.

Ne pas remplacer les PDF historiques ni confondre le rapport de revue avec les sources primaires qu'il cite. Si le rapport contient des exports bibliographiques ou des données de sélection, les conserver avec leur provenance et leur format d'origine.
