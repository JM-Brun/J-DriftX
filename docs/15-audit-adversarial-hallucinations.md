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
