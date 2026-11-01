# Revue mathématique ciblée — temps de parcours de Drift-X

> **Statut de la revue initiale et mise à jour (29 octobre 2026) :** revue mathématique ciblée, non exhaustive. La rédaction initiale précédait l'obtention du PDF de thèse. Celui-ci est désormais versionné dans `raw/`; des passages ciblés, notamment les équations (7.12)–(7.13), sont analysés dans [l'audit de thèse](43-audit-these-brun-conservation-g0s.md). La thèse entière n'a pas été relue de bout en bout, et la page de titre ainsi que l'identité binaire avec le fichier HAL restent à vérifier depuis les éléments de provenance existants. Ne pas relancer l'acquisition. Cette note distingue les définitions rapportées par les sources, les déductions analytiques vérifiables et les questions physiques ou numériques encore ouvertes ; elle ne certifie ni l'originalité de la formulation historique ni sa validité applicative.

> **Guide de lecture.** Une *définition* fixe l'objet étudié; une *hypothèse* précise quand il est défini; une *proposition démontrée* découle de ces éléments; une *illustration* aide à l'interpréter sans constituer une validation physique.

**Périmètre par rapport aux notes canoniques actuelles :** cette revue conserve la lecture critique des sources historiques, leurs formulations et les questions qui en découlent. Pour les définitions formelles et les propriétés de $T_{\\mathrm{arr}}$ et $T_{\\mathrm{proj}}$, utiliser l'[investigation G0-S](19-investigation-g0s-temps-de-parcours.md) ; pour la dérivation conditionnelle de conservation, utiliser [docs/32](32-conservation-coordonnees-travel-time.md). Les recouvrements historiques sont conservés pour la traçabilité, mais ces deux documents sont les références actuelles pour leurs sujets respectifs.

## 1. Question examinée

La page [Métrique travel-time](../site/theorie/metrique-travel-time.qmd) définit

\[
\tau(\mathbf{x}_0\to\mathbf{x})=\int_\gamma \frac{ds}{|\mathbf{u}(s)|},
\]

où \(\gamma\) est une ligne de courant. **Attention : cette formule ne restitue pas à elle seule toute la définition historique de la pseudo-distance.** L'article de 2006 définit le coût jusqu'à la projection \(B^\perp\) du point cible sur la caractéristique passant par le point de départ, et non nécessairement jusqu'au point cible lui-même. La différence est structurante et est détaillée en §2.1.

La question préalable n'est pas « cette idée est-elle nouvelle ? », mais **quel objet mathématique est exactement défini, sur quel domaine, et quelles propriétés en découlent réellement ?**

## 2. Résultat central : distinguer trois problèmes

| Objet | Définition opérationnelle | Conséquence | Littérature à comparer |
|---|---|---|---|
| **Temps le long d'une ligne de courant** | Champ stationnaire donné; trajectoire imposée par \(\dot X=\mathbf u(X)\); intégrale \(\int ds/|\mathbf u|\) entre deux points appartenant à la même trajectoire orientée | Le temps est défini pour les points atteignables dans le sens de l'écoulement. Les autres couples sont hors domaine ou peuvent recevoir la valeur \(+\infty\) par convention explicite | Équations caractéristiques, transport advectif |
| **Temps minimal de navigation** | On peut choisir une commande/direction admissible et minimise le temps parmi les trajectoires réalisables | Le coût est une fonction valeur d'un problème de contrôle; vent/courant et vitesse propre interagissent | Navigation de Zermelo, métriques de Randers/Finsler |
| **Temps de première arrivée / propagation** | Une loi de vitesse et une règle de propagation déterminent une front d'arrivée | Souvent formulé par une équation eikonale ou Hamilton–Jacobi; dépend de la loi de propagation et de ses conditions | Eikonale anisotrope, Hamilton–Jacobi–Bellman |

Ces trois objets peuvent se ressembler mais ne sont pas interchangeables. Une intégrale le long d'une ligne de courant n'est pas automatiquement le temps minimal entre deux points, et le temps minimal d'un navigateur n'est pas le temps d'un traceur passif purement advecté.

### Résultat particulier documenté : GZ-1

