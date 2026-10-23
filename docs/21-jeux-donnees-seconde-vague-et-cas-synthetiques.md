# Jeux de données seconde vague et cas synthétiques à vérité connue (issues #13, #17, #43)

> **Statut : document de travail du 23 octobre 2026**, suite directe de l’[audit technique de première vague](20-audit-technique-jeux-donnees.md) (DIFLU, DATEM, ETEX, ERIES). Deux objets : (1) auditer une **seconde vague de jeux de données réels** — classiques champ proche HARMO, soufflerie graduée, dérive de pulvérisation — ; (2) définir une **démarche de cas synthétiques à vérité connue**, pour avancer sans attendre les téléchargements manuels ni les confirmations de licence.
> **Limite de méthode explicite.** Comme en première vague, aucun fichier de données n’a été téléchargé ni inspecté unité par unité ; les points portant sur le contenu des fichiers restent **non vérifiés**, jamais validés. Exception de méthode : les pages d’archive Zenodo (dérive de pulvérisation) ont été lues directement et leurs licences sont confirmées en page.

## Synthèse

| Candidat | Type / échelle | Accès documenté (23/10/2026) | Licence | Unité d’indépendance | Apport propre |
|---|---|---|---|---|---|
| Prairie Grass (1956) | Traceur gazeux (SO2), 50–800 m, source à 46 cm | Archive numérique JSI (Harmonisation) ; volumes originaux en PDF (archive.org) ; inclus dans le guide ASTM D6589 | Non affichée — à vérifier au téléchargement | **Le lâcher : 68 périodes de 10 min** | Grand n en champ proche, source quasi au sol, micrométéo co-localisée — la niche exacte de J-DriftX |
| Model Validation Kit (Kincaid, Bull Run, Copenhagen, Lillestrøm, Indianapolis) | Panaches flottants en hauteur, 1–50 km | Kit v2.0 (2005) et logiciel BOOT téléchargeables ; extension 2012 (Kincaid doublé, Bull Run, Round Hill, Prairie Grass) | Non affichée — à vérifier | L’heure de lâcher | Panache flottant (hors socle « source au sol ») et 30 ans de méthodologie d’évaluation |
| CEDVAL et CODASC (Hambourg, TU/e) | Soufflerie : couche limite → cube isolé → rangées → canyon | Pages publiques ; accessibilité libre de CEDVAL documentée par de nombreux travaux tiers | À vérifier — certaines séries d’Hambourg exigent un accord de données signé (COST ES1006) | La configuration d’écoulement | Vent exactement connu, complexité graduée |
| Dérive de pulvérisation : deux jeux Zenodo et modèle DAD-drift | Dépôt au sol (0–5 m) ; modèle de référence complet | Zenodo (jeux) ; DAD-drift v1.0 (code source, documentation, exemples) | **CC BY 4.0 confirmées** (jeux) ; licence du code à documenter | Le passage / la configuration | Seule voie ouverte pour l’observable dérive ([issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)) |

## 1. Prairie Grass (1956) — le corpus champ proche à grand n

- **Dispositif.** Juillet–août 1956, plaine homogène du Nebraska (O’Neill) ; SO2 relâché en continu pendant 10 min à 46 cm au-dessus du sol ; prélèvements à 1,5 m sur cinq arcs à 50, 100, 200, 400 et 800 m sous le vent ; 68 périodes d’échantillonnage exploitées (70 lâchers réalisés selon le rapport original), nombre égal de cas de jour et de nuit.
- **Micrométéo co-localisée.** Température de l’air et pression de vapeur sur 8 hauteurs, vitesse du vent sur 7 hauteurs, température du sol à 6 profondeurs ; vent mesuré à 2 m à deux emplacements — les conditions de stabilité sont reconstructibles essai par essai.
- **Accès.** Archive de données de traceurs JSI (initiative Harmonisation) : la majorité du jeu en format numérique, avec les références originales (Barad 1958 ; Haugen 1959) ; le rapport original est en PDF sur archive.org (DTIC AD0152573) ; le guide ASTM D6589 (évaluation statistique des modèles de dispersion) embarque aussi le jeu.
- **Pourquoi cela compte.** C’est le seul corpus champ proche à **grand nombre d’essais indépendants** (n ≈ 68, contre 2 pour ETEX et 15–19 à trancher pour DIFLU) ; source quasi au sol, terrain plat, distances 50–800 m : la niche exacte du modèle réduit, avec des conditions de stabilité variées jour/nuit.
- **Verrous.** Âge du jeu (1956) ; traceur SO2 légèrement réactif (sur 10 min et à moins de 800 m, la perte est vraisemblablement faible mais à documenter) ; licence non affichée ; formats et unités à inspecter au téléchargement.

