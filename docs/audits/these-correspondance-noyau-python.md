# Thèse de Brun — premières correspondances avec le noyau Python

**Portée.** Ce relevé lie des passages vérifiés de la thèse à des capacités précises du noyau actuel, à la révision `a0545330d1a7f52aa3a0768890233f486a9c29fa`. Il ne revendique ni reproduction du code ancien ni validation physique. Les autres capacités restent à examiner dans TH-06 de la [liste de reprise](these-travaux-restants.md).

## Équation transverse de l'annexe B

La thèse, p. imprimée 154 (PDF 163), écrit (B.46) sous la forme $U\partial_x c=K\partial_{zz}c$ avec $U>0$ et identifie $t=x/U$. Elle considère une diffusion transverse, une source linéique de longueur $H$ et aucune frontière solide. P. 156 (PDF 165), (B.55) donne $\int_{\mathbb R}c\,dz=Q/(UH)$. Ces pages ont été contrôlées sur le fac-similé ; les incohérences imprimées de normalisation ultérieures sont analysées dans la [fiche source](../bibliographie/sources/these-brun.md).

La fonction Python [`gaussian_advection_diffusion`](../../src/jdriftx/advection_diffusion.py) résout sur $\mathbb R$ une advection–diffusion 1D à coefficients constants et largeur gaussienne initiale strictement positive. Pour une **reconstruction choisie**, poser

$$
t=x/U,\quad \texttt{velocity}=0,\quad \texttt{diffusivity}=K,\quad
\texttt{mass}=Q/(UH),\quad \texttt{initial\_sigma}=\sigma_0>0.
$$

L'argument spatial de la fonction représente alors $z$, la diffusion est transverse et la solution vérifie (B.46) pour $x\ge0$. La valeur `mass` est ici l'**intégrale linéique de la concentration**, d'unité kg/m² : elle ne représente pas une masse totale en kg. Avec $[c]=$ kg/m³, $[Q]=$ kg/s, $[U]=$ m/s et $[H]=$ m, l'intégrale reproduit la normalisation (B.55). Le paramètre $H$ est une longueur de source, pas une hauteur de rejet. À $x=0$, la reconstruction impose un profil gaussien de largeur $\sigma_0$ ; elle n'est donc pas une source transverse ponctuelle de largeur initiale nulle, que l'API refuse. Elle n'impose ni sol réfléchissant, ni dépôt, ni géométrie de couvert.

### Contrôle reproductible

Exécuter depuis la racine du dépôt avec les dépendances Python du projet :

```python
import numpy as np
from jdriftx.advection_diffusion import gaussian_advection_diffusion

U, K, Q, H, sigma0 = 3.0, 0.4, 2.0, 4.0, 0.5  # unités SI
x, z, h = 15.0, 0.7, 0.001  # m
mass = Q / (U * H)  # kg/m², intégrale transverse


def c(x, z):
    return gaussian_advection_diffusion(
        np.asarray(z),
        x / U,
        mass=mass,
        velocity=0.0,
        diffusivity=K,
        initial_sigma=sigma0,
    )


sigma = np.sqrt(sigma0**2 + 2 * K * x / U)
grid = np.linspace(-12 * sigma, 12 * sigma, 120001)
integral = np.trapezoid(c(x, grid), grid)
cx = (c(x + h, z) - c(x - h, z)) / (2 * h)
czz = (c(x, z + h) - 2 * c(x, z) + c(x, z - h)) / h**2
residual = U * cx - K * czz
print(integral, mass, residual)
assert abs(integral - mass) < 1e-12
assert abs(residual) < 1e-7
```

Exécution observée : intégrale $0{,}166666666666667$ kg/m² pour $Q/(UH)=1/6$ kg/m² et résidu par différences finies $-1{,}34\times10^{-10}$ kg·m⁻³·s⁻¹ au point indiqué. L'intégration est limitée à $\pm12\sigma$ et le résidu dépend du pas et des arrondis : ces contrôles illustrent la correspondance, ils ne remplacent pas la dérivation ou un test de terrain. Les [tests du noyau](../../tests/test_advection_diffusion.py) vérifient notamment translation, intégrale sur un domaine couvrant les queues et évolution de variance ; ils ne testent pas explicitement toute l'interface source–transport historique.

## Panache stationnaire avec réflexion au sol

Le chapitre 1, p. imprimée 31 (PDF 40), définit sous l'approximation de panache mince un **débit massique** sur une section transverse. La fonction [`concentration_panache`](../../src/jdriftx/similitude.py) évalue une référence gaussienne stationnaire avec $x>0$, un vent uniforme $U>0$, un débit $Q\ge0$, une hauteur de source $h\ge0$, les largeurs $\sigma_y(x),\sigma_z(x)>0$ et une image de même signe sous le sol. Pour $z\ge0$, sa forme mathématique est

