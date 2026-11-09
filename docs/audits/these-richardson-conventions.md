# Thèse de Brun — conventions des nombres de Richardson

**Périmètre et confiance.** Les pages imprimées 38 et 168 (PDF 47 et 177) ont été contrôlées sur le fac-similé de la [thèse versionnée](<../../raw/Modèles à complexité réduite de transport pour applications environnementales - pub00023263.pdf>) : confiance élevée sur ce qu'elles impriment. Les définitions ci-dessous sont des **conventions de comparaison explicitement choisies**, et non une correction historique certaine.

## Ce que la thèse permet et ne permet pas d'affirmer

Au chapitre 2, (2.2) imprime $Ri=\beta\,(\partial_zT)/(\partial_zU)^2$ et présente $\beta$ comme coefficient de dilatation. Si $\beta$ est le coefficient usuel en K⁻¹, $T$ en K, $z$ en m et $U$ en m/s, cette expression a pour dimension s²/m et n'est pas un nombre sans dimension. Une définition dimensionnée différente de $\beta$ ou une adimensionnalisation non explicitée reste possible : [DRX-ERR-038](../46-registre-erreurs-incoherences-documentaires.md).

L'annexe D.2.2 emploie $Ri_f$ : une phrase décrit le rapport cisaillement/flottabilité, la suivante flottabilité/cisaillement. Aucune formule n'y fixe les signes et les termes ; ces deux descriptions ne sont pas interchangeables. En particulier, un rapport flottabilité/cisaillement peut être nul en stratification neutre lorsque le dénominateur est non nul, tandis que son inverse n'est alors pas défini. L'intention historique n'est pas établie : [DRX-ERR-035](../46-registre-erreurs-incoherences-documentaires.md).

## Deux définitions distinctes pour une reconstruction

Dans un modèle simplifié de couche cisaillée, prenons $z$ vers le haut, une température potentielle moyenne $\Theta(z)$, une référence $\Theta_0>0$, $g>0$ et une vitesse moyenne horizontale $U(z)$. Si le cisaillement $S=\partial_zU$ est non nul, un nombre de Richardson **de gradient** est

$$
N^2=\frac{g}{\Theta_0}\partial_z\Theta,\qquad
Ri_g=\frac{N^2}{S^2}.
$$

Ici $N^2$ peut être négatif ; ce symbole désigne alors le carré signé de fréquence de flottabilité, sans supposer une fréquence réelle. Une variante atmosphérique utilise la température potentielle virtuelle et peut inclure les deux composantes de cisaillement horizontal : il faut annoncer la convention retenue. Cette grandeur ne résulte pas simplement d'un changement de nom de la température réelle imprimée dans (2.2). Les dimensions sont $[N^2]=[S^2]=$ s⁻². Dans la formulation correspondante avec deux composantes horizontales, [Mellor (1975)](https://www.gfdl.noaa.gov/bibliography/related_files/glm7501.pdf) inclut séparément le coefficient de dilatation et $g$ dans le numérateur.

Avec les fluctuations turbulentes $u',w',\theta'$ et la même convention simplifiée, définissons le terme de flottabilité $B$ et la production par cisaillement $P$ du bilan d'énergie cinétique turbulente :

$$
B=\frac{g}{\Theta_0}\overline{w'\theta'},\qquad
P=-\overline{u'w'}\,\partial_zU,\qquad
Ri_f=-\frac{B}{P}\quad(P>0).
$$

Les deux termes $B$ et $P$ sont en m²/s³. Le signe moins rend $Ri_f>0$ lorsque la flottabilité **consomme** de l'énergie turbulente ($B<0$), et $Ri_f<0$ lorsqu'elle en produit ($B>0$). Si $P=0$, ce rapport n'est pas défini ; si $P<0$, il faut analyser le bilan et ne pas appliquer sans examen ces interprétations. La définition par les flux et celle par les gradients sont distinctes ; voir [Williams et al. (2019), équations (1)–(3)](https://repository.library.noaa.gov/view/noaa/20362/noaa_20362_DS1.pdf).

