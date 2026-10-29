# Reproduire le téléchargement et l’audit initial de DIFLU

Cette procédure automatise le travail de récupération et les vérifications qui ont servi à établir les constats de l’issue [#204](https://github.com/JM-Brun/J-DriftX/issues/204). Elle évite de demander à chaque contributeur de retrouver les identifiants de fichiers, de comparer manuellement les formats ou de recompter les catégories.

## Prérequis

- Python 3.12 ou supérieur ;
- accès HTTPS à Recherche Data Gouv pour récupérer les originaux ;
- clone du dépôt J-DriftX.

Le téléchargement et les tests hors ligne sont deux opérations distinctes. Les données téléchargées sont conservées localement dans un répertoire ignoré par Git.

## Télécharger et auditer

Depuis la racine du dépôt :

```bash
uv run python scripts/audit_diflu.py
```

Pour choisir un répertoire et un délai d’attente :

```bash
uv run python scripts/audit_diflu.py --output-dir /tmp/diflu-audit --timeout 90
```

Le script résout les fichiers par leur nom dans le listing Dataverse, récupère les métadonnées détaillées, demande explicitement les octets originaux avec `?format=original`, vérifie la taille et le MD5 publiés quand disponibles, calcule un SHA-256, puis écrit `audit-report.json`.

Les trois fichiers de départ sont le tableau des prélèvements, le dictionnaire des médias et le dictionnaire des variables. Le rapport conserve les noms et identifiants Dataverse ainsi que les noms originaux, les URL, les tailles et les contrôles d’intégrité.

## Préparer un corpus de référence versionnable

Les trois fichiers compacts peuvent être versionnés afin que les audits sémantiques et les tests hors ligne ne dépendent pas de la disponibilité du réseau. Le dossier `/data/raw/` reste ignoré : aucun téléchargement local ne doit y être ajouté directement.

Après un audit réussi, exécuter :

```bash
uv run python scripts/vendor_diflu_reference.py
```

Le script lit le rapport de l’audit et vérifie à nouveau les octets sources contre la taille, le MD5 et le SHA-256 enregistrés avant de les copier vers `tests/fixtures/diflu/source/`. Il refuse de continuer si les sources ont changé depuis l’audit, si les contrôles officiels de taille/MD5 ne sont pas confirmés, ou si un fichier de destination existant contient d’autres octets. Les fichiers ne sont jamais transformés. Un `manifest.json` déterministe documente provenance, URL, identifiants Dataverse, taille, MD5 et SHA-256.

Les fichiers copiés et le manifeste doivent être inspectés puis ajoutés à Git dans une PR. Le dépôt ne doit pas inclure le ZIP complet, les séries temporelles météo/micrométéo, ni les médias volumineux par défaut. Voir aussi [le README du corpus de référence](../tests/fixtures/diflu/source/README.md).

## Contrôles inclus

- Le fichier de prélèvements doit exposer les colonnes `sampling_type` et `sampling_bag_id`.
- Les valeurs `EA` doivent porter la valeur littérale `NA` dans `sampling_bag_id`, conformément au dictionnaire.
- Les valeurs `VEGA` doivent avoir un identifiant de sac renseigné.
- Les contrôles d’intégrité échouent explicitement si une taille ou un MD5 publié ne correspond pas.
- Les valeurs `NA` ne sont pas globalement converties en valeurs manquantes.

Le CSV original et l’export TSV transformé de Dataverse ne sont pas interchangeables. L’API annonce, pour le tableau principal, un original de 75 701 octets avec MD5 `d4477017be8efa2ed0f920499c319e3e`, alors que la taille publiée pour l’export TSV ne correspond pas au corps TSV observé pendant l’audit. Le script demande donc l’original explicitement et ne compare pas ses octets à la taille du TSV.

## Tests hors ligne

```bash
uv run pytest tests/test_audit_diflu.py tests/test_vendor_diflu_reference.py
```

Ces tests simulent les cas de taille/MD5 conformes et non conformes, la règle sémantique EA/VEGA et les garanties du processus de staging. Ils n’appellent pas le réseau. L’exécution complète des scripts constitue, elle, une vérification d’intégration dépendante de la disponibilité de la source.

## Limites

Un contrôle d’intégrité démontre que les octets reçus correspondent aux métadonnées disponibles ; il ne démontre ni la validité scientifique des mesures ni leur exhaustivité. L’audit sémantique élargi de la PR #251 rapporte les comptes par expérience, les marqueurs `NA`/`< LC` par colonne, la cohérence des drapeaux de détection, les durées d’échantillonnage, les clés d’identité répétées et les plages numériques observées. Ces diagnostics ne prouvent ni l’indépendance statistique des expériences, ni la validité physique des variables, ni l’adéquation de l’ATC. Le fixture versionné sert de test de régression, pas de substitut à l'examen scientifique.
