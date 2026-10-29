# Unification de la source du panache : objet `SourcePanache` partagé

> **Statut — exécution de la recommandation P1 de [docs/40](40-standards-qualite-tests-proprietes.md), section 4, aucune vérité ni manifeste modifié.** Ce document répond au mandat du 30 octobre 2026 : continuer la modularisation du code (source, vent, relief, distance, transport) et tout tester. Le concept « source du panache », dupliqué entre les deux familles de cas S0, est extrait dans un module isolé ([source.py](../src/jdriftx/source.py)) ; chaque famille compose sa configuration avec le même objet de domaine. Aucune définition mathématique, aucun seuil ([#43](https://github.com/JM-Brun/J-DriftX/issues/43)), aucune vérité exacte et aucune clé de manifeste ne sont modifiés.

## 1. Question et modes de contribution

- **Question** : comment éliminer la duplication du concept « source » (débit, vent, classe de stabilité, hauteur) entre [experiences/cas_synthetiques.py](../src/jdriftx/experiences/cas_synthetiques.py) (jeux de données, docs/21) et [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py) (cas de benchmark, docs/39) sans changer les vérités exactes ni les manifestes JSON ?
- **Modes de contribution** : 3 (interface de domaine), 4 (tests) et 6 (documentation).

## 2. Ce qui change

| Élément | Avant | Après |
|---|---|---|
| Concept « source » | 4 champs plats (debit, u, classe, hauteur) répétés dans CasS0 et CasSynthetiqueS0, validés deux fois | Objet de domaine `SourcePanache` ([source.py](../src/jdriftx/source.py)), composé dans chaque famille, invariants portés une seule fois |
| Validation de la classe | CasS0 valide la classe ; CasSynthetiqueS0 ne la validait pas (écart documenté en docs/40, section 4) | La classe est validée à la construction dans les deux familles : l'écart est comblé |
| Manifestes (`DatasetS0.vers_dict`) | Clés plates « cas » : classe, debit, u, hauteur, altitude… | Clés et valeurs identiques octet par octet : la source est une structure interne, le JSON ne change pas |
| Vérités exactes | `concentration_panache` avec les champs du cas | Même appel, mêmes valeurs : aucun résultat numérique ne change |

`SourcePanache` est une frozen dataclass à quatre champs, validés en `__post_init__` : débit strictement positif, vent strictement positif, hauteur positive ou nulle, classe reconnue par [ClasseStabilite](../src/jdriftx/stabilite.py) (docs/24, source unique de vérité). Le nouveau module suit la charte : docstrings du code sans accents ni apostrophes, `dict` absent, `mypy --strict`.

## 3. Carte concepts → modules

La modularisation demandée (source, vent, relief, distance, transport) se lit dans le registre du graphe de connaissances ; chaque ligne est couverte par les tests de la CI :

| Concept | Modules | Objets et fonctions | Tests |
|---|---|---|---|
| **Source** | [source.py](../src/jdriftx/source.py) (nouveau), [experiences/identification_source.py](../src/jdriftx/experiences/identification_source.py) | `SourcePanache` (valeur partagée des familles S0, docs/41) ; identification inverse de la figure 6 (docs/36) | test_source.py (nouveau), test_cas_synthetiques.py, test_benchmarks_reference.py |
| **Vent (champ)** | [champ_analytique.py](../src/jdriftx/champ_analytique.py), [experiences/uniforme.py](../src/jdriftx/experiences/uniforme.py), [experiences/reconstruction_vent.py](../src/jdriftx/experiences/reconstruction_vent.py), [fields.py](../src/jdriftx/fields.py) | `ChampPlan`, `ChampFonctionCourant`, `SuperpositionChamps` (protocole PEP 544) ; `ChampUniforme`, `ScenarioUniforme` ; reconstruction à deux mesures (docs/23) ; champs vectoriels d'enseignement | test_champ.py, test_uniforme.py, test_recon.py, test_fields.py, test_proprietes.py |
| **Relief** | [terrain.py](../src/jdriftx/terrain.py), [experiences/relief.py](../src/jdriftx/experiences/relief.py) | `terrain_surface` (MNT synthétique d'enseignement) ; `ScenarioRelief`, figure 5 du chapitre 2008 (docs/34, niveau R1) | test_terrain.py, test_relief.py |
| **Distance** | [metric.py](../src/jdriftx/metric.py), [constraints.py](../src/jdriftx/constraints.py) | `temps_transport`, `pseudo_distance_uniforme` (métrique travel-time, docs/19 et docs/30) ; positivité, linéarité | test_metric.py, test_constraints.py, test_proprietes.py |
| **Transport** | [periodic_transport.py](../src/jdriftx/periodic_transport.py), [advection_diffusion.py](../src/jdriftx/advection_diffusion.py), [trajectories.py](../src/jdriftx/trajectories.py), [similitude.py](../src/jdriftx/similitude.py) | solveurs RK4/upwind et solution exacte 1D ; gaussienne advectée-diffusée ; intégration de trajectoires (cinématique seule) ; panache et puff gaussiens (Briggs) | test_periodic.py, test_advection.py, test_trajectories.py, test_similitude.py, test_proprietes.py |

La stabilité ([stabilite.py](../src/jdriftx/stabilite.py), docs/24) soutient tous ces concepts : elle est la source de vérité des classes de Pasquill et des lois de Briggs.

## 4. Registre du graphe

L'ajout du module `source.py` exige son nœud dans le registre ([site/data/graphe-connaissances.toml](../site/data/graphe-connaissances.toml)) — chaque module de `src/jdriftx` doit y figurer — plus trois arêtes structurelles « utilise » : `source` → `stabilite`, `benchmarks/cas` → `source`, `experiences/cas_synthetiques` → `source`. Le nœud rejoint la vue « Code, propriétés et preuves », groupe « Socle gaussien » ; le rendu ([site/projet/_graphes-mermaid.md](../site/projet/_graphes-mermaid.md)) est régénéré et committé avec le registre, la synchronisation octet par octet restant vérifiée par la CI.

## 5. Recommandations suivantes

- **P2 (candidate, non exécutée)** : `ScenarioRelief` ([experiences/relief.py](../src/jdriftx/experiences/relief.py)) porte aussi des champs de source (débit, classe, hauteur de source), mais ses invariants diffèrent — hauteur strictement positive (la source est posée sur le sol local), vent bidimensionnel (u, v), position (x, y) dans une fenêtre, collines sous le vent. L'unification avec `SourcePanache` n'est donc pas mécanique : elle n'a de valeur que si une troisième famille de cas partage réellement les mêmes invariants. À revisiter alors.
- **P3 (candidate, non exécutée)** : des propriétés générées bornées sur [terrain.py](../src/jdriftx/terrain.py) (colline et vallée bornées par ± hauteur, crête indépendante de x) et [fields.py](../src/jdriftx/fields.py) (champ uniforme de norme constante, cisaillement de divergence nulle) sont de bons candidats Hypothesis à coût de CI faible ; les solveurs itératifs ([periodic_transport.py](../src/jdriftx/periodic_transport.py), [trajectories.py](../src/jdriftx/trajectories.py)) restent exclus des propriétés générées, conformément à la règle 5 de docs/40, section 6.

## 6. Limites

Cette unification est une refactorisation structurelle : elle ne change ni les vérités exactes (mêmes appels à `concentration_panache`, mêmes valeurs), ni les manifestes (clés inchangées), ni les définitions FAC2/NMSE de [#43](https://github.com/JM-Brun/J-DriftX/issues/43). `SourcePanache` n'est pas une source physique : débit, vent, classe et hauteur effective sont des paramètres du modèle de similitude, pas des mesures. L'API des deux constructeurs change (champs plats → champ `source`) : les deux familles de tests sont adaptées dans la même PR, sans valeur d'assertion modifiée au-delà des chemins d'accès (`cas.debit` → `cas.source.debit`).

## 7. Périmètre et suivi

| Élément | Statut |
|---|---|
| Recommandation P1 (docs/40, section 4) | **Exécutée** (sections 2 et 4) |
| Écart de validation de la classe (CasSynthetiqueS0) | **Comblé**, test de rejet dédié |
| Manifestes S0 | **Inchangés octet par octet** (test de manifeste étendu aux quatre champs source) |
| Registre du graphe | **Mis à jour** (nœud `source`, 3 arêtes, vue code, rendu synchronisé) |
| Carte concepts → modules (source, vent, relief, distance, transport) | **Documentée** (section 3) |
| P2 (ScenarioRelief) et P3 (terrain, fields) | **Candidats documentés**, non exécutés |

## Références

- Exécution : [source.py](../src/jdriftx/source.py), [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py), [experiences/cas_synthetiques.py](../src/jdriftx/experiences/cas_synthetiques.py) ; tests : [test_source.py](../tests/test_source.py), [test_cas_synthetiques.py](../tests/test_cas_synthetiques.py), [test_benchmarks_reference.py](../tests/test_benchmarks_reference.py), [test_proprietes.py](../tests/test_proprietes.py).
- Contexte interne : docs/21 (jeux de données et cas synthétiques), docs/24 (objets de stabilité), docs/34 (relief, figure 5), docs/39 (benchmarks), docs/40 (diagnostic et recommandation P1) ; contrats inchangés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