## 2. Model Validation Kit et classiques EPRI — le panache flottant

- **Composition.** Kit = Kincaid (Illinois), Copenhagen, Lillestrøm, complété par Indianapolis (depuis 1997) ; logiciel BOOT pour les statistiques ; version 2.0 (octobre 2005), BOOT mis à jour (février 2007).
- **Extension 2012.** Données EPRI Kincaid doublées (seconde moitié des données SF6 ; concentrations horaires et à 5 min de SO2), plus Bull Run (Tennessee), Round Hill et de nouvelles données Prairie Grass (dont des profils verticaux).
- **Pourquoi cela compte.** Cheminées élevées et **panache flottant** : un régime absent du socle première vague (rejets au sol ou de cheminée sans flottabilité) — utile si J-DriftX étend sa similitude à la montée de panache ; la méthodologie d’évaluation du Kit (BOOT, valeurs near-centreline, métriques NMSE/FAC2) est réutilisable telle quelle pour le protocole G1.
- **Verrous.** Licences non affichées ; observable horaire moyen ; la montée de panache suppose une extension du modèle (ou une exclusion explicite du périmètre G1) ; météorologie ancienne.

## 3. CEDVAL et CODASC — la soufflerie à complexité graduée

- **CEDVAL** (laboratoire de soufflerie environnementale, Institut météorologique de l’université de Hambourg) : compilation de jeux de données de soufflerie avec documentation complète des conditions aux limites et assurance qualité pendant les mesures ; configurations graduées (couche limite seule, cube isolé A1, rangées et matrices de bâtiments B1, etc.), très largement utilisées par la communauté CFD ; la compilation sœur CEDVAL-LES documente trois couches limites (rugosités et échelles 1:500 à 1:225).
- **CODASC** (université de technologie d’Eindhoven, codasc.de) : concentrations normalisées de traceur dans des canyons de rue en soufflerie, sources linéiques — complément « routier » de R-LINE et des barrières EPA déjà listés dans le [catalogue du site](https://github.com/JM-Brun/J-DriftX/blob/main/site/projet/catalogue-donnees.qmd).
- **Pourquoi cela compte.** En soufflerie, l’écoulement est **connu exactement** (condition aux limites mesurée) : la réponse dispersion est isolée de l’incertitude météorologique ; la gradation couche limite → cube → rangée → canyon épouse la démarche à complexité réduite du projet ; la concentration normalisée K est directement comparable à un modèle adimensionné.
- **Verrous.** Échelle réduite (comme ERIES) ; l’accessibilité libre de CEDVAL est documentée par de nombreux travaux tiers, mais la page du laboratoire précise que **certaines séries exigent la signature d’un accord de données** (action COST ES1006) et que d’autres passent par contact (les gaz lourds d’Hambourg sont déjà consignés comme protégés au catalogue) — à trier série par série au téléchargement.

## 4. Dérive de pulvérisation — deux jeux CC BY 4.0 et un modèle de référence ouvert

- **UAV en vignoble** (Psiroukis 2025, [Zenodo 10.5281/zenodo.15123969](https://zenodo.org/records/15123969)) : essais de dérive suivant le protocole ISO 22866, tartrazine E102 comme traceur, capteurs de 0 à 5 m du dernier rang, août 2024, projet ICAERUS (Horizon Europe). **CC BY 4.0 confirmée** en page d’archive.
- **Pulvérisateur à dos** (van Steenbergen et al., [Zenodo 10.5281/zenodo.18713458](https://zenodo.org/records/18713458), version 2 de mars 2026) : mesures de fluorescence (huit fichiers xlsx), supplément de l’article 10.1093/inteam/vjag033 (Université de Wageningen et Corteva). **CC BY 4.0 confirmée** en page d’archive.
- **DAD-drift v1.0** (Fuchs, Gebler et Lorke) : modèle mécaniste de dérive à l’échelle du champ (modèle de gouttes + modèle micrométéorologique + diffusion gaussienne 3D), publié en code source complet avec documentation, projets d’exemple et exécutable (GitHub et Zenodo, archivé Software Heritage) ; évalué contre des essais de terrain récents (pulvérisation au sol, disques en acier, buses fines à ultra-grosses) ; sorties : courbes de dérive (résolution 1 m) et rasters paysage.
- **Références documentaires.** DRIFTSIM (USDA ARS, distances de dérive de gouttes individuelles, distribution publique via data.gov) ; validation d’AGDISP jusqu’à 400 m (Nsibande et al. 2015, *Chemosphere* 138:454–461) ; essais terrain de technologies de réduction de la dérive (Fritz et al., rapports publics USDA ARS).
- **Constat.** Aucun corpus ouvert ne mesure la **concentration aérienne** de dérive de pulvérisation à l’échelle du champ : les jeux ouverts mesurent des dépôts à très courte distance. Pour l’observable de l’[issue #43](https://github.com/JM-Brun/J-DriftX/issues/43), la voie praticable est donc le **jumeau numérique** (§5, famille S3) avec DAD-drift comme modèle de référence, les deux jeux CC BY 4.0 servant de contrôles d’ordre de grandeur du dépôt.

## 5. Cas synthétiques à vérité connue — la démarche

Principe : un cas synthétique **valide le code et le protocole, jamais la physique réelle** — les données réelles restent le juge final (G3). Règles transverses : générateur versionné dans le dépôt, graines fixées, partitions calibrage/évaluation figées avant toute expérience, et la clause explicite « vérité synthétique, pas une validation physique » dans chaque rapport.

- **S0 — solutions analytiques exactes** (régression du code, exécutables en CI) :
  - S0-a. Panache gaussien en vent uniforme (Briggs), réflexion au sol, préfacteur conservatif : le modèle réduit doit le reproduire **exactement** — test d’identité de la dérivation de similitude.
  - S0-b. Cisaillement en loi de puissance v(z) ∝ z^α : panache penché, solution asymptotique connue — teste en données le lemme de cisaillement de l’[investigation G0-S](19-investigation-g0s-temps-de-parcours.md).
  - S0-c. Superposition de puffs : conservation de la masse et linéarité (propriétés visées, [issue #42](https://github.com/JM-Brun/J-DriftX/issues/42)).
  - S0-d. Régimes de Taylor : croissance de σ(t) ballistique puis diffusive, bornes connues.
- **S1 — vérités bruitées** (protocole de mesure simulé) : champs S0 additionnés d’un bruit de mesure multiplicatif, avec censure sous seuil de détection, réseaux de capteurs épars (arcs à la Prairie Grass) et données manquantes ; métriques FAC2/NMSE par essai ; **baseline = panache gaussien simple** (conformément à l’[issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)). C’est le banc d’essai du protocole G1, sans aucune dépendance de licence.
- **S2 — jumeaux numériques hors famille** :
  - S2-a. Vérité = modèle concurrent connu (par exemple gaussien avec montée de panache) : J-DriftX doit au moins égaler la baseline sur son domaine.
  - S2-b. Vérité = modèle lagrangien stochastique (composantes gouttes/micrométéo de DAD-drift) : quantifie le **coût de la réduction**.
  - S2-c. Vérité figée = soufflerie (CEDVAL, ERIES) : test de structure sur un écoulement exactement connu.
- **S3 — cas d’application dérive** ([issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)) : vérité = DAD-drift sur des scénarios balayés (buses fines à ultra-grosses, vent, humidité, passages uniques ou multiples) ; observables : concentration aérienne et dépôt ; essai indépendant = configuration buse × vent × stabilité. Ce chemin rend l’issue #43 traitable sans attendre un corpus réel de dérive aérienne qui, à ce jour, n’existe pas en accès ouvert.
- **Atouts et limites.** Atouts : zéro dépendance de licence (générateur et vérités S0/S1 propres au projet), régression continue en CI dès le squelette de benchmarks ([issue #17](https://github.com/JM-Brun/J-DriftX/issues/17)), répétabilité totale. Limite majeure : le cas gaussien idéal est **dans la famille** du modèle — il révèle un défaut de code, jamais un défaut de physique ; d’où les vérités hors famille (S2, S3) et le jugement final par les données réelles (Prairie Grass, DIFLU, DATEM/ETEX).

## 6. Recommandations

1. Ajouter **Prairie Grass** et le **Model Validation Kit** en tête de la file de téléchargement manuel, aux côtés de DIFLU : fichiers vraisemblablement petits et textuels, grand nombre d’essais, complémentaires du socle première vague ; vérifier les licences au passage.
2. Implémenter **S0/S1 avec le squelette de benchmarks** (issue #17) — aucune licence n’y fait obstacle ; le protocole G1 (métriques, partitions) peut être figé sur ces bancs avant toute donnée réelle.
3. Ouvrir la voie **S3 (DAD-drift)** pour l’issue #43 : documenter la licence du code, générer les premières vérités de dérive, garder les deux jeux Zenodo CC BY 4.0 comme contrôles d’ordre de grandeur.
4. Mettre à jour la page catalogue du site après fusion des PR en cours (édition concurrente évitée dans cette PR).

## Sources de l’audit (consultées le 23 octobre 2026)

- Harmonisation, archive de traceurs JSI : [harmo.org/jsirwin/Tracer_Data.html](https://www.harmo.org/jsirwin/Tracer_Data.html) et [discussion Prairie Grass](https://www.harmo.org/jsirwin/PrairieGrassDiscussion.html) — format numérique, 68 périodes de 10 min, arcs 50–800 m, micrométéo multi-hauteurs.
- Archive.org, [DTIC AD0152573 — Project Prairie Grass](https://archive.org/details/DTIC_AD0152573) — rapport original (70 lâchers, Nebraska, 1956).
- Harmonisation, [jeux de données classiques](https://www.harmo.org/classic.php) et [Model Validation Kit](https://www.harmo.org/kit.php) — composition (Kincaid, Copenhagen, Lillestrøm, Indianapolis), BOOT, v2.0 (2005), extension 2012 (Kincaid doublé, Bull Run, Round Hill, Prairie Grass).
- Harmonisation, [Key to the Model Validation Kit](https://harmo.isac.cnr.it/Kit/Download/Kit_key.pdf) — éléments du paquet.
- ADMLC, [Datasets](https://admlc.com/datasets/) — mode d’accès des classiques (Kincaid, Prairie Grass, Round Hill, Bull Run, Cabauw, Green Glow/Hanford) ; archive MDA (51 jeux, par contact) ; dépôt JU2003 hors ligne.
- Université de Hambourg, [reference data sets (CEDVAL)](https://www.mi.uni-hamburg.de/en/arbeitsgruppen/windkanallabor/data-sets.html) — description, accord de données COST ES1006 pour certaines séries ; accessibilité libre documentée aussi par des travaux tiers (par exemple *Chinese Journal of Atmospheric Sciences* 2014).
- TU/e, [CODASC — A database for the validation of street canyon dispersion models](https://www.harmo.org/Conferences/Proceedings/_Madrid/publishedSections/H15-142.pdf) et [codasc.de](https://www.codasc.de) — concentrations normalisées de canyon de rue.
- Zenodo, [Spraying UAV Drift measurements in Vineyard](https://zenodo.org/records/15123969) (DOI 10.5281/zenodo.15123969) — ISO 22866, tartrazine E102, CC BY 4.0.
- Zenodo, [Off-target spray drift deposition assessment from a knapsack application](https://zenodo.org/records/18713458) (DOI 10.5281/zenodo.18713458 ; DOI toutes versions 10.5281/zenodo.18713457) — supplément de 10.1093/inteam/vjag033, CC BY 4.0.
- Zenodo, [DAD-drift v1.0](https://zenodo.org/records/18174928) et [GitHub Mike-Fuchs/DAD-drift](https://github.com/Mike-Fuchs/DAD-drift) — code source complet, documentation, exemples, exécutable, archivage Software Heritage.
- Fuchs, Gebler et Lorke, [The droplet and atmospheric dispersion drift (DAD-drift) model](https://www.sciencedirect.com/science/article/pii/S001393512500355X), *Environmental Research* — évaluation contre essais de terrain postérieurs à 2015 (disques en acier), sorties courbes de dérive et rasters.
- Data.gov, [DRIFTSIM](https://catalog.data.gov/dataset/driftsim-4b348) — distances de dérive de gouttes individuelles, USDA ARS.
- Nsibande et al. 2015, [Validation of the AGDISP model for predicting airborne atrazine spray drift](https://www.sciencedirect.com/science/article/abs/pii/S0045653515007122), *Chemosphere* 138:454–461 ; Fritz, Hoffmann, Bagley et Wolfenbarger, [rapport public USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30910515/Publications/2011/Fritz%20Field%20DRT.pdf) — validations AGDISP et essais terrain DRT.
