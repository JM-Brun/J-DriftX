# Audit des corpus de validation — Résultats (critère e de G0)

> **Statut : audit documentaire exécuté le 22 octobre 2026** selon le [protocole](14-protocole-audit-corpus-g0.md), à partir des métadonnées et de la documentation officielles des dépôts. Les vérifications au niveau des fichiers bruts (téléchargement, sommes de contrôle, unités champ par champ, limites de détection, trous) restent un **prérequis G1** avant tout benchmark ; elles ne conditionnent plus la porte G0.

## Synthèse

| Corpus | Piste | Verdict | Réserve principale |
|---|---|---|---|
| DIFLU | Champ proche (< 500 m) | **V** | La fiche actuelle du dépôt affiche la Licence Ouverte Etalab 2.0 ; l’article décrit 15 expériences. La signification de la valeur 19 relevée dans des métadonnées indexées reste à identifier ; ne pas l’assimiler à des essais sans preuve |
| NOAA DATEM | Far-field traceur | **V** | Campagnes anciennes et hétérogènes ; ETEX figure dans l'archive générale, mais est exclu de l'évaluation approfondie HYSPLIT |
| ETEX (JRC) | Far-field continental | **V** | Deux lâchers indépendants seulement ; l'un doit être réservé comme test final (G3) |

