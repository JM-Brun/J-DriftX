# 59 — Navigation de Zermelo : vérifications numériques et régime supercritique

Note du 1er novembre 2026, suite à l'issue #437 (formalisation Finsler/Zermelo de la
métrique travel-time). Elle documente : (1) l'explication pas à pas de la preuve du
théorème GZ-1 publié sur la page du site `site/theorie/navigation-fronts-controllabilite.qmd` ;
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

## 2. La preuve du théorème GZ-1, expliquée pas à pas

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

1. **Ne pas confondre les temps.** GZ-1 établit uniquement `T_nav = T_front`.
   Il ne démontre pas `T_nav = T_arr` : `T_arr` désigne une première arrivée passive,
   tandis que `T_nav` minimise un temps sous contrôle et `T_front` mesure le premier
   contact avec l'isoconcentration. Aucun écart entre ces objets ne peut être
   attribué au relief ou au cisaillement à partir de GZ-1 seul. Une comparaison
   exige des définitions opérationnelles communes et un benchmark distinct.
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

Pour une borne isotrope **constante** `c` et un vent uniforme `u`, un déplacement
`dω` (`d > 0`, `‖ω‖ = 1`) est atteignable s'il existe `t > 0` tel que
`‖dω − ut‖ ≤ ct`. Posons `q = d/t > 0` et divisons par `t` :

`q² − 2q(u·ω) + ‖u‖² − c² ≤ 0`.

Cette quadratique possède une racine positive si et seulement si `u·ω > 0` et
`Δ = (u·ω)² + c² − ‖u‖² ≥ 0`. En notant `θ` l'angle avec `u`, cela donne le
**cône aval** : `u·ω > 0` et `sin θ ≤ c/‖u‖`. La seule condition sur le sinus
serait insuffisante : elle sélectionnerait aussi un cône amont autour de `−u`.

La frontière `sin θ = c/‖u‖` est incluse : la droite issue de l'origine est tangente
à la boule mobile en un point strictement positif. La plus grande racine
`q₊ = u·ω + √((u·ω)² + c² − ‖u‖²)` maximise `q = d/t`, donc minimise le temps :

`T(dω) = d / (u·ω + √((u·ω)² + c² − ‖u‖²))`.

Hors du cône aval, `T = +∞` par convention. Sur l'axe aval,
`T = d/(‖u‖ + c)`.

