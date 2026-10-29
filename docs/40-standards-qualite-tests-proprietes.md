# Standards qualité : tests de propriété (Hypothesis), objet et diagnostic

> **Statut — revue des standards et extension de tests, aucun comportement du cœur modifié.** Ce document répond au mandat du 29 octobre 2026 : continuer l'amélioration du code Python (orientation objet, modules isolés, TDD, DDD, tests de propriété avec Hypothesis) et vérifier quels standards existent pour ces pratiques. Il documente la conformité du noyau, la duplication identifiée, les standards relevés et l'extension exécutée dans [tests/test_proprietes.py](../tests/test_proprietes.py). Aucune définition mathématique, aucun seuil ([#43](https://github.com/JM-Brun/J-DriftX/issues/43)) et aucun comportement du cœur ne sont modifiés.

## 1. Question et modes de contribution

- **Question** : quelles pratiques de test et d'architecture sont déjà standardisées, où le package s'y conforme déjà, et quelle extension exécuter sans toucher aux définitions préenregistrées ?
- **Modes de contribution** : 4 (tests et diagnostic de preuve) et 6 (documentation).

## 2. Standards existants

- **Test logiciel.** La famille ISO/IEC/IEEE 29119 normalise les processus, la documentation et les techniques du test logiciel ([softwaretestingstandard.org](https://www.softwaretestingstandard.org)) ; elle ne prescrit ni langage ni style de test unitaire et ne couvre pas la génération d'entrées. Le dépôt en retient l'exigence de traçabilité — chaque test énonce ce qu'il établit et sous quelles hypothèses, déjà la règle du [CONTRIBUTING](../CONTRIBUTING.md) — pas une conformité de certification.
- **Tests de propriété.** Le standard de fait en Python est [Hypothesis](https://hypothesis.readthedocs.io) : générer des entrées depuis des stratégies, vérifier une propriété, rétrécir les contre-exemples. Le dépôt l'utilise déjà comme dépendance de développement et dans [tests/test_proprietes.py](../tests/test_proprietes.py) ; la section 5 étend cet usage, la section 6 fixe les règles.
- **Logiciel scientifique.** Les enquêtes sur le test des logiciels de recherche (par exemple [arXiv:2205.15982](https://arxiv.org/abs/2205.15982), [arXiv:2501.17739](https://arxiv.org/abs/2501.17739)) soulignent l'absence d'oracle : la propriété mathématique — invariants, symétries, cas exacts — sert d'oracle de substitution. C'est la stratégie du dépôt : solutions exactes et identités (adjoint, conservation, superposition) comme oracles, jamais de captures ni de valeurs magiques.
- **Objet et domaine.** Le dépôt applique les principes utiles du DDD — modèle et langage explicites, objets de domaine portant leurs invariants ([Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)) — sans en adopter le vocabulaire d'infrastructure ; la structure Given–When–Then des tests, issue du BDD ([Behavior-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development)), est déjà la règle du [CONTRIBUTING](../CONTRIBUTING.md).
- **Typage structurel.** Les protocoles Python ([PEP 544](https://peps.python.org/pep-0544/), [mypy/protocols](https://mypy.readthedocs.io/en/stable/protocols.html)) fournissent le standard des contrats structurels du dépôt (par exemple ChampPlan) : une interface sans hiérarchie de classes.

## 3. Diagnostic du noyau : déjà conforme

| Principe (CONTRIBUTING « Qualité du code ») | État dans le package |
|---|---|
| Objets de domaine à invariants | Frozen dataclasses validées à la construction (ChampUniforme, CasS0, CasSynthetiqueS0…) |
| Contrats explicites sans hiérarchies profondes | Protocoles structurels (PEP 544), ABC minimale (CasSynthetique), StrEnum pour les vocabulaires fermés (ClasseStabilite, FormeSigmaZ) |
| Modules isolés, une responsabilité | benchmarks/ (cas, metriques, reference), experiences/, similitude/stabilite, metric/trajectories ; séparation calcul/rendu tenue |
| dict uniquement aux frontières JSON | vers_dict réservés aux manifestes et exports ; structures typées en interne |
| Registres avec garde-fous à l'enregistrement | enregistrer_cas, enregistrer_metrique : invariants vérifiés avant disponibilité |

Conclusion du diagnostic : le noyau est conforme à la charte ; aucun refactoring du cœur n'est motivé par cette revue. Les candidats d'amélioration sont des duplications de concept, pas des défauts de style.

## 4. Duplication identifiée (recommandation P1, hors de cette extension)

Le concept « cas S0 » existe en deux endroits, tous deux conformes à la charte mais redondants :

- [experiences/cas_synthetiques.py](../src/jdriftx/experiences/cas_synthetiques.py) : CasSynthetiqueS0 (tirage aléatoire versionné, PartitionS0 70/30, manifeste JSON) ;
- [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py) : CasS0 (grille croisée déterministe, registre de cas).

Les deux délèguent le calcul à concentration_panache et partagent le concept physique (classe, débit, vent, hauteur de source). La valeur commune pourrait être extraite en un objet partagé, chaque module gardant sa spécificité (jeu de données vs cas de benchmark). **Recommandation P1** : unification dans une PR dédiée, après décision du propriétaire — elle touche deux familles de tests et deux manifestes, et ne doit pas être mélangée avec l'extension de tests présentée ici. **P2** : les solveurs itératifs ([periodic_transport.py](../src/jdriftx/periodic_transport.py)) restent volontairement sans propriété générée — leur stabilité numérique conditionne le verdict et une propriété mal bornée ferait échouer la CI pour de mauvaises raisons ; les tests exacts existants suffisent.

## 5. Extension exécutée : propriétés ajoutées

[tests/test_proprietes.py](../tests/test_proprietes.py) passe de 6 à 18 propriétés générées :

| Zone | Propriété | Hypothèses exactes |
|---|---|---|
| [benchmarks/metriques.py](../src/jdriftx/benchmarks/metriques.py) | prédiction parfaite : FAC2 = 1, NMSE = 0 ; bornes FAC2 ∈ [0, 1] et NMSE ≥ 0 ; NMSE = 1 au double exact ; invariance par homothétie commune | vérité strictement positive (conventions [#43](https://github.com/JM-Brun/J-DriftX/issues/43)) ; ratios à distance des bornes FAC2 pour l'invariance |
| [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py) | grille croisée arcs × positions ; vérité strictement positive | cas S0 valide (invariants du constructeur) |
| [experiences/cas_synthetiques.py](../src/jdriftx/experiences/cas_synthetiques.py) | partition 70/30 couvrante et disjointe | au moins 2 points, graine quelconque |
| [metric.py](../src/jdriftx/metric.py) | symétrie t(a, b, v) = t(b, a, −v) ; valeur exacte en aval, infini en amont, zéro à la source | dynamique constante 1D |
| [similitude.py](../src/jdriftx/similitude.py) | sigma_y et sigma_z strictement positifs et strictement croissants en distance | classes Briggs du package, distance positive |
| [advection_diffusion.py](../src/jdriftx/advection_diffusion.py) | pic au centre advecté, symétrie, valeur du pic masse/√(2π·variance) | vitesse et diffusivité constantes, K ≥ 0 |
| [periodic_transport.py](../src/jdriftx/periodic_transport.py) | enveloppe [moyenne ± amplitude·exp(−K·k²·t)] et périodicité spatiale L | solution exacte, pas les solveurs itératifs |

Aucune définition FAC2/NMSE de [#43](https://github.com/JM-Brun/J-DriftX/issues/43) n'est modifiée : les propriétés affirment ce que les définitions garantissent, rien d'autre.

## 6. Règles retenues pour les tests de propriété

1. une propriété par test, énoncée sous ses hypothèses exactes (docs/30, section 2) ;
2. stratégies bornées : plages fermées et tailles maximales petites, pour un coût de CI borné ;
3. `@settings(deadline=None)` : la CI partage ses ressources, un délai par essai serait non déterministe ;
4. les discontinuités (bornes FAC2, conventions d'inaccessibilité) sont testées soit exactement (double exact), soit avec une marge explicite (bande autour des bornes) ;
5. pas de propriété générée sur les solveurs itératifs : leurs conditions de stabilité sont vérifiées par des tests exacts.

Ces règles rejoignent le [CONTRIBUTING](../CONTRIBUTING.md) (section « Tests — TDD »), mis à jour dans la même PR.

## 7. Limites

Un test de propriété générée n'est ni une preuve mathématique (Hypothesis échantillonne, il ne démontre pas), ni une validation physique (les hypothèses H1–H8 restent des hypothèses), ni un diagnostic d'utilité applicative. Un contre-exemple généré, en revanche, est un bogue avéré. Ce vocabulaire est celui du [CONTRIBUTING](../CONTRIBUTING.md) (« Validation et limites des preuves ») et de docs/08.

## 8. Périmètre et suivi

| Élément | Statut |
|---|---|
| Revue des standards (ISO/IEC/IEEE 29119, Hypothesis, littérature logiciel scientifique, DDD/BDD, PEP 544) | **Fait** (section 2) |
| Diagnostic architecture du noyau | **Fait** (section 3 : conforme, aucun refactoring motivé) |
| Duplication CasS0/CasSynthetiqueS0 | **Documentée** (section 4, recommandation P1 pour une PR dédiée) |
| Extension des tests de propriété (6 → 18) | **Fait** (section 5) |
| Règles Hypothesis dans le CONTRIBUTING | **Fait** (section 6) |
| Unification du concept S0 | **Non commencé** — décision du propriétaire requise |

## Références

- Extension : [tests/test_proprietes.py](../tests/test_proprietes.py) ; règles : [CONTRIBUTING.md](../CONTRIBUTING.md).
- Standards : ISO/IEC/IEEE 29119 ; Hypothesis ; enquêtes sur le test des logiciels de recherche (arXiv:2205.15982, arXiv:2501.17739) ; DDD et BDD (Given–When–Then) ; PEP 544 (protocoles).
- Contexte interne : docs/24 (objets de stabilité), docs/27 (traçabilité MVP-S), docs/30 (glossaire et carte des propriétés), docs/39 (benchmarks) ; contrats inchangés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
