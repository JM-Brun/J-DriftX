# Thèse de J.-M. Brun

> **Rôle et portée :** fiche de lecture de la source primaire, actualisée le 8 novembre 2026. La consultation est ciblée, non intégrale. Les résultats historiques ne valident pas J-DriftX ; l'audit de conservation est développé dans [docs/43](../../43-audit-these-brun-conservation-g0s.md).

## Identification et accès

Brun, Jean-Marc, *Modèles à complexité réduite de transport pour applications environnementales*, thèse de doctorat en mathématiques appliquées, Université Montpellier II, soutenue le **21 septembre 2007**. Ces éléments ont été vérifiés visuellement sur la page de titre, page 2 du [PDF versionné](../../../raw/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf). Sa première page porte l'identifiant HAL `tel-02589999` et une date de dépôt en 2020 : le dépôt et la soutenance sont deux événements distincts. L'article de Mohammadi et Brun (2006) citait la thèse sous le titre *Modélisation à complexité réduite de la dérive* ; cette variante reste une citation historique, pas le titre imprimé sur la page examinée.

Le fichier comprend 204 pages PDF ; sa provenance et son empreinte sont consignées dans le [sidecar](../../../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md). La présence d'un bandeau HAL ne prouve pas l'identité binaire avec le fichier actuellement hébergé par HAL ; les droits de redistribution restent distincts et non établis. Ne pas relancer l'acquisition.

## Carte de lecture, d'après la table des matières

Les pages ci-dessous sont les pages imprimées ; pour les passages vérifiés dans le corps de ce fichier, la page PDF est la page imprimée + 9. Cet écart ne doit pas être généralisé sans contrôle aux pages liminaires et aux annexes.

| Partie | Pages imprimées | Premier passage et portée |
|---|---:|---|
| 1 — Transport et dispersion | 11–31 | Bilans, fermeture turbulente, solutions gaussiennes et limites ; passages ciblés §§1.2–1.6. |
| 2 — Météorologie | 35–42 | Couche limite, stabilité et profil vertical du vent ; §§2.1–2.5 repérés. |
| 3 — Écoulement dans le couvert | 49–61 | Traînée, densité foliaire et moyennes spatiales ; §§3.1–3.2 repérés. |
| 4 — Modèle de canopée | 63–77 | Équations, problèmes inverses et résultats idéalisés ; §§4.1–4.4 examinés en lecture ciblée. |
| 5 — Pulvérisateur et jet | 85–109 | Similitude du jet, source et essais ; §§5.3–5.9 ciblés, dont pp. 103–109 examinées visuellement. |
| 6 — Modélisation atmosphérique | 115–124 | Entrées, limites des familles de modèles et échelles ; §§6.1–6.4 repérés. Les temps de calcul du tableau 6.1 sont historiques, pas un benchmark actuel. |
| 7 — Transport lointain | 125–138 | Géométrie, champ, panache, inverse et résultats ; pp. 126–137 contrôlées sur le PDF. Les figures 7.7–7.10 suivent la conclusion du chapitre. |
| Conclusion et perspectives | 141–145 | Limites de validation, besoins de données et couplages futurs ; passages ciblés pp. 141–145. |
| A — Réduction de modèle | 149–150 | Distinction entre base de snapshots et réduction construite avec information physique ; lecture ciblée. |
| B — Panache gaussien | 151–158 | Diffusion impulsionnelle, similitude stationnaire et transformées ; équations ciblées contrôlées sur le PDF. |
| C — Schéma Burgers | 159–161 | Discrétisation, intégration en temps et critère CFL ; contrôle visuel ciblé ci-dessous. |
| D — Modèles et échelles | 163–168 | Tableau comparatif, fréquences atmosphériques et stabilité ; lecture ciblée, y compris inspection visuelle du tableau D.1 en page paysage. |
| E — Calage de dispersion | 169–172 | Calage à un modèle gaussien et interface ; pp. 169–171 examinées visuellement, p. 172 repérée. |
| F — Distance | 173–175 | Distances sur courbes et coût directionnel du vent ; (F.10) contrôlée sur le PDF. |

Cette carte couvre **tous les chapitres et annexes par repérage ciblé**, sans prétendre à une vérification ligne par ligne de leurs démonstrations ou figures. L'extraction textuelle du PDF a servi au repérage ; les formules faisant l'objet d'un verdict ont été vérifiées visuellement.

Les prochaines lectures, les travaux conditionnés à des sources externes et leurs critères de clôture sont regroupés dans la [liste des travaux restants](../../audits/these-travaux-restants.md).

## Lecture transversale des chapitres 1 à 6

| Chapitre | Apport documenté | Limite pour J-DriftX |
|---|---|---|
| **1 — Transport** | Les §§1.2–1.4 introduisent bilan, moyenne turbulente et fermeture ; le §1.5 distingue profils gaussiens et approximation de panache mince. P. 31 (PDF 40), le flux de section est relié à la conservation sous les hypothèses retenues. | Les fermetures et l'approximation de diffusion longitudinale négligeable sont des hypothèses. Le noyau à masse $M$ des pp. 29–30 n'est pas automatiquement une solution stationnaire à débit $Q$ ; voir l'audit de l'annexe B ci-dessous. |
| **2 — Météorologie** | Les pp. 38–42 (PDF 47–51) relient stabilité, turbulence, rugosité et profils verticaux ; la loi logarithmique de (2.4) est présentée pour des conditions neutres. | Un vent uniforme et une classe de stabilité ne représentent ni les variations temporelles et verticales réelles ni toutes les situations de terrain complexe. Les valeurs indicatives du texte sont historiques et ne sont pas des règles universelles. |
| **3 — Couvert** | Les pp. 51–52 distinguent densité de surface foliaire par volume, d'unité m⁻¹, et indice intégré sans dimension. Les pp. 57–58 décrivent des moyennes spatiales dont les dérivées ne commutent pas toujours en présence d'interfaces. | Une densité moyenne ne détermine pas à elle seule la structure, l'orientation des feuilles ou les flux d'interface. L'identification des fermetures nécessite géométrie et observations. |
| **4 — Vitesse dans la canopée** | Les équations (4.8) et (4.9), pp. 66–67 (PDF 75–76), posent respectivement une équation de Burgers visqueuse forcée pour la vitesse 1D et une équation de transport pour le scalaire. Le §4.3 calibre une traînée et discute des objectifs moyens ou de pire cas. | C'est un **lien historique direct avec Burgers**, mais au niveau du vent local dans le couvert, non une équation de concentration ni une preuve pour le panache lointain. La conclusion, pp. 76–77, qualifie les applications d'idéalisées et indique que le transport du scalaire n'y est pas discuté en détail. |
| **5 — Jet et source** | Le §5.5 pose une forme de similitude ; les pp. 99–101 introduisent une décroissance axiale distincte dans le couvert et un profil radial gaussien. Les pp. 103–109 décrivent les essais discutés ci-dessous. | Le maintien du profil radial dans la végétation est explicitement une hypothèse forte. Une source simplifiée n'établit pas la performance du couplage lointain. |
| **6 — Dispersion atmosphérique** | Les pp. 116–124 recensent entrées, hypothèses, familles gaussienne/eulérienne/lagrangienne, échelles et compromis de modèles. Le texte souligne la nécessité de données et de contrôles qualité. | Cette synthèse reflète les connaissances et temps de calcul rapportés dans la thèse, pas un état de l'art 2026 ni une comparaison moderne mesurée. |

**Profil de vent neutre.** L'[audit de (2.4)](../../audits/these-profil-vent-neutre.md) distingue la hauteur de déplacement et la longueur de rugosité : le zéro extrapolé dans la coordonnée $z$ est $d+z_0$ lorsque $u_*>0$. Un exemple montre aussi que deux vitesses ne déterminent pas les trois paramètres $d,z_0,u_*$ libres. Ce contrôle n'établit pas que la loi soit applicable dans le couvert ou à une campagne particulière.

**Conséquence pour la reprise.** La thèse combine plusieurs niveaux : une EDP 1D pour le couvert, une modélisation de source proche et une représentation réduite du transport lointain. La promesse d'évaluation ponctuelle sans résolution complète d'EDP doit être rattachée au niveau et aux préparations concernés ; elle ne décrit pas uniformément toute la chaîne historique.

**Identifiabilité de la traînée locale.** La p. 70 (PDF 79), équation (4.19), utilise $F_u=-\tfrac12 C_Da_{LAD}u|u|$ et précise que le contrôle dépend du seul produit $C_Da_{LAD}$. Si tous les autres éléments du modèle et les conditions sont identiques, les couples $(C_D,a_{LAD})=(0{,}2,4\,\mathrm{m^{-1}})$ et $(0{,}4,2\,\mathrm{m^{-1}})$ fournissent le même terme de traînée. Des observations de vitesse ne peuvent donc identifier séparément ces deux paramètres **dans ce modèle réduit et avec cette seule dépendance** ; il faut une mesure ou une contrainte supplémentaire. Cette non-identifiabilité structurelle ne présume pas la qualité des données réelles.

## Chapitre 4 : cibles inverses et cas de contrôle analytique

**Périmètre.** Les équations (4.8), (4.14)–(4.19), pp. 66–70 (PDF 75–79), et la conclusion pp. 76–77 (PDF 85–86) ont été examinées sur le fichier versionné. Le cas analytique ci-dessous est une déduction sous hypothèses supplémentaires ; il n'est ni une reproduction du solveur historique ni une validation sur mesures.

### Domaine du profil cible et données aux limites

Pour $L=r_1-r_0>0$, $u_l>0$ et $u_r=\beta u_l$, l'équation (4.17) imprime le profil cible

$$
u_{\rm tar}(r)=u_l\exp\!\left[-\log\!\left(\frac{u_l}{u_r}\right)\frac{r-r_0}{L}\right]
=u_l\beta^{(r-r_0)/L}.
$$

