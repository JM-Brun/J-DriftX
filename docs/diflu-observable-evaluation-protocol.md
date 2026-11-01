# DIFLU : observable scientifique et protocole d'évaluation à valider

> Statut : cadrage documentaire, **pas encore un protocole validé sur les fichiers bruts**. Ne pas utiliser cette note comme autorisation de lancer un benchmark.

## Sources primaires

- Laguionie et al. (2022), « Investigation of a Gaussian Plume in the Vicinity of an Urban Cyclotron Using Helium as a Tracer Gas », *Atmosphere*, 13(8), 1223. [DOI: 10.3390/atmos13081223](https://doi.org/10.3390/atmos13081223). Les passages utiles sont les sections 2.3.2–2.3.4, le tableau 1 et la section 2.5.
- Laguionie, Connan & Darmau (2026), jeu de données DIFLU, version 1. [DOI: 10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C), [notice Dataverse](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C).

## 1. Observable candidat : coefficient de transfert atmosphérique (ATC)

L'article définit le coefficient de transfert atmosphérique observé par :

\[
\mathrm{ATC}(x,y,z) = \frac{C(x,y,z)}{Q}
\]

où :

- \(C\) est la concentration d'hélium attribuée au panache, en \(\mathrm{g\,m^{-3}}\) ;
- \(Q\) est le débit massique d'hélium rejeté, en \(\mathrm{g\,s^{-1}}\) ;
- l'ATC est donc exprimé en \(\mathrm{s\,m^{-3}}\).

L'ATC est un **candidat d'observable** pertinent pour comparer une mesure et un modèle de dispersion. Cela ne signifie pas que le calcul peut déjà être appliqué sans précaution aux colonnes du dépôt : la correspondance exacte entre les champs, les unités, les corrections et les valeurs manquantes doit d'abord être confirmée dans le dictionnaire et les données.

## 2. Corrections expérimentales à préserver

Selon la section 2.3.3 de l'article :

1. Le fond atmosphérique d'hélium est mesuré avant chaque mesure de concentration en sac.
2. Une mesure aval est considérée comme significative lorsqu'elle dépasse 1,05 fois le fond atmosphérique. Ce seuil vise notamment à éliminer l'influence du bruit électronique.
3. La concentration attribuée au panache est corrigée à partir de la différence entre la concentration mesurée et le fond, puis multipliée par le rapport entre durée de prélèvement et durée du rejet.
4. La conversion en \(\mathrm{g\,m^{-3}}\) dépend également des conditions de pression et de température au moment du prélèvement.

Ces éléments impliquent qu'une colonne de concentration brute, une concentration corrigée du fond et une concentration corrigée du passage ne sont pas interchangeables. Ne pas recalculer ni « corriger » une valeur avant d'avoir confirmé sa définition exacte dans le dictionnaire de variables. Une valeur absente ou un indicateur de non-significativité ne doit pas être transformé en zéro par défaut.

## 3. Réconcilier les unités d'observation avant les statistiques

Les sources donnent des comptes qui décrivent des périmètres différents. Attention à ne pas confondre les 194 prélèvements d'air en aval avec les 148 résultats significatifs : le premier est le nombre d'échantillons rapporté, le second le sous-ensemble dépassant le seuil de décision. Le dépôt 2026 décrit 19 événements de rejet au total, dont 15 correspondent à ceux étudiés dans l'article et quatre sont supplémentaires :

- l'article de 2022 porte sur 15 expériences : 7 du 15 au 17 octobre 2019 et 8 du 10 au 12 décembre 2019 ;
- il rapporte 194 prélèvements d'air en aval, dont 148 concentrations significatives, auxquels s'ajoute un prélèvement amont de contrôle par expérience ;
- la notice du dépôt de données publiée en 2026 décrit 19 expériences et annonce des données supplémentaires (mesures intégrées, mesures d'hélium en temps réel, données météorologiques et micrométéorologiques, documentation instrumentale) ;
- l'audit automatisé du fichier ciblé rapporte 387 lignes, dont 234 EA et 153 VEGA.

Ces comptes ne doivent pas être forcés à correspondre. L'audit doit établir la signification de chaque ligne et relier explicitement, lorsque c'est possible, les identifiants d'expérience, de prélèvement et de sac. Il faut aussi vérifier si les catégories EA et VEGA sont des méthodes, des instruments ou des représentations complémentaires d'un même événement, sans le présumer.


### 3.1. Rapprochement vérifié avec l'article de 2022 et limites du rapprochement

Les trois fichiers compacts versionnés ont été relus directement (tableau des prélèvements et deux dictionnaires). Le rapprochement des heures UTC de rejet, des débits et des durées permet d'identifier sans ambiguïté apparente les 15 événements de l'article dans le tableau de 2026. **Les identifiants ne sont toutefois pas identiques** : le premier événement de l'article, `1-1` (15/10/2019 à 13:45 UTC), correspond à `#1_3` dans le fichier 2026, et non à `#1_1`.

| ID article | ID fichier 2026 | Début du rejet UTC | EA dans le CSV / AS article (EA≈AS, fortement étayé) | EA `significant` dans le CSV / nombre article |
|---|---|---|---:|---:|
| 1-1 | `#1_3` | 15/10/2019 13:45 | 14 / 14 | 12 / 11 |
| 1-2 | `#1_4` | 16/10/2019 07:10 | 14 / 14 | 13 / 11 |
| 1-3 | `#1_5` | 16/10/2019 09:30 | 14 / 14 | 13 / 13 |
| 1-4 | `#1_6` | 16/10/2019 12:00 | 14 / 14 | 8 / 8 |
| 1-5 | `#1_7` | 17/10/2019 07:05 | 14 / 14 | 8 / 8 |
| 1-6 | `#1_8` | 17/10/2019 09:30 | 14 / 14 | 13 / 13 |
| 1-7 | `#1_9` | 17/10/2019 12:45 | **6 / 14** | **5 / 4** |
| 2-1 | `#2_1` | 10/12/2019 09:30 | 12 / 12 | 8 / 8 |
| 2-2 | `#2_2` | 10/12/2019 12:40 | 12 / 12 | 12 / 12 |
| 2-3 | `#2_3` | 10/12/2019 14:20 | 11 / 11 | 10 / 10 |
| 2-4 | `#2_4` | 11/12/2019 08:45 | 13 / 13 | 7 / 6 |
| 2-5 | `#2_5` | 11/12/2019 10:15 | 12 / 12 | 10 / 10 |
| 2-6 | `#2_6` | 11/12/2019 13:00 | 13 / 13 | 12 / 12 |
| 2-7 | `#2_7` | 11/12/2019 15:00 | 11 / 11 | 10 / 10 |
| 2-8 | `#2_8` | 12/12/2019 08:15 | 12 / 12 | 12 / 12 |
| **Total** | **15 événements** |  | **186 / 194** | **153 / 148** |

Les 194 échantillons sous le vent et 148 résultats significatifs sont ceux rapportés par l'article (sections 2.3.2 et 3.2, tableau 1). Les colonnes « CSV » sont des recomptages restreints aux lignes `EA` et aux 15 événements rapprochés, selon `helium_concentration_sampling_bg_corrected_flag`. **L'article ne nomme pas explicitement les catégories EA/VEGA**, donc l'équivalence terminologique EA = AS n'est pas une preuve textuelle. En revanche, plusieurs contrôles indépendants la rendent désormais fortement probable : le CSV contient 14 identifiants EA distincts, dont exactement 10 ont un débit d'échantillonnage enregistré et 4 n'en ont aucun ; l'article décrit jusqu'à 14 AS simultanés, dont 10 équipés d'un contrôleur de débit ([Laguionie et al., 2022, §2.3.2](https://www.mdpi.com/2073-4433/13/8/1223)). De plus, le nombre de lignes EA correspond au nombre d'échantillons du tableau 1 pour 14 des 15 événements. Le seul écart est l'événement `1-7` / `#1_9` (6 EA dans le CSV contre 14 AS dans l'article). Enfin, sur les 15 événements rapprochés, les 131 lignes EA avec débit enregistré ont une médiane de débit de 0,171 L/min, proche des 0,17 L/min rapportés par l'article ; la médiane ligne-à-ligne de `sampling_flowrate_sd / sampling_flowrate` est de 3,68 %, proche des 3,4 % publiés. Ces deux derniers rapprochements sont descriptifs et ne reproduisent pas exactement la méthode d'agrégation des auteurs. Le CSV donne au total 186 lignes EA contre 194 échantillons article et 153 flags `significant` contre 148 ; quatre événements ont des différences de significativité. **Conclusion : EA≈AS est une identification fortement étayée mais non explicitement nommée ; l'écart de huit lignes est localisé à `#1_9` et sa cause reste non résolue.** Les lignes VEGA ne doivent pas être utilisées comme substituts sans preuve qu'elles figurent dans les 194 mesures publiées.

Le fichier de 2026 contient en outre quatre événements de rejet qui ne figurent pas dans les 15 événements de l'article :

| ID fichier 2026 | Début UTC | Lignes EA | Lignes VEGA |
|---|---|---:|---:|
| `#1_1` | 15/10/2019 08:00 | 10 | 0 |
| `#1_2` | 15/10/2019 10:15 | 14 | 6 |
| `#2_9` | 12/12/2019 10:10 | 12 | 12 |
| `#2_10` | 12/12/2019 13:00 | 12 | 12 |

Ainsi, les 19 identifiants distincts du CSV correspondent bien à 15 événements rapprochés de l'article et à quatre événements supplémentaires présents dans le dépôt 2026. Les 387 lignes du CSV sont des enregistrements de prélèvement, pas 387 observations indépendantes : elles se répartissent en 234 lignes `EA` et 153 lignes `VEGA`. Sur les 15 événements communs, le CSV contient 309 lignes (186 `EA`, 123 `VEGA`) ; les quatre événements supplémentaires représentent 78 lignes (48 `EA`, 30 `VEGA`). Les deux campagnes restent des contextes expérimentaux distincts ; 19 identifiants de rejet ne démontrent pas à eux seuls 19 réalisations statistiquement indépendantes.

### 3.2. Sémantique des méthodes et des champs : conséquences pour l'observable

Le dictionnaire définit `EA` comme un prélèvement d'un sac unique par événement d'échantillonnage et `VEGA` comme un prélèvement séquentiel de plusieurs sacs pendant l'expérience. `sampling_bag_id` vaut littéralement `NA` pour EA et identifie les sacs VEGA. Ces deux types ne doivent pas être agrégés comme s'ils avaient la même résolution temporelle. En particulier, les 153 lignes VEGA ne sont pas 153 réplicats indépendants supplémentaires des 234 lignes EA.

Le dictionnaire indique également que `sampling_flowrate` et son écart-type valent `NA` lorsque le préleveur ne dispose pas d'un enregistreur de débit ou que celui-ci fonctionne mal. Dans le CSV, les 153 lignes VEGA ont `NA` pour ce débit ; 65 des 234 lignes EA l'ont aussi. Ces absences ne sont pas des débits nuls et ne peuvent pas être imputées à zéro.

Autre point à documenter : le champ `helium_concentration_sampling_bg_passage_corrected` est renseigné pour les 196 lignes EA marquées `significant`, mais reste `NA` pour les 127 lignes VEGA marquées `significant`. La description du dictionnaire (« calculé uniquement lorsque la concentration corrigée du fond est significative ») n'explicite pas cette restriction apparente à EA. Il faut demander/identifier la règle de traitement de VEGA avant d'utiliser ce champ comme cible commune aux deux méthodes.
La transformation appliquée aux EA est néanmoins vérifiable : sur les 196 lignes EA significatives, le rapport `passage_corrected / bg_corrected` concorde avec `durée_du_prélèvement / durée_du_rejet` pour chaque ligne. Les rapports théoriques rencontrés sont 1,5 (15/10 min), 2,0 (20/10), 1,8 (15/8,33) et 1,667 (15/9) ; l'écart relatif maximal observé est d'environ 0,58 %, compatible avec l'arrondi des concentrations publiées. Il n'y a aucune ligne EA significative sans valeur de correction de passage. En revanche, les 127 VEGA significatifs n'ont tous aucune valeur de correction de passage. Cela confirme l'algorithme numérique appliqué aux EA, mais ne justifie pas d'appliquer la même correction aux VEGA : leur acquisition séquentielle en sacs de 5 minutes est un protocole temporel différent, dont la règle de traitement doit être explicitée par la source ou les auteurs.


Enfin, le champ `helium_concentration_decision_threshold` décrit le seuil absolu de décision (1,05 × concentration de fond), tandis que `helium_concentration_sampling_bg_corrected` est déjà décrit comme corrigé du fond. Le flag de significativité ne doit donc pas être recalculé en comparant naïvement ces deux colonnes : le seuil s'applique à la concentration mesurée avant soustraction du fond, conformément à la section 2.3.3 de l'article. La transformation exacte entre mesure, concentration excédentaire et correction de passage doit être documentée avant toute réimplémentation.

**Conséquence provisoire :** le rapprochement confirme la présence des 15 rejets étudiés dans l'article et identifie quatre rejets supplémentaires, mais il ne reproduit pas encore le décompte publié des prélèvements ni des résultats significatifs. L'ATC ne peut pas être construit comme une cible homogène sur les 387 lignes en divisant simplement une colonne de concentration par `helium_release_flow`. Il faut d'abord définir le sous-ensemble, la méthode de prélèvement, la correction de concentration, l'instant ou l'intervalle d'observation et l'unité de validation.


### 3.3. Inventaire descriptif des champs numériques du CSV de prélèvements

Les plages ci-dessous sont calculées sur les 387 lignes du fixture versionné, sans imputation des marqueurs littéraux. Elles décrivent les valeurs observées, pas leur validité physique ni leur précision.

| Champ | Valeurs numériques | Min–max | Commentaire |
|---|---:|---:|---|
| Latitude du rejet (°) | 387 | 50.51371–50.51404 | WGS84 selon le dictionnaire |
| Longitude du rejet (°) | 387 | 2.67255–2.67270 | WGS84 selon le dictionnaire |
| Hauteur du rejet (m) | 387 | 1.9–10.2 | |
| Débit de rejet (g/s) | 387 | 1.49–5.49 | |
| Latitude de prélèvement (°) | 387 | 50.51361–50.51870 | WGS84 selon le dictionnaire |
| Longitude de prélèvement (°) | 387 | 2.67169–2.67490 | WGS84 selon le dictionnaire |
| Hauteur de prélèvement (m) | 387 | 0.15–3.4 | EA : 0.15–3.4 m ; VEGA : 0.2–1.3 m |
| Débit de prélèvement (L/min) | 169 | 0.049–0.428 | 65 EA et les 153 VEGA ont `NA` |
| Écart-type du débit (L/min) | 169 | 0.002–0.104 | Même couverture que le débit |
| Concentration corrigée du fond (g/m³) | 323 | 5.14×10⁻⁵–3.95×10⁻³ | 196 EA et 127 VEGA numériques ; 64 résultats `< LC` |
| Concentration corrigée du passage (g/m³) | 196 | 1.07×10⁻⁴–4.39×10⁻³ | EA uniquement ; 127 VEGA significatifs sont également `NA` |

Les champs de coordonnées et de hauteurs du rejet/prélèvement sont renseignés sur les 387 lignes. En revanche, ce constat ne valide pas les coordonnées, la référence verticale, l'exactitude des positions ni la représentativité des hauteurs. L'inventaire du fichier séparé `DIFLU_instrument_locations` reste à effectuer avant de considérer l'audit spatial comme complet.

La couverture des débits est structurée par type : 169/234 EA ont un débit numérique, contre 0/153 VEGA. Le dictionnaire autorise des `NA` lorsqu'un enregistreur est absent ou défaillant, mais ne permet pas d'affirmer laquelle de ces causes s'applique à chaque ligne. Aucune correction de concentration ne doit donc être réimplémentée pour VEGA à partir du débit moyen EA.

## 4. Protocole d'évaluation : garde-fous minimaux

Avant tout benchmark :

- [ ] confirmer la granularité d'une ligne et l'identifiant de l'essai indépendant ; le rapprochement temporel et des conditions de rejet relie 15 des 19 identifiants `experiment_id` aux 15 expériences de l'article, tandis que quatre rejets supplémentaires sont présents dans le dépôt 2026 ; cette correspondance d'événements ne démontre pas à elle seule l'indépendance statistique des essais ;
- [ ] définir une cible unique, sa formule, ses unités et les conditions d'inclusion ;
- [ ] déterminer quelles covariables sont disponibles au moment de la prédiction et lesquelles risqueraient de divulguer indirectement la cible ;
- [ ] auditer les valeurs manquantes, le seuil de significativité, les limites de détection et les corrections ;
- [ ] vérifier la couverture des expériences et le nombre d'essais réellement indépendants ;
- [ ] effectuer toute partition au niveau de l'expérience (ou d'une unité indépendante plus large si la structure des données le requiert), jamais par tirage aléatoire de lignes issues d'un même essai ;
- [ ] définir des métriques adaptées à la question physique et une baseline explicite ;
- [ ] distinguer calibration/validation du modèle, incertitude expérimentale et généralisation à des conditions météorologiques ou géométriques non observées.