**Lecture géométrique de la non-symétrie amont.** Le cône borne les directions
atteignables : remonter le vent est impossible dès que `c ≤ ‖u‖`. La convention
`T = +∞` hors du cône est la contrepartie ensembliste de la non-symétrie amont
`τ(B, A) = +∞` testée sur la métrique travel-time. **Statut** : dérivation exacte
pour la borne isotrope constante ; le cas `c(t)` instationnaire supercritique
(l'équivalent de la jauge du puff) reste ouvert.

## 5. Fonction de valeur HJ : pourquoi le plateau nul est nécessaire

La fonction de distance signée `d_s(x,t) = ‖x − x₀ − ut‖ − R(t)` décrit
correctement le niveau zéro, mais elle n'est pas la solution de viscosité globale
associée à la donnée initiale ponctuelle `φ(x,0) = ‖x − x₀‖`. La solution de
Hopf–Lax est

`φ(x,t) = max(‖x − x₀ − ut‖ − R(t), 0)`.

La dérivation est constructive :

1. **Suivre le centre.** Avec `y = x − ut`, poser
   `ψ(y,t) = φ(y + ut,t)`. Le vent uniforme disparaît de l'équation :
   `ψ_t + c(t)‖∇ψ‖ = 0`.
2. **Cumuler la vitesse disponible.** Pendant `0 < t < t*`,
   `c(t) = R'(t) > 0` et `ρ = R(t) = ∫₀ᵗ c(τ)dτ`. La singularité de `c`
   en zéro est intégrable ; `ρ` est une variable temporelle strictement croissante.
3. **Réduire à l'éikonale standard.** En utilisant `ρ` comme temps,
   `ψ_ρ + ‖∇ψ‖ = 0`, avec `ψ(y,0) = ‖y − x₀‖`.
4. **Appliquer Hopf–Lax.** La formule
   `ψ(y,ρ) = inf_{‖y−z‖≤ρ} ‖z−x₀‖` donne
   `max(‖y−x₀‖−ρ, 0)`. Si la boule `B̄(y,ρ)` contient `x₀`, le minimum
   est zéro ; sinon, il vaut la distance de `x₀` à cette boule.

Le zéro de `φ` est toute la boule atteignable ; le front géométrique est sa
frontière. À l'intérieur, `φ` est exactement nul. La distance signée est
utilisable comme fonction de niveau réinitialisée, mais ne doit pas être présentée
comme la fonction de valeur HJ globale : elle échoue notamment au test de
supersolution au centre de la boule.

Le test numérique contrôle le résidu classique uniquement dans les régions
différentiables (extérieur et plateau intérieur). Le coin du front n'a pas de
gradient classique ; sa propriété de solution de viscosité découle de Hopf–Lax,
pas d'un résidu ponctuel calculé au coin. Cette preuve spécifique ne se transpose
pas automatiquement à `u(x,t)` ou `c(x,t)` variables.

## 6. Protocole de vérification numérique — mapping tests

Toutes les vérifications ont été exécutées avant figeage (sandbox équivalent,
float64) puis transcrites dans `tests/test_navigation_controllabilite.py` :

| Affirmation | Test | Tolérance observée |
|---|---|---|
| Front d'isoconcentration exact (`C = C₀` sur `R(t)`) | `test_le_front_d_isoconcentration_est_exact` | rel 1e-12 |
| `c(t) = R'(t)` (dérivée centrale) | `test_la_vitesse_d_expansion_est_la_derivee_du_rayon` | rel 1e-8 |
| `t*` maximise `R` ; `Λ(e·t*) = 0` | `test_t_etoile_maximise_le_rayon` | abs 1e-9 |
| Singularité intégrable (`∫₁¹⁰⁰ c = R(100) − R(1)`) | `test_la_singularite_initiale_est_integrable` | rel 1e-6 |
| Théorème S0 : trajectoire à cap constant atteint la cible à `T_front` exactement | `test_le_theoreme_gz1_egalise_navigation_et_front` | abs 1e-9, ODE 1e-6 |
| Cible hors de portée : aucun contact sur `(0, t*]` | `test_une_cible_hors_de_portee_n_est_jamais_atteinte` | balayage 20 000 points |
| Jauge = forme de Randers (sous-critique), homogénéité, axe aval | `test_la_jauge_sous_critique_est_une_randers` | rel 1e-12 |
| Cône aval : condition angulaire + `u·ω > 0`, frontière incluse, amont rejeté | `test_le_regime_supercritique_definit_un_cone` | frontière 1e-9 rad |
| Équation HJ : résidu Hopf–Lax dans les zones lisses ; coin traité analytiquement | `test_le_front_satisfait_l_equation_hamilton_jacobi` | abs 1e-6 |
| Eikonale stationnaire `u·∇T + c|∇T| = 1` | `test_l_eikonale_stationnaire_en_champ_uniforme` | abs 1e-6 |

Paramètres du modèle : `M = 10⁶`, `K = 0,5`, `C₀ = 1`, `u = (2, 0, 0)` ; cibles
`(120, 20, 0)`, `(80, 0, 0)`, `(120, 30, 0)` (hors de portée). Chaque test
documente dans sa docstring ce qu'il établit et sous quelles hypothèses.

## 7. Statuts, limites et suites

**Démontré analytiquement** (page + cette note) : ensemble atteignable exact et
théorème GZ-1 sous les hypothèses posées ; formule de Hopf–Lax dans le cas uniforme ;
jauge de Randers sous-critique ; cône d'accessibilité à borne constante.
Les tests numériques contrôlent la cohérence de certaines identités et de leur
implémentation ; ils ne constituent pas des preuves indépendantes.

**Non démontré** (extensions ouvertes) : vent spatialement variable ; cible mobile ;
départ à âge positif (rayon atteignable `R(t) − R(t₀)` ≠ rayon du front) ; phase de
contraction `t > t*` ; classe de contrôles `L∞` ; équivalence front de
contrôlabilité ↔ front d'une EDP d'advection–diffusion générale ; jauge
supercritique instationnaire. Le traitement du cisaillement (S0-b) reste une
extension gelée : déclenchement propriétaire uniquement, injecteurs déjà
identifiés (ModèleDiffusion OU StructureLongitudinale).

## 8. Références vérifiées (1er novembre 2026, avant toute écriture)

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