Une relation entre les deux exige une fermeture supplémentaire. Si $K_m,K_h>0$, si $\overline{u'w'}=-K_m\partial_zU$ et $\overline{w'\theta'}=-K_h\partial_z\Theta$, alors $P=K_mS^2$, $B=-K_hN^2$ et

$$
Ri_f=\frac{K_h}{K_m}Ri_g=\frac{Ri_g}{Pr_t},\qquad Pr_t=\frac{K_m}{K_h}.
$$

Cette égalité découle de ces hypothèses de fermeture ; elle ne permet pas d'identifier les deux nombres en général. Une fermeture contre-gradient, des transports non locaux ou un $Pr_t$ variable exigent d'autres informations. Les conclusions du travail expérimental cité concernent ses conditions d'étude et ne fournissent pas un seuil universel de turbulence.

## Exemple numérique et singularités

Pour $\Theta_0=300$ K, $g=9{,}81$ m/s², $\partial_zU=0{,}1$ s⁻¹, $\partial_z\Theta=0{,}02$ K/m, $K_m=1$ m²/s et $K_h=0{,}5$ m²/s, la fermeture ci-dessus donne :

| Grandeur | Valeur synthétique |
|---|---:|
| $N^2$ | $0{,}000654$ s⁻² |
| $P$ | $0{,}010$ m²/s³ |
| $B$ | $-0{,}000327$ m²/s³ |
| $Ri_g$ | $0{,}0654$ |
| $Ri_f$ | $0{,}0327$ |
| $Pr_t$ | $2$ |

Le signe correspond ici à une stratification statiquement stable et à une consommation turbulente par flottabilité ; les deux nombres sont positifs mais diffèrent d'un facteur 2. L'exemple est construit, sans données de campagne, et ne justifie ni une classe de Pasquill ni une valeur de $Pr_t$ pour le site historique.

Si $S=0$, $Ri_g$ est indéfini, même lorsque $\partial_z\Theta=0$ ; si $P=0$, $Ri_f$ est indéfini. Un programme ne devrait pas convertir silencieusement ces cas en zéro. Pour un seul cisaillement $S\ne0$ et un gradient non nul, une petite perturbation relative donne au premier ordre $\delta Ri_g/Ri_g\simeq\delta(\partial_z\Theta)/(\partial_z\Theta)-2\delta S/S$ : une estimation de gradient incertaine, notamment lorsque $S$ est faible, peut donc rendre le rapport très sensible. Ce diagnostic local ne remplace pas une propagation complète des incertitudes.

La proximité du sol ne fixe pas à elle seule le signe de la stratification : sur une couche où $\Theta(z)=300+0{,}02z$ K et $U(z)=1+0{,}1z$ m/s, avec $z$ mesuré en mètres, $Ri_g=0{,}0654$ dans l'approximation $\Theta_0=300$ K à toutes les hauteurs de cette couche. Il s'agit d'un contre-exemple à une interprétation universelle de la phrase de l'annexe, pas d'une reconstitution du site. Les conditions réelles et les éventuelles inversions évoluent avec la météorologie.

## Contrat de réutilisation

Avant de calculer ou d'exploiter un Richardson, préciser sa variante, les termes et signes, les températures et unités, le domaine vertical, la méthode d'estimation des gradients ou flux, les incertitudes et le traitement des dénominateurs proches de zéro. Si une fermeture est utilisée, donner $K_m,K_h$ ou $Pr_t$ et son domaine. Une classe de stabilité discrète reste une entrée distincte : aucune conversion universelle vers la classe utilisée par J-DriftX n'est établie par les passages audités. Les décisions scientifiques et paramètres historiques restent à documenter dans la [liste de reprise](these-travaux-restants.md).
