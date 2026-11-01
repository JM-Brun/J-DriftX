# 59 — GZ-1 : intuitions, démonstrations et régime supercritique

Cette note accompagne la page canonique [Navigation de Zermelo, fronts et Hamilton–Jacobi](../site/theorie/navigation-fronts-controllabilite.qmd). Elle développe les intuitions, déroule les démonstrations et relie les affirmations aux tests du dépôt.

**Statut épistémique.** Les preuves analytiques établissent des propriétés du modèle idéal. Les tests contrôlent la cohérence de certaines implémentations float64 ; ils ne constituent ni une preuve mathématique indépendante, ni une validation physique, ni une validation d'un solveur HJ.

## 1. Le modèle en une image mentale

GZ-1 part d'un puff gaussien tridimensionnel en espace libre, issu d'une émission impulsionnelle de masse $M$. Le vent uniforme $u$ translate le centre sans déformer la sphère ; la diffusion isotrope de coefficient constant $K$ élargit le puff. Un seuil $C_0$ découpe une sphère dont le rayon évolue dans le temps.

La navigation ajoute un mobile contrôlable :
$$
\dot X=u+s,\qquad \|s(t)\|\leq c(t),\qquad c(t)=R'(t).
$$
Le vent est imposé ; $s$ est la vitesse relative que le mobile peut choisir. La borne est exactement la vitesse d'expansion du rayon du seuil. C'est une **hypothèse de contrôle construite à partir du modèle gaussien**, pas une loi physique générale disant qu'un mobile atmosphérique peut se déplacer à cette vitesse.

Hypothèses indispensables : espace $\mathbb R^3$ sans paroi ni sol ; $u$ uniforme et constant ; $K>0$ isotrope et constant ; émission ponctuelle initiale de masse $M>0$ ; seuil $C_0>0$ constant ; cible fixe $x_B\ne x_0$ ; contrôle mesurable avec borne presque partout $R'(t)$ sur la seule phase $0<t\leq t_*$.

Le modèle exclut les frontières, le dépôt, les réactions, les sources continues, les vents variables, la turbulence anisotrope et les conditions météorologiques réelles.

## 2. Du noyau gaussien au rayon du seuil

Le noyau fondamental est
$$
C(x,t)=\frac{M}{(4\pi Kt)^{3/2}}
\exp\left(-\frac{\|x-x_0-ut\|^2}{4Kt}\right).
$$

Deux facteurs ont une interprétation simple :

1. $M/(4\pi Kt)^{3/2}$ est la concentration au centre. La masse ne disparaît pas : elle se répartit dans un volume caractéristique qui croît comme $(Kt)^{3/2}$.
2. L'exponentielle fait décroître la concentration avec la distance au centre advecté $x_0+ut$. L'isotropie de $K$ rend les niveaux sphériques.

À seuil $C=C_0$, on prend le logarithme :
$$
\ln\frac{M}{C_0(4\pi Kt)^{3/2}}
=\frac{\|x-x_0-ut\|^2}{4Kt}.
$$
En posant
$$
\Lambda(t)=\ln\frac{M}{C_0(4\pi Kt)^{3/2}},
$$
le carré du rayon est donc $R(t)^2=4Kt\Lambda(t)$. La condition $\Lambda(t)\geq0$ est précisément la condition d'existence d'un niveau réel.

On définit
$$
t_* = \frac{1}{4\pi K}
\left(\frac{M}{C_0e^{3/2}}\right)^{2/3}.
$$
Ce choix donne $\Lambda(t_*)=3/2$. Puisque
$$
\Lambda(t)=\frac32+\frac32\ln\frac{t_*}{t},
$$
on obtient
$$
R(t)^2=6Kt\left(1+\ln\frac{t_*}{t}\right).
$$

Pour dériver le rayon sans manipuler directement une racine, on dérive $R^2$ :
$$
2RR'=4K(\Lambda+t\Lambda')
=4K\left(\Lambda-\frac32\right),
$$
car $\Lambda'=-3/(2t)$. Ainsi
$$
c(t)=R'(t)=\frac{2K}{R(t)}\left(\Lambda(t)-\frac32\right)
=\frac{3K}{R(t)}\ln\frac{t_*}{t}.
$$

Le signe est désormais lisible : $c(t)>0$ avant $t_*$, $c(t_*)=0$, puis $c(t)<0$ pendant la contraction. Le niveau disparaît à $t_{\rm ext}=et_*$. Le contrôle ne peut pas avoir une borne de norme négative ; GZ-1 est donc limité à $0<t\leq t_*$. De plus, $R'(t)\to+\infty$ quand $t\to0^+$, mais
$$
\int_0^t R'(\tau)\,d\tau=R(t)<\infty.
$$
La singularité est intégrable : les contrôles construits peuvent être non bornés près de zéro tout en étant intégrables.

