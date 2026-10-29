# 54 — EDP transitoire du puff (marche en temps de la marginale transverse)

**Statut.** Note d'expérience ouvrant la route EDP transitoire de la source impulsionnelle de l'[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : la marginale transverse Q(y, z, t) du puff est marchée en temps par un schéma FTCS, route indépendante de la solution fermée, comparée à celle-ci sur la grille du cas de référence S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2). Suite directe de l'évaluation dirigée ([note 53](53-evaluation-puff-source-impulsionnelle.md)). Implémentation : package [experiences/transitoire_puff/](../src/jdriftx/experiences/transitoire_puff) ; tests : [tests/test_transitoire_puff.py](../tests/test_transitoire_puff.py). Les sigles (FTCS, NMSE, FAC2, GWT, R1…) et les termes spécialisés (marginale, route, solution fermée, conditions de Dirichlet et de Neumann) sont définis dans le [Lexique et notations](#lexique-et-notations) ci-dessous.

**Date :** 29 octobre 2026. **Suivi :** [issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) ; étiquetage héritage/reconstruction/extension conformément au [contrat minimal](47-contrat-minimal-baseline.md) §3.4.

## Lexique et notations

Sigles et termes spécialisés utilisés par cette note, définis ici à leur premier emploi ; chaque entrée renvoie au document qui développe la notion.

