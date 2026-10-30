# 51 — Comparaison à référence indépendante du cas S0

**Statut.** Note d’expérience exécutant l’étape 5 de l’ordre confirmé de l’[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : reconstruire une route de calcul indépendante de la solution de similitude — une équation de diffusion marchée en longitude — et la comparer à la solution fermée du package sur le cas de référence S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2), avec les métriques préenregistrées et les coûts mesurés séparément. Implémentation : [experiences/reference_independante.py](../src/jdriftx/experiences/reference_independante.py) ; tests : [tests/test_reference_independante.py](../tests/test_reference_independante.py). La méthodologie des deux résolutions indépendantes suit la [note 35](35-figure-03-modele-reduit-edp.md).

**Date :** 29 octobre 2026. **Suivi :** [issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) (étape 5 sur 6) ; étiquetage héritage/reconstruction/extension conformément au [contrat minimal](47-contrat-minimal-baseline.md) §3.4.

## 1. Objectif et étiquetage

- **Héritage documentaire** : la comparaison à référence indépendante est « annoncée seulement » dans le chapitre « Reduced-Order Modelling of Dispersion » (Brun & Mohammadi, 2008, DOI 10.1007/978-1-4020-8758-5_14, figure 3). Aucun chiffre de l’ouvrage n’est utilisé comme cible.
- **Reconstruction** : résolution d’une EDP de diffusion transverse/verticale marchée en longitude, schéma explicite FTCS, sous les hypothèses du cas uniforme ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.1).
- **Extension** : aucune (source impulsionnelle et champ multi-niveaux restent des extensions conditionnelles, [contrat](47-contrat-minimal-baseline.md) §5).

## 2. Méthodologie (note 35)

Dans le cas uniforme, l’EDP de transport-diffusion se réduit à une diffusion transverse et verticale marchée en longitude :

~~~text
∂C/∂x = (1/2) · dσ_y²/dx · ∂²C/∂y² + (1/2) · dσ_z²/dx · ∂²C/∂z²
~~~

avec K_y = (U/2)·dσ_y²/dx et K_z = (U/2)·dσ_z²/dx dans l’équation de transport U·∂C/∂x = K_y·∂²C/∂y² + K_z·∂²C/∂z² ; après division par U, les coefficients de l’équation marchée en x sont donc (1/2)·dσ²/dx, sans facteur 1/U supplémentaire. Contrôle dimensionnel : dσ²/dx est en mètres et ∂²C/∂y² en kg·m⁻⁵, donc le membre droit est en kg·m⁻⁴, comme ∂C/∂x. La paramétrisation vient de Briggs ([note 24](24-classes-stabilite-pasquill-objet.md), source unique de vérité). La forme fermée du panache gaussien ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.5) est la solution exacte de cette équation : les deux routes partagent la paramétrisation, et la comparaison contrôle la route de diffusion — pas la physique ni l’entrée.

Choix numériques, tous étiquetés « reconstruction » :

- **Schéma** : FTCS explicite en longitude (forward en x, centré en y et z), coefficient de diffusion évalué au milieu du pas ; nombre de Fourier borné à 1/3 (somme des deux directions), évalué au dernier arc là où σ² croît le plus ; pas longitudinal 100/2^k, k choisi minimal pour la stabilité.
- **Conditions aux limites** : miroir au sol (Neumann, ∂C/∂z = 0 par réflexion), Dirichlet nul aux bords latéraux et au sommet de la fenêtre ; fenêtre couvrant quatre écarts-types au dernier arc (troncature documentée).
- **Entrée partagée** : la condition d’entrée à x = 100 m est la solution fermée du package évaluée sur la grille — la route EDP diffuse cette entrée, elle ne la recalcule pas. Le test d’entrée vérifie l’identité exacte avec le contrat partagé.
- **Prélèvement** : tranches prélevées aux arcs de mesure, interpolation bilinéaire aux 12 points de la grille du cas.

## 3. Frontière de substitution du solveur

La route `RouteEdp` dépend désormais du protocole structurel `SolveurDeReference`
(`resoudre() -> SolutionEdp`), et non directement de la classe FTCS. Le
`SolveurEdp` actuel reste le solveur par défaut ; un solveur alternatif peut
être injecté sans modifier l'échantillonnage ni l'assemblage de la mesure. Le
solveur accepte aussi une condition initiale injectable via le contrat
`ModeleConcentration` ; le panache gaussien partagé reste le défaut. La forme
et la finitude du champ retourné sont contrôlées à cette frontière.

