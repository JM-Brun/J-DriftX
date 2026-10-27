# 26 — Investigation de l'adjoint du temps de transport dirigé (26/10/2026)

## 1. Objet et méthode

L'issue #42 liste l'adjoint parmi les propriétés visées du projet, avec la
consigne suivante dans son suivi : investigation de définition avant tout
test, sur le modèle de docs/19 pour le temps de parcours dirigé. Ce document
est cette investigation. La démarche est ordonnée et explicite :

1. distinguer les acceptions du mot « adjoint » et ancrer le choix retenu
   dans le corpus historique (section 2) ;
2. formaliser les définitions et notations utilisées (section 2.2) ;
3. énoncer exactement la fonction que le code évalue (section 3.1), puis
   dériver pas à pas ses gradients (sections 3.2, 4 et 5) ;
4. préciser les domaines de validité, y compris les points de
   non-dérivabilité (sections 3.3, 4 et 5) ;
5. décrire les tests qui vérifient l'implémentation contre les formules
   (section 3.4), récapituler les gradients établis (section 6) et
   cartographier honnêtement ce qui reste non implémenté (sections 7 à 9).

Aucune capacité n'est revendiquée au-delà des gradients effectivement
testés.

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

Ce document et les tests associés couvrent l'acception 2 uniquement ; l'ancrage
historique (section 2.1) confirme que c'est la bonne acception pour J-DriftX :
le corpus Drift-X employait l'acception 2 quant à l'usage, construite par
différentiation automatique en mode inverse (acception 3). La
« rigueur » d'un adjoint n'est pas une propriété physique comme la
conservation : c'est l'exactitude du gradient fourni, qui doit coïncider avec
la dérivée réelle de la fonction coût.

### 2.1 Ancrage dans le corpus historique

Les sources primaires du corpus sont archivées dans le dépôt (extractions
texte brutes grep-ables dans raw/extracts ; revues détaillées dans
docs/04-revues-papiers-sources.md). Elles tranchent la définition :

**C. R. Mécanique 2006** (Mohammadi & Brun, « Similitude généralisée et
modélisation géométrique à complexité réduite », C. R. Mécanique 334(10),
634-638, DOI 10.1016/j.crme.2006.06.007 ; texte intégral relu, extraction
dans raw/extracts/2006-mohammadi-brun-crmeca.txt). La section 4, « Calcul de
gradient et identification des sources d'une pollution », énonce :

> « On utilise la différentiation automatique en mode inverse par Tapenade
> pour construire le code adjoint et accéder au gradient avec un coût
> indépendant du nombre des paramètres de contrôle. Ce gradient est aussi
> utilisé pour la résolution de (1). »

où (1) est le problème d'assimilation : min sur p de J(p) = |u(p) - u_obs| +
|c(p, u(p)) - c_obs|, p regroupant toutes les variables indépendantes du
modèle (domaine, topographie, météo, sources, buses). La figure 5 montre la
« sensibilité (gradient) d'une pollution observée [...] par rapport à la
position de la source » : l'identification de sources est l'usage dual du
même gradient.

**Chapitre Springer 2008** (Brun & Mohammadi, « Reduced-Order Modelling of
Dispersion », p. 245-256, DOI 10.1007/978-1-4020-8758-5_14 ; résumé verbatim
et notes analytiques). Résumé : « Model parameters identification is based on
data assimilation. [...] Sensitivity analysis is used for risk analysis and
also for the identification of the sources of an observed pollution. » Le
chapitre mobilise en outre la sensibilité dite incomplète (lignée Mohammadi &
Pironneau) : la linéarisation porte sur le modèle approché, pas sur l'équation
d'état directe.

**HAL 2009** (Bozon, Sinfort & Mohammadi, plateforme Drift-X/SIG, texte
intégral dans raw/extracts/) : aucune occurrence d'« adjoint », « gradient »
ou « sensibilité » — ce papier, dédié au couplage SIG, ne développe pas
l'adjoint. Absence documentée, pas contradiction.

**Verdict.** L'adjoint historique de Drift-X est défini sans ambiguïté par
son usage et sa construction :