| Terme ou sigle | Définition | Développé dans |
|---|---|---|
| EDP | Équation aux dérivées partielles — ici l'équation de diffusion parabolique ∂Q/∂t = Ky ∂²Q/∂y² + Kz ∂²Q/∂z², que la route numérique intègre pas à pas | [note 51](51-reference-independante-cas-s0.md) §2 |
| Puff | Source impulsionnelle : une masse M émise instantanément (1,0 kg ici), par opposition au panache continu | [note 53](53-evaluation-puff-source-impulsionnelle.md) |
| Marginale transverse | L'intégrale longitudinale de la concentration, Q(y, z, t) = ∫ C(x, y, z, t) dx (kg m⁻²) — « marginale » par analogie avec les lois marginales : la concentration vue depuis la direction intégrée | §2, étape 1 ci-dessous |
| Route de calcul | Procédure complète, des entrées partagées aux valeurs de concentration aux points de mesure ; comparer deux routes, c'est comparer deux résolutions indépendantes du même problème | [note 35](35-figure-03-modele-reduit-edp.md) |
| Solution fermée | Expression analytique exacte du puff (`jdriftx.similitude.concentration_puff`) : évaluation directe, sans itération ni discrétisation — c'est la lecture de la route fermée | [note 53](53-evaluation-puff-source-impulsionnelle.md) §2 |
| Route EDP | Résolution numérique de l'EDP par le schéma FTCS, échantillonnage aux points, puis application de la structure longitudinale | §2, étapes 2–4 ci-dessous |
| Mesure | Résultat typé d'une route : valeurs aux points et coût mesuré (`MesureFermeePuff`) ; la mesure EDP porte en plus les écarts de masse et la solution complète (`MesureEdpPuff`) | §6 ci-dessous |
| FTCS | *Forward in Time, Centred in Space* : schéma explicite — le champ à t + Δt est une combinaison directe du champ à t, aux différences finies centrées en espace ; aucun système linéaire à résoudre, en échange une condition de stabilité | [note 51](51-reference-independante-cas-s0.md) §2 |
| Nombre de Fourier | Fo = K·Δt/Δy² par direction : le critère de stabilité du schéma explicite, somme bornée à 1/3 ici | [note 51](51-reference-independante-cas-s0.md) §2 |
| Condition de Dirichlet | Condition aux limites qui impose la **valeur** de la solution au bord — ici concentration nulle aux bords latéraux et au sommet de la fenêtre (la masse qui y passe est perdue : c'est la troncature documentée) | [note 51](51-reference-independante-cas-s0.md) §2 |
| Condition de Neumann | Condition aux limites qui impose le **flux** normal (la dérivée) — ici ∂Q/∂z = 0 au sol : le champ se refléchit symétriquement (« miroir »), exact car le noyau du puff est pair en z | §2, étape 3 ci-dessous |
| Fenêtre 4σ | Domaine de calcul tronqué à quatre écarts-types (σ : écart-type des gaussiennes) aux derniers instants ; la masse au-delà est documentée comme tronquée | §3 ci-dessous ; [note 48](48-cas-reference-autonome-ecoulement-uniforme.md) |
| NMSE | *Normalized Mean Square Error* : somme des carrés des écarts divisée par la somme des carrés de la référence — une erreur quadratique sans unité, comparable entre expériences | registre [note 39](39-squelette-benchmarks-s0.md) §3 ; [issue #43](https://github.com/JM-Brun/J-DriftX/issues/43) |
| FAC2 | *Fraction within A factor of Two* : fraction des points dont la prédiction tombe entre 0,5 et 2 fois la référence (1,0 = tous) | registre [note 39](39-squelette-benchmarks-s0.md) §3 |
| Arcs, instants dirigés | La grille de mesure du cas S0 est organisée en arcs sous le vent (100/200/400/800 m) ; le vent uniforme u porte le puff : chaque arc x correspond à l'instant de passage t = x/u | [note 53](53-evaluation-puff-source-impulsionnelle.md) §2 |
| Carte travel-time | Changement de variable longitude → temps (t = x/u sous vent uniforme) : l'advection devient une simple translation du temps, la marche en longitude de l'étape 5 devient une marche en temps | [note 37](37-transformation-tau-eta-cas-uniforme.md) |
| Isotropie σx = σy | La solution fermée du package donne au puff la même largeur longitudinale et transverse | [note 53](53-evaluation-puff-source-impulsionnelle.md) §2 |
| Écart de masse | Écart relatif entre la masse de la marginale EDP et celle de la marginale fermée, à chaque instantané, intégré sur la même grille (trapèzes doubles) : contrôle de conservation | §4.1 ci-dessous |
| Cas S0 | Cas de référence synthétique à écoulement uniforme : vent, classe de stabilité, unités et grille de 12 points figés | [note 48](48-cas-reference-autonome-ecoulement-uniforme.md) |
| GWT | *Given–When–Then* : chaque test nomme son contexte, son action et sa conséquence attendue | [note 40](40-standards-qualite-tests-proprietes.md) |
| R1 | Niveau de fidélité « reconstruction conceptuelle » de l'échelle d'héritage documentaire : aucune donnée historique comme cible | [note 47](47-contrat-minimal-baseline.md) §3.4 |
| Manifeste étiqueté | Export JSON de l'expérience — identifiant, étiquettes héritage/reconstruction/extension, limites, comparaison, version, commande — reproductible hors du dépôt | [note 35](35-figure-03-modele-reduit-edp.md) ; [note 51](51-reference-independante-cas-s0.md) §5 |
| PEP 544 | Protocoles Python à typage structurel : une classe satisfait le contrat en exposant la méthode attendue, sans héritage ni inscription | [note 42](42-contrats-interoperabilite.md) ; [PEP 544](https://peps.python.org/pep-0544/) |

## 1. Objectif et étiquetage

- **Héritage documentaire** : aucune source historique — l'EDP transitoire du puff est la suite directe de l'étape 6 (note 53). Aucun chiffre de l'ouvrage de 2008 n'est utilisé comme cible.
- **Reconstruction** : marche explicite FTCS en temps de la marginale transverse ∂Q/∂t = Ky ∂²Q/∂y² + Kz ∂²Q/∂z², avec K = (u/2)·dσ²/dx évalué à la distance parcourue d = u·t ; entrée fermée au premier instant de passage, miroir au sol, Dirichlet aux bords ; structure longitudinale analytique (carte travel-time de la note 37, isotropie σx = σy du noyau fermé).
- **Extension** : seconde extension conditionnelle du [contrat minimal](47-contrat-minimal-baseline.md) §5 — la source impulsionnelle (note 53) reçoit sa route EDP transitoire, hors périmètre de la baseline continue.

## 2. Méthodologie (quatre étapes)

1. **Marginale transverse** (cf. lexique) : Q(y, z, t) = ∫ C(x, y, z, t) dx vérifie l'EDP de diffusion 2D en temps (le vent uniforme transporte, la diffusion transverse étale) ; K = (u/2)·d
σ²/dx à la distance parcourue d = u·t.
2. **Entrée fermée** : au premier instant de passage (t_e = 100/u), la marginale analytique du package est posée sur la grille ; bords latéraux et sommet mis à zéro (Dirichlet, cf. lexique).
3. **Marche FTCS** (schéma explicite, cf. lexique) : pas de temps t_e/2^k (k = 10 sur la grille fine, nombre de Fourier 0,235 au dernier passage ≤ 1/3) ; sol miroir (Neumann — exact car le noyau du puff est pair en z) ; instantanés prélevés aux instants de passage (pas 1024/3072/7168).
4. **Comparaison dirigée** : C(x, y, z, t) = Q(y, z, t)·exp(−(x − x0 − u·t)²/2σx²)/(√(2π)σx), σx = σy (isotropie, cf. lexique) ; les points du cas S0 sont aux arcs, où le facteur gaussien longitudinal est évalué au passage.

## 3. Paramètres

| Paramètre | Valeur |
|---|---|
| Puff | masse 1,0 kg, vent 3,0 m s⁻¹, classe C, x0 = 0 (note 53) |
| Grille fine | pas 2,5 m / 2,0 m, fenêtre 340 m / 240 m (273 × 121 nœuds) |
| Grille grossière | pas 5,0 m / 4,0 m, fenêtre 340 m / 240 m (137 × 61 nœuds) |
| Pas de temps fin | (100/3)/1024 s ≈ 3,26 × 10⁻² s, 7168 pas |
| Pas de temps grossier | (100/3)/256 s ≈ 1,30 × 10⁻¹ s, 1792 pas |
| Instants de passage | t = x/u : 33,3 / 66,7 / 133,3 / 266,7 s (arcs 100/200/400/800 m) |
| Grille de prélèvements | 12 points du cas S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2) |

## 4. Résultats

### 4.1 Grille fine

- **NMSE ≈ 3,4 × 10⁻⁵** (< 10⁻⁴) et **FAC2 = 1,0** — les deux métriques du lexique, aux seuils préenregistrés du registre ([note 39](39-squelette-benchmarks-s0.md) §3).
- **Écart relatif maximal ≈ 5,9 × 10⁻³** (arc 100, entrée partagée : pur effet de l'interpolation bilinéaire en z) ; arcs 200–800 : écarts ≤ 6,5 × 10⁻⁴.
- **Écarts de masse** vs marginale analytique sur la même grille : 0 à l'entrée, ~10⁻¹⁶ à 200 s, ~2 × 10⁻¹⁴ à 400 s, −1,1 × 10⁻⁴ à 800 s (troncature de la fenêtre 4σ).

### 4.2 Grille grossière (contrôle de convergence)

- **NMSE ≈ 7,5 × 10⁻⁴** : environ **22 fois** la grille fine — le même taux de convergence que l'étape 5 ; écart relatif maximal ≈ 2,8 × 10⁻².

## 5. Limites explicites

**Établit** : la cohérence interne du package entre la marche FTCS en temps de la marg
inale transverse et la solution fermée du puff, sur le cas S0 figé.

**N'établit pas** : une validation physique (cas synthétique) ; une résolution numérique de la structure longitudinale (analytique : carte travel-time + isotropie du noyau fermé) ; le traitement du noyau symétrique en z autour du sol (moitié de la masse du noyau fermé formellement sous le sol ; la grille porte la demi-colonne miroir et les écarts de masse comparent la marginale analytique sur la même grille) ; une physique de l'isotropie σx = σy (portée par la solution fermée du package).

## 6. Relations au code

| Objet du dépôt | Rôle |
|---|---|
| [experiences/transitoire_puff/marginale.py](../src/jdriftx/experiences/transitoire_puff/marginale.py) | Marginale fermée et bilan de masse sur la grille : condition d'entrée du schéma, référence des écarts de masse |
| [experiences/transitoire_puff/solveur.py](../src/jdriftx/experiences/transitoire_puff/solveur.py) | Géométrie des passages et schéma FTCS marché en temps : instants, solution transitoire |
| [experiences/transitoire_puff/routes.py](../src/jdriftx/experiences/transitoire_puff/routes.py) | Routes mesurées séparément, chacune rendant sa mesure typée (assemblables), structure longitudinale injectable (protocole PEP 544) |
| [experiences/transitoire_puff/comparaison.py](../src/jdriftx/experiences/transitoire_puff/comparaison.py) | Modèles gelés, assemblage des métriques (`assembler_comparaison`), manifeste étiqueté |
| [tests/test_transitoire_puff.py](../tests/test_transitoire_puff.py) | 19 tests GWT : calibration, entrée partagée, seuils, convergence, rejets, temps dirigé, coûts, assemblage des routes, manifeste, export JSON, injectabilité |
| [experiences/reference_independante.py](../src/jdriftx/experiences/reference_independante.py) | Grille EDP et modèle de diffusion injectable (étape 5) ; échantillonneur bilinéaire et pas longitudinal stable réutilisés par la marche en temps |
| [experiences/evaluation_puff.py](../src/jdriftx/experiences/evaluation_puff.py) | Source impulsionnelle et temps dirigé (étape 6) |
| [similitude.py](../src/jdriftx/similitude.py) | Solution fermée du puff et σ de Briggs |

**Écarts explicites : aucun** vis-à-vis des notes 47, 48, 49 et 53 ; les statuts figés ne sont pas modifiés.

## 7. Architecture du package et justifications

Le package sépare les considérations, une par module : une extension (nouveau modèle de diffusion, nouvelle structure longitudinale, nouveau format de manifeste) touche un seul fichier, et la façade `__init__.py` re-exporte l'API publique pour que l'import historique `jdriftx.experiences.transitoire_puff` reste stable.

- **Interfaces injectables (PEP 544).** `ModeleDiffusion` ([note 51](51-reference-independante-cas-s0.md)) et `StructureLongitudinale` sont des protocoles à typage structurel, la règle du package depuis `ChampPlan` et les contrats de la [note 42](42-contrats-interoperabilite.md) : le point d'extension de S0-b (cisaillement) s'exprime comme une structure alternative, sans toucher aux routes ni au solveur ; les tests d'injectabilité prouvent que le point d'extension est effectif (structure doublée → valeurs EDP exactement doublées, marginale inchangée).
- **Réutilisations bit-exact.** Le pas de temps est le pas longitudinal stable de l'étape 5 divisé par u (même nombre de Fourier, même exposant k) ; l'échantillonnage bilinéaire et le bilan d'intégrale réutilisent `EchantillonneurBilineaire` : la route EDP ne duplique ni interpolation ni choix de pas — une seule définition, deux consommateurs.
- **Mesures typées assemblables.** Chaque route rend sa mesure (`MesureFermeePuff`, `MesureEdpPuff`) ; `comparer_transitoire` orchestre les deux routes, `assembler_comparaison` assemble les mesures en métriques pures. Choix négatif justifié : pas de protocole de route générique — les retours sont distincts par nature (noyau fermé ponctuel contre solution complète portant les écarts de masse), un contrat unique serait artificiel ; l'échangeabilité est portée par les mesures assemblables, pas par une fausse interface commune.
- **Immuabilité et frontière JSON.** Dataclasses gelées et modèles Pydantic gelés ; les `dict` restent confinés à la frontière d'export JSON (`model_dump`), conformément à la charte du projet ([note 22](22-audit-package-code.md)).

## Références

- Interne : [évaluation dirigée du puff](53-evaluation-puff-source-impusionnelle.md) ; [comparaison à référence indépendante](51-reference-independante-cas-s0.md) ; [cas de référence autonome](48-cas-reference-autonome-ecoulement-uniforme.md) ; [carte travel-time](37-transformation-tau-eta-cas-uniforme.md) ; [deux résolutions indépendantes et coûts mesurés](35-figure-03-modele-reduit-edp.md) ; [contrats d'interopérabilité PEP 544](42-contrats-interoperabilite.md) ; [squelette de benchmarks et registre des métriques](39-squelette-benchmarks-s0.md) ; [standards qualité des tests](40-standards-qualite-tests-proprietes.md).
- Standards : [PEP 544 — protocoles à typage structurel](https://peps.python.org/pep-0544/) ; métriques FAC2/NMSE du registre partagé ([issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)).
- Suivi : [issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232) ; source étiquetée : Brun & Mohammadi (2008), [DOI 10.1007/978-1-4020-8758-5_14](https://doi.org/10.1007/978-1-4020-8758-5_14).
