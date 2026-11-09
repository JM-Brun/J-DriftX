# Thèse de Brun — inventaire local des éléments historiques

**État au 9 novembre 2026 : recherche bornée, pas preuve d'absence générale.** Cet inventaire sert TH-07 dans la [liste des travaux](these-travaux-restants.md). Il distingue les documents consultables, les observations imprimées et les fichiers nécessaires à une reproduction. Il ne donne aucun droit nouveau de redistribution et ne relance aucune acquisition.

## Périmètre et méthode

La recherche a porté sur l'arbre de travail local J-DriftX, y compris des fichiers ignorés, à la révision `d6127fb9d9568e18501fbe0bfa15a0fe281624fe` avec modifications préexistantes, et sur le clone de travail propre à la révision `320f18377750430116c1241f8c729534c56810cf`. Les deux arbres n'ont pas le même état ; les résultats sont rapportés avec leur périmètre. Les environnements, caches et répertoires Git ont été exclus de la recherche de fichiers locale. Aucun contenu de fichiers personnels externes au projet ni aucune archive distante n'a été exploré.

- Inventaire par nom de fichiers de données, d'archives et de codes usuels : `.csv`, `.tsv`, `.xls`, `.xlsx`, `.mat`, `.dat`, `.nc`, `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.for`, `.f90`, `.m` et `.exe` ; recherche par noms évoquant Drift-X, Brun, la canopée, BMO ou 2005. Les extensions, majuscules et noms inattendus peuvent échapper à ce filtre.
- Recherche textuelle ciblée dans `docs/`, `raw/`, `data/`, `src/`, `tests/` et `benchmarks/` sur la date de l'essai, Montpellier, les collecteurs, BMO et Fortran. Elle n'analyse pas le contenu de toutes les images, tous les PDF ou tous les fichiers binaires.
- Dans le clone propre, recherche de noms d'archives, de fichiers Fortran et des chaînes `2005`, `Gil` et `BMO` dans l'historique Git des références disponibles : aucun chemin ne correspond aux motifs testés. Elle ne couvre ni toutes les orthographes, ni les références Git non présentes, ni le contenu de chaque ancienne révision.
- Avec `pypdf.PdfReader(...).attachments`, les six PDF situés directement dans `raw/` du clone n'exposent aucune pièce jointe. Cela ne démontre rien sur les données publiées ailleurs ou sur un fichier incorporé par un autre mécanisme.

Ces contrôles décrivent un instantané des éléments accessibles, pas l'historique complet du projet ni les archives privées déjà obtenues mais non localisées dans ces arbres.

Pour répéter les contrôles de noms et d'empreintes depuis la racine de l'arbre considéré :

```sh
rg --files --hidden --no-ignore -g '!.git/**' -g '!.venv/**' -g '!_site/**' -g '!site/_site/**' -g '!**/__pycache__/**' -g '!**/.quarto/**' -g '!**/.pytest_cache/**' -g '!**/.mypy_cache/**' -g '!**/.ruff_cache/**' -g '!**/node_modules/**' -g '*.{zip,tar,gz,7z,rar,csv,tsv,xls,xlsx,mat,dat,nc,for,f90,m,exe}'
git log --all --format= --name-only -- '*.zip' '*.tar' '*.gz' '*.7z' '*.rar' '*.f' '*.f90' '*.for' '*2005*' '*Gil*' '*gil*' '*BMO*' '*bmo*'
shasum -a 256 tests/fixtures/diflu/source/DIFLU_*.csv
```

La seconde commande n'inspecte que les références Git présentes ; les fichiers `data/raw/diflu-audit/` ne sont pas garantis présents dans un autre arbre. L'inspection des pièces jointes utilise la propriété `attachments` de `pypdf` sur les PDF directement sous `raw/`.

## Éléments distingués

