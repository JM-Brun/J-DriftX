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
   (paramétré, 3 configurations) : l'identite tau = lambda . d est
   restituée à la precision machine pres ;
2. test_uniform_pseudodistance_gradient_wrt_wind_matches_analytic
   (paramétré, 3 configurations) : differences finies centrees contre la
   formule fermee grad_u tau ;
3. test_uniform_pseudodistance_gradient_wrt_points_is_adjoint_vector :
   d(tau)/db = lambda et d(tau)/da = -lambda par differences finies ;
4. test_1d_first_arrival_gradient_matches_closed_form : gradient exact du
   cas 1D (section 4).

Calibration (effectuee avant l'ecriture des tests, sur les memes
configurations) : pas central h = 1e-5 ; erreur maximale mesuree entre
differences finies et formules analytiques : 2,5e-9 en absolu (erreur de
troncature O(h^2) et d'annulation epsilon_machine . tau / h). Tolerances
retenues : 1e-6 (absolu et relatif), marge superieure a x400. Les
configurations couvrent un vent aligne sur un axe (4,3) tourne, un vent
exactement selon +x et un vent quelconque non aligne.

## 4. Cas 1D exact

temps_premiere_arrivee_1d donne tau = |b - a| / |v| sur le quadrant aval
(b > a, v > 0). Les derivees sont fermees et triviales :

d(tau)/dv = -tau / v ;  d(tau)/db = 1 / v ;  d(tau)/da = -1 / v.

Le test 4 de la section 3.3 les verifie par differences finies. Ce cas
documente la sensibilite du cas d'ecole du MVP-S : doubler la vitesse divise
le temps par deux, et la derivee est proportionnelle au temps lui-meme.

## 5. Primitive polyligne : gradient derivable, non teste

temps_transport calcule tau = somme(|ds_k| / |u_k|), lisse hors des
singularites (segment nul, norme egale a umin). Le gradient par rapport au
vent segmentaire est ferme :

grad_{u_k} tau = -|ds_k| u_k / |u_k|^3.

Il n'est pas teste dans cette PR : cette primitive est symetrique par
conception et n'est pas la metrique visee par la propriete « adjoint » de
l'issue #42 ; le test n'apporterait pas d'information sur la metrique
dirigee. A reconsiderer si cette primitive sert un jour d'oracle de
comparaison.

## 6. Ce qui reste non implémenté

- **Etat adjoint en champ variable** : la metrique historique de Drift-X
  est definie sur un champ multi-niveaux non reconstruit a ce jour ; son
  adjoint (acception 1) suivra la reconstruction.
- **Adjoint d'un schema numerique** : les solveurs periodiques (centre/RK4,
  amont/Euler) pourraient recevoir une transcription retrograde avec test
  croise adjoint-direct ; arbitrage futur, non lie a l'issue #42.
- **Sensibilite du panache gaussien** : les derivees de C par rapport a
  (u, classe, hauteur, sigma_y, sigma_z) sont derivables analytiquement ;
  utiles pour l'assimilation (jalon M3), a deriver quand le besoin
  apparaît.

## 7. Ce que les tests n'établissent pas

- Ils ne constituent pas un etat adjoint au sens du controle optimal
  (acception 1) : seul le gradient d'une reference analytique discrete est
  couvert.
- Ils ne couvrent pas la sensibilite de la metrique historique en champ
  variable, ni celle du panache gaussien.
- Ils n'etablissent pas la derivabilite a la borne transversale
  (section 3.2) : il n'y a rien a tester, le gradient n'existe pas la.
- Les differences finies valident l'implementation aux points testes
  contre les formules fermees ; la preuve generale est la derivation de la
  section 3.1, pas les tests.

## 8. Lien avec la feuille de route

Le jalon M3 (assimilation) presuppose une metrique dirigee differentiable :
toute assimilation de parametres de vent par methode de gradient a besoin du
gradient exact du cout. Le vecteur adjoint constant de la reference uniforme
en est le premier maillon verifie. Le MVP-S herite du gradient 1D exact
(section 4). La cartographie de ces resultats est tenue a jour dans
site/theorie/contraintes-physiques.qmd (section 6) et
site/projet/qualite.qmd.
