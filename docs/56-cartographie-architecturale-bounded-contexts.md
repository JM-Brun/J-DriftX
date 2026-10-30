# 56 — Cartographie architecturale et bounded contexts (chantier #303, P1)

## Statut

Note d'architecture portant la tranche P1 du [chantier qualité #303](https://github.com/JM-Brun/J-DriftX/issues/303) : cartographie des dépendances, définition des contextes délimités (bounded contexts) et des règles de dépendances autorisées. **État des lieux initial de `main` au commit `8869419` ; actualisations successives du suivi au 30 octobre 2026. Aucune migration ni réduction d'API n'est appliquée dans cette note** : les arbitrages de migration restent au propriétaire. Cette note ne change aucune équation, tolérance, contrat d'exécution ni test.

## Actualisation du suivi — 30 octobre 2026

Cette actualisation complète l'état des lieux initial sans modifier les décisions de migration :

- **PR #311** : stabilité des évaluations gaussiennes panache/puff, associée à l'issue #307 ; fusionnée, CI complète verte (672 tests, 95 % de couverture).
- **PR #313** : représentabilité des temps et coûts de transport dans `metric.py` ; fusionnée, CI complète verte (669 tests, 95 %).
- **PR #314** : réduction des phases et calcul robuste des composantes du champ analytique ; fusionnée, CI complète verte (666 tests, 95 %).
- **PR #315** : actualisation de cette cartographie et inventaire des usages de l'API racine ; fusionnée.
- **PR #316** : garde-fous AST sur les frontières architecturales, les dépendances de rendu et les cycles d'import ; fusionnée, CI complète verte (683 tests, 95 %).
- **PR #318** : immutabilité des tableaux détenus par `DatasetS0`, `GrilleEdp`, `TrancheEdp` et `SolutionEdp`, ainsi que contrôles des paramètres finis ; fusionnée, CI complète verte (691 tests, 95 %).

Les CI établissent des garanties logicielles dans leur périmètre, pas une validation physique. Le cas extrême d'interpolation bilinéaire du MNT est désormais couvert par une interpolation linéaire stable et des tests de régression ciblés (voir §4).

L'inventaire interne de l'API racine a été réalisé (§6.1). Il ne permet pas de conclure sur d'éventuels consommateurs externes ; aucune réduction d'API n'est proposée.

## 1. Méthode et sources

Trois sources factuelles, aucune inférence au-delà :

