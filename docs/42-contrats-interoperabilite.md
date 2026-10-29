# Contrats d'interopérabilité : protocoles PEP 544 entre relief, vent, sources et concentrations

> **Statut — modularisation demandée le 29 octobre 2026 : si un élément change (terrain/relief, sources/puits, champ de vent 2D/3D, concentrations), les interfaçages doivent continuer de se faire simplement, en s'appuyant sur les standards autant que possible (MNT, …).** Ce document et son exécution répondent à ce mandat : trois contrats (relief, vent, concentration) et leurs adaptateurs sont extraits dans un module isolé ([contrats.py](../src/jdriftx/contrats.py)) ; les éléments existants ([champ_analytique.py](../src/jdriftx/champ_analytique.py), [terrain.py](../src/jdriftx/terrain.py), [source.py](../src/jdriftx/source.py), [similitude.py](../src/jdriftx/similitude.py)) sont branchés derrière ces contrats sans modification. Aucune définition mathématique, aucun seuil ([#43](https://github.com/JM-Brun/J-DriftX/issues/43)), aucune vérité exacte n'est modifié.

## 1. Question et modes de contribution

- **Question** : comment permettre de changer un élément du modèle (relief, champ de vent plan ou tridimensionnel, modèle de concentration, sources simples ou superposées) sans réécrire les sites d'appel des autres éléments ?
- **Modes de contribution** : 3 (interface de domaine), 4 (tests) et 6 (documentation).

## 2. Le problème d'accouplement

| Élément | Avant | Après |
|---|---|---|
| Relief | `terrain_surface(x, y, kind, …)` : une fonction à sept paramètres, les cas plats et les MNT n'ont pas de surface commune | Contrat `Relief.altitude(x, y)` : implementations plat, synthétique (délégation pure) et MNT `.asc` interchangeable |
| Vent | `ChampPlan` (2D, ponctuel) d'un côté, `fields.vector_field` (2D, grille) de l'autre : pas de contrat pour un vent 3D | Contrat `Vent.vitesse(x, y, z) -> (u, v, w)` : uniforme 2D, adaptation d'un champ plan (w = 0), profil en loi de puissance (1D + z) |
| Sources | `SourcePanache` unifié (docs/41) mais consommé champ par champ dans les appels à la similitude | `PanacheGaussien(source)` : la source est composée ; `SuperpositionPanaches` combine tout objet satisfaisant le contrat |
| Concentrations | `concentration_panache(x, y, z, debit, u, classe, hauteur)` : sept paramètres répétés à chaque appel | Contrat `ModeleConcentration.concentration(x, y, z)` : le modèle porte ses paramètres, l'appelant ne les connaît plus |

Les contrats sont des protocoles PEP 544 à typage structurel — le même mécanisme que `ChampPlan` ([champ_analytique.py](../src/jdriftx/champ_analytique.py)) : toute classe exposant la méthode du contrat le satisfait, sans héritage ni inscription.

## 3. Les trois contrats

