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

## 3. PR et artefacts — état vérifié le 2026-11-01 à 20:10 UTC

Les intégrations récentes sont stabilisées. Au contrôle précédant cette mise à jour, aucune PR n'était ouverte ; cette actualisation est destinée à être publiée dans une PR documentaire dédiée.

| PR | Objet | État vérifié |
|---|---|---|
| [#428](https://github.com/JM-Brun/J-DriftX/pull/428) | Comptes article et crosswalk | Fusionnée dans `main` |
| [#432](https://github.com/JM-Brun/J-DriftX/pull/432) | Faisceau d'indices EA≈AS et limites | Fusionnée dans `main` |
| [#433](https://github.com/JM-Brun/J-DriftX/pull/433) | Valeurs manquantes et plages numériques | Fusionnée dans `main` |
| [#436](https://github.com/JM-Brun/J-DriftX/pull/436) | Document de passation initial | Fusionnée dans `main` |
| [#438](https://github.com/JM-Brun/J-DriftX/pull/438) | Audit ATC et extrema publiés | Fusionnée dans `main`, CI complète réussie |
| [#439](https://github.com/JM-Brun/J-DriftX/pull/439) | Actualisation précédente de la passation | Fusionnée dans `main` |
| [#440](https://github.com/JM-Brun/J-DriftX/pull/440) | Preuve S0 navigation / Hamilton–Jacobi | Fusionnée dans `main` ; sujet théorique distinct de DIFLU |

La PR #438 a été fusionnée par squash le 2026-11-01 (commit `570a66c8ac21980bb69d37f54c868b03680112e0`). Son run CI #1808 a réussi : rendu Quarto, contrôles documentaires, Ruff lint/format, mypy, pytest et diagnostic du graphe.

La PR #440 a été fusionnée le 2026-11-01 (commit `5aa1b30fb0ea1ca0e9ce5546f263df085b31feaa`). Elle publie une preuve analytique S0, sans revendiquer de validation physique générale.

### PR candidates examinées puis fermées

| PR | Branche | Décision |
|---|---|---|
| [#441](https://github.com/JM-Brun/J-DriftX/pull/441) | `fix/vectorized-core-bool-boundaries-2026-10-30` | Fermée : `main` contient déjà des validations réels finis/représentables, plus strictes que le patch booléen historique, et une suite de tests plus récente |
| [#442](https://github.com/JM-Brun/J-DriftX/pull/442) | `fix/trajectory-advection-real-input-contract-2026-10-30` | Fermée : les contrats réels finis/représentables et les tests sont déjà intégrés ; `main` ajoute aussi les garde-fous de débordement et de dernier pas |
| [#443](https://github.com/JM-Brun/J-DriftX/pull/443) | `fix/edp-intermediate-overflow-2026-10-30` | Fermée : les frontières EDP/métriques/contraintes dans `main` couvrent déjà les booléens, les complexes et les cas de représentabilité ; tests courants plus complets |
| [#444](https://github.com/JM-Brun/J-DriftX/pull/444) | `fix/puff-marginale-log-domain-final-v3-2026-10-30` | Fermée : calcul logarithmique déjà intégré ; les tests de `main` couvrent notamment le sous-débordement final et évitent une égalité exacte trop stricte |
| [#445](https://github.com/JM-Brun/J-DriftX/pull/445) | `docs/diflu-article-dataset-crosswalk-2026-10-31` | Fermée : le contenu EA/VEGA et la comparaison des périmètres sont déjà documentés et enrichis dans la section 3.2 de `main` |

Ces fermetures ne signifient pas que les problèmes historiques étaient imaginaires : elles signifient que leurs correctifs ont été dépassés par des implémentations plus récentes déjà présentes dans `main`. Ne pas rouvrir ces PR ni réintroduire leurs versions anciennes.

PR fermées sans fusion antérieures : #431 (remplacée par #433), #434 (première version ATC), #435 (branche divergente remplacée par #438), #324 (parseur MNT remplacé par #325), #341/#338 (remplacées par #342), #348, #358, #363, #365/#370, #382, #385/#386 et #394/#395/#396/#399. Certaines branches de ces PR ont été conservées dans l'inventaire pour audit, mais leurs fonctions ont depuis été intégrées ou renforcées dans `main`.

### Inventaire actuel des branches distantes et décision

Au dernier inventaire, les branches distantes sont :

| Branche | État du travail | Décision |
|---|---|---|
| `main` | Référence courante | **Conserver** |
| `audit/diflu-atc-extrema-current-main-2026-11-01` | Trois fichiers concernés identiques à `main` après #438 | Supprimer |
| `audit/diflu-atc-reference-extrema-ci-2026-11-01` | Ancienne tête de #435, supersédée par #438 | Supprimer |
| `docs/diflu-article-dataset-crosswalk-2026-10-31` | Section 3.2 déjà présente et enrichie dans `main` ; #445 fermée | Supprimer |
| `fix/c3-boolean-inputs-2026-10-30` | Contrats de réels et tests plus complets dans `main` | Supprimer |
| `fix/complex-inputs-concentration-edp-2026-10-30` | Doublon exact de la branche `rebase/edp-overflow-on-current-bool-2026-10-30` ; contenu dépassé par `main` | Supprimer |
| `fix/edp-intermediate-overflow-2026-10-30` | Contrôles EDP/overflow plus complets dans `main` | Supprimer |
| `fix/entrees-numeriques-reliefs-concentrations-2026-10-30` | PR #332 fusionnée ; renforcée ensuite par #340 | Supprimer |
| `fix/puff-marginale-log-domain-final-v2-2026-10-30` | Ancienne variante, dépassée par v3 puis par les tests courants de `main` | Supprimer |
| `fix/puff-marginale-log-domain-final-v3-2026-10-30` | Algorithme log-domain déjà présent dans `main`, avec tests plus stricts | Supprimer |
| `fix/reliefs-mixed-bool-validation-2026-10-30` | PR #340 fusionnée ; fichier de tests identique à `main` | Supprimer |
| `fix/robustesse-parseur-mnt-ascii` | PR #324 non fusionnée, mais comportement repris par #325 ; tests courants plus complets | Supprimer |
| `fix/trajectory-advection-real-input-contract-2026-10-30` | Supersédée par les contrats plus stricts et tests de `main` | Supprimer |
| `fix/vectorized-core-bool-boundaries-2026-10-30` | Supersédée par les contrats plus stricts et tests de `main` | Supprimer |
| `rebase/edp-overflow-on-current-bool-2026-10-30` | Doublon exact de `fix/complex-inputs-concentration-edp-2026-10-30` | Supprimer |

**Conclusion de l'audit : aucune branche de travail listée ne justifie une PR supplémentaire à conserver.** Les quatre PR de code #441–#444 ont été ouvertes en brouillon pour contrôler leur delta, puis fermées après vérification que `main` contenait déjà une version plus complète. La PR documentaire #445 a été fermée pour la même raison. La seule PR ouverte après cet audit est la présente PR documentaire [#446](https://github.com/JM-Brun/J-DriftX/pull/446).

### Nettoyage Git restant

Les refs distantes listées ci-dessus sont candidates à suppression. Les outils de gestion utilisés pour cet audit permettent de comparer les refs, créer/mettre à jour des fichiers et gérer les PR, mais ne fournissent pas d'opération de suppression de branche. **Aucune branche n'a été supprimée par cet audit.**

Après une dernière vérification de l'état local et distant, les commandes de nettoyage sont :

```bash
git fetch --prune origin
git push origin --delete \
  audit/diflu-atc-extrema-current-main-2026-11-01 \
  audit/diflu-atc-reference-extrema-ci-2026-11-01 \
  docs/diflu-article-dataset-crosswalk-2026-10-31 \
  fix/c3-boolean-inputs-2026-10-30 \
  fix/complex-inputs-concentration-edp-2026-10-30 \
  fix/edp-intermediate-overflow-2026-10-30 \
  fix/entrees-numeriques-reliefs-concentrations-2026-10-30 \
  fix/puff-marginale-log-domain-final-v2-2026-10-30 \
  fix/puff-marginale-log-domain-final-v3-2026-10-30 \
  fix/reliefs-mixed-bool-validation-2026-10-30 \
  fix/robustesse-parseur-mnt-ascii \
  fix/trajectory-advection-real-input-contract-2026-10-30 \
  fix/vectorized-core-bool-boundaries-2026-10-30 \
  rebase/edp-overflow-on-current-bool-2026-10-30
```

Ne pas supprimer `main`. Refaire un inventaire après suppression et vérifier que les refs ont disparu.

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