Cette substituabilité est une frontière logicielle, pas une validation
numérique automatique. Un solveur injecté doit respecter les invariants de
`SolutionEdp` : mêmes coordonnées de grille, tranches correspondant aux
abscisses des points demandés, unités et convention d'indexation. Ses
conditions initiales, conditions aux limites, stabilité, conservation et
convergence doivent faire l'objet de tests propres à sa méthode. La comparaison
scientifique documentée dans cette note reste celle du FTCS par défaut ; un
autre solveur ne doit pas être présenté comme équivalent sans étude dédiée.

## 4. Paramètres numériques (grille fine, calibrée)

| Paramètre | Valeur | Justification |
|---|---|---|
| Pas transverse Δy | 2,5 m | multiple de la demi-largeur |
| Pas vertical Δz | 2,0 m | multiple de la hauteur |
| Demi-largeur | 340 m | ≥ 4σ_y(800 m) = 338,7 m |
| Hauteur de colonne | 240 m | ≥ H + 4σ_z(800 m) = 238,7 m |
| Pas longitudinal Δx | 100/1024 ≈ 0,0977 m | plus grand 100/2^k stable |
| Nombre de Fourier à 800 m | 0,225 | ≤ 1/3 (seuil FTCS) |
| Pas de marche | 7 168 | de 100 m à 800 m |
| Grille | 273 × 121 | 33 033 nœuds par tranche |

Grille grossière de contrôle (pas doublés en transverse et vertical) : Δy = 5 m, Δz = 4 m, Δx = 100/256 m, 1 792 pas, grille 137 × 61, nombre de Fourier inchangé.

## 5. Résultats

### 4.1 Comparaison ponctuelle (12 points, z = z_m = 1,5 m)

| Arc (m) | y (m) | Fermée (kg m⁻³) | EDP (kg m⁻³) | Ratio |
|---|---|---|---|---|
| 100 | −50 | 7,018 × 10⁻⁸ | 6,978 × 10⁻⁸ | 0,99423 |
| 100 | 0 | 2,386 × 10⁻³ | 2,372 × 10⁻³ | 0,99423 |
| 100 | +50 | 7,018 × 10⁻⁸ | 6,978 × 10⁻⁸ | 0,99423 |
| 200 | −50 | 4,427 × 10⁻⁵ | 4,427 × 10⁻⁵ | 1,00008 |
| 200 | 0 | 6,168 × 10⁻⁴ | 6,172 × 10⁻⁴ | 1,00064 |
| 200 | +50 | 4,427 × 10⁻⁵ | 4,427 × 10⁻⁵ | 1,00008 |
| 400 | −50 | 8,147 × 10⁻⁵ | 8,145 × 10⁻⁵ | 0,99971 |
| 400 | 0 | 1,595 × 10⁻⁴ | 1,595 × 10⁻⁴ | 1,00017 |
| 400 | +50 | 8,147 × 10⁻⁵ | 8,145 × 10⁻⁵ | 0,99971 |
| 800 | −50 | 3,541 × 10⁻⁵ | 3,541 × 10⁻⁵ | 0,99996 |
| 800 | 0 | 4,215 × 10⁻⁵ | 4,215 × 10⁻⁵ | 0,99998 |
| 800 | +50 | 3,541 × 10⁻⁵ | 3,541 × 10⁻⁵ | 0,99996 |

La symétrie latérale est exacte à la précision machine (le schéma préserve l’identité des colonnes ±y). Au premier arc, l’écart (0,58 %) vient de la seule interpolation verticale — l’entrée y est la forme fermée elle-même.

### 4.2 Métriques préenregistrées ([note 39](39-squelette-benchmarks-s0.md) §3)

- **FAC2 = 1,0** : les 12 prédictions sont dans un facteur 2.
- **NMSE = 3,10 × 10⁻⁵** (dénominateur Σ(vérité)²).
- **Écart relatif maximal = 0,58 %** (arc 100, interpolation verticale).
- **Flux transverse** : le flux U·∫∫C dy dz vaut le débit Q = 2,0 kg s⁻¹ à l’entrée ; déficit maximal 2,28 × 10⁻⁴ au dernier arc (troncature à 4σ), nul aux arcs intermédiaires à la précision machine.

