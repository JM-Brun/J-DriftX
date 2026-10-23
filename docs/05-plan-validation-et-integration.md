# Plan d’intégration scientifique et de validation — J-DriftX

> Statut : plan de travail proposé à la revue du projet. Ce document traduit l’audit de l’état de l’art en décisions vérifiables ; il ne constitue pas une validation scientifique des hypothèses du modèle.

## 1. Décision générale

La revue de l’état de l’art justifie de poursuivre l’investigation de J-DriftX, mais elle ne démontre pas à elle seule la nouveauté, la supériorité prédictive ni la conformité réglementaire du modèle. Les conclusions comparatives sont des **hypothèses de recherche** tant qu’elles ne sont pas étayées par des sources suffisamment examinées et des benchmarks reproductibles.

La priorité reste le noyau mathématique et sa validation, avant l’ajout de fonctionnalités applicatives. Le cadrage G0 documentaire a été franchi le 22 octobre 2026 : il fixe la question scientifique sur la dispersion d’un scalaire passif et retient DIFLU comme premier corpus candidat au test discriminant. Ce verdict documentaire ne valide ni l’utilité applicative (G0-A), ni la disponibilité exploitable des fichiers bruts, ni la performance du modèle. La dérive de pulvérisation en champ lointain reste une piste applicative possible, non le cas d’usage prioritaire établi.

## 2. Intégration dans le dépôt

| Élément | Rôle | Action attendue |
|---|---|---|
| docs/02-revue-etat-art-2026.md | Synthèse documentaire détaillée | Distinguer faits sourcés, interprétations et hypothèses ; compléter la méthode de recherche |
| site/etat-art/panorama.qmd | Synthèse publique | Afficher les limites de couverture et renvoyer au protocole |
| site/etat-art/positionnement.qmd | Positionnement scientifique | Présenter les différenciateurs comme des hypothèses à tester, non comme des avantages acquis |
| Issues publiques | Suivi des questions ouvertes | Faire dépendre chaque étape d’un livrable vérifiable et d’un critère d’acceptation |
| docs/references.md et site/references.bib | Traçabilité bibliographique | Vérifier les métadonnées, DOI, liens, dates et correspondance citations/bibliographie |
| site/projet/qualite.qmd et tests | Preuves techniques | Relier les affirmations de conservation, positivité et symétrie à des tests ou preuves explicites |

## 3. Rendre la revue reproductible

Le choix méthodologique est documenté dans [docs/06-choix-methode-revue-systematique.md](06-choix-methode-revue-systematique.md). Il explique pourquoi PRISMA 2020 est retenu comme standard de reporting, comment il se combine avec une phase exploratoire, le snowballing, une cartographie systématique et une évaluation critique, et pourquoi ces éléments ne doivent pas être confondus avec la revue bibliographique effective.

Le document actuel est une **revue structurée de l’état de l’art**, mais les informations disponibles ne suffisent pas encore à qualifier le processus de revue systématique entièrement reproductible. Avant d’employer cette qualification, consigner :

1. Les bases et moteurs interrogés, avec la date de chaque recherche.
2. Les chaînes de recherche exactes, filtres et plages temporelles.
3. Les critères d’inclusion et d’exclusion (langue, type de publication, pertinence applicative, accès au texte).
4. Le nombre de références trouvées, dédoublonnées, examinées sur titre/résumé, examinées en texte intégral et retenues.
5. La manière dont la qualité et le niveau de preuve de chaque source ont été évalués.
6. Les limites d’accès au texte intégral et les affirmations reposant seulement sur une notice, un résumé ou une source secondaire.

Pour chaque affirmation structurante, indiquer si elle relève d’un fait directement sourcé, d’une interprétation de la littérature ou d’une hypothèse propre à J-DriftX. Les affirmations absolues telles que « aucun modèle concurrent » doivent être bornées par le corpus effectivement examiné.

## 4. Programme de validation scientifique

### M1 — Noyau et cas de référence

