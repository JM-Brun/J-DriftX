# 43 — Audit de l'article Mohammadi & Brun (2006)

**Périmètre :** lecture critique de l'extraction texte versionnée du PDF éditeur, pages imprimées 634–638. Ce document sépare ce qui est explicitement imprimé dans l'extraction, les conséquences mathématiques et les vérifications encore nécessaires sur le fac-similé. L'accès direct au PDF éditeur a renvoyé une erreur 403 pendant cette passe ; les figures et la typographie des équations n'ont donc pas été vérifiées visuellement ici. L'extraction brute n'est pas une transcription fiable des formules lorsque les symboles sont dégradés.

## Source et méthode

- Mohammadi, B. & Brun, J.-M. (2006), « Similitude généralisée et modélisation géométrique à complexité réduite », *Comptes Rendus Mécanique*, 334(10), 634–638, DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007).
- [Page officielle et texte indexé de l'article](https://comptes-rendus.academie-sciences.fr/mecanique/articles/10.1016/j.crme.2006.06.007/).
- [PDF éditeur](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf).
- Extraction du dépôt : [`raw/extracts/2006-mohammadi-brun-crmeca.txt`](../raw/extracts/2006-mohammadi-brun-crmeca.txt).
- Fiche de provenance du binaire : [`raw/provenance/2006-mohammadi-brun-crmeca.pdf.md`](../raw/provenance/2006-mohammadi-brun-crmeca.pdf.md).

## 1. Pages 634–635 — Objectif et modèle de similitude

Le résumé présente un modèle de complexité réduite pour le transport et la dispersion d'un scalaire passif, ajusté à partir d'observations partielles. Il propose de généraliser des solutions de similitude de jets/plumes dans une métrique non symétrique fondée sur des temps de transport. Il affirme que le modèle évite de résoudre une EDP à chaque évaluation et permet de calculer la solution en un point.

L'équation (1) est présentée comme un problème d'assimilation des paramètres du modèle à partir d'observations de vitesse et de concentration. L'extraction ne conserve pas assez bien la structure mathématique de l'objectif pour certifier ici chaque terme, signe, norme ou pondération : ils doivent être transcrits depuis le PDF visuel avant toute implémentation.

L'équation (2) introduit un profil de similitude du type
[
c(x,y)=c_c(x)f(y,delta(x)),
]
avec une décroissance axiale et un profil transversal dépendant de l'épaisseur (delta(x)). La formule exponentielle exacte et les paramètres doivent être contrôlés sur le fac-similé avant d'être utilisés comme spécification de code.

**Interprétation :** l'idée de base à préserver est une famille paramétrique de profils, alimentée par des variables physiques et calibrée à partir de données. L'article ne justifie pas à lui seul que cette famille soit exacte pour des vents variables ou pour d'autres mécanismes physiques.

## 2. Pages 635–636 — Pseudo-distance orientée

La section 3 définit une pseudo-distance directionnelle à partir d'une caractéristique issue de (A) et de la projection (B^perp) du point (B) sur cette caractéristique. Le temps de migration est une intégrale le long de la caractéristique, avec vitesse supposée non nulle et projection supposée suffisamment bien définie. L'article précise qu'il suppose la caractéristique unique et écarte les sources et puits pour cette construction.

Le texte avertit explicitement que l'objet construit **n'a pas toutes les propriétés d'une distance** :
- la séparation peut échouer : (d(A,B)=0) n'implique pas nécessairement (A=B) ;
- la symétrie échoue en général ;
- l'inégalité triangulaire peut être mise en défaut.

Ce sont des propriétés reconnues par les auteurs, et non des erreurs à « corriger » en imposant artificiellement les axiomes d'une distance métrique. Pour éviter la confusion avec une métrique mathématique standard, le code et la documentation doivent préciser s'il s'agit d'un temps de transport orienté, d'un coût de projection ou d'une pseudo-distance au sens propre.

Le texte indique aussi que la projection peut être non unique ; il propose alors une direction de projection qui satisfait au mieux une relation de transport de type (ucdot
abla c=0). Cette règle de départage est une heuristique à spécifier et tester, pas une preuve d'unicité ou de cohérence globale.

### Reconstruction mathématique à tester

Une définition exploitable doit expliciter :
- le domaine du champ de vitesse, sa régularité et ses zéros ;
- l'existence, l'unicité et la durée d'existence de la caractéristique ;
- la définition de la projection (B^perp), les cas de projection multiple et la règle de départage ;
- les cas amont, hors domaine, stagnation et trajectoire non atteignable ;
- les unités du temps de migration et le comportement en limite ;
- le fait que le coût peut dépendre de la source et de la cible et ne pas être une coordonnée globale.

Le contre-exemple de cisaillement déjà documenté dans le dépôt montre qu'un coût de projection peut ne pas satisfaire (ucdot
abla d_A=1). Cela interdit de traiter automatiquement ce coût comme une coordonnée régulière de temps de transport ; voir [la note de conservation](32-conservation-coordonnees-travel-time.md).

## 3. Page 636 — Conservation globale annoncée

L'extraction indique qu'une condition de conservation globale est introduite :
[
int_{mathbb R^3} c(p,u(p)),dV
= 	ext{quantité totale émise}.
]

La mise en page et la formule exacte doivent être revérifiées sur le PDF, mais le texte explicatif distingue bien cette **intégrale globale sur le volume** d'une affirmation concernant chaque surface iso-temps. Cette revendication ne prouve donc pas que le flux scalaire à travers toute surface définie par un temps de migration est constant.

