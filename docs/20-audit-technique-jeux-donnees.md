# Audit technique des jeux de données candidats — accès, licences et fichiers (issue #13)

> **Statut : audit exécuté le 23 octobre 2026**, suite de l'[audit documentaire G0](15-audit-corpus-g0-resultats.md). Objet : vérifier, depuis les **sources primaires**, l'accès réel, les licences, les formats de fichiers annoncés, l'unité d'indépendance des essais et la compatibilité physique de chaque corpus avec l'observable retenu (concentration aérienne, [issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)).
> **Limite de méthode explicite.** Les fichiers de données eux-mêmes n'ont pas pu être téléchargés ni inspectés unité par unité depuis l'environnement d'audit (accès automatisés bloqués : 403 sur le site NOAA, entrepôt Dataverse protégé contre les robots, page 4TU illisible pour les outils, archives binaires). Ces points sont consignés comme **non vérifiés** ci-dessous, jamais comme validés. Le téléchargement manuel et l'inspection des fichiers restent le prérequis suivant, avant tout benchmark — l'[issue #13](https://github.com/JM-Brun/J-DriftX/issues/13) reste ouverte jusqu'à cette étape.

## Synthèse

| Corpus | Accès distant (23/10/2026) | Licence (source primaire) | Unité d'indépendance | Compatible avec l'observable (concentration aérienne) | Reste à vérifier sur fichiers |
|---|---|---|---|---|---|
| [DIFLU](https://doi.org/10.57745/A9YC3C) ([Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C)) | Fiche actuelle du dépôt accessible publiquement ; archives de données annoncées ~381 Mo | **Licence Ouverte Etalab 2.0 affichée sur la fiche du dépôt** ; DataCite `rightsList` vide, conserver une copie de la fiche et vérifier les métadonnées par fichier | Le lâcher (15 expériences explicitement décrites par l’article ; une valeur 19 a été relevée dans des métadonnées indexées, mais son champ et sa signification comme nombre d’essais ne sont pas établis) | Oui — gaz traceur passif, champ proche < 500 m, couche de surface | Intégrité, unités, limites de détection, données manquantes, identification de la valeur 19 dans les métadonnées, décompte des lâchers, métadonnées par fichier |
| [NOAA DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) | Page officielle en 403 pour les accès automatisés ; contenu documenté via [snapshot d'archive (8 juin 2026)](https://web.archive.org/web/20260608053910/https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) | Aucune licence formelle affichée ; **attribution NOAA ARL demandée** pour les publications | L'expérience (la campagne) | Oui — traceurs far-field (dizaines à milliers de km) | Contenu des fichiers texte (unités par expérience), périmètre exact des 9 expériences listées |
| [ETEX / JRC](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm) | Page de téléchargement active : **quatre archives** (météo × traceur, lâchers 1 et 2) | Pas de licence par fichier ; **notice générique open data JRC** (© Union européenne, décision 2011/833/EU, Creative Commons) à confirmer pour ces fichiers | Le lâcher (**n = 2 seulement**) | Oui — traceur perfluorocarboné au sol, échelle continentale | Unités, complétude, contenu des archives météo |
| [ERIES](https://doi.org/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf) (4TU.ResearchData) | DOI actif (version 2, mars 2026) ; page d'accueil illisible pour les outils, métadonnées Datacite complètes | **CC BY 4.0 confirmée** (SPDX cc-by-4.0) — seule licence pleinement vérifiée aujourd'hui | La configuration (source S1/S2 × vent) : 2 essais ; la répétabilité quantifie l'incertitude | Oui — scalaire passif neutre, mais **échelle réduite** (soufflerie, 1:350) | Structure des fichiers (xlsx, txt, Matlab), unités, incertitudes chiffrées |

## 0. Méthode et limites

Consulté le 23 octobre 2026, en sources primaires uniquement :

- **DIFLU** : la fiche actuelle de [Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C) est accessible via le web et affiche la **Licence Ouverte Etalab 2.0**. La fiche DataCite du même DOI a toujours un `rightsList` vide : c'est une différence entre les couches de métadonnées, pas une preuve d'absence de licence sur le dépôt. La fiche annonce des fichiers téléchargeables ; aucun n'a été téléchargé ni inspecté pendant cette vérification.
- **DATEM** : le site officiel NOAA ARL rejette les accès automatisés (403 CloudFront) ; la page a été documentée via un snapshot d'archive web du 8 juin 2026, complété par les extraits des pages d'évaluation HYSPLIT/DATEM indexées.
- **ETEX** : les pages JRC (remon.jrc.ec.europa.eu) sont accessibles et ont été lues directement ; la notice de copyright open data JRC est constatée sur le portail open data (jeux voisins), pas sur les fichiers ETEX eux-mêmes.
- **ERIES** : métadonnées Datacite complètes du DOI 10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf, incluant licence, description détaillée, formats et liens de financement ; la page 4TU.ResearchData elle-même est illisible pour les outils.

**Les octets des fichiers de données n'ont pas pu être téléchargés ni inspectés** dans cette passe. Précision du 28/10/2026 pour ETEX : l'index de téléchargement et le répertoire de la deuxième campagne sont lisibles et donnent noms, tailles et dates des fichiers, mais le navigateur ne restitue pas le contenu des fichiers binaires et le téléchargement direct depuis l'environnement d'audit a échoué. Le répertoire de la première campagne a expiré en accès automatisé. Les unités, limites de détection, trous et formats internes restent donc non vérifiés : la visibilité d'un listing n'est pas une inspection du corpus. Conformément au critère de l'issue #13, ces points sont déclarés non vérifiés, et non validés.


### Mise à jour — 28 octobre 2026 : prudence sur le nombre d’expériences DIFLU

La lecture de la copie indexée de l’article associé (*Atmosphere* 2022, 13, 1223 ; [PDF consultable](https://pdfs.semanticscholar.org/52d1/ce7cffca878851e9a0aa91ca675ea2bd72b7.pdf)) identifie **15 expériences** : 7 en octobre 2019 et 8 en décembre, avec 194 prélèvements d’air sous le vent. La notice indexée indique 387 observations pour `DIFLU_helium_release_sampling.tab` (21 variables), tandis que `DIFLU_media_dictionary.tab` comporte 19 observations. Ni 387 observations ni 19 lignes d’un dictionnaire ne prouvent l’existence de 19 expériences. La valeur 19 reste à localiser précisément dans la notice ou les fichiers. Les données brutes n’ayant pas été téléchargées, cette correction concerne l’interprétation des éléments documentaires disponibles et ne constitue pas une inspection du corpus.

## 1. DIFLU — traceur hélium contrôlé, Beuvry (France) : corpus principal du test discriminant

| Point | Vérification (23/10/2026) | Résultat |
|---|---|---|
| Accès | DOI [10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C), [fiche du dépôt](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C) consultée via indexation web le 28/10/2026 ; producteur ASNR, auteurs Laguionie, Connan, Darmau. La fiche annonce deux archives ZIP (381,2 MB originales ; 380,9 MB tabulaires) et 114 fichiers ; dix premiers listés, avec métadonnées de taille, variables et observations | Accès public et structure du dépôt confirmés par la fiche indexée ; les archives complètes et les fichiers de mesures n'ont pas été téléchargés ni inspectés |
| Licence | DataCite `rightsList` **vide** ; fiche actuelle Recherche Data Gouv affichant la Licence Ouverte Etalab 2.0 | **Licence indiquée sur la fiche du dépôt** ; conserver la fiche/notice de licence et vérifier les métadonnées des fichiers précis au téléchargement |
| Terme source | Hélium libéré à débit massique contrôlé dans le flux d'air sortant de la cheminée du cyclotron hospitalier de Beuvry (description Datacite) ; site 50,51404° N, 2,67255° E (papier associé) | Oui, contrôlé et documenté |
| Campagnes et temps | L’article associé décrit 15 expériences réparties entre deux campagnes (7 en octobre 2019 et 8 en décembre), jusqu’à environ 560 m ; la période météo annoncée s’étend du 8 octobre 2019 au 7 janvier 2020. Une valeur 19 apparaît dans les informations indexées, mais le champ qui la porte n’est pas identifié comme un décompte d’expériences | Les 15 expériences sont attestées par l’article ; ne pas présenter 19 comme un nombre d’essais confirmé sans identifier la métadonnée source. Les fichiers restent non inspectés |
| Mesures | Concentrations par **échantillonnage discret et suivi continu en temps réel** (description Datacite) ; micrométéorologie co-localisée | Structure documentée ; unités à vérifier sur fichiers |
| Complétude | Non vérifiable sans les fichiers | **Non vérifié** — limites de détection, données manquantes : à documenter au téléchargement |
| Essais indépendants | **L’expérience/lâcher est l’unité d’indépendance** ; l’article associé (*Atmosphere* 13(8):1223) décrit 15 expériences. Le nombre 19 ne doit pas être interprété comme un décompte d’essais tant que sa métadonnée d’origine n’est pas identifiée | n = 15 est attesté par l’article ; le sens de la valeur 19 reste indéterminé. Ne pas partitionner les observations comme si elles étaient des essais indépendants |
| Compatibilité observable | Gaz traceur passif en champ proche (< 500 m), couche de surface, environnement urbain peu dense | Conforme à l'observable primaire (concentration aérienne) ; **ne teste pas la dérive de pulvérisation** (rejet de cheminée, pas de buse ; gaz, pas de gouttelettes) |

**Verdict : corpus principal candidat retenu sous réserve** pour le test discriminant de l'[issue #43](https://github.com/JM-Brun/J-DriftX/issues/43). La licence Etalab 2.0 est affichée sur la fiche du dépôt ; avant benchmark, restent obligatoires l’inspection des fichiers, la vérification des unités/limites de détection et l’identification de la métadonnée qui porte la valeur 19. À ce stade, 15 expériences sont attestées par l’article ; une contradiction « 19 vs 15 essais » n’est pas établie.

## 2. NOAA DATEM — archive longue distance : périmètre corrigé

La page officielle (snapshot du 8 juin 2026) précise le périmètre de l'archive :

- **Étude pilote fondatrice : cinq expériences de dispersion longue distance**, plus de **19 000 échantillons de concentration d'air**, champs de réanalyse NCAR/NCEP, programmes d'analyse statistique fondés sur l'évaluation ATMES-II d'ETEX ([Draxler et al., document DATEM](https://www.arl.noaa.gov/documents/datem/document/datem.pdf)).
- **Fichiers** : émissions et prélèvements en **fichiers texte délimités par des espaces** (lisibles par Fortran ou tableur) ; météorologie reformatée pour HYSPLIT (format ARL) en trois jeux : réanalyse globale 2,5°, réanalyse nord-américaine 32 km (NARR), WRF CONUS 27 km ; programmes statistiques en **Fortran avec sources** et exécutables PC ; logiciels de tracé ; configuration et résultats de modèles fournis.
- **Licence** : aucune licence formelle n'est affichée ; la page demande une **attribution NOAA ARL** dans les publications (texte d'exemple fourni). Données d'agence fédérale américaine — conditions de réutilisation à documenter avant toute redistribution.
- **Périmètre actuel : la page d'évaluation HYSPLIT/DATEM liste neuf expériences de traceurs contrôlés**, dont ACURATE, ANATEX, OKTEX, METREX, INEL74, SRPTEX **et ETEX** (lâcher de Rennes, octobre 1994) ; trois d'entre elles (INEL74, SRPTEX, ETEX) sont exclues de l'évaluation approfondie HYSPLIT (hors Amérique du Nord ou antérieures à 1980). **Ceci corrige la réserve de l'[audit G0](15-audit-corpus-g0-resultats.md)** (« ETEX absent de l'archive DATEM ») : c'était vrai du document pilote, pas de l'archive actuelle.

**Verdict :** accès et formats documentés par des sources primaires ; licence informelle (attribution) ; unité d'indépendance = l'expérience/campagne. Les fichiers texte restent à télécharger pour vérifier les unités expérience par expérience.

## 3. ETEX (JRC) — traceur continental : accès confirmé, n = 2

| Point | Vérification (23/10/2026) | Résultat |
|---|---|---|
| Accès | Page [Download datasets](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm) ; listing du répertoire Release 2 lisible le 28/10/2026. Il expose `pmcp.codv1.2` (32 406 octets), `pmcp.datv1.2` (32 403), `pmcp.readmev1.2`, `release2.txt`, `stationlist.950130` et le sous-répertoire `meteodat_2` | Présence et arborescence des fichiers Release 2 vérifiées au niveau HTTP ; téléchargement/lecture des octets de données non réalisé. Le répertoire Release 1 n'a pas pu être ouvert par l'outil (timeout). |
| Licence | Aucune licence affichée sur la page ; la distribution open data JRC applique la notice standard (© Union européenne, décision du 12 décembre 2011 sur la réutilisation des documents de la Commission, licence Creative Commons) | **Notice générique JRC, non confirmée fichier par fichier** — à documenter au téléchargement |
| Terme source | Lâcher 1 : 23/10/1994, 16:00 UTC, 340 kg de PMCH, 12 h ; lâcher 2 : 14/11/1994, 15:00 UTC, PMCP (490 kg ; 11,6 g/s, conditions de rejet documentées : température moyenne du gaz 73,4 °C, point de rosée −12,7 °C), 12 h ; site de Monterfil (Bretagne) | Oui, contrôlé et documenté |
| Mesures | 168 stations au sol dans 17 pays ; prélèvements d'environ 3 h pendant ~90 h après le rejet ; environ 9 000 échantillons au total sur les deux expériences | Documenté ; unités à vérifier sur fichiers |
| Essais indépendants | **Deux lâchers seulement**, dans des conditions météorologiques différentes | n = 2 : chaque lâcher fournit des centaines de couples station-temps, mais la généralisation reste limitée ; **réserver un lâcher comme test final (G3)**, jamais utilisé pour le calibrage |

**Verdict :** accès et termes source confirmés ; licence à confirmer au téléchargement ; réserve structurelle n = 2 inchangée.

## 4. ERIES — base de validation en soufflerie (nouvel entrant de l'audit)

| Point | Vérification (23/10/2026) | Résultat |
|---|---|---|
| Accès | DOI [10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf](https://doi.org/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf), 4TU.ResearchData, **version 2 du 23 mars 2026** ; page d'accueil illisible pour les outils, métadonnées Datacite complètes | Accès public documenté |
| Licence | **CC BY 4.0 International** (SPDX cc-by-4.0) dans les métadonnées Datacite | **Confirmée — seule licence pleinement vérifiée aujourd'hui** |
| Dispositif | Maquette du centre-ville de Sofia (Bulgarie), région d'environ 0,91 km de diamètre, soufflerie à couche limite atmosphérique de TU Eindhoven (circuit fermé), **échelle géométrique 1:350**, taux de blocage < 5 % | Documenté |
| Mesures | Concentrations en **76 points** répartis dans la zone cible, pour **deux sources ponctuelles S1 et S2** (deux jeux indépendants), à une hauteur réduite de 5 mm ; traceur **éthylène pur**, rejet **neutre** (sans flottabilité) ; vent dominant ouest-nord-ouest (293°, 0° = nord vrai) ; écoulement d'approche selon la ligne directrice VDI-3783 (terrain rugueux) | Documenté ; unités à vérifier sur fichiers |
| Incertitude | Essais d'**indépendance en Reynolds**, de **sensibilité à la force de source** et **répétabilité multiple** conduits pour quantifier l'incertitude expérimentale | Documenté ; valeurs chiffrées à extraire des fichiers |
| Fichiers | Formats annoncés : pdf, stp, jpg, xlsx, m (Matlab), asA, thA, txt ; rapport de métadonnées + **séries temporelles brutes** de concentrations, conditions d'approche et conditions ambiantes | Structure documentée ; inspection à faire |
| Contexte | Supplément du chapitre Springer [10.1007/978-3-031-98893-6_9](https://doi.org/10.1007/978-3-031-98893-6_9) ; projet ERIES (Horizon Europe, GA 101058684) ; auteurs Gillmeier, Radhakrishnan Jayakumari, Hristov, Pentusheva, Mitkov (TU/e, GATE Institute « Future Cities », Chalmers Digital Twin Cities) | Documenté |

**Verdict :** licence ouverte confirmée (CC BY 4.0), dispositif et incertitudes documentés. **Mais échelle réduite** (soufflerie 1:350, vent unique, pas de terrain réel) : la comparabilité avec un panache atmosphérique grandeur nature est limitée par construction (similarité en Reynolds, turbulence, rugosité) — utilisable pour éprouver la structure du modèle sur un écoulement canopée urbaine, pas pour valider la physique atmosphérique réelle.

## 5. Limites de comparabilité entre les corpus (et avec la dérive de pulvérisation)

- **Traceur gazeux ≠ gouttelettes.** Aucun des quatre corpus ne mesure une dérive de pulvérisation : DIFLU simule un rejet de cheminée (gaz), ETEX/DATEM des traceurs gazeux, ERIES un gaz traceur en soufflerie. Pas de distribution de tailles de gouttes, pas de dépôt liquide, pas d'évaporation. La dérive de pulvérisation n'est **pas validée** par ces corpus.
- **Échelles disjointes.** DIFLU : < 500 m (couche de surface) ; DATEM/ETEX : dizaines à milliers de km (far-field, résolution des réanalyses) ; ERIES : maquette urbaine à échelle réduite. Les performances d'un modèle réduit ne se transfèrent pas automatiquement d'une échelle à l'autre.
- **Taille d'échantillon d'essais indépendants.** ETEX : n = 2 lâchers ; ERIES : 2 configurations de source (× un seul vent) ; DIFLU : 15 expériences décrites par l’article ; valeur 19 de signification non établie ; DATEM : plusieurs campagnes mais anciennes (années 1980–1990) et hétérogènes. La généralisation (G3) doit s'appuyer sur des **essais** indépendants, jamais sur des points de mesure isolés d'un même essai.
- **Météorologie et terrain.** DIFLU : site réel, micrométéorologie co-localisée (fenêtre étendue 8 oct. 2019 – 8 janv. 2020) ; ETEX : réanalyses ECMWF ; DATEM : réanalyses NCAR/NCEP reformatées HYSPLIT ; ERIES : écoulement de soufflerie calibré VDI-3783, vent unique.
- **Conséquence pour le protocole** (conforme à l'[issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)) : DIFLU teste une **hypothèse de méthode** sur un cas compatible (transport passif en champ proche), avec baseline panache gaussien simple et métriques FAC2/NMSE **par lâcher indépendant** ; DATEM/ETEX servent une évaluation distincte far-field ; ERIES reste une référence de structure urbaine à échelle réduite.

## 6. Partition calibrage / évaluation (à figer avant tout benchmark)

1. **DIFLU** : partition **par lâcher** (par exemple calibrage sur les lâchers de la campagne d'octobre, évaluation sur ceux de décembre — ou toute autre partition fixée à l'avance et documentée) ; jamais par point de mesure isolé.
2. **ETEX** : un lâcher pour le développement, **le second réservé comme test final (G3)**, jamais utilisé pour le calibrage.
3. **DATEM** : partition par expérience/campagne ; les campagnes anciennes servent la robustesse, pas la calibration fine.
4. **ERIES** : S1 et S2 = deux essais ; les essais de répétabilité servent à quantifier l'incertitude expérimentale, pas à augmenter le nombre d'essais indépendants.

## 7. Reste à faire avant tout benchmark (prérequis G1)

| Priorité | Action | Verrou |
|---|---|---|
| Bloquante | Télécharger DIFLU depuis la fiche Recherche Data Gouv, conserver la notice Etalab 2.0 et vérifier l'intégrité, les unités et les métadonnées par fichier | Fichiers bruts non inspectés ; article : 15 expériences ; signification de la valeur 19 indexée à identifier |
| Haute | Identifier le champ source de la valeur 19 (ne pas l’assimiler à des essais) et documenter unités, limites de détection, données manquantes | Nécessite les fichiers |
| Haute | Télécharger les fichiers DATEM (texte délimité) et vérifier unités et cohérence par expérience | Site NOAA en 403 pour les outils — téléchargement manuel |
| Haute | Télécharger les quatre archives ETEX, vérifier la licence effective et l'horodatage | Fichiers non inspectés |
| Moyenne | Télécharger ERIES (xlsx, txt, Matlab) et vérifier unités et incertitudes chiffrées | Fichiers non inspectés |
| Moyenne | Fixer et documenter les partitions calibrage/évaluation ci-dessus | À figer avant tout entraînement |

### Procédure reproductible — récupérer un fichier DIFLU sans télécharger les archives complètes

Cette procédure est documentée mais **n’a pas pu être exécutée depuis l’environnement de rédaction** (résolution DNS/réseau externe indisponible). Elle doit être exécutée depuis une machine disposant d’un accès réseau. Elle cible d’abord le fichier tabulaire des prélèvements, sans télécharger les archives ZIP de ~381 Mo.

Prérequis : `curl`, `jq` et `sha256sum` (ou `shasum -a 256` sur macOS).

```bash
set -euo pipefail

BASE='https://entrepot.recherche.data.gouv.fr'
DATASET_PID='doi:10.57745/A9YC3C'
FILE_NAME='DIFLU_helium_release_sampling.tab'

# Enregistrer la réponse API qui décrit les fichiers de la version publiée.
curl --fail --location --show-error \
  --get "$BASE/api/datasets/:persistentId/versions/:latest/files" \
  --data-urlencode "persistentId=$DATASET_PID" \
  --output diflu-files.json

# Extraire l'identifiant Dataverse du fichier nommé, sans deviner son DOI.
FILE_ID="$(jq -er --arg name "$FILE_NAME" \
  '.data[] | select(.dataFile.filename == $name) | .dataFile.id' \
  diflu-files.json)"

# Télécharger le fichier ciblé, puis conserver une empreinte locale.
curl --fail --location --show-error \
  "$BASE/api/access/datafile/$FILE_ID" \
  --output "$FILE_NAME"

sha256sum "$FILE_NAME" | tee "$FILE_NAME.sha256"
wc -c "$FILE_NAME"
```

Si la requête API ou le filtre échoue, conserver le code HTTP, le corps d’erreur et la réponse JSON obtenue ; ne pas remplacer silencieusement l’identifiant ni considérer un fichier d’erreur comme les données. Le manifeste `diflu-files.json`, le fichier téléchargé, son empreinte et la date d’accès doivent être archivés ensemble. L’empreinte SHA-256 prouve l’identité des octets conservés pour les analyses ultérieures, pas l’exactitude scientifique des données.

Après téléchargement, contrôler le statut HTTP, le type et la taille du fichier, l’encodage et le séparateur, puis examiner les en-têtes, unités, horodatages, identifiants d’expérience, valeurs manquantes et limites de détection. Cette seule table ne suffit pas à vérifier la cohérence avec les mesures météorologiques : télécharger ensuite uniquement les fichiers météo/instrument nécessaires, selon le même mécanisme. La valeur 19 ne doit être interprétée comme un nombre d’essais que si un champ et sa sémantique l’établissent explicitement.

Référence API : [FAQ officielle Recherche Data Gouv — accès aux fichiers par API](https://recherche.data.gouv.fr/fr/faq) ; [documentation de l’API native Dataverse — liste des fichiers d’une version](https://guides.dataverse.org/en/latest/api/native-api.html).

## Sources de l'audit (consultées le 23 octobre 2026)

- Datacite, métadonnées DIFLU : [api.datacite.org/dois/10.57745/A9YC3C](https://api.datacite.org/dois/10.57745/A9YC3C) — titre complet, auteurs, producteur ASNR, description des campagnes 2019, rightsList vide, sous-DOIs `HasPart`.
- Datacite, métadonnées ERIES : [api.datacite.org/dois/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf](https://api.datacite.org/dois/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf) — licence CC BY 4.0 (SPDX), description du dispositif (Sofia 1:350, 76 points, S1/S2, éthylène, VDI-3783), formats, financement ERIES.
- NOAA ARL, page DATEM : [snapshot d'archive du 8 juin 2026](https://web.archive.org/web/20260608053910/https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) (site direct en 403 le 23/10/2026) — périmètre pilote (5 expériences, > 19 000 échantillons, NCAR/NCEP), formats, attribution demandée.
- NOAA ARL, [DATEM Tracer Evaluation](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/) et [HYSPLIT Evaluation Results Using DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/hysplit-evaluation-results-using-datem/) (extraits indexés) — neuf expériences listées dont ETEX ; exclusion d'INEL74/SRPTEX/ETEX de l'évaluation approfondie.
- JRC, [ETEX — Download datasets](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm), [Overview of the ETEX project](https://remon.jrc.ec.europa.eu/past_activities/etex/site/10.htm) et [Operations at the release site](https://remon.jrc.ec.europa.eu/past_activities/etex/site/71.htm) — quatre archives ; 168 stations, ~9 000 échantillons ; PMCP à 11,6 g/s au lâcher 2.
- JRC Open Data, [notice de copyright](https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/copyright.txt) (extraits indexés) — © Union européenne, décision du 12 décembre 2011, licence Creative Commons.
- Préalables issus de l'[audit documentaire G0](15-audit-corpus-g0-resultats.md) : termes source ETEX (340 kg PMCH / 490 kg PMCP, 12 h chacun, Monterfil), papier DIFLU associé (*Atmosphere* 13(8):1223, DOI [10.3390/atmos13081223](https://doi.org/10.3390/atmos13081223)), [catalogue des données](12-catalogue-donnees-transport-dispersion.md).