La page 69 (PDF 78) autorise $\beta\in[0,1]$, mais pour $\beta=0$ et $u_l>0$ le logarithme de (4.17) n'est pas défini. La limite $\beta\downarrow0$ vaut $u_l$ en $r_0$ et zéro en tout point $r>r_0$ : elle est discontinue à l'entrée. Un profil continu de cette famille exige donc $0<\beta\le1$ ; la valeur zéro demande une convention ou un autre modèle. Les quatre exemples de la figure 4.2 utilisent des rapports positifs et ne sont pas eux-mêmes au bord problématique. Voir [DRX-ERR-043](../../46-registre-erreurs-incoherences-documentaires.md).

En (4.8), p. 66 (PDF 75), la source impose $u(r,0)=0$ sur $[r_0,r_1]$ et $u(r_0,t)=u_l$ sur $[0,T]$. Pour $u_l\ne0$, ces deux valeurs se contredisent au point $(r_0,0)$ ; les exemples de la figure 4.2 prennent $u_l=10$ m/s. Il faut soit modifier la convention au coin, soit admettre et traiter une incompatibilité initiale dans un cadre de solution approprié. En outre, pour $\nu>0$, ce passage ne donne pas de condition à la frontière aval $r_1$ : le problème visqueux n'est pas complètement spécifié **par ce seul passage**. Cela n'exclut pas qu'un code ou une autre convention historique l'ait complété. Voir [DRX-ERR-044](../../46-registre-erreurs-incoherences-documentaires.md).

### Référence reconstruite : Burgers stationnaire sans viscosité

Posons $k=C_Da_{LAD}\ge0$, constant, et ajoutons aux équations historiques les hypothèses **stationnaire**, **$\nu=0$** et **$u>0$** sur le rang. Les équations (4.8) et (4.19) impliquent alors

$$
u\frac{du}{dr}=-\frac{k}{2}u^2,\qquad
u(r)=u_l e^{-k(r-r_0)/2},\qquad
\frac{u(r_1)}{u_l}=e^{-kL/2}.
$$

Pour reproduire la cible (4.17) avec $0<\beta\le1$, cette reconstruction exige $k=-2\log\beta/L$. La p. 70 donne $0\le k\le6\,\mathrm{m^{-1}}$ : pour $L=1$ m, les rapports accessibles dans ce modèle particulier sont $e^{-3}\le\beta\le1$. Les quatre exemples $\beta=0{,}4,0{,}3,0{,}2,0{,}1$ correspondraient respectivement à $k\simeq1{,}833,2{,}408,3{,}219,4{,}605\,\mathrm{m^{-1}}$. Ces valeurs sont des **prédictions du cas reconstruit**, pas des paramètres extraits des figures ni les résultats du problème visqueux transitoire.

La loi semi-empirique (3.46), p. 61 (PDF 70), écrit une décroissance en $e^{-C_Da_{LAD}r}$ : si l'on donne la même valeur numérique au produit dans les deux expressions, son exposant diffère d'un facteur 2 de celui du cas simplifié issu de (4.19). Les deux textes peuvent employer des conventions de traînée différentes ; ce contrôle ne suffit pas à attribuer une erreur au calcul historique. Toute comparaison doit préciser ces conventions et le rôle de la viscosité.

### Contrôle par morceaux : identification et sensibilité

La p. 71 (PDF 80), équations (4.20)–(4.24), décrit un produit de traînée constant par couche et un problème inverse pour les profils cibles. Pour étudier ce que les données peuvent identifier, considérons une **reconstruction distincte**, stationnaire, sans viscosité, avec $u>0$ et des interfaces $x_0<\cdots<x_m$, $h_i=x_{i+1}-x_i>0$. Sur la couche $i$, posons $k(r)=k_i\ge0$, pour $i=0,\ldots,m-1$. Les équations (4.8) et (4.19) donnent presque partout $u'=-ku/2$ ; avec une vitesse continue aux interfaces,

$$
u(r)=u_l\exp\!\left[-\frac12\int_{x_0}^{r} k(s)\,ds\right],\qquad
\frac{u(x_m)}{u_l}=\exp\!\left[-\frac12\sum_{i=0}^{m-1}k_i h_i\right].
$$

**Une sortie ne détermine pas chaque couche.** Pour deux couches de 0,5 m et $u_l=10$ m/s, les contrôles $(1,3)$ et $(2,2)$ m⁻¹ ont la même intégrale et donnent tous deux $u(x_m)=10e^{-1}\simeq3{,}679$ m/s. Leurs vitesses à l'interface sont pourtant respectivement $10e^{-1/4}\simeq7{,}788$ et $10e^{-1/2}\simeq6{,}065$ m/s. Une mesure de sortie et une mesure d'entrée, même exactes, identifient ici une intégrale de traînée et non les deux valeurs séparées. Ce constat porte sur ce cas analytique, pas sur l'identifiabilité du solveur visqueux historique ni sur toutes les données qui auraient pu être utilisées.

**Des mesures aux interfaces changent le problème.** Si toutes les vitesses aux interfaces $u_i=u(x_i)>0$ sont connues exactement, les contrôles de cette reconstruction sont uniques et valent

$$
k_i=-\frac{2}{h_i}\log\!\left(\frac{u_{i+1}}{u_i}\right).
$$

Une donnée croissante entre deux interfaces conduirait à $k_i<0$ : elle ne serait pas compatible exactement avec ce modèle à traînée non négative, sans pour autant invalider la mesure ou un modèle physique plus riche. Si les mesures vérifient $\log u_i^{obs}=\log u_i+\epsilon_i$, alors l'erreur du contrôle obtenu par différences vaut $\Delta k_i=2(\epsilon_i-\epsilon_{i+1})/h_i$. Pour des erreurs indépendantes, centrées et de même variance $\sigma^2$, $\operatorname{sd}(\Delta k_i)=2\sqrt2\,\sigma/h_i$ et deux erreurs voisines ont une covariance $-4\sigma^2/(h_i h_{i+1})$.

À titre synthétique, pour $L=1$ m, des couches égales et $\sigma=0{,}01$ en échelle logarithmique, cet écart-type vaut environ 0,113 m⁻¹ pour 4 couches et 0,566 m⁻¹ pour 20 couches. Il ne s'agit ni d'incertitudes mesurées sur la figure 4.3, ni d'une analyse du modèle visqueux. Le résultat montre le compromis : multiplier les couches accroît la liberté du contrôle, mais la reconstruction directe par différenciation amplifie le bruit si sa variance aux points ne diminue pas.

**Conventions à fixer avant reproduction.** Le texte écrit l'espace admissible $\mathbb R^m$, alors que la p. 70 borne les valeurs physiquement pertinentes à $0\le k\le6$ m⁻¹. $\mathbb R^m$ peut être lu comme espace ambiant et $[0,6]^m$ comme sous-ensemble physique, mais l'optimisation réellement contrainte n'est pas explicitée par ces lignes : une valeur négative serait autorisée par le premier ensemble et interdite par le second. De plus, (4.20) somme les indicatrices $[r_k,r_{k+1}[$ pour $k=1,\ldots,m$ après avoir appelé $[r_0,r_1]$ le domaine entier. Il faut préciser si ces indices désignent deux systèmes de noms différents : utilisés littéralement comme une seule liste ordonnée, ils ne couvrent pas le domaine annoncé. Le dernier intervalle ouvert à droite ne définit pas non plus le coefficient à son extrémité ; ce point seul est sans effet sur une formulation intégrale à égalité presque partout, mais une discrétisation nodale doit fixer sa convention. Ces ambiguïtés documentaires sont suivies sous [DRX-ERR-051](../../46-registre-erreurs-incoherences-documentaires.md) et [DRX-ERR-052](../../46-registre-erreurs-incoherences-documentaires.md), sans présumer le code historique.

### Cible exponentielle : condition exacte avec viscosité

Les équations (4.8), (4.17)–(4.19), pp. 66–70 (PDF 75–79), ont été contrôlées visuellement. Pour isoler le rôle de la viscosité, considérons une **reconstruction stationnaire** avec $u_l>0$, $L=r_1-r_0>0$, $0<\beta<1$, $\nu\ge0$ constant et un contrôle spatial $k(r)=C_Da_{LAD}$. Posons $q=-\log(\beta)/L>0$ et imposons le profil cible $u(r)=u_l e^{-q(r-r_0)}$. La substitution dans les équations d'état et de traînée donne, pour tout point où $u>0$,

$$
u u'-\nu u''=-\frac{k(r)}2u^2,
\qquad
k_{\rm requis}(r)=2q+\frac{2\nu q^2}{u(r)}
=2q+\frac{2\nu q^2}{u_l}e^{q(r-r_0)}.
$$

Les deux termes de $k_{\rm requis}$ sont en m⁻¹. Pour $\nu=0$, on retrouve le contrôle constant $2q$ du cas précédent. Pour $\nu>0$ et $0<\beta<1$, le contrôle exact est croissant en $r$ : **un seul coefficient constant ne peut pas reproduire exactement ce profil stationnaire** dans ce modèle. Des coefficients constants par morceaux ne le représentent pas non plus exactement avec un nombre fini de morceaux ; ils peuvent toutefois l'approcher. Le cas $\beta=1$ est différent : $q=0$ et $k=0$ convient à cette reconstruction.

La borne historique $0\le k\le6$ m⁻¹ impose en particulier

$$
2q+\frac{2\nu q^2}{\beta u_l}\le6\ \mathrm{m^{-1}}.
$$

À titre **synthétique**, prenons $L=1$ m, $u_l=10$ m/s, $\beta=0{,}1$ et $\nu=0{,}2$ m²/s. Alors $q\simeq2{,}303$ m⁻¹, $k_{\rm requis}(r_0)\simeq4{,}817$ m⁻¹ et $k_{\rm requis}(r_1)\simeq6{,}726$ m⁻¹. Cette cible stationnaire exacte viole donc la borne 6 dans cet exemple ; à ces mêmes $L,u_l,\beta$, elle la respecte seulement si $\nu\lesssim0{,}1315$ m²/s. La viscosité choisie est illustrative : elle n'est ni extraite de la figure 4.3 ni proposée comme valeur physique pour l'essai historique. Même si la borne est satisfaite, il faut encore définir les conditions aux limites et initiales. La reconstruction stationnaire ne reproduit pas le démarrage à vitesse nulle de (4.8) et ne permet pas de conclure sur l'atteignabilité de la cible à un instant d'un calcul transitoire.

