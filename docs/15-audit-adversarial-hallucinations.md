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

### A-03 — Chapitre Springer 2006 attribué à Mohammadi, Brun et Pironneau

- **Statut :** référence secondaire, métadonnées incomplètes ; existence et contenu exacts à confirmer.
- **Emplacement :** `docs/04-revues-papiers-sources.md`, `raw/README.md`.
- **Constat :** le dépôt indique que le chapitre « Reduced order modelling of dispersion » (Mohammadi, Brun & Pironneau, 2006) n'a pas été localisé en ligne et que la référence provient d'une bibliographie secondaire. Aucun éditeur/ouvrage complet, éditeurs scientifiques, pages, ISBN ou DOI n'est fourni dans la fiche actuelle.
- **Correction sûre :** garder l'entrée dans une section « références signalées mais non vérifiées » ; ne pas lui attribuer de résultats, de citations textuelles ni de contenu précis avant d'avoir une notice catalogue/éditeur ou le chapitre lui-même. Vérifier aussi qu'il ne s'agit pas d'une confusion avec le chapitre Brun & Mohammadi de 2008, qui est une publication distincte.
- **Preuve de clôture :** notice éditeur ou catalogue de bibliothèque avec titre, auteurs, ouvrage, année et pagination.

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
- **Emplacement :** `README.md` (l. 21), `docs/references.md` (l. 13), `site/references.bib` (l. 52-58), `site/references.qmd` (l. 15), `docs/01` (l. 16), `docs/04` (l. 123), `docs/bibliographie/fondements-et-heritage.md` (l. 61), `raw/README.md` (l. 44).
- **Constat :** le dépôt cite « Mohammadi & Bozon, Applied Geomatics 1, 33–39 ». La notice Springer/Crossref du DOI 10.1007/s12518-009-0006-0 donne : **Bozon, N. & Mohammadi, B.**, *Applied Geomatics* 1, 59–74 (2009).
- **Source :** https://doi.org/10.1007/s12518-009-0006-0.
- **Correction sûre :** inverser l'ordre des auteurs et corriger la pagination en 59–74.

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

### B-06 — Journal mal attribué (POD+RBF, Pékin, 2021)

- **Statut :** erroné.
- **Emplacement :** `docs/references.md` (l. 51), `docs/bibliographie/rom-et-apprentissage.md` (l. 40).
- **Constat :** le dépôt attribue l'étude POD+RBF sur 144 km² à Pékin à « Build. Sim. Eng. / Urban Clim. ». Le journal réel est le *Journal of Safety Science and Resilience* (ISSN 2666-4496). Le contenu (POD+RBF, 144 km²) est confirmé.
- **Source :** notice du journal *Journal of Safety Science and Resilience* (ISSN 2666-4496).
- **Correction sûre :** remplacer la source par *Journal of Safety Science and Resilience* (2021).

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
- **Prudence :** conformément au § 3, « erroné » n'est utilisé que pour des contradictions positives (B-01, B-02, B-04, B-05, B-06, B-07) ou une association démontrée (B-03) ; B-08 est une imprécision ; B-09 requalifie un constat de la première passe en faveur de l'existence de la référence. Les entrées non couvertes ne sont ni vraies ni fausses : elles restent à contrôler.


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

## 7. Modifications réalisées dans la PR #23

Cette PR ne se limite donc plus au registre initial. Elle :
- ajoute le registre d'audit ;
- corrige des affirmations excessives dans la revue d'état de l'art ;
- corrige la relation DATEM/ETEX dans le catalogue de données ;
- clarifie le statut G0 et la séparation entre cadrage documentaire, travail scientifique et prérequis G1.

Les changements n'établissent pas encore la validité de chaque référence du corpus. Les PDF de revue exécutive, les métadonnées bibliographiques complètes et les fichiers bruts de données restent à auditer.


### A-13 — Zenodo 22914336 : année de publication erronée

- **Statut :** erreur bibliographique confirmée ; le record et son contenu sont identifiés.
- **Emplacement :** `docs/references.md`, `docs/02-revue-etat-art-2026.md` et la bibliographie annotée.
- **Constat :** le dépôt citait « Source Term Estimation for Atmospheric Pollutant Releases » comme une ressource Zenodo de 2025. L'enregistrement 22914336 (Shafiyev et al., Bukhara State University) est publié le **22 septembre 2026 (v1)**. La description du contenu — méthodes adjointes, Tikhonov, bayésiennes/MCMC, PINN et problèmes ouverts en estimation de source — est cohérente avec la ressource.
- **Source :** [record Zenodo](https://zenodo.org/records/22914336).
- **Correction effectuée dans cette PR :** l'année est corrigée en 2026. La ressource est identifiée comme une ressource de synthèse, mais son statut de revue évaluée par les pairs n'est pas affirmé ; ses conclusions doivent être corroborées par les articles primaires.
- **Preuve de clôture :** vérifier que toutes les occurrences (notamment `site/references.bib`, `site/references.qmd` et `docs/bibliographie/identification-source-assimilation.md`) utilisent 2026 et que les affirmations associées sont attribuées à la ressource avec le niveau de preuve approprié.
