# Audit adversarial — références, sources et métadonnées

> **Périmètre :** vérifier l'identité, la version, la provenance et l'attribution des sources, et distinguer une référence erronée d'une référence non retrouvée. Les entrées conservent les constats et leurs limites ; elles ne valent pas revue systématique exhaustive.

> Le registre d'entrée est [`docs/15-audit-adversarial-hallucinations.md`](../15-audit-adversarial-hallucinations.md). Les constats sur la portée scientifique sont dans [l'audit des affirmations](15b-audit-portee-scientifique.md), et les incohérences de méthode/statut documentaire dans [l'audit méthodologique](15c-audit-methodologie-et-coherence.md).

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


## Sources externes vérifiées lors de cet audit

- Mohammadi, B. & Brun, J.-M. (2006), *Similitude généralisée et modélisation géométrique à complexité réduite*, C. R. Mécanique 334, 634–638, DOI 10.1016/j.crme.2006.06.007. Notice et bibliographie consultées : https://comptes-rendus.academie-sciences.fr/mecanique/articles/10.1016/j.crme.2006.06.007/
- Bozon, N., Sinfort, C. & Mohammadi, B., *A GIS-based atmospheric dispersion model*, notice JESA 2010, DOI 10.3166/jesa.44.445-461 : https://www.researchgate.net/publication/42782194_A_GIS-based_atmospheric_dispersion_model ; manuscrit HAL hal-00468863 : https://hal.science/hal-00468863.
- Brun, J.-M. & Mohammadi, B. (2008), *Reduced-Order Modelling of Dispersion*, Springer, DOI 10.1007/978-1-4020-8758-5_14. Notice et résumé consultés : https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion.
- Page et al. (2021), PRISMA 2020 statement : https://www.prisma-statement.org/prisma-2020.


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


## Références vérifiées exactes lors de la deuxième passe

Les entrées suivantes ont été contrôlées sur source primaire et correspondent aux métadonnées du dépôt (liste non exhaustive) :

- Mohammadi & Brun 2006, *C. R. Mécanique* 334, 634–638, DOI 10.1016/j.crme.2006.06.007 (auteurs, DOI, PDF libre ; sa bibliographie cite la thèse « 2007 » — voir A-01).
- Brun & Mohammadi 2008, chapitre Springer 14, p. 245 ; « e-sta » 2008 attestée par les bibliographies des papiers de 2009/2010 ; HAL hal-00468863 + *JESA* 2010, DOI 10.3166/jesa.44.445-461 (voir A-05).
- Muller 1979 (*Persée* 8(3), 215-227) ; Borouchaki et al. 1997 (*FEAD* 25(1-2), 61-83) ; Raupach & Thom 1981 ; Simpson 1997 ; Mohammadi & Pironneau 2001.
- Règle EPA Appendix W : FR 2024-27636, publié le 2024-11-29, effectif le 2025-01-28 ; FR 2014-01234 (29/01/2014).
- Guide EPA AGDISP-Gaussian : citation « extremely conservative » exacte ; limites 0,5 mi / 2 mi / barrières. Page EPA modèles : AgDRIFT v2.1.1, AGDISP v8.26.
- NCASI TB808 ; Bird et al. 2002 (*ET&C*, 161 essais, DOI 10.1002/etc.5620210328) ; Castro-Tanzi et al. 2025 (*STOTEN*, 18 événements, DOI 10.1016/j.scitotenv.2025.178725) ; UASS 2024 ; ANN/SVR 2022 (DOI 10.1007/s11356-022-23571-y) ; analyse de sensibilité 2023 (DOI 10.1007/s10668-023-04452-x) ; *Agronomy* 14(9):1977 ; Verveecken & Meyers 2015 (*Building and Environment*, DOI 10.1016/j.buildenv.2015.05.008, facteur 2500 confirmé).
- HAL hal-04310899 (ECCOMAS UNCE 2024) ; CMAME 2024 (Bologne) ; cea-04810109 (MCxM) ; Ayoub et al. 2024 (DOI 10.1007/s00477-024-02738-8) ; chapitre Springer 2025 (DOI 10.1007/978-3-032-02728-3_53) ; Hutchinson 2017 (*Information Fusion* 36, 130-148) ; MDPI *Appl. Sci.* 16(4):1833 (2026) ; plugin QGIS Sebapac90 (README : « based on Masters and Ela (2008) »).
- SICC 2026 session 3 ; NARAC ; ADMLC ; OIEau ; APSI ; revue IJRISS AERMOD (Shafie) ; TIERRAS (Zenodo 15794259, >400 essais) ; ERIES (4TU, Sofia, éthylène, 76 points, S1/S2) ; CAPRIV (Perriot et al. 2024, *Data in Brief* 54:110366, DOI vérifié) ; DIFLU (campagne hélium IRSN/ASNR confirmée institutionnellement) ; arrêté du 4 mai 2017 (LEGI + agriculture.gouv.fr) ; rapport InVS « quatre sites de l'Hérault en 2006 » (Santé publique France).

Réserves : les effectifs de CAPRIV (« 3 792 observations / 38 variables », `docs/11` l. 34) et les détails de DIFLU restent à recontrôler sur les sources primaires. Mise à jour du 28/10/2026 : la fiche Recherche Data Gouv est désormais consultable via indexation et confirme le DOI, la licence Etalab 2.0, 114 fichiers et leurs métadonnées descriptives ; l’article associé décrit 15 expériences. La valeur 19 correspond au nombre d’observations du fichier `DIFLU_media_dictionary.tab`, pas à un décompte établi d’expériences. Les fichiers bruts restent non inspectés.


### A-10 — NOAA DATEM et ETEX : contradiction interne dans le catalogue

- **Statut :** erreur factuelle interne confirmée et corrigée dans cette PR.
- **Emplacement :** `docs/12-catalogue-donnees-transport-dispersion.md`, première ligne de la table des corpus.
- **Constat :** le catalogue affirmait que NOAA DATEM « inclut ETEX et CAPTEX », tandis que `docs/15-audit-corpus-g0-resultats.md` indique explicitement qu'ETEX n'est pas inclus dans DATEM et renvoie au JRC pour le corpus ETEX. Les deux formulations ne peuvent pas être vraies simultanément.
- **Contrôle externe :** la documentation NOAA DATEM et le site JRC présentent des ressources distinctes ; la fiche ETEX du JRC propose les données des deux lâchers séparément. [NOAA DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) ; [JRC ETEX datasets](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm).
- **Correction effectuée dans cette PR :** le catalogue indique maintenant que DATEM inclut notamment CAPTEX, et que l'ETEX est documenté séparément par le JRC.
- **Preuve de clôture :** vérifier les autres lignes du catalogue contre les sources de données officielles, puis ajouter un contrôle automatisé des contradictions entre fiches.


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


### B-33 — Doublon bibliographique et ligne de tableau mal formée dans la comparaison Zermelo

- **Statut :** défaut éditorial confirmé et corrigé.
- **Emplacement :** `docs/14-revue-mathematique-ciblee.md`, section 4.
- **Constat :** l'article de 2024 *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* apparaissait deux fois. La seconde occurrence comportait en outre quatre cellules pour un tableau à trois colonnes, ce qui décalait la limitation scientifique hors de sa colonne prévue et pouvait rendre la comparaison ambiguë.
- **Correction effectuée :** fusion des deux lignes en une seule; la pertinence conditionnelle du comparateur et la limite (« ne démontre rien sur la pseudo-distance projetée en advection pure ») restent explicites dans la troisième colonne.
- **Preuve de clôture :** contrôle du tableau corrigé et rendu Quarto dans la CI de la branche.