### 4.3 Contrôle de convergence

Grille grossière : NMSE = 6,89 × 10⁻⁴, écart relatif maximal 2,72 %, FAC2 = 1,0. Affiner la grille (pas doublés en transverse/vertical, pas longitudinal divisé par 4) réduit l’erreur d’un facteur ≈ 22, cohérent avec l’ordre du schéma et l’interpolation bilinéaire.

## 6. Coûts (mesurés séparément, sans facteur historique)

Conformément à la [note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §3, les coûts des deux routes sont mesurés séparément au runtime (`perf_counter`) et exportés dans le manifeste `jdriftx-reference-independante-001` : coût de la route fermée (les 12 évaluations vectorisées) et coût de la route EDP (résolution complète puis interpolation), en secondes, machine-dépendants. Comptes déterministes du schéma, indépendants de la machine : la route fermée évalue 12 points en une passe vectorisée ; la route EDP met à jour environ 2,4 × 10⁸ cellules (7 168 pas × 33 033 nœuds). Le facteur historique 10³–10⁴ n’est ni reconstruit ni revendiqué.

## 7. Limites explicites — ce que la comparaison établit et n’établit pas

**Établit** : la cohérence interne du package entre la paramétrisation Briggs, la solution fermée et une route de diffusion numériquement indépendante (marche en x, conditions aux limites, interpolation) ; la conservation du flux aux seuils de troncature ; la convergence du schéma.

**Frontières non couvertes par cette architecture** : le solveur FTCS de cette note ne consomme pas le contrat `Vent` ni le contrat `Relief`. Il résout l'équation marchée en longitude sous l'hypothèse d'un écoulement uniforme, avec la paramétrisation Briggs et un sol plan représenté par la condition miroir en z = 0. Injecter un autre vent ou un relief dans ces interfaces ne modifierait pas cette équation et ne constituerait donc pas un modèle de transport sur terrain complexe. Ce cas nécessitera un opérateur d'advection-diffusion adapté, des conditions aux limites cohérentes avec le terrain et des validations indépendantes.

**N’établit pas** : une validation physique (cas synthétique, [note 21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md)) ; une vérification de la formule gaussienne elle-même — l’entrée est partagée et la paramétrisation est commune, donc une erreur conceptuelle commune aux deux routes resterait invisible ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §4) ; les formes INVERSE de σ_z (classes E et F) sont hors périmètre et rejetées explicitement ; le facteur historique 10³–10⁴ n’est pas revendiqué.

## 8. Relations au code

| Objet du dépôt | Rôle |
|---|---|
| [experiences/reference_independante.py](../src/jdriftx/experiences/reference_independante.py) | Module étape 5 : résolution EDP, protocole `SolveurDeReference`, condition initiale injectable, comparaison, manifeste étiqueté |
| [tests/test_reference_independante.py](../tests/test_reference_independante.py) | 19 tests GWT : calibrage, symétrie, convergence, entrée partagée, export JSON |
| [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py) | Cas S0 figé, grille et vérité (route fermée) |
| [benchmarks/metriques.py](../src/jdriftx/benchmarks/metriques.py) | FAC2/NMSE préenregistrées, conventions inchangées |
| [similitude.py](../src/jdriftx/similitude.py), [stabilite.py](../src/jdriftx/stabilite.py) | Paramétrisation partagée (σ, coefficients Briggs) |
| [contrats.py](../src/jdriftx/contrats.py) | Entrée partagée (PanacheGaussien, contrat de concentration) |

**Écarts explicites : aucun** vis-à-vis des notes 47, 48 et 49 ; les statuts figés ne sont pas modifiés.

## Références internes

- [Cas de référence autonome](48-cas-reference-autonome-ecoulement-uniforme.md) ; [contrat minimal de la baseline](47-contrat-minimal-baseline.md) ; [matrice des revendications](49-matrice-revendications-baseline.md)
- [Modèle réduit vs EDP : deux résolutions indépendantes](35-figure-03-modele-reduit-edp.md)
- [Squelette de benchmarks S0](39-squelette-benchmarks-s0.md) ; [classes de stabilité](24-classes-stabilite-pasquill-objet.md)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232) ; [issue #43 — critères](https://github.com/JM-Brun/J-DriftX/issues/43)