Avec peu d'expériences indépendantes, une validation leave-one-experiment-out peut être explorée, mais elle ne doit pas être adoptée automatiquement : la pertinence dépend de l'objectif de généralisation, de la dépendance entre campagnes et de la distribution des conditions expérimentales. Une analyse descriptive ou une comparaison déterministe avec des modèles physiques peut être plus défendable qu'un modèle appris.

## 5. Décision provisoire

**Statut : utilisable sous conditions pour un audit de données et une éventuelle comparaison physique ; pas encore validé pour un benchmark d'apprentissage.**

Le dépôt est une source primaire adaptée à l'étude de la dispersion d'un traceur dans les conditions observées, mais l'utilisabilité précise pour le MVP dépend encore de la vérification des dictionnaires, de la granularité des lignes, de la correspondance des variables et du protocole d'évaluation. Cette note ne présente aucun résultat de performance nouveau.

## Attribution et licence

La notice Dataverse indique l'Etalab Open Licence 2.0. Toute réutilisation doit conserver une attribution adéquate au jeu de données et aux auteurs, ainsi que la référence à l'article lorsque ses méthodes ou résultats sont repris. Vérifier les conditions affichées dans la version effectivement utilisée au moment de la réutilisation.

## Étapes restantes

Voir l'[issue #221](https://github.com/JM-Brun/J-DriftX/issues/221) pour la checklist d'audit sur les fichiers téléchargés et la décision finale d'usage MVP.

