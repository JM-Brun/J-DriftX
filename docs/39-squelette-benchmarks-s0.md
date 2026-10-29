# Squelette de benchmarks : cas analytique S0 et architecture extensible

> **Statut — squelette reproductible, aucun résultat anticipé.** Ce document répond à l'issue [#17](https://github.com/JM-Brun/J-DriftX/issues/17) : définir le cas analytique minimal, choisir les métriques et mesures de coût, préparer une commande reproductible et documenter la baseline — **sans anticiper aucun résultat**. Le cas S0 n'est pas une validation physique ; aucun benchmark applicatif ne démarre avant la porte G1 (inspection des fichiers, [#204](https://github.com/JM-Brun/J-DriftX/issues/204), déléguée).

## 1. Architecture : objets isolés pour évoluer séparément

Le package `jdriftx.benchmarks` sépare trois responsabilités, chacune avec son point d'extension :

| Module | Responsabilité | Extension prévue |
|---|---|---|
| [`benchmarks/cas.py`](../src/jdriftx/benchmarks/cas.py) | Contrat `CasSynthetique` (identifiant, grille de points, vérité exacte strictement positive), cas `CasS0`, registre (`enregistrer_cas`, `lister_cas`, `construire_cas`, `retirer_cas`) | Nouveaux cas : S0-b à S0-d, S1, S2, S3 ([docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md)) |
| [`benchmarks/metriques.py`](../src/jdriftx/benchmarks/metriques.py) | `Metrique` (nom stable, libellé, ancrage, calcul), `FAC2`/`NMSE` préenregistrées, registre `METRIQUES`, jeu par défaut `METRIQUES_DEFAUT` | Métriques futures, uniquement après pré-enregistrement des seuils ([#43](https://github.com/JM-Brun/J-DriftX/issues/43)) |
| [`benchmarks/reference.py`](../src/jdriftx/benchmarks/reference.py) | Pipeline : `evaluer_prediction` → `ResultatEvaluation` (export JSON), `mesurer_cout_inference`, commande `main` | Consomme les deux registres : un nouveau cas ou une nouvelle métrique enregistré fonctionne sans toucher au pipeline |

Deux invariants sont vérifiés **à l'enregistrement**, pas seulement à l'usage : identifiant unique, et pour un cas, grille non vide et vérité strictement positive sur la grille. Un cas invalide ne peut donc pas devenir silencieusement disponible.

## 2. Cas analytique reproductible S0

- **Source** : émission continue de débit massique Q (kg s⁻¹) à hauteur effective H.
- **Champ de vitesse** : vent uniforme U (m s⁻¹) selon +x, classe de stabilité de Pasquill fixée (défaut : C, site rural).
- **Vérité** : la solution de similitude du package elle-même (module jdriftx.similitude, fonction concentration_panache, tables de Briggs/Pasquill, réflexion au sol incluse) — aucun développement mathématique dupliqué.
- **Observable** : concentration aérienne (kg m⁻³), conformément à [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
- **Grille de prélèvements** : arcs sous le vent (défaut : 100, 200, 400, 800 m) × positions latérales (défaut : −50, 0, +50 m) à altitude de mesure fixée (défaut : 1,5 m).
- **Cas par défaut** : constante CAS_S0_DEFAUT (vent 3 m/s, débit 2 kg/s, classe C, hauteur 1 m).

Conformément à docs/21 (famille S0, sous-cas S0-a) : générateur déterministe, aucune donnée observée, clause « pas une validation physique ».

## 3. Métriques d'erreur et mesures de coût

Métriques **préenregistrées par [#43](https://github.com/JM-Brun/J-DriftX/issues/43), inchangées** :

- **FAC2** : fraction des points avec 0,5 ≤ prediction/vérité ≤ 2, bornes incluses, ratio point à point.
- **NMSE** : Σ(prediction − vérité)² / Σ(vérité)². **Convention explicite** : d'autres usages prennent Σ(vérité × prediction) au dénominateur ; le choix est documenté dans les docstrings pour lever toute ambiguïté avant tout benchmark.
- Évaluation **par essai/scénario indépendant** (jamais par point isolé), conformément à #43.

Mesures de coût (issue #17 : préparation et inférence) : la fonction mesurer_cout_inference mesure le temps d'un appel d'inférence ; la mesure est **non déterministe** et n'entre dans aucune assertion. Les seuils de succès G2 (au moins 60 % des essais indépendants ; coût total au moins 10× inférieur pour erreur comparable) restent ceux de #43.

## 4. Commande reproductible

~~~bash
uv run python -m jdriftx.benchmarks.reference [identifiant]
~~~

Le passage à vide évalue la prédiction contre elle-même : FAC2 = 1 et NMSE = 0 sont des **contrôles d'auto-cohérence du pipeline** (grille → vérité → métriques), pas un résultat scientifique. Sans argument, la commande utilise le cas enregistré `S0` ; `lister_cas()` expose les identifiants disponibles. Toute évaluation future d'un candidat contre la vérité S0 passe par evaluer_prediction(vérité, prédiction).

## 5. Baseline et hypothèses communes

- **Baseline** (préenregistrée par #43) : panache gaussien simple, mêmes entrées, même observable. Dans le cas S0, la vérité analytique **est** la baseline gaussienne : le squelette vérifie donc le pipeline, et n'établit aucune supériorité.
- **Hypothèses communes** : linéarité (H1), stationnarité sur la fenêtre (H3), homogénéité du segment (H5), vent uniforme non nul ; garde-fou de #43 : le cas S0 teste une hypothèse de méthode sur un scalaire, pas la dérive de pulvérisation.
- **Ce que le squelette ne fait pas** : aucune comparaison de modèle, aucun résultat rapporté, aucun seuil modifié, aucune donnée observée (G1) chargée.

## 6. Points d'extension : ajouter un cas, plus tard

Ajouter un cas (par exemple S0-b, cisaillement en loi de puissance de [docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md)) se fait sans toucher au pipeline :

1. implémenter une dataclass frozen dérivée de `CasSynthetique` : `identifiant`, `libelle`, `points()`, `verite()` ;
2. l'enregistrer par `enregistrer_cas` — invariants (grille non vide, vérité strictement positive) vérifiés à ce moment ;
3. ajouter ses tests GWT (validation des paramètres, exactitude de la vérité) ;
4. la commande `uv run python -m jdriftx.benchmarks.reference <identifiant>` fonctionne sans autre changement.

Ce qui reste volontairement hors du squelette : le bruit et les graines (famille S1 — docs/21 impose graines fixées et partitions calibrage/évaluation figées avant toute expérience, à spécifier dans une issue dédiée), les vérités hors famille (S2/S3 : dépendances de licence et de code à auditer d'abord) et tout format de fichier (les frontières du package restent dict/JSON, charte du dépôt). Ajouter une métrique est possible (`enregistrer_metrique`) mais délibérément gardé : sans seuils de succès G2/G3 préenregistrés dans [#43](https://github.com/JM-Brun/J-DriftX/issues/43), une métrique ne doit pas rejoindre `METRIQUES_DEFAUT`.

## 7. Standards existants pour ces métriques et données

- **Métriques.** FAC2 et NMSE sont les métriques usuelles de l'évaluation des modèles de dispersion atmosphérique, établies par l'initiative Harmonisation : le [Model Validation Kit](https://www.harmo.org/kit.php) (Kincaid, Copenhagen, Lillestrøm, Indianapolis) et son logiciel BOOT calculent NMSE, MG, VG, FAC2, FB et MOE ([clé du Kit](https://harmo.isac.cnr.it/Kit/Download/Kit_key.pdf)) ; le guide [ASTM D6589](https://www.astm.org/Standards/D6589.htm) formalise l'évaluation statistique des performances d'un modèle de dispersion. Les conventions de la section 3 (bornes incluses, dénominateur Σ(vérité)²) sont documentées précisément parce que ces standards admettent des variantes.
- **Données de validation terrain.** Les corpus classiques (Prairie Grass, Kit) circulent en fichiers texte simples structurés par essai indépendant (météorologie et concentrations aux récepteurs) ; l'essai — jamais le point isolé — y est l'unité d'évaluation, comme l'exige déjà [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
- **Données maillées et benchmarks ML.** Pour des données plus volumineuses, les standards de fait sont : NetCDF avec [conventions CF](https://cfconventions.org/) (dont les géométries d'échantillonnage discret pour les séries de points), HDF5 avec schéma documenté pour les vérités de solveurs ([PDEBench](https://github.com/pdebench/PDEBench), NeurIPS 2022 : tableaux échantillons × pas de temps × dimensions) et Zarr pour les séries climatiques ([WeatherBench 2](https://weatherbench2.readthedocs.io/)).
- **Décision pour J-DriftX.** Les vérités synthétiques restent générées par du code versionné (aucun fichier de données dans le dépôt), les échanges aux frontières du package restent JSON, et si un corpus réel (porte G1) exige un format binaire, CF-NetCDF ou Zarr seront les candidats par défaut — décision à consigner dans le protocole G1, pas ici.

## 8. Périmètre et suivi

| Élément de #17 | Statut |
|---|---|
| Cas analytique reproductible (source, champ, observable) | **Fait** (section 2, classe CasS0) |
| Métriques d'erreur et mesures de coût | **Fait** (section 3, conventions explicites, registre isolé) |
| Squelette + commande reproductible sans résultat | **Fait** (section 4, commande paramétrée par identifiant) |
| Baseline et hypothèses communes documentées | **Fait** (section 5) |
| Extension : nouveaux cas et benchmarks | **Préparé** (section 1 et 6, registres et contrat) |
| Benchmark applicatif sur données observées | **Non commencé — bloqué** par G1 (#204, DIFLU déléguée) et la décision G0-A du propriétaire |

L'issue #17 reste ouverte tant que le benchmark applicatif n'a pas de donnée inspectée ; le squelette S0 est la première brique, réutilisable telle quelle pour la famille S1 (vérités bruitées, docs/21) quand la porte G1 sera franchie.

## Références

- Squelette : [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py), [benchmarks/metriques.py](../src/jdriftx/benchmarks/metriques.py), [benchmarks/reference.py](../src/jdriftx/benchmarks/reference.py) ; tests GWT : [tests/test_benchmarks_reference.py](../tests/test_benchmarks_reference.py).
- Critères préenregistrés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43) ; cas synthétiques S0–S3 : [docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md).
- Standards : Model Validation Kit et BOOT (initiative Harmonisation) ; guide ASTM D6589 ; conventions CF ; PDEBench (NeurIPS 2022) ; WeatherBench 2.