## 3. Démonstration GZ-1 : l'ensemble atteignable exact

Le résultat à démontrer est
$$
\mathcal R(t)=\overline B(x_0+ut,R(t)).
$$
Il faut établir les deux inclusions. Une seule ne suffit pas.

### 3.1 Première inclusion : aucune trajectoire ne sort de la boule

On soustrait le mouvement du centre du puff :
$$
X(t)-(x_0+ut)=\int_0^t s(\tau)\,d\tau.
$$
L'inégalité triangulaire pour l'intégrale donne
$$
\begin{aligned}
\|X(t)-(x_0+ut)\|
&\leq\int_0^t\|s(\tau)\|\,d\tau\\
&\leq\int_0^tR'(\tau)\,d\tau\\
&=R(t)-R(0^+)=R(t).
\end{aligned}
$$
Intuition : le mobile dispose d'un budget total de déplacement relatif égal à l'intégrale de sa vitesse maximale. Ce budget vaut exactement $R(t)$. Aucune stratégie de commande ne peut produire un déplacement relatif plus grand.

On a donc $\mathcal R(t)\subseteq\overline B(x_0+ut,R(t))$.

### 3.2 Inclusion réciproque : construire une commande qui atteint chaque point

L'inclusion précédente ne dit pas si tous les points de la boule sont réellement atteignables. Il faut construire une commande.

Fixons un déplacement relatif $z$ tel que $\|z\|\leq R(t)$. Pour $z\ne0$, posons
$$
s(\tau)=\frac{z}{R(t)}R'(\tau).
$$
Le facteur $z/R(t)$ est un vecteur constant de norme au plus un. Par conséquent,
$$
\|s(\tau)\|=\frac{\|z\|}{R(t)}R'(\tau)\leq R'(\tau).
$$
Et son intégrale vaut exactement
$$
\int_0^t s(\tau)\,d\tau
=\frac{z}{R(t)}\int_0^tR'(\tau)\,d\tau=z.
$$
Pour $z=0$, on choisit $s=0$.

Cette commande garde une **direction constante dans le référentiel mobile** et module seulement sa norme selon $R'(\tau)$. Elle utilise exactement la fraction $\|z\|/R(t)$ du budget de déplacement disponible. Ainsi, chaque point de la boule est atteignable :
$$
\overline B(x_0+ut,R(t))\subseteq\mathcal R(t).
$$
Les deux inclusions donnent l'égalité. La construction repose fortement sur le fait que la borne dépend du temps, mais ni de la position ni de la direction.

### 3.3 De l'ensemble atteignable à l'égalité des temps

Par définition, la cible est atteignable à l'instant $t$ si et seulement si
$$
x_B\in\mathcal R(t)
\quad\Longleftrightarrow\quad
\|x_B-(x_0+ut)\|\leq R(t).
$$
Le membre de droite est exactement la condition de contact avec la boule du front. Les ensembles d'instants admissibles de $T_{\rm nav}$ et $T_{\rm front}$ sont donc identiques ; leurs infimums sont égaux :
$$
\boxed{T_{\rm nav}=T_{\rm front}.}
$$

**Ce qui n'est pas démontré :** cette preuve ne donne pas $T_{\rm nav}=T_{\rm arr}$. Le temps passif $T_{\rm arr}$, le temps contrôlé $T_{\rm nav}$, le premier contact $T_{\rm front}$ et le coût historique projeté $T_{\rm proj}$ sont des objets distincts.

## 4. Pourquoi l'équation HJ a un plateau nul

Pour un contrôle dans la boule $\|s\|\leq c(x,t)$, le Hamiltonien est le support de l'ensemble des vitesses :
$$
H(x,t,p)=\sup_{\|s\|\leq c}(u+s)\cdot p.
$$
Cauchy–Schwarz donne $s\cdot p\leq c\|p\|$, avec égalité pour $s=cp/\|p\|$ si $p\ne0$. Donc
$$
H=u\cdot p+c\|p\|,
\qquad
\phi_t+u\cdot\nabla\phi+c\|\nabla\phi\|=0.
$$

Pour GZ-1, il faut résoudre le problème de départ ponctuel avec $\phi(x,0)=\|x-x_0\|$. La fonction signée $\|x-x_0-ut\|-R(t)$ a le bon niveau zéro, mais n'est pas la solution de viscosité globale : à l'intérieur, elle est négative, alors que la formule de Hopf–Lax conserve un plateau nul.