### 3.2. Deux types de préleveurs : ne pas confondre sacs, instruments et échantillons publiés

La relecture directe des dictionnaires du dépôt 2026 apporte une précision qui interdit de réduire sans preuve le terme générique « Atmospheric Samplers » (AS) de l'article à la seule catégorie EA :

- le dictionnaire des variables définit `EA` comme un prélèvement d'un sac unique par événement, et `VEGA` comme le prélèvement séquentiel de plusieurs sacs pendant un événement ;
- le dictionnaire des médias décrit explicitement les « EA-type air samplers (orange case) » et les « VEGA-type air samplers (grey case) » ; l'image 16, datée du 10/12/2019, montre les deux types ensemble ;
- l'article de 2022 décrit les AS comme des pompes connectées à des sacs Tedlar, mais ne nomme ni EA ni VEGA.

Sur les 15 événements rapprochés de l'article, le CSV contient 186 lignes EA et 123 lignes VEGA, soit 309 enregistrements de sacs au total. Les 123 lignes VEGA ne sont pas 123 préleveurs indépendants : elles correspondent à des prélèvements séquentiels rattachés à des identifiants de préleveur. Il faut donc séparer au minimum trois unités : instrument/préleveur, sac prélevé et résultat analytique. Les 194 « air samples » de l'article ne peuvent pas être comparés mécaniquement aux 186 lignes EA, ni aux 309 lignes du CSV.

