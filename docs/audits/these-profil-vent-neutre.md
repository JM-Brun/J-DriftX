# Thèse de Brun — profil logarithmique et identification du vent

**Portée et confiance.** Les pages imprimées 37, 41 et 42 (PDF 46, 50 et 51) de la [thèse versionnée](<../../raw/Modèles à complexité réduite de transport pour applications environnementales - pub00023263.pdf>) ont été repérées ; les pages 41–42 ont été vérifiées sur le fac-similé. Les conséquences algébriques ci-dessous sont de confiance élevée sous leurs hypothèses. Elles ne constituent ni un calage historique ni une validation de terrain.

## Formule, origine des hauteurs et domaine

Le §2.4.1 donne, pour une atmosphère neutre et la couche inertielle, le profil

$$
\bar U(z)=\frac{u_*}{\kappa}\log\!\left(\frac{z-d}{z_0}\right),
\qquad u_*=\sqrt{-u'w'}\quad\text{(notation imprimée)}.
$$

Dans cette note, $z$ et $d$ sont mesurés depuis le même niveau, $z_0>0$ est une longueur de rugosité, $u_*>0$ une vitesse, $\kappa>0$ sans dimension et $\log$ le logarithme naturel. Le texte présente $d$ comme une hauteur de déplacement et décrit $z_0$ comme la hauteur extrapolée de vitesse nulle. Or, pour l'équation imprimée, le zéro algébrique est **$z=d+z_0$**. Si « hauteur » désigne la hauteur effective $z-d$, l'expression $z_0$ peut se comprendre ; si elle désigne la même coordonnée $z$ que la formule, les deux coïncident uniquement lorsque $d=0$. L'intention de la phrase n'est pas tranchée : [DRX-ERR-056](../46-registre-erreurs-incoherences-documentaires.md). Ce zéro est une extrapolation de la loi, pas une condition de non-glissement démontrée au niveau géométrique du sol ou du couvert.

Mathématiquement, l'argument du logarithme est strictement positif si $z>d$. Pour que la vitesse scalaire donnée par cette formule soit positive avec $u_*>0$, il faut $z>d+z_0$. **Cela ne suffit pas à rendre le profil physiquement applicable** : la thèse situe la loi dans la couche inertielle, distingue plus bas une sous-couche influencée par les obstacles et indique qu'une correction est nécessaire hors neutralité. La valeur indicative de 100 m dans le texte n'est pas une frontière universelle. Une étude expérimentale sur couvert forestier emploie également $d$, $z_0$ et une correction de stabilité distincte : [Floors et al. (2021)](https://wes.copernicus.org/articles/6/1379/2021/).

La racine imprimée pour $u_*$ est réelle lorsque le produit indiqué est non positif. Le texte parle de contrainte de Reynolds, mais n'imprime pas de barre de moyenne dans (2.3) ; si ce produit désigne la covariance moyenne $\overline{u'w'}$, la même condition de signe s'applique à cette covariance. La définition présuppose une convention de signe et la composante de vent choisie. Si $u_*=0$, le profil formel est nul partout où le logarithme est défini et les raisonnements d'inversion ci-dessous ne s'appliquent pas.

## Extrapolation à une autre hauteur

Si $d$ et $z_0$ sont connus, que les deux hauteurs sont dans le domaine d'application du même profil et que $z_r>d+z_0$, la valeur mesurée $U_r=\bar U(z_r)>0$ donne

$$
\bar U(z)=U_r\frac{\ln((z-d)/z_0)}{\ln((z_r-d)/z_0)}.
$$

Connaître $z_0$ seul ne détermine pas cette extrapolation si $d$ est inconnu ; la remarque du texte sur l'usage de la rugosité doit donc être lue avec la convention de déplacement. Les deux hauteurs, l'origine verticale, la direction et la période des mesures, la neutralité et l'homogénéité du secteur doivent aussi être compatibles. L'équation ne reconstruit pas une direction de vent variable avec l'altitude.

## Deux observations ne déterminent pas trois paramètres libres

Supposons deux valeurs idéales $0<U_1<U_2$ aux hauteurs $z_1<z_2$, une même valeur connue de $\kappa$ et les trois paramètres $d,z_0,u_*$ libres. Pour tout $0\le d<z_1$, les choix

$$
A(d)=\frac{\ln[(z_2-d)/(z_1-d)]}{U_2/U_1-1},\qquad
z_0(d)=(z_1-d)e^{-A(d)},\qquad
u_*(d)=\frac{\kappa U_1}{A(d)}
$$

sont positifs, vérifient $z_0<z_1-d$ et reproduisent exactement les deux vitesses. Une infinité de triplets est donc compatible avec ces deux observations ; une troisième mesure peut aider à contraindre le problème mais ne garantit ni unicité ni identification robuste dans un cas réel.

Avec $z_1=10$ m, $z_2=20$ m, $U_1=5$ m/s, $U_2=6$ m/s et $\kappa=0{,}4$, on obtient notamment :

| $d$ (m) | $z_0$ (m) | $u_*$ (m/s) | $\bar U(10)$ (m/s) | $\bar U(20)$ (m/s) | $\bar U(30)$ (m/s) |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,3125 | 0,5771 | 5 | 6 | 6,5850 |
| 5 | 0,02058 | 0,3641 | 5 | 6 | 6,4650 |

Ce calcul est synthétique : il ne prouve pas que ces hauteurs soient dans la couche inertielle pour un couvert donné. Il illustre un défaut d'identifiabilité de la famille mathématique, non une erreur quantitative du modèle historique.

Si $d$ est connu, la différence $U_2-U_1$ détermine formellement $u_*$, puis $z_0$. Mais lorsque $U_2-U_1$ est très petit, $u_*$ tend vers zéro et l'expression de $z_0$ dépend exponentiellement de l'inverse de cette différence : le bruit peut rendre l'estimation très sensible. Pour $U_2=U_1>0$ et $z_2>z_1$, aucun profil de cette famille avec $u_*>0$ et $d<z_1$ ne passe exactement par les deux points.

## Reprise

Pour utiliser cette loi, documenter le niveau de référence, $d$, $z_0$, $u_*$ ou les mesures qui les contraignent, les unités, le secteur et la période, les hauteurs effectivement dans la couche d'application et la correction de stabilité retenue. Évaluer l'incertitude et les conditions où l'extrapolation est refusée ; ne pas transformer la loi en profil de canopée ou en vent tridimensionnel complet. La [liste des travaux](these-travaux-restants.md) suit la poursuite de l'audit du chapitre 2 et des liens au noyau actuel.
