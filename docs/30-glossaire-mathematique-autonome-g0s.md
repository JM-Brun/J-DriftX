---
title: "Notions mathématiques des temps de parcours dirigés"
date: 2026-10-27
status: working
---

# Notions mathématiques des temps de parcours dirigés

Cette page fait partie du dépôt public **J-DriftX**. Elle rassemble les définitions nécessaires pour comprendre les temps de première arrivée et les propriétés mathématiques étudiées dans le « socle mathématique des temps de parcours dirigés » (nom de travail G0-S). Elle complète l’[investigation sur les temps de parcours dirigés](19-investigation-g0s-temps-de-parcours.md) ; elle ne la remplace pas.

**Comment lire le nom « G0-S ».** « G0-S » n'est pas une notion mathématique : c'est le repère d'un chantier dans la feuille de route du projet, à lire « G zéro S ». **G0** désigne le premier jalon de cadrage ; le suffixe **S** désigne l'axe **scientifique**, par opposition à l'axe applicatif **G0-A**, dont l'objet — l'utilité pratique — reste non démontré (détail dans la [carte d'articulation scientifique](18-carte-articulation-scientifique.md), section 3). En clair, « G0-S » désigne ici l'**étude des temps de parcours dirigés** : dans un vent donné, combien de temps faut-il pour aller d'un point $A$ à un point $B$ en suivant le courant, et quelles propriétés ce temps vérifie-t-il ? Dans toute la page, ce nom de code peut se lire comme « l'étude des temps de parcours dirigés ».