**Conclusion mise à jour :** la nature instrumentale de EA et VEGA est désormais documentée, mais le périmètre exact des 194 résultats de l'article (EA seulement, ou combinaison/sélection des deux types) n'est toujours pas démontré. Le tableau de rapprochement EA↔AS reste une comparaison conditionnelle, pas une preuve de huit mesures manquantes. Aucune ligne ne doit être ajoutée, supprimée ou reclassée pour forcer l'égalité des comptes. La résolution exige une documentation de protocole ou une confirmation des auteurs précisant quels préleveurs et quels sacs alimentent les 194 résultats publiés.


### 3.3. Contrôle numérique reproductible des extrema ATC

Le contrôle automatisé est exposé par `scripts/audit_diflu.py` sous `atc_candidate_check`. Il calcule, uniquement pour les lignes EA marquées `significant` et disposant de valeurs numériques positives et finies :

```
ATC = helium_concentration_sampling_bg_passage_corrected / helium_release_flow
```

L'unité est `s m-3`. Les 153 lignes EA significatives rattachées aux 15 événements de l'article donnent les extrema suivants :

| Extrême | Événement article / CSV | Échantillon | ATC calculé | Valeur publiée |
|---|---|---|---:|---:|
| Minimum | 1-4 / `#1_6` | `B14` | 2,0227×10⁻⁵ s m⁻³ | 2,0×10⁻⁵ s m⁻³ |
| Maximum | 2-4 / `#2_4` | `A7_D7` | 1,5084×10⁻³ s m⁻³ | 1,5×10⁻³ s m⁻³ |

Le contrôle exige la concordance des identifiants d'événement et une erreur relative inférieure ou égale à 2 %, tolérance destinée à l'arrondi des valeurs publiées à deux chiffres significatifs. Sur le fixture versionné, les 196 lignes EA significatives des 19 événements ont une valeur ATC calculable ; 153 appartiennent aux 15 événements rapprochés de l'article. Le maximum global du dépôt est associé à `#1_1`, événement supplémentaire absent de l'article.

Ce résultat reproduit les deux extrema publiés, mais ne constitue pas une validation ligne par ligne, ne résout pas l'écart entre 153 flags significatifs du CSV et 148 résultats significatifs publiés, et ne valide ni les coordonnées projetées, ni les covariables météorologiques, ni VEGA. Aucune valeur VEGA n'est imputée. Ce contrôle ne justifie pas le lancement d'un benchmark d'apprentissage.
