# Revue mathématique ciblée — temps de parcours de Drift-X

> **Statut :** revue mathématique ciblée, non exhaustive. Les passages pertinents de l'article de 2006 et du chapitre de 2008 ont été consultés ; la thèse n'est pas disponible dans le projet et sera examinée après son ajout ultérieur par l'utilisateur. Cette note distingue les définitions rapportées par les sources, les déductions analytiques vérifiables et les questions physiques ou numériques encore ouvertes. Elle ne certifie ni l'originalité de la formulation historique ni sa validité applicative.

> **Guide de lecture.** Une *définition* fixe l'objet étudié; une *hypothèse* précise quand il est défini; une *proposition démontrée* découle de ces éléments; une *illustration* aide à l'interpréter sans constituer une validation physique.

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

### Vocabulaire minimal de mécanique des fluides

- **Champ de vitesse** \(\mathbf u(\mathbf x,t)\): vecteur vitesse du fluide en chaque position et instant; son unité SI est le m·s⁻¹.
- **Ligne de courant** (*streamline*): courbe tangente au champ de vitesse à un instant fixé.
- **Trajectoire de particule** (*pathline*): chemin réellement suivi au cours du temps par une particule fluide, solution de \(\dot X(t)=\mathbf u(X(t),t)\).
- **Caractéristique**: courbe utilisée pour suivre l'information d'une équation de transport. Pour un champ de vitesse stationnaire suffisamment régulier, ses courbes spatiales coïncident avec les lignes de courant et les trajectoires spatiales. Dans un champ instationnaire, ces notions ne doivent pas être confondues.
- **Divergence** \(\nabla\cdot\mathbf u\): mesure locale du taux de dilatation volumique du champ. \(\nabla\cdot\mathbf u=0\) signifie un champ incompressible au sens cinématique; pour un fluide de densité constante, cela correspond à la continuité locale sans source volumique. Ce n'est pas, à lui seul, une preuve de conservation d'un flux sur une surface arbitraire.
- **Source/puits**: région où la quantité transportée est injectée ou retirée, ou point singulier du champ selon le modèle. Il faut préciser si l'on parle d'une source de fluide, d'une source de polluant ou d'une singularité mathématique : ces notions ne sont pas synonymes.
- **Stagnation**: point où \(\mathbf u=0\). L'intégrande \(1/\|\mathbf u\|\) y est singulier; la convergence de l'intégrale dépend du comportement local de la vitesse et de la trajectoire.

Dans la suite, sauf mention contraire, le contre-exemple est stationnaire et bidimensionnel. Les coordonnées et les vitesses sont **adimensionnées** pour éviter de mélanger des unités dans la formule \(u_x=1+9y\).

## 2.1 Lecture de la source primaire de 2006 : une clarification importante

