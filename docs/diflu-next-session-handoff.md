# DIFLU — état des travaux et plan de reprise

> Point de reprise : **2026-11-01**. Périmètre : audit scientifique et reproductible du jeu DIFLU pour J-DriftX. Décision : poursuivre l'audit ; **ne pas lancer de benchmark** à ce stade.

Ce document sépare résultats vérifiés, inférences et questions ouvertes. Les chiffres ci-dessous concernent les trois fichiers compacts versionnés dans `tests/fixtures/diflu/source/`, sauf indication contraire.

## 1. Résultats établis

- Le CSV de prélèvements contient **387 lignes**, **21 variables**, **19 identifiants de rejet** : **234 EA** et **153 VEGA**.
- Les 19 rejets se répartissent en **15 événements rapprochés de l'article de 2022** et **4 événements supplémentaires** absents de l'article.
- Le dictionnaire distingue EA (un sac unique par événement d'échantillonnage) et VEGA (prélèvements séquentiels multi-sacs). Ne pas agréger ces deux catégories comme des observations homogènes.
- Pour les **196 lignes EA significatives**, la correction de passage est cohérente : `passage_corrected / bg_corrected` concorde avec `durée prélèvement / durée rejet`, erreur relative maximale ≈ **0,58 %**.
- L'ATC candidat est calculé par `helium_concentration_sampling_bg_passage_corrected / helium_release_flow`, en **s m⁻³**.
- Sur les **153 EA significatifs** des 15 événements de l'article, les extrema publiés sont reproduits à l'arrondi près :
  - minimum : CSV `#1_6`, échantillon `B14`, **2,0227×10⁻⁵ s m⁻³**, article **2,0×10⁻⁵** ;
  - maximum : CSV `#2_4`, échantillon `A7_D7`, **1,5084×10⁻³ s m⁻³**, article **1,5×10⁻³**.
- Le maximum des 19 événements est sur `#1_1`, un rejet absent de l'article : ne pas le comparer aux extrema publiés pour les 15 événements.
- Les distances géodésiques release→sampler des deux échantillons extrêmes sont à moins d'un mètre des normes radiales déduites des coordonnées publiées. Cela ne valide ni l'orientation signée x/y ni la projection selon le vent.

## 2. Inférences fortes et limites

### EA ≈ Atmospheric Samplers (AS) : faisceau d'indices, pas preuve textuelle

- 14 identifiants EA distincts dans le CSV ; exactement 10 avec débit d'échantillonnage numérique, comme les 10 AS avec contrôleur de débit décrits dans l'article.
- Les comptes EA concordent avec les comptes AS de l'article pour **14 événements sur 15**.
- Débit EA médian observé : **0,171 L/min**, proche des **0,17 L/min** publiés.
- Médiane du rapport écart-type/débit : **3,68 %**, proche des **3,4 %** publiés.
- L'article ne nomme pas explicitement EA/VEGA. L'équivalence EA↔AS reste donc une hypothèse fortement étayée.

### Écarts encore inexpliqués

- Article `1-7` / CSV `#1_9` : l'article annonce 14 AS ; le CSV contient 6 EA et 9 VEGA. On ne sait pas si les périmètres ou méthodes de comptage diffèrent.
- Sous l'hypothèse EA≈AS, les 15 événements donnent 186 EA contre 194 AS publiés et 153 EA significatifs contre 148 résultats significatifs dans l'article. Ne pas qualifier ces écarts de lignes manquantes ou d'erreurs de classification sans preuve.
- Les 127 VEGA significatifs n'ont pas de correction de passage renseignée. Ne pas leur appliquer la règle EA par extrapolation.
- Les séries météo/micrométéo, les fichiers de localisation et les métadonnées instrumentales n'ont pas encore été audités.
- Les coordonnées x/y de l'article ne sont pas reconstruites sur l'ensemble des points.
- Aucune validation de généralisation à des conditions météo ou géométriques non observées n'a été faite.

## 3. PR et artefacts — état vérifié le 2026-11-01

Les PR scientifiques de la séquence DIFLU sont désormais intégrées ou explicitement supersédées. La présente actualisation du document est portée par la PR documentaire [#439](https://github.com/JM-Brun/J-DriftX/pull/439).

| PR | Objet | État vérifié |
|---|---|---|
| [#428](https://github.com/JM-Brun/J-DriftX/pull/428) | Comptes article (194 prélèvements, 148 significatifs) et crosswalk | Fusionnée dans `main` |
| [#432](https://github.com/JM-Brun/J-DriftX/pull/432) | Faisceau d'indices EA≈AS et limites | Fusionnée dans `main` |
| [#433](https://github.com/JM-Brun/J-DriftX/pull/433) | Valeurs manquantes et plages numériques par champ/type | Fusionnée dans `main` |
| [#436](https://github.com/JM-Brun/J-DriftX/pull/436) | Document de passation | Fusionnée dans `main` |
| [#438](https://github.com/JM-Brun/J-DriftX/pull/438) | Calcul ATC reproductible et contrôle des extrema sur le `main` courant | Fusionnée dans `main` ; CI complète réussie |

La PR #438 a été fusionnée par squash le 2026-11-01. Commit de merge : `570a66c8ac21980bb69d37f54c868b03680112e0`. Son run CI #1808 est terminé avec succès : rendu Quarto, contrôles documentaires, Ruff lint/format, mypy, pytest et génération/archivage du diagnostic de graphe.

PR fermées sans fusion :
- #434, première version de l'audit ATC, remplacée après retour Ruff ;
- #435, branche devenue divergente (12 commits de retard), remplacée par #438 recréée depuis `main` ;
- #431, déjà remplacée par #433.

Ne pas rouvrir ces PR. La branche de #435 est désormais redondante sur le plan fonctionnel, mais sa suppression doit attendre la vérification finale de son diff par rapport à `main`.

### Branches résiduelles : nettoyage à terminer

L'inventaire précédent identifiait 16 branches de travail. Les décisions ci-dessous sont des candidates, pas une autorisation de suppression aveugle :

- Les anciennes refs `docs/comparaison-jesa-2010-manuscrit-2009`, `docs/finalize-audit-followups` et `rebase/edp-overflow-current-bool-v2` ne sont plus présentes dans la recherche paginée des branches distantes au contrôle du 2026-11-01. Ne pas les traiter comme des suppressions encore à effectuer.
- **Doublon exact à supprimer en conservant l'autre nom** : `rebase/edp-overflow-on-current-bool-2026-10-30` et `fix/complex-inputs-concentration-edp-2026-10-30` sont **identiques** selon la comparaison GitHub (0 commit en avance/en retard, aucun fichier différent). Conserver `fix/complex-inputs-concentration-edp-2026-10-30` et supprimer le doublon `rebase/*`.
- **Branches ATC supersédées par la PR #438** : `audit/diflu-atc-extrema-current-main-2026-11-01` (branche fusionnée de #438) a des contenus de fichiers strictement identiques à `main` pour le protocole, le script et ses tests : suppression sûre après vérification du head. `audit/diflu-atc-reference-extrema-ci-2026-11-01` (ancienne branche de #435) est supersédée, mais son script n'est pas identique à `main` ; vérifier les différences résiduelles avant suppression.
- **Branche documentaire à comparer avant décision** : `docs/diflu-article-dataset-crosswalk-2026-10-31` a encore un commit propre et 12 lignes de diff dans le protocole ; le contenu paraît repris/évolué dans `main`, mais vérifier le sens de ces lignes avant suppression.
- **Branches à ne pas supprimer sur la seule base du retard** : les dix branches `fix/*` portent des changements sur les frontières booléennes, les entrées numériques, le parseur MNT, les trajectoires et la stabilité puff. Elles ont des commits propres et des recouvrements entre elles ; établir leur correspondance avec les PR historiques fusionnées et comparer les fichiers avant toute suppression.
- La branche `docs/s0-zermelo-hj-proof` apparaît aussi dans l'inventaire actuel mais relève d'un autre sujet ; la laisser hors de ce nettoyage.

Le nombre de commits en avance/en retard n'est pas une preuve suffisante d'équivalence fonctionnelle. Pour chaque suppression, comparer le diff net à `main`, vérifier les PR associées et conserver au moins une référence canonique du correctif. La suppression des refs distantes reste une opération GitHub/CLI distincte de la fermeture d'une PR.

Fichiers/scripts de référence :
- `scripts/audit_diflu.py`
- `scripts/vendor_diflu_reference.py`
- `tests/fixtures/diflu/source/`
- `docs/diflu-reproducible-audit.md`
- `docs/diflu-observable-evaluation-protocol.md`
- `docs/audits/15a-audit-bibliographique.md`

Issues : [#221](https://github.com/JM-Brun/J-DriftX/issues/221) (rapprochement article/CSV et ATC), [#204](https://github.com/JM-Brun/J-DriftX/issues/204) (récupération/intégrité). L'issue privée #167 et la PR privée #192 ne sont pas couvertes par cet inventaire public : vérifier séparément leur état et leur accès.

## 4. Prochaines tâches — ordre d'exécution

### P0 — Finaliser le nettoyage des branches

1. Recharger l'inventaire des refs distantes après la fusion de #438.
2. Refaire les comparaisons `main...branch` des candidates listées en section 3 ; vérifier les diffs de fichiers, pas seulement les nombres de commits.
3. Confirmer que les branches sans commits propres et le doublon exact ne contiennent aucun artefact utile non repris ailleurs.
4. Vérifier les branches `fix/*` contre les PR historiques fusionnées avant de décider de leur suppression ; ne pas regrouper des changements concurrents sans analyse de patch.
5. Supprimer les refs distantes uniquement après cette vérification, puis actualiser la liste des branches et ce document.

**Sortie attendue :** inventaire exhaustif et à jour, branches redondantes supprimées, branches conservées justifiées et aucun correctif unique perdu.

### P1 — Résoudre `#1_9`

1. Extraire toutes les lignes `#1_9` sans agrégation, EA et VEGA séparément.
2. Comparer `sampling_id`, `sampling_bag_id`, timestamps, durées, positions, hauteurs, flags, concentrations et débits disponibles.
3. Reconstituer le périmètre des 14 AS et des 4 résultats significatifs à partir du tableau 1, des méthodes et des métadonnées.
4. Vérifier si les 9 lignes VEGA entrent dans le périmètre des AS ; ne pas conclure sur la seule proximité des comptes.
5. Si les sources ne permettent pas de trancher, écrire une question précise aux auteurs et consigner l'incertitude. Ne pas les contacter sans autorisation explicite.

**Sortie attendue :** explication sourcée ou question précise restant à résoudre.

### P1 — Auditer les métadonnées instrumentales

1. Résoudre par nom dans le listing Dataverse, sans inventer d'identifiant, puis récupérer `DIFLU_instrument_locations.tab` et `DIFLU_instrument_metadata.tab`.
2. Préserver les octets originaux et enregistrer taille, MD5 et SHA-256.
3. Examiner structure, unités, référentiels, hauteurs, résolution et plages de mesure.
4. Distinguer les instruments météo (anémomètres, station, lidar Doppler) des positions de prélèvement. Ne pas joindre automatiquement les localisations instrumentales aux samplers.
5. Étendre la procédure d'audit seulement après compréhension de ces fichiers.

**Sortie attendue :** dictionnaire de jointure explicite et référentiels identifiés, sans jointure spatiale ambiguë.

### P1 — Auditer l'alignement temporel et les séries météo

1. Inventorier les séries météo/micrométéo et leurs dictionnaires dans le dépôt complet.
2. Confirmer fuseau et convention temporelle ; l'article utilise UTC pour les événements, mais ne pas supposer que toutes les séries partagent cette convention.
3. Inventorier variables, unités, fréquences, instruments, trous, doublons et changements de configuration.
4. Définir des fenêtres propres à chaque phénomène : rejet, prélèvement, intégration/transport. Ne pas moyenner automatiquement toute une expérience.
5. Reconstituer les variables météo de l'article (notamment vitesse/direction du vent et conditions thermodynamiques) et comparer aux tableaux publiés.
6. Quantifier l'incertitude d'alignement et la représentativité du vent mesuré pour chaque sampler.

**Sortie attendue :** table événement→mesures météo traçable et règles d'agrégation justifiées.

### P2 — Reconstruire la géométrie

1. Établir origine, axes, signes, orientation et éventuelle correction liée au vent des coordonnées x/y de l'article.
2. Recalculer les distances release→sampler WGS84 pour toutes les lignes.
3. Comparer les distances radiales publiées lorsqu'elles sont disponibles.
4. Reconstruire x/y uniquement si direction et convention sont suffisamment documentées ; sinon conserver les coordonnées géographiques et noter l'indétermination.
5. Vérifier les hauteurs et références verticales avec les métadonnées instrumentales.

**Sortie attendue :** transformation spatiale documentée et testée, ou décision motivée de ne pas reconstruire x/y.

### P2 — Clarifier VEGA et les observables

1. Déterminer le protocole temporel des sacs VEGA et leurs fenêtres d'échantillonnage.
2. Rechercher la définition d'une concentration représentative par sac et de ses corrections physiques.
3. Ne pas imputer les 127 corrections de passage VEGA absentes.
4. Définir des observables séparés EA/VEGA si nécessaire ; les réunir seulement si leur comparabilité est démontrée.
5. Documenter unités, seuils, limites de quantification et incertitudes.

**Sortie attendue :** observable défini par type, ou VEGA explicitement exclu du premier cas d'étude.

### P3 — Définir la validation physique, avant benchmark

1. Préciser la tâche : reconstruction de champ, prédiction d'ATC en un point, profil, ou généralisation.
2. Définir les variables disponibles à l'inférence et exclure toute fuite de cible.
3. Définir l'unité indépendante de validation ; jamais de split aléatoire de lignes issues d'un même événement.
4. Définir baselines physiques/statistiques, métriques, incertitudes et critères d'acceptation.
5. Évaluer si 15 événements article (ou 19 rejets du dépôt) suffisent ; ne pas supposer leur indépendance.
6. Privilégier d'abord comparaison déterministe à des modèles physiques et analyse de sensibilité. N'introduire un modèle appris que si la question et le nombre d'unités indépendantes le justifient.

**Sortie attendue :** protocole préétabli avec split par événement/campagne justifié. Aucun score avant cette étape.

## 5. Garde-fous

- Un checksum prouve l'intégrité des octets, pas la validité physique ni l'exhaustivité.
- La concordance des extrema ATC valide une partie de la chaîne de calcul, pas chaque ligne ni toute la distribution.
- Ne pas confondre identifiants de rejet, prélèvements et unités expérimentales indépendantes.
- EA≈AS reste une hypothèse étayée, non une équivalence explicitement écrite dans l'article.
- Ne pas mélanger les quatre rejets supplémentaires aux 15 événements lors de la reproduction des extrema.
- Ne pas assimiler VEGA à EA ni convertir les valeurs manquantes en zéro.
- Ne pas recalculer les flags de significativité en comparant directement une concentration déjà corrigée du fond au seuil absolu.
- Pas de benchmark, de validation croisée aléatoire ou de split par ligne avant validation des unités expérimentales, observables et covariables météo.
- Pas de refactoring général de J-DriftX : rester sur les travaux nécessaires à la validité scientifique.

## 6. Reprise pratique

1. Lire ce document, puis `docs/diflu-observable-evaluation-protocol.md` et `docs/diflu-reproducible-audit.md`.
2. Synchroniser GitHub : #428/#432/#433/#435, issues #221/#204 et issue privée #167.
3. Rejouer :
   ```bash
   uv run pytest tests/test_audit_diflu.py tests/test_vendor_diflu_reference.py
   ```
4. Rejouer l'audit du fixture et contrôler : 387 lignes, 234 EA, 153 VEGA ; 196 EA significatifs ; 153 sur les 15 événements article ; extrema article conformes à l'arrondi ; maximum global sur `#1_1`.
5. Commencer par le cas `#1_9` et les métadonnées instrumentales. Ne pas commencer par un benchmark.

## 7. Sources primaires

- Laguionie et al. (2022), *Investigation of a Gaussian Plume in the Vicinity of an Urban Cyclotron Using Helium as a Tracer Gas*, Atmosphere 13(8), 1223. [DOI 10.3390/atmos13081223](https://doi.org/10.3390/atmos13081223).
- Laguionie, Connan & Darmau (2026), DIFLU, version 1. [DOI 10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C).
