# Séance Emploi — J-DriftX : preuve mathématique et protocole d'évaluation

> **Durée maximale : 60 minutes.** Cette fiche prépare un exercice de raisonnement ; elle ne constitue ni un résultat scientifique ni une validation du projet.

## Pourquoi cette séance doit respecter la PR G0

**Terminologie à ne pas confondre :** le jalon documentaire **G0** a été déclaré franchi dans la fiche de cadrage du 22 octobre 2026. Cela ne signifie ni que l'exploration scientifique est terminée, ni que l'utilité applicative est démontrée. Dans cette séance, **G0-S** désigne le volet d'exploration scientifique minimale et **G0-A** le volet d'utilité applicative ; ce sont des sous-pistes de travail, pas le statut global de la porte G0.

- **Le travail G0-S peut avancer** : définition mathématique explicite, cas 1D analytique, propriétés, contre-exemples, tests et positionnement bibliographique.
- **La validation applicative reste bloquée** : la fiche G0 propose un utilisateur, un observable, des baselines et des corpus candidats, mais les fichiers bruts, les unités, les limites de détection, la licence DIFLU et la structure exacte des essais restent à vérifier en G1. Aucun résultat de performance n'est encore établi.
- Le catalogue de jeux de données est une présélection documentaire, **pas un audit des fichiers bruts**. Ne pas lancer un benchmark avant d'avoir satisfait les prérequis G1.

## Objectifs d'apprentissage

À la fin de la séance, pouvoir :
1. distinguer cohérence mathématique, validation physique et utilité décisionnelle ;
2. définir un objet mathématique, ses hypothèses et son domaine sans lui attribuer une interprétation physique non démontrée ;
3. choisir une vérification analytique ou un contre-exemple qui peut réfuter une propriété ;
4. expliquer pourquoi une recherche parmi plusieurs variantes ne doit pas être évaluée sur le même résultat qui a servi à les choisir ;
5. énoncer les preuves manquantes avant de pouvoir évaluer G0-A.

## Déroulé (60 min, sans code requis)

### 0–10 min — Classer les affirmations par niveau de preuve

Pour chacune des affirmations ci-dessous, classer la preuve requise : **(S) mathématique**, **(N) numérique/synthétique**, **(P) physique/expérimentale**, **(D) décisionnelle/applicative**. Une affirmation peut nécessiter plusieurs niveaux.

- A. « La fonction de temps de parcours vaut zéro entre un point et lui-même. »
- B. « Le solveur calcule correctement le cas 1D choisi. »
- C. « Le modèle prédit la concentration atmosphérique sur un site non observé. »
- D. « L'approche réduit le temps de calcul sans dégrader la précision utile. »
- E. « L'approche améliore une décision réelle par rapport à une baseline. »
- F. « L'idée constitue une contribution mathématique originale. »

Écrire pour chaque affirmation une preuve positive et un résultat qui la réfuterait ou limiterait sa portée.

### 10–25 min — Construire un cas 1D calculable à la main

Considérer un **modèle jouet abstrait**, et non un modèle physique de dispersion. Sur une ligne, le coût de parcours est défini par deux vitesses constantes : (c_+>0) dans le sens croissant et (c_->0) dans le sens décroissant.

Pour des positions (x,y\in\mathbb{R}), proposer puis vérifier la définition :
- si (y\ge x), (T(x,y)=(y-x)/c_+) ;
- si (y<x), (T(x,y)=(x-y)/c_-).

Avec (c_+=10) unités de distance/s et (c_-=5) unités de distance/s :
1. calculer (T(0,100)) et (T(100,0)) ;
2. vérifier (T(x,x)=0) et (T(x,y)\ge0) ;
3. expliquer quand (T(x,y)\ne T(y,x)) ;
4. tester l'inégalité triangulaire dirigée sur au moins trois triplets, dont un point intermédiaire situé en dehors de l'intervalle entre les deux extrémités ;
5. donner un exemple de formule plausible mais invalide (par exemple un temps négatif) et expliquer pourquoi elle échoue.

