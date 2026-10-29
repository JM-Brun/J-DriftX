# 31 — Investigation du champ de vent multi-niveaux historique

**Statut.** Investigation de définition, antérieure à toute implémentation et à tout test, sur le même principe que l'investigation G0-S ([note 19](19-investigation-g0s-temps-de-parcours.md)) et que l'investigation de l'adjoint ([note 26](26-investigation-adjoint-temps-transport.md)). Cette note ne modifie aucun code.

**Date :** 28 octobre 2026. **Suivi :** [issue #42](https://github.com/JM-Brun/J-DriftX/issues/42) ; citée par la page [Contraintes physiques](https://jm-brun.github.io/J-DriftX/theorie/contraintes-physiques.html) (sections 1 et 4).

**Source de travail.** Extraction du manuscrit HAL hal-00468863 (N. Bozon, C. Sinfort et B. Mohammadi, « A GIS-based atmospheric dispersion model », STIC & Environnement 2009) déposée dans le dépôt : `raw/extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt`, sections 2.1.1 et 2.2.1. Contexte du modèle et fiche de lecture : [docs/04](04-revues-papiers-sources.md).

## 0. Objet, périmètre et dépendance

La page Contraintes physiques (section 4) conditionne tout test de divergence du champ de vent multi-niveaux historique à sa définition préalable : définition continue, conditions aux limites, sources et puits. La présente note établit ce travail de définition à partir de la source : elle retranscrit la construction, en distingue les lectures possibles, démontre ce que chacune garantit ou non, et formule l'arbitrage requis avant toute implémentation.

**Dépendance explicite — hypothèse de travail.** La comparaison équation par équation des publications apparentées de 2009-2010 (manuscrit HAL, article Applied Geomatics 2009, article JESA 2010) est en cours de consolidation par ailleurs dans le projet ; ses conclusions ne sont pas disponibles ici. Cette note prend le **manuscrit HAL** (version déposée, extraction dans le dépôt) comme unique source de travail. Toute divergence de formulation entre les versions devra être re-vérifiée avant implémentation. L'extraction automatique ne conserve ni la mise en page ni les équations : les retranscriptions ci-dessous citent le texte extrait et restent soumises à cette limite ; le PDF HAL reste la référence.

**Périmètre différé.** La correction topographique de Bernoulli-Newton (section 2.2.1 de la source) et tout le couplage SIG/QGIS (section 3 de la source) ne sont pas traités : la topographie est une tranche séparée, l'intégration applicative est différée (issue #43 et décision G0-A).

## 1. Ce que dit la source (section 2.1.1)

### 1.1 Cascade de domaines emboîtés

La source construit le champ « on a cascade of embedded rectangular homothetic domains ω_i, i = 0, ..., with ω_0 = Ω the full domain », en se restreignant délibérément aux configurations rectangulaires (note 1 de la source). Deux précisions importantes : « No information is transferred at this time from fine to coarse » (la cascade va du grossier vers le fin, sans rétroaction), et l'approche est « mesh free in the sense that no meshes is used for calculation. Only, evaluated information on wind and concentration are stored at these locations ». Les simulations citées utilisent trois niveaux, de ω_0 d'environ 10 km² jusqu'à ω_2 d'environ 10 m², avec un échantillonnage identique par niveau (grille typique 20 × 20).

### 1.2 Champ total

$$
\tilde U = \sum_{i=0}^{n_{\mathrm{level}}} \tilde u_i \, \chi(\omega_i) \qquad \text{[S2]}
$$

avec ũ_0 = ũ_H le champ du niveau le plus grossier et χ(ω_i) la fonction caractéristique du sous-domaine : « the correction is equal to zero outside ω_i ». Le champ total est une somme de correctifs à support compact dans les ω_i.

### 1.3 Restriction de vitesse : deux formulations non équivalentes

La source donne **deux formulations** de la restriction de ũ_{i−1} vers ω_i :

(a) **voie potentielle** : « For i > 1, velocity restriction from level i−1 to i is evaluated using the information from the observation point being the information at the four corners q_j of a rectangle: ũ_i = −∇φ_i, −Δφ_i = 0, φ_i(q_j) = φ_{i−1}(q_j), j = 1, .., 4 » ;

(b) **voie d'interpolation**, introduite « par linéarité » :

$$
\tilde u_i(x) = \sum_{j=1}^{4} \lambda_j(x)\, \tilde u_{i-1}(q_j), \qquad \sum_{j=1}^{4} \lambda_j = 1, \quad \lambda_j(x_i) = \delta_{ij} \qquad \text{[S3]}
$$

**La source ne nomme pas la famille des fonctions λ_j** : elle donne seulement la partition de l'unité Σ_j λ_j = 1 et la propriété nodale λ_j(x_i) = δ_ij. Elle ne dit pas explicitement que l'interpolation est bilinéaire. L'hypothèse de fonctions de base bilinéaires sur le rectangle est donc une reconstruction possible, mais non une transcription de la source. La source précise que cette décomposition est « similar » à celle de ũ_0, « where the observation quantities are becoming the values at the corners » : le champ grossier ũ_0 = ũ_H est lui-même construit à partir de quantités d'observation (voir la fiche de lecture, [docs/04](04-revues-papiers-sources.md)).

Ces deux formulations **ne sont pas équivalentes** : la première égalise des potentiels aux coins, la seconde égalise des vitesses. La section 2 examine ce que chacune garantit.

### 1.4 Identité de flux

« If ũ_{i−1} is divergence free, then this construction guarantees that ∫_{∂ω_i} ũ_i·n_i dS = ∫_{∂ω_i} ũ_{i−1}|_{∂ω_i}·n_i dS = 0. Hence, the velocity restriction in ω_i remains divergence free and is compatible with the overall field. »

### 1.5 Restriction de concentration et identité de masse

$$
c_i = \sum_{j=1}^{4} \lambda_j(x)\, c_{i-1}(q_j) \qquad \text{[S4]}
$$

« This construction guarantees that the total mass in ω_i fits the entering quantity », identité appuyée sur la règle des quatre points : « The four points trapezoidal rule is exact for numerical integration of bilinear functions ∫_ω f(x,y) dxdy = ¼ Σ_{j=1}^4 f(q_j) » (note 2 de la source ; l'égalité s'entend à l'aire du rectangle près — voir la section 2.5).

### 1.6 Ce que la source ne précise pas

- l'espace dans lequel le potentiel φ_i est cherché (existence, unicité, base) ;
- si la compatibilité aux coins porte sur les potentiels (formulation a) ou sur les vitesses (formulation b) ;
- le traitement de la discontinuité de [S2] à travers la frontière ∂ω_i ;
- la construction exacte de ũ_0 = ũ_H (renvoyée aux travaux antérieurs du corpus).

Ces lacunes ne sont pas des critiques : elles délimitent ce qu'une implémentation doit arbitrer avant de pouvoir tester quoi que ce soit.

## 2. Ce que chaque lecture garantit — et ne garantit pas

Les résultats de cette section sont des démonstrations de la présente note (calcul élémentaire) ; ils ne sont pas attribués à la source.

### 2.1 Lecture R1 (égalité des potentiels aux coins) : sous-déterminée

La formulation (a) impose à φ_i d'être harmonique dans ω_i et de coïncider avec φ_{i−1} aux quatre coins. Ces conditions ne déterminent pas φ_i : l'espace des fonctions harmoniques sur un ouvert est de dimension infinie, et le noyau des quatre fonctionnelles d'évaluation φ ↦ φ(q_j) garde une dimension infinie. Il existe donc une infinité de potentiels compatibles, dont les gradients diffèrent : **R1 définit une famille, pas un champ**.

Plus grave : l'égalité des potentiels aux coins ne contraint même pas les vitesses aux coins. Si h est harmonique, nulle aux quatre coins et de gradient non nul aux coins (une telle h existe, cf. ci-dessus), alors φ_i = φ_{i−1} + h satisfait les conditions de (a) alors que ∇φ_i(q_j) ≠ ∇φ_{i−1}(q_j). Or la compatibilité du champ total se joue sur les vitesses. R1 seule ne peut pas être implémentée sans choix supplémentaire.

### 2.2 Hypothèse R2 (fonctions de base bilinéaires) : déterminée, mais à divergence non nulle en général

**Sous l'hypothèse supplémentaire de fonctions de base bilinéaires**, la formule (b) détermine ũ_i de façon unique. Chaque composante de ũ_i est alors bilinéaire, donc sa divergence est une fonction affine de (x, y) : elle est identiquement nulle seulement sous des conditions linéaires de compatibilité portant sur les huit valeurs de coins. Le flux net ne s'en sauve pas : pour un rectangle ω = [0, a] × [0, b] de coins q_1 = (0,0), q_2 = (a,0), q_3 = (a,b), q_4 = (0,b), le flux net de l'interpolé à travers ∂ω vaut

$$
\frac{b}{2}\,[u_x(q_2) + u_x(q_3) - u_x(q_1) - u_x(q_4)]
+ \frac{a}{2}\,[u_y(q_3) + u_y(q_4) - u_y(q_1) - u_y(q_2)],
$$

combinaison linéaire des valeurs de coins qui ne s'annule pas automatiquement, même lorsque le champ parent est à divergence nulle.

**Contre-exemple explicite** (démonstration de cette note). Soit ψ(x, y) = (x/a) · y² · (y − b) et u = ∇⊥ψ :

$$
u(x, y) = \left( \frac{x}{a}\,(3y^2 - 2by),\; -\frac{y^2 (y - b)}{a} \right).
$$

Ce champ est lisse et ∇·u = (3y² − 2by)/a − (3y² − 2by)/a = 0 partout. Aux coins : u(q_1) = u(q_2) = u(q_4) = (0, 0) et u(q_3) = (b², 0). L'interpolé bilinéaire [S3] est donc ũ = (b² · (x/a)(y/b), 0), de divergence (b/a) · y, d'où un flux net à travers ∂ω :

$$
\int_\omega \nabla\cdot\tilde u\; \mathrm{d}V = \frac{b}{a} \int_0^b y\, \mathrm{d}y \int_0^a \mathrm{d}x = \frac{b^3}{2} \neq 0 .
$$

**L'identité de flux annoncée dans la source n'est pas garantie par la reconstruction bilinéaire R2** : le contre-exemple montre qu'elle peut être fausse pour un champ parent pourtant à divergence nulle. Cela réfute la garantie générale sous cette hypothèse d'interpolation ; cela ne réfute pas toute interpolation satisfaisant les seules propriétés effectivement imprimées dans la source. On ne peut donc ni attribuer R2 à la source, ni conclure que la source est mathématiquement contradictoire sans connaître la famille λ_j réellement utilisée. Un test sous R2 caractérise cette reconstruction particulière, pas la méthode historique dans son ensemble.

### 2.3 Lecture R3 (potentiel harmonique ajusté aux vitesses de coins) : cohérente, mais non unique

Lecture la plus cohérente avec l'identité de flux (section 1.4) et avec la phrase « similar decomposition [...] than for ũ_0 » : chercher φ_i harmonique dans ω_i tel que −∇φ_i(q_j) = ũ_{i−1}(q_j) aux quatre coins.

- **Divergence ponctuelle nulle par construction** : ∇·(−∇φ_i) = −Δφ_i = 0. Le flux net à travers ∂ω_i est alors nul à chaque niveau (théorème de la divergence, absence de sources) : l'identité de la source devient exacte, chacune des deux intégrales étant nulle pour son propre compte — sous réserve que ũ_{i−1} soit lui-même à divergence nulle, ce que la construction assure de proche en proche depuis ũ_0.
- **Huit conditions** (4 coins × 2 composantes). Une base de fonctions harmoniques à gradient non nul de dimension au moins huit permet un ajustement exact générique : par exemple les parties réelles et imaginaires de (x + iy)^n pour n = 1, …, 4, soit les huit fonctions x, y, x² − y², 2xy, x³ − 3xy², 3x²y − y³, x⁴ − 6x²y² + y⁴, 4x³y − 4xy³. L'inversibilité du système 8 × 8 est générique mais doit être vérifiée numériquement : des symétries du rectangle peuvent créer des dépendances, et l'implémentation doit prévoir un repli (moindres carrés par exemple).
- **Non-unicité entre bases** : différentes bases harmoniques (polynômes, multipoles, solutions fondamentales) donnent des champs différents, tous harmoniques et passant par les mêmes vitesses de coins. **R3 définit une famille, paramétrée par le choix de base** ; l'implémentation devra fixer et documenter ce choix dans son contrat.

### 2.4 Champ total : discontinu aux frontières de niveaux

Sous quelque lecture que ce soit, [S2] définit Ũ par fonctions caractéristiques : le correctif ũ_i s'annule **brutalement** à l'extérieur de ω_i. Sauf coïncidence particulière, Ũ est discontinu à travers ∂ω_i, et la divergence au sens des distributions comprend un terme de saut :

$$
\nabla\cdot(\chi_{\omega_i}\, \tilde u_i) = \chi_{\omega_i}\, \nabla\cdot\tilde u_i + (\tilde u_i \cdot n)\, \delta_{\partial\omega_i}.
$$

La compatibilité garantie par la construction est donc un **bilan de flux nul par frontière de niveau** (version intégrée), pas une divergence ponctuelle du champ total. Toute formulation ultérieure (« divergence nulle comprise entre niveaux ») doit être lue en ce sens intégré ; l'affirmer ponctuellement à travers ∂ω_i serait inexact.

Conséquence pour le coût dirigé : le coût de polyligne intègre 1/|Ũ| le long du chemin ; les sauts de |Ũ| à travers les frontières de niveaux sont intégrables, sous réserve que la garde usuelle (vitesse minimale dans le coût) s'applique de part et d'autre — elle relève du coût, pas du champ.

### 2.5 Identité de masse et règle des quatre points

La règle des quatre points, correctement écrite ∫_ω f = (aire/4) · Σ f(q_j), est exacte pour les fonctions bilinéaires (itération de la règle du trapèze, exacte sur chaque variable). Elle est **inexacte en général** (erreur de quadrature) pour des champs non bilinéaires, et l'identité de masse de la section 1.5 hérite de cette limite : « la masse dans ω_i correspond à la quantité entrante » est exacte tant que c_i est bilinéaire et que le flux de bord est évalué de manière cohérente. C'est une propriété de la construction discrète, pas une conservation physique générale. La vérification complète de cette identité (flux de bord, conditions d'entrée) reste ouverte et relève du protocole de test, pas de cette note.

## 3. Conséquences pour les tests de l'issue #42

1. **Sous l'hypothèse bilinéaire R2**, un test de divergence du champ de niveau peut échouer mathématiquement (section 2.2) : ce résultat caractérise cette reconstruction et ne doit pas être extrapolé à une famille λ_j non spécifiée par la source.
2. **Sous R3**, la divergence ponctuelle d'un niveau est une identité de construction — comme pour les champs à fonction de courant de `champ_analytique.py`. Un test de divergence y vérifie l'implémentation (base, solveur aux coins, discrétisation), pas une propriété scientifique nouvelle. Les tests **informatifs** sont :
   - reproduction exacte des vitesses de coins, niveau par niveau ;
   - flux net nul à travers chaque ∂ω_i (le critère historique, version intégrée), y compris pour des coins issus d'un champ cisaillé ;
   - composition du champ total sur des rectangles emboîtés (évaluation par le niveau le plus fin contenant le point, fonctions caractéristiques correctes) ;
   - divergence ponctuelle par différences finies (contrôle d'implémentation) ;
   - comportement du coût de polyligne à travers une frontière de niveau (sauts intégrables, garde de vitesse minimale) ;
   - bilan de masse de la restriction de concentration [S4] avec sa règle des quatre points (section 2.5).
3. **Le test « divergence entre niveaux » au sens du champ total** doit être formulé en bilan de flux (section 2.4) : c'est ce que la construction garantit, et rien de plus.

## 4. Arbitrage requis avant implémentation

**Recommandation de cette note** (argumentée, à trancher par le propriétaire) : retenir **R3** — potentiel harmonique ajusté aux vitesses de coins — parce que R1 est sous-déterminée (section 2.1) et que la reconstruction bilinéaire R2 ne satisfait pas la garantie de flux annoncée (section 2.2). Cette recommandation reste une proposition de reconstruction, pas l'identification certaine de la méthode historique : la famille λ_j de la source n'est pas spécifiée. Conditions à fixer dans le contrat d'implémentation :

- base harmonique fixée et documentée (proposition : les huit polynômes harmoniques de degré au plus 4 listés en section 2.3, avec repli en moindres carrés si le système est singulier) ;
- rectangles homothétiques emboîtés, cascade du grossier vers le fin, pas de rétroaction fine → grossier (fidèle à la source) ;
- discontinuité aux frontières de niveaux assumée et documentée (section 2.4) ; garde de vitesse minimale inchangée côté coût ;
- périmètre 2D horizontal (le champ historique de la source est le vent horizontal ; la métrique du dépôt est 2D) ;
- **vérification préalable de la formulation sur les versions Applied Geomatics et JESA de 2009-2010** (dépendance de la section 0) : si la consolidation en cours révèle que la compatibilité aux coins porte sur les vitesses dans une version et sur les potentiels dans une autre, l'arbitrage devra en tenir compte.

## 5. Protocole d'implémentation proposé (TDD, charte qualité)

- **Phase A — décision** : arbitrage R3 et contrat (base, repli, invariants : rectangles emboîtés, ordre des coins, au moins deux niveaux).
- **Phase B — noyau typé** : dataclasses gelées (un niveau = rectangle + potentiel ou vitesses de coins validés ; champ multi-niveaux = liste ordonnée de niveaux, évaluation par le niveau le plus fin contenant le point, comportement hors cascade documenté) ; solveur harmonique aux coins isolé et testable ; NumPy seul, aucun dictionnaire interne non typé.
- **Phase C — tests GWT** : la liste de la section 3, tolérances calibrées numériquement avant poussée (leçon des notes 19 et 26).
- **Phase D — cartographie** : mise à jour de Contraintes physiques (sections 1 et 4), de la page qualité, et du graphe de connaissances, sans jamais transformer ces tests ciblés en certification générale.

## 6. Ce que l'implémentation débloquerait — et ce qui resterait ouvert

| Objet | Effet | Statut après implémentation |
|---|---|---|
| Divergence « du champ multi-niveaux » | test d'implémentation par niveau + bilan de flux par frontière | testé (portée exacte à écrire) |
| Conservation en champ variable | identité de masse [S4] à vérifier sous ses hypothèses exactes (section 2.5) | testable sous conditions ; pas une preuve générale |
| Adjoint en champ variable | champ lisse par niveau, gradients analytiques via la base harmonique ; la différentiabilité aux sauts de niveaux reste à traiter | structure favorable ; rien de revendiqué |
| Correction topographique Bernoulli-Newton | hors périmètre (section 2.2.1 de la source) | tranche séparée |
| Intégration SIG/QGIS | hors périmètre | différé (issue #43) |

## 7. Registre des statuts

| Affirmation | Statut | Fondement |
|---|---|---|
| Construction historique : cascade, [S2], restriction, [S3], identité de flux, [S4] | citation | extraction HAL du dépôt, section 2.1.1 |
| R1 sous-déterminée ; les potentiels aux coins ne fixent pas les vitesses de coins | démontré | section 2.1, calcul standard |
| Reconstruction bilinéaire R2 déterminée mais à divergence non nulle en général ; identité de flux non garantie sous R2 | démontré sous hypothèse bilinéaire | section 2.2, contre-exemple explicite |
| R3 à divergence ponctuelle nulle, flux net nul automatique | démontré | section 2.3, théorème de la divergence |
| R3 non unique entre bases harmoniques | démontré | section 2.3 |
| Champ total discontinu ; garantie = bilan de flux par niveau | démontré | section 2.4, calcul distributionnel |
| Règle des quatre points exacte pour les seules fonctions bilinéaires | démontré | section 2.5, quadrature |
| Identité de masse complète (flux de bord, conditions d'entrée) | ouvert | à vérifier dans le protocole de test |
| R3 est la lecture visée par la source | hypothèse de travail | cohérence argumentée (section 4) ; à confirmer par la consolidation des sources |
| Formulation identique dans les versions Applied Geomatics et JESA | non vérifié | dépendance de la section 0 |