### Existence d'un minimum inverse nul

Après (4.10)–(4.12), p. 67 (PDF 76), la thèse affirme qu'un contrôle $F_{\rm tar}$ fournit un minimum global nul, alors que l'espace admissible est encore à déterminer. Cette affirmation est vraie **si** un tel contrôle admissible existe et produit effectivement la cible dans la norme choisie. Ces deux propriétés ne découlent pas de la seule définition $J(F)=\lVert u_F-u_{\rm tar}\rVert$ ; la reconstruction visqueuse bornée ci-dessus illustre une cible exacte inaccessible **dans le sous-problème stationnaire choisi**, sans réfuter les autres formulations possibles.

Il faut également distinguer l'existence d'un minimum et la valeur de l'infimum : même un infimum nul peut ne pas être atteint si l'ensemble admissible n'est pas fermé ou si l'application contrôle–état manque des propriétés nécessaires. Ce constat ne dit pas que le problème historique est insoluble ; il indique les hypothèses de réalisabilité, de compacité ou de fermeture, de continuité et de conditions aux limites à établir avant de conclure. Voir [DRX-ERR-050](../../46-registre-erreurs-incoherences-documentaires.md).

### Extension de la traînée et portée des figures

La p. 75 (PDF 84), contrôlée visuellement, propose une famille plus souple pour le terme source de (4.8) :

$$
F_u=-\frac12u\left(a_0+a_1|u|+a_2|u|^2\right).
$$

Sous $[u]=\mathrm{m\,s^{-1}}$ et $[F_u]=\mathrm{m\,s^{-2}}$, les unités nécessaires sont $[a_0]=\mathrm{s^{-1}}$, $[a_1]=\mathrm{m^{-1}}$ et $[a_2]=\mathrm{s\,m^{-2}}$. Le cas $a_0=a_2=0$ et $a_1=C_Da_{LAD}$ redonne la traînée de (4.19). La thèse autorise des coefficients dépendant de la position et du temps dans (4.25), puis présente en figure 4.7 un exemple avec trois coefficients constants.

La seule forme polynomiale ne garantit pas que $F_u$ soit toujours une traînée : l'effet sur l'énergie cinétique spécifique est $uF_u=-u^2P(|u|)/2$, où $P(v)=a_0+a_1v+a_2v^2$. Il est dissipatif lorsque $P(v)\ge0$ sur les vitesses étudiées. Par exemple, les choix **synthétiques** $a_0=1$ s⁻¹, $a_1=-3$ m⁻¹, $a_2=1$ s·m⁻² et $u=1$ m/s donnent $P(1)=-1$ s⁻¹ et $F_u=0{,}5$ m/s² : le terme accélère alors l'écoulement. Imposer chaque coefficient non négatif suffirait à garantir $P(v)\ge0$ pour $v\ge0$, mais n'est pas nécessaire ; les contraintes réellement employées ne sont pas établies ici. La conclusion de la thèse, p. 77 (PDF 86), indique elle-même que les termes additionnels augmentent la liberté d'ajustement sans disposer encore d'une interprétation physique suffisante.

Pour identifier **trois coefficients constants** à partir de valeurs de force supposées connues, il faut aussi disposer d'informations suffisantes sur différentes vitesses : pour $u\ne0$, $-2F_u/u=a_0+a_1|u|+a_2|u|^2$. Trois vitesses absolues distinctes détermineraient algébriquement les trois coefficients dans le cas idéal sans bruit ; des vitesses trop proches rendent cette identification sensible aux erreurs. À $u=0$, le terme source est nul pour tous les coefficients et cette division n'est pas définie. Dans l'expérience inverse de la thèse, $F_u$ n'est pas supposé mesuré directement : il faut donc en outre identifier les dérivées, la viscosité et les conditions du problème d'état avant d'appliquer cet argument.

Les figures 4.6–4.8 montrent des comparaisons de profils et d'objectifs pour des cibles idéalisées ; la légende de 4.8 indique des poids tous égaux à 1. Elles illustrent les effets des formulations et des degrés de liberté, mais ne démontrent ni une validation indépendante sur une parcelle, ni l'identifiabilité physique des trois coefficients. Les valeurs complètes, le solveur, les frontières et un protocole d'évaluation restent nécessaires pour les reproduire.

### Ce que mesure l'optimisation multicritère

Les équations (4.14) et (4.16), p. 68, proposent respectivement une somme pondérée et le maximum pondéré des écarts à un ensemble de cibles ; les exemples sont des profils idéalisés. Un minimum du second objectif contrôle le pire écart **parmi les cibles et selon les poids et la norme retenus**, pas automatiquement sur toute une parcelle ou sur des profils non observés. Par exemple, si un modèle constant est ajusté en minimax à deux cibles scalaires 0 et 2, la solution 1 a une erreur maximale de 1 sur ces deux cibles ; sa distance à une troisième cible non incluse, 100, vaut 99. Ce contre-exemple ne réfute pas l'utilité de la méthode : il montre pourquoi la couverture des scénarios et l'évaluation sur des données distinctes sont indispensables avant une revendication générale de robustesse.

## Chapitre 1 : bilan et fermeture turbulente

**Périmètre.** Les équations (1.11)–(1.17), pp. 18–19 (PDF 27–28), et (1.32)–(1.44), pp. 22–25 (PDF 31–34), ont été examinées sur le fac-similé. L'analyse ci-dessous distingue les équations imprimées de leur reconstruction ; elle ne préjuge pas du code historique.

### Rapport de mélange : termes perdus entre (1.13) et (1.17)

La source imprime le bilan

$$
\partial_t c+\nabla\!\cdot(Uc)-\nabla\!\cdot(D\nabla c)=q
\tag{1.13}
$$

puis définit $\chi=c/\rho$ en (1.16). Sa relation (1.17) affiche seulement

$$
\partial_t\chi+U\cdot\nabla\chi
=-\frac{\chi}{\rho}\left(\partial_t\rho+\nabla\!\cdot(\rho U)\right).
\tag{1.17 imprimée}
$$

Sous l'interprétation $c=\rho\chi$, $\rho>0$ et la continuité du porteur $\partial_t\rho+\nabla\!\cdot(\rho U)=0$, le calcul à partir de (1.13) donne au contraire

$$
\partial_t\chi+U\cdot\nabla\chi
=\frac{q+\nabla\!\cdot\bigl(D\nabla(\rho\chi)\bigr)}{\rho}.
\tag{reconstruction depuis 1.13}
$$

La relation imprimée n'est donc pas la transformation générale de (1.13) lorsque diffusion ou source sont présentes ; elle peut décrire un cas additionnel où leur contribution nette s'annule. Si l'on choisit **une autre loi de flux**, $-\rho D\nabla\chi$, il faut dériver un bilan différent : cette autre convention ne résulte pas automatiquement de (1.13).

**Contre-exemple.** En une dimension périodique, prenons $U=0$, $\rho=1$, $q=0$, $D=0{,}5$, et $\chi(x,t)=1+0{,}5e^{-0{,}5t}\cos x$ en unités cohérentes. Alors $c=\chi$ satisfait (1.13), mais $\partial_t\chi(0,1)=-0{,}25e^{-0{,}5}\simeq-0{,}1516$ alors que (1.17) imposerait zéro. Le désaccord est donc observable même pour une concentration positive et un milieu incompressible. Voir [DRX-ERR-036](../../46-registre-erreurs-incoherences-documentaires.md).

Les unités demandent aussi une convention explicite : p. 18, la source qualifie $c$ de concentration sans dimension, tandis que p. 19 elle qualifie $c/\rho$ de rapport sans dimension. Si $\rho$ désigne une masse volumique dimensionnée et $c$ une concentration massique volumique, $\chi$ est bien sans dimension ; ce choix n'est pas établi uniformément par ces deux phrases. Le diagnostic ci-dessus est conditionné à cette interprétation et ne décide pas de l'intention de l'auteur.

### Fermeture : cohérence des objets vectoriels

Les équations (1.32)–(1.36), p. 22 (PDF 31), puis (1.38), p. 24 (PDF 33), utilisent imprimé $\nabla\!\cdot\bar c$ alors que $\bar c$ est un scalaire. Avec les conventions vectorielles usuelles, la divergence s'applique à un vecteur ; cette écriture ne définit donc pas le gradient scalaire nécessaire dans une fermeture de flux. La forme componentielle (1.39), p. 24, imprime en revanche $\overline{u_i'c'}=-K_{ij}\partial_j\bar c$. Une fermeture cohérente **reconstruite sous cette hypothèse** est $\overline{U'c'}=-K\nabla\bar c$, suivie de $\nabla\!\cdot(K\nabla\bar c)$ dans le bilan moyen. Cela conserve la fermeture comme hypothèse physique, non comme identité déduite du seul moyennage. Voir [DRX-ERR-037](../../46-registre-erreurs-incoherences-documentaires.md) et le [modèle direct actuel](../../../site/theorie/modele-direct.qmd).

## Chapitre 2 : contrôle dimensionnel de la stabilité

La p. 38 (PDF 47), §2.1.6, présente le nombre de Richardson comme une grandeur sans dimension et imprime

$$
R_i=\beta\,\frac{\partial T/\partial z}{(\partial U/\partial z)^2},
\tag{2.2 imprimée}
$$

