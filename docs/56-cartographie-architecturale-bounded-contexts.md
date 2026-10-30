# 56 — Cartographie architecturale et bounded contexts (chantier #303, P1)

## Statut

Note d'architecture portant la tranche P1 du [chantier qualité #303](https://github.com/JM-Brun/J-DriftX/issues/303) : cartographie des dépendances, définition des contextes délimités (bounded contexts) et des règles de dépendances autorisées. **État des lieux initial de `main` au commit `8869419` ; actualisation du suivi sur la base `main` du 30 octobre 2026 (commit `e036dad`). Aucune décision de migration n'est appliquée dans cette note** : les arbitrages (réduction de `__init__.py`, déplacement de l'outillage de graphe, gardes résiduelles) restent au propriétaire. Cette note ne change aucune équation, tolérance, contrat d'exécution ni test.

## Actualisation du suivi — 30 octobre 2026

Cette actualisation complète l'état des lieux initial sans modifier les décisions d'architecture. Les trois tranches numériques suivantes sont maintenant implémentées dans des PR distinctes, CI verte, mais **non fusionnées** :

- **PR #311** : stabilité des évaluations gaussiennes panache/puff, associée à l'issue #307 ; CI complète verte (672 tests, 95 % de couverture).
- **PR #313** : représentabilité des temps et coûts de transport dans `metric.py` ; CI complète verte (669 tests, 95 %).
- **PR #314** : réduction des phases et calcul robuste des composantes du champ analytique ; CI complète verte (666 tests, 95 %).

Ces résultats ne ferment pas les items P0 avant revue et intégration. Ils ne valent pas validation physique. Le résidu théorique sur l'interpolation bilinéaire du MNT reste à arbitrer.

L'inventaire d'usage interne de l'API racine a également été précisé (§6.1). Il ne permet pas de conclure sur d'éventuels consommateurs externes ; en conséquence, aucune réduction d'API n'est proposée.

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
| **C8. Applications, site et scripts** (hors package) | `apps/`, `site/`, `scripts/` | applications interactives, publication, contrôle | API publique du package (`__init__.py`) uniquement |

## 3. Règles de dépendances proposées

Constat préalable : **sur `main`, aucune inversion ni cycle n'existe** — les arêtes du registre vont toutes des contextes aval (C4–C7) vers l'amont (C1–C2), et chaque figure ne consomme que son expérience. La règle ci-dessous fige cet état de fait au lieu d'en inventer un nouveau ; elle servirait de base au contrôle d'architecture léger évoqué en P3 de #303.

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

## 4. État de P0 — frontières NumPy (verdict)

Le périmètre P0 de #303 est **épuisé** par les tranches fusionnées :

- **#302** : immutabilité réelle (bytes-backed `np.frombuffer`) et sentinelle `nodata` finie de `ReliefMntAscii`, coordonnées d'interpolation validées ;
- **#304** : audit `source` (déjà conforme), gardes `similitude` (scalaires et grilles finis, débordement `u·t`, distance sous le vent), `metric` (débordement `b − a`, somme des coûts), `terrain` (coordonnées finies) ;
- **#305** : normalisation avant mise au carré dans `terrain_surface` (sous-débordement `width²`) ;
- **#306** : somme `SuperpositionPanaches`, en-tête MNT (`ncols`/`nrows` finis), profil de vent en loi de puissance, champ plan adapté ;
- **#308** : nombre d'onde, coordonnées, vitesse et superposition de `champ_analytique` ;
- **#309** : échelles extrêmes gaussiennes (exposants normalisés, chemin de secours logarithmique, exception documentée) — les trois cas de l'[issue #307](https://github.com/JM-Brun/J-DriftX/issues/307) sont couverts par ses tests ; la [PR #311](https://github.com/JM-Brun/J-DriftX/pull/311) (en cours du propriétaire) étend la famille aux très grandes distances.

**Résidu théorique identifié** : la somme bilinéaire pondérée de `ReliefMntAscii.altitude` (`z00·p00 + z10·p10 + z01·p01 + z11·p11`) n'est pas contrôlée — quatre altitudes finies proches du maximum float64 peuvent sommer en débordement silencieux. Aucun MNT réel connu du projet n'atteint ces ordres de grandeur. Décision au propriétaire : ajouter une garde explicite ou documenter l'hypothèse de plage physique du MNT. Ce point reste distinct des PR #311/#313/#314.

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

- Aucun usage interne direct des symboles racine n'a été trouvé dans les imports des sources, applications et scripts inspectés.
- Le dépôt vérifie des ré-exports de compatibilité ciblés, mais ne fournit pas d'inventaire des notebooks personnels, scripts hors dépôt, installations publiées ou consommateurs externes.
- L'absence d'usage interne n'est pas une preuve d'absence d'usage public. Les exports du noyau, des contrats et des expériences restent donc inchangés.
- Toute réduction ultérieure devra être une décision explicite de versionnement/API, accompagnée d'une période de dépréciation si le package devient consommé hors du dépôt.

Conclusion : l'inventaire interne est terminé ; la réduction de l'API racine est **différée**, sans suppression ni renommage.

## 7. Outillage de graphe — évaluation, pas migration

`graphe_connaissances`, `extraction_graphe` et `diagnostic_graphe` (contexte C7) ne participent à aucun calcul scientifique, n'importent rien de C1–C6, et sont auto-testés. #303 demande d'« évaluer le déplacement » : **le statu quo est recommandé** — le déplacement hors package (par ex. `tools/`) n'apporterait qu'une étiquette, coûterait une migration d'imports (CI, `python -m jdriftx.diagnostic_graphe`, tests de synchronisation) et affaiblirait la règle « chaque module a un nœud ». À rouvrir seulement si le package est un jour publié sur PyPI avec un périmètre strictement scientifique.

## 8. Suites (P0 résiduel, P2/P3 de #303)

- **P0 résiduel** : faire relire et intégrer #311, #313 et #314 avant de cocher les tranches correspondantes ; arbitrer séparément le cas théorique de débordement de l'interpolation bilinéaire du MNT.
- **P2** : l'annexe A liste les modules > 15 ko. La règle de #303 s'applique : la taille seule ne justifie pas une extraction ; chaque candidat exige une évaluation de cohésion. Le précédent `transitoire_puff` (monolithe 648 lignes → package 5 modules, identité numérique prouvée par tests inchangés, [docs/54](54-transitoire-puff-edp-transitoire-marginale.md)) est le gabarit à réutiliser.
- **P3** : une fois les règles du §3 validées par le propriétaire, un contrôle d'architecture léger (imports interdits C1←C4/C6, absence de cycles) devient réalisable — #303 le conditionne explicitement à la définition des frontières, que cette note fournit.
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