**Décision : le critère (e) est renseigné et sourcé ; les critères (a)–(g) sont complets. G0 est franchi le 22 octobre 2026** ([issue publique de cadrage G0-A](https://github.com/JM-Brun/J-DriftX/issues/43)).

## 1. DIFLU — traceur hélium contrôlé, Beuvry (France)

| Point | Vérification | Résultat |
|---|---|---|
| 1. Accès et licence | DOI [10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C), [fiche actuelle Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C), producteur ASNR (LERTA, ex-IRSN), plus de 110 sous-DOIs et environ 381 Mo selon le [catalogue](12-catalogue-donnees-transport-dispersion.md) | Accès public ; la fiche du dépôt affiche **Licence Ouverte Etalab 2.0**. DataCite a toujours un `rightsList` vide : conserver une copie de la fiche et vérifier les métadonnées associées aux fichiers lors du téléchargement |
| 2. Terme source | Hélium libéré à débit massique contrôlé dans le flux d'air sortant de la cheminée du cyclotron hospitalier de Beuvry (description Datacite) ; site : 50,51404° N, 2,67255° E | Oui, contrôlé et documenté |
| 3. Coordonnées et temps | Campagnes octobre (14–18) et décembre (9–13) 2019 ; mesures à moins de 500 m de la source | Dates et site documentés ; horodatage des mesures à vérifier sur fichiers |
| 4. Météorologie | Micrométéorologie, anémomètres, lidar Doppler ([catalogue](12-catalogue-donnees-transport-dispersion.md)) | Oui, météo co-localisée |
| 5. Observable et unités | Concentration d'hélium par échantillonnage discret et mesures continues (description Datacite) ; le papier associé dérive des coefficients de transfert atmosphérique | Conforme à l'observable primaire ratifié (b) ; unités à vérifier sur fichiers |
| 6. Limites de détection | Discutées dans le papier associé | À vérifier sur fichiers |
| 7. Données manquantes | — | À vérifier sur fichiers |
| 8. Essais indépendants | Regroupement par lâcher obligatoire ; **15 expériences décrites dans le papier associé** (atmosphère instable, vent < 5 m s⁻¹) ; la valeur 19 relevée dans des métadonnées indexées n’est pas établie comme nombre d’essais | Structure identifiable ; décompte exact à trancher sur fichiers |
| 9. Reproductibilité des entrées | Terme source contrôlé + météo co-localisée + site documenté | Oui, en principe |

**Verdict : V** (Licence Ouverte Etalab 2.0 affichée sur la fiche actuelle du dépôt ; conserver la preuve de licence avec l'inventaire). La signification de la valeur 19 relevée dans des métadonnées indexées, les unités et les limites de détection restent à vérifier sur fichiers ; le papier atteste 15 expériences. Contexte : le papier associé compare déjà des panaches gaussiens (Doury, Briggs) aux mesures — utile pour la baseline gaussien simple du test discriminant.

## 2. NOAA DATEM — archive longue distance

| Point | Vérification | Résultat |
|---|---|---|
| 1. Accès et licence | Page officielle NOAA ARL ; données produites par une agence fédérale américaine ; mention d'attribution NOAA ARL demandée ; page momentanément inaccessible (erreur 403) lors de l'audit, contenu documenté par les extraits officiels | Accès public documenté ; usage conditionné à l'attribution |
| 2–3. Source et temps | Émissions et prélèvements dans des fichiers texte délimités, par expérience | Documentés par expérience |
| 4. Météorologie | Champs de réanalyse NCAR/NCEP reformatés pour HYSPLIT, téléchargeables | Oui, reconstitution possible |
| 5. Observable | Plus de 19 000 échantillons de concentration d'air, cinq expériences longue distance (dizaines à milliers de km) | Conforme à (b) ; unités à vérifier par expérience |
| 6–7. Détection et trous | — | À vérifier sur fichiers |
| 8. Essais indépendants | Expériences distinctes (l'archive documente chaque campagne) | Regroupement par expérience |
| 9. Reproductibilité | Termes source et météo documentés par expérience | Oui |

**Verdict : V.** Réserves : campagnes anciennes (années 1980, type CAPTEX/ANATEX). L'archive DATEM actuelle liste également **ETEX** (lâcher de Rennes, octobre 1994), mais cette expérience est exclue de l'évaluation approfondie HYSPLIT (hors Amérique du Nord ou antérieure à 1980). Les données ETEX sont aussi accessibles via le portail JRC, qui reste la source dédiée à ses deux lâchers.

## 3. ETEX (JRC) — traceur continental

| Point | Vérification | Résultat |
|---|---|---|
| 1. Accès et licence | [Page JRC](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm) vérifiée : téléchargements séparés pour les rejets 1 et 2 (météorologie et traceur) | Accès confirmé ; licence CE/JRC (réutilisation avec attribution) à confirmer sur le dépôt |
| 2. Terme source | Rejet 1 : 23 octobre 1994, 16:00 UTC, 340 kg de PMCH, durée 12 h ; rejet 2 : 14 novembre 1994, 15:00 UTC, 490 kg de PMCP (pour éviter la contamination croisée), durée 12 h ; site de Monterfil (Bretagne, France) | Oui, contrôlé et documenté |
| 3. Coordonnées et temps | 168 stations au sol dans 17 pays ; prélèvements d'environ 3 h pendant environ 90 h après le rejet | Oui |
| 4. Météorologie | Champs ECMWF archivés, fournis séparément par le JRC | Oui |
| 5. Observable | Concentrations de traceur perfluorocarboné au sol | Conforme à (b) ; unités à vérifier sur fichiers |
| 6–7. Détection et trous | — | À vérifier sur fichiers |
| 8. Essais indépendants | **Deux lâchers seulement**, dans des conditions météorologiques différentes | Oui, mais n = 2 : chaque lâcher fournit des centaines de couples station-temps, la généralisation reste limitée ; réserver un lâcher comme test final (G3) |
| 9. Reproductibilité | Terme source contrôlé + météo ECMWF | Oui |

**Verdict : V** (avec la réserve n = 2).

## 4. Décision et entrée en G1

1. Le critère (e) de la [fiche G0](13-fiche-g0-cadrage-besoin.md) est renseigné et sourcé ; G0 est **franchi**.
2. **Corpus principal du test discriminant : DIFLU** (champ proche, terme source contrôlé, météo co-localisée, observable conforme). **DATEM/ETEX** sont retenus en far-field pour la généralisation (G3).
3. Prérequis G1 avant tout benchmark, sans entraînement de modèle :
   - télécharger DIFLU, conserver la fiche indiquant la Licence Ouverte Etalab 2.0 et vérifier les métadonnées des fichiers ;
   - identifier le champ source de la valeur 19 sans l’assimiler à des essais, puis documenter unités, limites de détection et données manquantes ;
   - fixer la partition calibrage/évaluation par lâcher (jamais par point de mesure isolé) ;
   - réserver un lâcher ETEX (ou un sous-ensemble disjoint) comme test final jamais utilisé pour le calibrage.

## Sources de l'audit

- Datacite, métadonnées du jeu DIFLU : [api.datacite.org/dois/10.57745/A9YC3C](https://api.datacite.org/dois/10.57745/A9YC3C) (titre, producteur ASNR, dates des campagnes 2019, description des essais contrôlés).
- Papier associé : [Investigation of a Gaussian Plume in the Vicinity of an Urban Site](https://doi.org/10.3390/atmos13081223), *Atmosphere* 13(8):1223 — 15 expériences, site du cyclotron de Beuvry (50,51404° N, 2,67255° E), comparaison aux modèles de Doury et Briggs.
- ASNR, [projet DIFLU — campagne champ proche à l'hélium](https://recherche-expertise.asnr.fr/page/modelisation-3d-pour-dispersion-atmospherique-radionucleides-champ-proche).
- NOAA ARL, [DATEM — Data Archive of Tracer Experiments and Meteorology](https://www.arl.noaa.gov/hysplit/datem-tracer-evaluation/datem/) ; R. Draxler, [document de l'archive DATEM](https://www.arl.noaa.gov/documents/datem/document/datem.pdf).
- JRC, [ETEX — téléchargement des jeux de données](https://remon.jrc.ec.europa.eu/past_activities/etex/site/datasets.htm).
- Nodop et al. (s.d.), [ETEX: A European tracer experiment](https://www.sciencedirect.com/science/article/abs/pii/S1352231098002489) — deux rejets de traceurs PFC (340 kg PMCH le 23/10/1994, 490 kg PMCP le 14/11/1994, 12 h chacun, 168 stations dans 17 pays).
- Analyse ETEX-1 : [Robust Spatial Correlation Analysis of the ETEX-1 Tracer Data](https://www.researchgate.net/publication/287325710_Robust_Spatial_Correlation_Analysis_oftheETEX-1Tracer_Data) — site de Monterfil (Bretagne), prélèvements sur ~90 h.