- Formaliser les hypothèses, le domaine de validité et les conditions aux limites des solutions de similitude et de la métrique *travel-time*.
- Établir un cas gaussien de référence reproductible, avec paramètres et données publiés.
- Tester la convergence numérique, les unités, les cas limites, la symétrie lorsque celle-ci est attendue, la superposition si elle est théoriquement applicable, ainsi que la conservation de masse et la positivité lorsque le modèle les garantit.
- Mesurer erreur absolue et relative, temps de calcul, mémoire et stabilité ; enregistrer les versions du code et les paramètres.

**Critère d’acceptation :** tests automatisés reproductibles en CI, benchmark documenté et écarts expliqués. Toute propriété non démontrée doit être présentée comme objectif, pas comme garantie.

### M2 — Calibration et problème inverse

- Définir un jeu de données de calibration et un jeu de validation indépendant.
- Comparer aux méthodes de référence sur le même cas, les mêmes observations et le même budget de calcul.
- Tester la sensibilité au bruit, aux observations manquantes, à l’identifiabilité des paramètres et à la régularisation.
- Séparer explicitement l’ajustement des paramètres de l’évaluation hors échantillon.

**Critère d’acceptation :** protocole, données ou script de génération, métriques et limites documentés ; aucune conclusion de robustesse sans comparaison hors échantillon.

### M3 — Terrain et application

- Identifier en amont des campagnes de mesure publiées, documenter les licences et les métadonnées, puis réserver des observations à une validation indépendante.
- Comparer J-DriftX aux modèles de référence pertinents sans supposer qu’une différence de résultat signifie une amélioration.
- Tester séparément l’effet du vent non uniforme, du relief et des barrières végétales, en indiquant les conditions dans lesquelles chaque comparaison est valide.

**Critère d’acceptation :** résultats traçables sur données indépendantes, analyse d’incertitude et description des limites de généralisation.

### M4 — Publication

Préparer un article seulement après obtention de résultats vérifiables. Le manuscrit devra décrire la méthode, les hypothèses, les données, les baselines, les métriques, les résultats négatifs et les limites ; la revue de littérature seule ne suffit pas à revendiquer une supériorité du modèle.

## 5. Protocole de benchmark minimal

Pour chaque cas, publier :

- description physique, hypothèses, unités, paramètres et provenance des données ;
- version/commit du code et instructions de reproduction ;
- baselines et réglages identiques autant que possible ;
- erreur absolue et relative, conservation de masse et positivité si pertinentes ;
- temps de calcul, mémoire, sensibilité aux paramètres et incertitude ;
- domaine de validité, échecs observés et écarts non expliqués.

Les comparaisons POD/ML ne doivent pas être présentées comme une opposition générale : comparer des méthodes sur un problème, un jeu de données et un budget explicitement définis.

## 6. Gouvernance des affirmations et cohérence documentaire

- Employer « hypothèse », « objectif » ou « à valider » pour les propriétés qui n’ont pas encore de preuve ou de test.
- Ne pas qualifier J-DriftX de modèle réglementaire, ni annoncer une conformité réglementaire, avant une procédure d’évaluation adaptée.
- Maintenir un statut de jalon unique entre les pages du site et la feuille de route.
- Vérifier que les citations Quarto, les références bibliographiques et les fiches de lecture concordent.
- Construire le site Quarto et exécuter la CI avant fusion ; le déclenchement d’un workflow de publication ne prouve pas à lui seul que le déploiement a réussi.

## 7. Questions restant ouvertes

1. Le dépôt de la thèse et du chapitre historique est-il possible et autorisé ?
2. Quelles données de terrain peuvent être redistribuées et utilisées pour une validation indépendante ?
3. Quelle licence est compatible avec les droits sur le code historique et les documents ?
4. Quels tests théoriques établissent précisément les propriétés annoncées pour la métrique et les solutions généralisées ?
5. Quel cas d’usage et quelle baseline constituent le test le plus discriminant pour M1 ?

## Références internes

- [Revue de l’état de l’art](02-revue-etat-art-2026.md)
- [Questions scientifiques et techniques ouvertes](https://github.com/JM-Brun/J-DriftX/issues)
- [Références bibliographiques](references.md)
- [Choix de la méthode de revue systématique](06-choix-methode-revue-systematique.md)