La dérivation se fait en deux transformations :

1. Référentiel mobile $y=x-ut$, $\psi(y,t)=\phi(y+ut,t)$. Le vent disparaît :
   $$
   \psi_t+c(t)\|\nabla_y\psi\|=0.
   $$
2. Temps cumulé $\rho=R(t)=\int_0^t c(\tau)d\tau$. Sur $0<t<t_*$, $R$ est strictement croissant et la singularité initiale est absorbée dans cette intégrale finie.

On obtient l'éikonale standard $\psi_\rho+\|\nabla_y\psi\|=0$, avec donnée $\psi(y,0)=\|y-x_0\|$. Hopf–Lax donne
$$
\psi(y,\rho)=\inf_{\|y-z\|\leq\rho}\|z-x_0\|
=\max(\|y-x_0\|-\rho,0).
$$
Si $x_0$ appartient à la boule $\overline B(y,\rho)$, le minimum est zéro ; sinon, le point le plus proche de $x_0$ est le point de cette boule situé sur le segment $[y,x_0]$.

En revenant au référentiel fixe :
$$
\boxed{\phi(x,t)=\max(\|x-x_0-ut\|-R(t),0).}
$$
Son ensemble nul est la boule atteignable entière ; le front géométrique est sa frontière. La distance signée peut être réutilisée après réinitialisation numérique, mais ne doit pas être confondue avec cette fonction valeur. Le coin sur la frontière relève de la notion de solution de viscosité ; un résidu classique ponctuel n'y est pas défini.

Cette preuve par reparamétrisation est spécifique au vent uniforme et à $c(t)=R'(t)$. Elle ne justifie pas directement le cas $u(x,t)$ ou $c(x,t)$.

## 5. Randers : d'où vient la formule et pourquoi elle dégénère

À un instant fixé, la vitesse absolue est $v=u+s$, avec $\|s\|\leq c$. Pour réaliser un déplacement $v$ en un temps $F(v)$, la vitesse relative moyenne doit vérifier
$$
\left\|\frac{v}{F(v)}-u\right\|=c.
$$
Après multiplication par $F(v)$ et élévation au carré :
$$
\|v\|^2-2F(u\cdot v)+F^2\|u\|^2=c^2F^2.
$$
En posant $A=c^2-\|u\|^2$, on obtient
$$
AF^2+2(u\cdot v)F-\|v\|^2=0.
$$
Pour $A>0$, la racine positive est
$$
F(v)=\frac{\sqrt{(u\cdot v)^2+A\|v\|^2}-u\cdot v}{A}.
$$
En séparant le radical et le terme linéaire, on lit la forme de Randers :
$$
a_{ij}=\frac{A\delta_{ij}+u_i u_j}{A^2},
\qquad b_i=-\frac{u_i}{A}.
$

La régularité peut aussi se vérifier algébriquement. Pour tout $\xi\ne0$,
$
\xi^i a_{ij}\xi^j=\frac{A\|\xi\|^2+(u\cdot\xi)^2}{A^2}>0,
$
ce qui montre que $a$ est définie positive. Son inverse est
$
a^{ij}=A\delta_{ij}-\frac{A}{c^2}u_i u_j,
$
et donc
$
b_i a^{ij}b_j=\frac{\|u\|^2}{c^2}<1.
$
C'est la condition de régularité de Randers : la norme duale de $b$ relativement à $a$ est strictement inférieure à un.

L'intuition géométrique est simple : la boule des vitesses absolues est $\overline B(u,c)$. Si $c>\|u\|$, l'origine est à l'intérieur et toutes les directions sont accessibles ; la jauge de Randers est régulière. Si $c\leq\|u\|$, certaines directions deviennent inaccessibles : la formule ne définit plus une métrique de Randers régulière sur tout l'espace tangent. Dans GZ-1, $c(t)$ varie ; la formule décrit une géométrie instantanée et n'est pas une métrique stationnaire globale.

## 6. Régime supercritique : dériver le cône, pas extrapoler Randers

Considérons maintenant $c$ constant, $u$ constant et $\|u\|\geq c$. À l'instant $t$, l'ensemble atteignable depuis l'origine est $\overline B(ut,ct)$.