en décrivant $\beta$ comme coefficient de dilatation. Sous la convention usuelle $[\beta]=\mathrm{K^{-1}}$, $[\partial_zT]=\mathrm{K\,m^{-1}}$ et $[\partial_zU]=\mathrm{s^{-1}}$, le membre droit a l'unité $\mathrm{s^2\,m^{-1}}$ : il n'est pas sans dimension. Un coefficient $\beta$ qui inclurait une accélération aurait d'autres unités, mais cette convention n'est pas précisée dans le passage. Un facteur dimensionnel possible ne suffit pas à reconstruire la formule physique voulue : la grandeur thermique, la stratification adiabatique et la définition du cisaillement doivent aussi être précisées. Ne pas confondre ce $R_i$ de gradient avec le $Ri_f$ de flux discuté en annexe D. Voir [DRX-ERR-038](../../46-registre-erreurs-incoherences-documentaires.md).

## Chapitre 3 : traînée, interfaces et moyennage

### Darcy et Forchheimer : préciser les grandeurs

La p. 54 (PDF 63), §3.2.3, donne d'abord en (3.14) la loi 1D $u=-(K_p/\mu)\partial_xP$, puis imprime pour sa généralisation 3D $\mathbf u=-\mu^{-1}\mathbf K_p\Delta P$ en (3.15). La même page présente $\Delta P$ comme une chute de pression et $\mathbf K_p$ comme une perméabilité d'unité m². Sous cette lecture, $[\mu^{-1}K_p\Delta P]=\mathrm{m^2\,s^{-1}}$, différent d'une vitesse en m/s ; une chute de pression scalaire ne fournit pas non plus, à elle seule, une direction. Si $\Delta$ désignait plutôt le laplacien, l'unité et le type ne conviendraient pas davantage. La forme 3D $-\mu^{-1}\mathbf K_p\nabla P$ est cohérente avec (3.14), mais constitue une reconstruction explicite, non une transcription de (3.15). L'intention de notation historique reste inconnue ; voir [DRX-ERR-039](../../46-registre-erreurs-incoherences-documentaires.md).

L'équation (3.16) ajoute un terme quadratique de Forchheimer ; la relation (3.19), p. 55, entre les coefficients de porosité et de traînée est présentée pour le régime où ce terme domine. Elle ne doit pas être étendue automatiquement à une vitesse très faible ou à un couvert hétérogène sans justification.

### Moyennes et flux d'interface

Aux pp. 56–59 (PDF 65–68), la thèse présente un volume représentatif de la phase fluide et distingue moyennes temporelles, moyennes spatiales et fluctuations. Les équations (3.31)–(3.32) introduisent des intégrales sur les interfaces air–plante ; la moyenne spatiale de quantité de mouvement fait apparaître des contraintes dispersives en plus des flux turbulents et des forces de traînée. Le texte indique que cette fermeture est sous-déterminée et énonce des hypothèses de milieu homogène à grande échelle, matrice rigide, absence de réaction et conditions isothermes. L'approximation d'un couvert réel déformable par ce modèle est donc un choix à justifier, pas une conséquence de la seule densité foliaire.

Ce bilan n'est pas automatiquement celui des interfaces artificielles entre niveaux du champ lointain. Pour ces dernières, la [note sur le champ multi-niveaux](../../31-investigation-champ-multiniveaux.md) précise une convention de normale sortante et donne un contre-exemple : un flux net nul sur une frontière peut masquer des sauts locaux non nuls. La correction du signe de la dérivée d'une fonction indicatrice dans cette note est suivie sous [DRX-ERR-040](../../46-registre-erreurs-incoherences-documentaires.md).

## Chapitre 5 : profil de jet et interface de source

**Périmètre.** Les équations (5.43)–(5.67), pp. 99–103 (PDF 108–112), ont été vérifiées visuellement sur le fichier versionné. Les diagnostics ci-dessous portent sur les expressions imprimées et leurs hypothèses, pas sur le comportement d'un code historique non examiné.

La [dérivation cylindrique du transport scalaire et de la similitude](../../61-ingestion-these-chapitres-3-5-7.md) examine aussi (5.32)–(5.40), pp. 95–96 (PDF 104–105) : dérivée et facteur radial imprimés en (5.33), expression incomplète en (5.38), puis écart conditionnel de coefficient en (5.40). Le facteur $1/\eta$ peut se simplifier des deux côtés ; sa seule absence dans (5.38) ne prouve pas une omission.

### Continuité du profil axial à la sortie d'un rang

La source annonce en (5.43) un profil continu : à l'intérieur du couvert, $c_{\rm row}\exp[-d(x)A_{LAD}C_D]$ ; ailleurs, $c_0K_{cjet}/(x-x_0)$. Elle fixe explicitement $c_{\rm row}=c_{\rm free}(x_e)$ à l'entrée $x_e$, où $d(x_e)=0$. Cela raccorde bien les deux branches **à l'entrée**.

Pour contrôler la sortie, considérons un seul rang, $x_s>x_e>x_0$, une pénétration $d(x)=x-x_e$ dans le rang, et supposons que les paramètres imprimés $c_0$, $K_{cjet}$ et $x_0$ gardent leurs valeurs dans la branche libre en sortie. En posant $A=c_0K_{cjet}$ et $k=A_{LAD}C_D$, les limites sont

$$
c(x_s^-)=\frac{A}{x_e-x_0}e^{-k(x_s-x_e)},\qquad
c(x_s^+)=\frac{A}{x_s-x_0}.
$$

Elles ne coïncident que sous une condition supplémentaire, $e^{-k(x_s-x_e)}=(x_e-x_0)/(x_s-x_0)$. Par exemple, pour $x_0=0$, $x_e=2\,\mathrm m$, $x_s=3\,\mathrm m$ et $k=0{,}8\,\mathrm{m^{-1}}$, les deux limites rapportées à $A$ valent environ $0{,}2247\,\mathrm{m^{-1}}$ et $0{,}3333\,\mathrm{m^{-1}}$. La continuité annoncée ne découle donc pas de la formule imprimée pour ces paramètres. Une mise à jour des paramètres à la sortie pourrait définir une autre branche, mais elle n'est pas spécifiée dans ce passage ; la figure 5.8 et le code ancien ne suffisent pas ici à établir quelle règle a été exécutée. Voir [DRX-ERR-041](../../46-registre-erreurs-incoherences-documentaires.md).

### Normalisation de la source et passage du plan

Les équations (5.50)–(5.55), p. 102 (PDF 111), construisent, pour chaque buse, un taux volumique en normalisant une forme $g=c^i_{\rm flux}$ :

$$
s_i(x)=Q_i\,\frac{g_i(x)}{\int_V g_i\,dV},
\qquad \int_V s_i\,dV=Q_i,
$$

pour une intégrale finie et strictement positive et un débit $Q_i$ en kg/s. La quantité $s_i$ est en kg·m⁻³·s⁻¹ ; (5.56)–(5.57) accumulent ensuite $s_i\Delta t$ dans $c_{loc}$ en kg·m⁻³. Pour une sous-région $\Omega_+$, l'intégrale de $s_i$ donne la **part du taux injecté dans cette sous-région**. Cette normalisation algébrique ne démontre pas à elle seule une conservation dynamique ni un franchissement du plan.

Les équations (5.64)–(5.67), p. 103 (PDF 112), rapprochent le flux ascendant $\int_Swc_{loc}\,dS$ du taux volumique injecté au-dessus de $H$. Les deux termes sont bien en kg/s, mais leur équivalence approchée exige un bilan et des hypothèses supplémentaires. Pour un volume fixe $\Omega_+$ au-dessus du plan, avec flux total $J$, taux de source $s$ et puits $\ell$, le bilan général reconstruit est

$$
\frac{dM_+}{dt}=S_+-L_+ +\Phi_H-\Phi_{\rm autres},\qquad
\Phi_H=\frac{dM_+}{dt}-S_++L_++\Phi_{\rm autres},
$$

où $\Phi_H=\int_S J\cdot e_z\,dS$ est le flux net entrant par le bas, $\Phi_{\rm autres}$ le flux sortant par les autres frontières et $S_+,L_+$ les intégrales volumiques. Cette identité ne pose pas $\Phi_H=S_+$ : celle-ci nécessite une relation additionnelle entre stockage, sources, puits et sorties. Un écoulement stationnaire, à lui seul, n'impose pas que la concentration cumulée en (5.56) soit stationnaire.

**Contre-exemple.** Sur une section de 1 m² et $z\ge0$, prenons $g(z)=c_*e^{-z/L}$ avec $L=1$ m, un débit $Q=2$ kg/s, un vent vertical constant vers le haut et une concentration initiale nulle. La normalisation injecte instantanément au-dessus de $H=1$ m le taux $S_+=2e^{-1}\simeq0{,}736$ kg/s, mais le flux au plan à l'instant initial vaut zéro puisque $c_{loc}=0$. Le stockage augmente : il n'y a aucune contradiction avec la conservation. Cet exemple montre que (5.67) n'est pas une identité générale ; il ne démontre pas à lui seul l'erreur quantitative du scénario historique. Voir [DRX-ERR-042](../../46-registre-erreurs-incoherences-documentaires.md) et [l'audit de conservation](../../43-audit-these-brun-conservation-g0s.md).

L'[audit de l'interface source–transport](../../audits/these-interface-source-transport.md) complète ce contrôle par un bilan stationnaire conservatif où le flux au plan et la source au-dessus diffèrent, ainsi que par un tableau reliant ces grandeurs à l'inventaire lointain et à l'estimation expérimentale. Cet exemple stationnaire est une solution d'une équation de transport, distincte de la récurrence additive historique ; il ne mesure pas l'erreur de l'essai.

## Essais du modèle de source locale — lecture des pages 103–109

**Objet mesuré.** Les §§5.7–5.8 décrivent des essais sur parcelle artificielle à Montpellier, le 13 juillet 2005, avec collecteurs passifs de diamètre 2 mm et traceur fluorescent. Cinq lignes de 12 m, espacées de 2 m, échantillonnent un plan horizontal à 2,5 m du sol ; elles sont disposées parallèlement aux rangs. Le pulvérisateur effectue quatre passages pendant chaque essai ; trois essais sont rapportés pour chacune des deux qualités de pulvérisation (pp. 103–106). Les quantités collectées sont intégrées spatialement puis normalisées par la quantité pulvérisée : il s'agit d'une estimation de perte ascendante relative, pas d'une concentration atmosphérique lointaine ni d'une mesure directe de l'exposition.

