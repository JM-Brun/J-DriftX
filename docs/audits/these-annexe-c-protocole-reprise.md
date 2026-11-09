# Annexe C — décision de reproductibilité et protocole de reprise

**Verdict : la reprise fidèle du programme historique n'est pas déterminable avec les éléments consultés.** Les équations imprimées fixent certaines composantes, mais pas une exécution unique : les indices de (C.20)–(C.21), la sortie du pseudo-code, la relation entre viscosités et le pas de temps demandent des conventions supplémentaires. Le fac-similé des pp. imprimées 159–160 (PDF 168–169) a été revérifié ; (C.23), p. 161 (PDF 170), est analysée dans la [fiche source](../bibliographie/sources/these-brun.md) et DRX-ERR-047. Ce verdict ne prouve pas que le programme ancien avait ces incohérences. L'[audit de l'annexe C](these-annexe-c-integration-temporelle.md) conserve les transcriptions et contre-exemples conditionnels.

Le protocole ci-dessous définit **une reconstruction candidate**, choisie pour rendre les questions testables. Ce n'est ni une correction établie de la thèse ni un solveur historique retrouvé. Il clôt la définition documentaire de TH-05 ; l'identification du code ancien et toute validation physique restent distinctes.

## Contrat explicite de la candidate

Sur une grille périodique $j=0,\ldots,N-1$, de pas $h=L/N$, avec indices modulo $N$, posons le flux physique $f(u)=u^2/2$ et

$$
F_{j+1/2}=\frac{f(u_j)+f(u_{j+1})}{2}
-\frac{a_{j+1/2}}{2}(u_{j+1}-u_j),\qquad
a_{j+1/2}=\max(|u_j|,|u_{j+1}|),
$$
$$
L_j(u)=-\frac{F_{j+1/2}-F_{j-1/2}}{h}
+\nu\frac{u_{j+1}-2u_j+u_{j-1}}{h^2}+g_j(u),\qquad \nu\ge0.
$$

Le flux conservatif à dissipation de type Rusanov est un **choix nouveau** ; il ne reproduit pas littéralement le produit centré non conservatif de (C.20). La viscosité $\nu$ est physique et ajoutée explicitement ; la dissipation du flux est numérique. Il ne faut pas lui ajouter silencieusement la viscosité (C.22) : ce serait un troisième choix à justifier. La périodicité et $N\ge3$ sont des conditions de cet exemple, pas celles de la canopée historique.

Pour un pas fixé $\Delta t>0$, la candidate réutilise l'état de début de pas à chaque étape :

$$
w^0=u^n,\quad
w^1=u^n+\frac{\Delta t}{3}L(w^0),\quad
w^2=u^n+\frac{\Delta t}{2}L(w^1),\quad
w^3=u^n+\Delta t\,L(w^2),\quad
u^{n+1}=w^3.
$$

Les dénominateurs 3, 2, 1 sont choisis pour cette candidate et non attribués aux dénominateurs imprimés 4, 3, 2 de (C.20). L'opérateur, y compris $g$, est réévalué à chaque étape ; le pas ne change pas à l'intérieur d'un pas. Si $g=0$, la somme discrète de $L$ est nulle par télescopage périodique, donc chaque étape préserve la somme de $u$ à l'arrondi près. Avec $g\ne0$, il faut inclure sa contribution : la conservation de cette somme n'est pas garantie.

## Cohérence et ordre : deux équations nécessaires

À $T=0{,}5$, partons de $u(0)=1$ et répétons la candidate avec $\Delta t=T/N_t$. La solution de $u'=u$ vaut $e^{0,5}$ ; celle de $u'=u^2$ vaut $2$ à cet instant. Les erreurs absolues calculées sont :

| $N_t$ | $u'=u$ | $u'=u^2$ |
|---:|---:|---:|
| 10 | $4{,}1253\times10^{-6}$ | $1{,}0216\times10^{-3}$ |
| 20 | $5{,}2607\times10^{-7}$ | $2{,}3434\times10^{-4}$ |
| 40 | $6{,}6419\times10^{-8}$ | $5{,}5496\times10^{-5}$ |
| 80 | $8{,}3440\times10^{-9}$ | $1{,}3458\times10^{-5}$ |

Sur la séquence fine, un raffinement par 2 divise l'erreur linéaire par environ 8 mais l'erreur non linéaire par environ 4. En effet, le polynôme linéaire est $1+z+z^2/2+z^3/6$ ; il ne suffit pas à prouver l'ordre 3 non linéaire. Pour $u'=u^2$, le terme local en $\Delta t^3$ vaut $11/12$ au lieu de $1$. La candidate est cohérente et d'ordre 2 pour une équation autonome suffisamment régulière ; elle ne satisfait pas l'ordre 3 non linéaire annoncé dans le texte général. Cela ne préjuge pas du code historique.

Contrôle reproductible en Python :

```python
from math import exp


def step(u, dt, f):
    w1 = u + dt * f(u) / 3
    w2 = u + dt * f(w1) / 2
    return u + dt * f(w2)


for n in (10, 20, 40, 80):
    dt = 0.5 / n
    linear = nonlinear = 1.0
    for _ in range(n):
        linear = step(linear, dt, lambda x: x)
        nonlinear = step(nonlinear, dt, lambda x: x * x)
    print(n, abs(linear - exp(0.5)), abs(nonlinear - 2))
```

Avant d'interpréter un calcul complet, ajouter pour le problème choisi des contrôles à pas raffinés à espace fixé, puis à espace raffiné avec pas temporel contrôlé ; les erreurs spatiale et temporelle ne doivent pas être confondues. Pour des solutions non lisses, les ordres et les normes doivent être réévalués selon le problème.

## Stabilité : un résultat borné, pas une garantie générale

Linéarisons l'opérateur périodique choisi autour d'un état constant $U>0$, avec $g=0$ et $\nu$ constante. La dissipation du flux produit le décentrement amont et

$$
L_hq_j=-U\frac{q_j-q_{j-1}}{h}
+\nu\frac{q_{j+1}-2q_j+q_{j-1}}{h^2}.
$$

Soient $C=U\Delta t/h$, $r=\nu\Delta t/h^2$ et $P=I+\Delta t L_h$. Si $C+2r\le1$, $P$ est une moyenne convexe des valeurs aux indices $j-1,j,j+1$. Le pas multi-étapes linéarisé vérifie alors

$$
R(\Delta tL_h)=\frac13I+\frac12P+\frac16P^3,
\qquad R(z)=1+z+\frac{z^2}{2}+\frac{z^3}{6}.
$$

Sur cette grille périodique, cette combinaison préserve la somme et les constantes, conserve la non-négativité de $q$ et est contractante en $\ell^\infty$. La condition est **suffisante**, pas présentée comme nécessaire. Pour $N=100$, $h=0{,}01$, $U=1$, $\nu=0{,}005$, $\Delta t=0{,}004$ et $q_j=1+0{,}2\sin(2\pi j/N)$, on obtient $C+2r=0{,}8$, une variation de moyenne nulle à la précision affichée et $q^{n+1}\in[0{,}800378,1{,}199622]\subset[0{,}8,1{,}2]$.

Ce résultat concerne l'opérateur **linéarisé**, les frontières périodiques, le pas fixé et l'absence de source. Il ne démontre pas la positivité, la stabilité ni l'ordre de la candidate pour Burgers non linéaire avec des frontières ou sources quelconques. La règle (C.23) ne s'y substitue pas : sa dimension et son dénominateur nul restent à élucider selon DRX-ERR-047. Pour un problème non linéaire donné, spécifier et tester séparément la borne de pas, les flux de frontière et l'effet du terme source.

## Décision et suite

La transcription et le protocole permettent de distinguer **recherche historique**, **reconstruction numérique** et **évaluation physique**. TH-05 est close pour ce livrable : le code de canopée, ses paramètres, la convention de pas et les observations restent à retrouver au titre de TH-07 et TH-08. Une implémentation future doit annoncer ses propres choix de flux, viscosité, frontières et pas ; les résultats ci-dessus ne constituent pas une preuve sur le programme ancien.
