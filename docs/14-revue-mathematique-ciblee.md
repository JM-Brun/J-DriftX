# Revue mathématique ciblée — temps de parcours de Drift-X

> **Statut :** revue ciblée de cadrage, non exhaustive. Elle compare les définitions présentes dans le dépôt aux familles mathématiques voisines. Elle ne certifie ni l'originalité de la formulation historique, ni ses résultats physiques : les sources historiques primaires doivent encore être relues équation par équation.

## 1. Question examinée

La page [Métrique travel-time](../site/theorie/metrique-travel-time.qmd) définit

\[
\tau(\mathbf{x}_0\to\mathbf{x})=\int_\gamma \frac{ds}{|\mathbf{u}(s)|},
\]

où \(\gamma\) est une ligne de courant. **Attention : cette formule ne restitue pas à elle seule toute la définition historique de la pseudo-distance.** L'article de 2006 définit le coût jusqu'à la projection \(B^\perp\) du point cible sur la caractéristique passant par le point de départ, et non nécessairement jusqu'au point cible lui-même. La différence est structurante et est détaillée en §2.1.

La question préalable n'est pas « cette idée est-elle nouvelle ? », mais **quel objet mathématique est exactement défini, sur quel domaine, et quelles propriétés en découlent réellement ?**

## 2. Résultat central : distinguer trois problèmes

| Objet | Définition opérationnelle | Conséquence | Littérature à comparer |
|---|---|---|---|
| **Temps le long d'une ligne de courant** | Champ stationnaire donné; trajectoire imposée par \(\dot X=\mathbf u(X)\); intégrale \(\int ds/|\mathbf u|\) entre deux points appartenant à la même trajectoire orientée | Le temps est défini pour les points atteignables dans le sens de l'écoulement. Les autres couples sont hors domaine ou peuvent recevoir la valeur \(+\infty\) par convention explicite | Équations caractéristiques, transport advectif |
| **Temps minimal de navigation** | On peut choisir une commande/direction admissible et minimise le temps parmi les trajectoires réalisables | Le coût est une fonction valeur d'un problème de contrôle; vent/courant et vitesse propre interagissent | Navigation de Zermelo, métriques de Randers/Finsler |
| **Temps de première arrivée / propagation** | Une loi de vitesse et une règle de propagation déterminent une front d'arrivée | Souvent formulé par une équation eikonale ou Hamilton–Jacobi; dépend de la loi de propagation et de ses conditions | Eikonale anisotrope, Hamilton–Jacobi–Bellman |

Ces trois objets peuvent se ressembler mais ne sont pas interchangeables. Une intégrale le long d'une ligne de courant n'est pas automatiquement le temps minimal entre deux points, et le temps minimal d'un navigateur n'est pas le temps d'un traceur passif purement advecté.

## 2.1 Lecture de la source primaire de 2006 : une clarification importante

