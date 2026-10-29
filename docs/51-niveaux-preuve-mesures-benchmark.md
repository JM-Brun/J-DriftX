# 51 — Niveaux de preuve des mesures de coût et artefacts de benchmark

**Objet :** empêcher de confondre l'instrument de mesure, le protocole prévu, les mesures produites pendant une exécution et les résultats conservés dans Git.

## 1. Trois objets distincts

| Objet | Contenu | Preuve suffisante | Ce qu'il ne prouve pas |
|---|---|---|---|
| **Protocole de benchmark** | Cas, entrées, variantes comparées, répétitions, échauffement, métriques, tolérances, coûts inclus/exclus, environnement à relever et commande | Document versionné avant l'expérience, avec paramètres non ambigus | Qu'une exécution a eu lieu ou qu'une mesure existe |
| **Mesures d'une exécution** | Durées brutes, statistiques dérivées, erreurs, mémoire mesurée, métadonnées réelles de l'environnement et identifiant de l'exécution | Sortie produite par une invocation identifiée ; journaux ou artefact récupérable ; idéalement empreinte du fichier | Que ces mesures sont représentatives d'autres machines ou qu'elles valident le modèle physique |
| **Artefact de résultats versionné** | Fichier JSON/CSV/rapport archivé dans Git ou dans un stockage identifié, avec provenance et lien vers le protocole | Fichier effectivement retrouvé, version, empreinte, protocole associé et contexte d'exécution | Que l'absence d'un tel fichier signifie qu'aucune mesure n'a été produite ailleurs |

**Règle d'inférence :** « aucun artefact de résultat n'est présent dans l'arbre Git examiné » signifie seulement que le résultat n'a pas été retrouvé dans cet arbre et cette révision. Cela ne permet pas de conclure que le benchmark n'a jamais été exécuté, que les mesures n'ont pas été imprimées sur stdout, ni qu'elles n'ont pas été conservées dans un autre emplacement, une CI, un poste de travail ou un artefact externe. Documenter ces possibilités comme **non vérifiées**, pas comme inexistantes.

## 2. Application au benchmark S0 uniforme — étape 5

Le [protocole de coûts](50-protocole-oracle-couts-baseline-uniforme.md) décrit les mesures attendues : échauffement exclu, répétitions chronométrées, statistiques descriptives, coût de préparation du cas et de la grille, coût d'une grille de 12 points, coût médian par point et pic d'allocations Python suivies par `tracemalloc`.

- Le protocole versionné est une **spécification** ; il n'est pas une mesure.
- Le script `scripts/benchmark_baseline_uniforme.py` est un **instrument**. Ses sorties en mémoire ou sur stdout sont des mesures d'une exécution, même si aucun JSON n'est commité.
- L'option `--output artifacts/baseline-uniforme-step5.json` demande l'écriture d'un fichier. La seule présence de cette commande dans la documentation ne prouve pas qu'elle a été exécutée.
- Un JSON présent dans Git est un **artefact versionné** ; il doit être associé à une révision du code, un protocole, un environnement et une date d'exécution. Ne pas le remplacer silencieusement par un nouveau résultat : conserver l'historique ou créer un artefact distinct.
- Une sortie CI peut fournir une mesure d'exécution, mais elle ne doit pas être présentée comme une mesure de référence stable sans qualification de l'environnement et du contexte CI.

Le protocole et le script actuels ne démontrent pas, à eux seuls, si une exécution passée a eu lieu. Pour établir cet historique, inspecter les sorties et artefacts CI, les journaux disponibles et les fichiers d'exécution déjà produits avant de lancer une nouvelle campagne. Cette inspection n'est pas une nouvelle acquisition de source scientifique.

## 3. Métadonnées minimales à conserver

Pour chaque exécution exploitable, conserver autant que possible :

- identifiant d'expérience et version de schéma ;
- date/heure UTC de début, commande et nombre de répétitions ;
- commit Git exact, état propre/sale du répertoire et version du script ;
- paramètres, cas, grille, métriques et tolérances effectivement utilisés ;
- versions Python, OS/plateforme, dépendances pertinentes et méthode de mesure ;
- mesures brutes et statistiques calculées, unités explicites ;
- chemin de sortie, SHA-256 de l'artefact et statut de validation ;
- limites d'interprétation, notamment la distinction entre mémoire tracée Python et mémoire résidente, et entre coût de préparation et coût d'inférence.

Si une métadonnée n'est pas disponible pour une exécution historique, la marquer **inconnue/non enregistrée**. Ne pas reconstruire artificiellement un commit, un horodatage ou un environnement.

## 4. Politique de versionnement

1. Garder le protocole et les seuils pré-enregistrés versionnés indépendamment des résultats.
2. Archiver chaque exécution retenue sous un nom distinct ou un identifiant stable ; ne pas écraser un résultat précédent.
3. Ne versionner que les artefacts nécessaires à l'audit/reproduction ; si les fichiers sont volumineux, utiliser un stockage d'artefacts traçable et versionné et consigner son URI, son empreinte et sa rétention.
4. Distinguer explicitement « protocole prêt », « exécution lancée », « mesures récupérées », « résultat archivé » et « interprétation validée ».
5. Ne pas utiliser un test logiciel de cohérence numérique comme preuve de performance ; ne pas utiliser une mesure de performance comme preuve de validité physique.

## 5. État des preuves

À la date de rédaction, le dépôt contient le protocole et le script de l'étape 5. L'absence d'un fichier de résultat dans la révision inspectée n'est pas une preuve que les mesures n'ont jamais été produites. L'existence, la récupération et l'archivage de sorties antérieures doivent être vérifiés séparément avant de déclarer l'expérience non exécutée.

Voir aussi : [protocole de coûts S0](50-protocole-oracle-couts-baseline-uniforme.md), [squelette de benchmarks S0](39-squelette-benchmarks-s0.md), [issue #244](https://github.com/JM-Brun/J-DriftX/issues/244).
