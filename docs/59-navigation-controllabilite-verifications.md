# 59 — Navigation de Zermelo : vérifications numériques et régime supercritique

Note du 1er novembre 2026, suite à l'issue #437 (formalisation Finsler/Zermelo de la
métrique travel-time). Elle documente : (1) l'explication pas à pas de la preuve du
théorème S0 publié sur la page du site `site/theorie/navigation-fronts-controllabilite.qmd` ;
(2) ses corollaires ; (3) le régime supercritique et le cône d'accessibilité ajoutés à
cette page ; (4) le protocole de vérification numérique et son mapping vers
`tests/test_navigation_controllabilite.py`. Aucun module `src/` n'est concerné.

## 1. Objet et périmètre

La page du site publie, pour le puff gaussien tridimensionnel en espace libre, vent
uniforme constant, vitesse de contrôle égale à la vitesse d'expansion `c(t) = R'(t)`
du rayon d'isoconcentration : l'ensemble atteignable exact
`R(t) = B(x₀ + ut, R(t))`, le théorème `T_nav = T_front`, l'équation de
Hamilton–Jacobi du front de contrôlabilité et la forme de Randers de la jauge
sous-critique. Cette note vérifie, développe et explicite ces résultats, puis traite
le régime complémentaire `|u| ≥ c`, absent de la page initiale. Tout ce qui suit
concerne le modèle mathématique posé ; aucune validité physique n'est établie.

## 2. La preuve du théorème S0, expliquée pas à pas

**Énoncé** (page §3.2) : pour une cible fixe `x_B ≠ x₀`,
`T_nav = T_front`, où `T_nav` est l'infimum des instants où une trajectoire
admissible atteint la cible, et `T_front` l'infimum des instants où la cible
appartient à la boule `B(x₀ + ut, R(t))`.

**Idée directrice : changer de référentiel.** Dans le référentiel co-mobile du
centre du puff, `y(t) = X(t) − x₀ − ut`, la navigation s'écrit

`dy/dt = s(t)`,  `‖s(t)‖ ≤ R'(t)`  presque partout,

c'est-à-dire **sans vent** : le vent a disparu dans le changement de variable, il ne
reste qu'une contrainte de vitesse dont la borne ne dépend **que du temps**. C'est
cette propriété qui rend le problème exactement soluble.

- **Étape 1 (inclusion directe).** Toute trajectoire admissible vérifie
  `‖X(t) − x₀ − ut‖ = ‖∫₀ᵗ s(τ)dτ‖ ≤ ∫₀ᵗ R'(τ)dτ = R(t) − R(0+) = R(t)`,
  car `R(0+) = 0`. L'ensemble atteignable est inclus dans la boule fermée.
- **Étape 2 (inclusion réciproque).** Toute position `z` de la boule est atteinte
  par la commande **à cap constant** `s(τ) = (z/R(t))·R'(τ)` : elle est mesurable,
  respecte la borne partout, et son intégrale vaut exactement `z`, car
  `∫₀ᵗ R'(τ)dτ = R(t)`. Le cap constant suffit : la borne étant purement
  temporelle, répartir la vitesse selon une direction fixe dans le repère
  co-mobile exploite tout le budget de déplacement `R(t)`.
- **Étape 3 (égalité des infimums).** Les deux définitions réduisent la même
  condition : `x_B` est atteignable à l'instant `t` si et seulement si
  `‖x_B − x₀ − ut‖ ≤ R(t)`. Les ensembles d'instants coïncident, donc leurs
  infimums sont égaux. Pour une cible initialement extérieure, le premier contact
  est sur la frontière par continuité.

**Pourquoi la preuve est conditionnelle.** (i) La borne `R'(t)` n'est positive que
sur la phase d'expansion `0 < t ≤ t*` ; (ii) `R'(t) → +∞` en `t → 0+` : la
singularité est **intégrable** (`∫₀ᵗ R' = R(t) < ∞`) mais la classe des contrôles
est « mesurable, à borne ponctuelle », pas `L∞` ; (iii) la cible est fixe ; (iv) le
vent est uniforme — sinon le centre advecté n'est plus commun à toutes les
trajectoires. Chaque relâchement est une extension ouverte, listée page §4.