### Reconstruction de l'observable expérimentale

La figure 5.11 et les équations (5.68)–(5.69), p. imprimée 106 (PDF 115), ont été contrôlées sur le fac-similé. Après les quatre passages d'un essai, chaque ligne est lavée avec 200 ml d'eau ; la fluorimétrie et la concentration du mélange servent à estimer le volume $V_i$ de bouillie capté par cette ligne. Le volume de lavage n'est donc pas $V_i$. La thèse définit $S_i=V_i/d$, où $d=2$ mm, puis une somme de trapèzes entre lignes séparées de 2 000 mm. Elle rapporte $S_i$ en ml/mm et le résultat $Q$ en ml : les unités sont cohérentes si les distances sont exprimées en mm. La coordonnée $h_i$ repère ici la position **transversale** des lignes ; elle ne désigne pas leur hauteur commune de 2,5 m.

Pour cinq valeurs mesurées $S_1,\ldots,S_5$, une reconstruction explicitement limitée aux quatre intervalles entre lignes s'écrit

$$
Q_{[1,5]}=\sum_{i=1}^{4}\frac{S_i+S_{i+1}}{2}(h_{i+1}-h_i),\qquad
P_{[1,5]}=100\,\frac{Q_{[1,5]}}{V_{\rm pulvérisé}}.
$$

La formule imprimée somme jusqu'à $n$ et utilise $S_{i+1}$ ; le passage ne précise pas explicitement si $n$ désigne les intervalles ou les lignes. Si $n=4$ désigne les intervalles, elle correspond à la reconstruction ci-dessus ; si $n=5$ désigne les lignes, il faudrait une sixième valeur ou une convention de bord. Cette ambiguïté ne démontre pas une erreur du calcul effectivement réalisé. L'estimateur par trapèzes correspond à l'intégrale de l'interpolation linéaire sur les 8 m entre les deux lignes extrêmes ; il ne reconstitue pas les contributions hors de cet intervalle.

**Contrôle synthétique, pas une donnée historique.** Avec $S=(0{,}001,0{,}002,0{,}003,0{,}002,0{,}001)$ ml/mm et un espacement de 2 000 mm, la somme donne $Q_{[1,5]}=16$ ml. Pour un volume pulvérisé hypothétique de 1 000 ml sur les quatre passages, elle donne $P_{[1,5]}=1{,}6\ \%$. Ce calcul vérifie les indices, les unités et le dénominateur ; il ne reproduit aucun essai de la thèse.

**Efficacité et comparaison au modèle.** La thèse rapporte une efficacité des collecteurs comprise entre 78 % et 100 % et en déduit des pertes de 6,1–7,9 % et 11,0–14,0 % pour les deux séries. À titre de contrôle, diviser les moyennes 6,14 % et 10,95 % par 0,78 donne respectivement 7,87 % et 14,04 %, ce qui retrouve leurs bornes hautes arrondies. Cette opération suppose une efficacité multiplicative applicable à l'estimation intégrée ; la plage publiée n'est pas, à elle seule, un intervalle de confiance statistique ni une mesure de l'efficacité propre à chaque ligne et essai.

La collecte et le lavage fournissent des volumes **cumulés sur quatre passages**, sans résolution temporelle dans le protocole décrit. Pour comparer une simulation à cette observation, il faut expliciter l'opérateur de mesure : période et longueur échantillonnées, profils prédits aux cinq positions ou intégration comparable, capture des gouttes et efficacité, correction éventuelle, unités et même volume pulvérisé. Une concentration ponctuelle ou un flux instantané ne sont pas directement le pourcentage mesuré ; la perte de matière hors des lignes extrêmes et l'incertitude de l'interpolation doivent être traitées. L'approximation de source du modèle et la mesure ne sont pas automatiquement équivalentes (voir aussi DRX-ERR-042).

**Données nécessaires pour reproduire l'évaluation.** Retrouver, pour chaque essai, les cinq $V_i$ ou mesures fluorimétriques et étalonnages, les coordonnées et durée des passages, le volume réellement pulvérisé, les conditions météo par essai, les blancs/récupérations et l'efficacité ou son modèle selon les gouttes et conditions. Préciser les mesures et réglages utilisés pour calibrer le modèle, puis réserver des essais indépendants à l'évaluation. La référence [103] de la thèse est Gil et al., *Loss of spray above an artificial vineyard during air-assisted spraying*, indiquée comme soumise en 2006 dans sa bibliographie (p. imprimée 184, PDF 193) ; la disponibilité actuelle des données associées et l'identité de toute version ultérieure ne sont pas établies ici. Aucun jeu brut n'est revendiqué comme disponible sur la seule base de la thèse.

Un [inventaire local borné](../../audits/these-inventaire-elements-historiques.md) précise les fichiers et archives recherchés, les empreintes des documents identifiés et les limites du résultat négatif. Les CSV DIFLU retrouvés concernent une autre campagne et ne remplacent pas ces mesures.

**Conditions.** La parcelle comporte quatre rangs artificiels de 8 m ; la thèse rapporte pour les séries fine et très fine des vitesses moyennes de vent respectivement de 0,30 et 0,72 m/s et des paramètres de stabilité z/L de −1,23 et 0,23 (tableau 5.4, p. 105). Les deux séries diffèrent donc aussi par les conditions météorologiques rapportées : attribuer causalement l'écart à la seule taille des gouttes dépasse ces observations. L'indépendance statistique des essais et les données individuelles ne sont pas établies par cette lecture ciblée.

**Résultats et vérification.** La p. 106 rapporte des pertes moyennes de **6,14 %** pour la pulvérisation fine et **10,95 %** pour la très fine, avec des coefficients de variation de 5,93 % et 10,84 %, respectivement. La p. 107 rapporte pour une simulation environ 12 % de perte et environ 30 % captés par la végétation ; la figure 5.12 compare un profil simulé aux profils expérimentaux moyens. La conclusion (p. 109) qualifie les résultats de préliminaires et l'accord de faible. La thèse discute notamment l'absence du vent et de l'effet de la gravité selon la taille des gouttes dans le modèle local ; ces simplifications limitent l'interprétation.

La p. 106 affirme aussi que les pertes normalisées sont « 44% larger » en très fin. Or, à partir des moyennes imprimées, l'écart est de **4,81 points de pourcentage**, soit `(10,95 − 6,14) / 6,14 ≈ 78,3 %` relativement à la valeur fine. Le rapport à la valeur très fine vaut environ 43,9 %, mais ce calcul inverse le dénominateur ; il ne justifie pas l'affirmation « plus élevé de 44 % ». L'arrondi des deux moyennes ne peut expliquer l'écart. Il s'agit d'une incohérence du commentaire avec les nombres publiés ; sa cause historique et les valeurs brutes restent inconnues.

**Conséquence pour J-DriftX.** Cet essai est un candidat pour reconstruire et auditer l'interface de source locale : il faut retrouver les données individuelles et les conventions d'intégration, documenter l'efficacité des collecteurs et l'incertitude, puis comparer une observable identique, avec séparation calibration/évaluation. Les chiffres agrégés ne suffisent pas à reconstituer des profils ni à évaluer la dispersion lointaine. La comparaison de deux qualités sous des météorologies différentes ne permet pas d'isoler l'effet de la granulométrie.

## Conservation et géométrie

La page imprimée 129 (PDF 138) a été examinée visuellement sur le fichier versionné : elle imprime bien les deux alternatives de l'équation (7.12), puis l'objectif de conservation (7.13). Le diagnostic dimensionnel et la distinction entre inventaire et flux sont dans [docs/43](../../43-audit-these-brun-conservation-g0s.md). Cette vérification locale ne prouve ni la conservation générale, ni l'identité binaire avec une autre copie, ni l'absence d'une démonstration ailleurs dans la thèse.

## Transport lointain : formulation et approximations examinées

Les repères de cette section ont été contrôlés visuellement dans le PDF versionné, pp. imprimées 126–137 (PDF 135–146). Ils documentent la formulation historique ; ils ne garantissent ni son implémentation complète ni sa validité en terrain réel.

| Objet | Ce que le texte présente | Portée et questions pour une reconstruction |
|---|---|---|
| Temps dirigé | §7.1.3, p. 128 (PDF 137), équations (7.6)–(7.7) : si A est au vent de B, temps le long de la caractéristique issue de A jusqu'à la projection euclidienne $B^\perp$, et valeur infinie dans le sens inverse. La source suppose la caractéristique unique et propose un critère si la projection ne l'est pas. | C'est un temps **jusqu'à une projection**, pas nécessairement un temps d'arrivée en B. La règle opérationnelle de sélection, le cas de vitesse nulle et les frontières restent à expliciter. |
| Champ de vent | §7.2.1, p. 128 : $u=\nabla\phi$ et $-\Delta\phi=\sum_i\lVert\nabla\phi(x_i)-u_{obs}(x_i)\rVert$, puis prolongement vertical et adaptation locale au relief. | Les indices $i$ apparaissent explicitement dans la thèse, contrairement à l'ambiguïté relevée pour l'équation correspondante de 2006 dans [docs/45](../../45-audit-article-mohammadi-brun-2006.md). Cela ne résout pas les dimensions ou la compatibilité avec un champ sans divergence : sous les unités usuelles, le membre gauche est en s⁻¹ et la somme en m·s⁻¹ ; de plus $\nabla\!\cdot u=\Delta\phi$ ne s'annule pas en général si le résidu est non nul. Il faut définir domaine, conditions aux limites et toute normalisation avant implémentation. |
| Approximation numérique | Fin du §7.3, pp. 130–131 (PDF 139–140) : interpolation polynomiale itérative de la trajectoire, conditions aux extrémités et ajout de points intermédiaires choisis aléatoirement ; la source admet ensuite l'approximation $B^\perp=B$ et l'improbabilité que la caractéristique passe exactement par B. | Le passage ne donne pas à lui seul une tolérance d'arrêt, une graine, une preuve de convergence ou une règle de sélection des racines/projections. Il faut conserver distincts la définition géométrique et son approximation ; ne pas qualifier le chemin interpolé de caractéristique exacte sans contrôle du résidu. |
| Facteur imprimé | P. 131 (PDF 140), la source applique aux temps un facteur imprimé « $2/3=0.636$ », décrit comme cosinus moyen stochastique d'angles entre 0 et $\pi$. | $2/3\approx0,6667$, donc l'égalité imprimée est fausse. Pour une loi uniforme sur $[0,\pi]$, $E[\cos\theta]=0$ et $E[|\cos\theta|]=2/\pi\approx0,6366$ ; la valeur absolue et la loi uniforme sont ici des **hypothèses de comparaison**, non une interprétation établie de la source. Le calcul historique effectivement utilisé reste inconnu : [DRX-ERR-010](../../46-registre-erreurs-incoherences-documentaires.md). |
| Panache généralisé | Équations (7.14)–(7.15), pp. 129–130, puis (7.20), p. 131 : profil axial et profil radial, ensuite évalués à partir du temps de migration et d'une distance transverse approchée. La forme radiale imprimée en (7.15) est proportionnelle à $\exp(-b r)$. | Cette forme exponentielle en $r$ n'est pas automatiquement une gaussienne en $r^2$. Le passage de distances physiques à un temps exige des paramètres et unités compatibles ; la généralisation est une hypothèse de modèle, pas une démonstration d'équivalence à l'EDP. |