$$
c=\frac{Q}{2\pi U\sigma_y\sigma_z}e^{-y^2/(2\sigma_y^2)}
\left[e^{-(z-h)^2/(2\sigma_z^2)}+e^{-(z+h)^2/(2\sigma_z^2)}\right].
$$

L'image impose $\partial_zc=0$ à $z=0$. Avec une diffusivité verticale finie et sans vitesse verticale au sol, le flux vertical y est nul : c'est une frontière réfléchissante, **pas un dépôt absorbant**. Pour les sections complètes et les hypothèses de la formule,

$$
\int_{-\infty}^{\infty}\!\int_0^\infty Uc\,dz\,dy=Q.
$$

Il s'agit d'un débit en kg/s et non d'une masse contenue dans le domaine. L'intégration de la formule prolongée à $z<0$ sur tout $\mathbb R^2$ donne $2Q$ : ce prolongement est l'artifice mathématique de l'image, pas une seconde émission physique. La fonction accepte des coordonnées verticales négatives finies ; l'utilisateur doit donc appliquer lui-même le domaine physique $z\ge0$ lorsqu'il interprète ce cas. Elle ne calcule pas non plus le jet ni les pertes traversant un plan dans le couvert.

**Contrôle numérique ciblé.** Pour $Q=2$ kg/s, $U=4$ m/s, $h=30$ m, $x=1000$ m et la classe D, les fonctions Python renvoient $\sigma_y\simeq76{,}277$ m et $\sigma_z\simeq37{,}947$ m. Une quadrature trapézoïdale sur $y\in[-8\sigma_y,8\sigma_y]$ et $z\in[0,h+8\sigma_z]$, avec 801 points par axe, donne $1{,}999999999999995$ kg/s. Utiliser au contraire $z\in[-h-8\sigma_z,h+8\sigma_z]$ avec 1601 points donne $3{,}999999999999990$ kg/s. Ces fenêtres finies illustrent la normalisation ; elles ne valent pas preuve d'une conservation en présence de dépôt ou dans un champ variable.

Le [test de section avec source en hauteur](../../tests/test_similitude.py) utilise une fenêtre et une tolérance finies ; [docs/51](../51-reference-independante-cas-s0.md) examine aussi une route EDP à coefficients transverses liés aux mêmes largeurs. Leur accord teste cette reconstruction et sa discrétisation : les deux routes partagent des paramètres et une entrée, et aucune ne constitue une mesure indépendante. Le code de panache accepte un débit nul alors que [`SourcePanache`](../../src/jdriftx/source.py) exige un débit strictement positif ; cette différence de contrat doit être prise en compte par l'appelant.

## Autres objets examinés

| Passage historique | Noyau et contrôle associés | Écart et limite |
|---|---|---|
| Chapitre 7, (7.6)–(7.7) : temps jusqu'à une projection sur une caractéristique | [`pseudo_distance_uniforme`](../../src/jdriftx/metric.py) ; [tests de métrique](../../tests/test_metric.py) | Référence en vent constant 2D, temps longitudinal en secondes si les entrées sont en mètres et m/s. Le décalage transverse n'est pas pénalisé ; le cas amont utilise la convention locale $+\infty$. Cette fonction ne construit pas la projection historique en champ variable. |
| Temps de migration le long d'une trajectoire | [`temps_transport`](../../src/jdriftx/metric.py) ; [tests de métrique](../../tests/test_metric.py) | Additionne longueur de chaque segment divisée par la norme de son vent. Le résultat ne tient pas compte de l'orientation du vent et peut rester fini pour un chemin à contre-vent ; ce coût n'établit pas que la polyligne est une caractéristique. |
| Chapitre 5, source locale normalisée et flux au-dessus du couvert | [`SourcePanache`](../../src/jdriftx/source.py) ; [tests de source](../../tests/test_source.py) | Valeur immuable de panache gaussien : débit en kg/s, vitesse en m/s, classe A–F et hauteur en m, avec contrôles d'entrée. Cet objet ne calcule pas les jets, le stockage local, le dépôt ou le flux au plan des équations (5.50)–(5.67). |
| Chapitre 4 et annexe C : Burgers de canopée, traînée et schéma historique | Aucun solveur historique correspondant n'a été identifié dans les fonctions du noyau examinées pour cette note. | Une recherche de noms n'établit pas l'absence de toute capacité ailleurs. Le schéma et ses indices restent sous-spécifiés ; voir [l'audit de l'annexe C](these-annexe-c-integration-temporelle.md). |

Les tests ciblés `test_advection_diffusion.py`, `test_metric.py`, `test_source.py` et `test_shear_projected_cost.py` ont donné **134 succès** sur la révision indiquée. Les tests de cisaillement portent sur un contre-exemple analytique, pas sur un solveur général de projection historique. TH-06 reste ouverte pour les autres fonctions, leurs unités, conditions d'entrée et limitations.