| Élément | Identification et preuve | Ce que l'élément permet, et ce qui manque |
|---|---|---|
| Thèse versionnée | [PDF dans `raw/`](../../raw/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf), SHA-256 local `5594e31d9b220dbd25d21e93e54939d9c1dfdf3e7bb39c5544b1ad1d8d44ba2c` ; [provenance](../../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md) | Protocole, moyennes et figures des pp. imprimées 103–107, paramètres et équations historiques. Les cinq mesures par ligne et par essai, leurs métadonnées et les réglages complets ne sont pas établis par ces passages. L'identité binaire avec HAL et les droits sont deux questions distinctes. |
| Référence de l'essai | La thèse cite Gil, Sinfort, Brunet, Polveche et Bonicelli, *Loss of spray above an artificial vineyard during air-assisted spraying*, indiqué comme soumis en 2006, bibliographie p. 184 (PDF 193). | Piste bibliographique ciblée, déjà identifiée dans la [fiche](../bibliographie/sources/these-brun.md). La recherche locale ciblée n'a pas identifié le texte ou le jeu individuel associé ; ni l'identité d'une version ultérieure ni ses droits ne sont établis. |
| Manuscrit plateforme | [Manuscrit HAL 2009](../../raw/2009-bozon-sinfort-mohammadi-driftx-hal.pdf), SHA-256 `e102ff7a98a5489e258ff6dd82c9d5d2bf6542475ab47c7c250c2c5ae646745d` ; [provenance et distinction des versions](../../raw/provenance/2009-bozon-sinfort-mohammadi-driftx-hal.pdf.md) | Décrit notamment une architecture Fortran et des échanges de fichiers ; cette description n'est pas le code source. Les conditions de réutilisation restent à vérifier. Ne pas le confondre avec le PDF final JESA 2010, déjà obtenu mais dont le binaire distinct reste à localiser dans les éléments archivés. |
| Note 2006 | [PDF éditeur](../../raw/2006-mohammadi-brun-crmeca.pdf), SHA-256 `230990bb30919b4853613a3eecaa3c4de0766a04bccae74c6bcf5680465315cc` ; [provenance](../../raw/provenance/2006-mohammadi-brun-crmeca.pdf.md) | Source mathématique primaire, pas une archive des essais ou du code. L'existence du PDF ne prouve pas le droit de redistribution. |
| Fichiers DIFLU | Trois CSV présents dans [`tests/fixtures/diflu/source/`](../../tests/fixtures/diflu/source/README.md) et dans `data/raw/diflu-audit/` de l'arbre partagé ; [manifest versionné](../../tests/fixtures/diflu/source/manifest.json) et empreintes comparées ci-dessous. | Jeu sur des rejets d'hélium d'une autre campagne : ne remplace ni les collecteurs fluorimétriques de l'essai viticole de 2005 ni sa météorologie. La licence indiquée dans le manifest est propre à DIFLU et ne s'étend pas à la thèse ou à d'autres données. |
| Code et paramètres historiques | La recherche par noms et les mentions textuelles examinées n'ont identifié ni archive de code de canopée/BMO ni fichier de paramètres historiques associé à l'essai. | Résultat négatif limité aux motifs et chemins ci-dessus. Le Python actuel est un projet exploitable, mais sa présence n'établit pas qu'il soit une copie du code historique. Versions, empreintes et droits d'un éventuel code ancien restent à établir après identification. |

## Contrôle d'identité des trois copies DIFLU

Le 9 novembre, les SHA-256 calculés sur chaque paire `data/raw/diflu-audit/` et `tests/fixtures/diflu/source/` sont identiques, et concordent avec le manifest versionné :

| Fichier | SHA-256 des deux copies |
|---|---|
| `DIFLU_helium_release_sampling.csv` | `de0ec5e2deeb2720b6d22abe54d749f99fb5827bd426ea7855c48acb3d1a8314` |
| `DIFLU_media_dictionary.csv` | `b779f88706e7495476413f550af162548dba34f2a8470e43e8635ef53ae82f4a` |
| `DIFLU_variables_dictionary.csv` | `749d2495d146ceca8c05580bd4074f8de21e14660cdae397da1f8ba250ae4f17` |

Cette égalité est locale : elle ne certifie pas à elle seule l'origine distante, les droits ou l'aptitude scientifique des données. Le dictionnaire média situe notamment des observations d'hélium en 2019 ; la thèse situe son essai de pulvérisation à Montpellier le 13 juillet 2005. Il s'agit d'une incompatibilité de campagne et d'observable, non d'un jugement sur l'utilité de DIFLU pour une autre question.

## Reprise ciblée

1. Localiser dans les éléments déjà obtenus, lorsqu'un emplacement exploitable est identifié, les fichiers de mesures par collecteur et essai, le volume pulvérisé, les étalonnages et les données météo. Conserver leur origine, version, empreinte et droits ; ne pas fabriquer les valeurs à partir des moyennes ou de la figure.
2. Identifier une éventuelle archive ou copie de code de canopée, de l'optimiseur et de son paramétrage ; confronter sa version, ses unités et son comportement à l'annexe C et au contrat de [calage](these-calage-identification-sources.md). Une recherche de noms négative ne démontre pas qu'elle n'existe pas.
3. Retrouver le chemin de la copie finale JESA déjà obtenue, sans nouvel accès, pour la comparaison de versions suivie par son [sidecar](../../raw/provenance/2010-bozon-sinfort-mohammadi-jesa.pdf.md). Ne pas substituer le manuscrit HAL 2009.

Tant que ces éléments ne sont pas identifiés, la reproduction historique reste non démontrée et l'évaluation indépendante TH-08 reste en attente de données et de droits. TH-07 reste ouverte pour ces recherches ciblées ; les résultats négatifs de ce seul inventaire ne sont pas étendus au-delà de son périmètre.