## Calage, comparaison numérique et identification de source

| Preuve | Lecture directe et interprétation limitée |
|---|---|
| **Fonction objectif**, §§7.5.1–7.5.2, pp. 131–132 (PDF 140–141) | La fonction (7.22) additionne une norme discrète des écarts de vitesse et une norme discrète des écarts de concentration. Les unités de ces deux termes diffèrent en général ; les poids, normalisations, erreurs de mesure, domaine de paramètres et conditions d'identifiabilité ne sont pas précisés dans ces passages. Le texte décrit aussi une recherche des sources possibles par sensibilité : une sensibilité élevée ne démontre pas l'unicité de la source. |
| **Calage à une référence**, annexe E.1, pp. 169–171 (PDF 178–180) | La thèse présente un exemple en vent uniforme stationnaire sur terrain plat et indique ajuster les paramètres pour minimiser l'écart à un modèle gaussien, à l'aide de BMO. C'est un **calage à un autre modèle** pour ces conditions ; la concordance obtenue après ajustement ne constitue pas une validation indépendante sur des observations de terrain. Les valeurs finales des paramètres, les points et poids utilisés, et un jeu indépendant ne sont pas spécifiés dans ces trois pages examinées. |
| **Comparaison EDP**, §7.6 et figure 7.5, pp. 132–133 (PDF 141–142) | Le texte rapporte une comparaison avec une simulation EDP et un maillage cartésien de pas $\Delta x=\Delta y=1$ km, ainsi qu'un accord qualitatif de tendance. La légende précise une EDP transport–diffusion–dépôt par éléments finis, un même vent interpolé, un domaine annoncé de 30 km² et une évaluation du modèle réduit aux nœuds. Les pages examinées ne donnent pas de métrique d'erreur ni les données et réglages complets permettant de reproduire cette figure. La comparaison intermodèles n'est pas, à elle seule, une validation empirique. |
| **Coût**, p. 133 (PDF 142) | Un facteur d'environ $10^3$–$10^4$ est rapporté pour une évaluation ponctuelle comparée à un calcul global, pour un maillage décrit comme d'environ 1 000 points. Cette affirmation ne fixe pas dans le passage un protocole complet à précision comparable incluant reconstruction du vent, trajectoires, calibration, nombre de requêtes et mémoire ; elle ne suffit pas à démontrer ce gain pour J-DriftX. |
| **Cas illustratifs**, figures 7.8–7.10, pp. 136–137 (PDF 145–146) | Deux sources et relief sont illustrés par des cartes normalisées ; la figure 7.10 montre une analyse de sensibilité pour une pollution détectée. La légende permet de parler de zones d'origine possibles, non de localisation unique démontrée ou d'un essai indépendant sur pollution réelle. |

**Suite scientifique recommandée.** Pour rendre le chapitre exploitable, commencer par un contrat de reproduction du cas uniforme : source et observable, unités, paramètres et données de calage, solution de référence et domaine de comparaison. Ensuite geler une approximation de trajectoire distincte de la définition projetée et mesurer son résidu ainsi que ses échecs. Une évaluation physique demanderait des observations indépendantes, avec séparation des données de calage et de test et prise en compte des incertitudes.

L'[analyse du calage et de la sensibilité](../../audits/these-calage-identification-sources.md) donne un exemple où la somme numérique brute de (7.22) change de minimum selon les unités, puis propose un contrat de reconstruction sans attribuer ses poids à l'histoire. Un second exemple distingue sensibilité de l'objectif et bonne localisation de source ; les paramètres et conventions historiques restent à retrouver.

## Annexe E : stabilité par défaut et portée du calage

**Lecture de la source.** Pour les rejets horizontaux au sol, le tableau E.1, p. 170 (PDF 179), associe D à 5 m/s comme conditions médianes et F à 3 m/s comme conditions défavorables. La p. 171 (PDF 180), contrôlée visuellement, indique que la classe est déterminée d'après les mesures météorologiques ou prise par défaut à D « afin de majorer les pertes ». Ces deux passages ne définissent pas suffisamment l'observable « pertes », le domaine spatial et les scénarios concurrents pour établir une borne générale. La qualification de F comme défavorable pour des distances de danger ne prouve pas, à elle seule, une contradiction formelle : les deux passages pourraient viser des grandeurs différentes.

**Contre-exemple explicite pour une concentration, reconstruit dans J-DriftX.** Considérons un panache stationnaire gaussien en terrain plat, sans dépôt, avec réflexion au sol, source continue au sol de $Q=1$ kg/s, et récepteurs au sol à $x=1\,000$ m. Les deux scénarios utilisent les couples du tableau E.1 : D à 5 m/s et F à 3 m/s. Les largeurs ci-dessous proviennent des **lois rurales de Briggs implémentées dans le dépôt**, et non de l'équation E.1 historique ni de mesures de terrain :

| Scénario | $\sigma_y$ (m) | $\sigma_z$ (m) | $C$ sur l'axe, $y=0$ (kg/m³) | $C$ à $y=200$ m (kg/m³) |
|---|---:|---:|---:|---:|
| D, 5 m/s | 76,28 | 37,95 | $2{,}20\times10^{-5}$ | $7{,}07\times10^{-7}$ |
| F, 3 m/s | 38,14 | 12,31 | $2{,}26\times10^{-4}$ | $2{,}41\times10^{-10}$ |

Sur l'axe, F donne environ 10,3 fois la concentration de D ; à 200 m latéralement, D donne une concentration supérieure à F. Le changement de classe **et** de vitesse contribue au premier rapport, tandis que les différences de largeurs expliquent le renversement spatial. Ainsi, même dans cette reconstruction simple, aucune des deux configurations ne majore partout la concentration ponctuelle. Ce calcul n'établit pas quelle classe majore une perte agricole, un dépôt ou une autre grandeur non définie ; il ne valide pas non plus les lois de Briggs sur un site réel. Voir [DRX-ERR-046](../../46-registre-erreurs-incoherences-documentaires.md).

**Reproductibilité du calage historique.** Les équations (E.1)–(E.3), p. 171, donnent $TH=0{,}017453293[c-d\log(x)]$ et $\sigma_y=465{,}11628\,x\tan(TH)$, avec $x$ en km. Les pages de l'annexe examinées ne précisent pas les valeurs de $c,d$, la base du logarithme, l'unité de sortie de $\sigma_y$ ni une loi complète de $\sigma_z$ pour ce calage. Elles ne donnent pas non plus la grille de comparaison, la fonction d'écart détaillée et ses poids, les paramètres obtenus ou les critères d'arrêt de BMO. Ne pas injecter silencieusement les coefficients de Briggs actuels pour combler ces lacunes : c'est un autre choix de référence dont l'équivalence historique n'est pas établie. Une reproduction demanderait de retrouver ces conventions et de séparer calibration et évaluation indépendante.

## Annexe B : noyau transitoire et similitude stationnaire

**Portée de lecture.** Les équations discutées ci-dessous ont été contrôlées visuellement sur les pp. imprimées 151–158 (PDF 160–167). La revue cible les étapes et conséquences indiquées ; elle ne constitue pas une certification exhaustive de chaque ligne de calcul. Les formules imprimées sont conservées ci-dessous : les expressions déduites sont des reconstructions explicitement séparées.

### B.1 : une masse impulsionnelle en espace entier

La thèse pose en (B.1) une équation de diffusion tridimensionnelle en coordonnées relatives au centre de masse, puis une masse totale $M$ en (B.4). En (B.44)–(B.45), p. 154 (PDF 163), elle imprime un produit de gaussiennes de masse $M$ et des largeurs $\sigma_i=\sqrt{2K_i t}$. Sous diffusivités constantes positives et donnée initiale **ponctuelle** $M\delta_0$, cette forme est le noyau d'une émission impulsionnelle en espace entier. Avec un vent uniforme en coordonnées fixes, son centre est translaté par $Ut$ ; ce passage est une déduction sous hypothèses, pas une équation d'advection supplémentaire imprimée en (B.1).

**Limites.** Malgré le nom « plume » employé dans le texte, cette formule contient une masse $M$ et dépend du temps : elle ne doit pas être identifiée au panache stationnaire entretenu par un débit $Q$. La masse imprimée dans (B.4) porte sur $z\in\mathbb R$ : la formule de cette section ne contient pas de condition au sol réfléchissant. Elle est centrée sur $z=0$ ; intégrée sur le seul demi-espace $z\ge0$, elle donne $M/2$, pas $M$. La source ponctuelle sous forme de Dirac est une hypothèse nécessaire à la reconstruction de ce noyau, à distinguer de la seule masse totale.

