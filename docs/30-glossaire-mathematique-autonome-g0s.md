---
title: "Glossaire mathématique autonome pour G0-S"
date: 2026-10-27
status: working
---

# Glossaire mathématique autonome pour G0-S

Cette page fait partie du dépôt public **J-DriftX**. Elle contient les définitions dont le lecteur a besoin pour comprendre l'étude des temps de parcours, sans devoir consulter un wiki privé ou un autre dépôt. Elle complète l'investigation [G0-S — temps de parcours dirigé](19-investigation-g0s-temps-de-parcours.md) ; elle ne la remplace pas.

## 1. Distance, métrique et variantes

Soit $E$ un ensemble. Une fonction $d:E\times E\to[0,+\infty[$ est une **métrique** si, pour tous $x,y,z\in E$, elle vérifie les cinq axiomes suivants.

| Propriété | Définition | Signification |
|---|---|---|
| Non-négativité | $d(x,y)\geq 0$ | Une distance ne prend pas de valeur négative. |
| Diagonale nulle | $d(x,x)=0$ | Un point est à distance nulle de lui-même. |
| Séparation | $d(x,y)=0\Rightarrow x=y$ | Deux points distincts ne sont jamais confondus par la distance. |
| Symétrie | $d(x,y)=d(y,x)$ | Inverser les points ne change pas la distance. |
| Inégalité triangulaire | $d(x,z)\leq d(x,y)+d(y,z)$ | Passer par un point intermédiaire ne raccourcit pas la distance par rapport au coût direct. |

Le terme **distance** désigne parfois, de manière informelle, une mesure d'écart qui ne vérifie pas tous ces axiomes. Pour éviter cette ambiguïté, J-DriftX précise les axiomes vérifiés au lieu de déduire le mot « métrique » de la seule interprétation physique.

### Variantes utiles dans J-DriftX

- Une **pseudo-métrique** vérifie la non-négativité, la diagonale nulle, la symétrie et l'inégalité triangulaire, mais la séparation peut échouer : deux points distincts peuvent être à distance nulle.
- Une **quasi-métrique dirigée** (convention de terminologie variable selon les sources) autorise l'échec de la symétrie. Selon la convention, la séparation et l'inégalité triangulaire restent exigées.
- Une **quasi-distance étendue dirigée**, au sens utilisé ici pour V1, prend ses valeurs dans $[0,+\infty]$ et vérifie la diagonale nulle, la non-négativité, la séparation et l'inégalité triangulaire dirigée. Elle peut valoir $+\infty$ lorsque la cible n'est pas atteinte et elle n'est pas nécessairement symétrique. Ce n'est donc pas une métrique au sens strict.

Pour V1, la convention $T(A,B)=+\infty$ en l'absence d'arrivée est utile pour représenter l'inaccessibilité dans le sens du flot. Elle doit toutefois être distinguée d'une non-existence de la trajectoire dans le domaine : ce dernier cas relève du temps maximal de solution et des conventions de sortie de domaine.

## 2. Pourquoi tester chaque propriété séparément ?

Une propriété ne découle pas du fait qu'une quantité soit positive, exprimée en secondes ou appelée « distance ». Il faut une preuve sous des hypothèses identifiées. Un contre-exemple suffit, en revanche, à montrer qu'une propriété ne peut pas être garantie dans le cadre général considéré.

| Propriété | V1 : temps de première arrivée | V2 : temps après projection |
|---|---|---|
| Non-négativité | Oui, par définition du temps $t\geq0$, avec $+\infty$ autorisé | Oui lorsque la projection est définie et que V2 est calculée comme un temps V1 |
| Diagonale nulle | Oui : $T(A,A)=0$, puisque $t=0$ est admis | Oui si la projection de $A$ sur sa propre caractéristique est bien définie et vaut $A$ |
| Séparation | Oui dans le cadre du flot continu et univoque retenu ; un temps nul implique la même position initiale et finale | Pas garantie en dimension 2 : une projection peut coïncider avec $A$ alors que $B\ne A$ |
| Symétrie | Pas garantie : le flot est orienté dans le temps | Pas garantie ; la projection et le flot sont orientés et peuvent dépendre du point de départ |
| Inégalité triangulaire | Oui sous les hypothèses d'un flot autonome univoque, via la propriété de semi-groupe | Pas garantie en général : les projections intermédiaires ne se composent pas comme des segments de trajectoire |
| Finitude | Pas garantie : une cible peut être inaccessible ou seulement approchée asymptotiquement | Pas garantie, notamment si la projection cible n'est pas atteignable dans le sens positif |

Ce tableau est un résumé des résultats du document d'investigation, pas une preuve autonome. Les conditions exactes et les contre-exemples sont détaillés dans [l'investigation G0-S](19-investigation-g0s-temps-de-parcours.md), notamment ses sections 3 à 6.

## 3. Champ lipschitzien : définition et rôle

Soit $u:E\to\mathbb R^d$, où $E\subseteq\mathbb R^d$. Le champ $u$ est **lipschitzien** sur $E$ s'il existe une constante $L\geq0$ telle que, pour tous $x,y\in E$,
$$
\|u(x)-u(y)\|\leq L\|x-y\|.
$$
La constante $L$ est une constante de Lipschitz. Le champ est **localement lipschitzien** si cette condition est satisfaite dans un voisinage de chaque point. Si $u\in C^1$, alors $u$ est localement lipschitzien sur son domaine ouvert ; la réciproque est fausse.

### Pourquoi cette hypothèse intervient-elle ?

Pour l'équation différentielle ordinaire
$$
\dot X(t)=u(X(t)),\qquad X(0)=A,
$$
la continuité du champ assure notamment l'existence locale d'au moins une solution (théorème de Peano), mais **ne garantit pas à elle seule son unicité**. Une hypothèse locale de Lipschitz est une condition suffisante standard pour l'existence et l'unicité locales (théorème de Cauchy–Lipschitz/Picard–Lindelöf). Elle permet de définir un flot $X(t;A)$ non ambigu, puis d'utiliser sa propriété de semi-groupe pour démontrer l'inégalité triangulaire de V1.

Il faut distinguer les implications :
- $u\in C^1\Rightarrow u$ localement lipschitzien $\Rightarrow$ unicité locale ;
- $u$ seulement continu $\Rightarrow$ existence locale sous les hypothèses usuelles, mais pas nécessairement unicité ;
- la condition de Lipschitz est suffisante, pas nécessaire : certains champs non lipschitziens ont tout de même un flot unique.

### Contre-exemple explicite : continuité sans unicité

Considérons
$$
\dot x=\sqrt{x},\qquad x(0)=0,\qquad x\geq0.
$$
La solution $x(t)=0$ existe. Mais pour tout délai $\tau\geq0$, la fonction
$$
x_\tau(t)=
\begin{cases}
0,&0\leq t\leq\tau,\\
\dfrac{(t-\tau)^2}{4},&t\geq\tau
\end{cases}
$$
est également une solution : après le délai, sa dérivée vaut $(t-\tau)/2=\sqrt{x_\tau(t)}$, et avant le délai les deux membres valent zéro. Le champ est continu, mais non localement lipschitzien en zéro, et plusieurs solutions issues du même état sont possibles.

**Conséquence pour le temps de parcours :** la formule obtenue sur une branche mobile ne suffit pas à définir un temps unique si l'équation ne détermine pas une trajectoire unique.

## 4. Temps de première arrivée (hitting time)

Dans le cadre retenu par G0-S, $u:\Omega\to\mathbb R^d$ est un champ stationnaire suffisamment régulier pour que la solution maximale $X(t;A)$ issue de $A$ soit unique. Son intervalle maximal d'existence est noté $I_A$, avec $0\in I_A$.

Le **temps de première arrivée** de $B$ depuis $A$ est
$$
T(A,B)=\inf\{t\in I_A\cap[0,+\infty[\mid X(t;A)=B\},
\qquad \inf\varnothing=+\infty.
$$
Autrement dit, c'est le premier temps non négatif où la trajectoire issue de $A$ atteint $B$, si elle l'atteint pendant son existence. Le temps $t=0$ est admis : ainsi $T(A,A)=0$. Le **temps de retour** en $A$, lui, désigne généralement le premier temps strictement positif où une trajectoire revient en $A$, s'il existe ; il s'agit d'une autre quantité.

Pourquoi définir l'ensemble sur $I_A$ ? Parce qu'une solution ne peut être évaluée après la fin de son intervalle maximal. Écrire simplement $t\geq0$ sans cette restriction masque cette condition d'existence.

Si $B$ n'appartient pas à l'orbite positive de $A$, la convention donne $T(A,B)=+\infty$. Si la trajectoire quitte le domaine avant d'atteindre $B$, il faut signaler cette sortie comme telle plutôt que confondre automatiquement les causes d'inaccessibilité.

## 5. Composante connexe sans stagnation en dimension 1

En dimension 1, soit $u:I\to\mathbb R$ un champ continu sur un intervalle $I$. Un **point de stagnation** est un point $x^*$ où $u(x^*)=0$. L'ensemble
$$
I\setminus\{x\in I:u(x)=0\}
$$
est l'ensemble des points non stagnants. Une **composante connexe** de cet ensemble est un sous-ensemble connexe maximal ; sur la droite réelle, chaque composante est un intervalle.

Sur une telle composante, $u$ ne s'annule pas et, par continuité, conserve un signe constant. La trajectoire y est donc monotone tant qu'elle y reste. Cela ne signifie pas qu'elle visite les points dans les deux sens : elle avance seulement dans le sens indiqué par le signe de $u$.

Cette précision est essentielle pour comparer V1 et V2 en dimension 1. La coïncidence $V2=V1$ ne doit pas être affirmée pour deux points quelconques d'une même composante sans préciser l'orientation : la cible $b$ doit être atteignable depuis $a$ dans le temps positif, avant une éventuelle sortie du domaine. Si $u>0$, par exemple, $b>a$ est dans le sens du flot et
$$
T(a,b)=\int_a^b\frac{dx}{u(x)},
$$
tandis que $b<a$ n'est pas atteint dans le temps positif et $T(a,b)=+\infty$ selon la convention de V1.

## 6. Orbite périodique et asymétrie

Une trajectoire $X(t;A)$ est **périodique** s'il existe $p>0$ tel que $X(t+p;A)=X(t;A)$ pour tout temps où l'expression est définie. La **période minimale** est le plus petit $p>0$ satisfaisant cette propriété, lorsqu'il existe. L'orbite géométrique est l'ensemble des points parcourus par cette trajectoire.

Exemple : le champ stationnaire
$$
\dot x=-y,\qquad \dot y=x
$$
a pour solution issue de $A=(1,0)$,
$$
X(t;A)=(\cos t,\sin t),
$$
une orbite circulaire de période minimale $2\pi$. Pour deux points distincts $A,B$ sur ce cercle, le temps de première arrivée de $B$ depuis $A$ est fini dans le sens positif, et le temps de première arrivée de $A$ depuis $B$ est lui aussi fini. La somme des deux temps vaut $2\pi$ si $A$ et $B$ sont distincts sur une orbite de période minimale.

Cet exemple montre que V1 est **non symétrique en général, mais pas nécessairement asymétrique pour chaque paire**. À l'inverse, pour le champ uniforme unidimensionnel $u(x)=U>0$, on a $T(a,b)=(b-a)/U$ si $b>a$ et $T(a,b)=+\infty$ si $b<a$. Ce contre-exemple établit que la symétrie n'est pas une propriété générale de V1.

## 7. Pourquoi l'intégrale seule ne définit pas toujours la dynamique

Sur une branche mobile monotone, la séparation des variables dans $\dot x=u(x)>0$ donne
$$
t=\int_{x(0)}^{x(t)}\frac{ds}{u(s)}.
$$
Si $u(x)\sim c|x-x^*|^\alpha$ près d'une stagnation, avec $c>0$ et $\alpha>0$, le temps le long de cette branche est comparable à
$$
\int_0^\delta\frac{dr}{c r^\alpha}.
$$
Cette intégrale converge si et seulement si $\alpha<1$.

Mais cette convergence répond uniquement à la question : **combien de temps dure la branche mobile choisie ?** Elle ne répond pas à la question distincte : **la condition initiale détermine-t-elle une seule solution ?**

Pour $u(x)=\sqrt{x}$, le calcul donne $2\sqrt b$ pour la branche mobile qui part immédiatement de zéro et atteint $b>0$. Pourtant, les solutions $x(t)=0$ et $x_\tau(t)$ décrites plus haut peuvent rester à zéro, ou y attendre un délai arbitraire avant de partir. L'intégrale ne sélectionne ni la branche stationnaire, ni le délai, ni une convention de sélection. Par conséquent, elle ne définit pas à elle seule un temps de première arrivée **univoque** lorsque l'unicité échoue.

Pour rendre le modèle bien défini, il faut alors au moins l'une des options suivantes :
1. imposer des hypothèses assurant l'unicité du flot, par exemple un champ localement lipschitzien ;
2. définir explicitement une règle de sélection de branche ou une convention d'attente ;
3. abandonner la valeur unique et définir un objet différent, par exemple l'ensemble des temps d'arrivée possibles.

Ces options ne sont pas équivalentes. Le MVP-S retient le cadre à flot unique pour V1 ; les exemples non lipschitziens servent à expliquer les limites du calcul intégral, et non à étendre silencieusement la définition de V1.

## 8. Contre-exemples de référence

| Contre-exemple | Ce qu'il démontre | Ce qu'il ne démontre pas |
|---|---|---|
| $u(x)=U>0$ sur la droite | V1 peut être non symétrique et étendue ($+\infty$ dans le sens inaccessible) | Que V1 soit asymétrique pour toute paire |
| $\dot x=\sqrt{x},\ x(0)=0$ | Un champ continu non lipschitzien peut avoir plusieurs solutions ; une intégrale finie sur une branche ne suffit pas | Que tous les champs non lipschitziens aient des solutions non uniques |
| $\dot x=x$ au point $x=0$ | La solution issue de la stagnation reste à zéro dans ce champ lipschitzien | Que toute stagnation soit une barrière pour un champ seulement continu |
| $\dot x=\sqrt{1-x}$ au voisinage de $x=1$ | Une cible stagnante peut être atteinte en temps fini lorsque le champ n'est pas $C^1$ au point cible | Que ce comportement soit possible sous l'hypothèse $C^1$ |
| $\dot x=-y,\ \dot y=x$ | Une orbite périodique permet des arrivées finies dans les deux sens entre deux points distincts de l'orbite | Que le temps de parcours soit une métrique symétrique |
| V2 avec projection non unique (exemple détaillé dans l'investigation G0-S, § 6.1) | La construction projetée peut ne pas définir une valeur scalaire unique sans règle de projection | Que toute projection dans tout champ soit non unique |

Les contre-exemples sont des diagnostics de portée logique. Ils ne remplacent ni les démonstrations générales ni les tests du code. La matrice de traçabilité du projet relie les affirmations aux définitions, aux preuves, aux implémentations et aux tests : [matrice de traçabilité MVP-S](27-matrice-tracabilite-mvp-s.md).


## 9. Flot, semi-groupe, atteignabilité et projection

### Flot et propriété de semi-groupe

Lorsque le problème initial
$$
\dot X(t)=u(X(t)),\qquad X(0)=A
$$
admet une solution unique, on peut noter $X(t;A)$ la position au temps $t$. Pour un champ autonome, l'évolution ne dépend pas explicitement de l'horloge : si la trajectoire existe aux temps concernés, elle vérifie
$$
X(t+s;A)=X\bigl(t;X(s;A)\bigr).
$$
C'est la **propriété de semi-groupe** du flot. Elle signifie qu'évoluer pendant $s+t$ revient à évoluer d'abord pendant $s$, puis pendant $t$ depuis la position atteinte. Cette identité repose sur l'unicité : sans elle, le membre de droite ne désigne pas nécessairement la même branche de solution.

Elle fournit la preuve de l'inégalité triangulaire dirigée de V1. Si $B$ est atteint depuis $A$ au temps $s$ et $C$ est atteint depuis $B$ au temps $t$, la propriété de semi-groupe donne $X(s+t;A)=C$. Ainsi, le premier temps d'arrivée de $C$ depuis $A$ satisfait
$$
T(A,C)\leq s+t=T(A,B)+T(B,C),
$$
lorsque les deux temps d'arrivée sont finis et les trajectoires existent jusqu'aux instants considérés. Si l'un des termes du membre de droite vaut $+\infty$, l'inégalité étendue est triviale. Cette preuve ne s'applique pas automatiquement à une quantité qui n'est pas construite à partir du même flot, comme V2 projetée.

### Atteignabilité et temps infini

Dire que $B$ est **atteignable depuis $A$ dans le temps positif** signifie qu'il existe $t\in I_A\cap[0,+\infty[$ tel que $X(t;A)=B$. Ce terme porte sur une arrivée exacte en temps fini, pas seulement sur une limite asymptotique. Par exemple, pour $\dot x=1-x$ avec $x(0)=0$, la solution $x(t)=1-e^{-t}$ tend vers $1$ mais ne l'atteint à aucun temps fini ; selon la définition de première arrivée ci-dessus, $T(0,1)=+\infty$. À l'inverse, pour $\dot x=\sqrt{1-x}$ sur le domaine $x\leq1$, la branche issue de $x(0)=0$ atteint $1$ au temps fini $2$, même si le champ n'est pas localement lipschitzien au point cible. Cet exemple appartient à une extension non $C^1$ et ne contredit pas les résultats formulés sous l'hypothèse de base $C^1$.

### Projection et définition de V2

Dans la référence codée en champ uniforme non nul $u\in\mathbb R^2$, la direction unitaire du champ est $e=u/\|u\|$. Le déplacement longitudinal de $A$ vers $B$ est $(B-A)\cdot e$. La fonction `pseudo_distance_uniforme` calcule
$$
V2(A,B)=
\begin{cases}
\dfrac{(B-A)\cdot u}{\|u\|^2}, & (B-A)\cdot u\geq0,\\
+\infty, & (B-A)\cdot u<0.
\end{cases}
$$
La formule est un temps longitudinal pour la convention locale choisie ; elle ignore le déplacement transversal. En particulier, un déplacement transversal non nul peut donner zéro : V2 ne satisfait donc pas la séparation des points. La formule suppose un champ uniforme et ne doit pas être extrapolée à un champ variable sans définir comment la caractéristique est construite, si plusieurs projections sont possibles et comment les cibles non atteignables sont traitées.

### Carte explicite entre notions, documentation et code

| Notion | Définition / preuve publique | Code actuel | Portée effective |
|---|---|---|---|
| Temps de première arrivée 1D à vitesse constante | Section 4 de cette page et annexe B du bilan MVP-S 1D | `temps_premiere_arrivee_1d` dans [`src/jdriftx/metric.py`](../src/jdriftx/metric.py) | Cas analytique constant uniquement |
| Coût discret d'une polyligne | Définition de la primitive dans le [module](../src/jdriftx/metric.py) et la [matrice](27-matrice-tracabilite-mvp-s.md) | `temps_transport` | Somme longueur/norme de vitesse ; ne tient pas compte du signe du vent |
| V2 uniforme projetée | Formule ci-dessus et investigation G0-S, section 6 | `pseudo_distance_uniforme` | Champ constant non nul en 2D ; convention amont explicite |
| Propriétés générales du flot V1 | Sections 2 à 7 de l'[investigation G0-S](19-investigation-g0s-temps-de-parcours.md) | Pas de solveur général de champ variable | Résultats analytiques sous hypothèses ; pas validés par les seuls tests de la primitive 1D |
| Contre-exemple de non-unicité | Section 3 et section 7 de cette page | Exemple mathématique documenté, non implémenté comme solveur ODE dans `src/` | Sert à préciser les limites logiques ; ce n'est pas une fonctionnalité logicielle |

Les tests de `tests/test_metric.py` vérifient des cas ciblés des primitives implémentées. Ils ne démontrent ni l'existence d'un flot pour tout champ, ni l'unicité générale, ni les propriétés analytiques universelles de V1, ni la validité physique de la méthode historique. Pour chaque affirmation générale, la preuve et ses hypothèses restent la référence ; pour chaque comportement logiciel, le code et les tests constituent la référence d'implémentation.