| Contrat | Signature | Implémentations livrées | Rôle |
|---|---|---|---|
| `Relief` | `altitude(x, y)` (vectorisé, grilles) | `ReliefPlat`, `ReliefSynthetique`, `ReliefMntAscii` | Géométrie du sol pour le rendu, la planification de prélèvements et les futurs cas de terrain |
| `Vent` | `vitesse(x, y, z) -> (u, v, w)` (ponctuel, comme l'intégration des trajectoires) | `VentUniforme`, `VentDeChampPlan`, `VentProfilPuissance` | Champ de vent plan ou 3D, interchangeable derrière une seule signature |
| `ModeleConcentration` | `concentration(x, y, z)` (vectorisé) | `PanacheGaussien`, `SuperpositionPanaches` | Modèle de concentration interchangeable (similitude aujourd'hui, solveurs demain) |

Le choix vectorisé/ponctuel suit l'usage réel : le relief et les concentrations s'évaluent sur des grilles (rendu, jeux de mesures), le vent s'échantillonne point par point (intégration des trajectoires, [trajectories.py](../src/jdriftx/trajectories.py)).

## 4. Standards retenus

- **MNT : ESRI ASCII Grid (`.asc`)** — format d'échange lisible par QGIS et GDAL, exporté par les altimétries nationales, analysable sans dépendance au-delà de numpy. `ReliefMntAscii.depuis_texte` lit l'en-tête standard (`ncols`, `nrows`, `xllcorner`, `yllcorner`, `cellsize`, `nodata_value` optionnel), les centres de cellules suivent la convention du format (ligne 0 au nord, `x0`/`y0` au centre de la cellule sud-ouest), l'interpolation est bilinéaire, l'emprise et les cellules sans données sont refusées explicitement. GeoTIFF et CF-NetCDF restent des candidats post-G1, conformément à la décision de [docs/39](39-squelette-benchmarks-s0.md), section 7 : ils exigent des dépendances de lecture que le paquet n'embarque pas encore.
- **Profil de vent : loi de puissance** — `VentProfilPuissance` implémente u(z) = u_réf · (z/z_réf)^exposant, le profil de couche de surface utilisé par les modèles de dispersion opérationnels ; l'exposant est contraint à [0, 1], z strictement positif.
- **Contrats : PEP 544** — protocoles à typage structurel, déjà la règle du package pour `ChampPlan` (docs/25, docs/40) ; `@runtime_checkable` permet aux tests de vérifier la conformité.

## 5. Registre du graphe

Le module `contrats.py` rejoint le registre ([site/data/graphe-connaissances.toml](../site/data/graphe-connaissances.toml)) — nœud module `contrats` et quatre arêtes structurelles « utilise » : `contrats` → `terrain`, `contrats` → `champ_analytique`, `contrats` → `source`, `contrats` → `similitude`. Le nœud rejoint la vue « Code, propriétés et preuves », groupe dédié « Contrats d'interface » ; le rendu ([site/projet/_graphes-mermaid.md](../site/projet/_graphes-mermaid.md)) est régénéré et committé avec le registre, la synchronisation octet par octet restant vérifiée par la CI.

## 6. Limites

Le relief du contrat est une **géométrie** (altitude du sol) : aucun effet du relief sur l'écoulement (déflexion, couche limite interne) n'est inféré. Les **puits** (dépôt au sol, sédimentation) ne sont pas modélisés avant la porte G1 : `SuperpositionPanaches` superpose des sources, pas des puits. Le vent du contrat est **stationnaire** (pas de temps dans la signature) : un contrat `Vent` dépendant du temps reste un candidat, à aligner sur `trajectories.Velocity` si les trajectoires l'adoptent. Enfin, `VentProfilPuissance` est un profil de surface, pas un champ 3D complet : il satisfait le contrat pour ce que sa physique affirme, rien de plus.

## 7. Périmètre et suivi

| Élément | Statut |
|---|---|
| Contrats `Relief`, `Vent`, `ModeleConcentration` (PEP 544) | **Livrés** ([contrats.py](../src/jdriftx/contrats.py)) |
| Adaptateurs des éléments existants (terrain, champ plan, source, similitude) | **Livrés**, délégation pure sans duplication |
| MNT standard ESRI ASCII Grid (`.asc`) | **Lu et interpolé** (bilinéaire, emprise et nodata explicites) |
| Profil de vent en loi de puissance | **Livré** (standard de couche de surface) |
| Superposition de sources derrière le contrat (H8) | **Livré** (`SuperpositionPanaches`) |
| Puits / dépôt, vent non stationnaire, GeoTIFF/CF-NetCDF | **Candidats documentés**, non exécutés (limites, section 6) |
| Vérités exactes, manifestes, seuils [#43](https://github.com/JM-Brun/J-DriftX/issues/43) | **Inchangés** |

## Références

- Exécution : [contrats.py](../src/jdriftx/contrats.py) ; tests : [test_contrats.py](../tests/test_contrats.py).
- Contexte interne : docs/24 (objets de stabilité), docs/25 (harmonisation OOP), docs/39 section 7 (standards de données), docs/40 (standards de qualité, PEP 544), docs/41 (unification de la source) ; contrats inchangés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
