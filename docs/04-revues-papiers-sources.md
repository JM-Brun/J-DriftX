# Revues détaillées des papiers sources (corpus Drift-X, 2006–2009)

> Document établi en octobre 2026. Objectif : relire **papier par papier** le corpus historique de Drift-X, extraire un maximum d'information vérifiable de chaque source, et expliciter ce que J-DriftX reprend de chacune.
> Méthode : chaque fiche distingue clairement (i) le contenu **extrait** de la source (résumés verbatim, équations, détails techniques, issus des pages accessibles ou du chapitre fourni par l'auteur), (ii) le **statut d'accès** de la source, et (iii) les apports pour J-DriftX. Rien n'est affirmé qui ne soit pas vérifiable dans une source citée.
> Fichier complémentaire du dossier de travail : les autres documents sont <code>01-audit-heritage-driftx.md</code>, <code>02-revue-etat-art-2026.md</code>, <code>03-roadmap-jdriftx-v2.md</code>, <code>references.md</code>.

## 0. Vue d'ensemble et accès aux sources

| # | Source | Accès en ligne (oct. 2026) | Information extraite dans cette revue |
|---|---|---|---|
| 1 | Brun 2006 (thèse) | Non disponible (jamais déposée/numérisée) | Métadonnées via citations croisées uniquement |
| 2 | Mohammadi & Brun 2006 (C. R. Mécanique) | Résumé FR+EN libre ; texte intégral sur abonnement | Résumés verbatim, mots-clés, pagination |
| 3 | Mohammadi, Brun & Pironneau 2006 (chapitre) | Non localisé | Citation exacte via bibliographie du papier n° 7 |
| 4 | Brun & Mohammadi 2008 (Springer, chap. 14) | Chapitre fourni par l'auteur ; notice publique (DOI) | Résumé + pages 245–246 (OCR) : introduction et début de la section ROM |
| 5 | Bozon, Mohammadi & Sinfort 2008 (e-sta) | Non localisé (archives introuvables) | Citation exacte via bibliographie des papiers n° 6 et 7 |
| 6 | Bozon, Sinfort & Mohammadi 2009 (STIC & Env. / HAL) + version journal JESA 2010 | Manuscrit auteur intégral accessible (HAL via ResearchGate) ; DOI JESA valide (accès réservé) | Quasi-intégralité : équations, multi-niveaux, correction topographique, architecture logicielle |
| 7 | Mohammadi & Bozon 2009 (Applied Geomatics) | Résumé libre ; texte intégral sur abonnement | Résumé verbatim, extraits d'introduction et bibliographie |

Points notables de cette campagne de relecture : la source n° 6 s'est révélée la plus riche — le manuscrit auteur complet est accessible et documente l'architecture logicielle historique (cœur Fortran + plugin QGIS) et la construction multi-niveaux. Une **version journal inédite dans notre bibliographie** a été identifiée et vérifiée (JESA 2010, DOI valide). Détail en section 8.

## 1. Fiche — J.-M. Brun (2006), thèse de doctorat

**Référence.** Brun, J.-M. (2006). *Modélisation à complexité réduite de la dérive*. Thèse de doctorat, Université Montpellier II.

**Statut d'accès.** Introuvable en ligne à ce jour (theses.fr, HAL, moteur général). Jamais numérisée ni déposée. Le document papier est en possession de l'auteur. Action roadmap : M0 (dépôt HAL).

**Ce que l'on sait par recoupement (sources vérifiables).**
- Le titre exact et l'année sont confirmés par la bibliographie du chapitre Springer 2008 (source n° 4) et par la bibliographie du papier Applied Geomatics 2009 (source n° 7), qui citent toutes deux : « J. M. Brun. Modélisation à complexité réduite de la dérive. PhD thesis, University of Montpellier, 2006. »
- Le résumé du C. R. Mécanique 2006 (source n° 2, mêmes auteurs, même année) décrit le contenu scientifique contemporain de la thèse : assimilation de données partielles, solutions de similitude dans une métrique non symétrique basée sur les temps de transport, sans EDP ni maillage, évaluation ponctuelle.
- Le chapitre 2008 (source n° 4) précise que la hiérarchie multi-niveaux traite « du rang de plants de vigne aux bassins versants », avec le champ proche de la buse construit à partir d'observations expérimentales — soit la partie viticulture/ITAP du travail de thèse.

**Apports pour J-DriftX.** La thèse est le document fondateur, mais aucune information supplémentaire ne peut en être extraite tant qu'elle n'est pas numérisée. Le dépôt HAL (action M0) est le prérequis pour sa relecture.

## 2. Fiche — B. Mohammadi & J.-M. Brun (2006), C. R. Mécanique

**Référence.** Mohammadi, B. & Brun, J.-M. (2006). « Similitude généralisée et modélisation géométrique à complexité réduite ». *C. R. Mécanique* 334(10), 634–638, octobre 2006. DOI 10.1016/j.crme.2006.06.007. Notice : https://www.em-consulte.com/article/69927

**Statut d'accès.** Résumés français et anglais en accès libre sur la notice EM-consulte ; texte intégral sur abonnement ; papier de 5 pages.

**Résumé verbatim (extrait de la notice).**
- FR : « Nous présentons une modélisation à complexité réduite pour le transport et la dispersion d'un scalaire passif pour les applications environnementales. Le modèle utilise l'assimilation de données partielles d'observations. On propose une généralisation des solutions de similitudes pour les jets dans une métrique non symétrique basée sur les temps de transport. L'approche ne nécessite pas la solution d'EDP, donc pas de maillage et on peut accéder à la solution en un point sans avoir à la calculer partout. »
- EN : « We present low complexity models for the transport of passive scalars for environmental applications. The model uses partial observations assimilation. Similitude solutions are proposed in a non symmetric metric based on travel times. The approach does not require the solution of any PDE and is mesh free. Also, the solution can be computed in one point only without computing the whole solution. »
- Mots-clés : Mécanique des fluides numérique, Dispersion, Transport, Similitude, Modèles réduits, Jets (EN : Computational fluid mechanics, Dispersion, Transport, Similarity, Reduced order models, Plumes).

**Lecture.** C'est la **première formulation publique compacte** du paradigme. En 5 pages, les quatre piliers sont déjà tous nommés : (i) assimilation de données partielles, (ii) solutions de similitude **généralisées dans une métrique non symétrique basée sur les temps de transport**, (iii) pas d'EDP donc pas de maillage, (iv) évaluation en un point isolé. La mention « jets » dans les mots-clés confirme l'ancrage dans les solutions de similitude des jets et panaches neutres, et « plumes » la visée panache. Aucune topographie ni SIG dans ce papier : c'est le cœur mathématique seul.

**Apports pour J-DriftX.** Référence-cadre du noyau Python : la formulation de la métrique τ et la promesse d'évaluation ponctuelle correspondent exactement aux modules <code>similitude</code> et <code>metrique</code> du socle, et aux tests « évaluation ponctuelle » et « non-symétrie de τ ».

## 3. Fiche — B. Mohammadi, J.-M. Brun & O. Pironneau (2006), chapitre Springer

**Référence.** Mohammadi, B., Brun, J.-M. & Pironneau, O. (2006). « Reduced order modelling of dispersion ». In *Numerical Analysis and Scientific Computing with PDE and their challenging applications*, Springer.

**Statut d'accès.** Non localisé en ligne : la notice du recueil n'a pas été trouvée en accès ouvert. La référence exacte est confirmée par la bibliographie du papier Applied Geomatics 2009 (source n° 7), qui cite « Mohammadi B, Brun JM, Pironneau O (2006) Reduced order modelling of dispersion ».

**Lecture (par recoupement).** Trois indices rapprochent ce chapitre du chapitre 14 de 2008 (source n° 4) : mêmes deux premiers auteurs, même intitulé à un mot près, et présence d'O. Pironneau — co-auteur avec Mohammadi de la lignée « shape optimization / sensibilité incomplète » (Applied Shape Optimization for Fluids, 2001, citée dans le chapitre 2008). Il s'agit vraisemblablement d'une étape intermédiaire entre la note CR 2006 (5 pages) et le chapitre long de 2008, mais **ce point ne peut pas être affirmé sans le document** : à revoir à l'obtention du recueil.

**Apports pour J-DriftX.** Tant que le document est introuvable, la seule valeur est la traçabilité de la lignée Pironneau (sensibilité incomplète) — déjà couverte par le chapitre 2008, mieux accessible.

## 4. Fiche — J.-M. Brun & B. Mohammadi (2008), chapitre Springer CSM vol. 16

**Référence.** Brun, J.-M. & Mohammadi, B. (2008). « Reduced-Order Modelling of Dispersion ». In Glowinski, R. & Neittaanmäki, P. (eds), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, Dordrecht, chap. 14, p. 245 et s. DOI 10.1007/978-1-4020-8758-5_14

**Statut d'accès.** Version longue de référence, fournie par l'auteur. Les pages 245–246 ont été océrisées pour cette revue (résumé, introduction, début de la section 2). Affiliations : J.-M. Brun, Cemagref/ITAP, Montpellier ; B. Mohammadi, I3M, Université Montpellier II.

**Résumé verbatim (extrait).** « We present low complexity models for the transport of passive scalars for environmental applications. Multi-level analysis has been used with a reduction in dimension of the solution space at each level. Similitude solutions are used in a non-symmetric metric for the transport over long distances. Model parameters identification is based on data assimilation. The approach does not require the solution of any PDE and, therefore, is mesh free. The model also permits to access the solution in one point without computing the solution over the whole domain. Sensitivity analysis is used for risk analysis and also for the identification of the sources of an observed pollution. » Mots-clés : Reduced order modelling, source identification, risk analysis by sensitivity, non-symmetric geometry.

**Contenu extrait des pages 245–246 (OCR).**
- *Introduction.* Motivation : contamination de l'air et de l'eau par les pesticides ; objectif d'un coût de calcul suffisamment bas pour rendre réalistes « assimilation-simulation » et **analyse de risque statistique par simulations Monte Carlo**. Données disponibles incomplètes, forte variabilité, grand nombre de paramètres — d'où la réduction de l'espace des solutions. Construction multi-niveaux : « a given level provides the inlet condition for the level above ».
- *Champ proche.* « A near field (to the injection device) search space is build using experimental observations » — le champ proche de la buse est construit sur des mesures ; la quantité quittant la sous-couche atmosphérique est ensuite estimée et devient le candidat au transport longue distance via les solutions de similitude pour couches de mélange et panaches, « connues en métrique cartésienne ».
- *Verrou central.* « An original contribution here is the generalization of these solutions in a non-symmetric travel-time based metric to account for non-uniform winds. »
- *Contraintes physiques.* Les solutions construites doivent rester solutions du modèle direct : **divergence nulle du vent généré, conservation, positivité, linéarité** de l'équation de transport.
- *Annoncé de la suite (non couvert par l'OCR).* Comparaison avec une simulation EDP, configurations multi-sources, analyse de sensibilité d'une pollution détectée.
- *Section 2 (début).* Positionnement vis-à-vis des ROM classiques : la solution d'état V(p) est remplacée par une projection sur un sous-espace S(w_n) généré par des snapshots dans l'approche classique (n ≪ N, référence [VP05]) ; « In our approach, we aim to remove the calculation of these snapshots ». Le modèle direct est remplacé par un modèle approché p → v(p) plus facile à évaluer, avec un **domaine de validation local** (pas nécessairement le même modèle réduit sur toute la plage des paramètres). Renvoi au concept de **sensibilité incomplète** [MP01] : « the linearization is performed not for the direct model but for an approximate state equation ».
- *Bibliographie visible (extraits).* Thèse Brun 2006 ; Borouchaki, George & Mohammadi (1997), Delaunay mesh generation governed by metric specifications ; Mohammadi & Pironneau, Analysis of the k-epsilon turbulence model ; Mohammadi & Pironneau, Applied shape optimization for fluids (2001) ; Ivorra (2006), thèse Semi-deterministic global optimization. Ces entrées confirment la lignée « métriques de l'adaptation de maillage » et « optimisation de forme » du projet.

**Apports pour J-DriftX.** C'est le **cahier des charges scientifique** du noyau : multi-niveaux avec entrée/sortie de sous-couche, métrique τ non symétrique, quatre contraintes physiques (deux déjà testées dans le socle : conservation et non-symétrie), sensibilité/identification. Les pages restantes (exemples numériques, analyse de sensibilité) sont la prochaine extraction à faire sur le document papier.

## 5. Fiche — N. Bozon, B. Mohammadi & C. Sinfort (2008), e-sta

**Référence.** Bozon, N., Mohammadi, B. & Sinfort, C. (2008). « Similitude and non symmetric geometry for dispersion modelling ». e-sta, vol. 5, numéro spécial STIC et Environnement'07.

**Statut d'accès.** Non localisé en ligne : les archives du périodique e-sta (revue de la SEE) n'ont pas été trouvées en accès ouvert. La référence exacte (revue, volume, numéro spécial, année) est confirmée par la bibliographie du papier Drift-X (source n° 6), qui cite : « N. Bozon, B. Mohammadi and C. Sinfort, Similitude and non symmetric geometry for dispersion modelling, Special issue STIC and Environnement'07, e-sta vol. 5, 2008 ».

**Lecture (par recoupement).** C'est le **chaînon manquant** entre le cœur mathématique 2006 (sources 2–4) et la plateforme SIG 2009 (source 6) : première publication avec N. Bozon et C. Sinfort (ITAP), titre centré sur « similitude et géométrie non symétrique » — soit l'introduction de la topographie/non-symétrie géométrique dans le modèle, avant le couplage SIG complet. Le contenu exact ne peut pas être affirmé sans le document.

**Apports pour J-DriftX.** Prioritaire à localiser (contact SEE / auteurs) pour dater précisément l'arrivée de la correction topographique dans le modèle. Rien d'extractible à ce stade au-delà de la citation exacte.

## 6. Fiche — N. Bozon, C. Sinfort & B. Mohammadi (2009), plateforme Drift-X — la fiche la plus riche

**Référence.** Bozon, N., Sinfort, C. & Mohammadi, B. (2009). « A GIS-based atmospheric dispersion model ». Actes de STIC & Environnement, Calais (2009) ; manuscrit auteur déposé sur HAL : https://hal.science/hal-00468863 (version 1, 31 mars 2010). **Version journal identifiée lors de cette revue** : *Journal Européen des Systèmes Automatisés (JESA)* 44(4-5), 445–461, 2010, DOI 10.3166/jesa.44.445-461 (DOI vérifié : il résout vers la page revue, accès réservé).

**Statut d'accès.** Manuscrit auteur intégral consulté (17 pages) via le dépôt HAL (relais ResearchGate). Affiliations : N. Bozon, Cemagref–UMR ITAP ; C. Sinfort, Montpellier SupAgro–UMR ITAP ; B. Mohammadi, Université Montpellier 2–UMR5149, I3M.

**Résumé verbatim (extraits).** « This work aims to model pesticide atmospheric dispersion during vine spraying, from the plot to the watershed scales, using fluid mechanics equations and open-source GIS programming capabilities. [...] Our goal is to provide a GIS based atmospheric transport simulation platform at very low calculation cost using solution space reduction and reduced order modelling. [...] ground variations are implemented in the model using digital elevation model (DEM). The use of DEM is an asset to replace former Cartesian outputs by georeferenced raster pesticide cloud and also, it allows to use the model on any area. [...] The plateform has been developed as a plugin for Quantum GIS open source software. » Résumé français équivalent présent. Mots-clés : Atmospheric Dispersion, risk analysis, reduced-order modelling, Gaussian plume model, multi-scaled, digital elevation models, open source GIS development, Quantum GIS.

**Contenu extrait — modèle (section 2).**
- *Forme du panache.* Le scalaire passif émis en un point et transporté par un écoulement plan uniforme U suivant x s'écrit c(x,y,z) = c_c(x) · f(r, δ(x)) avec r = √(y²+z²), c_c ~ exp(−a(U)·x) le comportement le long de l'axe central, f ~ exp(−b(U,δ)·r) l'étalement transverse, δ(x) l'épaisseur (parabolique pour un jet laminaire, linéaire en turbulent, par analogie avec les couches de mélange et panaches neutres), a(.) positive monotone décroissante et b(.,.) positive, croissante en U, décroissante en δ. Cette solution est ensuite généralisée dans la métrique non symétrique des temps de transport ; pour la topographie, « the flow is locally rotated to remain parallel to the ground ».
- *Construction multi-niveaux.* Cascade de domaines rectangulaires homothétiques emboîtés ω_i (ω_0 = Ω le domaine complet), le vent total étant la somme des restrictions : chaque restriction est obtenue par interpolation aux 4 coins q_j du rectangle (poids λ_j(x), partition de l'unité : Σ λ_j = 1, λ_j(x_i) = δ_ij, éq. [3]). Cette construction **garantit que la restriction reste à divergence nulle** et compatible avec le champ global ; la concentration est restreinte de la même façon (éq. [4]), ce qui **garantit la conservation de la masse** dans chaque sous-domaine (l'intégrale exacte par règle du trapèze à 4 points est soulignée). En pratique : **3 niveaux**, de Ω ≈ 10 km² à ω_2 ≈ 10 m², avec un échantillonnage type de 20×20 par niveau — topographie tous les 500 m au niveau grossier, tous les 50 cm au niveau fin.
- *Données intégrales.* Connaissant la quantité totale injectée K sur [0,T], le modèle fournit des estimateurs analytiques : dépôt au sol C_g(x,y) = ∫ c dz (au-dessous de z_0) ; quantité encore en suspension au-delà d'un rayon R_0 : C_a = K − ∫ C_g dV. Ces quantités sont la base de l'analyse de risque géoréférencée.
- *Correction topographique multi-niveaux (section 2.2).* À chaque niveau, une correction de vent u_t_i est ajoutée (éq. [5]) : correction de type **Bernoulli-Newton** (référencée comme largement utilisée en aéronautique pour la distribution de pression autour d'un cylindre en écoulement potentiel) : u_t_i = −(1/ρ) sgn(U_t) ∇p_i, avec p_i fonction d'une pression locale de référence calculée sur la vitesse moyenne d'entrée aux coins entrants. Sont distingués la normale au sol n_t_i (issue du MNT) et la normale au sous-domaine n_i — orthogonales en l'absence de relief. Le papier souligne qu'une topographie non constante brise la symétrie : même à vent uniforme, la cross-diffusion n'est pas symétrique sur une pente quand la dispersion est parallèle aux iso-contours. Les fonctions a et b du modèle gaussien sont ensuite **corrigées sous contrainte de conservation de la masse** entrante (éq. [7]) : a_i_t = a_i · ||u_i + u_t_i|| / ||u_i|| — si la topographie accélère l'écoulement local, la dispersion va plus loin vers l'aval avec moins de cross-diffusion (b diminué par la contrainte).

**Contenu extrait — couplage SIG (section 3).**
- *Choix d'architecture.* Couplage **loose** (par opposition aux couplages « tight » ou « integrating ») : interfaces développées avec un minimum d'hypothèses entre les parties, réduisant le risque qu'un changement dans une application force un changement dans l'autre ; coût de développement réduit, réutilisation d'un SIG existant plutôt qu'écriture d'un SIG complet. Choix de **QGIS** : API C++ robuste exposée par des bindings Python, permettant des plugins dédiés.
- *Architecture réelle du prototype (dette technique documentée).* Le cœur de calcul est un **programme Fortran** : le plugin QGIS extrait le MNT par commandes **GDAL** (deux appels successifs à gdal_translate : extraction Float32 de l'emprise définie par l'utilisateur, puis export en grille ESRI ASCII), convertit la grille en triplets x,y,z (classe grd2xyz, inspirée d'un code de l'USGS), et transmet le tout au Fortran **au format CSV** ; le Fortran lit le fichier (open/do/read sur le CSV) et sort ses résultats en CSV (longitude, latitude, concentration), réimportés dans QGIS. Le zoom multi-niveaux est défini interactivement par l'utilisateur par un outil de type « Region Tool » (code inspiré d'un outil de B. S. Rowlingson, Université de Lancaster), chaque rectangle dessiné définissant un nouveau niveau.
- *Cartographie des nuages.* Sorties vecteur : écriture de shapefiles ESRI via QgsVectorFileWriter (URI CSV avec délimiteur et champs x/y), coloration continue via QgsContinuousColorRenderer (vert→rouge sur le champ concentration). Sorties raster : interpolation des points par **gdal_grid** (algorithme inverse-distance, paramètres power=1.0, smoothing=50.0, driver VRT, sortie GeoTIFF Float64), masquage du nodata par découpe vectorielle, rendu pseudo-couleur + transparence via QgsRasterLayer.
- *Limites assumées (extrait).* L'objectif du modèle réduit est de fournir « mean tendancies of the spray drift with very low calculation cost », et « potential errors are duplicated into the GIS » ; les traitements automatisés (génération de MNT, interpolation) « can also add some more spatial incoherence and introduce a new level of uncertainties ».

**Conclusion du papier (extrait).** « The solution search space has been reduced using a priori physical information and a non symmetric metric based on migration times has been used to generalize injection and plume similitude solutions in the context of variable flow fields. »

**Apports pour J-DriftX.** Fiche la plus opérationnelle du corpus : elle documente (i) la forme gaussienne exacte avec ses fonctions a et b et leurs monotonies — directement testables (tests conservation/non-symétrie) et implémentables ; (ii) la construction multi-niveaux à 4 coins avec ses deux garanties (divergence nulle, conservation) — à réimplémenter en Python et à couvrir par des tests ; (iii) la correction topographique Bernoulli-Newton et la contrainte de masse sur a/b ; (iv) l'architecture historique Fortran+CSV+QGIS que le noyau Python moderne remplace avantageusement (le format CSV d'échange reste une bonne interface de compatibilité) ; (v) les sorties raster/vecteur et l'interpolation invdist comme spécification de la couche SIG future. La version journal JESA 2010 doit être ajoutée à la bibliographie (fait dans <code>references.md</code>).

## 7. Fiche — B. Mohammadi & N. Bozon (2009), Applied Geomatics

**Référence.** Mohammadi, B. & Bozon, N. (2009). « GIS-based atmospheric dispersion modelling ». *Applied Geomatics* 1, 33–39. DOI 10.1007/s12518-009-0006-0

**Statut d'accès.** Résumé libre (notice Springer) ; texte intégral sur abonnement (la page Springer est protégée contre les robots). 7 pages.

**Résumé verbatim (extrait de la notice).** « A multileveled, low-complexity model for flow field reconstruction and transport of passive scalars within an open-source geographic information system (GIS) is presented. Similitude solutions are used in a nonsymmetric metric for the transport, and the model parameters' identification is based on data assimilation. »

**Extraits vérifiables (introduction et bibliographie, via extraits accessibles).** « In a previous work, we have treated the problem of agricultural pesticide emission and dispersion by coupling local (i.e., emission and near-field distribution) and global (i.e., transport over large distance) models (Brun 2006; Mohammadi et al. 2006). In this approach, the local model provides the inlet conditions for the levels above. » La bibliographie du papier cite notamment : Markiewicz (2006), rapport Modelling of air pollution dispersion (vol. 2511) ; Mohammadi & Pironneau (1994), Analysis of the k-epsilon turbulence model ; Mohammadi & Pironneau (2001), Applied shape optimization for fluids ; Mohammadi, Brun & Pironneau (2006), Reduced order modelling of dispersion.

**Lecture.** Déclinaison journal de la plateforme : c'est la version « proceedings SIG » du même travail que la source n° 6, avec la reconstruction de champ de vent (« flow field reconstruction ») comme accent propre. Le passage extrait reformule explicitement le principe multi-niveaux : le modèle local (émission, champ proche) fournit les conditions d'entrée des niveaux supérieurs (transport longue distance) — le principe « entrée/sortie de niveaux » du chapitre 2008, ici appliqué aux échelles de la pulvérisation.

**Apports pour J-DriftX.** Référence la plus courte du corpus : utile comme synthèse de positionnement (réduction + métrique + assimilation + SIG en 7 pages) et pour sa bibliographie, qui relie le projet aux fondements (k-epsilon, optimisation de forme, Markiewicz). Le texte intégral est à récupérer pour détailler la partie « flow field reconstruction » (probablement proche de la section 2.1 de la source n° 6).

## 8. Découvertes bibliographiques de cette revue

1. **Version journal JESA 2010 du papier plateforme** : *Journal Européen des Systèmes Automatisés* 44(4-5), 445–461, DOI 10.3166/jesa.44.445-461 — DOI vérifié (il résout vers la page revue, accès réservé) ; vol/pages/année confirmés par la notice ResearchGate de la publication. Ajoutée à <code>references.md</code> et <code>site/references.qmd</code>.
2. **Titre exact de la thèse 2006** confirmé par deux bibliographies indépendantes (chapitre 2008, papier Applied Geomatics 2009) : « Modélisation à complexité réduite de la dérive », PhD thesis, University of Montpellier, 2006.
3. **Lignée méthodologique confirmée** : les bibliographies des sources 4, 6 et 7 pointent toutes vers Borouchaki–George–Mohammadi 1997 (métriques de maillage), Mohammadi–Pironneau (k-epsilon, Applied Shape Optimization 2001) — la matrice intellectuelle « métrique + optimisation de forme + sensibilité » du projet est ainsi traçable dans les sources elles-mêmes.
4. **Commanditaires académiques du papier plateforme** : affiliations Cemagref–UMR ITAP, Montpellier SupAgro–UMR ITAP et Université Montpellier 2–UMR5149 (I3M) — documentées pour la fiche « héritage » du site.

## 9. Ce qui reste à extraire (feuille de route documentaire)

| Priorité | Action | Verrou |
|---|---|---|
| Haute | Déposer la thèse 2006 sur HAL (action M0), puis en faire la fiche complète | Document en possession de l'auteur |
| Haute | Récupérer le texte intégral du chapitre 2008 au-delà des pages 245–246 (exemples numériques, analyse de sensibilité, identification de source) | Chapitre fourni par l'auteur — OCR à poursuivre |
| Moyenne | Localiser l'article e-sta 2008 (archives SEE) | Introuvable en ligne — contacter la SEE ou les auteurs |
| Moyenne | Localiser le recueil Springer 2006 du chapitre Mohammadi–Brun–Pironneau | Recueil introuvable en accès ouvert |
| Moyenne | Obtenir le texte intégral CR Mécanique 2006 et Applied Geomatics 2009 | Abonnements (l'auteur a vraisemblablement les tirés-à-part) |
| Basse | Obtenir l'exemplaire JESA 2010 de la source n° 6 pour vérifier les éventuelles évolutions vs le manuscrit HAL | Accès réservé |

---

*Fiches établies uniquement à partir de contenus extraits et vérifiables ; les passages verbatim sont en anglais ou français d'origine, non reformulés silencieusement. Sources d'accès consultées en octobre 2026 : EM-consulte (notice CR Mécanique), HAL hal-00468863 via relais ResearchGate, notice Springer/Applied Geomatics, OCR du chapitre Springer 2008 fourni par l'auteur.*