La note de Mohammadi & Brun, *Similitude généralisée et modélisation géométrique à complexité réduite* (2006, §3, pp. 635–636, [DOI](https://doi.org/10.1016/j.crme.2006.06.007)), est accessible en texte intégral. Elle permet de préciser l'objet historique plus nettement que la seule formule intégrale donnée dans les pages actuelles du dépôt.

La construction historique ne définit pas simplement le temps d'une trajectoire jusqu'au point cible \(B\). Pour un point \(A\), elle considère la caractéristique passant par \(A\), projette \(B\) sur cette caractéristique en un point \(B^\perp\), puis définit le coût dirigé comme le temps de migration de \(A\) vers \(B^\perp\). Elle suppose la caractéristique unique et écarte les sources et puits; les cas où la projection n'est pas unique sont traités par un critère lié à \(\mathbf u\cdot\nabla c\).

La source appelle explicitement cette construction une **pseudo-distance** et précise qu'elle ne satisfait pas en général les propriétés d'une distance : elle peut vérifier \(d(A,B)=0\) sans \(A=B\), elle est non symétrique, et l'inégalité triangulaire peut échouer. Ces échecs ne sont donc pas simplement des lacunes de documentation dans la reprise : au moins pour la séparation et la triangulation, ils sont annoncés dans la formulation historique elle-même.

### Vérification complémentaire du chapitre de 2008

Le chapitre *Reduced-Order Modelling of Dispersion* est également disponible dans le volume Springer, pp. 245–256 ([texte du volume](https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf), §2.2, pp. 248–250). Il confirme la définition projetée, mais ajoute un détail qui change le statut de l'implémentation :

- la définition exacte utilise \(B^\perp\), projection euclidienne de \(B\) sur la caractéristique passant par \(A\);
- plus loin, la méthode numérique approxime \(B^\perp=B\), en indiquant que la caractéristique passant par \(A\) passe exactement par \(B\), ce qui est présenté comme peu probable en général;
- en champ uniforme, le chapitre introduit un facteur correctif \(2/\pi\) (noté dans le texte comme une moyenne cosinus stochastique) pour corriger le temps calculé sous cette approximation;
- la méthode est présentée comme satisfaisante pour des champs atmosphériques lisses et dans un contexte applicatif particulier, pas comme une construction sans restriction pour tout champ de vitesse.

Il faut donc séparer **la définition géométrique idéale** et **l'algorithme approché publié**. Reproduire seulement la projection exacte teste la définition; reproduire l'algorithme de 2008 demande également de documenter l'approximation \(B^\perp\approx B\), le facteur correctif, l'interpolation de la caractéristique et son domaine de validité.

Le chapitre formule aussi des contraintes de divergence nulle, d'advection, de positivité et de conservation pour les champs et les solutions réduites. Dans les passages examinés, cela ne remplace pas une preuve détaillée du résultat plus spécifique « le flux sur chaque surface iso-\(\tau\) restitue exactement \(Q\) ». Cette dernière affirmation doit être rattachée à une dérivation précise avant d'être conservée comme résultat démontré dans la documentation actuelle.

### Contre-exemple analytique minimal : champ uniforme

Prenons le champ 2D uniforme \(\mathbf u=(U,0)\), avec \(U>0\), et les points \(A=(x_A,y_A)\), \(B=(x_B,y_B)\). La caractéristique passant par \(A\) est horizontale. La projection normale décrite dans l'article donne \(B^\perp=(x_B,y_A)\). Pour \(x_B\ge x_A\), le coût historique devient

\[
d(A,B)=\frac{x_B-x_A}{U}.
\]

Le coût ne dépend pas de \(y_B-y_A\). Ainsi, pour \(B=(x_A,y_B)\) avec \(y_B\ne y_A\), on obtient \(d(A,B)=0\) alors que \(A\ne B\). Ce n'est pas un paradoxe : la construction mesure un avancement le long de la caractéristique de \(A\), et non une distance complète jusqu'à \(B\).

Pour ce champ uniforme, cette expression satisfait l'inégalité triangulaire dans la direction admissible lorsque les abscisses sont ordonnées, mais cela ne prouve pas la propriété pour des champs non uniformes avec projections multiples ou géométrie plus complexe. L'article avertit explicitement que la triangulation peut être mise en défaut dans la construction générale.

### Conséquence pour le vocabulaire et le MVP

- Conserver le terme historique **pseudo-distance de transport** lorsque l'on parle de la construction de 2006.
- Ne pas la confondre avec le simple temps d'arrivée à \(B\), ni avec une distance de navigation obtenue par minimisation.
- Distinguer le temps le long de la caractéristique, la projection \(B^\perp\), le coût étendu en cas d'inaccessibilité et le modèle de concentration construit ensuite.
- Le premier test 1D/2D doit reproduire cette définition historique avant de tester une variante plus intuitive. Sinon, il teste un nouveau modèle et non la formulation publiée.

## 3. Ce que les définitions actuelles permettent — et ne permettent pas — d'affirmer

### 3.1 La non-uniformité du champ ne suffit pas à établir la non-symétrie

Pour une **même courbe géométrique** parcourue dans les deux sens avec la même vitesse scalaire positive \(v(s)\), l'intégrale de longueur de temps \(\int ds/v(s)\) est identique dans les deux sens. La variation spatiale de la vitesse, à elle seule, ne rend donc pas cette intégrale asymétrique.

Dans un champ vectoriel d'advection, l'asymétrie peut venir du fait que la dynamique impose un sens de parcours : l'inverse d'une ligne de courant n'est généralement pas une trajectoire admissible du même champ. On doit alors définir explicitement le temps inverse comme **non défini**, **inaccessible** ou \(+\infty\), plutôt que déduire cette valeur de la seule non-uniformité du champ.

Un exemple 1D suffit à le montrer : pour \(\dot x=u(x)>0\), le temps de \(a\) vers \(b>a\) vaut \(\int_a^b dx/u(x)\). Le mouvement inverse n'est pas une solution de cette même dynamique. Si l'on introduit plutôt une vitesse de retour positive, on a défini une autre dynamique; si on autorise un contrôle de direction, on a défini un problème de navigation.

### 3.2 Les singularités près d'une stagnation demandent une hypothèse locale

L'intégrande \(1/|\mathbf u|\) devient singulier lorsque la vitesse tend vers zéro. Cela ne suffit pas à conclure, sans hypothèses sur le champ et sur la trajectoire, que toute intégrale de temps diverge : il faut examiner le comportement local de \(|\mathbf u|\) et la manière dont la trajectoire approche la zone. Le dépôt doit préciser si une stagnation est exclue du domaine, si le temps est infini, ou si un modèle physique différent prend le relais.

### 3.3 « Métrique » est un terme à justifier

Une métrique usuelle est finie et satisfait notamment séparation, symétrie et inégalité triangulaire. Une distance asymétrique ou quasi-distance peut relâcher la symétrie, mais ses axiomes doivent être énoncés. Une fonction étendue qui vaut \(+\infty\) pour des points inaccessibles ne doit pas être appelée sans qualification une métrique finie. Il faut vérifier séparément :
- le domaine de définition et la relation d'accessibilité;
- \(\tau(x,x)=0\) et la positivité pour les couples admissibles;
- la séparation des points distincts;
- l'inégalité triangulaire dirigée, quand les trois segments sont admissibles;
- la régularité et le comportement aux points critiques.

### 3.4 La conservation de masse est une affirmation distincte

La conservation de masse ne découle pas de la seule définition de \(\tau\). Elle dépend de l'équation de transport, de la divergence du champ, des sources/puits, des conditions aux limites et du jacobien de la transformation de coordonnées. La revendication historique selon laquelle un flux intégré sur une surface iso-\(\tau\) restitue exactement \(Q\) doit être reliée à une dérivation complète et à ses hypothèses, et non considérée comme démontrée par la définition de temps de parcours.

## 4. Comparaison ciblée avec les antécédents

| Référence | Objet et proximité avec J-DriftX | Différence à établir avant toute revendication |
|---|---|---|
| Gibbons et al. (2009), [*Stationary metrics and optical Zermelo-Randers-Finsler geometry*](https://doi.org/10.1103/PhysRevD.79.044022) | Lien entre navigation de Zermelo et géométrie de Randers/Finsler; temps minimal dans un champ de vent/courant | Le navigateur garde une vitesse propre et choisit sa direction; un traceur passif advecté suit le champ. La limite de vitesse propre nulle n'est pas automatiquement une métrique de Randers régulière |
| Dušek (2018), [*Zermelo Navigation Problem in Geometry*](https://doi.org/10.17818/NM/2018/4SI.16) | Formulation géométrique du problème de navigation et des métriques de Randers | Établir si J-DriftX optimise sur des trajectoires contrôlables ou intègre une trajectoire imposée |
| *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), [DOI](https://doi.org/10.1016/j.difgeo.2024.102177) | Navigation à temps minimal avec contraintes et obstacles mobiles | Pertinent seulement si J-DriftX inclut un choix de chemin/contrôle et des contraintes comparables |
| Markvorsen, Pendás-Recondo & Rygaard (2025), [*Time-dependent Zermelo navigation with tacking*](https://arxiv.org/abs/2508.07274) | Navigation dépendant du temps, changement de stratégie de cap | À comparer si le modèle évolue vers des champs temporels et une optimisation de trajectoire |
| Contreras & Kachroo (2020), [*The Viscosity Solution for Hamilton Jacobi Travel Time Dynamics*](https://doi.org/10.1109/TITS.2019.2946109) | Équation de temps de parcours de type Hamilton–Jacobi et solution de viscosité | Application au trafic/LWR : analogue méthodologique, pas la même dynamique physique |
| Sethian & Vladimirsky (2001), [*Ordered upwind methods for static Hamilton–Jacobi equations*](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/) | Problèmes de temps minimal anisotrope et équations Hamilton–Jacobi–Bellman | Pertinent si le temps est un minimum sur un ensemble de directions et si un solveur de front est envisagé |

Cette liste établit que le voisinage conceptuel est riche; elle **n'établit pas** que la contribution historique de Drift-X est redondante. Les sections pertinentes du rapport CR Mécanique (2006) et du chapitre Springer de 2008 ont maintenant été lues. La thèse elle-même n'a pas encore été examinée; sa date bibliographique reste incohérente entre les références consultées.

## 5. Décision scientifique pour le MVP

Le cas 1D à deux vitesses constantes proposé dans la fiche MVP est utile pour tester des propriétés élémentaires, mais il **ne doit pas être présenté comme une réduction démontrée du modèle de ligne de courant historique**. Il définit par construction deux directions et deux vitesses, donc un autre modèle jouet.

Ordre recommandé :

1. **Geler la définition cible** : champ stationnaire ou temporel, trajectoire imposée ou contrôlée, couples accessibles, traitement de l'inaccessibilité, unités et conditions aux limites.
2. **Séparer les affirmations** : propriétés de l'intégrale sur une trajectoire; propriétés de la fonction de coût sur des paires de points; conservation de masse; conséquences pour les solutions de similitude.
3. **Reproduire un cas 1D issu de la définition retenue**, puis calculer indépendamment l'intégrale et tester les propriétés annoncées.
4. **Relire les sources historiques primaires** et tracer chaque formule ou théorème à sa source.
5. Seulement ensuite, décider si un solveur 2D synthétique répond à une question non résolue.

### Conclusion provisoire

Le risque le plus immédiat n'est pas simplement que « Zermelo existe déjà ». C'est que le dépôt emploie le même vocabulaire de temps de parcours pour des objets différents : intégrale advective le long d'une caractéristique, coût asymétrique sur des paires de points, et temps minimal de navigation. Leur relation doit être démontrée plutôt que supposée.

À ce stade :
- **résultat établi par la revue** : le texte primaire de 2006 définit une pseudo-distance fondée sur la projection sur une caractéristique, et annonce explicitement la perte de séparation et l'échec possible de l'inégalité triangulaire; plusieurs familles mathématiques voisines sont pertinentes;
- **non établi** : originalité de Drift-X, validité générale des propriétés annoncées, conservation exacte sous les hypothèses réellement implémentées, valeur applicative;
- **prochaine action discriminante** : lire la thèse de 2007 et le chapitre de 2008, puis implémenter un test de référence du champ uniforme reproduisant la projection (B^\perp), avec tests sur (d(A,B)=0) pour des points distincts et sur l'accessibilité orientée.

### Écart entre la source historique et le code actuel

L'audit de la fonction `jdriftx.metric.temps_transport` révèle un verrou supplémentaire : elle calcule \(\sum_i |L_i|/\|\mathbf u_i\|\) sur une polyligne fournie. Elle ne calcule pas les caractéristiques du champ, n'effectue pas la projection \(B^\perp\), et ne dépend que de la norme des vecteurs vitesse. Les tests précédents nommaient à tort certains cas « non-symétrie », alors qu'ils démontraient soit l'égalité sous inversion, soit l'effet de la longueur du chemin.

La PR corrige les docstrings et les noms de tests pour que les tests décrivent la primitive réellement implémentée. Elle ajoute aussi `pseudo_distance_uniforme`, une référence analytique limitée aux champs uniformes 2D, avec tests de projection longitudinale, coût nul transversal, coût infini en amont, rotation et vitesse nulle. Cette fonction n'est pas une implémentation générale : elle ne résout pas les caractéristiques d'un champ variable et ne reproduit pas les approximations numériques de 2008.

## 6. Registre des incertitudes après cette lecture

| Point | État après lecture du rapport 2006 | Ce qui reste nécessaire pour le lever |
|---|---|---|
| Implémentation Python actuelle | **Écart désormais explicite** : la fonction est un coût de polyligne qui ignore l'orientation et la projection historique | Étendre la référence seulement après avoir spécifié les caractéristiques et cas limites des champs variables; conserver la primitive de polyligne comme API distincte |
| Définition historique | **Partiellement levé** : la projection \(B\mapsto B^\perp\) et le statut de pseudo-distance sont explicités au §3 | Lire la thèse et le chapitre de 2008 pour vérifier la cohérence des variantes et les extensions proposées |
| Domaine de validité | **Partiellement levé** : l'article suppose une caractéristique unique et écarte sources/puits | Définir précisément le traitement des séparatrices, stagnations, caractéristiques multiples et limites du domaine |
| Séparation des points | **Levé pour la construction publiée** : la source reconnaît que \(d(A,B)=0\) n'implique pas \(A=B\) | Ajouter un test analytique de reproduction; ne pas présenter cette propriété comme un défaut nouvellement découvert |
| Inégalité triangulaire | **Levé au niveau de l'affirmation historique** : la source dit qu'elle peut échouer | Trouver ou construire un contre-exemple explicite à partir de la définition exacte avant d'écrire un test de non-régression |
| Non-symétrie | **Partiellement levé** : la définition est orientée et fixe \(+\infty\) pour certains couples amont/aval | Formaliser la convention de domaine et distinguer coût non défini, coût étendu \(+\infty\), et trajet physiquement impossible |
| Conservation de masse | **Non levé** : les sources imposent des contraintes de conservation au modèle réduit, mais les passages lus ne démontrent pas le résultat plus précis de conservation exacte du flux sur chaque surface iso-\(\tau\) | Reconstituer le jacobien, les hypothèses sur \(\nabla\cdot\mathbf u\), les frontières et le lien avec le scalaire \(c\) dans la thèse/chapitre |
| Originalité | **Non levé** : un article de 2006 décrit déjà la pseudo-distance et son usage pour les solutions de similitude | Comparer les équations et résultats spécifiques, sans revendiquer la pseudo-distance elle-même comme nouvelle |
| Date de la thèse | **Métadonnées incohérentes** : la bibliographie du dépôt indique 2006, alors que l'article de 2006 cite la thèse comme 2007 | Vérifier la page de titre ou le dépôt institutionnel de la thèse avant de normaliser la référence |

### Prochaine action à plus forte valeur

Ne pas lancer encore un solveur 2D. Reproduire d'abord la pseudo-distance historique dans le champ uniforme, avec cas de test calculés à la main. En parallèle, obtenir et lire la thèse de Brun et le chapitre de 2008 pour formaliser la conservation de masse et vérifier si les sources développent ou modifient la définition du rapport de 2006. Si la source primaire complète n'est pas accessible, documenter cette limite plutôt que combler les lacunes par inférence.

## Références web consultées

- Gibbons et al. (2009), DOI [10.1103/PhysRevD.79.044022](https://doi.org/10.1103/PhysRevD.79.044022).
- Dušek (2018), DOI [10.17818/NM/2018/4SI.16](https://doi.org/10.17818/NM/2018/4SI.16).
- *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), DOI [10.1016/j.difgeo.2024.102177](https://doi.org/10.1016/j.difgeo.2024.102177).
- Markvorsen et al. (2025), [arXiv:2508.07274](https://arxiv.org/abs/2508.07274).
- Contreras & Kachroo (2020), DOI [10.1109/TITS.2019.2946109](https://doi.org/10.1109/TITS.2019.2946109).
- Sethian & Vladimirsky (2001), [Ordered upwind methods for static Hamilton–Jacobi equations](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/).