**Audit des étapes de Fourier, pp. 151–153 (PDF 160–162).** Les écarts ci-dessous portent sur les égalités imprimées ; ils ne prouvent pas, à eux seuls, que le noyau final (B.44) soit faux dans le cas gaussien centré :

| Repère | Constat contrôlé | Conséquence |
|---|---|---|
| (B.5)–(B.6) | Les deux formules utilisent $e^{-i\mathbf k\cdot\mathbf x}$, avec le même facteur de normalisation symétrique. | Composer ces deux transformations renvoie en général $c(-\mathbf x,t)$, non $c(\mathbf x,t)$. Pour l'inverse de (B.5), le signe attendu est positif. La symétrie du noyau centré peut masquer cet écart. |
| (B.20)–(B.21) | Le coefficient de la somme de $K_i k_i^2$ est positif dans (B.20), négatif dans (B.21). | Les deux lignes ne sont pas égales en général. Avec $K_i\ge0$, le signe négatif découle de $(ik_i)^2=-k_i^2$ et donne la décroissance diffusive de (B.21). |
| (B.24)–(B.25) | La factorisation (B.25) répète trois fois le facteur longitudinal $\exp(-K_xk_x^2t)$ ; (B.24) et (B.29) comportent trois directions distinctes. | La factorisation imprimée ne suit pas de (B.24) pour des diffusivités et nombres d'onde quelconques ; ne pas l'utiliser comme définition de l'anisotropie. |
| (B.30)–(B.33) | La substitution imprimée en (B.30) ne conserve qu'un facteur $(2\pi)^{-3/2}$ alors que (B.6) et (B.29) en apportent chacun un ; (B.32)–(B.33) omettent aussi les facteurs de phase présents en (B.31). | Ces lignes ne constituent pas une dérivation valide telle qu'imprimée. Une reconstruction cohérente utilise le produit des deux normalisations et conserve la phase dans chaque intégrale. |

Avec la convention directe de (B.5), une dérivation cohérente sur $\mathbb R^3$ utilise le signe positif à l'inversion, $\widehat c(\mathbf k,0)=M/(2\pi)^{3/2}$ pour $M\delta_0$, puis $\widehat c(\mathbf k,t)=\widehat c(\mathbf k,0)\exp[-t\sum_iK_i k_i^2]$. Pour $K_i>0$ constants et $t>0$, elle redonne le noyau de (B.44) avec $\sigma_i^2=2K_it$. Cette vérification reconstruit une preuve sous hypothèses ; elle n'efface pas les incohérences des étapes imprimées. Voir [DRX-ERR-031](../../46-registre-erreurs-incoherences-documentaires.md).

### B.2 : une source linéique continue et le contrôle de normalisation

La thèse considère une source de longueur $H$, de débit total $Q$, sans frontière solide, et une seule direction de diffusion transverse $z$ ; dans cette section, $H$ désigne **la longueur de source**, pas la hauteur de rejet du cas S0. Elle écrit $U\,\partial_x\bar c=K\,\partial^2_z\bar c$ en (B.46), pose $\eta=z/\sigma$ et $\bar c=c_0f(\eta)$, puis obtient $K=(U/2)d\sigma^2/dx$ en (B.54) et le bilan $\int_{\mathbb R}\bar c\,dz=Q/(UH)$ en (B.55).

Une [correspondance exécutable avec le noyau Python](../../audits/these-correspondance-noyau-python.md) utilise $t=x/U$ et une largeur transverse initiale positive pour vérifier un cas de (B.46) et (B.55). Elle ne reproduit ni une source ponctuelle idéale, ni les conditions de canopée ou de dépôt.

L'[analyse des frontières de section](../../audits/these-flux-sections-diffusion.md) dérive le terme diffusif transverse à partir de (B.46) : sa disparition, les limites à l'infini et le bilan de source sont nécessaires pour relier ce calcul à (B.55). Un exemple à section finie illustre une fuite diffusante ; ses conditions ne sont pas celles de l'exemple historique infini.

**Contrôle de l'imprimé, p. 156 (PDF 165).** L'équation (B.59) donne $f(\eta)=\exp(-\eta^2/2)$, alors que (B.61) imprime $I_0=\int_{\mathbb R}\exp(-\eta^2)\,d\eta=1/\sqrt{2\pi}$. Or l'intégrale telle qu'imprimée vaut $\sqrt\pi$ ; pour le profil de (B.59), elle vaut $\sqrt{2\pi}$. L'équation (B.62) imprime ensuite

$$
\bar c_{\rm impr}(x,z)=\frac{Q/H}{\sqrt{2\pi U\sigma}}\exp\!\left(-\frac{z^2}{\sigma^2}\right).
$$

Elle ne reproduit pas le profil de (B.59). Sous $[Q]=\mathrm{kg\,s^{-1}}$, $[H]=[\sigma]=\mathrm m$ et $[U]=\mathrm{m\,s^{-1}}$, son unité est $\mathrm{kg\,m^{-2}\,s^{-1/2}}$, différente de $\mathrm{kg\,m^{-3}}$. Ces constats ne déterminent pas si l'origine est typographique ou conceptuelle ; voir [DRX-ERR-030](../../46-registre-erreurs-incoherences-documentaires.md).

**Reconstruction cohérente, non transcription.** Pour $H,U,\sigma>0$, en conservant le profil de (B.59), le bilan de (B.55) impose

$$
\bar c_{\rm reconstruit}(x,z)=\frac{Q}{HU\sqrt{2\pi}\,\sigma(x)}
\exp\!\left(-\frac{z^2}{2\sigma(x)^2}\right),\qquad
\int_{\mathbb R}\bar c_{\rm reconstruit}\,dz=\frac{Q}{HU}.
$$

La relation (B.54), avec $U$ constant et $K>0$ constant, donne $\sigma^2(x)=\sigma^2(x_0)+2K(x-x_0)/U$ ; la forme $\sigma^2=2Kx/U$ exige en plus une condition initiale ou origine compatible. Cette reconstruction vérifie la normalisation et l'EDP de l'exemple sous ces conditions ; elle ne résout ni les ambiguïtés du modèle historique lointain ni la validation empirique. La comparaison au S0 du dépôt est explicitée dans [docs/51](../../51-reference-independante-cas-s0.md).

**Contrôle numérique ponctuel.** Avec $U=3\,\mathrm{m\,s^{-1}}$, $Q=2\,\mathrm{kg\,s^{-1}}$, $H=4\,\mathrm m$, $K=0{,}4\,\mathrm{m^2\,s^{-1}}$ et $x=15\,\mathrm m$, on a $\sigma=2\,\mathrm m$. Une quadrature trapézoïdale sur $[-12\sigma,12\sigma]$ avec 120 001 points donne $\int\bar c\,dz\simeq0{,}166666666667=Q/(UH)$. Au point $z=1{,}7\,\mathrm m$, les dérivées analytiques évaluées numériquement donnent un résidu $U\partial_x\bar c-K\partial^2_z\bar c\simeq-1{,}1\times10^{-19}$ en unités SI cohérentes. Ce contrôle fini illustre les identités ; il ne remplace ni leur dérivation ni une validation physique.

### B.3 : signe du transport dans la solution imprimée

En (B.63), p. 157 (PDF 166), la thèse part de l'équation $\partial_t f+u\partial_xf-D\partial_{xx}f=0$ ; elle utilise une impulsion initiale en $x_0$. En (B.75), p. 158 (PDF 167), elle imprime pourtant, pour $D,t>0$,

$$
f_{\rm impr}(x,t)=\frac{1}{\sqrt{4\pi Dt}}
\exp\!\left[-\frac{(x-x_0+ut)^2}{4Dt}\right].
$$

Son maximum se déplace selon $x=x_0-ut$. En posant $\xi=x-x_0+ut$, une substitution directe donne

$$
\partial_t f_{\rm impr}+u\partial_xf_{\rm impr}-D\partial_{xx}f_{\rm impr}
=2u\partial_x f_{\rm impr}=-\frac{u\xi}{Dt}f_{\rm impr},
$$

résidu non nul en général lorsque $u\ne0$. La formule imprimée résout l'équation avec le signe d'advection opposé ; elle ne résout pas (B.63) telle qu'imprimée. Le résultat cohérent avec (B.63) et $f(x,0)=\delta(x-x_0)$ est le noyau **reconstruit** obtenu avec $(x-x_0-ut)^2$ ; son centre suit $x_0+ut$. Ce diagnostic ne suppose pas connaître l'intention historique et ne prouve pas que le code ancien utilisait le signe imprimé. Voir [DRX-ERR-032](../../46-registre-erreurs-incoherences-documentaires.md) et la [dérivation actuelle du puff](../../../site/theorie/similitude.qmd).

**Contrôle numérique ponctuel.** Pour $u=2$, $D=0{,}5$, $t=1$, $x_0=0$ et $x=1$ en unités cohérentes, les dérivées analytiques donnent un résidu d'environ $-0{,}0531822$ pour la formule imprimée et zéro à la précision de calcul pour la formule reconstruite. Ce cas illustre la contradiction ; la substitution symbolique ci-dessus établit sa portée pour les paramètres généraux indiqués.

## Annexes A, C, D, E et F : points de reprise

**A — Réduction, pp. 149–150 (PDF 158–159).** La thèse oppose une réduction par base de solutions précalculées à la construction d'un espace approché à partir d'informations physiques. Cela motive une famille de solutions à bas coût, mais ne fournit ni borne générale d'erreur ni mesure complète du coût de préparation. Dans le passage relatif à l'approximation par espaces de dimension croissante, la p. 149 affirme aussi qu'une approche « consistante » converge vers la solution exacte lorsque $N\to\infty$ ; elle ne précise ni le sens de la consistance ni les hypothèses de stabilité. Le passage a été vérifié visuellement.

