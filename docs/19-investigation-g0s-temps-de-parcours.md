# Investigation G0-S — temps de parcours dirigé : définitions, cas 1D, contre-exemples

> **Statut (22 octobre 2026).** Document de travail G0-S, réponse à l'[issue #41](https://github.com/JM-Brun/J-DriftX/issues/41). Périmètre strict, conforme à [13-mvp-scientifique-et-g0.md](13-mvp-scientifique-et-g0.md) : aucune prédiction de dépôt ou de concentration, aucun benchmark applicatif, aucune revendication de supériorité ou d'originalité. Tous les résultats ci-dessous sont établis analytiquement et calculables à la main ; les contrôles numériques indépendants (annexe A) vérifient les calculs, ils ne sont pas des benchmarks.

## 1. Objet et réponse courte

La question de l'issue #41 est : **quelles propriétés possède une fonction de temps de parcours dirigé définie par une dynamique explicite, et lesquelles ne découlent pas de sa seule définition ?**

Réponse courte, démontrée dans les sections 3 à 7 :

1. Le **temps de première arrivée** (variante V1, définition 2.3) satisfait automatiquement, par sa seule définition : positivité, séparation des points, inégalité triangulaire dirigée (propositions 3.2 et 3.3). Il ne satisfait pas, en général : la symétrie (structurellement), ni la finitude (points inaccessibles). C'est une **quasi-distance étendue** au sens des axiomes (D1)–(D4) ci-dessous.
2. La **pseudo-distance projetée historique** (variante V2, définition 2.4, Mohammadi & Brun 2006) ne conserve **automatiquement aucune** propriété de distance dès la dimension 2 : la séparation (§ 5.2), l'inégalité triangulaire (§ 5.4–5.6) et même l'unicité de la valeur (§ 6.1) peuvent échouer. En dimension 1, V2 coïncide avec V1 (proposition 5.1) : les pathologies de V2 sont des phénomènes de dimension supérieure ou égale à 2.
3. Aucune des deux variantes n'entraîne de propriété physique (conservation de masse, positivité d'une concentration) : ces propriétés relèvent de l'équation de transport et de ses hypothèses, pas du temps de parcours (renvoi à [14-revue-mathematique-ciblee.md](14-revue-mathematique-ciblee.md), § 3.4).
4. Le risque de nouveauté est tranché (§ 7) : l'intégrale de temps le long d'une ligne de courant est un objet classique (time-of-flight des méthodes streamline, distances-temps en géographie) ; la construction projetée par paires et son statut de pseudo-distance sont annoncés dans la source primaire de 2006 elle-même. Conclusion du MVP : **idée connue, utile pédagogiquement, désormais délimitée précisément** — l'une des conclusions autorisées par le document MVP (§ 3).

## 2. Définitions, hypothèses, conventions

### 2.1 Champ admissible

Soit \(\Omega\) un ouvert de \(\mathbb R^d\) (d = 1 ou 2 dans ce document). Un **champ admissible** est une application \(\mathbf u : \Omega \to \mathbb R^d\) de classe \(C^1\), **stationnaire**. Le caractère stationnaire est une hypothèse de périmètre : dans un champ instationnaire, lignes de courant, trajectoires et lignes d'émission diffèrent, et rien ci-dessous ne se transfère sans retravail (§ 10).

### 2.2 Flot, trajectoire, caractéristique

Pour \(A \in \Omega\), la **trajectoire** issue de \(A\) est l'unique solution maximale \(t \mapsto X(t; A)\) de

\[
\dot X = \mathbf u(X), \qquad X(0) = A,
\]