**Nomenclature des temps étudiés.** Pour éviter toute confusion avec les autres notations du dépôt — en particulier le modèle direct $V(p)$ et le modèle approché $v(p)$ de la réduction, ou la base $\{W_N\}$ — les deux constructions du socle G0-S portent des identifiants courts en mode mathématique : $T_{\mathrm{arr}}$ désigne le **temps de première arrivée** (définition 2.3 de l'[investigation G0-S](19-investigation-g0s-temps-de-parcours.md) : premier instant auquel la trajectoire issue de $A$ atteint exactement $B$) et $T_{\mathrm{proj}}$ le **temps après projection** (définition 2.4 : construction historique de Mohammadi & Brun 2006, où $B$ est d'abord projeté sur la caractéristique passant par $A$, d'où son nom historique de « pseudo-distance »). Les formes à deux arguments $T(A,B)$ et $d(A,B)=T(A,B^\perp)$ désignent leurs valeurs entre deux points donnés. Convention d'écriture : à sa première occurrence dans un document ou une page, chaque identifiant est accompagné de son étiquette sémantique — « temps de première arrivée $T_{\mathrm{arr}}$ » ou « temps après projection $T_{\mathrm{proj}}$ » — puis les occurrences suivantes emploient l'identifiant seul ; dans le code et les schémas en texte brut, les formes ASCII `T_arr` et `T_proj` sont utilisées. Ces identifiants remplacent les codes de travail V1 et V2 des premières notes du chantier.

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

### Comparer les notions par leurs axiomes

Le tableau explicite les recouvrements : chaque notion reprend les axiomes indiqués, et se distingue par les propriétés qu’elle n’exige pas. Les conventions de « quasi-métrique » varient selon les ouvrages ; la colonne correspond à la convention retenue ici, sauf mention contraire.

| Notion | Valeurs | Non-négativité | Diagonale nulle | Séparation | Symétrie | Triangle | Commentaire |
|---|---|---:|---:|---:|---:|---:|---|
| **Métrique** | $[0,+\infty[$ | Oui | Oui | Oui | Oui | Oui | Notion de référence ; tous les axiomes sont requis. |
| **Pseudo-métrique** | $[0,+\infty[$ | Oui | Oui | **Non** | Oui | Oui | Peut attribuer une distance nulle à deux points distincts. |
| **Quasi-métrique dirigée** | $[0,+\infty[$ | Oui | Oui | Oui selon la convention stricte | **Non** | Oui, dans le sens dirigé | Le terme est polysémique ; vérifier la définition de chaque source. |
| **Quasi-distance étendue dirigée ($T_{\mathrm{arr}}$ ici)** | $[0,+\infty]$ | Oui | Oui | Oui dans le cadre retenu | **Non exigée** | Oui, dans le sens dirigé | Autorise $+\infty$ pour une cible non atteinte. |
| **$T_{\mathrm{proj}}$ — temps après projection** | $[0,+\infty]$ selon la convention | Oui si le temps projeté est défini | Oui si la projection de $A$ est bien définie | **Pas garantie en 2D** | Pas garantie | Pas garantie en général | Construction particulière, pas une classe métrique standard. |

La pseudo-métrique abandonne précisément l’axiome de séparation. Une quasi-distance dirigée abandonne la symétrie, et la version étendue autorise en plus la valeur infinie. $T_{\mathrm{proj}}$ peut perdre la séparation parce que la projection ignore un décalage transversal.


Pour $T_{\mathrm{arr}}$, la convention $T(A,B)=+\infty$ en l'absence d'arrivée est utile pour représenter l'inaccessibilité dans le sens du flot. Elle doit toutefois être distinguée d'une non-existence de la trajectoire dans le domaine : ce dernier cas relève du temps maximal de solution et des conventions de sortie de domaine.

## 2. Pourquoi tester chaque propriété séparément ?

Une propriété ne découle pas du fait qu'une quantité soit positive, exprimée en secondes ou appelée « distance ». Il faut une preuve sous des hypothèses identifiées. Un contre-exemple suffit, en revanche, à montrer qu'une propriété ne peut pas être garantie dans le cadre général considéré.

| Propriété | $T_{\mathrm{arr}}$ : temps de première arrivée | $T_{\mathrm{proj}}$ : temps après projection |
|---|---|---|
| Non-négativité | Oui, par définition du temps $t\geq0$, avec $+\infty$ autorisé | Oui lorsque la projection est définie et que $T_{\mathrm{proj}}$ est calculée comme un temps $T_{\mathrm{arr}}$ |
| Diagonale nulle | Oui : $T(A,A)=0$, puisque $t=0$ est admis | Oui si la projection de $A$ sur sa propre caractéristique est bien définie et vaut $A$ |
| Séparation | Oui dans le cadre du flot continu et univoque retenu ; un temps nul implique la même position initiale et finale | Pas garantie en dimension 2 : une projection peut coïncider avec $A$ alors que $B\ne A$ |
| Symétrie | Pas garantie : le flot est orienté dans le temps | Pas garantie ; la projection et le flot sont orientés et peuvent dépendre du point de départ |
| Inégalité triangulaire | Oui sous les hypothèses d'un flot autonome univoque, via la propriété de semi-groupe | Pas garantie en général : les projections intermédiaires ne se composent pas comme des segments de trajectoire |
| Finitude | Pas garantie : une cible peut être inaccessible ou seulement approchée asymptotiquement | Pas garantie, notamment si la projection cible n'est pas atteignable dans le sens positif |

Ce tableau est un résumé des résultats du document d'investigation, pas une preuve autonome. Les conditions exactes et les contre-exemples sont détaillés dans [l'investigation G0-S](19-investigation-g0s-temps-de-parcours.md), notamment ses sections 3 à 6.

## 3. Champ lipschitzien, solution et flot

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
la continuité du champ assure notamment l'existence locale d'au moins une solution (théorème de Peano), mais **ne garantit pas à elle seule son unicité**. Une hypothèse locale de Lipschitz est une condition suffisante standard pour l'existence et l'unicité locales (théorème de Cauchy–Lipschitz/Picard–Lindelöf). Elle permet de définir un flot $X(t;A)$ non ambigu, puis d'utiliser sa propriété de semi-groupe pour démontrer l'inégalité triangulaire de $T_{\mathrm{arr}}$.

**Définition du flot.** Une *solution* est une fonction $X(t)$ qui satisfait l’équation différentielle et la condition initiale sur un intervalle donné. Lorsque la solution est unique, l’*application d’évolution* $\Phi_t(A)$ désigne l’état atteint au temps $t$ depuis l’état initial $A$, tant que la solution existe. Un *flot autonome* est la famille de ces applications, compatible avec le passage du temps et vérifiant la propriété de semi-groupe
$$
\Phi_{s+t}(A)=\Phi_t(\Phi_s(A)),
$$
à condition que les deux côtés soient définis. Le terme « flot » ne désigne donc pas une solution arbitraire lorsque plusieurs solutions partent du même état. Cette propriété de composition est précisément celle utilisée pour démontrer l’inégalité triangulaire de $T_{\mathrm{arr}}$. L'image est celle d'un transport : de même qu'un courant porte une particule de $A$ vers l'aval, le champ transporte chaque point, et le flot rassemble tous ces transports en un objet unique.

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

## 4. Temps de première arrivée

Dans le cadre retenu par G0-S — l’étude des temps de parcours dirigés, explicitée en tête de page —, $u:\Omega\to\mathbb R^d$ est un champ stationnaire suffisamment régulier pour que la solution maximale $X(t;A)$ issue de $A$ soit unique. Son intervalle maximal d'existence est noté $I_A$, avec $0\in I_A$.

Le **temps de première arrivée** de $B$ depuis $A$ est
$$
T(A,B)=\inf\{t\in I_A\cap[0,+\infty[\mid X(t;A)=B\},
\qquad \inf\varnothing=+\infty.
$$
Autrement dit, c'est le premier temps non négatif où la trajectoire issue de $A$ atteint $B$, si elle l'atteint pendant son existence. Le temps $t=0$ est admis : ainsi $T(A,A)=0$. Le **temps de retour** en $A$, lui, désigne généralement le premier temps strictement positif où une trajectoire revient en $A$, s'il existe ; il s'agit d'une autre quantité.

Pourquoi définir l'ensemble sur $I_A$ ? Parce qu'une solution ne peut être évaluée après la fin de son intervalle maximal. Écrire simplement $t\geq0$ sans cette restriction masque cette condition d'existence.

L'**intervalle maximal d'existence** $I_A$ est l'intervalle de temps, contenant $0$, au-delà duquel la solution issue de $A$ ne peut plus être prolongée en restant dans le modèle. Il peut être strictement plus petit que $[0,+\infty[$ pour deux raisons distinctes :

1. **Sortie du domaine.** La trajectoire atteint le bord de $\Omega$ et ne peut plus y être prolongée. Exemple : pour le champ uniforme $u\equiv U>0$ restreint à $\Omega=\,]0,1[$, la solution issue de $a$ atteint le bord au temps $(1-a)/U$ ; au-delà, elle quitte le domaine et le modèle ne la définit plus.
2. **Explosion en temps fini.** La solution grandit sans borne et cesse d'exister au bout d'un temps fini. Exemple : pour $\dot x=x^2$ avec $x(0)=1$, la solution $x(t)=1/(1-t)$ n'est définie que pour $t<1$.

Ces deux fins d'existence ne disent pas la même chose qu'une cible inaccessible dans le sens du flot : la distinction entre inaccessibilité par orientation ($+\infty$) et sortie de domaine est précisée par les conventions (C1) et (C2) de l'investigation. C'est pourquoi l'ensemble des temps de la définition est restreint à $I_A$ au lieu de tous les $t\geq0$.

Si $B$ n'appartient pas à l'orbite positive de $A$, la convention donne $T(A,B)=+\infty$. Si la trajectoire quitte le domaine avant d'atteindre $B$, il faut signaler cette sortie comme telle plutôt que confondre automatiquement les causes d'inaccessibilité.

## 5. Intervalles sans point de stagnation en dimension 1

En dimension 1, soit $u:I\to\mathbb R$ un champ continu sur un intervalle $I$. Un **point de stagnation** est un point $x^*$ où $u(x^*)=0$. L'ensemble
$$
I\setminus\{x\in I:u(x)=0\}
$$
est l'ensemble des points non stagnants. Une **composante connexe** de cet ensemble est un sous-ensemble connexe maximal ; sur la droite réelle, chaque composante est un intervalle. En langage courant, il s’agit d’un « intervalle maximal où le champ ne s’annule pas » : on ne peut pas l’agrandir sans rencontrer un point de stagnation ou la frontière du domaine.

Sur une telle composante, $u$ ne s'annule pas et, par continuité, conserve un signe constant. La trajectoire y est donc monotone tant qu'elle y reste. Cela ne signifie pas qu'elle visite les points dans les deux sens : elle avance seulement dans le sens indiqué par le signe de $u$.

Cette précision est essentielle pour comparer $T_{\mathrm{arr}}$ et $T_{\mathrm{proj}}$ en dimension 1. La coïncidence $$T_{\mathrm{proj}}$=$T_{\mathrm{arr}}$$ ne doit pas être affirmée pour deux points quelconques d'une même composante sans préciser l'orientation : la cible $b$ doit être atteignable depuis $a$ dans le temps positif, avant une éventuelle sortie du domaine. Si $u>0$, par exemple, $b>a$ est dans le sens du flot et
$$
T(a,b)=\int_a^b\frac{dx}{u(x)},
$$
tandis que $b<a$ n'est pas atteint dans le temps positif et $T(a,b)=+\infty$ selon la convention de $T_{\mathrm{arr}}$.

## 6. Trajectoire périodique et temps de parcours dirigé

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

Cet exemple montre que $T_{\mathrm{arr}}$ est **non symétrique en général, mais pas nécessairement asymétrique pour chaque paire**. À l'inverse, pour le champ uniforme unidimensionnel $u(x)=U>0$, on a $T(a,b)=(b-a)/U$ si $b>a$ et $T(a,b)=+\infty$ si $b<a$. Ce contre-exemple établit que la symétrie n'est pas une propriété générale de $T_{\mathrm{arr}}$.

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

Ces options ne sont pas équivalentes. Le MVP-S retient le cadre à flot unique pour $T_{\mathrm{arr}}$ ; les exemples non lipschitziens servent à expliquer les limites du calcul intégral, et non à étendre silencieusement la définition de $T_{\mathrm{arr}}$.

## 8. Contre-exemples de référence

| Contre-exemple | Ce qu'il démontre | Ce qu'il ne démontre pas |
|---|---|---|
| $u(x)=U>0$ sur la droite | $T_{\mathrm{arr}}$ peut être non symétrique et étendue ($+\infty$ dans le sens inaccessible) | Que $T_{\mathrm{arr}}$ soit asymétrique pour toute paire |
| $\dot x=\sqrt{x},\ x(0)=0$ | Un champ continu non lipschitzien peut avoir plusieurs solutions ; une intégrale finie sur une branche ne suffit pas | Que tous les champs non lipschitziens aient des solutions non uniques |
| $\dot x=x$ au point $x=0$ | La solution issue de la stagnation reste à zéro dans ce champ lipschitzien | Que toute stagnation soit une barrière pour un champ seulement continu |
| $\dot x=\sqrt{1-x}$ au voisinage de $x=1$ | Une cible stagnante peut être atteinte en temps fini lorsque le champ n'est pas $C^1$ au point cible | Que ce comportement soit possible sous l'hypothèse $C^1$ |
| $\dot x=-y,\ \dot y=x$ | Une orbite périodique permet des arrivées finies dans les deux sens entre deux points distincts de l'orbite | Que le temps de parcours soit une métrique symétrique |
| $T_{\mathrm{proj}}$ avec projection non unique (exemple détaillé dans l'investigation G0-S, § 6.1) | La construction projetée peut ne pas définir une valeur scalaire unique sans règle de projection | Que toute projection dans tout champ soit non unique |

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

Elle fournit la preuve de l'inégalité triangulaire dirigée de $T_{\mathrm{arr}}$. Si $B$ est atteint depuis $A$ au temps $s$ et $C$ est atteint depuis $B$ au temps $t$, la propriété de semi-groupe donne $X(s+t;A)=C$. Ainsi, le premier temps d'arrivée de $C$ depuis $A$ satisfait
$$
T(A,C)\leq s+t=T(A,B)+T(B,C),
$$
lorsque les deux temps d'arrivée sont finis et les trajectoires existent jusqu'aux instants considérés. Si l'un des termes du membre de droite vaut $+\infty$, l'inégalité étendue est triviale. Cette preuve ne s'applique pas automatiquement à une quantité qui n'est pas construite à partir du même flot, comme $T_{\mathrm{proj}}$ projetée.

### Atteignabilité et temps infini

Dire que $B$ est **atteignable depuis $A$ dans le temps positif** signifie qu'il existe $t\in I_A\cap[0,+\infty[$ tel que $X(t;A)=B$. Ce terme porte sur une arrivée exacte en temps fini, pas seulement sur une limite asymptotique. Par exemple, pour $\dot x=1-x$ avec $x(0)=0$, la solution $x(t)=1-e^{-t}$ tend vers $1$ mais ne l'atteint à aucun temps fini ; selon la définition de première arrivée ci-dessus, $T(0,1)=+\infty$. À l'inverse, pour $\dot x=\sqrt{1-x}$ sur le domaine $x\leq1$, la branche issue de $x(0)=0$ atteint $1$ au temps fini $2$, même si le champ n'est pas localement lipschitzien au point cible. Cet exemple appartient à une extension non $C^1$ et ne contredit pas les résultats formulés sous l'hypothèse de base $C^1$.

### Projection et définition de $T_{\mathrm{proj}}$

Dans la référence codée en champ uniforme non nul $u\in\mathbb R^2$, la direction unitaire du champ est $e=u/\|u\|$. Le déplacement longitudinal de $A$ vers $B$ est $(B-A)\cdot e$. La fonction `pseudo_distance_uniforme` calcule
$$
$T_{\mathrm{proj}}$(A,B)=
\begin{cases}
\dfrac{(B-A)\cdot u}{\|u\|^2}, & (B-A)\cdot u\geq0,\\
+\infty, & (B-A)\cdot u<0.
\end{cases}
$$
La formule est un temps longitudinal pour la convention locale choisie ; elle ignore le déplacement transversal. En particulier, un déplacement transversal non nul peut donner zéro : $T_{\mathrm{proj}}$ ne satisfait donc pas la séparation des points. La formule suppose un champ uniforme et ne doit pas être extrapolée à un champ variable sans définir comment la caractéristique est construite, si plusieurs projections sont possibles et comment les cibles non atteignables sont traitées.

### Carte explicite entre notions, documentation et code

| Notion | Définition / preuve publique | Code actuel | Portée effective |
|---|---|---|---|
| Temps de première arrivée 1D à vitesse constante | Section 4 de cette page et annexe B du bilan MVP-S 1D | `temps_premiere_arrivee_1d` dans [`src/jdriftx/metric.py`](../src/jdriftx/metric.py) | Cas analytique constant uniquement |
| Coût discret d'une polyligne | Définition de la primitive dans le [module](../src/jdriftx/metric.py) et la [matrice](27-matrice-tracabilite-mvp-s.md) | `temps_transport` | Somme longueur/norme de vitesse ; ne tient pas compte du signe du vent |
| $T_{\mathrm{proj}}$ uniforme projetée | Formule ci-dessus et investigation G0-S, section 6 | `pseudo_distance_uniforme` | Champ constant non nul en 2D ; convention amont explicite |
| Propriétés générales du flot $T_{\mathrm{arr}}$ | Sections 2 à 7 de l'[investigation G0-S](19-investigation-g0s-temps-de-parcours.md) | Pas de solveur général de champ variable | Résultats analytiques sous hypothèses ; pas validés par les seuls tests de la primitive 1D |
| Contre-exemple de non-unicité | Section 3 et section 7 de cette page | Exemple mathématique documenté, non implémenté comme solveur ODE dans `src/` | Sert à préciser les limites logiques ; ce n'est pas une fonctionnalité logicielle |

Les tests de `tests/test_metric.py` vérifient des cas ciblés des primitives implémentées ; `tests/test_proprietes.py` étend ces vérifications à des entrées générées (hypothesis), évaluées à travers les objets du package (`ScenarioUniforme` pour la référence dirigée, `ClasseStabilite` pour le panache). Ils ne démontrent ni l'existence d'un flot pour tout champ, ni l'unicité générale, ni les propriétés analytiques universelles de $T_{\mathrm{arr}}$, ni la validité physique de la méthode historique. Pour chaque affirmation générale, la preuve et ses hypothèses restent la référence ; pour chaque comportement logiciel, le code et les tests constituent la référence d'implémentation.
