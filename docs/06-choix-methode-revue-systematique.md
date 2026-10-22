# Choix méthodologique pour la revue de l’état de l’art de J-DriftX

> **Statut : protocole méthodologique proposé.** Ce document justifie le choix de la méthode avant la revue bibliographique effective. Il ne décrit pas des résultats de recherche et ne préjuge ni du nombre de références qui seront retenues, ni des conclusions scientifiques.

## 1. Décision en bref

Nous retenons une **revue systématique structurée et traçable, rapportée selon PRISMA 2020**, complétée par quatre éléments adaptés au sujet :

1. une phase exploratoire de *scoping review* pour stabiliser le vocabulaire et cartographier les domaines ;
2. des recherches documentaires explicites et reproductibles dans plusieurs sources bibliographiques ;
3. le *backward* et le *forward citation chasing* (*snowballing*) pour retrouver les travaux fondateurs et les travaux connexes ;
4. une *systematic mapping study* et une évaluation critique de la qualité et de la pertinence des preuves.

Il ne s’agit donc **pas de considérer PRISMA comme une méthode de recherche autonome**. PRISMA 2020 est avant tout une ligne directrice de **reporting** : elle aide à rendre compte de manière complète et transparente de la façon dont les références ont été identifiées, sélectionnées et synthétisées. Les choix de recherche, les critères d’éligibilité, l’extraction et l’évaluation des preuves relèvent du protocole de revue lui-même.

La revue effective fera l’objet d’un changement distinct. Cette PR documente uniquement le raisonnement méthodologique et son mode opératoire prévu.

## 2. Pourquoi une revue systématique pour J-DriftX ?

La question scientifique n’est pas limitée à une discipline ou à une famille de modèles. Elle croise au moins quatre axes :

- **A — Travaux directement liés à Drift-X / J-DriftX** : publications historiques, méthodes sources, prolongements et réutilisations documentés ;
- **B — Réduction de complexité** : modèles d’ordre réduit, solutions de similitude, modèles substituts (*surrogates*), réduction de dimension et méthodes apparentées ;
- **C — Distances et géométries non symétriques en physique** : métriques ou divergences directionnelles, temps de transport et formulations pertinentes pour la dispersion ;
- **D — Réseaux de neurones pour des problèmes comparables** : modèles substituts, opérateurs neuronaux, PINNs, autoencodeurs et modèles réduits appris, lorsque le problème physique et les objectifs sont réellement comparables.

Une recherche narrative seule serait utile pour se familiariser avec ces domaines, mais elle laisserait trop de latitude à la sélection des sources et rendrait difficile l’audit de la couverture. À l’inverse, une méta-analyse quantitative unique n’est pas justifiée a priori : les objets physiques, hypothèses, données, métriques et protocoles peuvent être trop hétérogènes pour agréger les résultats de manière valide.

Le choix vise donc à **réduire le biais de sélection, rendre la recherche répétable et organiser un corpus hétérogène sans forcer une synthèse quantitative artificielle**.

## 3. Comparaison des approches

| Approche | Apport | Limite pour J-DriftX | Décision |
|---|---|---|---|
| Revue narrative / revue traditionnelle | Compréhension rapide, mise en contexte et discussion conceptuelle | Stratégie de sélection parfois implicite ; couverture et biais difficiles à auditer | À utiliser pour l’orientation et l’interprétation, pas comme seul protocole |
| Revue systématique | Question, recherche, critères de sélection et synthèse explicités ; traçabilité du corpus | Exige de délimiter plusieurs axes et de documenter les écarts au protocole | **Cadre principal de la revue** |
| PRISMA 2020 | Checklist et diagramme de flux pour rapporter l’identification, la sélection et l’inclusion des sources | Ne définit pas à elle seule les bases à interroger, les requêtes, la qualité des études ni la méthode de synthèse | **Standard de reporting**, associé à un protocole explicite |
| *Scoping review* / revue de portée | Cartographie un domaine large, clarifie les concepts et révèle le vocabulaire et les sous-domaines | Ne vise pas nécessairement une évaluation approfondie de chaque preuve ou une réponse ciblée à une question d’efficacité | Phase exploratoire, puis intégration des termes et catégories au protocole |
| *Systematic mapping study* | Classe les publications selon les problèmes, méthodes, données, validations et lacunes | Une cartographie seule peut rester descriptive et évaluer insuffisamment la validité des résultats | Complément pour structurer les quatre axes |
| *Backward/forward snowballing* | Retrouve des sources fondatrices, des variantes terminologiques et des travaux citant les articles clés | Dépend des sources de départ et de la couverture des index ; peut amplifier un réseau de citations biaisé | Complément documenté aux recherches par mots-clés |
| Revue critique / évaluation de qualité | Examine les hypothèses, les baselines, la reproductibilité, les données et les limites | Nécessite une grille explicite et adaptée aux types d’études ; peut comporter un jugement subjectif | À appliquer avec une grille publiée dans le protocole |
| Méta-analyse | Agrège quantitativement des résultats compatibles | Suppose une comparabilité suffisante des problèmes, résultats et protocoles | **Pas prévue par défaut** ; envisageable seulement si un sous-corpus est réellement comparable |

