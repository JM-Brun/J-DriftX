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

Les sources donnent des comptes qui décrivent des périmètres différents :

- l'article de 2022 porte sur 15 expériences : 7 du 15 au 17 octobre 2019 et 8 du 10 au 12 décembre 2019 ;
- il rapporte 194 prélèvements d'air significatifs en aval, auxquels s'ajoute un prélèvement amont de contrôle par expérience ;
- la notice du dépôt de données publiée en 2026 décrit 19 expériences et annonce des données supplémentaires (mesures intégrées, mesures d'hélium en temps réel, données météorologiques et micrométéorologiques, documentation instrumentale) ;
- l'audit automatisé du fichier ciblé rapporte 387 lignes, dont 234 EA et 153 VEGA.

Ces comptes ne doivent pas être forcés à correspondre. L'audit doit établir la signification de chaque ligne et relier explicitement, lorsque c'est possible, les identifiants d'expérience, de prélèvement et de sac. Il faut aussi vérifier si les catégories EA et VEGA sont des méthodes, des instruments ou des représentations complémentaires d'un même événement, sans le présumer.

## 4. Protocole d'évaluation : garde-fous minimaux

Avant tout benchmark :

- [ ] confirmer la granularité d'une ligne et l'identifiant de l'essai indépendant ;
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