La page [Navigation de Zermelo, fronts et Hamilton–Jacobi](../site/theorie/navigation-fronts-controllabilite.qmd) établit le théorème conditionnel **GZ-1** pour un noyau fondamental gaussien 3D à diffusivité isotrope constante, un vent uniforme et une borne de commande \(c(t)=R'(t)\) sur la phase d'expansion. Le résultat est \(T_{\mathrm{nav}}=T_{\mathrm{front}}\), avec un ensemble atteignable démontré exactement. La formulation HJ du cas GZ-1 est également clarifiée : dans le référentiel mobile, la reparamétrisation \(\rho=R(t)\) ramène l'équation à l'eikonale standard et absorbe la singularité intégrable de \(R'(t)\) à l'origine. La formule de Hopf–Lax donne \(\phi=\max(\lVert x-x_0-ut\rVert-R(t),0)\) : le zéro représente la boule atteignable, dont la frontière est le front ; la distance signée réinitialisée ne doit pas être confondue avec la solution de viscosité globale. La lecture intuitive et les démonstrations détaillées, y compris la conservation de masse, le contrôle dimensionnel, la dérivation de Randers et le régime supercritique à borne constante, sont regroupées dans la [note 59 — GZ-1](59-navigation-controllabilite-verifications.md). Attention : le seuil instantané $t_Z$ marque seulement la perte de régularité de Randers ; il ne réduit pas l'ensemble atteignable GZ-1, qui dépend du budget cumulé $\int_0^t R'(\tau)\,d\tau=R(t)$. Le cône aval à borne constante est un résultat distinct et ne se transpose pas par substitution de $c(t)$.

Ce résultat est une instance particulière du **temps minimal de navigation contrôlée**, comparée à un front d'isoconcentration dans ce modèle idéal. Il ne redéfinit pas \(T_{\mathrm{arr}}\), ne démontre rien de nouveau sur le coût projeté historique \(T_{\mathrm{proj}}\), et ne s'étend pas sans preuve aux champs variables ou à l'implémentation concentration_puff. Il ne doit pas être lu comme une extension des conclusions G0-S sur le temps passif.


### Vocabulaire minimal de mécanique des fluides

- **Champ de vitesse** \(\mathbf u(\mathbf x,t)\): vecteur vitesse du fluide en chaque position et instant; son unité SI est le m·s⁻¹.
- **Ligne de courant** (*streamline*): courbe tangente au champ de vitesse à un instant fixé.
- **Trajectoire de particule** (*pathline*): chemin réellement suivi au cours du temps par une particule fluide, solution de \(\dot X(t)=\mathbf u(X(t),t)\).
- **Caractéristique**: courbe utilisée pour suivre l'information d'une équation de transport. Pour un champ de vitesse stationnaire suffisamment régulier, ses courbes spatiales coïncident avec les lignes de courant et les trajectoires spatiales. Dans un champ instationnaire, ces notions ne doivent pas être confondues.
- **Divergence** \(\nabla\cdot\mathbf u\): mesure locale du taux de dilatation volumique du champ. \(\nabla\cdot\mathbf u=0\) signifie un champ incompressible au sens cinématique; pour un fluide de densité constante, cela correspond à la continuité locale sans source volumique. Ce n'est pas, à lui seul, une preuve de conservation d'un flux sur une surface arbitraire.
- **Source/puits**: région où la quantité transportée est injectée ou retirée, ou point singulier du champ selon le modèle. Il faut préciser si l'on parle d'une source de fluide, d'une source de polluant ou d'une singularité mathématique : ces notions ne sont pas synonymes.
- **Stagnation**: point où \(\mathbf u=0\). L'intégrande \(1/\|\mathbf u\|\) y est singulier; la convergence de l'intégrale dépend du comportement local de la vitesse et de la trajectoire.

Dans la suite, sauf mention contraire, le contre-exemple est stationnaire et bidimensionnel. Les coordonnées et les vitesses sont **adimensionnées** pour éviter de mélanger des unités dans la formule \(u_x=1+9y\).

## 2.1 Lecture de la source primaire de 2006 : une clarification importante

La note de Mohammadi & Brun, *Similitude généralisée et modélisation géométrique à complexité réduite* (2006, §3, pp. 635–636, [DOI](https://doi.org/10.1016/j.crme.2006.06.007)), est accessible en texte intégral. Elle permet de préciser l'objet historique plus nettement que la seule formule intégrale donnée dans les pages actuelles du dépôt.

La construction historique ne définit pas simplement le temps d'une trajectoire jusqu'au point cible \(B\). Pour un point \(A\), elle considère la caractéristique passant par \(A\), projette \(B\) sur cette caractéristique en un point \(B^\perp\), puis définit le coût dirigé comme le temps de migration de \(A\) vers \(B^\perp\). Elle suppose la caractéristique unique et écarte les sources et puits; les cas où la projection n'est pas unique sont traités dans la source par un critère lié à \(\mathbf u\cdot\nabla c\), c'est-à-dire à la dérivée directionnelle de la concentration le long du champ de vitesse. Cette phrase explique la notation, mais ne reconstitue pas le critère complet : ses hypothèses et son rôle exact restent à vérifier dans le passage source.

La source appelle explicitement cette construction une **pseudo-distance** et précise qu'elle ne satisfait pas en général les propriétés d'une distance : elle peut vérifier \(d(A,B)=0\) sans \(A=B\), elle est non symétrique, et l'inégalité triangulaire peut échouer. Ces échecs ne sont donc pas simplement des lacunes de documentation dans la reprise : au moins pour la séparation et la triangulation, ils sont annoncés dans la formulation historique elle-même.

### Vérification complémentaire du chapitre de 2008

Le chapitre *Reduced-Order Modelling of Dispersion* est également disponible dans le volume Springer, pp. 245–256 ([texte du volume](https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf), §2.2, pp. 248–250). Il confirme la définition projetée, mais ajoute un détail qui change le statut de l'implémentation :

- la définition exacte utilise \(B^\perp\), projection euclidienne de \(B\) sur la caractéristique passant par \(A\);
- plus loin, la méthode numérique approxime \(B^\perp=B\), en indiquant que la caractéristique passant par \(A\) passe exactement par \(B\), ce qui est présenté comme peu probable en général;
- en champ uniforme, le chapitre Springer (2008, p. 251) imprime le facteur correctif « 2/3 = 0.636 » et le décrit comme un cosinus moyen stochastique pour des angles entre 0 et $\pi$. Ces valeurs sont arithmétiquement incompatibles : $2/3\approx0.667$, tandis que $2/\pi\approx0.637$. La moyenne de $|\cos\theta|$ pour un angle uniforme sur $[0,\pi]$ vaut $2/\pi$, mais il ne faut pas corriger silencieusement la source : le coefficient exact à reproduire dans l’algorithme historique reste à confirmer (possible coquille typographique dans le chapitre).
- la méthode est présentée comme satisfaisante pour des champs atmosphériques lisses et dans un contexte applicatif particulier, pas comme une construction sans restriction pour tout champ de vitesse.

Il faut donc séparer **la définition géométrique idéale** et **l'algorithme approché publié**. Reproduire seulement la projection exacte teste la définition; reproduire l'algorithme de 2008 demande également de documenter l'approximation \(B^\perp\approx B\), le facteur correctif, l'interpolation de la caractéristique et son domaine de validité.

Le chapitre formule des contraintes de divergence nulle, d’advection, de positivité et de conservation pour les champs et les solutions réduites. L’article de 2006 précise notamment une contrainte globale $\int_{\mathbb R^3} c\,dV=Q$; le chapitre de 2008 définit ensuite la quantité transportée $C=\int_{\mathbb R^2}c^+(x,y)\,d\sigma$ comme une quantité à conserver par le modèle réduit. Dans les passages consultés, ces formulations ne démontrent pas à elles seules l’énoncé plus spécifique « le flux sur chaque surface iso-$\tau$ restitue exactement $Q$ ». Cette dernière affirmation doit rester une question distincte tant qu’une dérivation source explicite n’a pas été identifiée.

### Schéma de la construction et du contre-exemple

Le schéma ci-dessous sépare la projection utilisée par la définition historique du mécanisme responsable de l'échec de l'inégalité triangulaire. Les flèches sont qualitatives; elles ne représentent pas une simulation numérique.

![À gauche : projection du point B sur la caractéristique issue de A. À droite : champ horizontal plus rapide à y=1 et trois points donnant une violation de l'inégalité triangulaire.](../site/images/pseudo-distance-projection-et-triangulation.svg)

### Contre-exemple analytique minimal : champ uniforme

Prenons le champ 2D uniforme \(\mathbf u=(U,0)\), avec \(U>0\), et les points \(A=(x_A,y_A)\), \(B=(x_B,y_B)\). La caractéristique passant par \(A\) est horizontale. La projection normale décrite dans l'article donne \(B^\perp=(x_B,y_A)\). Pour \(x_B\ge x_A\), le coût historique devient

\[
d(A,B)=\frac{x_B-x_A}{U}.
\]

Le coût ne dépend pas de \(y_B-y_A\). Ainsi, pour \(B=(x_A,y_B)\) avec \(y_B\ne y_A\), on obtient \(d(A,B)=0\) alors que \(A\ne B\). Ce n'est pas un paradoxe : la construction mesure un avancement le long de la caractéristique de \(A\), et non une distance complète jusqu'à \(B\).

Pour ce champ uniforme, cette expression satisfait l'inégalité triangulaire dans la direction admissible lorsque les abscisses sont ordonnées, mais cela ne prouve pas la propriété pour des champs non uniformes avec projections multiples ou géométrie plus complexe. L'article avertit explicitement que la triangulation peut être mise en défaut dans la construction générale.

### Contre-exemple explicite à l'inégalité triangulaire

La source de 2006 affirme que l'inégalité triangulaire peut échouer. On peut le vérifier sur un champ analytique simple, sans sources ni puits :

\[
\mathbf u(x,y)=(1+9y,\,0),\qquad (x,y)\in\mathbb R\times[0,1].
\]

Ce champ est stationnaire, strictement dirigé vers \(+x\), sans divergence (\(\nabla\cdot\mathbf u=0\)); ses caractéristiques sont les droites horizontales. Avec la définition historique projetée, pour un déplacement vers l'aval,

\[
d(A,B)=\frac{x_B-x_A}{1+9y_A}.
\]

Choisissons \(A=(0,0)\), \(B=(1,1)\) et \(C=(2,0)\). Alors

\[
d(A,C)=2,\qquad d(A,B)=1,\qquad d(B,C)=\frac{1}{10},
\]

d'où \(d(A,C)=2>1+\frac{1}{10}=d(A,B)+d(B,C)\). L'inégalité triangulaire échoue donc même pour un champ lisse, divergence nulle et sans singularité dans le domaine considéré. Le mécanisme est géométrique : \(d(A,C)\) mesure la progression sur la caractéristique de \(A\), tandis que \(d(B,C)\) mesure la progression sur celle de \(B\), où la vitesse est plus élevée.

Ce contre-exemple confirme que la construction est une pseudo-distance directionnelle, et non une distance asymétrique satisfaisant automatiquement l'inégalité triangulaire.

### Conséquence pour le vocabulaire et le MVP

- Conserver le terme historique **pseudo-distance de transport** lorsque l'on parle de la construction de 2006.
- Ne pas la confondre avec le simple temps d'arrivée à \(B\), ni avec une distance de navigation obtenue par minimisation.
- Distinguer le temps le long de la caractéristique, la projection \(B^\perp\), le coût étendu en cas d'inaccessibilité et le modèle de concentration construit ensuite.
- Le test de référence uniforme est maintenant implémenté séparément. Toute variante plus intuitive doit conserver un nom et des tests distincts; elle ne constitue pas une reproduction de la formulation publiée.

## 3. Ce que les définitions actuelles permettent — et ne permettent pas — d'affirmer

### 3.1 La non-uniformité du champ ne suffit pas à établir la non-symétrie

Pour une **même courbe géométrique** parcourue dans les deux sens avec la même vitesse scalaire positive \(v(s)\), l'intégrale de longueur de temps \(\int ds/v(s)\) est identique dans les deux sens. La variation spatiale de la vitesse, à elle seule, ne rend donc pas cette intégrale asymétrique.

Dans un champ vectoriel d'advection, l'asymétrie peut venir du fait que la dynamique impose un sens de parcours : l'inverse d'une ligne de courant n'est généralement pas une trajectoire admissible du même champ. On doit alors définir explicitement le temps inverse comme **non défini**, **inaccessible** ou \(+\infty\), plutôt que déduire cette valeur de la seule non-uniformité du champ.

Un exemple 1D suffit à le montrer : pour \(\dot x=u(x)>0\), le temps de \(a\) vers \(b>a\) vaut \(\int_a^b dx/u(x)\). Le mouvement inverse n'est pas une solution de cette même dynamique. Si l'on introduit plutôt une vitesse de retour positive, on a défini une autre dynamique; si on autorise un contrôle de direction, on a défini un problème de navigation.

### 3.2 Les singularités près d'une stagnation demandent une hypothèse locale

L'intégrande \(1/|\mathbf u|\) devient singulier lorsque la vitesse tend vers zéro. Cela ne suffit pas à conclure, sans hypothèses sur le champ et sur la trajectoire, que toute intégrale de temps diverge : il faut examiner le comportement local de \(|\mathbf u|\) et la manière dont la trajectoire approche la zone. Le dépôt doit préciser si une stagnation est exclue du domaine, si le temps est infini, ou si un modèle physique différent prend le relais.

### 3.3 « Métrique » est un terme à justifier

Une métrique usuelle est finie et satisfait notamment séparation, symétrie et inégalité triangulaire. Une distance asymétrique ou quasi-distance peut relâcher la symétrie, mais ses axiomes doivent être énoncés. Une fonction étendue qui vaut \(+\infty\) pour des points inaccessibles ne doit pas être appelée sans qualification une métrique finie. Il faut vérifier séparément :
- le domaine de définition et la relation d'accessibilité;
- \(\tau(x,x)=0\) et la positivité pour les couples admissibles;
- la séparation des points distincts;
- l'inégalité triangulaire dirigée, quand les trois segments sont admissibles;
- la régularité et le comportement aux points critiques.

### 3.4 La conservation de masse est une affirmation distincte

La conservation de masse ne découle pas de la seule définition de $\tau$. L’article de 2006 formule une contrainte globale $\int_{\mathbb R^3}c\,dV=Q$; le chapitre de 2008 définit $C=\int_{\mathbb R^2}c^+(x,y)\,d\sigma$ comme la quantité totale transportée que le modèle réduit doit conserver. Dans les passages vérifiés, ces contraintes ne sont pas accompagnées d’une preuve générale selon laquelle le flux intégré sur toute surface iso-$\tau$ vaut exactement $Q$. Il faut distinguer cette revendication plus forte du résultat conditionnel obtenu par le théorème de la divergence pour le débit volumique à travers deux sections d’un même tube de courant. Pour le flux du scalaire $c$, le bilan doit inclure sources/puits, conditions aux limites et tous les termes physiques retenus.

### 3.4.1 Test analytique de l'équation locale de temps de transport

Une fonction de temps d'arrivée régulière $\tau$ le long d'un flot stationnaire satisfait localement $\mathbf u\cdot\nabla\tau=1$ là où elle est bien définie, différentiable et où les trajectoires restent dans le domaine. Cette équation ne doit pas être supposée vraie pour la pseudo-distance projetée historique $d_A(B)=T(A,B^\perp)$.

Considérons le champ de cisaillement lisse $\mathbf u(x,y)=(v(y),0)$ avec $v(y)>0$, et la source $A=(x_A,y_A)$. Les caractéristiques sont horizontales et la projection de $B=(x,y)$ sur la caractéristique de $A$ vaut $B^\perp=(x,y_A)$. Pour une cible aval, la définition historique donne

$$
d_A(x,y)=\frac{x-x_A}{v(y_A)}.
$$

Par dérivation directe, $\nabla d_A=(1/v(y_A),0)$, donc

$$
\mathbf u(x,y)\cdot\nabla d_A=\frac{v(y)}{v(y_A)}.
$$

Ce résultat diffère de $1$ dès que $v(y)\ne v(y_A)$. Il vaut $1$ sur la caractéristique source, mais pas globalement sur le domaine. Ainsi, même pour un champ $C^1$, stationnaire, positif et de divergence nulle, la pseudo-distance projetée par paires n'est pas généralement un champ de temps d'arrivée satisfaisant l'équation locale $\mathbf u\cdot\nabla d_A=1$. Cela ne réfute pas toute construction historique de concentration, mais interdit de justifier la généralisation par la seule identité de temps de parcours. Il faut dériver séparément le modèle de concentration et ses contraintes.


### 3.4.1.1 Portée logique du contre-exemple et décision de test

Le contre-exemple établit une non-implication précise, et rien de plus :

| Propriété / affirmation | Ce qui est établi | Ce qui n'en découle pas |
|---|---|---|
| Incompressibilité, \(\nabla\cdot\mathbf u=0\) | Pour \(\mathbf u=(v(y),0)\), la divergence vaut zéro car \(u_x=v(y)\) ne dépend pas de \(x\) et \(u_y=0\) | Ni conservation du scalaire, ni identité locale de temps, ni conservation du flux sur toute surface |
| Identité locale d'un temps d'arrivée régulier | Le long d'une trajectoire régulière, une coordonnée d'arrivée compatible vérifie \(\mathbf u\cdot\nabla\tau=1\) sur son domaine de validité | Cette identité ne peut pas être attribuée automatiquement à toute fonction appelée « temps » |
| Coût projeté historique | Pour la cible aval, \(d_A=(x-x_A)/v(y_A)\) et \(\mathbf u\cdot\nabla d_A=v(y)/v(y_A)\) | Hors de \(y=y_A\), cette dérivée n'est généralement pas égale à \(1\) |
| Axiomes de distance | La source historique qualifie l'objet de pseudo-distance; séparation, symétrie et triangle doivent être examinés séparément | Un échec d'axiome ne signifie pas que la formule est mal implémentée si cet échec appartient à sa définition |
| Conservation du débit volumique | Pour un tube de courant régulier sans singularité, \(\nabla\cdot\mathbf u=0\) implique l'égalité des débits signés à travers ses sections | Ce résultat ne vaut pas automatiquement pour le flux de polluant \(c\mathbf u\), et n'identifie pas ce flux à la quantité émise \(Q\) |
| Conservation de masse du scalaire | Elle relève d'un bilan du type \(\partial_t c+\nabla\cdot(c\mathbf u-D\nabla c)=s\) | Elle ne se déduit ni de la pseudo-distance seule ni de la seule incompressibilité |

Le contre-exemple ne prouve donc pas que le modèle de concentration historique est faux. Il montre que la chaîne d'arguments « champ incompressible → coût projeté → équation locale de temps → conservation du scalaire » contient des implications qui doivent être démontrées séparément.

#### Faut-il coder le contre-exemple maintenant ?

**Pas comme test de régression de l'API actuelle.** Le code Python actuel expose un temps de parcours sur polyligne et un cas 1D de première arrivée; il ne fournit pas encore une API de référence qui calcule, pour un champ 2D variable, la projection historique \(B\mapsto B^\perp\) et son coût. Un test ajouté aujourd'hui risquerait donc de tester une formule recopiée dans le test plutôt qu'un comportement réel du logiciel.

Décision de travail :

1. **Maintenant — preuve documentaire/analytique :** conserver le calcul exact ci-dessus comme contre-exemple mathématique, avec les hypothèses explicites \(v\in C^1\), \(v(y)>0\), champ stationnaire, source et cible aval. Ce résultat est déjà vérifiable à la main.
2. **Avant toute implémentation de la projection historique — test de spécification :** fixer la convention de projection, l'accessibilité amont/aval, les cibles hors domaine, les projections non uniques et les unités.
3. **Après implémentation d'une API dédiée — test automatisé :** choisir par exemple \(v(y)=1+y\) sur un domaine où \(v>0\), avec \(y_A=0\) et une cible \(y=1\). Vérifier la valeur analytique \(d_A=x-x_A\) et la dérivée directionnelle \(\mathbf u\cdot\nabla d_A=2\), donc différente de \(1\). Vérifier séparément que sur la caractéristique \(y=y_A\), cette dérivée vaut \(1\). Le test doit appeler l'API de production, non une copie de la formule écrite uniquement dans le test.
4. **Ne pas faire échouer le test de l'implémentation de polyligne** sur cette identité : cette fonction représente un autre objet mathématique et n'est pas censée résoudre le problème de projection en champ variable.

Le test futur vérifiera la fidélité à la définition projetée et son domaine de validité; il ne « corrigera » pas la pseudo-distance pour la forcer à être un vrai temps d'arrivée. Si le projet choisit plutôt d'implémenter un véritable solveur de temps d'arrivée, ce sera une API distincte avec ses propres hypothèses et tests.


## 3.4.2 Résultat conditionnel démontrable par le théorème de la divergence

On peut établir une conservation de flux entre deux sections transverses d'un même tube de courant sans supposer d'emblée une formule particulière pour le jacobien. Soit \(V\) le volume borné par deux sections \(S_1\) et \(S_2\), et par une surface latérale \(\Sigma\) formée de lignes de courant. Si le champ \(\mathbf u\) est suffisamment régulier dans \(V\), si \(\nabla\cdot\mathbf u=0\), et si aucune singularité ou ouverture supplémentaire n'intersecte la frontière, le théorème de la divergence donne

\[
0=\int_V \nabla\cdot\mathbf u\,dV
 =\int_{\partial V}\mathbf u\cdot\mathbf n\,dS
 =\int_{S_2}\mathbf u\cdot\mathbf n\,dS
  -\int_{S_1}\mathbf u\cdot\mathbf n\,dS.
\]

Le terme latéral disparaît parce que \(\mathbf u\) y est tangent; les signes opposés viennent des normales sortantes aux deux sections. Le débit volumique signé est donc identique aux deux sections. Cela vaut pour des sections iso-\(\tau\) **si** elles sont bien définies, transverses au champ et découpent le même tube de courant.

Ce résultat ne prouve pas automatiquement que l'intégrale du flux de polluant vaut le débit source \(Q\). Pour un scalaire \(c\), il faut considérer le flux advectif \(\mathbf J=c\mathbf u\) et l'équation de bilan correspondante. En régime stationnaire, si \(\nabla\cdot(c\mathbf u)=s\), alors

\[
\int_{\partial V}c\mathbf u\cdot\mathbf n\,dS=\int_V s\,dV.
\]

La différence de flux entre sections dépend donc de la source \(s\) contenue dans le volume; elle est nulle dans un volume sans source, et égale à l'émission intégrée uniquement si le volume et les conventions de signe englobent exactement cette émission, sans pertes ni flux non comptabilisés. Si l'équation comprend diffusion, réaction, dépôt ou d'autres termes, leurs flux/contributions doivent être ajoutés au bilan.

**Limites de cette dérivation :** elle établit un résultat conditionnel pour un tube de courant régulier, pas une preuve universelle de la revendication historique. Elle ne règle ni les caractéristiques multiples, ni les stagnations, ni les surfaces iso-$\tau$ non globalement définies, ni les conditions aux limites du problème réel. La prochaine étape est de définir précisément la quantité conservée (masse totale, débit volumique ou flux de scalaire), son domaine d’intégration, et les sources/puits. Le jacobien d’une transformation $(x,y,z)\mapsto(\tau,\eta_1,\eta_2)$ ne doit être dérivé qu’après avoir défini cette transformation et vérifié qu’elle est localement inversible.

## 4. Comparaison ciblée avec les antécédents

| Référence | Objet et proximité avec J-DriftX | Différence à établir avant toute revendication |
|---|---|---|
| Gibbons et al. (2009), [*Stationary metrics and optical Zermelo-Randers-Finsler geometry*](https://doi.org/10.1103/PhysRevD.79.044022) | Lien entre navigation de Zermelo et géométrie de Randers/Finsler; temps minimal dans un champ de vent/courant | Le navigateur garde une vitesse propre et choisit sa direction; un traceur passif advecté suit le champ. La limite de vitesse propre nulle n'est pas automatiquement une métrique de Randers régulière |
| Dušek (2018), [*Zermelo Navigation Problem in Geometry*](https://doi.org/10.17818/NM/2018/4SI.16) | Formulation géométrique du problème de navigation et des métriques de Randers | Établir si J-DriftX optimise sur des trajectoires contrôlables ou intègre une trajectoire imposée |
| *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), [DOI](https://doi.org/10.1016/j.difgeo.2024.102177) | Navigation à temps minimal avec contraintes et obstacles mobiles | Comparateur si J-DriftX introduit un choix de trajectoire/contrôle et des contraintes comparables; cet article n'établit rien sur la pseudo-distance projetée en advection pure |
| Markvorsen, Pendás-Recondo & Rygaard (2025), [*Time-dependent Zermelo navigation with tacking*](https://arxiv.org/abs/2508.07274) | Navigation dépendant du temps, changement de stratégie de cap | À comparer si le modèle évolue vers des champs temporels et une optimisation de trajectoire |
| Contreras & Kachroo (2020), [*The Viscosity Solution for Hamilton Jacobi Travel Time Dynamics*](https://doi.org/10.1109/TITS.2019.2946109) | Équation de temps de parcours de type Hamilton–Jacobi et solution de viscosité | Application au trafic/LWR : analogue méthodologique, pas la même dynamique physique |
| Sethian & Vladimirsky (2001), [*Ordered upwind methods for static Hamilton–Jacobi equations*](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/) | Problèmes de temps minimal anisotrope et équations Hamilton–Jacobi–Bellman | Pertinent si le temps est un minimum sur un ensemble de directions et si un solveur de front est envisagé |

Cette liste établit que le voisinage conceptuel est riche; elle **n'établit pas** que la contribution historique de Drift-X est redondante. Les sections pertinentes du rapport CR Mécanique (2006) et du chapitre Springer de 2008 ont été lues. Le PDF de thèse a désormais été obtenu et des passages ciblés sont examinés dans [docs/43](43-audit-these-brun-conservation-g0s.md), mais la thèse entière n'a pas été relue ; sa date bibliographique reste incohérente entre les références consultées.

## 5. Décision scientifique pour le MVP

Le cas 1D à deux vitesses constantes proposé dans la fiche MVP est utile pour tester des propriétés élémentaires, mais il **ne doit pas être présenté comme une réduction démontrée du modèle de ligne de courant historique**. Il définit par construction deux directions et deux vitesses, donc un autre modèle jouet.

Ordre recommandé :

1. **Geler la définition cible** : champ stationnaire ou temporel, trajectoire imposée ou contrôlée, couples accessibles, traitement de l'inaccessibilité, unités et conditions aux limites.
2. **Séparer les affirmations** : propriétés de l'intégrale sur une trajectoire; propriétés de la fonction de coût sur des paires de points; conservation de masse; conséquences pour les solutions de similitude.
3. **Reproduire un cas 1D issu de la définition retenue**, puis calculer indépendamment l'intégrale et tester les propriétés annoncées.
4. **Relire les sources historiques primaires** et tracer chaque formule ou théorème à sa source.
5. Seulement ensuite, décider si un solveur 2D synthétique répond à une question non résolue.

### Conclusion provisoire

Le risque le plus immédiat n'est pas simplement que « Zermelo existe déjà ». C'est que le dépôt emploie le même vocabulaire de temps de parcours pour des objets différents : intégrale advective le long d'une caractéristique, coût asymétrique sur des paires de points, et temps minimal de navigation. Leur relation doit être démontrée plutôt que supposée.

À ce stade :
- **résultat établi par la revue** : le texte primaire de 2006 définit une pseudo-distance fondée sur la projection sur une caractéristique, et annonce explicitement la perte de séparation et l'échec possible de l'inégalité triangulaire; plusieurs familles mathématiques voisines sont pertinentes;
- **non établi** : originalité de Drift-X, validité générale des propriétés annoncées, conservation exacte sous les hypothèses réellement implémentées, valeur applicative;
- **prochaine action discriminante hors lecture intégrale de la thèse** : traduire le contre-exemple de triangulation en test de référence lorsque l'API de champ variable sera spécifiée et formaliser la preuve de conservation à partir des sources déjà disponibles. L'acquisition de la thèse est terminée ; poursuivre l'examen des passages utiles à partir du PDF versionné et de la provenance existante, sans relancer l'acquisition. Le cas uniforme analytique est déjà implémenté et testé.

### Écart entre la source historique et le code actuel

L'audit de la fonction `jdriftx.metric.temps_transport` révèle un verrou supplémentaire : elle calcule \(\sum_i |L_i|/\|\mathbf u_i\|\) sur une polyligne fournie. Elle ne calcule pas les caractéristiques du champ, n'effectue pas la projection \(B^\perp\), et ne dépend que de la norme des vecteurs vitesse. Les tests précédents nommaient à tort certains cas « non-symétrie », alors qu'ils démontraient soit l'égalité sous inversion, soit l'effet de la longueur du chemin.

La PR corrige les docstrings et les noms de tests pour que les tests décrivent la primitive réellement implémentée. Elle ajoute aussi `pseudo_distance_uniforme`, une référence analytique limitée aux champs uniformes 2D, avec tests de projection longitudinale, coût nul transversal, coût infini en amont, rotation et vitesse nulle. Cette fonction n'est pas une implémentation générale : elle ne résout pas les caractéristiques d'un champ variable et ne reproduit pas les approximations numériques de 2008.

## 6. Références et rôle de chaque source

Les liens ci-dessous pointent vers les documents cités; les pages indiquées précisent où se trouve le résultat mobilisé. Les références de navigation sont des comparateurs conceptuels, pas des preuves directes sur Drift-X.

| Référence | Type et emplacement utile | Ce qui est utilisé ici | Ce qu'elle ne prouve pas pour J-DriftX |
|---|---|---|---|
| Mohammadi & Brun (2006), [*Similitude généralisée et modélisation géométrique à complexité réduite*](https://doi.org/10.1016/j.crme.2006.06.007), *Comptes Rendus Mécanique*, 334(10), 634–638 | Source primaire; §3, pp. 635–636 | Définition projetée de la pseudo-distance et limites concernant séparation et triangulation | Validité de toutes les variantes numériques, conservation iso-τ complète ou originalité actuelle |
| Brun & Mohammadi (2008), [*Reduced-Order Modelling of Dispersion*](https://doi.org/10.1007/978-1-4020-8758-5_14), dans *Partial Differential Equations: Modelling and Numerical Simulation*, Springer, pp. 245–256 | Chapitre de synthèse; §2.2, pp. 248–250 | Distinction entre définition géométrique, approximation (B^\perp\approx B) et correction en champ uniforme | Une preuve indépendante de chaque propriété physique annoncée |
| Gibbons et al. (2009), [*Stationary metrics and optical Zermelo-Randers-Finsler geometry*](https://doi.org/10.1103/PhysRevD.79.044022) | Géométrie de navigation | Relation entre navigation contrôlée et géométrie de Randers/Finsler | Équivalence à l'advection pure d'un traceur passif |
| Dušek (2018), [*Zermelo Navigation Problem in Geometry*](https://doi.org/10.17818/NM/2018/4SI.16) | Présentation géométrique | Vocabulaire et formulation du problème de navigation | La définition historique projetée de Drift-X |
| Contreras & Kachroo (2020), [*The Viscosity Solution for Hamilton Jacobi Travel Time Dynamics*](https://doi.org/10.1109/TITS.2019.2946109) | Temps de parcours/Hamilton–Jacobi, contexte trafic | Comparaison avec les fonctions de temps d'arrivée définies par une équation | Même dynamique physique ou même observable que la dispersion atmosphérique |
| Sethian & Vladimirsky (2001), [*Ordered upwind methods for static Hamilton–Jacobi equations*](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/) | Méthode numérique pour Hamilton–Jacobi | Référence éventuelle si un problème de temps minimal est retenu | Justification d'un solveur pour la définition projetée sans analyse préalable |

### Comment relier ces notions à la physique

Pour un traceur passif sans diffusion, l'équation d'advection s'écrit, sous forme conservative, \(\partial_t c+\nabla\cdot(c\mathbf u)=s\), où \(c\) est la concentration et \(s\) un terme source. Si \(\nabla\cdot\mathbf u=0\), elle se réduit à \(\partial_t c+\mathbf u\cdot\nabla c=s\). Le long d'une trajectoire, la dérivée matérielle est \(Dc/Dt=\partial_t c+\mathbf u\cdot\nabla c\). Ces identités expliquent pourquoi les caractéristiques sont naturelles pour l'advection; elles ne suffisent cependant pas à transformer la pseudo-distance projetée en solution de l'équation de concentration. Il faut encore spécifier la source, les conditions initiales/aux limites et les hypothèses de réduction.

De même, \(\nabla\cdot\mathbf u=0\) contraint la cinématique du champ, mais la conservation du débit \(Q\) à travers une surface dépend aussi de la surface traversée, de son orientation, des sources/puits et du théorème de transport adapté. La conservation sur une surface iso-\(\tau\) doit donc être démontrée à partir de la transformation de coordonnées et de son jacobien, et non déduite du seul mot « divergence nulle ».

## 7. Registre des incertitudes après cette lecture

| Point | État après lecture du rapport 2006 | Ce qui reste nécessaire pour le lever |
|---|---|---|
| Implémentation Python actuelle | **Écart désormais explicite** : la fonction est un coût de polyligne qui ignore l'orientation et la projection historique | Étendre la référence seulement après avoir spécifié les caractéristiques et cas limites des champs variables; conserver la primitive de polyligne comme API distincte |
| Définition historique | **Partiellement levé** : la projection \(B\mapsto B^\perp\) et le statut de pseudo-distance sont explicités au §3 | Le PDF de thèse est obtenu ; des passages ciblés sont audités dans docs/43. Compléter la lecture des parties non examinées et vérifier la page de titre/identité binaire à partir des éléments de provenance existants. Le chapitre 2008 reste une source complémentaire |
| Domaine de validité | **Partiellement levé** : l'article suppose une caractéristique unique et écarte sources/puits | Définir précisément le traitement des séparatrices, stagnations, caractéristiques multiples et limites du domaine |
| Séparation des points | **Levé pour la construction publiée** : la source reconnaît que \(d(A,B)=0\) n'implique pas \(A=B\) | Ajouter un test analytique de reproduction; ne pas présenter cette propriété comme un défaut nouvellement découvert |
| Inégalité triangulaire | **Levé pour un cas analytique** : le champ divergence nulle \(\mathbf u=(1+9y,0)\) et trois points donnent \(d(A,C)=2>d(A,B)+d(B,C)=1.1\) | Traduire ce cas en test de référence quand l'API de champ variable sera spécifiée |
| Non-symétrie | **Partiellement levé** : la définition est orientée et fixe \(+\infty\) pour certains couples amont/aval | Formaliser la convention de domaine et distinguer coût non défini, coût étendu \(+\infty\), et trajet physiquement impossible |
| Conservation de masse | **Non levé** : les sources imposent des contraintes de conservation au modèle réduit, mais les passages lus ne démontrent pas le résultat plus précis de conservation exacte du flux sur chaque surface iso-\(\tau\) | Reconstituer le jacobien, les hypothèses sur \(\nabla\cdot\mathbf u\), les frontières et le lien avec le scalaire \(c\) dans la thèse/chapitre |
| Originalité | **Non levé** : un article de 2006 décrit déjà la pseudo-distance et son usage pour les solutions de similitude | Comparer les équations et résultats spécifiques, sans revendiquer la pseudo-distance elle-même comme nouvelle |
| Filiation avec les métriques d'adaptation de maillage | **Non établie** : une référence sur la génération de maillages anisotropes ne prouve pas une filiation directe avec la pseudo-distance travel-time | Trouver une source historique explicite ou présenter le rapprochement uniquement comme analogie conceptuelle |
| Date de la thèse | **Métadonnées incohérentes** : la bibliographie du dépôt indique 2006, alors que l'article de 2006 cite la thèse comme 2007 | Vérifier la page de titre ou le dépôt institutionnel de la thèse avant de normaliser la référence |

### Prochaine action à plus forte valeur

Ne pas lancer encore un solveur 2D. Reproduire d'abord la pseudo-distance historique dans le champ uniforme, avec cas de test calculés à la main. En parallèle, formaliser la conservation de masse à partir des sources déjà disponibles. Le PDF de la thèse est déjà obtenu ; poursuivre la lecture ciblée/intégrale et les contrôles de provenance à partir des éléments versionnés, sans relancer l'acquisition. Le chapitre de 2008 reste une source complémentaire à consulter au-delà des pages déjà extraites. Si une source primaire reste partiellement examinée, documenter précisément cette limite plutôt que combler les lacunes par inférence.

## Références web consultées

- Gibbons et al. (2009), DOI [10.1103/PhysRevD.79.044022](https://doi.org/10.1103/PhysRevD.79.044022).
- Dušek (2018), DOI [10.17818/NM/2018/4SI.16](https://doi.org/10.17818/NM/2018/4SI.16).
- *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), DOI [10.1016/j.difgeo.2024.102177](https://doi.org/10.1016/j.difgeo.2024.102177).
- Markvorsen et al. (2025), [arXiv:2508.07274](https://arxiv.org/abs/2508.07274).
- Contreras & Kachroo (2020), DOI [10.1109/TITS.2019.2946109](https://doi.org/10.1109/TITS.2019.2946109).
- Sethian & Vladimirsky (2001), [Ordered upwind methods for static Hamilton–Jacobi equations](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/).
