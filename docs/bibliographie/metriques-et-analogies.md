# Métriques, temps de transport et analogies conceptuelles

## Question centrale

J-DriftX utilise historiquement une pseudo-distance directionnelle liée au temps de transport le long des caractéristiques d'un champ de vitesse. Pour comprendre sa place mathématique, il faut distinguer : métrique mathématique au sens strict, distance de temps de trajet, métrique anisotrope utilisée en calcul scientifique et pseudo-distance directionnelle du modèle. Ces notions sont apparentées, mais ne sont pas automatiquement équivalentes.

### Muller (1979) — « La cartographie d'une métrique non euclidienne : les distances-temps »

- **Relation :** analogie conceptuelle dans un autre domaine, la géographie.
- **Idée commune :** représenter la proximité par un temps de déplacement et construire des isochrones plutôt que s'appuyer uniquement sur une distance euclidienne.
- **Intérêt pour J-DriftX :** vocabulaire et intuition sur les espaces dont la notion de distance dépend du processus de déplacement.
- **Limite :** le domaine, les hypothèses et la définition mathématique diffèrent potentiellement ; cette référence ne prouve pas que la pseudo-distance Drift-X possède les propriétés d'une métrique.
- [Article](https://www.persee.fr/doc/spgeo_0046-2497_1979_num_8_3_1915)

### Borouchaki et al. (1997) — *Delaunay mesh generation governed by metric specifications. Part I: Algorithms*

- **Relation :** parenté mathématique/numérique avec les métriques anisotropes utilisées pour contrôler l'adaptation de maillage.
- **Idée commune :** une géométrie locale variable permet de décrire des notions de proximité qui ne sont pas euclidiennes.
- **Différence :** une métrique de maillage symétrique et définie positive n'est pas la pseudo-distance directionnelle de Drift-X, qui dépend de l'orientation amont/aval et des caractéristiques.
- **Intérêt :** éclairer la généalogie mathématique, les notations et les conditions de validité, pas fournir une preuve directe du modèle de dispersion.
- [Article](https://doi.org/10.1016/S0168-874X(96)00057-1)

### Trindade da Silva et al. (2021) — dispersion atmosphérique et urbanisme

- **Relation :** analogie conceptuelle dans la représentation géométrique : typologie de blocs pour modéliser les villes dans les études de dispersion, approche interdisciplinaire urbanisme/CFD.
- **Intérêt :** vocabulaire et exemples de réduction géométrique de la ville pour la dispersion ; parenté lointaine avec la « modélisation géométrique à complexité réduite » du corpus Drift-X.
- **Limite :** contexte urbain/planification, pas la dérive de pulvérisation ; aucune équivalence démontrée avec la métrique travel-time ni la pseudo-distance Drift-X.
- [Article](https://doi.org/10.1016/j.scs.2021.102882)


## Tests mathématiques recommandés

- Vérifier explicitement la non-symétrie et les cas où le temps de transport est infini.
- Identifier les conditions d'existence et d'unicité des caractéristiques.
- Documenter les singularités aux sources, puits, points stagnants et zones de champ de vitesse incomplet.
- Ne pas appeler « métrique » une fonction sans qualifier les axiomes satisfaits ou violés.
- Distinguer une intuition géométrique utile d'une équivalence démontrée.
