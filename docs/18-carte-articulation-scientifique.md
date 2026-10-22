# Carte d'articulation scientifique et technique

> **Rôle de cette page :** point d'entrée pour comprendre ce que le dépôt contient, ce que les expériences démontrent réellement, ce qui reste une hypothèse et dans quel ordre poursuivre. Ce document ne remplace ni la feuille de route ni les preuves détaillées ; il les relie.

## 1. Résumé de l'état actuel

J-DriftX est une **recherche exploratoire**, issue de Drift-X (2006–2009). Le projet cherche à déterminer si des solutions de similitude combinées à une représentation dirigée par les temps de transport peuvent fournir une approximation utile de certains problèmes de dispersion atmosphérique à coût réduit.

La formulation cible n'est pas encore une méthode prédictive validée. Il faut garder distincts cinq niveaux :

1. **Héritage documenté** — ce que les articles historiques disent effectivement.
2. **Hypothèse de modèle** — ce que J-DriftX propose de généraliser ou de tester.
3. **Vérification mathématique et numérique** — ce que des définitions, cas analytiques et tests permettent de contrôler.
4. **Comparaison différentielle** — ce qui pourrait montrer un avantage sur des méthodes de référence équitables.
5. **Validation et utilité** — ce qui établirait la fiabilité sur des données indépendantes et un bénéfice pour une décision réelle.

Une preuve à un niveau ne vaut pas preuve aux niveaux suivants.

## 2. Carte des niveaux de preuve

| Niveau | État | Ce qui existe | Ce que cela ne permet pas de conclure |
|---|---|---|---|
| Sources historiques | Documenté, avec limites bibliographiques explicites | Articles et fiches de lecture liés à l'héritage Drift-X | Que toutes les propriétés historiques sont reproduites par le code actuel |
| Formulation mathématique cible | Partielle et à instruire | Documentation sur similitude, métrique de temps de transport, contraintes et travaux connexes | Que la formulation est complète, nouvelle ou bien posée pour un cas applicatif |
| Cœur Python actuel | Modules limités, testés sur des cas précis | Calculs utilitaires, champs synthétiques, trajectoires cinématiques, références analytiques | Que temps_transport implémente la pseudo-distance historique, ou que le code constitue un modèle de dispersion complet |
| Laboratoires numériques | Vérification sur des cas synthétiques/connus | Comparaisons Euler/RK4, advection-diffusion analytique, schémas périodiques indépendants et études de convergence | Que les paramètres sont calibrés, que les résultats représentent un vent réel ou que le modèle est validé physiquement |
| Valeur comparative | Non démontrée | Protocole, hypothèses sceptiques et baselines à définir | Que J-DriftX est plus rapide, plus précis ou plus utile que les solutions disponibles |
| Validation indépendante / usage | Non démontrée | Besoins et candidats de données à instruire | Toute revendication prédictive, opérationnelle ou réglementaire |

## 3. Portes de décision : ne pas confondre G0-S et G0-A

- **G0 documentaire : franchi le 22 octobre 2026.** Le cadrage documentaire, les questions, les baselines candidates et les critères de preuve ont été structurés. Cela valide un état de préparation documentaire, pas la solution.
- **G0-S — exploration scientifique minimale : autorisée sous périmètre strict.** Définir les objets mathématiques, étudier les cas analytiques, construire des contre-exemples et vérifier les propriétés nécessaires.
- **G0-A — utilité applicative : non démontrée.** Le besoin prioritaire, la décision utilisateur et la valeur différentielle restent à établir indépendamment de la méthode.
- **G1 — cohérence théorique : à poursuivre sur un problème précisément borné.** Expliciter variables, unités, hypothèses, conditions aux limites et preuves.
- **G2–G4 — comparaison, validation indépendante et pertinence applicative : conditionnels.** Ne pas démarrer de benchmark applicatif coûteux ni revendiquer un bénéfice avant de disposer d'un protocole réfutable et de données adaptées.

Voir le [cadre de décision et de preuve](08-decision-utilite-et-preuve.md), la [revue adversariale G0](10-revue-adversariale-g0.md) et la [feuille de route](03-roadmap-jdriftx-v2.md).

## 4. Comment lire les laboratoires

Les applications sous apps/ sont des **outils pédagogiques et de vérification numérique**. Elles servent à inspecter un comportement, confronter un calcul à une solution connue, observer une erreur et tester une propriété sous des hypothèses explicites.

- apps/interactive_lab.py : champs vectoriels et reliefs synthétiques ; aucune dynamique vent–relief n'est calculée.
- apps/scientific_validation.py : intégration de trajectoires cinématiques et transport gaussien 1D, comparés à des références analytiques.
- apps/convergence_lab.py : advection-diffusion périodique, deux schémas numériques et convergence sur un profil sinusoïdal lisse.

Ces cas sont utiles pour détecter des erreurs de code et clarifier les méthodes. Ils ne représentent ni une validation météorologique, ni une validation des gouttelettes, ni une comparaison applicative de J-DriftX. Les hypothèses et limites spécifiques sont détaillées dans [la spécification des laboratoires](17-laboratoire-interactif.md) et dans la page Quarto [Laboratoire interactif](../site/projet/laboratoire-interactif.qmd).

## 5. Ordre de travail recommandé

1. **Stabiliser les définitions.** Définir sans ambiguïté la trajectoire/caractéristique, le temps de parcours, le champ de vitesse admissible, les singularités et les cas où le temps n'existe pas ou n'est pas unique.
2. **Construire le plus petit cas analytique discriminant.** Vérifier les cas uniformes, les limites, l'orientation, la non-symétrie et les contre-exemples ; ne pas appeler une formule « métrique » sans préciser les axiomes satisfaits.
3. **Relier chaque affirmation à une preuve.** Pour chaque propriété, indiquer si elle est documentée par une source, définie, démontrée, testée numériquement, mesurée empiriquement ou encore conjecturale.
4. **Choisir le besoin indépendamment de la solution.** Nommer utilisateur, observable, décision, baseline, seuil de succès et condition d'arrêt avant tout benchmark applicatif.
5. **Comparer seulement après ces étapes.** Séparer erreur de modèle, erreur numérique, incertitude des données et coût total de préparation/calibration/exécution.

## 6. Règles éditoriales et scientifiques

- Employer « objectif », « hypothèse », « candidat » ou « à démontrer » tant que les preuves ne justifient pas une formulation plus forte.
- Toujours associer une affirmation quantitative à son protocole, son domaine de validité et sa source.
- Distinguer les résultats historiques des résultats obtenus dans le dépôt actuel.
- Ne pas transformer la présence de tests en validation physique.
- Ne pas présenter une absence de référence trouvée comme une preuve d'absence de travaux concurrents.
- Conserver les résultats négatifs et les critères d'arrêt ; l'objectif est de décider si la piste mérite d'être poursuivie, pas de confirmer à tout prix l'hypothèse initiale.

## Sources de référence dans le dépôt

- [Feuille de route](03-roadmap-jdriftx-v2.md)
- [Cadre de décision et de preuve](08-decision-utilite-et-preuve.md)
- [Revue adversariale G0](10-revue-adversariale-g0.md)
- [MVP scientifique minimal et G0](13-mvp-scientifique-et-g0.md)
- [Spécification des laboratoires](17-laboratoire-interactif.md)
- [Page de qualité et tests](../site/projet/qualite.qmd)
