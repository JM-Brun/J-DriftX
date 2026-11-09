# Thèse de Brun — interface entre source locale et transport lointain

**Portée.** Cette note rassemble les grandeurs nécessaires à TH-03 dans la [liste des travaux restants](these-travaux-restants.md). Les équations (5.50)–(5.67), pp. imprimées 102–103 (PDF 111–112), et (7.12)–(7.13), p. 129 (PDF 138), ont été contrôlées sur le fac-similé de la [thèse versionnée](<../../raw/Modèles à complexité réduite de transport pour applications environnementales - pub00023263.pdf>). Les bilans et exemples ci-dessous sont des reconstructions explicites ; ils n'établissent pas le comportement du code historique.

## Grandeurs à ne pas confondre

Notons $H$ la hauteur du plan de séparation, $S$ sa section horizontale, $V$ le domaine de normalisation, $\Omega_+=V\cap\{z>H\}$, et $s_i=c_{\Delta t}^{,i}$ le terme volumique de la buse $i$ pendant un intervalle $\Delta t$. Les domaines et les temps doivent être effectivement alignés avant toute comparaison.

| Grandeur | Définition et unité | Source et hypothèses |
|---|---|---|
| Débit éjecté $Q_0^i$ | Masse par temps, kg/s. | (5.50)–(5.55) normalisent la forme de chaque buse pour obtenir $\int_Vs_i\,dV=Q_0^i$, si son intégrale de normalisation est finie et non nulle. Cela ne dit pas quelle fraction traverse $H$. |
| Source au-dessus du plan $S_+(t)$ | $\int_{\Omega_+}\sum_i s_i\,dV$, kg/s. | (5.61)–(5.62), (5.66) : intégrée en temps, elle donne la **masse injectée dans ce volume**. Elle n'est pas un flux au plan par définition. |
| Inventaire au-dessus du plan $M_+(t)$ | $\int_{\Omega_+}c_{loc}(t)\,dV$, kg. | (5.56) ajoute des contributions locales ; (5.63) intègre $c_{loc}$ au temps final. Pour la seule récurrence additive, l'incrément intégré est la source injectée ; cette égalité ne décrit pas un bilan de transport complet avec flux et pertes. L'égalité avec la masse cumulée exige aussi l'inventaire initial nul ou sa soustraction. |
| Flux advectif au plan $\Phi_H(t)$ | $\int_S w c_{loc}\,dS$, kg/s. | (5.64) intègre ce débit en temps pour obtenir une masse traversante en kg. C'est le flux advectif signé si $w$ change de signe ; des flux diffusifs ou d'autres vitesses de chute nécessiteraient une définition supplémentaire. |
| Entrée lointaine $c^+$ et masse $M_C$ | La branche intégrée verticalement de (7.12) donne $c^+=\int_H^\infty c_{loc}\,dz$ en kg/m², puis (7.13) donne $M_C=\int c^+dS$ en kg. | Sous mêmes domaine, temps et hypothèses d'intégrabilité, cette branche représente un inventaire au-dessus de $H$. Son unité et sa définition ne font pas d'elle une masse traversante. L'autre branche imprimée est dimensionnellement différente : [docs/43](../43-audit-these-brun-conservation-g0s.md). |
| Estimation sur collecteurs | Pour chaque essai, le volume estimé entre lignes est normalisé par le volume pulvérisé ; le résultat est un pourcentage sans dimension. | §§5.7–5.8 : cinq lignes à 2,5 m accumulent quatre passages ; l'estimation utilise une interpolation spatiale et une efficacité de collecte. Ce n'est pas une concentration ponctuelle ni une mesure directe de la source volumique. Voir la [fiche](../bibliographie/sources/these-brun.md). |

Si les calculs sont effectués en masse et les observations en volume, la comparaison des fractions exige une convention de conversion cohérente pour le mélange ; une densité et une composition identiques rendent les rapports masse/masse et volume/volume équivalents. L'égalité ne doit pas être présumée pour des objets ou mélanges différents.

## Bilan physique au-dessus du plan