## 4. Pourquoi PRISMA 2020 plutôt qu’un autre standard de reporting ?

PRISMA 2020 est retenu comme référence générale parce que le livrable doit permettre à un lecteur de reconstruire le chemin allant des recherches documentaires au corpus finalement analysé. Sa checklist et son diagramme de flux fournissent un cadre reconnu pour rendre visibles les étapes de sélection, les exclusions et les limites de couverture.

Ce choix est **pragmatique et proportionné**, et non l’affirmation que PRISMA serait universellement supérieur :

- **PRISMA 2020** convient au reporting général d’une revue systématique ;
- **PRISMA-ScR** est plus directement adapté au reporting d’une revue de portée ; il pourra servir pour la phase exploratoire si celle-ci devient un livrable autonome ;
- les recommandations de **Kitchenham et Charters** sont historiquement liées aux revues systématiques en génie logiciel. Elles sont utiles pour la discipline du protocole et la traçabilité, mais le sujet de J-DriftX relève surtout de la modélisation physique, des mathématiques appliquées et de l’apprentissage scientifique, pas d’une revue exclusivement logicielle ;
- les pratiques de **snowballing** décrites par Wohlin sont complémentaires : elles renforcent la recherche de références mais ne remplacent ni les recherches par bases, ni les critères d’éligibilité, ni le reporting du processus ;
- une *scoping review* seule serait trop descriptive pour les questions qui nécessitent d’évaluer la solidité des preuves et les comparaisons expérimentales.

PRISMA 2020 ne règle pas tous les problèmes propres à la recherche interdisciplinaire. Il faut donc expliciter les adaptations : axes de recherche séparés, vocabulaire alternatif, distinction entre pertinence directe et analogie méthodologique, et grille critique adaptée à la modélisation et aux études numériques.

## 5. Protocole de travail prévu

### Étape 0 — Fixer les questions et les périmètres

Avant de sélectionner les résultats, définir pour chaque axe les questions, les concepts, les termes alternatifs et les relations recherchées. Séparer systématiquement :

- les références directement liées au projet ou à son héritage ;
- les références méthodologiques analogues ;
- les références de contexte qui aident à interpréter le domaine sans constituer une preuve directe pour J-DriftX.

Ne pas traiter une méthode comme comparable au seul motif qu’elle utilise un réseau neuronal ou une réduction de dimension : la physique, les hypothèses, les observables et le protocole de validation doivent être examinés.

### Étape 1 — Exploration de portée

Réaliser une recherche exploratoire limitée pour repérer les termes historiques, synonymes, auteurs, conférences, revues et travaux de référence. Cette étape sert à améliorer les requêtes finales ; ses résultats ne doivent pas être mélangés silencieusement au corpus systématique. Toute référence découverte à cette étape et retenue ensuite doit repasser par les règles d’éligibilité du protocole.

### Étape 2 — Recherches systématiques

Pour chaque source interrogée, conserver :

- son nom et son périmètre connu ;
- la date et, si possible, l’heure de recherche ;
- la requête exacte, les champs interrogés, les filtres et la période couverte ;
- le nombre de résultats retournés et le format d’export ;
- les erreurs, limites d’accès ou indisponibilités ;
- la version des scripts et des fichiers utilisés pour le traitement.

Les requêtes seront adaptées à la syntaxe de chaque moteur, sans prétendre qu’une même chaîne est exécutée de façon identique partout. Les bases accessibles, leur couverture et les éventuelles restrictions devront être rapportées ; une recherche Google Scholar, par exemple, ne sera déclarée exhaustive que si les conditions d’accès et la méthode d’examen permettent réellement de soutenir cette affirmation.

### Étape 3 — Dédoublonnage et sélection

Conserver les identifiants bibliographiques disponibles (DOI, arXiv ID, HAL ID, URL stable) et documenter la règle de dédoublonnage. Appliquer les critères d’inclusion et d’exclusion dans un ordre défini : titre/résumé, puis texte intégral lorsque celui-ci est accessible.

Chaque exclusion en texte intégral doit avoir un motif enregistré. Si un texte intégral n’est pas accessible, le noter comme tel et distinguer les conclusions fondées sur le résumé de celles vérifiées dans le texte complet. Ne jamais présenter une référence inaccessible comme si son contenu avait été lu.

