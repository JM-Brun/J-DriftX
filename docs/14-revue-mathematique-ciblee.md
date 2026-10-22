# Revue mathématique ciblée — temps de parcours de Drift-X

> **Statut :** revue ciblée de cadrage, non exhaustive. Elle compare les définitions présentes dans le dépôt aux familles mathématiques voisines. Elle ne certifie ni l'originalité de la formulation historique, ni ses résultats physiques : les sources historiques primaires doivent encore être relues équation par équation.

## 1. Question examinée

La page [Métrique travel-time](../site/theorie/metrique-travel-time.qmd) définit

\[
\tau(\mathbf{x}_0\to\mathbf{x})=\int_\gamma \frac{ds}{|\mathbf{u}(s)|},
\]

où \(\gamma\) est une ligne de courant. Elle associe à cette quantité la non-symétrie, la divergence du temps près des zones où \(|\mathbf u|\to0\), et une transformation de coordonnées liée à la conservation de masse.

La question préalable n'est pas « cette idée est-elle nouvelle ? », mais **quel objet mathématique est exactement défini, sur quel domaine, et quelles propriétés en découlent réellement ?**

## 2. Résultat central : distinguer trois problèmes

| Objet | Définition opérationnelle | Conséquence | Littérature à comparer |
|---|---|---|---|
| **Temps le long d'une ligne de courant** | Champ stationnaire donné; trajectoire imposée par \(\dot X=\mathbf u(X)\); intégrale \(\int ds/|\mathbf u|\) entre deux points appartenant à la même trajectoire orientée | Le temps est défini pour les points atteignables dans le sens de l'écoulement. Les autres couples sont hors domaine ou peuvent recevoir la valeur \(+\infty\) par convention explicite | Équations caractéristiques, transport advectif |
| **Temps minimal de navigation** | On peut choisir une commande/direction admissible et minimise le temps parmi les trajectoires réalisables | Le coût est une fonction valeur d'un problème de contrôle; vent/courant et vitesse propre interagissent | Navigation de Zermelo, métriques de Randers/Finsler |
| **Temps de première arrivée / propagation** | Une loi de vitesse et une règle de propagation déterminent une front d'arrivée | Souvent formulé par une équation eikonale ou Hamilton–Jacobi; dépend de la loi de propagation et de ses conditions | Eikonale anisotrope, Hamilton–Jacobi–Bellman |

Ces trois objets peuvent se ressembler mais ne sont pas interchangeables. Une intégrale le long d'une ligne de courant n'est pas automatiquement le temps minimal entre deux points, et le temps minimal d'un navigateur n'est pas le temps d'un traceur passif purement advecté.

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

Cette liste établit que le voisinage conceptuel est riche; elle **n'établit pas** que la contribution historique de Drift-X est redondante. Pour le savoir, il faut comparer ses équations et théorèmes précis aux sources originales, notamment la thèse de Brun (2006), le rapport CR Mécanique (2006) et le chapitre de Brun (2008) déjà cités dans la bibliographie du projet.

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
- **résultat établi par la revue** : plusieurs familles mathématiques voisines sont clairement pertinentes et la définition du dépôt exige une clarification;
- **non établi** : originalité de Drift-X, validité générale des propriétés annoncées, conservation exacte sous les hypothèses réellement implémentées, valeur applicative;
- **prochaine action discriminante** : retrouver les équations sources historiques et formaliser un modèle 1D qui correspond exactement à l'objet revendiqué.

## Références web consultées

- Gibbons et al. (2009), DOI [10.1103/PhysRevD.79.044022](https://doi.org/10.1103/PhysRevD.79.044022).
- Dušek (2018), DOI [10.17818/NM/2018/4SI.16](https://doi.org/10.17818/NM/2018/4SI.16).
- *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), DOI [10.1016/j.difgeo.2024.102177](https://doi.org/10.1016/j.difgeo.2024.102177).
- Markvorsen et al. (2025), [arXiv:2508.07274](https://arxiv.org/abs/2508.07274).
- Contreras & Kachroo (2020), DOI [10.1109/TITS.2019.2946109](https://doi.org/10.1109/TITS.2019.2946109).
- Sethian & Vladimirsky (2001), [Ordered upwind methods for static Hamilton–Jacobi equations](https://pmc.ncbi.nlm.nih.gov/articles/PMC58684/).