- quant à l'usage : l'acception 2 (gradient, fonction d'influence) — le
  gradient de la fonction coût d'assimilation J et la sensibilité d'une
  pollution observée par rapport à la position des sources ;
- quant à la construction : l'acception 3 — l'adjoint du code du modèle
  réduit, produit par différentiation automatique en mode inverse
  (Tapenade), avec la propriété économique caractéristique du mode inverse :
  un coût du gradient indépendant du nombre de paramètres de contrôle ;
- les sources examinées ne décrivent pas un état adjoint de l'EDP directe :
  elles documentent un gradient obtenu par différentiation automatique en mode
  inverse du code du modèle réduit. Le fait que le modèle ne requière pas la
  résolution d'une EDP (« The approach does not require the solution of any
  PDE ») et que la sensibilité soit dite incomplète — linéarisation du modèle
  approché — étaye cette lecture historique, sans exclure en général qu'un
  modèle réduit ou un système discret puisse avoir une formulation adjointe.
  Dans J-DriftX, aucun état adjoint d'EDP n'est actuellement implémenté.

Conséquence pour J-DriftX : les gradients exacts testés dans cette PR
(vecteur adjoint constant de la référence uniforme, gradient 1D) sont du
même nature que l'usage historique (fonction d'influence pour
l'assimilation et l'identification), à deux différences près, toutes deux
documentées : (i) la construction historique était automatique (AD inverse
du code entier), la nôtre est analytique et fermée sur des primitives
exactes — directement vérifiables analytiquement sur ces cas, sans
établir une supériorité générale sur la différentiation automatique ; (ii) le gradient historique portait sur la fonction
d'assimilation J (paramètres p du modèle complet), pas sur la seule métrique
dirigée — couvrir J suppose la chaîne complète c(p, u(p)), dont seul le
maillon tau est vérifié ici.

### 2.2 Définitions et notations

Cette section fixe le vocabulaire utilisé dans toutes les dérivations qui
suivent, pour que « gradient », « adjoint » et « exact » n'aient qu'un sens.

**Notations.** a (source) et b (cible) sont des points de R^2 ; u est un
vecteur vitesse de R^2 non nul ; d = b - a est le déplacement ; u_hat = u/|u|
est la direction du vent ; x.y désigne le produit scalaire euclidien et |x|
la norme euclidienne. Les formules sont écrites en texte simple : tau,
lambda et u_hat en toutes lettres, sans LaTeX.

**Définition 1 (différentiabilité, gradient).** Une fonction f de R^n dans R
est différentiable en x s'il existe un vecteur g tel que

    f(x + delta) = f(x) + g . delta + o(|delta|),   |delta| -> 0.

Ce vecteur est unique : si g1 et g2 conviennent tous deux, alors
(g1 - g2) . delta = o(|delta|) pour tout delta ; en choisissant
delta = t (g1 - g2) et en faisant tendre t vers 0, on obtient |g1 - g2|^2
= o(t |g1 - g2|), donc g1 = g2. Il est noté grad_x f, le gradient de f en
x. La quantité g . delta est la variation de f au premier ordre sous la
perturbation delta.

