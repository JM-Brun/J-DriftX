# Catalogue de données ouvertes pour tester J-DriftX

> **État au 22 octobre 2026.** Pré-sélection documentaire de sources publiques. Ce catalogue n'est ni une revue systématique ni un audit des fichiers bruts. Les liens, licences, schémas, variables, unités et identifiants d'essais doivent être vérifiés avant tout usage scientifique. « Public » ne signifie pas toujours téléchargement immédiat ou réutilisation sans condition.

## Synthèse et priorité

| Priorité | Jeu / ressource | Domaine et échelle | Observations disponibles | Intérêt pour J-DriftX | Limite principale |
|---|---|---|---|---|---|
| **A1** | [NOAA DATEM](https://www.arl.noaa.gov/research/atmospheric-transport-and-dispersion/atd-programs-datem/) | Dispersion atmosphérique longue distance, dizaines à milliers de km | Expériences de traceurs, concentrations, métadonnées expérimentales et météorologie; inclut notamment CAPTEX. ETEX est documenté séparément par le JRC et n'est pas inclus dans l'archive DATEM selon la documentation NOAA | Candidat prioritaire si l'hypothèse reste le transport atmosphérique de traceur passif / far-field. Données et outils d'évaluation sont explicitement proposés au téléchargement | Campagnes anciennes; vérifier chaque expérience, unité, source, données météo et indépendance. Un traceur gazeux ne valide pas automatiquement les aérosols ou gouttelettes |
| **A1** | [ETEX — JRC](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm) et [ENSEMBLE long-range](https://joint-research-centre.ec.europa.eu/scientific-tools-and-databases-0/ensemble-atmospheric-chemistry-transport-and-dispersion-models/ensemble-case-studies/ensemble-long-range-atmospheric-dispersion_en) | Dispersion atmosphérique continentale, plus de 2 000 km dans les exercices associés | Données de rejet de traceur, prélèvements et météorologie pour deux expériences; exercices de dispersion à longue distance | Candidat de validation indépendant pour le transport à grande échelle, selon la variable effectivement mesurée et le scénario | Modèle de transport simplifié peut ne pas représenter la chimie, la déposition ou les sources réelles; vérifier l'accès exact et la documentation |
| **A1** | [DIFLU — traceur hélium à Beuvry](https://doi.org/10.57745/A9YC3C) | Dispersion atmosphérique proche d'une installation, jusqu'à environ 560 m | 19 lâchers contrôlés d'hélium, mesures de concentration, météorologie et micrométéorologie, anémomètres, lidar Doppler | Jeu expérimental particulièrement intéressant pour tester transport atmosphérique local, vent/turbulence et effet d'un site bâti | Le traceur est un gaz; les fichiers font environ 381 MB et doivent être audités. Le régime proche n'est pas le far-field |
| **A1** | [ERIES — dispersion urbaine en soufflerie](https://doi.org/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf) | Dispersion urbaine à l'échelle de quartier, maquette de Sofia | Concentrations de traceur éthylène en 76 points pour deux sources, avec essais de répétabilité et incertitude | Données contrôlées pour tester la réponse spatiale à la géométrie urbaine et comparer une approximation de dispersion | Soufflerie et similitude à l'échelle réduite; deux configurations de source ne sont pas deux grandes populations indépendantes |
| **A2** | [MODISAFE WP32 — Surrey](https://doi.org/10.15126/surreydata.901739) | Dispersion en zone urbaine, sources plus lourdes ou plus légères que l'air | Mesures synchronisées de vitesse et de concentration en soufflerie autour d'une maquette d'Oslo | Utile pour éprouver les limites d'un modèle de scalaire passif : les rejets non neutres rendent explicite l'écart de régime physique | Vérifier les fichiers et la licence du dépôt; un modèle passif ne devrait pas être jugé sur un cas buoyant sans adaptation physique |
| **A2** | [R-LINE — modèle et jeux d'évaluation](https://cmascenter.org/r-line/) | Émissions routières, dispersion près du sol | Paquet public comprenant code, cas de test et jeux d'évaluation; documente études traceur Idaho Falls et Caltrans Highway 99 et étude routière Raleigh | Bon candidat si le cas d'usage s'oriente vers la pollution automobile et les sources linéaires | Les données historiques ne sont pas nécessairement toutes dans le paquet; vérifier la provenance et l'autorisation des données d'évaluation |
| **A2** | [EPA — dispersion au bord des barrières routières](https://catalog.data.gov/dataset/data-for-dispersion-at-the-edges-of-near-road-barriers) | Pollution routière, soufflerie | Distributions normalisées de concentration d'un traceur hydrocarboné pour plusieurs configurations de barrières anti-bruit | Données relativement ciblées pour tester l'effet d'obstacles et de géométrie sur une concentration | Étude à échelle réduite; concentration normalisée et scénarios de soufflerie, pas exposition réelle directement |
| **B — analogie de méthode** | [TIERRAS — plus de 400 essais de traceur en rivières](https://doi.org/10.5281/zenodo.15794259) | Transport de solutés en rivières et cours d'eau | Base compilée d'expériences d'injection de traceurs; version Zenodo annoncée CC BY-NC 4.0 | Utile pour comparer des idées mathématiques de transport, temps de séjour, stockage transitoire et validation groupée | **Pas une validation de dispersion atmosphérique** : dynamique, frontières, advection et échange avec les sédiments diffèrent. Licence non commerciale |
| **B — analogie de trajectoire** | [Cefas — Historical Seabed Drifters 1969–1990](https://doi.org/10.14466/CefasDataHub.93) | Transport marin côtier / fond marin | 11 704 entrées de déploiement et retours de flotteurs; licence Open Government Licence | Pourrait tester des méthodes de trajectoire et l'incertitude de transport marin | Données de trajectoire et de récupération, pas mesures de concentration de polluant; biais de retour important (41 % environ) |
| **B — analogie de trajectoire** | [NOAA Global Drifter Program](https://www.aoml.noaa.gov/global-drifter-program/) | Courants de surface océaniques | Trajectoires de bouées dérivantes et jeux dérivés | Potentiellement utile pour comparer une formulation de trajectoire dans un champ de vitesse | Ne mesure pas directement le transport d'un contaminant; la dynamique océanique n'est pas celle de l'atmosphère |
| **C — surveillance, pas validation de panache** | [OpenRadiation](https://www.data.gouv.fr/datasets/openradiation) | Radioactivité ambiante, mesures citoyennes géolocalisées | Débit de dose, date, GPS et métadonnées variables; CSV/API; ODbL | Peut documenter des observations environnementales et leur qualité | Attribution à une source, terme source, météo et historique d'exposition généralement insuffisants pour valider un modèle de dispersion |
| **C — métadonnées d'accident** | [RADARC311 — métadonnées Fukushima](https://radarc311.isee.nagoya-u.ac.jp/en/) | Mesures de radioactivité liées à Fukushima | Catalogue de métadonnées sur des observations, méthodes, lieux et dates; certaines données seulement publiques | Point d'entrée pour repérer des mesures historiques exploitables | C'est un méta-catalogue, pas un jeu homogène prêt à l'emploi; accès aux données sources variable |
| **C — accès à confirmer** | [Hamburg EWTL — données de dispersion de gaz lourds](https://www.mi.uni-hamburg.de/en/arbeitsgruppen/windkanallabor/data-sets.html) | Rejets industriels de gaz lourds, parc chimique et obstacles | Mesures de champ d'écoulement, densité et dispersion en soufflerie | Très pertinent si J-DriftX vise des rejets industriels denses | Téléchargements protégés par mot de passe et accès sur demande : **publicement décrit, mais pas immédiatement ouvert** |

Les niveaux A/B/C indiquent la priorité pour une investigation de données, pas une note de qualité scientifique absolue.

## Ce que ce catalogue change pour le choix de J-DriftX

La recherche ne devrait pas être structurée par le seul type de pollution (« nucléaire », « automobile », « marine »), mais par les **équations et observables** :

1. **Transport atmosphérique de traceur passif** : DATEM/ETEX, puis DIFLU et ERIES selon l'échelle.
2. **Sources routières et géométrie urbaine** : R-LINE et données EPA de barrières.
3. **Rejets industriels denses ou buoyants** : MODISAFE et EWTL, seulement si le modèle inclut les effets de densité/flottabilité pertinents.
4. **Trajectoires marines ou transport hydrologique** : Cefas, NOAA GDP et TIERRAS sont des analogies méthodologiques, pas des validations directes de la physique atmosphérique.
5. **Accidents radiologiques** : OpenRadiation et RADARC311 sont des portes d'entrée de surveillance / métadonnées; ils ne remplacent pas des observations de traceur avec terme source et météo connus.

Une réutilisation inter-domaines peut tester la robustesse d'un algorithme mathématique, une méthode de calcul ou une stratégie d'incertitude. Elle ne prouve pas que les paramètres ou lois physiques se transfèrent entre air, eau et océan.

## Recommandation concrète

Ne pas lancer tout de suite un benchmark multi-domaines. Faire un **audit de faisabilité sans modèle** sur trois candidats, dans cet ordre :

1. **DATEM/ETEX** : meilleure correspondance avec la question du far-field atmosphérique et des traceurs.
2. **DIFLU** : données contrôlées de terrain avec météorologie et concentrations jusqu'à quelques centaines de mètres.
3. **ERIES ou EPA near-road barriers** : données contrôlées pour tester les effets de géométrie; choisir selon que l'on privilégie un panache urbain ponctuel ou une source routière.

Pour chacun, relever : accès et licence, version et sommes de contrôle des fichiers, terme source, coordonnées et temps, météorologie, observable/unité, limite de détection, données manquantes, nombre d'expériences réellement indépendantes, variables de groupement, et séparation historique entre calibration et évaluation. Conserver un jeu final indépendant des décisions de conception.

**Critère d'arrêt :** si les fichiers bruts ne contiennent pas assez d'informations pour reconstruire le scénario, si l'observable ne correspond pas aux équations du modèle, ou si les expériences ne peuvent pas être séparées de façon indépendante, classer le jeu comme référence bibliographique seulement — ne pas l'utiliser comme benchmark.

## Sources documentaires complémentaires

- [ADMLC — catalogue de jeux de données de dispersion](https://admlc.com/datasets/) : index utile de jeux de données atmosphériques et de conditions d'accès.
- [HARMO — jeux classiques pour l'évaluation de modèles](https://harmo.org/classic.php) : Kincaid, Bull Run, Round Hill, Prairie Grass et autres campagnes classiques.
- [NOAA DATEM — archives et outils d'évaluation](https://www.arl.noaa.gov/research/atmospheric-transport-and-dispersion/atd-programs-datem/).
- [JRC — ETEX](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm).
- [EPA — R-LINE](https://cmascenter.org/r-line/) et [données de barrières routières](https://catalog.data.gov/dataset/data-for-dispersion-at-the-edges-of-near-road-barriers).
- [TIERRAS — dépôt Zenodo](https://doi.org/10.5281/zenodo.15794259).
- [Cefas — données de flotteurs](https://doi.org/10.14466/CefasDataHub.93).
- [NOAA Global Drifter Program](https://www.aoml.noaa.gov/global-drifter-program/).
- [OpenRadiation — data.gouv.fr](https://www.data.gouv.fr/datasets/openradiation).
- [RADARC311](https://radarc311.isee.nagoya-u.ac.jp/en/).