Le diagramme PRISMA ne sera rempli qu’à partir des comptes réellement produits par ces opérations. Aucun nombre ne doit être estimé ou reconstitué de mémoire.

### Étape 4 — Recherche par citations

Appliquer le *backward snowballing* (références citées) et le *forward snowballing* (publications citantes) à un ensemble de sources de départ justifié. Pour chaque cycle, conserver les sources de départ, l’outil utilisé, la date, les références nouvellement trouvées et leur décision d’éligibilité. Les références trouvées par citations sont soumises aux mêmes critères que les autres.

### Étape 5 — Extraction et cartographie

Pour chaque étude retenue, extraire au minimum : référence vérifiée, année, type de publication, problème physique, hypothèses, méthode, données, baselines, métriques, protocole de validation, disponibilité du code/données, résultats revendiqués, limites et pertinence pour chacun des axes A–D.

La cartographie décrira le corpus sans confondre fréquence de publication et niveau de preuve. Elle permettra notamment d’identifier les axes bien couverts, les zones peu documentées et les comparaisons impossibles faute de données ou de protocoles compatibles.

### Étape 6 — Évaluation critique et synthèse

Utiliser une grille d’évaluation adaptée au type de contribution : théorie, méthode numérique, étude sur données, modèle d’apprentissage ou application. Examiner notamment la clarté des hypothèses, la pertinence des baselines, le risque de fuite de données, la séparation calibration/validation, les analyses d’incertitude, la reproductibilité et la portée réelle des conclusions.

La synthèse sera principalement qualitative et structurée par question. Une agrégation quantitative ne sera envisagée que si la comparabilité des études est défendable et explicitement justifiée.

## 6. Garanties contre les conclusions excessives

La revue doit distinguer trois niveaux dans les textes et tableaux :

1. **Constat documenté** : directement soutenu par une source examinée et citée.
2. **Interprétation de synthèse** : conclusion tirée de plusieurs sources, avec le raisonnement et les limites indiqués.
3. **Hypothèse pour J-DriftX** : proposition à tester par une preuve théorique ou un benchmark ; elle ne devient pas un résultat de la revue par simple absence de contre-exemple dans le corpus.

L’absence de résultat dans les bases interrogées ne prouve pas l’inexistence d’une méthode. Les formulations telles que « premier modèle », « aucun concurrent » ou « supérieur » doivent être évitées, ou précisément bornées par les sources, dates, requêtes et critères effectivement examinés.

La qualité de la revue sera jugée sur la transparence du protocole, la traçabilité des références et la solidité de la synthèse, pas sur le nombre de publications recueillies ni sur le fait que les résultats confirment les choix de conception de J-DriftX.

## 7. Livrables attendus de la PR distincte consacrée à la revue effective

La future PR de revue devra fournir, selon ce que les outils et les accès permettent réellement :

- le protocole final daté, les questions de recherche et les critères d’éligibilité ;
- les requêtes exactes, les sources et dates de recherche ;
- les exports ou manifestes de résultats et les règles de dédoublonnage ;
- les comptes de sélection et les motifs d’exclusion nécessaires au diagramme PRISMA ;
- le corpus bibliographique annoté, avec DOI/URL et statut d’accès au texte ;
- la grille d’extraction et l’évaluation critique ;
- la cartographie des axes A–D, la synthèse des résultats, les lacunes et les limites ;
- les scripts ou instructions nécessaires pour reproduire les transformations lorsque cela est techniquement possible.

La portée de la recherche devra être décrite honnêtement si certains index, textes intégraux ou outils de citation ne sont pas accessibles. L’étiquette « revue systématique reproductible » ne sera revendiquée qu’une fois les éléments nécessaires présents et vérifiés.

## 8. Références méthodologiques

- **PRISMA 2020** — Page officielle, checklist et diagrammes : https://www.prisma-statement.org/prisma-2020
- **PRISMA Extension for Scoping Reviews (PRISMA-ScR)** — Page officielle : https://www.prisma-statement.org/scoping
- **Kitchenham, B. & Charters, S. (2007)** — *Guidelines for performing Systematic Literature Reviews in Software Engineering*. Source historique pour la planification et la conduite de revues systématiques en génie logiciel : https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf
- **Wohlin, C. (2014)** — *Guidelines for snowballing in systematic literature studies and a replication in software engineering*. ESEM 2014. DOI : https://doi.org/10.1145/2601248.2601268

Ces références justifient des composantes de la méthode ; elles ne remplacent pas les décisions spécifiques au domaine scientifique de J-DriftX.

## 9. Liens internes

- [Plan d’intégration scientifique et de validation](05-plan-validation-et-integration.md)
- [Revue de l’état de l’art](02-revue-etat-art-2026.md)
- [Références bibliographiques du projet](references.md)
