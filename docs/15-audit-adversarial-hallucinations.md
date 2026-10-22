# Audit adversarial des affirmations et références — 2026-10-22

> **Statut : audit initial, non exhaustif.** Ce document distingue une référence inexistante d'une référence non retrouvée, une erreur bibliographique d'une affirmation scientifique non démontrée. « Non vérifié » ne signifie pas « faux ». L'audit porte sur les documents présents dans `main` à la date indiquée et sur quelques contrôles externes ciblés. Il ne remplace pas une vérification systématique ligne à ligne de chaque fichier et de chaque PDF.

## 1. Résumé exécutif

Aucune preuve suffisante n'a été trouvée pour qualifier une référence historique centrale de « fausse » au sens strict. Plusieurs entrées sont toutefois **insuffisamment vérifiées ou présentées avec un degré de certitude trop élevé**. Le risque principal observé est la transformation d'une citation secondaire, d'une soumission annoncée ou d'une hypothèse en fait bibliographique/scientifique établi.

Priorités :
1. résoudre l'identité et l'année de la thèse de Brun (2006/2007, et variantes du titre) ;
2. ne pas présenter la soumission IJNMF de 2006 comme un article publié ;
3. vérifier la référence du chapitre Springer 2006 attribué à Mohammadi, Brun et Pironneau à partir d'un catalogue éditeur/bibliothèque ;
4. vérifier que les résumés exécutifs de la revue systématique sont traités comme documents secondaires, jamais comme preuve primaire ;
5. maintenir une séparation stricte entre résultats historiques publiés, hypothèses J-DriftX, et résultats effectivement reproduits par le code actuel.

## 2. Registre des constats

### A-01 — Thèse de J.-M. Brun : année et titre non résolus