**Définition 2 (adjoint d'une entrée).** Pour une sortie scalaire tau et une
entrée x, l'adjoint de x est grad_x tau. Le vocabulaire vient de la
différentiation automatique en mode inverse, où les « variables adjointes »
sont les dérivées de la sortie par rapport aux variables du calcul : c'est
le pont exact entre les acceptions 2 et 3 de la section 2. Dans toute la
suite, « vecteur adjoint » signifie gradient d'une sortie scalaire par
rapport à une entrée, au sens de la définition 1 — rien d'autre.

**Définition 3 (gradient exact, formule fermée).** Une formule est fermée si
elle exprime le résultat explicitement en les entrées, sans limite, somme
infinie ou procédure itérative (l'entrée « Formule fermée (formule close) »
du glossaire du site en donne l'intuition avec pi r^2). Un gradient est dit
exact s'il coïncide, sur un domaine explicité, avec la dérivée de la
fonction que le code évalue réellement — pas seulement avec celle d'un
modèle voisin.

**Outil de validation : différences finies centrées.** L'estimation

    ( f(x + h e_i) - f(x - h e_i) ) / (2 h)

approche la i-ème composante du gradient avec une erreur de troncature en
O(h^2) et une erreur d'arrondi de l'ordre de epsilon_machine |f| / h ; le
pas h résulte d'un compromis entre les deux, calibré en section 3.4. Les
différences finies valident une implémentation en des points ; elles ne
constituent pas une preuve générale — la preuve est la dérivation, les
différences finies en sont le contrôle.

## 3. Référence uniforme : adjoint exact fermé

### 3.1 La fonction évaluée par le code

pseudo_distance_uniforme(a, b, u) retourne exactement (aucune ligne du code
de production n'est modifiée dans cette PR) :

    tau(a, b, u) = (d . u_hat) / |u|    si d . u > 0,
                 = 0                    si d . u = 0,
                 = +inf                si d . u < 0,

avec rejet explicite (ValueError) des entrées non finies et du vent nul.
Trois précisions lèvent des ambiguïtés de vocabulaire :

- le nom « pseudo-distance » est historique ; la quantité évaluée ici est un
  temps de parcours, en secondes, comme le contrôle d'unités de la section
  3.2 le confirme ;
- la dérivation qui suit part de cette définition piecewise, pas d'une
  écriture voisaine ;
- équivalence algébrique : u_hat = u/|u| donne d . u_hat = (d . u)/|u|, puis
  (d . u_hat)/|u| = (d . u)/|u|^2 = (d . u)/(u . u). Toutes les formules de
  ce document utilisent la dernière écriture ; elles sont identiquement
  égales à ce que le code évalue.

### 3.2 Dérivation

**Identité adjointe.** Sur le demi-plan aval ouvert (d . u > 0, section 3.3),
le coût se réécrit

    tau = (d . u)/(u . u) = lambda . d,   avec lambda := u/(u . u).

lambda = u_hat/|u| : direction du vent, norme 1/|u|. Contrôle d'unités :
[lambda] = (m/s)/(m^2 s^-2) = s/m, donc lambda . d est en secondes, l'unité
attendue d'un temps de transport.

**Gradient par rapport à la cible b.** Sur le demi-plan aval, tau est
affine en b : pour toute perturbation delta telle que b + delta reste en
aval,

    tau(b + delta) - tau(b) = lambda . delta,   exactement,

sans reste du tout : le o(|delta|) de la définition 1 est ici nul et
l'égalité vaut globalement, pas seulement au voisinage. Donc
grad_b tau = lambda. C'est en ce sens précis que lambda est le « vecteur
adjoint constant » de la référence uniforme : l'adjoint de l'entrée b ne
dépend ni de a ni de b. Lecture : déplacer la cible de 1 m selon la
direction du vent allonge le temps d'exactement 1/|u| secondes.

**Gradient par rapport à la source a.** Le déplacement entre par la
différence d = b - a : grad_a tau = -lambda. Le coût est affine en a
également ; déplacer la source de delta change le coût d'exactement
-lambda . delta.

**Gradient par rapport au vent u.** Sur le demi-plan aval, tau = N/Q avec
N = d . u et Q = u . u. Composantes : N = d_x u_x + d_y u_y donne
grad_u N = d ; Q = u_x^2 + u_y^2 donne grad_u Q = 2 u. La règle du quotient
(applicable car Q > 0 sur le domaine) donne alors

    grad_u tau = (Q grad_u N - N grad_u Q) / Q^2
               = d/(u . u) - 2 (d . u) u / (u . u)^2.

Contrôle d'unités : chaque terme est en m/(m^2 s^-2) = s^2/m, l'unité
attendue d'une dérivée de secondes par rapport à une vitesse (m/s).
L'adjoint de l'entrée u est ce vecteur grad_u tau — à ne pas confondre avec
lambda, qui est l'adjoint des entrées de position.

**Contrôles de cohérence.** Deux vérifications indépendantes relient la
formule à des propriétés déjà connues du dépôt ; elles ne sont pas des
preuves supplémentaires, mais des garde-fous contre une erreur de calcul :

- Projection sur la direction du vent : en substituant u . u = |u|^2 et
  u . u_hat = |u|,

      (grad_u tau) . u_hat = (d . u)/|u|^3 - 2 (d . u)/|u|^3 = -tau/|u|.

  Signe attendu : renforcer le vent dans sa propre direction (delta |u| > 0
  à géométrie fixée) raccourcit le temps ; la variation au premier ordre
  vaut -(tau/|u|) delta |u|.
- Homogénéité : pour alpha > 0, tau(a, b, alpha u) = tau(a, b, u)/alpha
  (l'amont/aval est préservé par homothétie positive ; c'est le test
  d'échelle existant de tests/test_metric.py). La dérivation en alpha de
  cette identité en alpha = 1 impose u . grad_u tau = -tau, et la forme
  fermée le restitue :

      (grad_u tau) . u = (d . u)/(u . u) - 2 (d . u)/(u . u) = -tau.

### 3.3 Domaine de validité et non-dérivabilité

Les formules de la section 3.2 valent sur l'ouvert

    H = { (a, b, u) : u non nul, (b - a) . u > 0 },

le demi-plan aval strict. Sur H, tau est un quotient de polynômes à
dénominateur strictement positif : elle y est lisse, affine en les
positions, différentiable — mais pas affine — en le vent.

La borne transversale d . u = 0 n'appartient pas au domaine. Le code y
renvoie 0 (section 3.1), mais toute boule ouverte centrée en un point de la
borne contient des points amont où tau = +inf : tau n'y est pas continue,
donc pas différentiable, et il n'y a rien à approcher par différences
finies. Le gradient de la restriction lisse (d . u)/(u . u) — c'est-a-dire
lambda, pour les positions — existe sur la borne, mais ce n'est pas le
gradient de la fonction piecewise que le code évalue ; la nuance doit
rester explicite dans tout usage futur. C'est une limite de la convention
+inf, pas du calcul différentiel. Toute assimilation utilisant ce gradient
devra décider explicitement du traitement de cette frontière (domaine
strict, régularisation, ou coût pénalisé).

Une exigence pratique en découle pour les tests : les différences finies
de la section 3.4 n'ont de sens que si les points perturbés x ± h e_i
restent dans H ; les configurations de test sont strictement aval, avec
une marge très supérieure au pas.

### 3.4 Tests : validation croisée par différences finies

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

Les contrôles de cohérence de la section 3.2 ne sont pas re-testés
séparément : l'un recoupe le test d'échelle existant du même fichier
(test_uniform_pseudodistance_scales_inversely_with_wind_magnitude,
tau(alpha u) = tau(u)/alpha), l'autre est une identité algébrique établie
dans la dérivation.

## 4. Cas 1D exact

**La fonction.** Sur le quadrant aval {b > a, v > 0}, le code évalue

    tau_1d = abs((b - a)/v) = (b - a)/v

(les signes de b - a et de v y coïncident). Les cas dégénérés suivent la
convention du code : b = a donne 0 ; v = 0 ou signes opposés donnent +inf.

**Dérivation.** tau_1d = (b - a)/v est affine en b et en a, quotient en v :

    d(tau_1d)/db = 1/v ;  d(tau_1d)/da = -1/v ;
    d(tau_1d)/dv = -(b - a)/v^2 = -tau_1d/v.

La dernière égalité dérive du quotient : la dérivée de (b - a) v^-1 en v est
-(b - a) v^-2, et (b - a)/v = tau_1d. Lecture : doubler v divise le temps
par deux ; la sensibilité à la vitesse est proportionnelle au temps
lui-même. Ce cas documente la sensibilité du cas d'école du MVP-S.

**Domaine.** Ces formules valent sur le quadrant ouvert {b > a, v > 0}. Aux
dégénéréscences, la convention piecewise reprend la main : en b = a la
fonction vaut 0 mais saute à +inf dès que b passe en amont de a — pas de
dérivabilité ; en v = 0 la cible est inaccessible (+inf).

**Cohérence avec la référence 2D (levée d'ambiguïté).** Le cas 1D est la
restriction de la référence uniforme au vent u = (v, 0) et aux déplacements
portés par l'axe x. La section 3.2 y specialisée donne lambda = (1/v, 0),
d'où d(tau_1d)/db = 1/v — exactement grad_b tau de la section 3.2 — et la
dérivée en vitesse -tau_1d/v est la composante de grad_u tau le long de
u_hat (contrôle de la section 3.2 avec |u| = v : -tau/|u|). Les formules 1D
et 2D ne sont donc pas deux objets distincts mais le même gradient évalué
dans deux cadres ; toute divergence future entre elles signalerait une
erreur.

## 5. Primitive polyligne : gradient dérivable, non testé

**La fonction.** temps_transport calcule tau = somme_k L_k / |u_k|, où
ds_k = p_{k+1} - p_k sont les segments de la polyligne et L_k = |ds_k|.

**Dérivation (vent segmentaire).** Pour u non nul, la norme euclidienne
satisfait d|u|/du = u/|u|. La dérivation de L_k |u_k|^-1 en u_k donne alors

    grad_{u_k} tau = -L_k u_k / |u_k|^3,

car la dérivée de |u_k|^-1 est -|u_k|^-2 (u_k/|u_k|).

**Domaine.** Formules valables pour u_k non nul et segment non nul : la
norme n'est pas différentiable en 0, ni pour |u_k| ni pour |ds_k|. La
fonction gardée par le code refuse en pratique |u_k| < umin : son domaine
d'évaluation est |u_k| >= umin, et les formules ci-dessus s'appliquent sur
|u_k| > umin.

**Pourquoi ce gradient n'est pas testé ici.** Cette primitive est
symétrique par conception (elle n'utilise que la norme des vitesses) et
n'est pas la métrique visée par la propriété « adjoint » de l'issue #42 ;
le test n'apporterait pas d'information sur la métrique dirigée. À
reconsidérer si cette primitive sert un jour d'oracle de comparaison.

## 6. Récapitulatif des gradients établis

| Objet | Gradient (formule fermée) | Domaine | Statut |
|---|---|---|---|
| Référence uniforme, entrée b | lambda = u/(u . u) | demi-plan aval ouvert | dérivé (3.2), testé (3.4) |
| Référence uniforme, entrée a | -lambda | demi-plan aval ouvert | dérivé (3.2), testé (3.4) |
| Référence uniforme, entrée u | d/(u . u) - 2 (d . u) u / (u . u)^2 | demi-plan aval ouvert | dérivé (3.2), testé (3.4) |
| Cas 1D | d/db = 1/v ; d/da = -1/v ; d/dv = -tau_1d/v | quadrant b > a, v > 0 | dérivé (4), testé (3.4) |
| Polyligne, vent segmentaire | -L_k u_k / |u_k|^3 | u_k et segment non nuls | dérivé (5), non testé |
| Panache gaussien, champ variable | non dérivé | - | hors périmètre (7) |

## 7. Ce qui reste non implémenté

- **Gradient historique en champ variable** : la métrique historique de
  Drift-X est définie sur un champ multi-niveaux non reconstruit à ce jour ;
  le gradient au sens historique (différentiation automatique inverse du code,
  section 2.1) ne pourra être reproduit qu'après reconstruction des éléments
  nécessaires du modèle. Les sources examinées ne décrivent pas d'état adjoint
  de l'EDP directe ; aucun état adjoint d'EDP n'est implémenté dans J-DriftX.
  Cette limite de périmètre ne signifie pas qu'une formulation adjointe d'un
  modèle réduit ou d'un système discret soit impossible en général.
- **Adjoint d'un schéma numérique** : les solveurs périodiques (centré/RK4,
  amont/Euler) pourraient recevoir une transcription rétrograde avec test
  croisé adjoint-direct ; arbitrage futur, non lié à l'issue #42.
- **Sensibilité du panache gaussien** : les dérivées de C par rapport à
  (u, classe, hauteur, sigma_y, sigma_z) sont dérivables analytiquement ;
  utiles pour l'assimilation (jalon M3), à dériver quand le besoin
  apparaît.

## 8. Ce que les tests n'établissent pas

- Ils ne constituent pas un état adjoint au sens du contrôle optimal
  (acception 1) : seul le gradient d'une référence analytique discrète est
  couvert.
- Ils ne couvrent pas non plus le gradient de la fonction d'assimilation J
  du corpus (métrique + concentration + paramètres complets) : seul le
  maillon métrique tau est vérifié.
- Ils ne couvrent pas la sensibilité de la métrique historique en champ
  variable, ni celle du panache gaussien.
- Ils n'établissent pas la dérivabilité à la borne transversale
  (section 3.3) : il n'y a rien à tester, le gradient n'existe pas là.
- Les différences finies valident l'implémentation aux points testés
  contre les formules fermées ; la preuve générale est la dérivation de la
  section 3.2, pas les tests.
- Les entrées générées de `tests/test_proprietes.py` (hypothesis) étendent
  l'identité tau = lambda . d et l'homogénéité en le vent à des
  configurations aval aléatoires, évaluées à travers les objets
  `ScenarioUniforme` de l'expérience champ uniforme ; elles élargissent la
  couverture des points testés, pas la nature de la preuve — la dérivation
  de la section 3.2 reste la référence.

## 9. Lien avec la feuille de route

Le jalon M3 (assimilation) présuppose une métrique dirigée différentiable :
toute assimilation de paramètres de vent par méthode de gradient a besoin du
gradient exact du coût. Le vecteur adjoint constant de la référence uniforme
en est le premier maillon vérifié ; l'usage historique du gradient — résoudre
le problème d'assimilation et identifier les sources d'une pollution observée
(section 2.1) — en donne la finalité exacte. Le MVP-S hérite du gradient 1D exact
(section 4). La cartographie de ces résultats est tenue à jour dans
site/theorie/contraintes-physiques.qmd (section 6) et
site/projet/qualite.qmd.
