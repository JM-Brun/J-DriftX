# Audit technique des jeux de données candidats — accès, licences et fichiers (issues #204–#207)

> **Statut : audit initial du 23 octobre 2026, DIFLU actualisé le 31 octobre 2026**, suite de l'[audit documentaire G0](15-audit-corpus-g0-resultats.md). Objet : vérifier, depuis les **sources primaires**, l'accès réel, les licences, les formats de fichiers annoncés, l'unité d'indépendance des essais et la compatibilité physique de chaque corpus avec l'observable retenu (concentration aérienne, [issue #43](https://github.com/JM-Brun/J-DriftX/issues/43)).
> **Limite de méthode explicite.** Exception DIFLU : les trois originaux compacts (tableau de prélèvements et dictionnaires variables/médias) ont été récupérés, leur taille et MD5 vérifiés contre Dataverse, leurs SHA-256 consignés et leurs octets versionnés dans `tests/fixtures/diflu/source/`. Le reste du dépôt (114 fichiers, ZIP d'environ 381 MB, notamment séries météo/micrométéo et médias) n'a pas été téléchargé ni inspecté. Pour DATEM, ETEX et ERIES, les limites d'accès et vérifications restent celles précisées ci-dessous. L'intégrité des trois fichiers DIFLU ne valide ni le corpus complet, ni son usage scientifique, ni un benchmark. Le suivi est réparti entre [#204 (récupération/intégrité DIFLU)](https://github.com/JM-Brun/J-DriftX/issues/204), [#221 (audit sémantique et décision MVP DIFLU)](https://github.com/JM-Brun/J-DriftX/issues/221), [#205 (ETEX/DATEM)](https://github.com/JM-Brun/J-DriftX/issues/205), [#206 (ERIES)](https://github.com/JM-Brun/J-DriftX/issues/206) et [#207 (corpus complémentaires et protocole)](https://github.com/JM-Brun/J-DriftX/issues/207).

## Synthèse

| Corpus | Accès distant (23/10/2026) | Licence (source primaire) | Unité d'indépendance | Compatible avec l'observable (concentration aérienne) | Reste à vérifier sur fichiers |
|---|---|---|---|---|---|
| [DIFLU](https://doi.org/10.57745/A9YC3C) ([Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C)) | Trois originaux compacts téléchargés, taille/MD5 vérifiés et versionnés ; dépôt complet de 114 fichiers non inspecté | **Etalab Open Licence 2.0** sur la notice et dans le manifeste ; DataCite `rightsList` vide (couches de métadonnées distinctes) | 19 identifiants de rejet dans le CSV ; 15 rapprochés des événements de l'article, 4 supplémentaires ; l'indépendance statistique n'est pas établie | Oui — gaz traceur passif, champ proche < 500 m, couche de surface | Écart conditionnel à l'hypothèse EA↔AS : 186 lignes EA contre 194 prélèvements article ; 153 flags EA significatifs contre 148 ; séries météo/micrométéo et protocole d'usage restent à auditer |
| [NOAA DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) | Page officielle en 403 pour les accès automatisés ; contenu documenté via [snapshot d'archive (8 juin 2026)](https://web.archive.org/web/20260608053910/https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) | Aucune licence formelle affichée ; **attribution NOAA ARL demandée** pour les publications | L'expérience (la campagne) | Oui — traceurs far-field (dizaines à milliers de km) | Contenu des fichiers texte (unités par expérience), périmètre exact des 9 expériences listées |
| [ETEX / JRC](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm) | Page de téléchargement active : **quatre archives** (météo × traceur, lâchers 1 et 2) | Pas de licence par fichier ; **notice générique open data JRC** (© Union européenne, décision 2011/833/EU, Creative Commons) à confirmer pour ces fichiers | Le lâcher (**n = 2 seulement**) | Oui — traceur perfluorocarboné au sol, échelle continentale | Unités, complétude, contenu des archives météo |
| [ERIES](https://doi.org/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf) (4TU.ResearchData) | DOI actif (version 2, mars 2026) ; page d'accueil illisible pour les outils, métadonnées Datacite complètes | **CC BY 4.0 confirmée** (SPDX cc-by-4.0) — seule licence pleinement vérifiée aujourd'hui | La configuration (source S1/S2 × vent) : 2 essais ; la répétabilité quantifie l'incertitude | Oui — scalaire passif neutre, mais **échelle réduite** (soufflerie, 1:350) | Structure des fichiers (xlsx, txt, Matlab), unités, incertitudes chiffrées |

## 0. Méthode et limites

Consulté le 23 octobre 2026, en sources primaires uniquement :

- **DIFLU** : la notice [Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C) affiche l'**Etalab Open Licence 2.0** ; le `rightsList` DataCite est vide, ce qui relève d'une différence entre couches de métadonnées. Les trois originaux compacts (prélèvements, dictionnaire des variables, dictionnaire des médias) ont depuis été téléchargés, vérifiés par taille/MD5, dotés de SHA-256 et versionnés. Le ZIP complet et les séries météo/micrométéo restent hors du périmètre inspecté.
- **DATEM** : le site officiel NOAA ARL rejette les accès automatisés (403 CloudFront) ; la page a été documentée via un snapshot d'archive web du 8 juin 2026, complété par les extraits des pages d'évaluation HYSPLIT/DATEM indexées.
- **ETEX** : les pages JRC (remon.jrc.ec.europa.eu) sont accessibles et ont été lues directement ; la notice de copyright open data JRC est constatée sur le portail open data (jeux voisins), pas sur les fichiers ETEX eux-mêmes.
- **ERIES** : métadonnées Datacite complètes du DOI 10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf, incluant licence, description détaillée, formats et liens de financement ; la page 4TU.ResearchData elle-même est illisible pour les outils.

Les octets des fichiers des autres corpus n'ont pas pu être inspectés dans cette passe. Pour ETEX, l'index de téléchargement et le répertoire de la deuxième campagne sont lisibles et donnent noms, tailles et dates, mais le contenu des archives n'a pas été inspecté ; le répertoire de la première campagne a expiré en accès automatisé. Pour DATEM et ERIES, les limites d'accès restent celles précisées ci-dessous. Les unités, limites de détection, trous et formats internes de ces corpus restent donc non vérifiés : la visibilité d'un listing n'est pas une inspection des données.


### Mise à jour — 31 octobre 2026 : rapprochement des identifiants DIFLU

Les trois fichiers compacts versionnés ont été inspectés. Le CSV de prélèvements contient 387 lignes et 19 valeurs distinctes de `experiment_id`. Le rapprochement par heure UTC de rejet, débit et durée identifie les 15 événements de l'article de 2022 parmi ces 19 identifiants : par exemple, l'événement article `1-1` (15/10/2019 13:45) correspond au CSV `#1_3`, et non à `#1_1`. Les quatre événements supplémentaires du dépôt sont `#1_1`, `#1_2`, `#2_9` et `#2_10`. Ce sont des identifiants de rejets présents dans le fichier, pas une preuve de 19 essais statistiquement indépendants.

Sur les 15 événements rapprochés, le CSV contient 186 lignes EA contre 194 prélèvements annoncés par l'article ; les flags EA `significant` totalisent 153 contre 148. Cette comparaison suppose que les lignes EA correspondent aux « Atmospheric Samplers » (AS) de l'article ; cette équivalence n'est pas explicitement nommée dans l'article. Sous cette hypothèse, l'écart de 8 lignes se concentre sur l'événement article `1-7` / CSV `#1_9` (6 EA contre 14 AS dans le tableau 1), et quatre événements présentent des écarts de significativité. Il s'agit d'écarts conditionnels à la correspondance EA↔AS, pas encore de la preuve de lignes manquantes ou d'erreurs de classification. Le détail est dans le [protocole d'évaluation DIFLU](diflu-observable-evaluation-protocol.md).

## 1. DIFLU — traceur hélium contrôlé, Beuvry (France) : corpus principal du test discriminant

| Point | Vérification initiale (23/10/2026), actualisée DIFLU (31/10/2026) | Résultat |
|---|---|---|
| Accès | DOI [10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C), [fiche du dépôt](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C) ; notice version 1, 114 fichiers. Les trois originaux compacts sont vérifiés et versionnés dans `tests/fixtures/diflu/source/` ; les séries météo/micrométéo, médias et archives complètes ne sont pas inclus dans cet audit | Accès et intégrité des trois fichiers compacts confirmés ; corpus complet non téléchargé |
| Licence | DataCite `rightsList` **vide** ; notice Recherche Data Gouv et manifeste du corpus compact indiquent Etalab Open Licence 2.0 | Licence de la notice identifiée ; conserver l'attribution et vérifier les conditions spécifiques aux autres fichiers si le corpus complet est réutilisé |
| Terme source | Hélium libéré à débit massique contrôlé dans le flux d'air sortant de la cheminée du cyclotron hospitalier de Beuvry (description Datacite) ; site 50,51404° N, 2,67255° E (papier associé) | Oui, contrôlé et documenté |
| Campagnes et temps | L'article décrit 15 rejets (7 en octobre, 8 en décembre 2019). Le CSV 2026 contient 19 identifiants de rejet : 15 rapprochés à l'article par date/heure, débit et durée, plus quatre rejets supplémentaires (`#1_1`, `#1_2`, `#2_9`, `#2_10`) | Rapprochement établi ; les quatre rejets supplémentaires sont identifiés. L'indépendance statistique des 19 rejets n'est pas démontrée |
| Mesures | Le CSV compact comprend 387 enregistrements : 234 EA (sac unique) et 153 VEGA (sacs séquentiels), avec 323 flags `significant` et 64 `< LC`. Les 15 rejets communs à l'article contiennent 186 lignes EA et 123 VEGA ; les quatre rejets supplémentaires, 48 EA et 30 VEGA | Granularité et dictionnaires inspectés ; les lignes ne sont pas des essais indépendants et EA/VEGA ne sont pas des supports interchangeables |
| Complétude | Aucun horodatage de prélèvement invalide/inversé ni clé d'identité répétée ; `sampling_flowrate` vaut `NA` sur 218 lignes (65 EA, 153 VEGA), et 64 lignes portent `< LC`. Les plages numériques et autres champs manquants restent à examiner exhaustivement | Contrôles structurels partiels ; pas de validation physique ni de complétude du dépôt entier |
| Essais indépendants | L'unité de partition minimale est le rejet (`experiment_id`), jamais la ligne ; le CSV contient 19 identifiants de rejet, dont 15 alignés sur l'article. Les deux campagnes (octobre/décembre) constituent aussi des contextes distincts | Le nombre de rejets est établi ; leur indépendance statistique et le niveau de partition approprié (rejet vs campagne) restent à justifier |
| Compatibilité observable | Gaz traceur passif en champ proche (< 500 m), couche de surface, environnement urbain peu dense | Conforme à l'observable primaire (concentration aérienne) ; **ne teste pas la dérive de pulvérisation** (rejet de cheminée, pas de buse ; gaz, pas de gouttelettes) |

**Verdict : corpus candidat pour l'audit et une éventuelle comparaison physique, sous conditions.** La licence Etalab 2.0 est affichée sur la notice et les trois fichiers compacts sont intègres et inspectés structurellement. Le corpus n'est pas encore validé pour le MVP : les comptes article/CSV diffèrent sous l'hypothèse EA↔AS (186 EA vs 194 prélèvements ; 153 flags significatifs vs 148), mais la correspondance EA/AS reste à confirmer ; la formule de correction de passage est vérifiée pour EA mais le traitement VEGA reste non documenté, et les séries météo/micrométéo complètes ne sont pas jointes. Aucun benchmark n'est autorisé à ce stade.

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
- **Taille d'échantillon d'essais indépendants.** ETEX : n = 2 lâchers ; ERIES : 2 configurations de source (× un seul vent) ; DIFLU : 19 identifiants de rejet dans le CSV, dont 15 alignés sur l'article et 4 supplémentaires ; leur indépendance statistique n'est pas établie. DATEM : plusieurs campagnes mais anciennes (années 1980–1990) et hétérogènes. La généralisation (G3) doit s'appuyer sur des **essais** indépendants, jamais sur des points de mesure isolés d'un même essai.
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
| Bloquante | Expliquer les écarts entre le CSV versionné et l'article 2022 (échantillons et significativité) ; obtenir la règle VEGA pour la correction de passage | Trois originaux compacts intègres ; rapprochement 15 événements fait, mais 186/194 EA et 153/148 significatifs restent inexpliqués |
| Haute | Compléter l'inventaire des champs, coordonnées/hauteurs et plages numériques ; établir la jointure avec les séries météo/micrométéo si nécessaire | Audit structurel partiel ; dépôt complet non inspecté |
| Haute | Télécharger les fichiers DATEM (texte délimité) et vérifier unités et cohérence par expérience | Site NOAA en 403 pour les outils — téléchargement manuel |
| Haute | Télécharger les quatre archives ETEX, vérifier la licence effective et l'horodatage | Fichiers non inspectés |
| Moyenne | Télécharger ERIES (xlsx, txt, Matlab) et vérifier unités et incertitudes chiffrées | Fichiers non inspectés |
| Moyenne | Fixer et documenter les partitions calibrage/évaluation ci-dessus | À figer avant tout entraînement |

### Procédure reproductible — récupération et audit DIFLU

La procédure canonique est désormais [docs/diflu-reproducible-audit.md](diflu-reproducible-audit.md). Elle utilise `scripts/audit_diflu.py` pour récupérer les trois originaux compacts, vérifier taille/MD5 et calculer SHA-256, puis `scripts/vendor_diflu_reference.py` pour les copier byte-for-byte dans `tests/fixtures/diflu/source/` après nouvelle vérification. Les tests hors ligne sont séparés du téléchargement réseau.

Les trois originaux sont déjà versionnés et leur manifeste est [tests/fixtures/diflu/source/manifest.json](../tests/fixtures/diflu/source/manifest.json). Les données brutes complètes, les séries météo/micrométéo et les médias restent hors du dépôt. Ne pas relancer l'ancien `scripts/download_diflu.py` décrit dans l'historique : la procédure actuelle est `audit_diflu.py` + `vendor_diflu_reference.py`. L'intégrité des originaux ne prouve ni la validité scientifique, ni l'exhaustivité du corpus, ni l'admissibilité de l'ATC comme cible.

## Sources de l'audit (consultées le 23 octobre 2026 ; compléments DIFLU le 31 octobre 2026)

- Datacite, métadonnées DIFLU : [api.datacite.org/dois/10.57745/A9YC3C](https://api.datacite.org/dois/10.57745/A9YC3C) — titre complet, auteurs, producteur ASNR, description des campagnes 2019, rightsList vide, sous-DOIs `HasPart`.
- Datacite, métadonnées ERIES : [api.datacite.org/dois/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf](https://api.datacite.org/dois/10.4121/e7f87f46-1d17-43ed-be81-60bee65081bf) — licence CC BY 4.0 (SPDX), description du dispositif (Sofia 1:350, 76 points, S1/S2, éthylène, VDI-3783), formats, financement ERIES.
- NOAA ARL, page DATEM : [snapshot d'archive du 8 juin 2026](https://web.archive.org/web/20260608053910/https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) (site direct en 403 le 23/10/2026) — périmètre pilote (5 expériences, > 19 000 échantillons, NCAR/NCEP), formats, attribution demandée.
- NOAA ARL, [DATEM Tracer Evaluation](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/) et [HYSPLIT Evaluation Results Using DATEM](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/hysplit-evaluation-results-using-datem/) (extraits indexés) — neuf expériences listées dont ETEX ; exclusion d'INEL74/SRPTEX/ETEX de l'évaluation approfondie.
- JRC, [ETEX — Download datasets](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm), [Overview of the ETEX project](https://remon.jrc.ec.europa.eu/past_activities/etex/site/10.htm) et [Operations at the release site](https://remon.jrc.ec.europa.eu/past_activities/etex/site/71.htm) — quatre archives ; 168 stations, ~9 000 échantillons ; PMCP à 11,6 g/s au lâcher 2.
- JRC Open Data, [notice de copyright](https://jeodpp.jrc.ec.europa.eu/ftp/public/JRC-OpenData/copyright.txt) (extraits indexés) — © Union européenne, décision du 12 décembre 2011, licence Creative Commons.
- Préalables issus de l'[audit documentaire G0](15-audit-corpus-g0-resultats.md) : termes source ETEX (340 kg PMCH / 490 kg PMCP, 12 h chacun, Monterfil), papier DIFLU associé (*Atmosphere* 13(8):1223, DOI [10.3390/atmos13081223](https://doi.org/10.3390/atmos13081223)), [catalogue des données](12-catalogue-donnees-transport-dispersion.md).
