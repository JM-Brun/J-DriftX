# G0 — chemin scientifique minimal et trajectoire maximale

> **Décision proposée (22 octobre 2026).** Autoriser un MVP scientifique exploratoire très restreint, sans prétention prédictive ou applicative, tout en conservant une trajectoire d'extension conditionnelle. Cette décision ne vaut pas validation du cas d'usage industriel ni franchissement du G0 applicatif.

## 1. Découpler deux questions qui ne doivent plus se bloquer mutuellement

Le cadrage précédent traitait parfois G0 comme une porte unique. Cela confond deux propositions distinctes :

- **G0-S — valeur scientifique exploratoire :** existe-t-il une question mathématique précise autour du temps de parcours dirigé qui mérite une étude minimale, même sans application validée ?
- **G0-A — utilité applicative :** un utilisateur et une décision réels bénéficieraient-ils de J-DriftX par rapport à des outils existants ?

Le chemin minimal peut avancer sur G0-S, à condition d'annoncer le projet comme **exploration scientifique / modèle jouet** et de ne revendiquer ni utilité applicative, ni supériorité, ni nouveauté avant vérification. G0-A reste ouvert et bloquant pour tout benchmark applicatif, choix d'un domaine industriel, ou revendication opérationnelle.

Cette séparation n'abaisse pas le niveau de preuve : elle rend explicite ce que chaque expérience peut démontrer.

## 2. MVP scientifique proposé

### Question minimale

**Quelles propriétés possède une fonction de temps de parcours dirigé définie par une dynamique explicite, et lesquelles ne découlent pas de sa seule définition ?**

Cette question est plus petite que « prédire la dispersion atmosphérique ». Elle permet de tester une brique mathématique liée à la vision de J-DriftX sans supposer qu'elle améliore déjà une prédiction physique.

### Périmètre inclus

1. Définir précisément l'espace, les directions admissibles, la dynamique de propagation, les unités et les conditions aux limites.
2. Distinguer distance géométrique, temps de parcours et coût dirigé. Ne pas appeler une fonction « métrique » sans vérifier les axiomes pertinents.
3. Étudier d'abord un cas 1D calculable à la main, puis un cas 2D synthétique uniquement si le cas 1D révèle une propriété précise à tester.
4. Démontrer ou réfuter : positivité, séparation, inégalité triangulaire dirigée, asymétrie éventuelle, continuité/stabilité dans les hypothèses retenues.
5. Construire des contre-exemples : vitesse uniforme, vitesse spatialement variable, changement de direction, absence de chemin admissible, et cas où une asymétrie apparente disparaît.
6. Fournir une implémentation de référence minimale, des tests automatiques et des figures reproductibles qui illustrent les propriétés prouvées.
7. Rechercher les antécédents bibliographiques des définitions et résultats avant toute revendication d'originalité.

### Hors périmètre explicite du MVP

- Pas de dépôt au sol, concentration de polluant ou exposition comme cible prédite.
- Pas de prétention à représenter turbulence, diffusion, sédimentation, évaporation, dépôt ou flottabilité.
- Pas d'entraînement ML, d'assimilation de données ou de calibration empirique.
- Pas de benchmark CAPRIV, DATEM, ETEX ou autre jeu réel pour revendiquer une validation physique.
- Pas de comparaison de performance applicative, d'outil réglementaire, de plugin QGIS, d'API ou d'interface utilisateur.
- Pas d'affirmation que le temps de parcours dirigé est nouveau, qu'il améliore l'extrapolation ou qu'il est déjà une métrique au sens mathématique.

Ces exclusions sont des protections contre les conclusions non justifiées, pas une fermeture définitive des possibilités futures.

## 2.1. Antécédents à examiner avant de revendiquer une contribution

Le temps de parcours minimal et sa géométrie ne sont pas des territoires vierges. Le problème de navigation de Zermelo et les métriques de Randers/Finsler relient déjà des champs de vent/courant à des trajectoires à temps minimal. Les travaux à examiner incluent notamment :