**Limite logique de la consistance seule.** Si « consistante » signifie que le résidu sur la solution exacte tend vers zéro, cela ne suffit pas à garantir la convergence des solutions numériques. Un contre-exemple reconstruit dans $H=\ell^2$ le montre : soit $A=I$, $f=(1,1/2,1/3,\ldots)$ et $P_N$ la projection sur les $N$ premières coordonnées. Sur $\mathbb R^N$, prenons

$$
A_N=\operatorname{diag}(1,\ldots,1,1/N),\qquad A_Nu_N=P_Nf.
$$

Pour tout $v\in\ell^2$, $\lVert A_NP_Nv-P_Nv\rVert=(1-1/N)|v_N|\to0$ : cette consistance forte est satisfaite et les espaces de projection couvrent asymptotiquement $H$. Pourtant $u_N$ a pour dernière coordonnée $1$, alors que $f_N=1/N$ ; après prolongement par zéro, $\lVert u_N-f\rVert\ge1-1/N\to1$. Les inverses vérifient $\lVert A_N^{-1}\rVert=N$ : leur stabilité uniforme manque. Ce n'est pas un contre-exemple à une méthode d'éléments finis particulière ni à la convergence d'une projection orthogonale exacte sur des espaces denses ; il montre la nécessité de préciser le sens de « consistance » et les autres hypothèses de l'affirmation. Voir [DRX-ERR-055](../../46-registre-erreurs-incoherences-documentaires.md).

**C — Schéma de Burgers, pp. 159–161 (PDF 168–170).** L'annexe présente un schéma aux différences finies, une intégration en plusieurs étapes et une condition de pas de temps. L'équation (C.7), p. 159, imprime pour la dérivée seconde le quotient $(u_{i+1}-2u_i+u_{i-1})/(2h)$, alors que (C.9), sur la même page, utilise $h^2$ pour le terme diffusif. Avec $u(x)=x^2$ et $x_i=0$, la dérivée exacte vaut 2 ; le quotient de (C.7) vaut $h$ et tend vers zéro quand $h\to0$. Le quotient à $h^2$ vaut 2. Ce contre-exemple établit l'erreur de la ligne imprimée, sans déterminer le schéma réellement utilisé par le code historique. Le critère CFL et les conditions aux limites doivent être spécifiés et analysés séparément avant toute reproduction numérique ; voir [DRX-ERR-033](../../46-registre-erreurs-incoherences-documentaires.md).

### Annexe C : contrôle du pas de temps et stabilité

Les équations (C.9), (C.20)–(C.23), pp. imprimées 159–161 (PDF 168–170), ont été contrôlées visuellement. La dernière propose $\Delta t=\min_j\{h/\max(\lVert u_{j+1}^{n,p}\rVert,\lVert u_{j-1}^{n,p}\rVert,\lVert u_j^{n,p}\rVert,\lVert u_{j+1}^{n,p}\rVert,h\lVert g_j^{n,p}\rVert)\}$ : l'indice $j+1$ apparaît deux fois dans le maximum imprimé, sans effet sur sa valeur. Ici $h=\Delta x$. Le texte présente cette règle comme une extension du CFL tenant compte du terme source ; il ne fournit pas dans cette annexe une preuve générale de stabilité.

**Contrôle dimensionnel conditionnel.** Si $r$ et $t$ sont en mètres et secondes, si $u$ est la vitesse en m/s du chapitre 4 et si $g$ est le terme source de (C.1), alors $[g]=\mathrm{m\,s^{-2}}$ et $[h g]=\mathrm{m^2\,s^{-2}}$, tandis que $[u]=\mathrm{m\,s^{-1}}$. Le maximum compare donc des grandeurs de dimensions différentes ; $h/\max(\cdots)$ ne définit pas un temps de manière homogène. Les équations du chapitre 4 interprètent bien $u$ comme une vitesse et $r$ comme une distance, mais une adimensionnalisation de l'algorithme ou une autre convention pour $g$ n'est pas exclue. Quand toutes les valeurs du dénominateur s'annulent, la formule imprimée ne spécifie pas non plus de pas fini. Ne pas choisir par conjecture une racine ou un coefficient correctif : [DRX-ERR-047](../../46-registre-erreurs-incoherences-documentaires.md).

**Référence analytique distincte pour (C.9).** Pour examiner le schéma d'Euler explicite centré (C.9), et non le schéma multi-étapes (C.20), linéarisons autour d'une vitesse constante $U$, avec $g=0$, $\nu\ge0$ et une grille uniforme périodique. Pour une perturbation de Fourier de phase $\theta$, son facteur d'amplification est

$$
G(\theta)=1-i\lambda\sin\theta-4\mu\sin^2(\theta/2),\qquad
\lambda=\frac{U\Delta t}{h},\quad \mu=\frac{\nu\Delta t}{h^2}.
$$

La condition $|G|\le1$ pour toutes les phases $\theta\in[-\pi,\pi]$ est équivalente, dans ce cas linéarisé, à $0\le\mu\le1/2$ et $\lambda^2\le2\mu$. Pour une grille périodique finie donnée, seules certaines phases sont admises ; ce critère continu est alors suffisant, sans être nécessaire dans tous les cas. Par exemple, pour $\nu=0$, $U\ne0$ et $\lambda=1$, le mode $\theta=\pi/2$ a $|G|=\sqrt2>1$, bien que le CFL advectif $|\lambda|\le1$ soit satisfait ; ce mode existe sur une grille périodique dont le nombre de points est multiple de quatre. Le CFL advectif seul n'est donc pas une preuve de stabilité du schéma centré (C.9) ; la diffusion physique, les termes sources et les frontières demandent leurs propres contrôles. Ce contre-exemple **ne démontre pas** l'instabilité de (C.20), qui utilise plusieurs étapes et une viscosité numérique ; son analyse doit être menée sur son opérateur et son pas de temps effectifs.

**Intégration multi-étapes.** L'[audit de l'intégration temporelle](../../audits/these-annexe-c-integration-temporelle.md) examine (C.10)–(C.22) sur le fac-similé : le premier coefficient de la factorisation imprimée et la sortie du pseudo-code ne concordent pas avec l'avancement annoncé ; les indices du schéma à trois étapes nécessitent une convention supplémentaire. Une lecture conditionnelle des dénominateurs conduit à un demi-pas pour une source uniforme constante ; une analyse linéarisée périodique montre aussi qu'elle peut conserver la somme et rester stable tout en transportant à demi-vitesse. Ces exemples ne prouvent pas le comportement du code historique (DRX-ERR-053/054).

Le [protocole de reprise](../../audits/these-annexe-c-protocole-reprise.md) conclut à une exécution historique indéterminée avec les sources consultées et définit séparément une candidate avec ses contrôles d'ordre et de stabilité linéarisée. Il ne transforme ni cette candidate ni ses conditions périodiques en transcription historique.

**D — Échelles et stabilité, pp. 163–168 (PDF 172–177).** Le tableau D.1, p. 164 (PDF 173), compare qualitativement modèles gaussien, intégral et 3D, essais de terrain et sur maquette ; ses coûts et domaines d'usage sont des appréciations historiques, non une comparaison actuelle mesurée. La section D.2 présente des échelles et la fréquence de flottabilité ; elle rappelle que les phénomènes peuvent se chevaucher. P. 168 (PDF 177), la première phrase décrit le nombre de Richardson comme rapport cisaillement/flottabilité puis le paragraphe suivant emploie l'ordre inverse. La définition et les conventions de signe de la grandeur exacte doivent être vérifiées avant réutilisation : l'alternance imprimée ne permet pas de choisir automatiquement une formule.

L'[audit des conventions de Richardson](../../audits/these-richardson-conventions.md) distingue une définition de gradient d'une définition de flux et donne les hypothèses de fermeture reliant les deux. Leurs signes, domaines et singularités ne permettent pas de déduire automatiquement la formule historique ou une classe de stabilité discrète.

**E — Calage, pp. 169–172 (PDF 178–181).** L'annexe présente un calage au modèle gaussien en vent uniforme et terrain plat ; la p. 172 montre une interface historique. Ce calage à un modèle et cette interface ne sont pas des données d'évaluation indépendante ; détails dans le tableau « Calage » ci-dessus.

**F — Géométrie directionnelle, pp. 173–175 (PDF 182–184).** L'annexe distingue d'abord une distance minimale sur des courbes d'un temps calculé le long d'une courbe fixée. En (F.10), p. 175 (PDF 184), avec $y\ne0$ et $u(x)\cdot y\ne0$, elle imprime

$$
F_{\rm wind}(x,y)=\frac{\lVert y\rVert^2}{u(x)\cdot y}.
$$

Cette formule est homogène pour les facteurs positifs, mais n'est pas définie pour une direction transverse non nulle et devient négative si $u\cdot y<0$. Elle ne définit donc pas une métrique de Finsler positive et régulière sur **tout** l'espace tangent privé de zéro, contrairement aux propriétés générales rappelées sur la même page. La ligne précédente assimile de plus une norme de projection, toujours positive, à une projection signée ; cette égalité n'est valable que si la projection est positive. Une restriction au cône $u\cdot y>0$ est une option mathématique distincte, dont l'interprétation physique et le traitement des autres directions doivent être définis, non une correction attribuable à l'auteur. Voir [DRX-ERR-034](../../46-registre-erreurs-incoherences-documentaires.md).

Le coût de (F.10) ne se confond pas non plus avec le temps projeté du chapitre 7. Exemple en unités cohérentes : $u=(1,0)$, $A=(0,0)$, $B=(1,1)$ et chemin droit $\gamma(s)=(s,s)$ pour $0\le s\le1$. L'intégrale de (F.10) vaut 2 s ; le temps projeté sur la ligne issue de $A$ vaut 1 s ; une particule purement advectée suit $(t,0)$ et n'atteint pas $B$. Il s'agit de trois objets différents, même en champ uniforme.