Pour un déplacement $d\omega$, $d>0$, $\|\omega\|=1$, il faut qu'il existe $t>0$ tel que
$$
\|d\omega-ut\|\leq ct.
$$
Posons $q=d/t>0$. Après division par $t$, on obtient
$$
q^2-2q(u\cdot\omega)+\|u\|^2-c^2\leq0.
$$
Une racine strictement positive existe si et seulement si
$$
u\cdot\omega>0,
\qquad
\Delta=(u\cdot\omega)^2+c^2-\|u\|^2\geq0.
$$
En notant $\theta$ l'angle entre $u$ et $\omega$, cela équivaut à
$$
u\cdot\omega>0,
\qquad
\sin\theta\leq\frac{c}{\|u\|}.
$$
C'est un **cône aval** : la condition sur le sinus seule serait incorrecte, car elle inclurait aussi le cône amont autour de $-u$.

Pour $c<\|u\|$, la frontière $\sin\theta=c/\|u\|$ est incluse : la demi-droite est tangente à la boule mobile en un point strictement positif. Au cas critique $c=\|u\|$, les directions exactement transverses ont $u\cdot\omega=0$ et ne sont pas atteignables en temps fini.

La plus grande racine positive
$$
q_+=u\cdot\omega+\sqrt{(u\cdot\omega)^2+c^2-\|u\|^2}
$$
maximise $q=d/t$ et donne le temps minimal :
$$
T(d\omega)=\frac{d}{u\cdot\omega+\sqrt{(u\cdot\omega)^2+c^2-\|u\|^2}}.
$$
Hors du cône aval, $T=+\infty$ par convention. Cette dérivation est exacte pour $u,c$ constants ; elle **ne résout pas** le cas instationnaire supercritique $c(t)=R'(t)$.

## 7. Matrice de traçabilité : affirmations et tests

| Affirmation | Test | Ce que le test contrôle | Limite |
|---|---|---|---|
| Seuil gaussien atteint sur $R(t)$ | test_le_front_d_isoconcentration_est_exact | Cohérence du rayon avec le noyau | Pas de validation physique |
| $c(t)=R'(t)$ | test_la_vitesse_d_expansion_est_la_derivee_du_rayon | Dérivée numérique hors singularité | Pas de validation du contrôle |
| $t_*$ maximise $R$, $R(et_*)=0$ | test_t_etoile_maximise_le_rayon | Cas limites de la formule | Pas une preuve analytique |
| $R'$ diverge mais est intégrable | test_la_singularite_initiale_est_integrable | Quadrature sur intervalle tronqué | L'intégrabilité exacte vient de $R(t)-R(0)$ |
| $T_{\rm nav}=T_{\rm front}$ | test_le_theoreme_gz1_egalise_navigation_et_front | Une trajectoire constructive et sa borne | La preuve générale est la double inclusion §3 |
| Commande radiale et ensemble atteignable | test_la_commande_radiale_remplit_exactement_la_boule | Dérivée de la primitive et respect de la borne | Test de cohérence, pas preuve générale |
| Cible hors de portée | test_une_cible_hors_de_portee_n_est_jamais_atteinte | Balayage temporel discret | Ne prouve pas l'absence de contact entre mailles |
| Jauge Zermelo = Randers | test_la_jauge_sous_critique_est_une_randers | Identité algébrique, homogénéité et norme duale de b | Domaine sous-critique seulement |
| Cône aval et cas critique | test_le_regime_supercritique_definit_un_cone | Intérieur, frontière, amont et direction transverse critique | Cas constant uniquement |
| Équation HJ | test_le_front_satisfait_l_equation_hamilton_jacobi | Résidu classique extérieur et plateau intérieur | Le coin est traité analytiquement par Hopf–Lax |
| Eikonale stationnaire | test_l_eikonale_stationnaire_en_champ_uniforme | Résidu de la solution fermée | Ne valide pas le HJ instationnaire |

Les onze tests sont des tests de cohérence déterministes en float64. Ils ne remplacent pas la preuve et ne démontrent pas une validité atmosphérique.

## 8. Frontières de validité et prochaines étapes

**Établi analytiquement :** rayon du seuil, vitesse d'expansion, ensemble atteignable GZ-1, égalité $T_{\rm nav}=T_{\rm front}$, solution Hopf–Lax dans le cas uniforme, jauge de Randers sous-critique et cône aval à borne constante.

**Contrôlé numériquement :** cohérence des formules et résidus lisses décrits dans la matrice. Le balayage discret d'une cible hors de portée reste un diagnostic, pas une preuve d'absence de zéro.

**Non établi :** vent spatialement variable, cible mobile, départ à âge positif, classe de contrôles globalement bornés, régime supercritique instationnaire, front d'une EDP d'advection–diffusion générale, validité physique de $c(t)$, solveur HJ convergent.

La suite rationnelle est de stabiliser cet oracle analytique avant de développer un solveur HJ. Toute extension doit recevoir son propre énoncé, ses hypothèses, une preuve ou un contre-exemple, puis des tests numériques séparés.