- Gibbons et al. (2009), *Stationary metrics and optical Zermelo-Randers-Finsler geometry*, [Physical Review D](https://doi.org/10.1103/PhysRevD.79.044022).
- Dušek (2018), *Zermelo Navigation Problem in Geometry*, [DOI 10.17818/NM/2018/4SI.16](https://doi.org/10.17818/NM/2018/4SI.16).
- *Time-optimal solutions of Zermelo's navigation problem with moving obstacles* (2024), [Differential Geometry and its Applications](https://doi.org/10.1016/j.difgeo.2024.102177).
- Markvorsen, Pendás-Recondo et Rygaard (2025), *Time-dependent Zermelo navigation with tacking*, [arXiv:2508.07274](https://arxiv.org/abs/2508.07274).

Cette liste est un point de départ, pas une revue exhaustive ni une preuve que les idées spécifiques de J-DriftX sont couvertes. Il faut comparer les définitions exactes, hypothèses, résultats et objectifs. La simple réutilisation d'une géométrie de temps de parcours connue n'est pas une nouveauté.

**Conséquence pour le MVP :** la première tâche est une note de positionnement mathématique. Si aucune propriété ou construction nouvelle n'émerge, continuer comme ressource pédagogique / banc d'essai reproductible reste valide, mais la revendication de contribution originale doit être abandonnée ou reformulée autour d'un différentiel précisément démontré.

### Prérequis ajouté après lecture de la source primaire

Le MVP ne doit pas commencer par une pseudo-distance simplifiée inventée pour le besoin. La note de 2006 définit une projection du point cible \(B\) sur la caractéristique passant par \(A\), puis le temps de migration vers \(B^\perp\). Elle reconnaît que la construction peut perdre la séparation des points et violer l'inégalité triangulaire.

En conséquence, le premier test de référence doit distinguer deux implémentations explicitement nommées :

1. **Reproduction historique** : pseudo-distance projetée, avec règles de caractéristique unique, projection, orientation et points inaccessibles.
2. **Variante exploratoire** : temps d'arrivée au point cible ou autre coût, si une question scientifique le justifie. Cette variante doit porter un nom distinct et ne peut pas être présentée comme reproduction de la méthode de 2006.

**État du verrou** : le cas uniforme \(\mathbf u=(U,0)\) est maintenant implémenté comme fonction de référence distincte et couvert par des tests : temps longitudinal, coût nul entre points distincts de même abscisse, coût infini en amont, invariance par rotation et rejet d'une vitesse nulle. Les cas sans caractéristique unique, les sources/puits et les champs variables restent exclus de cette implémentation limitée et doivent recevoir des règles documentées avant généralisation.

## 3. Critères d'acceptation du MVP

Le MVP est terminé lorsqu'il contient :

- une définition mathématique sans ambiguïté, avec domaine, hypothèses et unités ;
- une séparation explicite entre propositions démontrées, conjectures et illustrations numériques ;
- au moins un cas analytique résolu indépendamment du code ;
- des tests de propriétés et des contre-exemples, y compris les cas limites ;
- une implémentation reproductible sans dépendances applicatives lourdes ;
- une courte revue ciblée des concepts voisins (temps de parcours, géométrie de Finsler/asymétrique, géodésiques, eikonale/optimal control si pertinents), avec citations vérifiées ;
- une conclusion explicite parmi : propriété utile démontrée, idée connue mais pédagogiquement utile, résultat nul/incohérent, ou piste à abandonner.

**Pas de seuil de performance arbitraire.** Pour ce MVP, le critère est la validité mathématique, la reproductibilité et la valeur explicative. Toute revendication de vitesse ou de précision nécessite un protocole distinct.

## 4. Porte suivante : une seule extension à la fois

| Porte | Extension possible | Condition nécessaire |
|---|---|---|
| **S1 — Champ 2D synthétique** | Calculer un temps de parcours dans un champ de vitesse spatialement variable | Définition de dynamique et conditions aux limites; référence numérique indépendante et étude de convergence |
| **S2 — Transport physique minimal** | Relier la géométrie du temps de parcours à une équation de transport définie | Dérivation ou approximation justifiée; préciser advection, diffusion, source et observable |
| **S3 — Cas atmosphérique contrôlé** | Étudier un cas analytique ou une expérience de traceur | Régime physique compatible, baseline équitable, métadonnées et protocole préétabli |
| **S4 — Cas applicatif étroit** | Choisir éventuellement dispersion routière, industrielle, marine ou dérive agricole | Besoin utilisateur documenté, observable, baseline de référence et validation indépendante |
| **S5 — Extension multi-cas** | Réutiliser le noyau dans plusieurs régimes | Chaque domaine a son modèle physique, ses données et ses critères; aucun transfert automatique des paramètres ou conclusions |

Chaque extension est optionnelle. L'échec d'une porte ne bloque pas la publication d'un résultat négatif ou pédagogique de niveau inférieur, et n'autorise pas à sauter la porte.

## 5. Trajectoire maximale conservée

La vision maximale reste un moteur de dispersion à complexité réduite qui pourrait, si les preuves le permettent, combiner solutions de similitude, géométrie/temps de transport, contraintes physiques, calibration et calcul ponctuel. Des applications potentielles incluent l'atmosphère, les sources routières ou industrielles, certains problèmes de transport marin/fluvial, et éventuellement la dérive de pulvérisation.

Mais cette vision devient une **carte d'options**, pas un engagement à implémenter toutes les branches :

- **Cœur mathématique commun :** définitions et algorithmes génériques, sans encoder des hypothèses physiques non justifiées.
- **Adaptateurs physiques distincts :** air, gouttelettes, eau, courants marins ou rejets denses ne sont pas des configurations interchangeables d'un même modèle sans dérivation.
- **Validations distinctes :** un succès sur traceur gazeux ne valide pas la dispersion de gouttelettes; une trajectoire marine ne valide pas un panache atmosphérique.
- **Applications en aval :** calibration, estimation de source, GIS/QGIS et API seulement après démonstration de valeur du noyau dans un problème défini.

La modularité doit préserver la possibilité d'étendre, sans créer dès maintenant des abstractions génériques inutiles.

## 6. Règles de gouvernance scientifique

1. **Une hypothèse, une expérience discriminante.** Chaque extension doit nommer le résultat qui confirmerait, limiterait ou réfuterait l'hypothèse.
2. **Baseline avant avantage revendiqué.** Aucun « plus rapide », « plus précis », « plus robuste » ou « meilleur hors domaine » sans comparaison équitable.
3. **Séparer les niveaux de preuve.** Théorème, simulation synthétique, validation expérimentale et utilité décisionnelle sont des catégories distinctes.
4. **Pas de données pour décorer.** Un jeu de données n'est utilisé que si son observable correspond à la formulation physique; les analogies multi-domaines testent au plus la méthode numérique, pas la physique.
5. **Données indépendantes.** Grouper les mesures par expérience/scénario; ne pas répartir aléatoirement des observations corrélées entre calibration et test.
6. **Résultats négatifs conservés.** Les hypothèses abandonnées et les échecs restent traçables.
7. **Pas de scope creep.** Aucun module applicatif ne démarre tant qu'il ne sert pas un test approuvé.
8. **Nouveauté non présumée.** Une idée connue peut rester un excellent outil pédagogique, mais elle n'est pas annoncée comme contribution originale.

## 7. État G0 et décision

| Volet | État | Décision |
|---|---|---|
| **G0-S : exploration scientifique minimale** | Question mathématique isolable; les définitions et l'état de l'art ciblé restent à compléter | **Autoriser le cadrage et le MVP mathématique** |
| **G0-A : utilité applicative** | Utilisateur, décision et observable applicatif non établis; données brutes des candidats non auditées | **Toujours bloqué** |
| Extension multi-domaines | Pas de formulation physique commune démontrée | **Conserver comme trajectoire, pas comme MVP** |
| Revendication de nouveauté | État de l'art ciblé sur la définition exacte à faire | **Interdite jusqu'à vérification** |

La décision n'est donc ni « arrêter J-DriftX » ni « lancer le modèle complet ». C'est : **avancer maintenant sur la plus petite question mathématique réfutable, tout en gardant les applications conditionnelles aux preuves**.

## 8. Prochaines actions concrètes

1. Stabiliser une définition mathématique du temps de parcours orienté et des conditions où il est réellement asymétrique.
2. Faire une recherche bibliographique ciblée sur cette définition, ses axiomes et ses formulations proches.
3. Écrire les cas analytiques et contre-exemples avant d'implémenter un solveur général.
4. Formaliser tests unitaires et tests de propriétés sur la définition retenue.
5. Publier les figures et une note de résultats avec limites, sans revendiquer de validation physique.
6. En parallèle, maintenir le catalogue de données et le cadrage applicatif en état de veille; ne lancer l'audit des fichiers bruts que lorsqu'un candidat d'application est choisi sur des critères explicites.

## Liens

- [Fiche de séance — validation expérimentale et G0-S/G0-A](14-seance-validation-experimentale.md)
- [Cadre de décision et de preuve](08-decision-utilite-et-preuve.md)
- [Revue adversariale G0](10-revue-adversariale-g0.md)
- [Catalogue de données de transport et dispersion](12-catalogue-donnees-transport-dispersion.md)
- [Fallback scientifique : modèle jouet](09-fallback-modele-jouet.md)
- [Feuille de route](03-roadmap-jdriftx-v2.md)