Sous l'interprétation conventionnelle (c) = concentration massique volumique, l'intégrale de (c) sur un volume a l'unité d'une masse. Pour comparer cette quantité à une émission, il faut que la définition de la source, la durée d'intégration, les pertes et les conditions aux limites soient compatibles. L'article renvoie à la thèse pour le traitement à l'échelle de la rangée de culture ; ce bilan d'entrée doit être audité séparément.

## 4. Page 636 — Reconstruction du champ de vitesse

Le texte propose de compléter des observations météorologiques clairsemées par un champ de vitesse dérivé d'un potentiel, avec une formulation d'optimisation. L'extraction de l'équation (4) est trop dégradée pour certifier le signe de l'opérateur elliptique, le fonctionnel exact, les contraintes ou les conditions aux limites.

**Point à vérifier avant implémentation :** une écriture du type (mathbf u=
ablaphi) impose un champ irrotationnel sur le domaine où le potentiel est régulier. Cela ne suffit pas à garantir que le champ respecte les contraintes physiques de vent dans un relief ou une couche limite. Le choix de potentiel, l'objectif d'assimilation, les contraintes de divergence et les conditions aux limites doivent être transcrits et justifiés séparément.

L'article propose aussi une alternative par grille grossière des temps de migration et interpolation. Cette variante doit être traitée comme une méthode numérique distincte, avec erreur d'interpolation et convergence mesurées, plutôt que supposée équivalente à l'intégration exacte des caractéristiques.

## 5. Pages 636–638 — Résultats et revendication de coût

Le texte décrit une comparaison entre la solution de similitude et une simulation directe d'une équation instationnaire de transport–diffusion–dépôt par éléments finis stabilisés, pour le même champ de vitesse. Le terme de dépôt aurait été calibré dans le cas de vitesse uniforme pour retrouver la solution analytique. Il est également indiqué que la linéarité sert à accumuler des solutions de similitude pour une source mobile.

Les auteurs rapportent un facteur de réduction d'environ (10^3) à (10^4) pour l'évaluation en un point, en comparant avec un maillage d'environ 3 000 points, et indiquent une croissance favorable du rapport avec la taille du problème.

Cette valeur est une **mesure rapportée dans le contexte expérimental de l'article**, pas un benchmark moderne reproductible ni une preuve du coût total inférieur. Il reste à récupérer les paramètres, le code ou une description suffisante du protocole, les tailles exactes, les tolérances, le temps de préparation/calibration et le coût de reconstruction du champ. Pour une comparaison actuelle, mesurer séparément :
1. préparation des champs et des caractéristiques ;
2. calibration/assimilation ;
3. coût par requête et coût pour un champ complet ;
4. mémoire, erreur de prédiction et stabilité ;
5. temps de développement ou d'intégration si l'objectif est opérationnel.

Le papier indique également que les campagnes de mesure nécessaires à la validation terrain sont prévues pour l'avenir. Les exemples de simulation présentés ne doivent donc pas être décrits comme une validation indépendante sur données de terrain.

## 6. Registre provisoire des anomalies et questions

| ID | Observation | Qualification actuelle | Action de vérification |
|---|---|---|---|
| A06-01 | La pseudo-distance ne vérifie pas nécessairement séparation, symétrie ou inégalité triangulaire | Limite structurelle explicitement reconnue, pas une faute | Préserver le caractère orienté ; définir précisément le domaine d'usage |
| A06-02 | Existence/unicité de la caractéristique et de la projection sont supposées ou traitées par heuristique | Hypothèses insuffisamment formalisées | Définir cas admissibles, échecs et tests analytiques |
| A06-03 | L'intégrale globale de concentration est liée à la quantité émise sans démonstration complète dans le passage | Conservation globale revendiquée ; bilan physique à reconstruire | Vérifier unités, source, dépôt, frontières et bilan du modèle multi-niveaux |
| A06-04 | L'équation du potentiel et son fonctionnel d'assimilation sont dégradés dans l'extraction | Incertitude de transcription, pas encore une erreur de source confirmée | Transcription visuelle de l'équation (4), conditions aux limites et opérateur |
| A06-05 | Le facteur (10^3)–(10^4) est rapporté sur un cas avec maillage d'environ 3 000 points | Résultat contextuel non généralisable sans protocole | Reproduire les coûts complets à précision comparable |
| A06-06 | Le papier annonce une validation terrain future | Limite de preuve historique explicite | Ne pas présenter les figures synthétiques comme validation terrain |

## 7. Décision pour J-DriftX

La reconstruction doit préserver l'idée originale d'un profil de similitude évalué au moyen d'un coût de transport dirigé, ainsi que l'usage de données partielles et la possibilité d'évaluation ponctuelle. Elle ne doit pas imposer des propriétés de distance métrique que la source rejette explicitement.

En parallèle, le projet doit corriger ou circonscrire les hypothèses non démontrées : définition et régularité du champ, projection, conservation, bilan de dépôt, identification des paramètres et comparaison des coûts. Une version moderne peut remplacer certaines briques par des caractéristiques robustes, des solveurs EDP de référence, des méthodes de réduction alternatives ou des modèles hybrides, à condition de documenter la divergence par rapport à la source et de comparer les résultats sur des tests communs.

## 8. Vérifications encore ouvertes

- [ ] Inspecter visuellement les cinq pages du PDF éditeur et confirmer toutes les équations, signes, indices et figures.
- [ ] Authentifier le binaire versionné par comparaison SHA-256 avec le PDF officiel téléchargé.
- [ ] Reconstituer l'équation (1) d'assimilation et l'équation (4) de potentiel à partir du fac-similé.
- [ ] Vérifier les unités et les bilans du modèle local, du modèle réduit et de la source mobile.
- [ ] Distinguer clairement résultats analytiques, résultats synthétiques, comparaison à une EDP et validation terrain.
