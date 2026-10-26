# 26 — Investigation de l'adjoint du temps de transport dirigé (26/10/2026)

## 1. Objet et méthode

L'issue #42 liste l'adjoint parmi les propriétés visées du projet, avec la
consigne suivante dans son suivi : investigation de définition avant tout
test, sur le modèle de docs/19 pour le temps de parcours dirigé. Ce document
est cette investigation. Il précise ce que « adjoint » signifie pour ce dépôt,
dérive les gradients exacts disponibles dans l'état actuel du code, décrit
les tests qui les vérifient et cartographie honnêtement ce qui reste non
implémenté. Aucune capacité n'est revendiquée au-delà des gradients
effectivement testés.

## 2. Définition retenue

Trois acceptions du mot « adjoint » existent dans la littérature et doivent
être distinguées avant tout test :

1. **État adjoint d'un problème de contrôle optimal** : les multiplicateurs
   de Lagrange de l'équation de transport contrainte, solution d'un problème
   rétrograde couplé au modèle direct. Il présuppose un modèle direct complet
   (EDP discrétisée, conditions aux limites) : aucun n'est implémenté dans ce
   dépôt.
2. **Fonction d'influence (gradient)** : le gradient de la fonction coût
   évaluée par le code, par rapport à ses entrées (champ de vent, positions
   source et cible). C'est la seule acception opérationnelle aujourd'hui.
3. **Adjoint d'un schéma numérique** : la transcription rétrograde terme à
   terme d'un opérateur itératif, validée par test croisé adjoint-direct
   (produit scalaire d'une perturbation d'état et de la sortie adjointe).
   Les solveurs périodiques du dépôt en sont les candidats futurs.

Ce document et les tests associés couvrent l'acception 2 uniquement. La
« rigueur » d'un adjoint n'est pas une propriété physique comme la
conservation : c'est l'exactitude du gradient fourni, qui doit coïncider avec
la dérivée réelle de la fonction coût.

## 3. Référence uniforme : adjoint exact fermé

### 3.1 Dérivation

Le coût dirigé de la référence uniforme s'écrit, pour d = b - a et u non
nul :

tau(a, b, u) = (d.u) / (u.u).

Cette forme est exactement un produit scalaire :

tau = lambda . d, avec lambda = u / (u.u) = u_hat / |u|.

Le vecteur lambda, de direction u_hat et de norme 1/|u|, est le **vecteur
adjoint constant** de la référence uniforme : déplacer la cible b de db
change le coût d'exactement lambda . db, et ce globalement, puisque le coût
est linéaire en la position. Les gradients par rapport aux trois entrées
sont fermés :

d(tau)/db = lambda ;  d(tau)/da = -lambda ;

grad_u tau = d / (u.u) - 2 (d.u) u / (u.u)^2.

La dernière formule est la dérivée du quotient de (d.u) par (u.u) : le
numérateur contribue d/(u.u), le dénominateur -2 (d.u) u/(u.u)^2.
Vérification d'homogénéité : chaque terme est en m / (m^2 s^-2) = s^2/m,
les unités attendues d'une dérivée de secondes par rapport à (m/s).

Interprétations utiles :

- déplacer la cible de 1 m selon la direction du vent allonge le temps de
  1/|u| secondes, exactement ;
- la composante du gradient le long du vent vaut -tau/|u| : renforcer le
  vent dans sa propre direction diminue le coût, à angle de d fixé.

### 3.2 Domaine de validité

Ces formules valent sur le demi-plan aval ouvert {d.u > 0}. La borne
transversale d.u = 0 n'est pas un point de dérivabilité : le coût y vaut
zéro par la convention locale, mais saute à +inf dès que d.u < 0. Le
gradient n'y est pas défini ; c'est une limite de la convention +inf, pas
du calcul différentiel. Tout usage futur du gradient dans une assimilation
devra décider explicitement du traitement de cette frontière (domaine
strict, régularisation, ou coût pénalisé).

### 3.3 Tests : validation croisée par différences finies

Quatre tests Given/When/Then ajoutés à tests/test_metric.py (aucune ligne
de code de production modifiée) :