Pour un domaine fixe $\Omega_+$ et un flux massique total $J$, posons $\Phi_H=\int_S J\cdot e_z\,dS$ positif vers le haut, $\Phi_{autres}=\int_{\partial\Omega_+\setminus S}J\cdot n\,dS$ positif vers l'extérieur et $L_+$ le taux de perte interne. La conservation donne

$$
\frac{dM_+}{dt}=S_+-L_++\Phi_H-\Phi_{autres}.
$$

En régime stationnaire, $dM_+/dt=0$ conduit à $\Phi_{autres}=S_+-L_++\Phi_H$, pas à $\Phi_H=S_+$. L'égalité approchée (5.67) demande donc une relation quantitative additionnelle entre ces termes ; des unités identiques et une vitesse stationnaire ne suffisent pas.

### Contre-exemple stationnaire avec source normalisée

Prenons une colonne de section $1$ m², $0\le z\le3$ m, un vent ascendant constant $w=1$ m/s et une source volumique uniforme $s=1$ kg·m⁻³·s⁻¹, sans dépôt ni diffusion. Imposons $c(0)=0$ et $J_z=wc$. La solution stationnaire $c(z)=sz/w$ vérifie $dJ_z/dz=s$ ; par exemple $c(1\,\mathrm m)=1$ kg/m³. Son débit total à la sortie est 3 kg/s, comme l'intégrale de la source dans tout le volume. Pour $H=1$ m :

$$
\Phi_H=1\ \mathrm{kg/s},\qquad S_+=2\ \mathrm{kg/s},\qquad
\Phi_{haut}=3\ \mathrm{kg/s}.
$$

Le bilan stationnaire est exact : $\Phi_{haut}=\Phi_H+S_+$. Mais le flux qui traverse le plan et la source placée au-dessus diffèrent d'un facteur 2. La source de l'exemple est uniformément répartie et normalisée sur le volume ; elle ne prétend pas reproduire la forme du jet ni quantifier l'erreur de l'essai historique. Cette solution utilise une équation de transport avec sortie par le haut et n'est **pas** la récurrence purement additive de (5.56). Elle montre qu'un bilan physique stationnaire peut conserver la masse sans imposer (5.67), même lorsque le champ de concentration et le vent sont stationnaires et qu'il n'y a ni puits ni fuite latérale. Cet exemple renforce l'analyse de DRX-ERR-042.

## Stationnarité du vent et flux intégré

L'équation (5.65) remplace l'intégrale temporelle de $\Phi_H$ par $\Delta t$ fois une valeur de flux. C'est exact si le flux est constant, ou si la valeur retenue est sa moyenne sur l'intervalle ; un vent $w$ constant ne garantit pas à lui seul que $c_{loc}$ ou $wc_{loc}$ le soient.

Par exemple, supposons $w$ indépendant du temps et utilisons la même récurrence additive que (5.56) au plan, avec $s=\sum_i s_i$ constant pendant l'intervalle. Alors

$$
\Phi_H(t+\Delta t)-\Phi_H(t)
=\Delta t\int_S ws\,dS.
$$

Si cette intégrale est strictement positive, le flux aux deux extrémités diffère malgré le vent constant. Avec, en outre, une interpolation linéaire de $c_{loc}$ et un flux initial nul, le flux moyen vaut la moitié du flux final : utiliser la valeur finale comme flux constant donnerait le double de l'intégrale temporelle correspondante. Cette interpolation est une hypothèse de l'exemple, pas une étape établie du calcul historique. Une évaluation à la moyenne temporelle pourrait satisfaire (5.65) ; les conventions utilisées en pratique restent à retrouver.

## État et travaux distincts

Le tableau, le bilan et les contre-exemples clôturent **l'analyse documentaire de TH-03** : ils identifient les objets, leurs unités et les hypothèses nécessaires sans décréter que l'approximation est erronée pour un essai donné. La conservation générale du modèle lointain reste suivie dans [docs/43](../43-audit-these-brun-conservation-g0s.md) et [#123](https://github.com/JM-Brun/J-DriftX/issues/123). La reproduction du code et la comparaison aux observations individuelles restent conditionnées à leur identification, à leurs unités et à leurs droits ; elles sont distinctes de ce contrôle.