La note de Mohammadi & Brun, *Similitude généralisée et modélisation géométrique à complexité réduite* (2006, §3, pp. 635–636, [DOI](https://doi.org/10.1016/j.crme.2006.06.007)), est accessible en texte intégral. Elle permet de préciser l'objet historique plus nettement que la seule formule intégrale donnée dans les pages actuelles du dépôt.

La construction historique ne définit pas simplement le temps d'une trajectoire jusqu'au point cible \(B\). Pour un point \(A\), elle considère la caractéristique passant par \(A\), projette \(B\) sur cette caractéristique en un point \(B^\perp\), puis définit le coût dirigé comme le temps de migration de \(A\) vers \(B^\perp\). Elle suppose la caractéristique unique et écarte les sources et puits; les cas où la projection n'est pas unique sont traités dans la source par un critère lié à \(\mathbf u\cdot\nabla c\), c'est-à-dire à la dérivée directionnelle de la concentration le long du champ de vitesse. Cette phrase explique la notation, mais ne reconstitue pas le critère complet : ses hypothèses et son rôle exact restent à vérifier dans le passage source.

La source appelle explicitement cette construction une **pseudo-distance** et précise qu'elle ne satisfait pas en général les propriétés d'une distance : elle peut vérifier \(d(A,B)=0\) sans \(A=B\), elle est non symétrique, et l'inégalité triangulaire peut échouer. Ces échecs ne sont donc pas simplement des lacunes de documentation dans la reprise : au moins pour la séparation et la triangulation, ils sont annoncés dans la formulation historique elle-même.

### Vérification complémentaire du chapitre de 2008

Le chapitre *Reduced-Order Modelling of Dispersion* est également disponible dans le volume Springer, pp. 245–256 ([texte du volume](https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf), §2.2, pp. 248–250). Il confirme la définition projetée, mais ajoute un détail qui change le statut de l'implémentation :

- la définition exacte utilise \(B^\perp\), projection euclidienne de \(B\) sur la caractéristique passant par \(A\);
- plus loin, la méthode numérique approxime \(B^\perp=B\), en indiquant que la caractéristique passant par \(A\) passe exactement par \(B\), ce qui est présenté comme peu probable en général;
- en champ uniforme, le chapitre introduit un facteur correctif \(2/\pi\) (noté dans le texte comme une moyenne cosinus stochastique) pour corriger le temps calculé sous cette approximation;
- la méthode est présentée comme satisfaisante pour des champs atmosphériques lisses et dans un contexte applicatif particulier, pas comme une construction sans restriction pour tout champ de vitesse.

Il faut donc séparer **la définition géométrique idéale** et **l'algorithme approché publié**. Reproduire seulement la projection exacte teste la définition; reproduire l'algorithme de 2008 demande également de documenter l'approximation \(B^\perp\approx B\), le facteur correctif, l'interpolation de la caractéristique et son domaine de validité.

Le chapitre formule aussi des contraintes de divergence nulle, d'advection, de positivité et de conservation pour les champs et les solutions réduites. Dans les passages examinés, cela ne remplace pas une preuve détaillée du résultat plus spécifique « le flux sur chaque surface iso-\(\tau\) restitue exactement \(Q\) ». Cette dernière affirmation doit être rattachée à une dérivation précise avant d'être conservée comme résultat démontré dans la documentation actuelle.

### Schéma de la construction et du contre-exemple

Le schéma ci-dessous sépare la projection utilisée par la définition historique du mécanisme responsable de l'échec de l'inégalité triangulaire. Les flèches sont qualitatives; elles ne représentent pas une simulation numérique.

![À gauche : projection du point B sur la caractéristique issue de A. À droite : champ horizontal plus rapide à y=1 et trois points donnant une violation de l'inégalité triangulaire.](../site/images/pseudo-distance-projection-et-triangulation.svg)

### Contre-exemple analytique minimal : champ uniforme

Prenons le champ 2D uniforme \(\mathbf u=(U,0)\), avec \(U>0\), et les points \(A=(x_A,y_A)\), \(B=(x_B,y_B)\). La caractéristique passant par \(A\) est horizontale. La projection normale décrite dans l'article donne \(B^\perp=(x_B,y_A)\). Pour \(x_B\ge x_A\), le coût historique devient

\[
d(A,B)=\frac{x_B-x_A}{U}.
\]

Le coût ne dépend pas de \(y_B-y_A\). Ainsi, pour \(B=(x_A,y_B)\) avec \(y_B\ne y_A\), on obtient \(d(A,B)=0\) alors que \(A\ne B\). Ce n'est pas un paradoxe : la construction mesure un avancement le long de la caractéristique de \(A\), et non une distance complète jusqu'à \(B\).

Pour ce champ uniforme, cette expression satisfait l'inégalité triangulaire dans la direction admissible lorsque les abscisses sont ordonnées, mais cela ne prouve pas la propriété pour des champs non uniformes avec projections multiples ou géométrie plus complexe. L'article avertit explicitement que la triangulation peut être mise en défaut dans la construction générale.

### Contre-exemple explicite à l'inégalité triangulaire

La source de 2006 affirme que l'inégalité triangulaire peut échouer. On peut le vérifier sur un champ analytique simple, sans sources ni puits :

\[
\mathbf u(x,y)=(1+9y,\,0),\qquad (x,y)\in\mathbb R\times[0,1].
\]

Ce champ est stationnaire, strictement dirigé vers \(+x\), sans divergence (\(\nabla\cdot\mathbf u=0\)); ses caractéristiques sont les droites horizontales. Avec la définition historique projetée, pour un déplacement vers l'aval,

\[
d(A,B)=\frac{x_B-x_A}{1+9y_A}.
\]

Choisissons \(A=(0,0)\), \(B=(1,1)\) et \(C=(2,0)\). Alors

\[
d(A,C)=2,\qquad d(A,B)=1,\qquad d(B,C)=\frac{1}{10},
\]

d'où \(d(A,C)=2>1+\frac{1}{10}=d(A,B)+d(B,C)\). L'inégalité triangulaire échoue donc même pour un champ lisse, divergence nulle et sans singularité dans le domaine considéré. Le mécanisme est géométrique : \(d(A,C)\) mesure la progression sur la caractéristique de \(A\), tandis que \(d(B,C)\) mesure la progression sur celle de \(B\), où la vitesse est plus élevée.

Ce contre-exemple confirme que la construction est une pseudo-distance directionnelle, et non une distance asymétrique satisfaisant automatiquement l'inégalité triangulaire.

### Conséquence pour le vocabulaire et le MVP

- Conserver le terme historique **pseudo-distance de transport** lorsque l'on parle de la construction de 2006.
- Ne pas la confondre avec le simple temps d'arrivée à \(B\), ni avec une distance de navigation obtenue par minimisation.
- Distinguer le temps le long de la caractéristique, la projection \(B^\perp\), le coût étendu en cas d'inaccessibilité et le modèle de concentration construit ensuite.
- Le test de référence uniforme est maintenant implémenté séparément. Toute variante plus intuitive doit conserver un nom et des tests distincts; elle ne constitue pas une reproduction de la formulation publiée.

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
| *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), [DOI](https://doi.org/10.1016/j.difgeo.2024.102177) | Navigation à temps minimal avec contraintes et obstacles mobiles | Comparateur si J-DriftX introduit un choix de trajectoire/contrôle et des contraintes comparables; cet article n'établit rien sur la pseudo-distance projetée en advection pure |
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
- **prochaine action discriminante hors thèse** : traduire le contre-exemple de triangulation en test de référence lorsque l'API de champ variable sera spécifiée et formaliser la preuve de conservation à partir des sources déjà disponibles. L'examen de la thèse est différé jusqu'à son ajout ultérieur par l'utilisateur ; le cas uniforme analytique est déjà implémenté et testé.

### Écart entre la source historique et le code actuel

L'audit de la fonction `jdriftx.metric.temps_transport` révèle un verrou supplémentaire : elle calcule \(\sum_i |L_i|/\|\mathbf u_i\|\) sur une polyligne fournie. Elle ne calcule pas les caractéristiques du champ, n'effectue pas la projection \(B^\perp\), et ne dépend que de la norme des vecteurs vitesse. Les tests précédents nommaient à tort certains cas « non-symétrie », alors qu'ils démontraient soit l'égalité sous inversion, soit l'effet de la longueur du chemin.

La PR corrige les docstrings et les noms de tests pour que les tests décrivent la primitive réellement implémentée. Elle ajoute aussi `pseudo_distance_uniforme`, une référence analytique limitée aux champs uniformes 2D, avec tests de projection longitudinale, coût nul transversal, coût infini en amont, rotation et vitesse nulle. Cette fonction n'est pas une implémentation générale : elle ne résout pas les caractéristiques d'un champ variable et ne reproduit pas les approximations numériques de 2008.

## 6. Références et rôle de chaque source

Les liens ci-dessous pointent vers les documents cités; les pages indiquées précisent où se trouve le résultat mobilisé. Les références de navigation sont des comparateurs conceptuels, pas des preuves directes sur Drift-X.

| Référence | Type et emplacement utile | Ce qui est utilisé ici | Ce qu'elle ne prouve pas pour J-DriftX |
|---|---|---|---|
| Mohammadi & Brun (2006), [*Similitude généralisée et modélisation géométrique à complexité réduite*](https://doi.org/10.1016/j.crme.2006.06.007), *Comptes Rendus Mécanique*, 334(10), 634–638 | Source primaire; §3, pp. 635–636 | Définition projetée de la pseudo-distance et limites concernant séparation et triangulation | Validité de toutes les variantes numériques, conservation iso-τ complète ou originalité actuelle |
| Brun & Mohammadi (2008), [*Reduced-Order Modelling of Dispersion*](https://doi.org/10.1007/978-1-4020-8758-5_14), dans *Partial Differential Equations: Modelling and Numerical Simulation*, Springer, pp. 245–256 | Chapitre de synthèse; §2.2, pp. 248–250 | Distinction entre définition géométrique, approximation (B^\perp\approx B) et correction en champ uniforme | Une preuve indépendante de chaque propriété physique annoncée |
| Gibbons et al. (2009), [*Stationary metrics and optical Zermelo-Randers-Finsler geometry*](https://doi.org/10.1103/PhysRevD.79.044022) | Géométrie de navigation | Relation entre navigation contrôlée et géométrie de Randers/Finsler | Équivalence à l'advection pure d'un traceur passif |
| Dušek (2018), [*Zermelo Navigation Problem in Geometry*](https://doi.org/10.17818/NM/2018/4SI.16) | Présentation géométrique | Vocabulaire et formulation du problème de navigation | La définition historique projetée de Drift-X |
| Contreras & Kachroo (2020), [*The Viscosity Solution for Hamilton Jacobi Travel Time Dynamics*](https://doi.org/10.1109/TITS.2019.2946109) | Temps de parcours/Hamilton–Jacobi, contexte trafic | Comparaison avec les fonctions de temps d'arrivée définies par une équation | Même dynamique physique ou même observable que la dispersion atmosphérique |
| Sethian & Vladimirsky (2001), [*Ordered upwind methods for static Hamilton–Jacobi equations*](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/) | Méthode numérique pour Hamilton–Jacobi | Référence éventuelle si un problème de temps minimal est retenu | Justification d'un solveur pour la définition projetée sans analyse préalable |

### Comment relier ces notions à la physique

Pour un traceur passif sans diffusion, l'équation d'advection s'écrit, sous forme conservative, \(\partial_t c+\nabla\cdot(c\mathbf u)=s\), où \(c\) est la concentration et \(s\) un terme source. Si \(\nabla\cdot\mathbf u=0\), elle se réduit à \(\partial_t c+\mathbf u\cdot\nabla c=s\). Le long d'une trajectoire, la dérivée matérielle est \(Dc/Dt=\partial_t c+\mathbf u\cdot\nabla c\). Ces identités expliquent pourquoi les caractéristiques sont naturelles pour l'advection; elles ne suffisent cependant pas à transformer la pseudo-distance projetée en solution de l'équation de concentration. Il faut encore spécifier la source, les conditions initiales/aux limites et les hypothèses de réduction.

De même, \(\nabla\cdot\mathbf u=0\) contraint la cinématique du champ, mais la conservation du débit \(Q\) à travers une surface dépend aussi de la surface traversée, de son orientation, des sources/puits et du théorème de transport adapté. La conservation sur une surface iso-\(\tau\) doit donc être démontrée à partir de la transformation de coordonnées et de son jacobien, et non déduite du seul mot « divergence nulle ».

## 7. Registre des incertitudes après cette lecture

| Point | État après lecture du rapport 2006 | Ce qui reste nécessaire pour le lever |
|---|---|---|
| Implémentation Python actuelle | **Écart désormais explicite** : la fonction est un coût de polyligne qui ignore l'orientation et la projection historique | Étendre la référence seulement après avoir spécifié les caractéristiques et cas limites des champs variables; conserver la primitive de polyligne comme API distincte |
| Définition historique | **Partiellement levé** : la projection \(B\mapsto B^\perp\) et le statut de pseudo-distance sont explicités au §3 | Lire la thèse et le chapitre de 2008 pour vérifier la cohérence des variantes et les extensions proposées |
| Domaine de validité | **Partiellement levé** : l'article suppose une caractéristique unique et écarte sources/puits | Définir précisément le traitement des séparatrices, stagnations, caractéristiques multiples et limites du domaine |
| Séparation des points | **Levé pour la construction publiée** : la source reconnaît que \(d(A,B)=0\) n'implique pas \(A=B\) | Ajouter un test analytique de reproduction; ne pas présenter cette propriété comme un défaut nouvellement découvert |
| Inégalité triangulaire | **Levé pour un cas analytique** : le champ divergence nulle \(\mathbf u=(1+9y,0)\) et trois points donnent \(d(A,C)=2>d(A,B)+d(B,C)=1.1\) | Traduire ce cas en test de référence quand l'API de champ variable sera spécifiée |
| Non-symétrie | **Partiellement levé** : la définition est orientée et fixe \(+\infty\) pour certains couples amont/aval | Formaliser la convention de domaine et distinguer coût non défini, coût étendu \(+\infty\), et trajet physiquement impossible |
| Conservation de masse | **Non levé** : les sources imposent des contraintes de conservation au modèle réduit, mais les passages lus ne démontrent pas le résultat plus précis de conservation exacte du flux sur chaque surface iso-\(\tau\) | Reconstituer le jacobien, les hypothèses sur \(\nabla\cdot\mathbf u\), les frontières et le lien avec le scalaire \(c\) dans la thèse/chapitre |
| Originalité | **Non levé** : un article de 2006 décrit déjà la pseudo-distance et son usage pour les solutions de similitude | Comparer les équations et résultats spécifiques, sans revendiquer la pseudo-distance elle-même comme nouvelle |
| Filiation avec les métriques d'adaptation de maillage | **Non établie** : une référence sur la génération de maillages anisotropes ne prouve pas une filiation directe avec la pseudo-distance travel-time | Trouver une source historique explicite ou présenter le rapprochement uniquement comme analogie conceptuelle |
| Date de la thèse | **Métadonnées incohérentes** : la bibliographie du dépôt indique 2006, alors que l'article de 2006 cite la thèse comme 2007 | Vérifier la page de titre ou le dépôt institutionnel de la thèse avant de normaliser la référence |

### Prochaine action à plus forte valeur

Ne pas lancer encore un solveur 2D. Reproduire d'abord la pseudo-distance historique dans le champ uniforme, avec cas de test calculés à la main. En parallèle, formaliser la conservation de masse à partir des sources déjà disponibles. L'examen de la thèse de Brun est différé jusqu'à son ajout ultérieur au projet ; le chapitre de 2008 reste une source complémentaire à consulter au-delà des pages déjà extraites. Si la source primaire complète n'est pas accessible, documenter cette limite plutôt que combler les lacunes par inférence.

## Références web consultées

- Gibbons et al. (2009), DOI [10.1103/PhysRevD.79.044022](https://doi.org/10.1103/PhysRevD.79.044022).
- Dušek (2018), DOI [10.17818/NM/2018/4SI.16](https://doi.org/10.17818/NM/2018/4SI.16).
- *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), DOI [10.1016/j.difgeo.2024.102177](https://doi.org/10.1016/j.difgeo.2024.102177).
- Markvorsen et al. (2025), [arXiv:2508.07274](https://arxiv.org/abs/2508.07274).
- Contreras & Kachroo (2020), DOI [10.1109/TITS.2019.2946109](https://doi.org/10.1109/TITS.2019.2946109).
- Sethian & Vladimirsky (2001), [Ordered upwind methods for static Hamilton–Jacobi equations](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/).
