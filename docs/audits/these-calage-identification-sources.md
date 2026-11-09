# Thèse de Brun — calage et identification des sources

**Statut :** analyse du texte et exemples synthétiques ; ni transcription du code historique ni validation sur mesures. La [fiche de lecture](../bibliographie/sources/these-brun.md) et [DRX-ERR-027](../46-registre-erreurs-incoherences-documentaires.md) conservent le constat documentaire ; la [liste des travaux](these-travaux-restants.md) suit les informations encore nécessaires.

## Fonction objectif et unités

Dans le fac-similé, la page imprimée 131 (PDF 140) donne, en (7.21)–(7.22), un objectif qui somme la norme des résidus de vent et celle des résidus de concentration. La page 132 (PDF 141) précise une norme $L^2$ discrète aux points de mesure et indique que $p$ regroupe notamment les variables de domaine, de topographie et de source. Ces passages ne spécifient pas de normalisation ni de poids entre les deux blocs. Une normalisation dans le code ou une autre convention non retrouvée reste possible.

Sous les unités usuelles, le premier terme est en m/s et le second en kg/m³ ; leur somme n'a pas d'unité physique commune. Le problème n'est pas seulement typographique : **si l'on additionne directement les valeurs numériques**, un changement d'unité d'un bloc peut changer le minimum. Considérons une observation de chaque type, $p\in[0,1]$ sans dimension et les réponses synthétiques

$$
u(p)=(1+2p)\ \mathrm{m/s},\quad u_{obs}=1\ \mathrm{m/s},\qquad
c(p)=(2-p)\ \mathrm{kg/m^3},\quad c_{obs}=1\ \mathrm{kg/m^3}.
$$

Avec une seule observation par bloc, chaque norme $L^2$ est une valeur absolue. Pour les mêmes quantités physiques, le calcul de la somme numérique non normalisée donne :

| Unité utilisée pour la concentration | Expression numérique de l'objectif | Minimum sur $[0,1]$ |
|---|---|---|
| kg/m³ | $2p+(1-p)=1+p$ | $p=0$ |
| g/m³ | $2p+1000(1-p)=1000-998p$ | $p=1$ |

Ce contre-exemple est un problème inverse jouet ; il ne prétend pas être une sortie du modèle de dispersion ni montrer les paramètres historiques réellement obtenus. Le changement du résultat provient de la pondération numérique implicite, pas d'un changement physique des observations. En outre, si une norme est la racine de la somme des carrés sans division par le nombre de points, dupliquer toutes les observations d'un bloc $k$ fois multiplie ce bloc par $\sqrt{k}$ ; le texte ne précise pas ici cette convention de moyenne.

## Contrat de reconstruction proposé

Pour une reconstruction distincte de l'histoire, définir avant le calcul :

1. Les prédictions aux positions et temps d'observation, les unités, le domaine admissible de $p$ et les données de calibration, avec leurs valeurs et leur provenance.
2. Des échelles strictement positives $s_u$ et $s_c$ exprimées dans les unités respectives de chaque bloc, des poids sans dimension $w_u,w_c\ge0$ non tous deux nuls et la convention choisie pour les nombres de mesures $n_u,n_c>0$. Une possibilité, parmi d'autres, est

   $$
   J_{\mathrm{rec}}(p)=
   w_u\frac{\lVert u(p)-u_{obs}\rVert_2}{s_u\sqrt{n_u}}
   +w_c\frac{\lVert c(p,u(p))-c_{obs}\rVert_2}{s_c\sqrt{n_c}}.
   $$

   Convertir une grandeur et son échelle dans la même unité laisse cet objectif inchangé. Les divisions par $\sqrt n$ choisissent des erreurs quadratiques moyennes par bloc : elles modifient la pondération relative par rapport à une somme de normes brutes. Les échelles et poids doivent être justifiés et fixés avant l'ajustement ; choisir une autre normalisation ou minimiser des normes **au carré** définit en général un autre objectif. L'inverse des incertitudes peut être envisagé si elles sont disponibles et leur structure prise en compte, sans en déduire automatiquement un modèle statistique pour cette somme de normes.
3. Le solveur, l'initialisation ou la graine, les limites, les critères d'arrêt et un contrôle de sensibilité aux choix d'échelle et aux initialisations. Prévoir des observations ou scénarios de test indépendants ; un accord avec le modèle gaussien servant de cible reste un calage intermodèles.

Les valeurs historiques des échelles, poids, données, paramètres et critères d'arrêt restent à retrouver : cette proposition ne les remplace pas implicitement. L'annexe E décrit un calage à un modèle gaussien en vent uniforme et terrain plat, sans permettre à elle seule de fixer toutes ces conventions dans les pages examinées.

## Sensibilité et localisation d'une source

La page 132 définit la région des sources possibles par un $J'_p$ élevé. Une grande dérivée indique une variation locale de l'objectif ; elle ne suffit pas à établir une bonne correspondance aux observations ni l'unicité de la source. Par exemple, pour une position synthétique sans dimension $p\in[0,1]$, une observation $c_{obs}=0$ et une prédiction $c(p)=c_*p$ avec $c_*>0$, l'objectif normalisé $J(p)=|c(p)-c_{obs}|/c_*=|p|$ a $J'(p)=1$ pour tout $p\in(0,1)$, tandis que l'écart augmente avec $p$ et est minimal en $p=0$. En prolongeant cet objectif à une droite autour de zéro, il n'y est pas différentiable. Cet exemple ne reproduit pas l'algorithme historique ; il montre la limite logique du seul critère de sensibilité.

Pour une identification exploitable, associer à la carte de sensibilité les écarts aux observations, les sources admissibles, la résolution spatiale et les incertitudes ; rechercher les solutions concurrentes et tester leur séparation avec les mesures disponibles. Une région sensible peut être utile au diagnostic sans constituer une preuve de localisation unique.