- **Statut :** incohérence bibliographique confirmée ; identité exacte à résoudre.
- **Emplacement :** `README.md`, `docs/04-revues-papiers-sources.md`, `raw/fiches/*`, `raw/README.md`.
- **Constat :** le dépôt utilise « *Modélisation à complexité réduite de la dérive* », avec une année tantôt 2006, tantôt 2007. La page de l'article primaire de Mohammadi & Brun (2006) cite la thèse comme 2007, tandis que d'autres références la citent comme 2006. Un résultat ResearchGate associe aussi à J.-M. Brun une thèse de 2007 au titre différent « *Modèles à complexité réduite de transport pour applications environnementales* ». Ces éléments ne suffisent pas à établir s'il s'agit d'une variation de titre, d'une date de soutenance/dépôt, ou d'une notice distincte.
- **Source primaire de contrôle :** [article de 2006 et sa bibliographie](https://comptes-rendus.academie-sciences.fr/mecanique/articles/10.1016/j.crme.2006.06.007/).
- **Correction sûre :** jusqu'à vérification de la page de titre ou d'une notice institutionnelle, afficher « thèse de J.-M. Brun, titre/année à confirmer (citée comme 2006 ou 2007 selon les sources) ». Ne pas affirmer qu'elle n'a jamais été déposée/numérisée sans recherche documentée, datée et reproductible dans les catalogues concernés.
- **Preuve de clôture :** page de titre du document ou notice institutionnelle stable ; enregistrer séparément année de soutenance, année de dépôt et titre exact.

### A-02 — « Reduced-order geometrical modelling of dispersion », IJNMF, 2006

- **Statut :** publication non confirmée ; la source primaire consultée la présente comme « submitted for publication ».
- **Emplacement :** `docs/04-revues-papiers-sources.md`, `raw/fiches/2006-mohammadi-brun-crmeca.md`, `docs/references.md`.
- **Constat :** la bibliographie de l'article de 2006 mentionne B. Mohammadi et J.-M. Brun, « Reduced-order geometrical modelling of dispersion », *Int. J. Num. Meth. Fluids*, 2006, « submitted for publication ». Une soumission n'est pas une preuve de publication ultérieure. Les recherches ciblées réalisées pour cet audit n'ont pas établi de notice éditeur, volume, pages ou DOI pour cet intitulé.
- **Source primaire :** [PDF de l'article de 2006](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf).
- **Correction sûre :** classer comme « manuscrit/soumission mentionné dans la bibliographie de 2006 ; publication ultérieure non confirmée », pas comme article publié. Ne pas inventer de DOI ni de pagination. Une absence de résultat de recherche ne prouve toutefois pas l'inexistence du manuscrit.

### A-03 — Référence attribuée à Mohammadi, Brun et Pironneau (2006), statut éditorial non confirmé

- **Statut :** référence secondaire, métadonnées incomplètes ; existence et contenu exacts à confirmer.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, `raw/README.md`.
- **Constat :** une bibliographie publiée cite « Reduced order modelling of dispersion » avec les auteurs Mohammadi, Brun et Pironneau (2006), et l'associe à un recueil intitulé *Numerical Analysis and Scientific Computing with PDE and their Challenging Applications*. Cela atteste l'existence de la citation, pas à lui seul celle d'un chapitre publié dans cet ouvrage. Aucune notice éditoriale primaire confirmant cet enregistrement n'a été établie lors de cette passe.
- **Correction sûre :** garder l'entrée dans une section « références signalées mais non vérifiées » ; ne pas lui attribuer de résultats, de citations textuelles ni de contenu précis avant d'avoir une notice catalogue/éditeur ou le chapitre lui-même. Le chapitre distinct de Brun & Mohammadi (2008), *Reduced-Order Modelling of Dispersion*, pages 245–256, DOI 10.1007/978-1-4020-8758-5_14, est confirmé par la notice officielle Springer : https://link.springer.com/book/10.1007/978-1-4020-8758-5.
- **Preuve de clôture :** notice éditeur ou catalogue de bibliothèque avec titre, auteurs, ouvrage, année et pagination pour la référence 2006. Ne pas confondre cette recherche avec la notice Springer confirmée du chapitre de 2008.

### A-04 — Thèse et chapitres : accès au document vs informations déduites

- **Statut :** risque de formulation trop catégorique.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, `raw/README.md`, fiches de sources.
- **Constat :** le dépôt distingue utilement les documents lus, les extraits OCR et les références secondaires, mais certaines formulations comme « jamais déposée/numérisée » dépassent ce que prouve « non trouvée lors des recherches effectuées ». Une fiche de référence peut également donner l'impression que le chapitre entier a été relu alors que seul un extrait est archivé.
- **Correction sûre :** employer des statuts normalisés : « texte intégral lu », « extrait lu (pages précisées) », « résumé seul », « cité par une source secondaire », « notice bibliographique vérifiée », « non localisé à la date du … ». Attacher chaque résumé/affirmation à la page ou section réellement consultée.
- **Preuve de clôture :** matrice source × accès × pages lues × affirmations appuyées, mise à jour lors de chaque nouvelle lecture.

### A-05 — Article HAL 2009 et article JESA 2010 : risque de double comptage

- **Statut :** même lignée/travail à rapprocher, pas deux preuves indépendantes sans comparaison.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, `docs/bibliographie-annotee-jdriftx.md`, `raw/README.md`.
- **Constat :** le dépôt signale le manuscrit « A GIS-based atmospheric dispersion model » sur HAL (hal-00468863, version du 31 mars 2010) et une version de revue *JESA* 44(4–5), 445–461 (2010), DOI 10.3166/jesa.44.445-461. Une notice publique confirme le titre, les auteurs et le DOI de la version JESA. Il ne faut donc pas compter automatiquement le manuscrit HAL et l'article de revue comme deux études indépendantes.
- **Sources :** [notice ResearchGate avec DOI et métadonnées JESA](https://www.researchgate.net/publication/42782194_A_GIS-based_atmospheric_dispersion_model) ; [manuscrit HAL](https://hal.science/hal-00468863).
- **Correction sûre :** relier les deux notices comme versions d'un même travail et documenter les différences de contenu, date et pagination avant toute synthèse quantitative. Conserver séparément l'article distinct de *Applied Geomatics* (2009), sans présumer qu'il s'agit du même texte.

### A-06 — Facteur de gain de coût 10³–10⁴ : résultat historique, pas promesse actuelle

- **Statut :** affirmation publiée à contextualiser ; pas une performance vérifiée de J-DriftX.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, fiches 2006, roadmap et éventuelles pages de présentation.
- **Constat :** l'article Mohammadi & Brun (2006) rapporte un gain d'environ 10³–10⁴ par point dans ses exemples, comparé à une simulation de référence donnée par les auteurs. Ce chiffre dépend du cas, de l'implémentation, du nombre de points et du périmètre du coût mesuré. Il ne peut pas être transposé au code Python actuel, à un autre domaine ou au coût total (calibration, préparation du champ, assimilation et validation) sans nouveau benchmark.
- **Source :** [article primaire de 2006](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf).
- **Correction sûre :** toujours écrire « les auteurs rapportent, pour les exemples de leur article… » et fournir la comparaison exacte ; présenter toute performance J-DriftX comme « non mesurée » jusqu'à un benchmark reproductible à précision comparable.

### A-07 — « Sans résolution d'EDP », « sans maillage » : portée historique à circonscrire

- **Statut :** description d'une approche historique, pas preuve d'absence de toute résolution PDE dans la chaîne complète.
- **Emplacement :** README, pages de positionnement et revue.
- **Constat :** les résumés de 2006 et 2008 présentent une évaluation à faible coût ne nécessitant pas de résoudre directement l'EDP sur le domaine pour chaque évaluation. L'article de 2006 compare toutefois la méthode à un modèle de référence résolvant une équation de transport-diffusion-dépôt par éléments finis. La formulation ne doit pas laisser entendre que la méthode a été validée sans modèle de référence, ni que toute préparation/calibration est sans calcul numérique.
- **Correction sûre :** préciser « l'évaluation réduite décrite par les auteurs ne résout pas l'EDP complète à chaque point d'évaluation » ; décrire séparément les calculs de construction, assimilation et référence.

### A-08 — Revue systématique : méthode de reporting ≠ preuve d'exhaustivité

- **Statut :** risque méthodologique connu, déjà partiellement reconnu dans le dépôt.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, `docs/05-plan-validation-et-integration.md`, `docs/06-choix-methode-revue-systematique.md`, pages Quarto et résumés exécutifs dans `raw/reviews/`.
- **Constat :** PRISMA 2020 est une ligne directrice de reporting. Sa mention ne prouve pas à elle seule que la recherche documentaire est exhaustive, reproductible ou évaluée sur le risque de biais. Il faut des sources et dates de recherche, requêtes exactes, critères d'éligibilité, nombres réellement observés aux étapes de sélection, raisons d'exclusion et méthode d'évaluation critique.
- **Source de méthode :** [PRISMA 2020 — site officiel](https://www.prisma-statement.org/prisma-2020) ; [article explicatif en accès libre](https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/).
- **Correction sûre :** ne pas appeler la revue « exhaustive » ou « entièrement reproductible » avant d'avoir produit et vérifié les éléments ci-dessus. Les documents de synthèse stockés dans `raw/reviews/` ne sont pas des sources primaires et ne peuvent pas confirmer eux-mêmes les affirmations qu'ils rapportent.

### A-09 — Hypothèses de conservation, divergence et propriétés de la pseudo-distance

- **Statut :** point mathématique à contrôler proposition par proposition, sans généralisation.
- **Emplacement :** documentation scientifique et implémentation.
- **Constat :** les sources historiques imposent certaines contraintes physiques et décrivent une pseudo-distance non symétrique qui peut ne pas séparer les points et violer l'inégalité triangulaire. Cela ne suffit pas à démontrer que toute construction J-DriftX conserve exactement la masse sur toute surface iso-temps, pour tout champ de vitesse ou en présence de sources, puits, stagnations et caractéristiques non uniques.
- **Correction sûre :** pour chaque affirmation de conservation, donner l'équation, les hypothèses (régularité, stationnarité, divergence, conditions aux limites, source/puits, unicité de caractéristique/projection) et une preuve ou un contre-exemple. Séparer les propriétés citées de la source historique des propriétés démontrées pour le modèle actuel.

## 3. Échelle de confiance à utiliser dans les futures fiches

- **Vérifié sur source primaire :** notice officielle ou texte intégral consulté ; localiser l'affirmation (page, section, équation).
- **Métadonnées vérifiées, contenu non lu :** DOI/éditeur/catalogue confirmé, mais pas de conclusion sur le contenu.
- **Rapporté par une source secondaire :** attribuer explicitement l'information à cette source ; ne pas la traiter comme vérification indépendante.
- **Non localisé / non confirmé au [date] :** indique l'état de la recherche, jamais une preuve d'inexistence.
- **Hypothèse de J-DriftX :** proposition à tester, non résultat.
- **Résultat reproduit :** protocole, code, données, métrique, baseline et sortie vérifiables.
- **Réfuté / erroné :** réserver ce statut à une contradiction positive démontrée.

## 4. Protocole de traque continue

Pour chaque référence ou affirmation non triviale :
1. Vérifier titre, auteurs, année, support, volume/pages et DOI/URL dans une source bibliographique primaire ou un catalogue institutionnel.
2. Résoudre DOI/URL et comparer les métadonnées de la page cible avec la citation.
3. Lire le texte primaire pertinent ; enregistrer pages, équations, conditions et limites.
4. Rechercher les versions (prépublication, manuscrit auteur, article final) et éviter le double comptage.
5. Pour les affirmations quantitatives, retrouver le tableau/figure/protocole exact et conserver les conditions de comparaison.
6. Pour les affirmations mathématiques, vérifier les hypothèses et tenter un contre-exemple ; ne pas confondre propriété du champ historique et propriété de l'implémentation actuelle.
7. Vérifier les liens internes, les citations de pages Quarto, les extraits OCR et les fichiers PDF associés.
8. Marquer explicitement les points ouverts et la preuve attendue pour fermer chacun.

## 5. Sources externes vérifiées lors de cet audit

- Mohammadi, B. & Brun, J.-M. (2006), *Similitude généralisée et modélisation géométrique à complexité réduite*, C. R. Mécanique 334, 634–638, DOI 10.1016/j.crme.2006.06.007. Notice et bibliographie consultées : https://comptes-rendus.academie-sciences.fr/mecanique/articles/10.1016/j.crme.2006.06.007/
- Bozon, N., Sinfort, C. & Mohammadi, B., *A GIS-based atmospheric dispersion model*, notice JESA 2010, DOI 10.3166/jesa.44.445-461 : https://www.researchgate.net/publication/42782194_A_GIS-based_atmospheric_dispersion_model ; manuscrit HAL hal-00468863 : https://hal.science/hal-00468863.
- Brun, J.-M. & Mohammadi, B. (2008), *Reduced-Order Modelling of Dispersion*, Springer, DOI 10.1007/978-1-4020-8758-5_14. Notice et résumé consultés : https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion.
- Page et al. (2021), PRISMA 2020 statement : https://www.prisma-statement.org/prisma-2020.

## 6. Limites de cet audit

Cet audit est une première passe ciblée sur les références historiques et les revendications scientifiques les plus susceptibles d'être amplifiées. Les contrôles web n'ont pas établi l'inexistence des références non retrouvées. Les PDF de revue systématique, l'intégralité des pages Quarto, les métadonnées de chaque entrée de bibliographie et tous les liens du dépôt doivent encore être examinés systématiquement. Les conclusions doivent donc rester proportionnées aux preuves effectivement consultées.
## 7. Deuxième passe — vérification bibliographique externe (2026-10-22)

Cette seconde passe a comparé environ 45 références et affirmations du dépôt à des sources externes (Crossref, OpenAlex, HAL, Zenodo, Persée, Federal Register, sites éditeur et institutionnels). Elle complète la première passe : les constats A-xx portaient sur le risque de sur-affirmation ; les constats B-xx ci-dessous portent sur des erreurs bibliographiques ou des associations source-affirmation. Conformément à l'échelle du § 3, « erroné » désigne ici une contradiction positive démontrée avec la source primaire.

### B-01 — Turbelin, Singh & Issartel : année et sous-titre erronés

- **Statut :** erroné (contradiction positive avec la notice éditeur).
- **Emplacement :** `docs/references.md` (l. 61), `site/references.bib` (clé `renormalization2016`, l. 134-142), `site/references.qmd` (n° 20), `docs/02-revue-etat-art-2026.md` (l. 91), `docs/bibliographie/identification-source-assimilation.md` (l. 15).
- **Constat :** le dépôt cite « (2016), "… : the renormalization technique" ». La notice Crossref du DOI 10.1002/2014MS000385 donne : publication en ligne le 17 décembre 2014, *JAMES* 6, 1244–1255, sous-titre « … : Optimality analysis of an inversion technique ».
- **Source :** https://doi.org/10.1002/2014MS000385 (notice Crossref).
- **Correction sûre :** citer « Turbelin, Singh & Issartel (2014), *JAMES* 6, 1244–1255, DOI 10.1002/2014MS000385 » et remplacer le sous-titre partout.

### B-02 — Applied Geomatics 2009 : auteurs inversés et pagination erronée

- **Statut :** erroné.
- **Emplacement initial :** `README.md`, `docs/references.md`, `site/references.bib`, `site/references.qmd`, `docs/01`, `docs/04`, `docs/bibliographie/fondements-et-heritage.md`, `raw/README.md`.
- **Constat :** la notice Springer et le PDF de l'article donnent **Bozon, N. & Mohammadi, B.**, *Applied Geomatics* 1(3), 59–74 (2009), DOI 10.1007/s12518-009-0006-0. Une nouvelle inspection de la branche a révélé que `site/references.bib` conservait encore l'ordre d'auteurs et la pagination erronés malgré les corrections ailleurs.
- **Source :** https://doi.org/10.1007/s12518-009-0006-0 ; PDF de l'article accessible via https://d-nb.info/1239408757/34.
- **Correction appliquée dans cette passe :** `site/references.bib` utilise maintenant Bozon puis Mohammadi, numéro 3 et pages 59–74. Les métadonnées de cette entrée doivent rester synchronisées dans toutes les représentations de la bibliographie.

### B-03 — CAREA / pesticides : affirmation rattachée à la mauvaise source

- **Statut :** association source-affirmation erronée.
- **Emplacement :** `docs/references.md` (l. 39), `docs/02-revue-etat-art-2026.md` (l. 37 et 96), `docs/bibliographie/sig-exposition-applications.md` (l. 14), `docs/bibliographie/spray-drift-et-modeles-operationnels.md` (l. 50).
- **Constat :** le lien STOTEN (Teggi, Costanzini, Ghermandi & Malagoli, *STOTEN* 610-611, 175-190, DOI 10.1016/j.scitotenv.2017.07.196) renvoie au papier du modèle CAREA (sources complexes), pas à l'application pesticides. L'application pesticides/exposition résidentielle (4 % → 54 % de récepteurs exposés) se trouve dans Costanzini et al. 2018, *Atmosphere* 9(2):38, DOI 10.3390/atmos9020038 (CAREA + modèle de proximité).
- **Sources :** https://doi.org/10.1016/j.scitotenv.2017.07.196 ; https://doi.org/10.3390/atmos9020038.
- **Correction sûre :** attribuer l'affirmation pesticides à Costanzini et al. 2018, ou citer les deux papiers avec leurs rôles respectifs.

### B-04 — Zenodo « STE » 22914336 : année erronée

- **Statut :** erroné.
- **Emplacement :** `docs/references.md` (l. 62), `docs/02-revue-etat-art-2026.md` (l. 48 et 93), `docs/bibliographie/identification-source-assimilation.md` (l. 29).
- **Constat :** le dépôt cite l'enregistrement Zenodo 22914336 comme « (2025) ». L'enregistrement (Shafiyev et al., Bukhara State University) a été publié le 22 septembre 2026 (v1). La description du contenu (adjoint, Tikhonov, bayésien/MCMC, PINN, problèmes ouverts) est par ailleurs exacte.
- **Source :** https://zenodo.org/records/22914336.
- **Correction sûre :** remplacer « (2025) » par « (2026) » et citer le DOI Zenodo plutôt qu'une année approximative.

### B-05 — Journal mal attribué (ROM + assimilation de données, 2023)

- **Statut :** erroné.
- **Emplacement :** `docs/references.md` (l. 50), `docs/bibliographie/rom-et-apprentissage.md` (l. 34).
- **Constat :** le dépôt attribue « A reduced order with data assimilation model: Theory and practice » à *Applied Mathematics and Computation*. La notice du DOI 10.1016/j.compfluid.2023.105862 montre que le journal réel est *Computers & Fluids*.
- **Source :** https://doi.org/10.1016/j.compfluid.2023.105862.
- **Correction sûre :** remplacer « Appl. Math. Comput. » par *Computers & Fluids* (2023).

### B-06 — Référence POD+RBF, Pékin (2021) : attribution non vérifiée

- **Statut :** erroné.
- **Emplacement :** `docs/references.md` (l. 51), `docs/bibliographie/rom-et-apprentissage.md` (l. 40).
- **Constat :** le dépôt attribuait le PII ScienceDirect S2666449621000372 à une étude POD+RBF sur 144 km² à Pékin et donnait des journaux incompatibles (« Build. Sim. Eng. / Urban Clim. »). Les contrôles disponibles n'ont pas confirmé de façon indépendante le titre, les auteurs, le journal, l'année ni le contenu. Il n'est donc pas possible d'affirmer quel journal est correct ni que le contenu POD+RBF est confirmé.
- **Source :** [lien éditeur ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666449621000372), non exploitable par le contrôle automatisé ; aucune notice primaire exploitable n'a été obtenue lors de cette passe.
- **Correction sûre :** retirer l'attribution bibliographique et la description de méthode des éléments probants jusqu'à vérification de la notice éditeur/Crossref et du résumé. Ce constat est non vérifié, pas une erreur démontrée.

### B-07 — « Le régulateur lui-même lance (2026) une modernisation open source d'AGDISP »

- **Statut :** affirmation erronée ; reformulation requise.
- **Emplacement :** `docs/02-revue-etat-art-2026.md` (l. 19).
- **Constat :** l'AGDISP Modernization Project est une initiative de l'industrie agricole, pas de l'EPA. La source citée dans le même document (AgAir Update, 2026-03-09, l. 81) décrit Bayer rejoignant un effort de l'industrie agricole autour d'AGDISP, modèle « utilisé par les régulateurs de pesticides ». L'EPA n'est donc ni l'auteur ni le porteur de l'initiative.
- **Source :** AgAir Update (2026-03-09), citée dans le même document.
- **Correction sûre :** écrire « une initiative de l'industrie agricole (2026), pour un modèle utilisé par les régulateurs de pesticides ».

### B-08 — SERRA « Seveso » : année d'édition

- **Statut :** imprécision mineure.
- **Emplacement :** `docs/references.md` (l. 55), `docs/02-revue-etat-art-2026.md` (l. 89), `docs/bibliographie/rom-et-apprentissage.md` (l. 55 et 60).
- **Constat :** le papier 10.1007/s00477-022-02288-x est paru en ligne en octobre 2022 mais au numéro 2023 (*SERRA* 37(1), 275-290).
- **Source :** https://doi.org/10.1007/s00477-022-02288-x.
- **Correction sûre :** citer « (2023), en ligne 2022 » ou uniformiser selon le style bibliographique choisi.

### B-09 — « Mohammadi, Brun & Pironneau (2006) » : existence attestée, notice du recueil toujours manquante — complément au constat A-03

- **Statut :** complément qui requalifie A-03 : la référence n'est pas une invention, mais sa notice reste incomplète.
- **Emplacement :** `README.md` (l. 17), `docs/references.md` (l. 9), `site/references.bib` (l. 12-15, clé `mohammadi2006pironneau`), `site/references.qmd` (l. 11), `docs/01` (l. 12), `docs/bibliographie/fondements-et-heritage.md` (l. 26-29), `docs/04` (§3), `raw/README.md` (l. 41).
- **Constat :** la bibliographie du papier Bozon & Mohammadi 2009 (*Applied Geomatics* 1, 59–74, DOI 10.1007/s12518-009-0006-0) cite textuellement : Mohammadi, B., Brun, J.-M. & Pironneau, O. (2006), « Reduced order modelling of dispersion », in *Numerical Analysis and Scientific Computing with PDE and their Challenging Applications* (Springer). L'existence de la référence est donc attestée par une source primaire publiée. En revanche, le recueil lui-même reste introuvable (Crossref, Springer, OpenAlex, web — recherches du 2026-10-22) : éditeur, année, pagination, ISBN et DOI de la notice restent non vérifiables depuis la seule citation. Le renvoi croisé A-03 demeure pour la notice, mais la référence ne doit plus être traitée comme une invention probable.
- **Source :** bibliographie de https://doi.org/10.1007/s12518-009-0006-0 (Crossref).
- **Correction sûre :** conserver la référence avec le statut « attestée par la bibliographie de Bozon & Mohammadi 2009 ; notice du recueil non localisée au 2026-10-22 » ; ne pas lui attribuer de contenu, pages, ISBN ou DOI non confirmés.

## 8. Références vérifiées exactes lors de la deuxième passe

Les entrées suivantes ont été contrôlées sur source primaire et correspondent aux métadonnées du dépôt (liste non exhaustive) :

- Mohammadi & Brun 2006, *C. R. Mécanique* 334, 634–638, DOI 10.1016/j.crme.2006.06.007 (auteurs, DOI, PDF libre ; sa bibliographie cite la thèse « 2007 » — voir A-01).
- Brun & Mohammadi 2008, chapitre Springer 14, p. 245 ; « e-sta » 2008 attestée par les bibliographies des papiers de 2009/2010 ; HAL hal-00468863 + *JESA* 2010, DOI 10.3166/jesa.44.445-461 (voir A-05).
- Muller 1979 (*Persée* 8(3), 215-227) ; Borouchaki et al. 1997 (*FEAD* 25(1-2), 61-83) ; Raupach & Thom 1981 ; Simpson 1997 ; Mohammadi & Pironneau 2001.
- Règle EPA Appendix W : FR 2024-27636, publié le 2024-11-29, effectif le 2025-01-28 ; FR 2014-01234 (29/01/2014).
- Guide EPA AGDISP-Gaussian : citation « extremely conservative » exacte ; limites 0,5 mi / 2 mi / barrières. Page EPA modèles : AgDRIFT v2.1.1, AGDISP v8.26.
- NCASI TB808 ; Bird et al. 2002 (*ET&C*, 161 essais, DOI 10.1002/etc.5620210328) ; Castro-Tanzi et al. 2025 (*STOTEN*, 18 événements, DOI 10.1016/j.scitotenv.2025.178725) ; UASS 2024 ; ANN/SVR 2022 (DOI 10.1007/s11356-022-23571-y) ; analyse de sensibilité 2023 (DOI 10.1007/s10668-023-04452-x) ; *Agronomy* 14(9):1977 ; Verveecken & Meyers 2015 (*Building and Environment*, DOI 10.1016/j.buildenv.2015.05.008, facteur 2500 confirmé).
- HAL hal-04310899 (ECCOMAS UNCE 2024) ; CMAME 2024 (Bologne) ; cea-04810109 (MCxM) ; Ayoub et al. 2024 (DOI 10.1007/s00477-024-02738-8) ; chapitre Springer 2025 (DOI 10.1007/978-3-032-02728-3_53) ; Hutchinson 2017 (*Information Fusion* 36, 130-148) ; MDPI *Appl. Sci.* 16(4):1833 (2026) ; plugin QGIS Sebapac90 (README : « based on Masters and Ela (2008) »).
- SICC 2026 session 3 ; NARAC ; ADMLC ; OIEau ; APSI ; revue IJRISS AERMOD (Shafie) ; TIERRAS (Zenodo 15794259, >400 essais) ; ERIES (4TU, Sofia, éthylène, 76 points, S1/S2) ; CAPRIV (Perriot et al. 2024, *Data in Brief* 54:110366, DOI vérifié) ; DIFLU (campagne hélium IRSN/ASNR confirmée institutionnellement) ; arrêté du 4 mai 2017 (LEGI + agriculture.gouv.fr) ; rapport InVS « quatre sites de l'Hérault en 2006 » (Santé publique France).

Réserves : les effectifs de CAPRIV (« 3 792 observations / 38 variables », `docs/11` l. 34) et les détails de DIFLU (« 19 lâchers / ~560 m », `docs/12` l. 11 ; DOI 10.57745/A9YC3C non résolu depuis l'audit) restent à recontrôler sur le document primaire.

## 9. Couverture et limites de la deuxième passe

- **Vérifié :** environ 45 références/affirmations, principalement sur les métadonnées (DOI, notices Crossref/OpenAlex/Springer/HAL/Zenodo, Federal Register, Persée, pages institutionnelles) et, pour quelques affirmations chiffrées, sur le contenu des documents.
- **Non couvert :** fiches `raw/fiches/*` page à page, PDF de `raw/reviews/*`, pages Quarto individuelles, liens institutionnels individuels (MODISAFE, R-LINE, Cefas, barrières near-road EPA, HARMO, Hamburg EWTL).
- **Prudence :** « erroné » doit être réservé aux contradictions positives (B-01, B-02, B-04, B-05, B-07) ou à une association démontrée (B-03). B-06 est désormais classé non vérifié ; B-08 est une imprécision ; B-09 précise que l'existence d'une citation secondaire ne valide pas toutes les métadonnées. Les entrées non couvertes ne sont ni vraies ni fausses : elles restent à contrôler.


### A-10 — NOAA DATEM et ETEX : contradiction interne dans le catalogue

- **Statut :** erreur factuelle interne confirmée et corrigée dans cette PR.
- **Emplacement :** `docs/12-catalogue-donnees-transport-dispersion.md`, première ligne de la table des corpus.
- **Constat :** le catalogue affirmait que NOAA DATEM « inclut ETEX et CAPTEX », tandis que `docs/15-audit-corpus-g0-resultats.md` indique explicitement qu'ETEX n'est pas inclus dans DATEM et renvoie au JRC pour le corpus ETEX. Les deux formulations ne peuvent pas être vraies simultanément.
- **Contrôle externe :** la documentation NOAA DATEM et le site JRC présentent des ressources distinctes ; la fiche ETEX du JRC propose les données des deux lâchers séparément. [NOAA DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) ; [JRC ETEX datasets](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm).
- **Correction effectuée dans cette PR :** le catalogue indique maintenant que DATEM inclut notamment CAPTEX, et que l'ETEX est documenté séparément par le JRC.
- **Preuve de clôture :** vérifier les autres lignes du catalogue contre les sources de données officielles, puis ajouter un contrôle automatisé des contradictions entre fiches.

### A-11 — Statut G0 contradictoire dans la documentation

- **Statut :** incohérence de statut confirmée ; formulation corrigée dans cette PR.
- **Emplacement :** `docs/11-g0-evidence-externe.md` et `docs/14-seance-validation-experimentale.md`.
- **Constat :** `docs/11` déclarait d'abord « G0 n'est pas franchi », puis plus loin « G0 est franchi ». La séance de validation utilisait en parallèle G0-S/G0-A sans distinguer clairement ces pistes du jalon documentaire G0. Le lecteur pouvait conclure à tort que le cadrage global restait bloqué, ou au contraire que la validation applicative était autorisée.
- **Correction effectuée dans cette PR :** le premier statut est désormais explicitement historique et remplacé par la mise à jour ; la séance distingue le jalon G0 déclaré franchi des travaux scientifiques encore ouverts et des prérequis G1 sur les fichiers bruts.
- **Réserve :** « G0 franchi » signifie que le cadrage documentaire est rempli selon les critères du projet ; cela ne signifie pas que les données ont été validées au niveau des fichiers, que la licence DIFLU est confirmée ou qu'un benchmark a été exécuté.

### A-12 — Conclusions de la revue d'état de l'art plus fortes que les preuves consignées

- **Statut :** extrapolations non démontrées ; formulation corrigée dans cette PR.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`.
- **Constat :** le résumé exécutif et les tableaux comparatifs affirmaient notamment qu'aucun concurrent n'avait repris la métrique travel-time, que la niche restait ouverte, que la dérive mécaniste rapide était une « case vide », que les ROM exigeaient toutes des snapshots CFD/LES, que J-DriftX extrapolerait « par construction » et qu'un adjoint serait « disponible par construction ». La revue elle-même reconnaissait que les requêtes, les critères et les décomptes n'étaient pas entièrement reproductibles.
- **Pourquoi c'est problématique :** une recherche ciblée ne prouve pas l'absence de travaux ; les familles de ROM sont hétérogènes ; une formule analytique ne garantit ni extrapolation prédictive ni disponibilité d'un adjoint utile ; un besoin réglementaire non couvert ne prouve pas qu'une méthode proposée le couvre.
- **Correction effectuée dans cette PR :** réécriture des conclusions exécutives et de plusieurs affirmations thématiques en hypothèses bornées ; correction du tableau de positionnement et des recommandations pour ne pas présenter la nouveauté, la supériorité ou le besoin d'une extension AGDISP comme acquis.
- **Preuve de clôture :** chaque comparaison restante doit pointer vers le passage précis de la source primaire, expliciter le régime et l'observable, et être classée comme fait, hypothèse ou question ouverte.

## 7. Modifications réalisées dans la PR de suivi

Cette PR de suivi ne se limite donc plus au registre initial. Elle :
- ajoute le registre d'audit et conserve les constats A-01 à A-14 ainsi que B-01 à B-28 avec leur niveau de preuve ;
- corrige des affirmations excessives dans la revue d'état de l'art et distingue les hypothèses J-DriftX des résultats établis ;
- corrige la relation DATEM/ETEX dans le catalogue de données et clarifie le statut G0 par rapport aux prérequis G1 ;
- corrige les métadonnées Turbelin et al. (2014), Bozon & Mohammadi (2009), Arcucci et al. (2023) et la date de la ressource Zenodo (2026) ;
- sépare la source CAREA sur les sources complexes (Teggi et al., 2018) de l'étude d'exposition aux pesticides (Costanzini et al., 2018) ;
- requalifie la référence ScienceDirect PII S2666449621000372 comme non vérifiée (les métadonnées et l'association à POD+RBF ne sont pas confirmées), distingue l'année de publication en ligne de l'année de volume pour l'article Seveso, complète des métadonnées bibliographiques et borne l'interprétation du speed-up U-FNO ×4000 et des ratios de performance du ROM Vervecken et al. (2015) ;
- retire les affirmations non étayées sur l'absence de dépôt de la thèse et précise que l'année officielle doit être vérifiée sur la page de titre.

Les changements n'établissent pas encore la validité de chaque référence du corpus. Les PDF de revue exécutive, les métadonnées bibliographiques complètes et les fichiers bruts de données restent à auditer. Le `main` actuel inclut une étape CI qui installe Quarto et rend le site ; elle a réussi sur le contenu du site de cette PR lors du contrôle disponible. Ce succès de compilation ne remplace pas la revue du contenu scientifique.


### A-13 — Zenodo 22914336 : année de publication erronée

- **Statut :** erreur bibliographique confirmée ; le record et son contenu sont identifiés.
- **Emplacement :** `docs/references.md`, `docs/02-revue-etat-art-2026.md` et la bibliographie annotée.
- **Constat :** le dépôt citait « Source Term Estimation for Atmospheric Pollutant Releases » comme une ressource Zenodo de 2025. L'enregistrement 22914336 (Shafiyev et al., Bukhara State University) est publié le **22 septembre 2026 (v1)**. La description du contenu — méthodes adjointes, Tikhonov, bayésiennes/MCMC, PINN et problèmes ouverts en estimation de source — est cohérente avec la ressource.
- **Source :** [record Zenodo](https://zenodo.org/records/22914336).
- **Correction effectuée dans cette PR :** l'année est corrigée en 2026. La ressource est identifiée comme une ressource de synthèse, mais son statut de revue évaluée par les pairs n'est pas affirmé ; ses conclusions doivent être corroborées par les articles primaires.
- **Preuve de clôture :** vérifier que toutes les occurrences (notamment `site/references.bib`, `site/references.qmd` et `docs/bibliographie/identification-source-assimilation.md`) utilisent 2026 et que les affirmations associées sont attribuées à la ressource avec le niveau de preuve approprié.

### B-10 — PII ScienceDirect S2666449621000372 : méthode et métadonnées non confirmées

- **Statut :** non vérifié ; ne pas qualifier de faux en l'absence de contradiction positive.
- **Emplacement :** `docs/bibliographie/rom-et-apprentissage.md` et les mentions associées éventuelles.
- **Constat :** le dépôt associait ce PII à une étude POD+RBF pour un environnement urbain et indiquait *Journal of Safety Science and Resilience* (2021). La page ScienceDirect a renvoyé HTTP 403 lors du contrôle automatisé et une recherche exacte sur le PII n'a pas retrouvé de notice exploitable permettant de confirmer le titre, les auteurs, la méthode ou la revue.
- **Correction effectuée :** la fiche décrit désormais cette référence comme non vérifiée et interdit de l'utiliser comme preuve méthodologique avant vérification primaire.
- **Preuve de clôture :** obtenir une notice éditeur ou Crossref avec titre/auteurs/revue/année, puis lire au minimum le résumé et confirmer que la méthode POD+RBF est bien celle annoncée.

### B-11 — Métadonnées non vérifiées encore présentées comme établies dans la bibliographie du site

- **Statut :** incohérence interne documentaire confirmée et corrigée dans cette PR.
- **Emplacement :** `site/references.bib`, `site/references.qmd`.
- **Constat :** malgré les constats A-01 et A-03 qui signalent que les métadonnées exactes de la thèse de Brun et du chapitre attribué à Mohammadi, Brun et Pironneau restent à confirmer, la bibliographie BibTeX et la page Quarto du site leur attribuaient encore des métadonnées fermes (titre, année/établissement pour la thèse ; livre et éditeur pour le chapitre).
- **Correction effectuée :** ces entrées sont maintenant explicitement provisoires/non vérifiées ; le chapitre n'est plus présenté comme un chapitre Springer confirmé et la thèse n'est plus figée sous un titre et une année non résolus.
- **Preuve de clôture :** retrouver la page de titre ou une notice institutionnelle de la thèse et une notice éditeur/catalogue pour le chapitre ; rétablir les métadonnées complètes seulement après contrôle.

### B-12 — Métadonnées incomplètes de trois références de dispersion

- **Statut :** métadonnées incomplètes confirmées ; corrections bibliographiques appliquées, sans préjuger du contenu scientifique des articles.
- **Emplacement :** `site/references.bib` et citations correspondantes dans `site/references.qmd`.
- **Constat :** le contrôle des notices éditeur a montré que l'entrée Vervecken et al. omettait le coauteur Johan Camps, les pages 360–367 et le DOI 10.1016/j.buildenv.2015.05.008 ; l'entrée Hutchinson et al. omettait le DOI 10.1016/j.inffus.2016.11.010 ; l'entrée Ayoub et al. utilisait « et al. » et omettait le volume, le numéro et les pages malgré des métadonnées éditeur disponibles.
- **Sources :** [Vervecken et al., *Building and Environment* 92, 360–367](https://doi.org/10.1016/j.buildenv.2015.05.008) ; [Hutchinson et al., *Information Fusion* 36, 130–148](https://doi.org/10.1016/j.inffus.2016.11.010) ; [Ayoub et al., *Stochastic Environmental Research and Risk Assessment* 38, 3165–3175](https://doi.org/10.1007/s00477-024-02738-8).
- **Correction effectuée :** les auteurs et métadonnées vérifiés ont été ajoutés à BibTeX ; la page Quarto affiche désormais le DOI de Hutchinson et les quatre auteurs, volume, numéro et pagination d'Ayoub. Pour Vervecken, la note sur une méthode précise a été retirée tant que le texte intégral pertinent n'a pas été relié à cette affirmation.
- **Limite :** ces vérifications confirment les métadonnées, pas l'exactitude des résumés méthodologiques ou la transférabilité des performances vers J-DriftX.

### B-13 — Facteur ×4000 du surrogate U-FNO : périmètre de comparaison et validation

- **Statut :** chiffre primaire vérifié ; toute généralisation au coût total ou à la validation terrain serait non étayée.
- **Emplacement :** `docs/bibliographie/rom-et-apprentissage.md` ; à contrôler dans tout résumé comparatif des méthodes rapides.
- **Constat :** Ayoub et al. (2024) rapportent un surrogate U-FNO entraîné sur un corpus de 616 simulations WSPEEDI, avec une séparation 85/15. Le facteur annoncé d'environ 4000 compare environ 82 minutes pour une simulation WSPEEDI de six heures à environ 1,26 seconde pour une inférence du modèle entraîné. Il n'inclut donc pas, à lui seul, la génération des simulations d'apprentissage, la préparation des données ni l'entraînement. La cible évaluée est le simulateur numérique, pas une mesure indépendante du monde réel.
- **Source primaire :** [texte intégral éditeur, sections 2, 4–6](https://link.springer.com/article/10.1007/s00477-024-02738-8).
- **Correction effectuée :** la fiche bibliographique précise le périmètre du speed-up, les limites du corpus fini, la sous-estimation signalée lors de dépôts humides et le besoin de validation sur données réelles reconnu par les auteurs. Le facteur ×4000 n'est pas traité comme benchmark transférable à J-DriftX.
- **Preuve de clôture :** toute comparaison J-DriftX/ML doit mesurer séparément coût de préparation, entraînement, inférence, erreur sur test indépendant, extrapolation et validation terrain.

### B-14 — Vervecken et al. (2015) : méthode et accélérations à contextualiser

- **Statut :** métadonnées et résumé éditeur vérifiés ; portée des chiffres explicitée dans la fiche, texte intégral non audité ligne à ligne.
- **Emplacement :** `docs/bibliographie/rom-et-apprentissage.md`, entrée BibTeX `vervecken2015rom`.
- **Constat :** la notice éditeur confirme trois auteurs (Vervecken, Camps et Meyers), *Building and Environment* 92, 360–367, DOI 10.1016/j.buildenv.2015.05.008. Le résumé décrit une projection Krylov/Arnoldi d'un modèle CFD d'advection-diffusion instationnaire sur un champ de vitesse de fond stationnaire, pour un rejet temporel de gaz neutre à la centrale de Doel. Les ratios rapportés — environ 2500× par rapport au CFD après initialisation, 25× plus rapide que le temps réel et un coût calculatoire annoncé 10⁵ fois inférieur — ont des périmètres distincts et sont spécifiques aux cas étudiés.
- **Source primaire de contrôle :** [notice éditeur et résumé](https://doi.org/10.1016/j.buildenv.2015.05.008).
- **Correction effectuée :** la fiche distingue le coût de construction initial, le champ CFD pré-calculé, les hypothèses de régime et les ratios de performance ; elle interdit de les transférer directement à J-DriftX ou à la dérive de pulvérisation.
- **Preuve de clôture :** lire les sections méthodologiques et résultats du texte intégral, relever précisément les cas, métriques et périmètres de coût, puis comparer seulement sur un protocole commun.

### B-15 — Brun & Mohammadi (2008) : contenu du chapitre présenté comme lu au-delà de l'extrait consulté

- **Statut :** sur-attribution documentaire confirmée et formulation corrigée.
- **Emplacement :** `docs/01-audit-heritage-driftx.md`, fiche source `raw/fiches/2008-brun-mohammadi-springer-chap14.md`.
- **Constat :** la notice éditeur confirme le chapitre, mais la fiche de lecture indique que seules les pages 245–246 ont été extraites/relues ; elle précise que les exemples numériques et l'analyse détaillée restent à extraire des pages suivantes. La synthèse de l'héritage présentait pourtant les contraintes physiques et les exemples numériques multi-sources comme des éléments du chapitre déjà vérifiés.
- **Source de contrôle interne :** fiche de lecture du chapitre, qui distingue explicitement l'extrait de deux pages du chapitre complet ; [notice Springer](https://doi.org/10.1007/978-1-4020-8758-5_14) pour les métadonnées, pas pour les détails non lus.
- **Correction effectuée :** la synthèse de l'héritage distingue désormais les éléments décrits par le résumé/extrait des détails méthodologiques et exemples qui restent à vérifier dans le texte intégral. La fiche de lecture conserve les pages consultées et les éléments à extraire.
- **Preuve de clôture :** relire les pages restantes du chapitre, rattacher chaque affirmation à une page/équation/figure et mettre à jour la matrice d'accès aux sources.

### B-16 — POD-GPR : nombre de snapshots LES non corroboré dans la source primaire

- **Statut :** chiffre non vérifié, non qualifié de faux.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, ligne du panorama des ROM ; référence HAL `hal-04310899`.
- **Constat :** une version précédente de la synthèse donnait « ~50 snapshots LES » sans localiser dans la source primaire le passage qui définit le nombre, le rôle des snapshots ou le protocole de sélection. Le document HAL n'a pas pu être contrôlé directement lors de cette passe ; le nombre ne doit donc pas être repris comme fait vérifié.
- **Source à contrôler :** [document HAL annoncé](https://hal.science/hal-04310899/document).
- **Correction effectuée :** la synthèse indique maintenant que le nombre de snapshots et le protocole restent à vérifier dans la source primaire.
- **Preuve de clôture :** retrouver le texte intégral, citer la section/table correspondante et distinguer nombre de simulations LES, snapshots temporels/spatiaux et cas de test.

### B-17 — Comparaisons réglementaires : portée des conclusions EPA et AERMOD/CALPUFF

- **Statut :** sur-généralisation identifiée et formulation corrigée.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, sections sur modèles opérationnels, dérive de pulvérisation et AGDISP.
- **Constat :** la guidance EPA de 2010 décrit l'extension gaussienne AGDISP comme « extremely conservative » dans un cadre FIFRA défini, en supposant notamment l'absence de barrières sur la trajectoire et en ne représentant pas certaines variables météorologiques au-delà du site d'application. Elle limite les usages recommandés à certains cas de pulvérisation aérienne et note le manque de validation au-delà de 2 miles. La formule générale « extrêmement conservatrice » sans ces conditions aurait pu être lue comme une propriété de toutes les applications. De même, un résultat d'une comparaison AERMOD/CALPUFF en environnement bâti ne permet pas de classer globalement ces modèles.
- **Sources primaires :** [guidance EPA de 2010, sections Background/Guidance/Validation](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension) ; [étude de comparaison en environnement bâti](https://doi.org/10.1016/j.buildenv.2012.02.017) ; [annonce AMP du 9 mars 2026](https://agairupdate.com/2026/03/09/bayer-crop-science-joins-ag-industry-efforts-to-modernize-spray-drift-model-used-by-pesticide-regulators/).
- **Correction effectuée :** les conditions d'application et la portée de validation EPA sont explicitées ; le résultat AERMOD/CALPUFF est attribué à un cas précis ; l'AMP est présenté comme une voie de modernisation concurrente, sans inventer un besoin de module explicitement annoncé par la source.
- **Preuve de clôture :** les autres affirmations comparatives de la revue doivent, de même, identifier le cas, l'observable, le protocole et la portée de validité de chaque source.

### B-18 — Tendances CBRN / jumeaux numériques : consensus et « format gagnant » non démontrés

- **Statut :** formulations de tendance trop fortes, corrigées.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, section « Tendances transverses » et tableau des sources.
- **Constat :** les sources sur les jumeaux numériques urbains, une session SICC/CBRNe et les prévisions ECMWF attestent des applications et initiatives spécifiques, mais ne démontrent ni un consensus universel en faveur d'une architecture donnée, ni que la conformité EU AI Act est explicitement exigée dans tous les cas, ni qu'une chaîne « données météo ouvertes → modèle rapide → tableau de bord » est un « format gagnant ». En revanche, la page CbrnAlert de l'European Weather Cloud décrit concrètement une plateforme utilisant FLEXPART et des prévisions ECMWF récentes.
- **Sources :** [CbrnAlert / European Weather Cloud](https://www.europeanweather.cloud/use-cases/cbrnalert-web-application-near-real-time-dispersion-modelling-cbrn-releases) ; [session SICC/CBRNe 2026](https://www.sicc-series.com/technical-and-poster-sessions/session-3-artificial-intelligence-digital-twins-decision-support-in-cbrne-risk-management/) ; [étude sur jumeau numérique feu/fumée](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513986/).
- **Correction effectuée :** les sources sont décrites comme exemples contextualisés, l'existence d'une intégration ECMWF–FLEXPART est citée directement et les superlatifs/conclusions de consensus sont retirés.
- **Preuve de clôture :** les conclusions transverses restantes doivent être distinguées des constats source par source et ne pas transformer un exemple de déploiement en preuve de supériorité générale.

### B-19 — Affirmations négatives (« aucun code », « jamais publié », idée non reprise) non démontrées

- **Statut :** formulations absolues non soutenues par une recherche d'absence exhaustive ; corrigées.
- **Emplacement :** `docs/01-audit-heritage-driftx.md` et conclusion/positionnement de `docs/02-revue-etat-art-2026.md`.
- **Constat :** des formulations telles que « aucun dépôt de code n'a accompagné les publications », « l'ensemble n'a jamais été consolidé en un article de revue » ou « l'idée n'a été ni reprise ni démentie » transforment l'absence de résultat dans le corpus consulté en affirmation générale sur la littérature ou l'historique du projet. La recherche effectuée n'étant pas exhaustive et reproductible, ces propositions ne sont pas démontrées.
- **Correction effectuée :** les formulations précisent désormais « aucune ressource identifiée dans le corpus/recherches consignées » et explicitent que cela ne prouve pas une absence générale ; la conclusion de l'état de l'art ne prétend plus établir la non-reprise ou la non-réfutation de l'idée.
- **Preuve de clôture :** si une conclusion d'absence doit être maintenue, documenter les bases consultées, requêtes exactes, dates, langues, critères, décomptes et recherche de citation/rétrospective ; sinon conserver le statut « non identifié dans cette passe ».

### B-20 — Scores de « crédibilité » sans barème et colonne de date ambiguë

- **Statut :** précision méthodologique non justifiée, corrigée.
- **Emplacement :** tableau « Notes de sources » de `docs/02-revue-etat-art-2026.md`.
- **Constat :** les valeurs 2/5 à 5/5 n'étaient accompagnées d'aucun barème observable (type de source, revue par les pairs, accès au texte, indépendance, risque de biais). Elles donnaient donc une apparence de quantification sans procédure reproductible. La colonne « Dernière mise à jour » mélangeait en outre années de publication, dates de version et mises à jour de pages web.
- **Correction effectuée :** les notes numériques ont été remplacées par une description du type de source et de ses limites de lecture ; l'en-tête devient « Année de publication ou version », avec les cas de dates distinctes explicités.
- **Preuve de clôture :** si un score de qualité documentaire est réintroduit, définir des critères, des ancrages observables et une procédure de double-évaluation avant de noter les sources.

### B-21 — Hybridation CMAQ/AERMOD : temporalité et portée mal décrites

- **Statut :** source et formulation recontextualisées.
- **Emplacement :** `docs/02-revue-etat-art-2026.md`, section « Modèles opérationnels et réglementaires ».
- **Constat :** le texte parlait de « revues récentes d'AERMOD » pour soutenir l'hybridation CMAQ+AERMOD et un couplage SIG/santé publique. Une source primaire pertinente est plutôt l'étude d'Isakov et al. (2009), qui combine un modèle régional chimique CMAQ, le modèle local AERMOD et des modèles d'exposition humaine. La référence démontre l'existence d'une approche hybride dans ce contexte, pas une revue récente ni une supériorité universelle.
- **Source :** [Isakov et al. (2009), DOI 10.3155/1047-3289.59.4.461](https://doi.org/10.3155/1047-3289.59.4.461).
- **Correction effectuée :** la phrase est attribuée à cette lignée précise et ne présente plus le travail comme une revue récente d'AERMOD.
- **Preuve de clôture :** si une autre source est destinée à soutenir une tendance plus récente, l'ajouter explicitement et vérifier le passage exact.

### B-22 — Verdict global de validité/originalité et garanties physiques trop catégoriques

- **Statut :** formulations trop fortes, corrigées dans les documents de synthèse et de lecture.
- **Emplacements :** `docs/01-audit-heritage-driftx.md`, `site/projet/audit.qmd`, `docs/04-revues-papiers-sources.md`, `raw/fiches/2009-bozon-sinfort-mohammadi-driftx-hal.md`.
- **Constat 1 — verdict scientifique :** la conclusion « cœur scientifique sain, original et toujours différenciant » dépassait les preuves disponibles. Une revue ciblée, quelques articles historiques et l'absence de benchmarks modernes indépendants ne suffisent pas à établir la validité mathématique, la nouveauté exhaustive ou l'avantage actuel. Les lacunes portent donc aussi sur la formalisation et la validation, pas seulement sur le code.
- **Constat 2 — invariants :** le manuscrit Bozon, Sinfort & Mohammadi (2009) affirme que sa restriction multi-niveaux préserve la divergence nulle **si** le champ précédent vérifie cette propriété, et que la restriction de concentration satisfait le bilan de masse entrant. Les fiches résumaient cela comme des garanties inconditionnelles et transférables à une réimplémentation. Le texte source rapporte une propriété sous construction/hypothèses ; il ne valide pas automatiquement les calculs numériques, les données, ni un nouveau code.
- **Sources internes primaires :** extraction du manuscrit HAL `raw/extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt`, autour des équations [2]–[4] (notamment les lignes extraites autour de 461–505) ; fiche documentaire [HAL hal-00468863](https://hal.science/hal-00468863).
- **Corrections effectuées :** le verdict global est remplacé par une hypothèse méthodologique à tester ; les propriétés multi-niveaux sont explicitement attribuées aux auteurs et conditionnées à leurs hypothèses ; les fiches demandent une dérivation et des tests avant de les traiter comme garanties d'une implémentation moderne. Les absences de publication de synthèse sont également formulées comme « non identifiée dans les recherches consignées ».
- **Tests requis avant clôture :** (1) écrire les hypothèses et la définition précise de la divergence pour le champ utilisé ; (2) vérifier symboliquement que l'interpolation par fonctions de forme conserve les conditions aux limites revendiquées ; (3) vérifier le bilan de masse par intégration de flux sur des cas analytiques ; (4) tester les erreurs discrètes sur plusieurs grilles, géométries et niveaux ; (5) distinguer propriété continue, propriété de l'algorithme discret et résultat observé dans le prototype historique.

### B-23 — Page « Contraintes physiques » : couverture CI exagérée et garanties non implémentées

- **Statut :** affirmation directement contredite par le code et les tests actuels ; corrigée.
- **Emplacements :** `site/theorie/contraintes-physiques.qmd`, docstring de `src/jdriftx/constraints.py`.
- **Constat :** l'ancienne page affirmait que quatre contraintes (conservation, positivité, linéarité et divergence nulle) étaient « vérifiées en continu par la CI ». Or le module de contraintes ne contient que des helpers de positivité et de superposition ; il n'implémente pas de vérification de divergence. La conservation est testée séparément sur un seul panache gaussien, avec une grille finie et une tolérance de 2 %. Les tests de positivité et de linéarité couvrent eux aussi des configurations ciblées, pas toutes les extensions possibles. La page appelait en outre la concentration une « densité de probabilité », ce qui confond deux grandeurs différentes, et affirmait sans comparaison sourcée que les surrogates ML ne garantissent aucune propriété physique.
- **Preuves de code :** `src/jdriftx/constraints.py` (seuls les helpers `positivite` et `linearite`) ; `tests/test_constraints.py` ; `tests/test_similitude.py::test_conservation_masse_panache` (grille `y ∈ [-500,500]`, `z ∈ [0,400]`, cas unique, tolérance relative 2 %).
- **Correction effectuée :** la page expose maintenant un tableau propriété/test/limite, précise que la divergence n'est pas testée, borne le résultat de conservation au cas numérique testé, corrige la distinction concentration/probabilité et remplace l'opposition générale aux modèles ML par une comparaison empirique des garanties et erreurs.
- **Preuve de clôture :** ajouter séparément les tests/proofs nécessaires à chaque invariant et préciser leur domaine de validité ; tant que le champ de vent historique n'est pas implémenté, ne pas revendiquer la vérification de sa divergence.

### B-24 — Pages théoriques : garanties, complexités et gradients présentés comme acquis

- **Statut :** plusieurs généralisations et avantages non démontrés corrigés.
- **Emplacements :** `site/theorie/reduction-a-priori.qmd`, `assimilation-identification.qmd`, `modele-direct.qmd`, `comparaison-complexites.qmd`.
- **Constats :** les pages présentaient la consistance physique comme « garantie par contraintes » alors que le champ de vent historique n'est pas implémenté ; les méthodes POD étaient décrites comme exigeant toutes des snapshots CFD/LES et comme fragiles hors domaine ; l'optimisation était dite triviale grâce à un coût d'évaluation quasi nul ; les gradients/adjoints J-DriftX étaient dits exacts, gratuits et disponibles par construction ; la comparaison affirmait que les surrogates ML ne respectent pas les contraintes physiques et que les modèles CFD repartent toujours de zéro pour chaque scénario. Ces propositions sont trop générales ou contredites par l'état du code.
- **Correction effectuée :** les pages distinguent les objectifs historiques des capacités du prototype actuel ; elles conditionnent les propriétés aux formulations et aux tests, séparent coût d'évaluation et coût total de calibration, décrivent les gradients comme non établis pour la métrique complète et reconnaissent que certaines méthodes ROM/ML peuvent intégrer des contraintes physiques. Les coûts CFD et particulaires sont décrits comme dépendants du workflow et de l'observable. Une clé bibliographique périmée `renormalization2016` a aussi été remplacée par `renormalization2014`.
- **Preuve de clôture :** toute comparaison quantitative devra utiliser un protocole commun (observable, précision, régime, coûts de préparation/calibration/inférence, mémoire et incertitude) ; toute affirmation de gradient/adjoint devra être rattachée à une dérivation ou à une implémentation testée.

### B-25 — Page d'utilité scientifique en contradiction avec le statut G0 courant

- **Statut :** contradiction documentaire confirmée et corrigée.
- **Emplacements :** `site/projet/utilite-scientifique.qmd` et `site/projet/preuves-g0.qmd`, conclusions de page.
- **Constat :** la page affirmait encore « G0 non franchi », alors que `docs/13-fiche-g0-cadrage-besoin.md` et `docs/15-audit-corpus-g0-resultats.md` enregistrent une décision G0 franchie le 22 octobre 2026 sur la base du cadrage et d'un audit documentaire des corpus. La contradiction risquait de faire confondre le statut du jalon documentaire et l'absence de validation scientifique/applicative.
- **Correction effectuée :** les deux pages indiquent désormais que G0 est franchi au niveau documentaire, mais que G1, la validation des fichiers bruts et le benchmark restent en attente ; elles rappellent que ce statut ne prouve ni l'utilité prédictive ni l'adéquation scientifique du modèle.
- **Preuve de clôture :** maintenir un statut unique et cohérent entre fiche G0, audit de corpus, page publique et roadmap ; ne faire évoluer G1 qu'après contrôle des fichiers et licences.

### B-26 — Page qualité : tests inexistants cités et portée de la CI exagérée

- **Statut :** erreurs de documentation directement vérifiables, corrigées.
- **Emplacement :** `site/projet/qualite.qmd`.
- **Constat :** la page citait `test_non_symetrie_champ_non_uniforme`, absent de la suite de tests, et présentait plusieurs tests comme s'ils validaient simultanément plusieurs propriétés (par exemple la superposition et la positivité). Elle annonçait aussi « pytest + coverage », alors que la commande CI exécute pytest sans rapport de couverture. Le slogan « l'oracle des tests est la physique elle-même » et l'idée que chaque test indique nécessairement une propriété physique violée étaient trop catégoriques.
- **Preuves :** `tests/test_metric.py`, `tests/test_constraints.py`, `tests/test_similitude.py`, `.github/workflows/ci.yml` et `pyproject.toml`.
- **Correction effectuée :** la page énumère les tests existants par nom, explique ce qu'ils testent et ce qu'ils ne testent pas, retire le test fictif et la mention de couverture non exécutée, et distingue tests ciblés, preuve mathématique et validation physique. Elle précise que la divergence n'est pas testée parce que le champ de vent multi-niveaux n'est pas implémenté.
- **Preuve de clôture :** garder cette page synchronisée avec les fichiers de tests et le workflow CI ; toute nouvelle affirmation de couverture doit pointer vers un test existant et décrire sa portée.

### B-27 — Synthèse publique de l'héritage : coût nul, transférabilité et disponibilité des données sur-généralisés

- **Statut :** formulations trop fortes, corrigées dans la synthèse web et la note de fond.
- **Emplacements :** `site/projet/audit.qmd` et `docs/01-audit-heritage-driftx.md`.
- **Constats :** l'ancienne synthèse décrivait la métrique comme « originale et transposable », le coût comme indépendant du domaine ou nul par évaluation, et les données modernes comme ayant remplacé la rareté de 2006. Elle présentait également l'absence de comparaison STE comme un fait général. Ces affirmations dépassaient les éléments documentés : une évaluation ponctuelle ne supprime pas les coûts de préparation, de caractéristique et de calibration ; l'accès aux données reste soumis à la couverture, à la résolution, à la qualité et aux droits ; une revue ciblée ne suffit pas à conclure à la nouveauté ou à l'absence exhaustive de comparateurs.
- **Correction effectuée :** les deux synthèses parlent désormais d'hypothèses historiques et de contexte ayant évolué, sans affirmer que les coûts sont nuls, que la nouveauté est établie ou que les contraintes d'accès aux données ont disparu.
- **Preuve de clôture :** comparer les coûts complets et la transférabilité sur un protocole reproductible ; documenter la couverture et les licences des données réellement utilisées ; formaliser le protocole de recherche bibliographique avant toute conclusion d'originalité.

### B-28 — Roadmap et revue G0 : statut de porte obsolète après la décision documentaire

- **Statut :** contradiction de statut corrigée.
- **Emplacements :** `site/projet/roadmap.qmd`, `docs/10-revue-adversariale-g0.md`.
- **Constat :** après la décision du 22 octobre 2026, qui a fait franchir G0 au niveau documentaire sur la base du cadrage et de l'audit de corpus, certaines pages continuaient à dire que G0 « reste bloqué » ou à présenter le prochain test comme conditionné à un franchissement futur de G0. Cela confondait le jalon documentaire G0 avec G0-A (utilité applicative) et G1 (audit des fichiers/licences).
- **Correction effectuée :** les pages précisent désormais que G0 documentaire est franchi, que G0-A reste non démontré et que G1/benchmark restent bloqués jusqu'à la vérification des fichiers bruts et des licences.
- **Preuve de clôture :** garder les statuts synchronisés dans la roadmap, la fiche G0, l'audit des corpus et les pages publiques ; ne pas traiter le franchissement documentaire comme une autorisation de benchmark.

### B-29 — Plan de validation et roadmap interne : statut G0 périmé et prochaine action obsolète

- **Statut :** contradiction documentaire confirmée et corrigée.
- **Emplacements :** `docs/03-roadmap-jdriftx-v2.md`, `docs/05-plan-validation-et-integration.md`, `docs/08-decision-utilite-et-preuve.md`.
- **Constat :** ces documents continuaient à présenter G0 comme le jalon immédiat à franchir ou à demander la rédaction future de la fiche G0, alors que la fiche et l'audit des corpus actent un franchissement documentaire le 22 octobre 2026. Un passage de `docs/08` disait également que la distinction G0-S/G0-A ne signifiait pas que G0 était franchi, ce qui contredisait le statut documentaire enregistré ailleurs.
- **Correction effectuée :** la roadmap distingue désormais G0 documentaire (franchi), G0-A (utilité applicative non démontrée), G1 (cohérence théorique et vérification des fichiers bruts) et G2 (valeur différentielle non évaluée). Le plan de validation nomme DIFLU comme corpus candidat au test discriminant, sous réserve de l'audit G1. La prochaine action demande de vérifier les fichiers bruts et de préparer un protocole, non de refaire le cadrage G0.
- **Limite :** ces corrections harmonisent le statut documentaire ; elles ne valident pas les fichiers, les licences, la pertinence physique du corpus ni la performance de J-DriftX.
- **Preuve de clôture :** vérifier après chaque décision que les statuts des documents de gouvernance restent cohérents et qu'aucun benchmark n'est annoncé avant le contrôle G1.

### B-30 — Filiation historique non établie entre la pseudo-distance travel-time et les métriques d'adaptation de maillage

- **Statut :** affirmation historique trop catégorique, corrigée.
- **Emplacement :** `site/theorie/metrique-travel-time.qmd`, section « Généalogie ».
- **Constat :** le texte affirmait que la métrique travel-time « descend » de la métrique utilisée pour l'adaptation de maillage anisotrope et que Drift-X transfère cette technologie au contrôle de la géométrie du panache. La référence Borouchaki et al. sur la génération de maillages ne suffit pas, à elle seule, à prouver une filiation historique ou une équivalence mathématique avec la pseudo-distance définie dans les sources Drift-X.
- **Correction effectuée :** le rapprochement est présenté comme une analogie conceptuelle entre deux usages de géométries dépendantes du problème. La filiation directe reste non établie faute de source explicite.
- **Preuve de clôture :** retrouver une source historique primaire décrivant ce transfert, ou conserver la formulation en termes d'analogie et non de généalogie.

### B-31 — Domaine d'entrée incomplet des primitives travel-time

- **Statut :** défaut de validation d'entrée confirmé et corrigé dans cette PR.
- **Emplacements :** `src/jdriftx/metric.py`, `tests/test_metric.py`.
- **Constat :** les fonctions convertissaient les entrées en tableaux numériques et contrôlaient leur forme, mais ne rejetaient pas systématiquement les coordonnées/vitesses non finies (`NaN`, (+\infty), (-\infty)). Dans `temps_transport`, une valeur `umin` nulle ou négative pouvait également neutraliser le garde-fou sur la vitesse; les calculs pouvaient alors retourner `NaN` ou `inf` au lieu d'un rejet explicite.
- **Correction effectuée :** les primitives rejettent maintenant les coordonnées et vitesses non finies; `temps_transport` exige en outre un seuil `umin` fini et strictement positif. Des tests paramétrés couvrent ces cas.
- **Limite :** ces contrôles améliorent la robustesse numérique des API; ils ne valident ni la définition historique complète de la pseudo-distance, ni la physique du modèle.
- **Preuve de clôture :** suite de tests et CI sur le HEAD de la PR; conserver une distinction explicite entre validité des entrées, propriétés mathématiques et validation physique.


### B-32 — Liens internes Quarto non résolus détectés par la CI

- **Statut :** deux liens internes cassés confirmés et corrigés dans cette PR.
- **Emplacements :** `site/projet/utilite-scientifique.qmd`, `site/etat-art/revue-mathematique.qmd`.
- **Constat :** le rendu Quarto de la CI signalait `projet/15-audit-corpus-g0-resultats.md` et `etat-art/mvp-scientifique.qmd) comme cibles introuvables. Les documents visés existaient, mais les chemins relatifs étaient erronés depuis les pages sources. Le rendu réussissait malgré ces avertissements : un rendu vert seul ne prouve donc pas que tous les liens internes sont résolus.
- **Correction effectuée :** les liens pointent désormais respectivement vers `../../docs/15-audit-corpus-g0-resultats.md` et `../projet/mvp-scientifique.qmd`.
- **Preuve de clôture :** nouveau rendu Quarto sans ces avertissements. À terme, ajouter un contrôle de liens internes explicite au workflow plutôt que compter uniquement sur le succès de `quarto render`.

### B-33 — Doublon bibliographique et ligne de tableau mal formée dans la comparaison Zermelo

- **Statut :** défaut éditorial confirmé et corrigé.
- **Emplacement :** `docs/14-revue-mathematique-ciblee.md`, section 4.
- **Constat :** l'article de 2024 *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* apparaissait deux fois. La seconde occurrence comportait en outre quatre cellules pour un tableau à trois colonnes, ce qui décalait la limitation scientifique hors de sa colonne prévue et pouvait rendre la comparaison ambiguë.
- **Correction effectuée :** fusion des deux lignes en une seule; la pertinence conditionnelle du comparateur et la limite (« ne démontre rien sur la pseudo-distance projetée en advection pure ») restent explicites dans la troisième colonne.
- **Preuve de clôture :** contrôle du tableau corrigé et rendu Quarto dans la CI de la branche.
