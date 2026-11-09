# Thèse de Brun — audit de l'intégration temporelle de l'annexe C

**Périmètre et confiance.** Les équations (C.10)–(C.22), p. imprimée 160 (page PDF 169), ont été contrôlées sur le fac-similé de la [thèse versionnée](<../../raw/Modèles à complexité réduite de transport pour applications environnementales - pub00023263.pdf>). Les écarts de transcription ci-dessous sont de confiance élevée. Les calculs associés sont des reconstructions mathématiques sous hypothèses explicites : ils ne permettent pas de conclure sur le programme historique, non examiné.

## Ce que la source imprime

L'annexe annonce une intégration en plusieurs étapes de type Runge–Kutta, puis :

1. (C.10)–(C.11) présentent un développement temporel dont le terme de premier ordre vaut $\Delta t\,du/dt$.
2. La factorisation (C.12), pour $s=3$, place les dénominateurs $3$, $2$ et $1$ de l'extérieur vers l'intérieur.
3. Dans l'algorithme (C.14)–(C.18), la variable $C$ est mise à jour en (C.16), mais la dernière ligne imprimée est $u^{n+1}=u^n$. Prise littéralement, cette ligne recopie l'ancienne valeur ; aucune affectation explicite de $C$ à la sortie n'apparaît dans ce bloc.
4. En (C.20), avec $p=0,1,2$, la nouvelle valeur porte l'indice supérieur $(n+1,p+1)$, alors que l'étape utilisée au membre droit porte $(n,p)$. La sortie (C.21) est quant à elle notée $u_j^{n+1}=u_j^{n,3}$. La correspondance entre les étapes produites, les étapes consommées et la sortie demande donc une convention qui n'est pas explicitée dans ces lignes.

Ces observations ne démontrent pas que le logiciel ancien contenait les mêmes écritures ni qu'une seule correction est possible.

## Contrôle de la factorisation imprimée

Appliquons formellement (C.12) à l'équation test linéaire scalaire $u'=\lambda u$, en posant $z=\lambda\Delta t$. Le facteur extérieur imprimé donne, pour $s=3$,

$$
R_{C.12}(z)=1+\frac z3+O(z^2).
$$

Or le développement de la solution exacte sur un pas est $e^z=1+z+z^2/2+z^3/6+O(z^4)$. Le coefficient linéaire de la factorisation littérale est $1/3$ au lieu de $1$ : elle ne reproduit donc pas même le terme du premier ordre de (C.10)–(C.11), sous cette lecture et si $\Delta t$ désigne le même pas dans les deux écritures. Les points de suspension et l'emboîtement imprimés ne déterminent pas ici de façon fiable les autres coefficients : aucun polynôme complet n'est attribué à (C.12). Ce contrôle porte sur la **formule imprimée** ; il ne certifie pas les coefficients utilisés dans un calcul historique.

## Reconstruction conditionnelle des trois étapes de (C.20)

La différence des indices empêche une exécution littérale non ambiguë. Pour déterminer une conséquence possible des **dénominateurs imprimés**, supposons séparément que $u^{n,0}=u^n$, que le résultat de chaque étape alimente la suivante et que $u^{n+1}$ soit la troisième étape. Pour une équation semi-discrète $u'=L(u)$, cela donne la reconstruction

$$
w^0=u^n,\qquad
w^{p+1}=u^n+\frac{\Delta t}{4-p}L(w^p)\quad(p=0,1,2),
\qquad u^{n+1}=w^3.
$$

Cette convention est une hypothèse de lecture, **pas** la transcription littérale des indices de (C.20)–(C.21). Pour $L(u)=\lambda u$, elle fournit

$$
R_{20}(z)=1+\frac z2+\frac{z^2}{6}+\frac{z^3}{24},
$$

dont le coefficient du premier ordre vaut $1/2$. Le même constat se voit sans analyse spectrale : pour un champ uniforme et $u'=g=a\ne0$ constant, cette reconstruction avance de $a\Delta t/2$ au lieu de $a\Delta t$. À temps final fixé $T$, elle donnerait $u(T)=u(0)+aT/2$ quel que soit le nombre de pas ; sa différence avec $u(0)+aT$ ne disparaît pas quand le pas tend vers zéro. Ce contre-exemple concerne exclusivement la reconstruction ci-dessus, et non une implémentation historique inconnue.

À l'inverse, si l'on choisit à titre illustratif les dénominateurs $3-p$, le polynôme linéaire devient $1+z+z^2/2+z^3/6$. Cela ne suffit pas à établir l'ordre trois pour une équation non linéaire : pour $u'=u^2$, $u(0)=1$, cette récurrence illustrative donne $1+h+h^2+11h^3/12+O(h^4)$, alors que la solution exacte vaut $1/(1-h)=1+h+h^2+h^3+O(h^4)$. Ces dénominateurs ne sont pas attribués au texte ou au code comme correction historique.

## Conséquences pour la reproduction

- Retrouver le code ou une source primaire décrivant l'ordre des étapes, leurs indices et la variable renvoyée.
- Spécifier si la viscosité physique et la viscosité numérique se cumulent, ainsi que la règle de pas et les conditions aux limites ; ces questions sont distinctes de la cohérence temporelle.
- Définir les tests de cohérence et d'ordre sur des équations linéaire **et** non linéaire avant de tester la stabilité ou de comparer des trajectoires de canopée.
- Conserver séparément la transcription, toute reconstruction et son domaine de validité. Aucune de ces étapes ne constitue une validation sur données physiques.

La [fiche de lecture](../bibliographie/sources/these-brun.md) décrit les autres contrôles de l'annexe C et la reproductibilité du modèle historique.
