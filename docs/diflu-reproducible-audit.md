# Reproduire le téléchargement et l’audit initial de DIFLU

Cette procédure automatise le travail de récupération et les vérifications qui ont servi à établir les constats de l’issue [#204](https://github.com/JM-Brun/J-DriftX/issues/204). Elle évite de demander à chaque contributeur de retrouver les identifiants de fichiers, de comparer manuellement les formats ou de recompter les catégories.

## Prérequis

- Python 3.12 ou supérieur ;
- accès HTTPS à Recherche Data Gouv ;
- clone du dépôt J-DriftX.

Aucune donnée brute n’est nécessaire dans Git. Les fichiers récupérés et le rapport sont écrits dans un répertoire local ignoré ou choisi par l’utilisateur.

## Exécuter

Depuis la racine du dépôt :

```bash
uv run python scripts/audit_diflu.py
```

Pour choisir un répertoire et un délai d’attente :

```bash
uv run python scripts/audit_diflu.py --output-dir /tmp/diflu-audit --timeout 90
```

Le script résout les fichiers par leur nom dans le listing Dataverse, récupère les métadonnées détaillées, demande explicitement les octets originaux avec `?format=original`, vérifie la taille et le MD5 publiés quand disponibles, calcule un SHA-256, puis écrit `audit-report.json`.

Les trois fichiers de départ sont le tableau des prélèvements, le dictionnaire des médias et le dictionnaire des variables. Le rapport conserve les noms et identifiants Dataverse ainsi que les noms originaux, les URL, les tailles et les contrôles d’intégrité. Il n’inclut pas les octets des données.

## Contrôles inclus

- Le fichier de prélèvements doit exposer les colonnes `sampling_type` et `sampling_bag_id`.
- Les valeurs `EA` doivent porter la valeur littérale `NA` dans `sampling_bag_id`, conformément au dictionnaire.
- Les valeurs `VEGA` doivent avoir un identifiant de sac renseigné.
- Les contrôles d’intégrité échouent explicitement si une taille ou un MD5 publié ne correspond pas.
- Les valeurs `NA` ne sont pas globalement converties en valeurs manquantes.

Le CSV original et l’export TSV transformé de Dataverse ne sont pas interchangeables. L’API annonce, pour le tableau principal, un original de 75 701 octets avec MD5 `d4477017be8efa2ed0f920499c319e3e`, alors que la taille publiée pour l’export TSV ne correspond pas au corps TSV observé pendant l’audit. Le script demande donc l’original explicitement et ne compare pas ses octets à la taille du TSV.

## Tests hors ligne

```bash
uv run pytest tests/test_audit_diflu.py
```

Ces tests simulent les cas de taille/MD5 conformes et non conformes ainsi que la règle sémantique EA/VEGA. Ils n’appellent pas le réseau. L’exécution complète du script constitue, elle, une vérification d’intégration dépendante de la disponibilité de la source.

## Limites

Un contrôle d’intégrité démontre que les octets reçus correspondent aux métadonnées disponibles ; il ne démontre ni la validité scientifique des mesures ni leur exhaustivité. L’audit sémantique actuel ne couvre qu’une règle documentée. L’analyse scientifique plus large (unités, limites de détection, horodatages, nombre d’expériences et partition indépendante des essais) reste une étape distincte et doit être automatisée progressivement à partir des dictionnaires et des critères de l’étude.