1. test_uniform_pseudodistance_is_adjoint_vector_dot_displacement
   (paramétré, 3 configurations) : l'identité tau = lambda . d est
   restituée à la précision machine près ;
2. test_uniform_pseudodistance_gradient_wrt_wind_matches_analytic
   (paramétré, 3 configurations) : différences finies centrées contre la
   formule fermée grad_u tau ;
3. test_uniform_pseudodistance_gradient_wrt_points_is_adjoint_vector :
   d(tau)/db = lambda et d(tau)/da = -lambda par différences finies ;
4. test_1d_first_arrival_gradient_matches_closed_form : gradient exact du
   cas 1D (section 4).

Calibration (effectuée avant l'écriture des tests, sur les mêmes
configurations) : pas central h = 1e-5 ; erreur maximale mesurée entre
différences finies et formules analytiques : 2,5e-9 en absolu (erreur de
troncature O(h^2) et d'annulation epsilon_machine . tau / h). Tolérances
retenues : 1e-6 (absolu et relatif), marge supérieure à x400. Les
configurations couvrent un vent (4, 3) tourné, un vent exactement selon +x
et un vent quelconque non aligné.

## 4. Cas 1D exact

temps_premiere_arrivee_1d donne tau = |b - a| / |v| sur le quadrant aval
(b > a, v > 0). Les dérivées sont fermées et triviales :

d(tau)/dv = -tau / v ;  d(tau)/db = 1 / v ;  d(tau)/da = -1 / v.

Le test 4 de la section 3.3 les vérifie par différences finies. Ce cas
documente la sensibilité du cas d'école du MVP-S : doubler la vitesse divise
le temps par deux, et la dérivée est proportionnelle au temps lui-même.

## 5. Primitive polyligne : gradient dérivable, non testé

temps_transport calcule tau = somme(|ds_k| / |u_k|), lisse hors des
singularités (segment nul, norme égale à umin). Le gradient par rapport au
vent segmentaire est fermé :

grad_{u_k} tau = -|ds_k| u_k / |u_k|^3.

Il n'est pas testé dans cette PR : cette primitive est symétrique par
conception et n'est pas la métrique visée par la propriété « adjoint » de
l'issue #42 ; le test n'apporterait pas d'information sur la métrique
dirigée. À reconsidérer si cette primitive sert un jour d'oracle de
comparaison.

## 6. Ce qui reste non implémenté

- **État adjoint en champ variable** : la métrique historique de Drift-X
  est définie sur un champ multi-niveaux non reconstruit à ce jour ; son
  adjoint (acception 1) suivra la reconstruction.
- **Adjoint d'un schéma numérique** : les solveurs périodiques (centré/RK4,
  amont/Euler) pourraient recevoir une transcription rétrograde avec test
  croisé adjoint-direct ; arbitrage futur, non lié à l'issue #42.
- **Sensibilité du panache gaussien** : les dérivées de C par rapport à
  (u, classe, hauteur, sigma_y, sigma_z) sont dérivables analytiquement ;
  utiles pour l'assimilation (jalon M3), à dériver quand le besoin
  apparaît.

## 7. Ce que les tests n'établissent pas

- Ils ne constituent pas un état adjoint au sens du contrôle optimal
  (acception 1) : seul le gradient d'une référence analytique discrète est
  couvert.
- Ils ne couvrent pas la sensibilité de la métrique historique en champ
  variable, ni celle du panache gaussien.
- Ils n'établissent pas la dérivabilité à la borne transversale
  (section 3.2) : il n'y a rien à tester, le gradient n'existe pas là.
- Les différences finies valident l'implémentation aux points testés
  contre les formules fermées ; la preuve générale est la dérivation de la
  section 3.1, pas les tests.

## 8. Lien avec la feuille de route

Le jalon M3 (assimilation) présuppose une métrique dirigée différentiable :
toute assimilation de paramètres de vent par méthode de gradient a besoin du
gradient exact du coût. Le vecteur adjoint constant de la référence uniforme
en est le premier maillon vérifié. Le MVP-S hérite du gradient 1D exact
(section 4). La cartographie de ces résultats est tenue à jour dans
site/theorie/contraintes-physiques.qmd (section 6) et
site/projet/qualite.qmd.