## 3. Corollaires

1. **Diagnostic d'hétérogénéité.** Sur S0, l'écart entre le temps de navigation
   optimal et le temps d'arrivée du modèle dirigé est identiquement nul. Cet écart
   ne peut donc naître que de l'hétérogénéité (relief, cisaillement) : c'est un
   observable quantitatif du quatrième objet, à mesurer après exécution du
   benchmark de coûts (issue #232/#244).
2. **Singularité initiale et borne de validité.** `c(t) → ∞` en `t → 0+` traduit
   le régime de diffusion instantanée, hors domaine de validité de l'approximation
   diffusive. Toute utilisation physique du quatrième objet exige une borne
   inférieure `t_min` de validité — à inscrire dans les hypothèses du catalogue,
   pas dans le code.
3. **Cap constant, pas poursuite.** Quand `c(t) < ‖u‖`, la poursuite directe de la
   cible co-mobile échoue (la cible fuit à la vitesse `‖u‖`) alors que le cap
   constant atteint : la trajectoire optimale vise le point de coïncidence futur.
   C'est le pont vers l'équation de Zermelo `dθ/dt` en champ cisaillé, où les
   géodésiques se courbent pour chercher les vents favorables.

## 4. Régime supercritique et cône d'accessibilité

La forme de Randers (page §6) exige `A = c² − ‖u‖² > 0`. Le régime complémentaire
`‖u‖ ≥ c` — le régime usuel de la dispersion atmosphérique, où l'advection domine
la propagation relative — donne une jauge non définie dans toutes les directions.

Pour une borne isotrope **constante** `c` et un vent uniforme `u`, un déplacement de
direction `ω` est atteignable si et seulement si le rayon `{λω : λ > 0}` rencontre
une boule `B(ut, ct)`. La distance de `u` à ce rayon vaut `‖u‖·sin θ` (θ = angle
avec `u`), d'où la condition exacte :

`sin θ ≤ c/‖u‖` — les directions atteignables forment le **cône d'accessibilité**
d'axe `u`, de demi-angle `arcsin(c/‖u‖)`. Pour une direction intérieure, le temps
minimal de navigation admet la forme fermée

`T(d x) = ‖d x‖ / (ω·u + √((ω·u)² + c² − ‖u‖²))`,

lorsque le dénominateur est strictement positif ; hors du cône, `T = +∞` par
convention. Sur l'axe aval, `T = ‖d x‖/(‖u‖ + c)`.

**Lecture géométrique de la non-symétrie amont.** Le cône borne les directions
atteignables : remonter le vent est impossible dès que `c ≤ ‖u‖`. La convention
`T = +∞` hors du cône est la contrepartie ensembliste de la non-symétrie amont
`τ(B, A) = +∞` testée sur la métrique travel-time. **Statut** : dérivation exacte
pour la borne isotrope constante ; le cas `c(t)` instationnaire supercritique
(l'équivalent de la jauge du puff) reste ouvert.

## 5. Protocole de vérification numérique — mapping tests

Toutes les vérifications ont été exécutées avant figeage (sandbox équivalent,
float64) puis transcrites dans `tests/test_navigation_controllabilite.py` :

| Affirmation | Test | Tolérance observée |
|---|---|---|
| Front d'isoconcentration exact (`C = C₀` sur `R(t)`) | `test_le_front_d_isoconcentration_est_exact` | rel 1e-12 |
| `c(t) = R'(t)` (dérivée centrale) | `test_la_vitesse_d_expansion_est_la_derivee_du_rayon` | rel 1e-8 |
| `t*` maximise `R` ; `Λ(e·t*) = 0` | `test_t_etoile_maximise_le_rayon` | abs 1e-9 |
| Singularité intégrable (`∫₁¹⁰⁰ c = R(100) − R(1)`) | `test_la_singularite_initiale_est_integrable` | rel 1e-6 |
| Théorème S0 : trajectoire à cap constant atteint la cible à `T_front` exactement | `test_le_theoreme_s0_egalise_navigation_et_front` | abs 1e-9, ODE 1e-6 |
| Cible hors de portée : aucun contact sur `(0, t*]` | `test_une_cible_hors_de_portee_n_est_jamais_atteinte` | balayage 20 000 points |
| Jauge = forme de Randers (sous-critique), homogénéité, axe aval | `test_la_jauge_sous_critique_est_une_randers` | rel 1e-12 |
| Cône `arcsin(c/‖u‖)` : frontière exacte, `+∞` hors cône et amont | `test_le_regime_supercritique_definit_un_cone` | frontière 1e-9 rad |
| Équation HJ du front : résidu de `φ_t + u·∇φ + c|∇φ|` | `test_le_front_satisfait_l_equation_hamilton_jacobi` | abs 1e-6 |
| Eikonale stationnaire `u·∇T + c|∇T| = 1` | `test_l_eikonale_stationnaire_en_champ_uniforme` | abs 1e-6 |

Paramètres du modèle : `M = 10⁶`, `K = 0,5`, `C₀ = 1`, `u = (2, 0, 0)` ; cibles
`(120, 20, 0)`, `(80, 0, 0)`, `(120, 30, 0)` (hors de portée). Chaque test
documente dans sa docstring ce qu'il établit et sous quelles hypothèses.

## 6. Statuts, limites et suites

**Démontré** (page + cette note) : ensemble atteignable exact et théorème S0 sous
les hypothèses posées ; équations HJ/eikonale ; jauge de Randers sous-critique ;
cône d'accessibilité supercritique à borne constante.

**Non démontré** (extensions ouvertes) : vent spatialement variable ; cible mobile ;
départ à âge positif (rayon atteignable `R(t) − R(t₀)` ≠ rayon du front) ; phase de
contraction `t > t*` ; classe de contrôles `L∞` ; équivalence front de
contrôlabilité ↔ front d'une EDP d'advection–diffusion générale ; jauge
supercritique instationnaire. Le traitement du cisaillement (S0-b) reste une
extension gelée : déclenchement propriétaire uniquement, injecteurs déjà
identifiés (ModèleDiffusion OU StructureLongitudinale).

## 7. Références vérifiées (1er novembre 2026, avant toute écriture)

1. Zermelo, « Über das Navigationsproblem bei ruhender oder veränderlicher
   Windverteilung als mathematisches Problem », Z. Angew. Math. Mech. **11
   (1931) 114–124**.
2. Randers, « On an Asymmetrical Metric in the Four-Space of General Relativity »,
   Phys. Rev. **59**, 195–199 (15 janvier 1941), DOI 10.1103/PhysRev.59.195.
3. Bao, Robles & Shen, « Zermelo navigation on Riemannian manifolds »,
   J. Differential Geom. **66 (3)**, 377–435, mars 2004 ; arXiv math/0311233.
   (Année corrigée par rapport à la première proposition : 2004, pas ~2000.)
4. Bao, Chern & Shen, « An Introduction to Riemann-Finsler Geometry », Springer,
   GTM 200, DOI 10.1007/978-1-4612-1268-3. (Auteurs corrigés : Bao–Chern–Shen.)
5. Shen, « Lectures on Finsler Geometry », World Scientific, 2001,
   ISBN 9810245300 / 978-981-024530-6.
6. Sethian, « A fast marching level set method for monotonically advancing
   fronts », PNAS **93 (4)**, 1591–1595 (1996), DOI 10.1073/pnas.93.4.1591.
7. Sethian & Vladimirsky, « Ordered upwind methods for static Hamilton–Jacobi
   equations », PNAS **98** (2001), DOI 10.1073/pnas.201222998.

Les sept références sont authentiques ; les deux corrections de notice ont été
appliquées avant figeage, conformément à l'audit anti-hallucinations d'octobre 2026.