- les arêtes `utilise` / `implemente-par` / `couvre` du [registre du graphe de connaissances](https://github.com/JM-Brun/J-DriftX/blob/main/site/data/graphe-connaissances.toml), source de vérité déjà vérifiée par la CI (chaque module de `src/jdriftx` y a un nœud) ;
- les imports réels des modules (les arêtes structurelles du registre les reflètent) ;
- l'inventaire des exports de `src/jdriftx/__init__.py` et les tailles de fichiers de `main` (annexe A).

## 2. Contextes délimités

| Context | Modules | Rôle | Dépend (constaté sur main) |
|---|---|---|---|
| **C1. Noyau scientifique** | `metric`, `similitude`, `similitude_objets`, `stabilite`, `source`, `champ_analytique`, `constraints` | formulations et évaluations numériques, numpy uniquement | interne au noyau uniquement (`similitude` → `stabilite`, `source` → `stabilite`, `similitude_objets` → `similitude`) |
| **C2. Contrats et implémentations interopérables** ([docs/42](42-contrats-interoperabilite.md)) | `_protocoles`, `reliefs`, `vents`, `concentrations`, `contrats` (façade) | protocoles PEP 544 et implémentations de référence | C1, `_protocoles` (`reliefs` → `terrain` qui est un module d'enseignement) |
| **C3. Solveurs et modules d'enseignement** | `periodic_transport`, `advection_diffusion`, `trajectories`, `fields`, `terrain` | vérification pédagogique et contre-références, non exportés à la racine ([docs/25](25-audit-harmonisation-oop-2026.md), recommandation 7) | autonomes (aucune arête `utilise` vers le reste du package) |
| **C4. Expériences et reconstructions** | `experiences/*` (dont le package `transitoire_puff/`) | tranches verticales typées, manifestes étiquetés, jamais dans l'API racine | C1, C2, C5 |
| **C5. Benchmarks de référence** ([docs/39](39-squelette-benchmarks-s0.md)) | `benchmarks/cas`, `benchmarks/metriques`, `benchmarks/reference` | cas synthétiques enregistrés, métriques FAC2/NMSE, pipeline d'évaluation | C1 (`cas` → `similitude`, `source`) |
| **C6. Figures et rendu** | `figures/figure_01` … `figure_06`, `figures/wind_field_explorer` | générateurs SVG et explorateur, consomment des tranches typées | C4 (chaque figure → son expérience), `wind_field_explorer` → `fields` (C3) |
| **C7. Outillage de traçabilité documentaire** | `graphe_connaissances`, `extraction_graphe`, `diagnostic_graphe` | rendu du registre TOML, inventaire, diagnostic ; aucun calcul scientifique | autonomes (aucune arête vers C1–C6) |
| **C8. Applications, site et scripts** (hors package) | `apps/`, `site/`, `scripts/` | applications interactives, publication, contrôle | imports explicites de sous-modules C1/C3/C4/C5 selon le cas ; l'API racine n'est pas l'unique frontière utilisée |

## 3. Règles de dépendances proposées

Constat préalable : **sur `main`, aucune inversion ni cycle n'existe** — les arêtes du registre vont des contextes aval vers l'amont, et chaque figure ne consomme que son expérience. Depuis la PR #316, les frontières décrites ici sont protégées par `tests/test_architecture_boundaries.py` : classification des modules, matrice d'imports, exception C2 → C3 et absence de cycles statiques. Le contrôle est volontairement limité aux imports statiques.

| Depuis ↓ vers → | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|---|---|---|---|---|---|---|
| C1 Noyau | interne | **interdit** | **interdit** | **interdit** | **interdit** | **interdit** | **interdit** |
| C2 Contrats | autorisé | interne | autorisé* | **interdit** | **interdit** | **interdit** | **interdit** |
| C3 Enseignement | — | — | interne | **interdit** | **interdit** | **interdit** | **interdit** |
| C4 Expériences | autorisé | autorisé | autorisé | interne | autorisé | **interdit** | **interdit** |
| C5 Benchmarks | autorisé | — | — | **interdit** | interne | **interdit** | **interdit** |
| C6 Figures | autorisé | — | autorisé | autorisé | — | interne | **interdit** |
| C7 Outillage | — | — | — | — | — | — | interne |

\* L'arête `reliefs` → `terrain` (C2 → C3) est l'unique franchissement actuel : `ReliefSynthetique` délègue au module d'enseignement `terrain_surface`. Deux options pour le propriétaire : l'accepter comme exception documentée, ou faire de `terrain_surface` une fonction du noyau (déplacement à équivalence byte-exact, PR dédiée).

Interdits transverses : cycle quelconque ; import de rendu (matplotlib/plotly/streamlit) dans C1–C5 (déjà respecté : les dépendances de rendu vivent dans `apps/` et `site/`, [docs/22](22-audit-package-code.md)) ; `dict`/JSON au-delà des frontières d'export (charte qualité, [CONTRIBUTING](https://github.com/JM-Brun/J-DriftX/blob/main/CONTRIBUTING.md)).

## 4. État de P0 — frontières NumPy

Le P0 a déjà produit plusieurs tranches fusionnées. Les corrections numériques #311/#313/#314 sont maintenant intégrées ; l'audit des objets portant des tableaux est intégré par #318 (fusionnée, CI verte). Les cas ciblés de l'interpolation bilinéaire MNT sont également traités sur `main` et couverts par des tests de régression. L'audit P0 reste ouvert pour les frontières d'entrée et exceptions qui n'ont pas encore été examinées.

- **#302** : immutabilité réelle (bytes-backed `np.frombuffer`) et sentinelle `nodata` finie de `ReliefMntAscii`, coordonnées d'interpolation validées ;
- **#304** : audit `source` (déjà conforme), gardes `similitude` (scalaires et grilles finis, débordement `u·t`, distance sous le vent), `metric` (débordement `b − a`, somme des coûts), `terrain` (coordonnées finies) ;
- **#305** : normalisation avant mise au carré dans `terrain_surface` (sous-débordement `width²`) ;
- **#306** : somme `SuperpositionPanaches`, en-tête MNT (`ncols`/`nrows`) finis, profil de vent en loi de puissance, champ plan adapté ;
- **#308** : nombre d'onde, coordonnées, vitesse et superposition de `champ_analytique` ;
- **#309** : échelles extrêmes gaussiennes (exposants normalisés, chemin de secours logarithmique, exception documentée) ; les trois cas de l'[issue #307](https://github.com/JM-Brun/J-DriftX/issues/307) sont couverts par les tests ;
- **#311 (fusionnée)** : extension de la robustesse des lois de Briggs et des concentrations panache/puff aux échelles extrêmes ; CI verte, 672 tests, couverture 95 % ;
- **#313 (fusionnée)** : représentabilité des métriques et temps de transport, y compris les intermédiaires de norme et de produit scalaire ; CI verte, 669 tests, couverture 95 % ;
- **#314 (fusionnée)** : réduction des phases périodiques et calcul représentable des composantes du champ analytique ; CI verte, 666 tests, couverture 95 % ;
- **#318 (fusionnée)** : copie défensive et immutabilité profonde des tableaux de `DatasetS0`, `GrilleEdp`, `TrancheEdp` et `SolutionEdp`, validation des formes et paramètres finis ; CI verte, 691 tests, couverture 95 %.

Les corrections #311/#313/#314 sont intégrées et testées ; elles ne valident pas physiquement les modèles.

**Revue complémentaire de la frontière de similitude après #335** :

- Un cas résiduel est identifié : NumPy promeut une séquence hétérogène telle que `[1.0, True]` en tableau entier avant que le contrôle du `dtype` puisse détecter le booléen. La validation des tableaux doit donc inspecter les éléments avant de retenir le type numérique promu. Une régression ciblée est ajoutée pour les deux fonctions sigma et les deux fonctions de concentration.
- `_distance_sous_le_vent` ne faisait que répéter le contrôle de finitude déjà effectué par `_tableau_reel_fini` ; le wrapper est supprimé, sans changement de domaine ni de résultat attendu.
- Les helpers `_reel_fini` présents dans `similitude`, `source`, `reliefs` et `vents` ne sont pas factorisés à ce stade. Ils se trouvent à des frontières de contextes distincts (C1/C2) et portent des messages contextuels ; créer un module commun ajouterait une dépendance transversale sans bénéfice contractuel démontré. Une future factorisation devra être motivée par un contrat partagé explicite.
- Les annotations scalaires publiques en `float` décrivent le type normalisé attendu en sortie et la convention de l'API ; elles ne prétendent pas exclure les autres `numbers.Real` acceptés à l'exécution. Les paramètres de coordonnées restent annotés `ArrayLike`. Les erreurs de validation restent des `ValueError` contextualisées ; les erreurs de représentabilité des calculs internes conservent leurs exceptions documentées.
- Ces tests établissent le rejet logiciel de certaines entrées ambiguës ; ils ne démontrent aucune propriété physique.

**Interpolation bilinéaire MNT — correction présente sur `main`** : `ReliefMntAscii.altitude` délègue chaque interpolation linéaire à `_interpole_lineairement_stable`, qui utilise `a + t·(b − a)` pour deux valeurs de même signe et la forme pondérée pour des signes opposés. Cette sélection évite de faire dépendre le résultat retenu d'une expression intermédiaire susceptible de déborder. Les tests `test_mnt_ascii_interpolation_preserves_the_finite_convex_bound`, `test_mnt_ascii_interpolation_preserves_a_tiny_active_corner`, `test_mnt_ascii_interpolation_preserves_tiny_corner_at_grid_node` et `test_mnt_ascii_interpolation_handles_opposite_sign_extremes` couvrent les cas extrêmes correspondants. Il s'agit de garanties numériques ciblées sur l'interpolation, pas d'une validation topographique générale.

### Complément P0 — cohérence des scalaires booléens (#343)

Une revue complémentaire a identifié des frontières d'objets où `math.isfinite` ou
`np.isfinite` étaient utilisés seuls. Ces fonctions considèrent les booléens comme
des valeurs numériques finies ; elles ne suffisent donc pas à garantir qu'une
coordonnée ou un paramètre déclaré numérique est réellement un scalaire réel.

La tranche dédiée couvre :

- C1 : `similitude_objets.Point3D` et `ParametresPuff` ;
- C4 : `CasSynthetiqueS0` et les tableaux détenus par `DatasetS0`, avant conversion
  en `float64` ;
- C5 : `PointMesure` et `CasS0`.

Les booléens Python et NumPy sont rejetés explicitement. Les champs entiers
`graine` et `nombre_points` de `CasSynthetiqueS0` sont également vérifiés à la
construction afin d'éviter une erreur différée au moment de la génération.
Aucune équation, unité, convention de génération, tolérance ou hypothèse physique
n'est modifiée. La validation de `SourcePanache` reste la référence déjà en place
pour les scalaires physiques.

## 5. Séparation de `contrats.py` — soldée par #302

L'item P1 « séparer progressivement `contrats.py` » est **déjà effectif** sur `main` : `contrats.py` est une façade de 26 lignes ré-exportant 11 noms ; les protocoles vivent dans `_protocoles.py` ; les implémentations dans `reliefs.py`, `vents.py`, `concentrations.py` ; les chemins d'import historiques sont conservés et couverts par un test d'identité. Rien à refaire ; les futures implémentations de contrat vont dans leur module dédié, la façade n'ajoute que des ré-exports.

## 6. Inventaire de `__init__.py` et recommandation

`src/jdriftx/__init__.py` exporte 40 symboles (+ `__version__`), répartis en trois familles :

- **contrats C2 (11)** : `ModeleConcentration`, `Relief`, `Vent`, `ReliefMntAscii`, `ReliefPlat`, `ReliefSynthetique`, `VentDeChampPlan`, `VentProfilPuissance`, `VentUniforme`, `PanacheGaussien`, `SuperpositionPanaches` ;
- **expériences C4 (10)** : `ChampUniforme`, `ManifesteReconstruction`, `ManifesteScenario`, `Rectangle`, `ResultatDirige`, `ResultatReconstruction`, `ScenarioReconstruction`, `ScenarioUniforme`, `construire_manifeste`, `resoudre_scenario` ;
- **noyau C1 (19)** : champ_analytique (3 : `ChampFonctionCourant`, `ChampPlan`, `SuperpositionChamps`), constraints (3 : `linearite`, `linearite_panache`, `positivite`), metric (2), similitude (4), similitude_objets (4), source (1), stabilite (2).

Les modules d'enseignement C3 (`trajectories`, `fields`, `terrain`, `periodic_transport`, `advection_diffusion`) ne sont pas exportés à la racine : exclusion déjà décidée ([docs/25](25-audit-harmonisation-oop-2026.md), recommandation 7) et rappelée dans le docstring du module.

**Inventaire interne effectué — décision : ne pas réduire la surface maintenant.** La recherche des imports Python du dépôt montre que les sources, applications et scripts importent les sous-modules explicitement ; l'unique occurrence de `from jdriftx import` trouvée dans les tests importe les sous-modules `concentrations`, `contrats`, `reliefs` et `vents`, pas les 40 symboles ré-exportés. Les tests d'architecture vérifient déjà l'identité de plusieurs ré-exports historiques.

### 6.1 Résultat et limite de l'inventaire d'usage

- Aucun usage direct des symboles ré-exportés à la racine n'a été trouvé dans les imports des sources, applications et scripts inspectés ; ces consommateurs utilisent explicitement les sous-modules.
- Exemples constatés : `apps/convergence_lab.py` importe `periodic_transport` ; `apps/interactive_lab.py` importe `fields` et `terrain` ; `apps/scientific_validation.py` importe `advection_diffusion` et `trajectories` ; `scripts/benchmark_baseline_uniforme.py` importe `benchmarks.cas`, `experiences.baseline_uniforme` et `source`.
- Les modules C3 utilisés par les applications ne sont volontairement pas ré-exportés à la racine. Les déplacer ou les supprimer casserait donc des consommateurs internes même en l'absence d'import racine.
- Le dépôt vérifie des ré-exports de compatibilité ciblés, mais ne fournit pas d'inventaire des notebooks personnels, scripts hors dépôt, installations publiées ou consommateurs externes.
- L'absence d'usage interne n'est pas une preuve d'absence d'usage public. Les exports du noyau, des contrats et des expériences restent donc inchangés.
- Toute réduction ultérieure devra être une décision explicite de versionnement/API, accompagnée d'une période de dépréciation si le package devient consommé hors du dépôt.

Conclusion : l'inventaire interne est terminé ; la réduction de l'API racine est **différée**, sans suppression ni renommage.

## 7. Outillage de graphe — évaluation, pas migration

`graphe_connaissances`, `extraction_graphe` et `diagnostic_graphe` (contexte C7) ne participent à aucun calcul scientifique, n'importent rien de C1–C6, et sont auto-testés. #303 demande d'« évaluer le déplacement » : **le statu quo est recommandé** — le déplacement hors package (par ex. `tools/`) n'apporterait qu'une étiquette, coûterait une migration d'imports (CI, `python -m jdriftx.diagnostic_graphe`, tests de synchronisation) et affaiblirait la règle « chaque module a un nœud ». À rouvrir seulement si le package est un jour publié sur PyPI avec un périmètre strictement scientifique.

## 8. Suites (P0 résiduel, P2/P3 de #303)

### Complément P0 — frontières des champs et géométries (issue #345, PR #346)

La recherche des usages de `math.isfinite` a révélé un autre cas de coercition
implicite : les booléens Python et NumPy sont des valeurs finies pour ces
fonctions. Le correctif ciblé couvre :

- C1 : paramètres et coordonnées de `ChampFonctionCourant` ;
- C4 : composantes du vent de `ChampUniforme`, coordonnées de
  `ScenarioUniforme`, paramètres géométriques de `Rectangle`, ainsi que les
  points de mesures et de trajectoire de `ScenarioReconstruction` ;
- l'appel direct à `Rectangle.contient`, qui doit respecter le même contrat
  que la construction des scénarios.

Les booléens sont rejetés avant les calculs de phase, de norme ou de
comparaison géométrique. Les formules du champ, les unités, les coordonnées
et les hypothèses des expériences restent inchangées. Les validateurs
`_valide_point` restent locaux à leurs contextes : cette tranche ne remet pas
en cause l'arbitrage antérieur de ne pas introduire de module transversal
uniquement pour factoriser de petits helpers.


### Complément P0 — autres expériences C4 (issue #347, PR #352)

L'audit des autres configurations d'expérience a étendu le même contrôle aux
frontières suivantes :

- `relief` : points, vent, paramètres des collines et paramètres physiques
  du scénario ; les évaluations publiques d'altitude et de concentration
  vérifient aussi leurs coordonnées ;
- `superposition_sources` : positions, paramètres des sources, seuils,
  mesures et évaluations directes ;
- `identification_source` : points, vent, diffusivité, débit, seuils, pas de
  grille et indice de détection (qui doit exclure `bool`, sous-classe de `int`) ;
- `modele_reduit_edp` : paramètres positifs du scénario.

Les entrées booléennes Python et NumPy sont rejetées avant les calculs.
Aucune formule de transport, loi gaussienne, équation EDP, unité, condition
aux limites, hypothèse ou valeur par défaut n'est modifiée. La tranche
n'introduit aucun validateur transversal.

### Complément P0 — noyaux numériques vectorisés (issue #353, PR #357)

Une nouvelle vérification, après définition explicite du contrat d'exclusion des
booléens, a révélé que plusieurs fonctions convertissaient immédiatement les
coordonnées en `float64`. Cette conversion effaçait la nature booléenne avant
les contrôles de finitude.

La tranche couvre :

- `fields.vector_field` : coordonnées et quatre paramètres du champ ;
- `terrain.terrain_surface` : coordonnées et paramètres du relief ;
- `advection_diffusion.gaussian_advection_diffusion` : coordonnées et
  paramètres scalaires ;
- `periodic_transport.periodic_sine_solution` et les solveurs périodiques :
  coordonnées, paramètres et nombre de cellules.

Les séquences Python sont inspectées avant coercition ; les tableaux NumPy
booléens et objets contenant des booléens sont également rejetés. Les tableaux
déjà convertis en dtype entier ne conservent plus l'information de provenance,
limite inhérente à l'API ndarray et déjà documentée pour les autres frontières.

Aucune formule, condition de stabilité, unité, condition aux limites ni valeur
par défaut n'est modifiée. La note antérieure sur la conformité de
`fields.py` et `advection_diffusion.py` portait sur les contrôles de finitude,
pas sur l'exclusion explicite des booléens désormais exigée par le contrat.

### Complément P0 — métriques, trajectoires et explorateur (issue #360, PR #362)

Les frontières publiques suivantes rejettent explicitement les booléens Python et NumPy avant coercition numérique :

- `metric.temps_premiere_arrivee_1d` : positions et vitesse ;
- `metric.temps_transport` : polyligne, vent et seuil `umin` ;
- `metric.pseudo_distance_uniforme` : points et vecteur de vent ;
- `trajectories.integrate_trajectory` : conditions initiales et paramètres temporels ;
- `WindFieldExplorerConfig` : paramètres du champ et coordonnées de lecture.

Les tableaux et séquences sont inspectés avant coercition en `float64`. Aucune formule de temps, équation d'intégration, convention d'accessibilité ou règle de rendu n'est modifiée.

### Complément P0 — représentabilité des calculs EDP (issue #366, PR #372)

L'audit a confirmé que les paramètres de grille pouvaient être individuellement finis et positifs tout en donnant un rapport de multiplicité non représentable ; le chemin antérieur atteignait alors `round(inf)`. Les rapports sont désormais calculés avec une division ordonnée pour éviter un débordement intermédiaire inutile, puis contrôlés avant l'arrondi. Les rapports nuls par sous-débordement sont également rejetés. La dérivée analytique `derivee_sigma_carre` normalise les entrées en float64, contrôle les valeurs non finies et vérifie la représentabilité des intermédiaires et du résultat ; les débordements et sous-débordements silencieux sont convertis en `ValueError` contextualisée. Les expressions mathématiques, les coefficients, les domaines de signe et les unités restent inchangés. Ces garde-fous logiciels ne constituent pas une analyse de stabilité physique.

### Complément P0 — champs de concentration, métriques et grille EDP (issue #364, PR #371)

Le balayage des frontières C1/C5 a identifié des coercitions booléennes dans le champ passé à `constraints.positivite`, les observations des métriques FAC2/NMSE (y compris la façade `calculer_metriques`), et les tableaux et scalaires de `experiences.reference_independante`. La façade `benchmarks.reference.evaluer_prediction` conserve désormais le dtype de la vérité jusqu'à la validation des métriques.

Les booléens sont rejetés avant promotion en `float64`, y compris dans les séquences mixtes et les tableaux de type objet. Les formules, tolérances, unités, géométries, coefficients, conditions aux limites et domaines de signe restent inchangés. Ces tests établissent des contrats logiciels, pas une validation physique.

- **P0 résiduel** : poursuivre l'audit des validations d'entrée, des exceptions et des cas limites sur les frontières non encore couvertes ; le défaut bilinéaire MNT décrit au §4 n'est plus un travail restant.
- **P2** : l'annexe A liste les modules > 15 ko. La règle de #303 s'applique : la taille seule ne justifie pas une extraction ; chaque candidat exige une évaluation de cohésion. Le précédent `transitoire_puff` (monolithe 648 lignes → package 5 modules, identité numérique prouvée par tests inchangés, [docs/54](54-transitoire-puff-edp-transitoire-marginale.md)) est le gabarit à réutiliser.
- **P3** : contrôle d'architecture statique désormais intégré par #316 (`tests/test_architecture_boundaries.py`) ; il couvre la matrice d'imports, les dépendances de rendu et les cycles statiques, sans couvrir les imports dynamiques.
- La réduction de `__init__.py` suit l'inventaire d'usage du §6.

## Références

- [Chantier qualité #303](https://github.com/JM-Brun/J-DriftX/issues/303) — plan P0–P3 et définition of done par tranche.
- [docs/22](22-audit-package-code.md) — audit du package au regard de la charte qualité ; [docs/25](25-audit-harmonisation-oop-2026.md) — harmonisation OOP (recommandation 7 : modules d'enseignement non exportés) ; [docs/40](40-standards-qualite-tests-proprietes.md) — standards de tests et diagnostic architecture.
- [docs/42](42-contrats-interoperabilite.md) — contrats d'interopérabilité PEP 544 et standard MNT ESRI ASCII Grid.
- [docs/39](39-squelette-benchmarks-s0.md) — squelette de benchmarks ; [docs/41](41-unification-source-panache.md) — carte concepts → modules établie lors de l'unification `SourcePanache`.
- [docs/52](52-gouvernance-documentaire.md) — gouvernance documentaire (cette note est un document de travail d'architecture, pas une page publique du site).
- PR concernées : [#302](https://github.com/JM-Brun/J-DriftX/pull/302), [#304](https://github.com/JM-Brun/J-DriftX/pull/304), [#305](https://github.com/JM-Brun/J-DriftX/pull/305), [#306](https://github.com/JM-Brun/J-DriftX/pull/306), [#308](https://github.com/JM-Brun/J-DriftX/pull/308), [#309](https://github.com/JM-Brun/J-DriftX/pull/309) ; issue [#307](https://github.com/JM-Brun/J-DriftX/issues/307).

## Annexe A — Tailles des fichiers Python de `main` (30 octobre 2026, octets)

Modules > 15 ko (candidats P2) :

| Fichier | Taille (o) |
|---|---|
| `src/jdriftx/experiences/reference_independante.py` | 34 153 |
| `src/jdriftx/experiences/identification_source.py` | 27 307 |
| `src/jdriftx/figures/figure_06.py` | 20 849 |
| `src/jdriftx/experiences/modele_reduit_edp.py` | 20 485 |
| `src/jdriftx/experiences/relief.py` | 20 139 |
| `src/jdriftx/graphe_connaissances.py` | 19 244 |
| `src/jdriftx/experiences/superposition_sources.py` | 18 685 |
| `src/jdriftx/figures/wind_field_explorer.py` | 17 863 |

Bandes 10–15 ko (surveillance) : `figures/figure_04.py` (14 709), `figures/figure_03.py` (14 278), `figures/figure_05.py` (14 165), `experiences/reconstruction_vent.py` (14 163), `figures/figure_01.py` (12 612), `experiences/baseline_uniforme.py` (11 239), `experiences/evaluation_puff.py` (10 770). Le dépassement du seuil de 300 lignes correspond approximativement à la bande > 11–12 ko ; l'évaluation P2 se fait sur la cohésion, pas sur le décompte.