définie sur un intervalle ouvert \(I_A\) contenant 0 (unicité : Cauchy–Lipschitz, \(\mathbf u\) de classe \(C^1\)). On note \(\gamma_A = \{X(t; A) : t \in I_A\}\) la courbe trajectoire et \(\gamma_A^+ = \{X(t; A) : t \in I_A \cap [0,+\infty[\}\) l'**orbite positive**. Champ stationnaire : la courbe trajectoire coïncide avec la ligne de courant et sert de caractéristique à l'équation d'advection ; ces trois notions ne doivent pas être confondues en instationnaire (revue ciblée, § 2).

### 2.3 Variante V1 — temps de parcours dirigé (première arrivée)

Pour \(A, B \in \Omega\) :

\[
T(A, B) = \inf\{\, t \ge 0 : X(t; A) = B \,\}, \qquad \inf \varnothing = +\infty.
\]

\(T(A,B)\) est le **temps de première arrivée** de \(B\) sur l'orbite positive de \(A\). Unités : \([\mathbf u] = \mathrm{m\,s^{-1}}\), \([T] = \mathrm{s}\).

### 2.4 Variante V2 — pseudo-distance projetée historique

(Mohammadi & Brun 2006, § 3.) Pour \(A, B \in \Omega\) :

\[
d(A, B) = T(A, B^\perp),
\]

où \(B^\perp\) est la projection (euclidienne, dans les cas du § 5) de \(B\) sur la caractéristique \(\gamma_A\). Hypothèses implicites de la source : **(H1)** la caractéristique passant par \(A\) est unique (sources et puits écartés) ; **(H2)** la projection \(B \mapsto B^\perp\) est bien définie. (H2) est mise en défaut au § 6.1 : la source résout la non-unicité de la projection par un critère en \(\mathbf u \cdot \nabla c\), qui dépend de la concentration — donc de la sortie du modèle. Cette dépendance circulaire est documentée ici, non résolue. Dans un champ uniforme ou de cisaillement (§ 5), \(\gamma_A\) est une droite horizontale et \(B^\perp = (x_B, y_A)\) — lecture confirmée par la relecture de la source ([14-revue-mathematique-ciblee.md](14-revue-mathematique-ciblee.md), § 2.1).

### 2.5 Conventions et axiomes de référence

- **(C1)** \(+\infty\) désigne l'inaccessibilité dans le sens de l'écoulement : un choix de modélisation, pas une propriété démontrée.
- **(C2)** Le **temps de sortie** \(\sigma(A) = \inf\{t \ge 0 : X(t; A) \notin \Omega\}\) distingue un troisième état : si \(\sigma(A) < T(A,B)\), le point \(B\) est inaccessible **par sortie de domaine** — « n'existe pas » au sens strict, à ne pas confondre avec le \(+\infty\) d'orientation.
- **(C3)** \(t = 0\) est admis dans l'infimum : \(T(A,A) = 0\). Le « temps de retour » sur une orbite fermée est une autre grandeur (§ 6.3).
- **Axiomes.** (D1) \(T(x,x)=0\) ; (D2) \(T(x,y) \ge 0\) ; (D3) inégalité triangulaire dirigée \(T(x,z) \le T(x,y) + T(y,z)\) au sens étendu ; (D4) séparation : \(T(x,y) = 0 \Rightarrow x = y\). Une **quasi-distance étendue** vérifie (D1)–(D4) ; une distance vérifie en outre la symétrie et la finitude.

## 3. V1 : ce qui découle de la seule définition

**Lemme 3.1 (le temps de première arrivée est atteint).** Si \(T(A,B) < +\infty\), alors \(X(T(A,B); A) = B\).

*Preuve.* L'ensemble \(H = \{t \ge 0 : X(t;A) = B\}\) est fermé (image réciproque du fermé \(\{B\}\) par l'application continue \(t \mapsto X(t;A)\), intersecté avec \([0,+\infty[\)) et non vide ; son infimum est limite d'une suite d'éléments de \(H\), donc appartient à \(H\). ∎

**Proposition 3.2 (positivité et séparation).** V1 vérifie (D1), (D2) et (D4).

*Preuve.* (D1) : \(t=0 \in H_{A,A}\), donc \(T(A,A)=0\). (D2) : infimum sur \([0,+\infty[\). (D4) : si \(A \ne B\), posons \(\delta = |A-B| > 0\). Par continuité de \(t \mapsto X(t;A)\) en 0, il existe \(\varepsilon > 0\) tel que \(|X(t;A) - A| < \delta/2\) pour \(t \in [0,\varepsilon]\) ; alors \(|X(t;A) - B| \ge \delta/2 > 0\) sur \([0,\varepsilon]\), donc \(T(A,B) \ge \varepsilon > 0\). ∎

**Proposition 3.3 (inégalité triangulaire dirigée).** V1 vérifie (D3), au sens étendu (\(+\infty + a = +\infty\)).

*Preuve.* Si \(T(A,B) = +\infty\) ou \(T(B,C) = +\infty\), l'inégalité est triviale. Sinon, posons \(t_1 = T(A,B)\), \(t_2 = T(B,C)\), atteints (lemme 3.1). Le flot autonome vérifie la propriété de semi-groupe \(X(s; X(t;A)) = X(s+t; A)\) (les deux membres résolvent la même équation avec la même condition initiale ; unicité de Cauchy–Lipschitz). Donc \(X(t_1+t_2; A) = X(t_2; X(t_1;A)) = X(t_2; B) = C\) : \(t_1 + t_2 \in H_{A,C}\), donc \(T(A,C) \le t_1 + t_2\). ∎

**Remarque 3.4 (additivité et cas d'égalité).** L'égalité \(T(A,C) = T(A,B)+T(B,C)\) vaut lorsque le premier passage en \(B\) depuis \(A\) précède le premier passage en \(C\) — en particulier pour trois points d'une même trajectoire non périodique rangés dans l'ordre du flot, et pour tout triplet 1D ordonné (théorème 4.2). Sur une orbite fermée, l'inégalité peut être **stricte** :

**Exemple 3.5 (sous-additivité stricte, champ rotationnel).** \(\mathbf u(x,y) = (-y, x)\), \(A=(1,0)\), \(B=(-1,0)\), \(C=(0,1)\). La trajectoire est \(X(t;A) = (\cos t, \sin t)\) : \(T(A,B) = \pi\), \(T(B,C) = 3\pi/2\) (trois quarts de tour), \(T(A,C) = \pi/2\). Donc \(T(A,C) = \pi/2 < \pi + 3\pi/2\). (Contrôlé numériquement, annexe A.)

**Proposition 3.6 (non-symétrie structurelle et retournement).** (i) En général \(T(B,A) = +\infty\) alors que \(T(A,B) < +\infty\) (tout champ dirigé, § 5). (ii) **Retournement exact** : pour le champ opposé \(-\mathbf u\), \(T_{-\mathbf u}(B,A) = T_{\mathbf u}(A,B)\) chaque fois que l'un des deux membres est fini. La non-symétrie n'est donc pas une propriété de la courbe géométrique \(\gamma_A\), mais du couple (champ, orientation).

*Preuve de (ii).* Si \(X(t^*;A) = B\), alors \(s \mapsto X(t^*-s; A)\) est une trajectoire de \(-\mathbf u\) issue de \(B\) qui atteint \(A\) en \(s = t^*\) : \(T_{-\mathbf u}(B,A) \le T_{\mathbf u}(A,B)\). En appliquant le même argument à \(-\mathbf u\), l'inégalité inverse. ∎

**Proposition 3.7 (les orbites fermées restaurent l'accessibilité bilatérale).** Si la trajectoire issue de \(A\) est périodique de période \(p\) et si \(B \in \gamma_A\), \(B \ne A\), alors \(T(A,B) \in\, ]0, p]\) et \(T(B,A) = p - T(A,B) < +\infty\). Sur une orbite fermée, tout couple de points est accessible dans les deux sens : l'« asymétrie » y disparaît.

*Preuve.* L'orbite est parcourue entièrement en une période : le premier passage en \(B\) existe dans \(]0, p]\), noté \(t_1\), avec \(X(t_1;A) = B\). Les temps d'atteinte d'un point d'une orbite fermée depuis un autre point de la même orbite forment une progression arithmétique de raison \(p\) ; ceux de \(A\) depuis \(B\) sont donc \((p - t_1) + k p\), \(k \ge 0\), dont le plus petit est \(p - t_1\). ∎

**Proposition 3.8 (stabilité locale).** Si \(X(t^*; A_0) = B\) avec \(\mathbf u(B) \ne 0\), alors chaque temps d'atteinte isolé de \(B\) dépend de façon \(C^1\) de \(A\) au voisinage de \(A_0\) (théorème des fonctions implicites appliqué à \((t,A) \mapsto X(t;A) - B\), dont la dérivée partielle en \(t\) vaut \(\mathbf u(B) \ne 0\)) ; si en outre \(t^*\) est l'unique temps d'atteinte (trajectoire non périodique), \(T(\cdot, B)\) est \(C^1\) au voisinage de \(A_0\). La stabilité se perd aux cibles stagnantes (§ 6.4). (Preuve : esquisse standard par fonctions implicites et unicité locale.)

**Tableau 3.9 (V1, récapitulatif).**

| Axiome / propriété | V1 | Référence |
|---|---|---|
| (D1) \(T(x,x)=0\) | oui, par définition | 3.2 |
| (D2) positivité | oui, par définition | 3.2 |
| (D4) séparation | **oui, démontrée** | 3.2 |
| (D3) triangulation dirigée | **oui, démontrée** | 3.3 |
| symétrie | non (structurelle) ; bilatérale sur les orbites fermées | 3.6, 3.7 |
| finitude | non : \(+\infty\) amont, sortie de domaine | 2.5, 6.2 |
| unicité de la valeur | oui (flot unique sous \(C^1\)) | 2.2 |

## 4. Cas 1D calculés à la main

**Lemme 4.1 (unicité du flot 1D sans stagnation).** Pour \(d=1\), \(\mathbf u = u : I \to\, ]0,+\infty[\) **continue** (non nécessairement lipschitzienne), le flot est unique : toute solution est strictement croissante (car \(u > 0\)) et vérifie \(t = \int_a^{x(t)} dx/u(x)\), donc \(x(t) = F^{-1}(t)\) où \(F(x) = \int_a^x dx'/u(x')\) est strictement croissante. En 1D, la non-unicité ne peut apparaître qu'aux points de stagnation \(u = 0\) (contre-exemple 4.6).

**Théorème 4.2 (forme explicite 1D).** Pour \(u > 0\) continue sur un intervalle et \(a, b\) dans cet intervalle :

\[
T(a,b) = \int_a^b \frac{dx}{u(x)} \text{ si } b > a ; \qquad T(a,a) = 0 ; \qquad T(a,b) = +\infty \text{ si } b < a.
\]

*Preuve.* Cas \(b > a\) : lemme 4.1, l'atteinte de \(b\) a lieu à \(t = F(b)\). Cas \(b < a\) : la trajectoire est strictement croissante, \(b\) n'est jamais atteint. ∎

Conséquences immédiates : positivité stricte (\(b > a \Rightarrow T > 0\)), séparation, additivité stricte par relation de Chasles (\(a < b < c \Rightarrow T(a,c) = T(a,b) + T(b,c)\)), monotonie de \(T(a, \cdot)\), et **non-symétrie maximale** : \(T(b,a) = +\infty\) pour \(b > a\) — le trajet retour est impossible dans le même champ ; le retournement exige le champ opposé (proposition 3.6).

**Tableau 4.3 (exemples calculés à la main ; tous contrôlés, annexe A).**

| Champ | Temps calculé | Propriété illustrée |
|---|---|---|
| \(u \equiv U > 0\) | \(T(a,b) = (b-a)/U\) si \(b > a\), \(+\infty\) sinon | quasi-distance étendue linéaire ; cas implémenté (<code>pseudo_distance_uniforme</code>) |
| \(u(x) = x\) sur \(]0,+\infty[\) | \(T(1,2) = \ln 2\) ; \(T(0,b) = +\infty\) | stagnation d'ordre 1 **au départ** : jamais quittée |
| \(u(x) = \sqrt{x}\) sur \([0,+\infty[\) | branche mobile : \(T(0,b) = 2\sqrt{b}\) | stagnation d'ordre 1/2 : évasion en temps fini, mais flot non unique (4.6) |
| \(u(x) = 1 - x\) sur \([0,1[\) | \(T(0,b) = -\ln(1-b) \to +\infty\) quand \(b \to 1\) | stagnation d'ordre 1 **à l'arrivée** : jamais atteinte |
| \(u(x) = \sqrt{1-x}\) sur \([0,1]\) | \(T(0,1) = 2\) | stagnation d'ordre 1/2 à l'arrivée : atteinte en temps fini (flot unique ici) |

**Proposition 4.4 (critère d'ordre de la stagnation).** Soit \(x^*\) un point de stagnation (\(u(x^*) = 0\)) avec \(|u(x)| \sim c\,|x - x^*|^{\alpha}\) (\(c > 0\), \(\alpha > 0\)) d'un côté de \(x^*\). Alors : (i) partir de \(x^*\) vers ce côté, et (ii) atteindre \(x^*\) depuis ce côté, prennent tous deux un temps fini **si et seulement si** \(\alpha < 1\).

*Preuve.* Les deux temps sont comparables à \(\int_0^\delta dr/(c r^\alpha)\), qui converge si et seulement si \(\alpha < 1\). ∎

Ce critère tranche la question 1D de l'issue : la singularité de l'intégrande \(1/|u|\) près d'une stagnation ne conduit pas toujours à un temps infini — **l'ordre d'annulation décide**.

**Corollaire 4.5 (barrière C¹).** Pour un champ de classe \(C^1\), un point de stagnation n'est **ni atteint ni quitté** en temps fini le long d'une trajectoire, et aucune trajectoire ne le traverse. *Preuve.* \(u'\) bornée au voisinage de \(x^*\) donne \(|u(x)| \le M |x - x^*|\), donc \(\int dr/|u| \ge (1/M)\int dr/r = +\infty\) ; traverser \(x^*\) imposerait \(X(t^*) = x^*\), donc (unicité de Cauchy–Lipschitz) \(X \equiv x^*\). ∎ Conséquence pour le contexte atmosphérique : dans un champ \(C^1\), toute zone de vent nul est une barrière en temps infini pour le temps de parcours dirigé. Les temps finis du tableau 4.3 (\(\alpha < 1\)) exigent une annulation d'ordre non entier, donc un champ **non \(C^1\)** au point de stagnation — précisément le régime du contre-exemple suivant.

**Contre-exemple 4.6 (nécessité de l'unicité du flot — la régularité n'est pas décorative).** \(\dot x = \sqrt{x}\), \(x(0) = 0\) : \(x(t) \equiv 0\) et \(x(t) = (t/2)^2\) sont deux solutions (vérification : \(\frac{d}{dt}(t/2)^2 = t/2 = \sqrt{(t/2)^2}\)). Le « temps de parcours de 0 vers \(b\) » dépend de la branche : la branche mobile donne \(2\sqrt{b}\), la branche stationnaire ne part jamais. La définition 2.3 (un seul \(T\)) exige donc l'unicité du flot : en 1D elle est acquise dès que \(u > 0\) (lemme 4.1) ; en dimension supérieure, l'hypothèse \(C^1\) (Cauchy–Lipschitz) est le garde-fou standard. Un champ admissible pour V1/V2 ne doit donc pas présenter de stagnation « plate » non lipschitzienne, ou doit spécifier une convention de branche.

**Remarque 4.7 (limites et sortie de domaine).** Sur \(\Omega =\, ]0,1[\) avec \(u \equiv U\) : le temps de sortie vaut \(\sigma(a) = (1-a)/U\) ; les points au-delà du domaine relèvent de la convention (C2), pas du \(+\infty\) d'orientation.

## 5. V2 : champ uniforme et champs de cisaillement (2D, calculables à la main)

**Proposition 5.1 (V2 = V1 en dimension 1).** Pour \(d = 1\), la caractéristique \(\gamma_a\) est l'intervalle lui-même : tout \(b\) se projette sur lui-même, \(b^\perp = b\), donc \(d(a,b) = T(a,b)\). Toutes les pathologies de V2 (séparation, triangulation, unicité) sont donc des phénomènes de dimension supérieure ou égale à 2. ∎

### 5.2 Champ uniforme — dégénérescence transversale

\(\mathbf u = (U, 0)\), \(U > 0\). Caractéristiques : droites horizontales ; \(B^\perp = (x_B, y_A)\) ;

\[
d(A,B) = \frac{x_B - x_A}{U} \text{ si } x_B \ge x_A, \qquad +\infty \text{ sinon.}
\]

- **Échec de la séparation** (dégénérescence transversale) : \(d(A,B) = 0\) pour tout \(B\) de même abscisse que \(A\), \(A \ne B\). La construction mesure un avancement longitudinal le long de \(\gamma_A\), pas une distance jusqu'à \(B\) : le coût transversal est nul.
- **Triangulation dirigée** : pour \(x_A \le x_B \le x_C\), \(d(A,C) = d(A,B) + d(B,C)\) (égalité).
- Conclusion : le champ uniforme fait échouer la séparation mais pas (encore) la triangulation. C'est le cas implémenté et testé (<code>pseudo_distance_uniforme</code>).

### 5.3 Champs de cisaillement

\(\mathbf u(x,y) = (v(y), 0)\), \(v : [0,1] \to\, ]0,+\infty[\) de classe \(C^1\). Champ lisse, sans stagnation (\(v > 0\)), à **divergence nulle** (\(\partial_x v(y) = 0\)). Caractéristiques : droites horizontales ; \(B^\perp = (x_B, y_A)\) ;

\[
d(A,B) = \frac{x_B - x_A}{v(y_A)} \text{ si } x_B \ge x_A, \qquad +\infty \text{ sinon.}
\]

**Lemme 5.4 (caractérisation exacte de la triangulation en cisaillement).** Pour \(x_A \le x_B \le x_C\) :

\[
d(A,C) \le d(A,B) + d(B,C) \iff v(y_B) \le v(y_A).
\]

*Preuve.* En développant, puis en soustrayant \((x_B - x_A)/v(y_A)\) et en divisant par \(x_C - x_B > 0\) : l'inégalité équivaut à \(1/v(y_A) \le 1/v(y_B)\), soit \(v(y_B) \le v(y_A)\). ∎

Interprétation : la triangulation dirigée échoue **exactement** lorsque le point intermédiaire \(B\) est porté par une caractéristique plus rapide que celle de \(A\).

**Corollaire 5.5.** Dans la classe des champs de cisaillement, la triangulation dirigée vaut pour tous les triplets d'abscisses ordonnées **si et seulement si** \(v\) est constante. Tout champ de cisaillement non uniforme fournit donc une violation.

**Contre-exemple 5.6 (triangulation, champ lisse, divergence nulle, sans singularité).** \(v(y) = 1 + 9y\), \(A = (0,0)\), \(B = (1,1)\), \(C = (2,0)\) :

\[
d(A,C) = 2 > 1 + 0{,}1 = 1{,}1 = d(A,B) + d(B,C).
\]

(Généralise l'exemple de [14-revue-mathematique-ciblee.md](14-revue-mathematique-ciblee.md) § 2.1 en une caractérisation complète ; contrôlé, annexe A.)

**Mécanisme 5.7.** La violation vient du **mélange de caractéristiques** : \(d(A,C)\) est mesuré sur \(\gamma_A\), \(d(B,C)\) sur \(\gamma_B\). V2 n'est pas un coût sur un espace commun de chemins ; c'est un paramètre de coordonnée longitudinale par paires. Cohérent avec l'usage historique (coordonnée de solutions de similitude), cela interdit d'utiliser V2 comme une distance au sens de (D1)–(D4) — ce que la source de 2006 annonce elle-même (« pseudo-distance »).

## 6. Non-unicité, singularités, non-existence

### 6.1 Projection non unique (V2)

Champ rotationnel \(\mathbf u = (-y, x)\) : les caractéristiques sont les cercles centrés en \(O\). Prenons \(A = (1,0)\), \(B = O\) : **tout point du cercle \(\gamma_A\) est à la distance 1 de \(B\)** ; la projection \(B^\perp\) est totalement indéterminée et \(d(A,B)\) n'a pas de valeur unique. La source historique résout ce cas par le critère \(\mathbf u \cdot \nabla c\) : le coût dépend alors de la concentration — donc de la sortie du modèle. Cette dépendance circulaire doit être documentée avant toute implémentation générale de V2 (hors périmètre G0-S). Cas moins extrême : une caractéristique courbe peut admettre plusieurs minima locaux de la distance de projection.

### 6.2 Trois états distincts (V1 et V2)

(i) accessible : \(T\) fini ; (ii) inaccessible par orientation : \(+\infty\) (C1) ; (iii) non-existence par sortie de domaine : \(\sigma(A) < T(A,B)\) (C2). La documentation du module métrique doit nommer ces trois états ; les confondre fausse les tests comme les interprétations.

### 6.3 Orbites fermées et convention de première arrivée

Sur l'orbite fermée du champ rotationnel (période \(p = 2\pi\)) : \(T(A,A) = 0\) par la convention (C3) ; le temps de retour est \(p\) ; pour \(B \ne A\) sur l'orbite, \(T(A,B) + T(B,A) = p\) (proposition 3.7). Un test qui confondrait « première arrivée » et « retour » échouerait sans que le modèle soit en cause : la convention doit être gelée avant #42.

### 6.4 Stagnation du point cible (2D)

Point selle \(\mathbf u = (x, -y)\) : depuis \(A = (0,1)\), la trajectoire est \((0, e^{-t})\) ; l'origine (stagnation) est approchée exponentiellement mais jamais atteinte : \(T(A, O) = \int_0^1 dy/y = +\infty\) (cohérent avec le corollaire 4.5, champ \(C^1\)). La proposition 3.8 ne s'applique pas (\(\mathbf u(B) = 0\)) : la dépendance en \(A\) n'est pas localement lisse près des cibles stagnantes.

### 6.5 Récapitulatif : cas où le temps « n'existe pas » ou « n'est pas unique »

| Situation | Variante | Statut |
|---|---|---|
| \(B\) hors de l'orbite positive de \(A\) | V1, V2 | \(+\infty\) par convention (C1) |
| \(B\) atteint seulement après sortie de domaine | V1, V2 | non-existence (C2) |
| champ non lipschitzien + stagnation | V1 | flot non unique (4.6) : \(T\) dépend de la branche |
| projection multiple sur \(\gamma_A\) | V2 | \(d\) non unique (6.1) |
| cible stagnante, champ \(C^1\) | V1 | \(T = +\infty\) (4.5) ; régularité perdue (3.8) |

## 7. Positionnement : objets voisins et risque de nouveauté

| Famille | Ce que c'est | Différence structurelle avec V1/V2 | Verdict pour la nouveauté |
|---|---|---|---|
| **Navigation de Zermelo / métriques de Randers** (Gibbons et al. 2009 ; Dušek 2018 ; Zermelo avec obstacles 2024 ; Markvorsen et al. 2025) | temps minimal d'un navigateur doté d'une **vitesse propre**, dans un vent ; géométrie de Randers \(F = \sqrt{h} + W\) | **contrôle** contre **pas de contrôle** : le traceur passif suit le champ, il ne choisit pas sa direction. La limite vitesse propre \(\to 0\) est **singulière** (la forte convexité \(\|W\|_h < 1\) est perdue) ; V1 en est la limite dégénérée, pas un cas particulier régulier | pas d'équivalence ; pas de nouveauté de ce côté |
| **Time-of-flight, simulation streamline** (Pollock 1988 ; Batycky et al. 1997 ; Datta-Gupta & King 2007) | \(\tau(x) = \int ds/|\mathbf u|\) depuis une source le long des lignes de courant ; coordonnée naturelle du transport en réservoir, vérifiant \(\mathbf u \cdot \nabla \tau = 1\) | V1 avec \(A\) = source : **même intégrale**. L'usage comme coordonnée de solutions de similitude est l'apport revendiqué par Drift-X, pas l'intégrale elle-même | l'intégrale est **classique** : aucune revendication possible sur elle |
| **Distances-temps** (Muller 1979, géographie) | cartographie de métriques non euclidiennes de type temps de trajet | mêmes questions d'axiomes, autre dynamique (réseaux) | idée ancienne ; caution de vocabulaire |
| **Eikonale / Hamilton–Jacobi** (Contreras & Kachroo 2020 ; Sethian & Vladimirsky 2001) | temps de première arrivée d'un front régi par une loi de vitesse, éventuellement contrôlée | sans contrôle, l'équation se réduit à l'advection linéaire \(\mathbf u \cdot \nabla \tau = 1\) ; avec contrôle, c'est un problème différent (fonction valeur) | analogue méthodologique seulement |
| **Pseudo-distance projetée** (Mohammadi & Brun 2006) | \(d(A,B) = T(A, B^\perp)\) | l'objet historique lui-même | déjà publié ; ses échecs (séparation, triangulation) y sont **annoncés** |

**Verdict (risque de nouveauté, tranché).** L'intégrale est classique (time-of-flight, distances-temps) ; la construction projetée est publiée (2006) et ses échecs d'axiomes y sont annoncés. Les caractérisations élémentaires ajoutées ici — dichotomie V1/V2, coïncidence en dimension 1 (5.1), lemme de cisaillement (5.4), critère d'ordre (4.4), barrière \(C^1\) (4.5) — sont des clarifications mathématiques de niveau licence, utiles pour délimiter le contrat du module métrique ; elles ne fondent **aucune** revendication de contribution de recherche. La conclusion du MVP relève de la catégorie « idée connue, utile pédagogiquement, délimitée précisément » ([13-mvp-scientifique-et-g0.md](13-mvp-scientifique-et-g0.md), § 3). Si un différenciel doit être cherché, ce sera dans l'**usage** des temps de parcours comme coordonnées de solutions de similitude (hors périmètre G0-S), pas dans leur définition.

## 8. Réponse à la question de l'issue : ce qui découle de la seule définition

| Propriété | V1 (première arrivée) | V2 (projetée historique) | Où |
|---|---|---|---|
| (D1) \(T(x,x)=0\) | oui, par définition | oui (hérite de V1) | 3.2 |
| (D2) positivité | oui, par définition | oui | 3.2 |
| (D4) séparation | **oui, démontrée** | **non** dès \(d \ge 2\) (dégénérescence transversale) | 3.2, 5.2 |
| (D3) triangulation dirigée | **oui, démontrée** | **non** (cisaillement non uniforme) ; oui en champ uniforme | 3.3, 5.4–5.6 |
| symétrie | non (structurelle) ; bilatérale sur les orbites fermées | non ; \(+\infty\) amont | 3.6, 3.7 |
| finitude | non : \(+\infty\) amont, non-existence par sortie | idem | 6.2 |
| unicité de la valeur | oui (flot unique sous \(C^1\)) | **non** (projection multiple) | 2.2, 6.1 |
| additivité le long d'une trajectoire | stricte en 1D ; \(\le\) en général (stricte possible sur orbites fermées) | sans objet | 3.4, 4.2 |
| propriétés physiques (conservation, positivité de \(c\), etc.) | **aucune** ne découle de la définition | idem | [14-revue-mathematique-ciblee.md](14-revue-mathematique-ciblee.md) § 3.4 |

## 9. Conséquences pour #42 (tests) et #17 (benchmarks)

Conformément à la règle de dépendance de la feuille de route (« aucun test de propriété avant les définitions de #41 »), les définitions ci-dessus gèlent le vocabulaire :

- **Contrats de test V1** : positivité/séparation ; triangulation dirigée sur le champ rotationnel (avec l'exemple 3.5 comme garde-fou d'interprétation) ; \(+\infty\) amont en 1D ; retournement \(T_{-\mathbf u}(B,A) = T_{\mathbf u}(A,B)\) — qui n'est **pas** un test de « non-symétrie » (cf. l'écart documenté dans [14-revue-mathematique-ciblee.md](14-revue-mathematique-ciblee.md) § 5) ; orbites fermées : \(T(A,B) + T(B,A) = p\).
- **Contrats de test V2** : champ uniforme (déjà implémenté) ; cisaillement : contre-exemple 5.6 comme test de non-triangulation ; refus explicite et documenté des projections non uniques (6.1) ; conventions (C1)–(C3) dans les docstrings.
- **Frontière V1/V2** : aucun test ne doit mélanger les deux variantes ; la primitive polyligne existante reste une API distincte.
- **#17** : le cas analytique minimal pour <code>benchmarks/reference</code> est le triplet {uniforme, cisaillement \(v(y) = 1+9y\), rotation} — trois champs calculables à la main, sans solveur. Aucun benchmark applicatif n'est introduit (G0-A non franchi).
- **Cas 2D synthétique (solveur)** : non requis — toutes les questions de l'issue ont été tranchées analytiquement.

## 10. Registre des incertitudes et limites

| Point | État |
|---|---|
| champs instationnaires | hors périmètre (lignes de courant ≠ trajectoires) ; aucun résultat transféré |
| critère historique exact de projection (\(\mathbf u \cdot \nabla c\)) | à relire dans la source intégrale ; dépendance circulaire documentée (6.1), non résolue |
| approximation \(B^\perp \approx B\) et facteur \(2/\pi\) (chapitre 2008) | non couverts ici ; relèvent de la reproduction de l'algorithme publié (revue ciblée § 2.1) |
| généralisation du lemme 5.4 hors cisaillement | ouverte : caractériser les classes de champs où la triangulation dirigée de V2 tient |
| dimension 3 | non traitée ; aucune raison d'attendre de meilleurs axiomes (les contre-exemples 2D s'étendent) |
| thèse (2006/2007) | non consultée ; examen différé jusqu'au dépôt (issue #44) |

## Annexe A — Contrôles numériques

Méthode : intégration RK4 indépendante des formules fermées (pas \(\le 2\cdot10^{-3}\), champs adimensionnés), comparaison aux valeurs exactes. **Ces contrôles vérifient des calculs à la main ; ils ne sont pas des benchmarks** au sens de la feuille de route.

| Contrôle | Valeur exacte | Résultat |
|---|---|---|
| rotation : \(X(\pi/2) = (0,1)\) depuis \(A=(1,0)\) | \(\pi/2\) | écart \(< 10^{-15}\) |
| rotation : \(X(3\pi/2) = (1,0)\) depuis \(B=(0,1)\) (retour fini) | \(3\pi/2\) | écart \(< 10^{-13}\) |
| rotation : sous-additivité stricte \(\pi/2 < \pi + 3\pi/2\) | — | confirmé |
| \(u = 1-x\) : \(X(-\ln 10^{-4}) = 0{,}9999\) ; \(X(20) = 1 - e^{-20} < 1\) | \(9{,}2103\) | écart \(< 10^{-6}\) ; jamais 1 |
| \(u = \sqrt{1-x}\) : \(X(2) = 1\) ; \(X(1{,}999) < 1\) | 2 | écart \(< 2\cdot10^{-3}\) |
| \(u = \sqrt{x}\) depuis \(\varepsilon\) : \(X(2(1-\sqrt{\varepsilon})) = 1\) | \(\to 2\) | confirmé (\(\varepsilon = 10^{-6}\)) |
| point selle \((x,-y)\) : \(X(50) = (0, e^{-50}) \ne (0,0)\) | jamais atteint | confirmé (\(\approx 1{,}9\cdot10^{-22} > 0\)) |
| cisaillement \(v = 1+9y\) : \(d(A,C) = 2 > 1{,}1\) | exact | confirmé |
| lemme 5.4 (équivalence) sur 300 triplets ordonnés variés | — | cohérent partout ; ~50 % de violations |
| \(\dot x = \sqrt{x}\) depuis 0 : deux solutions (0 et \((t/2)^2\)) | — | confirmé |

## Références

Sauf mention contraire, références déjà auditées dans le dépôt ([15-audit-adversarial-hallucinations.md](15-audit-adversarial-hallucinations.md), [04-revues-papiers-sources.md](04-revues-papiers-sources.md)) :

- Mohammadi, B. & Brun, J.-M. (2006). Similitude généralisée et modélisation géométrique à complexité réduite. *C. R. Mécanique* 334(10), 634–638. DOI 10.1016/j.crme.2006.06.007 — source primaire de V2.
- Brun, J.-M. & Mohammadi, B. (2008). Reduced-Order Modelling of Dispersion. Springer, CSM 16, chap. 14, p. 245–256. DOI 10.1007/978-1-4020-8758-5_14.
- Gibbons, G. W. et al. (2009). Stationary metrics and optical Zermelo-Randers-Finsler geometry. *Phys. Rev. D* 79, 044022. DOI 10.1103/PhysRevD.79.044022.
- Dušek, M. (2018). Zermelo Navigation Problem in Geometry. DOI 10.17818/NM/2018/4SI.16.
- Contreras, J. & Kachroo, P. (2020). The Viscosity Solution for Hamilton Jacobi Travel Time Dynamics. DOI 10.1109/TITS.2019.2946109.
- Sethian, J. A. & Vladimirsky, A. (2001). Ordered upwind methods for static Hamilton–Jacobi equations. PNAS 98(20).
- Muller, J.-C. (1979). La cartographie d'une métrique non euclidienne : les distances-temps. *L'Espace géographique* 8(3), 215–227. DOI 10.3406/spgeo.1979.1915.
- **Time-of-flight (ajoutées par cette passe, niveau de vérification indiqué)** :
  - Pollock, D. W. (1988), formulation des lignes de courant en termes de time-of-flight, *Ground Water* — attestation : « Pollock's method is simple, analytical, and is formulated in terms of time-of-flight (TOF) » (extraits des forums internationaux sur la simulation de réservoir, streamsim.com/papers/rsf2001.pdf et rsf2005.pdf) ; pagination exacte non recontrôlée dans cette passe, à confirmer avant usage en publication.
  - Batycky, R., Blunt, M. & Thiele, M. (1997). A 3D field-scale streamline-based reservoir simulator. *SPE Reservoir Engineering* 12, 246 — attestation via la bibliographie d'un article *Transport in Porous Media* (Springer, DOI 10.1007/s11242-015-0520-y) et le même extrait : « The time of flight describes the travel time needed by a non-reactive particle to arrive at a particular point in the reservoir given the velocity field ».
  - Datta-Gupta, A. & King, M. J. (2007). *Streamline Simulation: Theory and Practice*. Society of Petroleum Engineers — attestation via la même bibliographie Springer ; le TOF y est décrit comme coordonnée naturelle le long des lignes de courant.