**Limite obligatoire :** ce calcul vérifie seulement la définition jouet choisie. Il ne prouve ni nouveauté, ni représentation d'un champ de vent, ni transport de masse, ni précision de dispersion.

### 25–40 min — Revue adversariale : définition, nouveauté, sélection

Répondre sans consulter les documents :

1. Quelle propriété est réellement démontrée par le calcul précédent, et laquelle ne l'est pas ?
2. Pourquoi le problème de navigation de Zermelo et les géométries de Randers/Finsler sont-ils des antécédents à comparer plutôt que des citations décoratives ?
3. Si 40 variantes de la définition ou du solveur sont essayées et que seule la variante avec les meilleurs résultats synthétiques est rapportée, quel biais de sélection apparaît ? Comment conserver les cas de validation séparés de ceux utilisés pour choisir la variante ?
4. Pourquoi ajouter plusieurs métriques après coup ne corrige-t-il pas la sélection du « gagnant » ?
5. Quel résultat conduirait à conserver le travail comme ressource pédagogique, mais à abandonner une revendication de nouveauté ?

### 40–50 min — Garder G0-A conditionnel

À partir du catalogue, choisir **un seul candidat à examiner plus tard** (par exemple DATEM/ETEX, DIFLU ou ERIES), mais ne pas présumer qu'il est exploitable.

Compléter les champs ci-dessous avec « inconnu » lorsque la preuve manque :
- utilisateur et décision visée ;
- phénomène et régime physique ;
- observable primaire et unité ;
- baseline réellement comparable ;
- données brutes, licence, métadonnées et nombre d'expériences indépendantes ;
- unité de séparation entre développement et évaluation ;
- métrique primaire, incertitude et seuil de succès justifié ;
- critère d'arrêt.

**Règle :** tant que le besoin et l'observable ne sont pas choisis, aucune métrique de performance ne peut être désignée sérieusement comme primaire. Le nombre de collecteurs, points ou fichiers n'est pas le nombre d'expériences indépendantes.

### 50–60 min — Livrable

Rédiger une page avec :
1. la définition exacte du modèle jouet et ses hypothèses ;
2. une propriété vérifiée, un contre-exemple et une limite ;
3. la revendication scientifique la plus forte qui soit réellement justifiée ;
4. les affirmations interdites à ce stade ;
5. les informations manquantes avant toute évaluation G0-A ;
6. la prochaine expérience discriminante la moins coûteuse.

## Critères de correction (0–2 chacun)

- **C1 — Niveau de preuve :** ne confond pas propriété mathématique, test logiciel, validation physique et utilité.
- **C2 — Définition et hypothèses :** explicite le domaine, les unités, les directions et les cas limites.
- **C3 — Contre-exemple :** vérifie les propriétés sur des cas non triviaux et cherche à réfuter, pas seulement à illustrer.
- **C4 — Sélection :** distingue résultat de sélection et estimation indépendante ; reconnaît le biais du maximum parmi plusieurs variantes.
- **C5 — G0-A :** identifie les inconnues au lieu de les remplir par supposition ; ne lance pas de benchmark prématuré.
- **C6 — Portée :** formule une conclusion proportionnée aux preuves et nomme au moins une limite.

Un score faible n'invalide pas le projet ; il indique ce que l'expérience suivante doit rendre vérifiable. Ne pas modifier de statut de compétence sur la seule base de la lecture de cette fiche.

## Sources de travail du projet

- [Décision G0-S / G0-A et MVP scientifique](13-mvp-scientifique-et-g0.md)
- [Cadre de décision, utilité et preuve](08-decision-utilite-et-preuve.md)
- [Catalogue de données de transport et dispersion](12-catalogue-donnees-transport-dispersion.md)
- [Gibbons et al. (2009), Zermelo–Randers–Finsler geometry](https://doi.org/10.1103/PhysRevD.79.044022)
- [Time-optimal Zermelo navigation with moving obstacles (2024)](https://doi.org/10.1016/j.difgeo.2024.102177)
- [Time-dependent Zermelo navigation (2025)](https://arxiv.org/abs/2508.07274)

Cette séance prépare une méthode de travail. Elle ne déclare pas G0-S achevé, G0-A franchi, ni la nouveauté établie.
