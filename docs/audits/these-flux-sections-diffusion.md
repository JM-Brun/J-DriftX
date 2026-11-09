# Thèse de Brun — flux de section et diffusion latérale

**Portée.** Cette note explicite une hypothèse du bilan de section utilisé dans la thèse et donne un contre-exemple construit. Elle ne décrit ni les conditions aux limites du logiciel historique, ni une erreur mesurée de sa simulation. Le bilan général en coordonnées régulières reste dans [docs/32](../32-conservation-coordonnees-travel-time.md) ; l'identification de la grandeur conservée du modèle lointain reste ouverte dans [docs/43](../43-audit-these-brun-conservation-g0s.md).

## Ce que donne le passage de l'annexe B

À la page imprimée 154 (PDF 163), l'équation (B.46) considère une diffusion transverse, sans frontière solide, et écrit $U\partial_x c=K\partial_{zz}c$ ; le coefficient transverse y est noté $K_x$. La page imprimée 156 (PDF 165) énonce ensuite le bilan de section (B.55) sur $z\in\mathbb R$. Ces deux pages ont été contrôlées sur le fac-similé. La source est une ligne de longueur $H$ et de débit $Q$ ; ici $H$ n'est pas une hauteur de rejet.

Pour comprendre le rôle de la frontière, prenons $U,K>0$ constants et une solution suffisamment régulière de cette équation. Sur un intervalle transverse fini $[z_1,z_2]$, intégrer l'équation donne exactement

$$
\frac{d}{dx}\left(U\int_{z_1}^{z_2}c\,dz\right)
=K\bigl[\partial_zc(x,z_2)-\partial_zc(x,z_1)\bigr].
$$

Le débit advectif de cette portion de section est donc constant si le **flux diffusif net** par ses deux bords s'annule ; il n'est pas nécessaire que les deux flux soient individuellement nuls. Pour passer à la section entière de (B.55), il faut notamment justifier l'intégrabilité, le passage à la limite et l'annulation du flux diffusif net à l'infini. Identifier ensuite ce débit à $Q/H$ demande un bilan de source et une normalisation compatibles. L'équation seule ne fournit pas cette valeur.

Ce bilan réduit néglige la diffusion longitudinale dans le flux de section. Pour l'équation complète avec diffusion isotrope $D$, le flux à utiliser est $\mathbf J=c\mathbf u-D\nabla c$ et son intégrale sur une section comprend aussi $-D\partial_xc$. C'est ce flux total qui intervient dans le théorème de divergence de [docs/32](../32-conservation-coordonnees-travel-time.md).

## Contre-exemple stationnaire sur une section finie

Sur le cube $0\le x,y,z\le1\,\mathrm m$, prenons $\mathbf u=(1,0,0)\,\mathrm{m/s}$, $D=1\,\mathrm{m^2/s}$ et, en unités SI,

$$
c(x,y,z)=2-0{,}2x-0{,}1y^2\quad\mathrm{kg/m^3}.
$$

Les coefficients de $x$ et $y^2$ portent respectivement les unités kg/m⁴ et kg/m⁵. La concentration est positive sur le cube. Le champ est stationnaire et incompressible ; sans source ni puits, il vérifie l'équation complète car $\nabla^2c=-0{,}2$ et $\mathbf u\cdot\nabla c=-0{,}2$ en unités SI. Il vérifie aussi l'équation réduite analogue à (B.46), en prenant $y$ comme direction transverse : $U\partial_xc=D\partial_{yy}c$. Il s'agit d'un problème de frontières construit pour cet exemple, pas du panache infini ni de la source linéique de la thèse.

Le flux total vaut $\mathbf J=(c+0{,}2,\;0{,}2y,\;0)$ en kg·m⁻²·s⁻¹ et $\nabla\cdot\mathbf J=0$. Les débits intégrés sur les sections de 1 m² sont

$$
\Phi(0)=\frac{13}{6}\ \mathrm{kg/s},\qquad
\Phi(1)=\frac{59}{30}\ \mathrm{kg/s},\qquad
\Phi(1)-\Phi(0)=-\frac15\ \mathrm{kg/s}.
$$

Le flux latéral sortant vaut $1/5$ kg/s par la face $y=1$ m et zéro sur les trois autres faces latérales. Ainsi $\Phi(1)-\Phi(0)+\Phi_{\rm lat}=0$ : la masse est bien conservée dans le bilan, mais les flux de section diffèrent. Le vent est tangent aux parois latérales ; seule la diffusion traverse la face $y=1$. Imposer une paroi imperméable à cet endroit exclurait cette solution.

Dans le modèle réduit, le débit advectif seul vaut $59/30$ kg/s en $x=0$ et $53/30$ kg/s en $x=1$ ; il décroît aussi de $1/5$ kg/s. La différence constante de $1/5$ kg/s entre les flux totaux et advectifs de chaque section provient ici de la diffusion longitudinale. Les deux bilans sont compatibles parce que $\partial_{xx}c=0$ pour cet exemple particulier.

La carte uniforme $\tau=x/U$, $\eta_1=y$, $\eta_2=z$ est régulière et son jacobien vaut $U$ : même une carte de temps exacte ne supprime pas les flux diffusifs latéraux. L'exemple ne contredit pas (B.55), qui porte sur une autre section et d'autres conditions, et ne démontre pas que le modèle lointain historique possède ce champ ou ces frontières.

## Conséquence pour la reprise

Pour revendiquer une égalité de flux entre sections, préciser le flux total ou l'approximation retenue, le domaine, le stockage, les sources et puits et le **flux net latéral**, puis relier la première section à la source. Pour (7.12)–(7.13), établir d'abord si la quantité visée est un inventaire ou un débit : le résultat ci-dessus ne transforme pas $M_C$ en flux. Les éléments manquants de la construction historique sont suivis par TH-02 dans la [liste de reprise](these-travaux-restants.md) et dans [#123](https://github.com/JM-Brun/J-DriftX/issues/123).
