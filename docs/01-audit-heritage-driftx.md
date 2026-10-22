# Audit du projet historique Drift-X (2006–2009)

> Audit établi en octobre 2026 dans le cadre de la reprise du projet sous le nom **J-DriftX**.
> Sources : chapitre Springer 2008 (fourni par l'auteur), notices CR Mécanique, HAL, Applied Geomatics, extraits bibliographiques publics.

## 1. Corpus historique du projet

Le projet **Drift-X** (modèle de dispersion atmosphérique de pesticides couplé à un SIG, développé à Cemagref/ITAP et I3M Montpellier) repose sur le corpus suivant :

1. **Thèse de J.-M. Brun sur la modélisation à complexité réduite de la dérive** (description de travail ; titre officiel, établissement et année à confirmer). L'article primaire de Mohammadi & Brun (2006) la cite comme 2007 ; certaines bibliographies secondaires donnent 2006. Non localisée dans les recherches consignées ; vérifier la page de titre et les notices institutionnelles avant de figer les métadonnées ou d'affirmer qu'elle n'a jamais été déposée/numérisée.
2. **Mohammadi, B. & Brun, J.-M. (2006)**. « Similitude généralisée et modélisation géométrique à complexité réduite ». *C. R. Mécanique* 334(10), 634–638. DOI 10.1016/j.crme.2006.06.007 — première formulation publique : assimilation de données partielles, solutions de similitude dans une métrique non symétrique basée sur les temps de transport, sans EDP ni maillage, évaluation ponctuelle.
3. **Mohammadi, B., Brun, J.-M. & Pironneau, O. (2006)**. « Reduced order modelling of dispersion ». Cette référence apparaît dans une bibliographie secondaire publiée, mais le recueil et les métadonnées éditoriales ne sont pas confirmés ; ne pas la présenter comme un chapitre Springer vérifié.
4. **Brun, J.-M. & Mohammadi, B. (2008)**. « Reduced-Order Modelling of Dispersion ». In Glowinski, R. & Neittaanmäki (eds), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, Dordrecht, chap. 14, pp. 245–256. DOI 10.1007/978-1-4020-8758-5_14. — Métadonnées éditeur confirmées ; dans le corpus de lecture actuel, seul le résumé et l'extrait des pages 245–246 ont été examinés. Ils décrivent l'approche multi-niveaux, les solutions de similitude dans une métrique non symétrique, l'assimilation de données, l'évaluation ponctuelle et l'analyse de sensibilité. Les détails des contraintes physiques et les exemples numériques du chapitre complet restent à vérifier dans les pages non lues.
5. **Bozon, N., Mohammadi, B. & Sinfort, C. (2008)**. « Similitude and non symmetric geometry for dispersion modelling ». e-sta vol. 5, numéro spécial STIC et Environnement'07.
6. **Bozon, N., Sinfort, C. & Mohammadi, B. (2009)**. « A GIS-based atmospheric dispersion model » — la plateforme **Drift-X** proprement dite : panache gaussien spatialisé, MNT, sorties raster géoréférencées, plugin **QGIS**. Dépôt HAL : https://hal.science/hal-00468863 (fichier : MO2009-PUB00026817).
7. **Bozon, N. & Mohammadi, B. (2009)**. « GIS-based atmospheric dispersion modelling ». *Applied Geomatics* 1(3), 59–74. DOI 10.1007/s12518-009-0006-0 — déclinaison journal de la plateforme.

## 2. Fond scientifique : ce que le projet affirmait

1. **Réduction a priori** : l'espace de recherche de la solution est construit à partir d'information physique (solutions de similitude de jets/panaches), et non à partir de snapshots coûteux d'un modèle complet (différence revendiquée avec les ROM-POD).
2. **Métrique non symétrique de transport** : généralisation des solutions de similitude connues en métrique cartésienne vers une métrique basée sur les **temps de transport**, pour représenter des vents non uniformes — verrou conceptuel central du projet.
3. **Sans EDP complète à chaque évaluation, sans maillage du domaine de calcul réduit** : selon les publications historiques, la solution peut être évaluée en un point sans calculer le champ entier. Les auteurs rapportent un faible coût ponctuel et envisagent des analyses répétées/Monte Carlo ; le coût de construction, d'assimilation et de préparation des champs doit être compté séparément, et le coût total reste à mesurer pour J-DriftX.
4. **Contraintes physiques revendiquées dans les publications** : les articles décrivent des propriétés structurelles recherchées (notamment divergence nulle du champ de vent restreint et bilan de masse dans la construction multi-niveaux). Leur portée dépend des hypothèses et de la formulation de chaque article ; la positivité, la linéarité et la satisfaction du modèle direct ne doivent pas être considérées comme garanties globales de toute implémentation sans définition et tests dédiés.
5. **Approche multi-niveaux** : chaque niveau fournit la condition d'entrée du niveau supérieur (champ proche de la buse → couche limite → transport longue distance).
6. **Assimilation de données partielles** pour l'identification des paramètres du modèle.
7. **Analyse de sensibilité** à double usage : analyse de risque et identification de source d'une pollution observée (problème inverse).
8. **Intégration SIG** : couplage à QGIS, MNT, raster géoréférencé, multi-échelles (parcelle → bassin versant), appliqué à la dérive de pulvérisation en viticulture.

## 3. Bilan forces / faiblesses

| # | Forces | Faiblesses héritées |
|---|---|---|
| 1 | Réduction a priori : évaluation ponctuelle sans calculer le champ complet dans les exemples historiques | Validation quantitative limitée face à des références CFD/LES ou campagnes de terrain ; peu de benchmarks chiffrés publiés |
| 2 | Proposition historique de métrique fondée sur les temps de transport, à formaliser et comparer | Formalisation mathématique dispersée entre plusieurs publications ; nouveauté exhaustive et transposabilité non établies par cette revue ciblée |
| 3 | Construction multi-niveaux conçue pour préserver divergence et bilan de masse sous les hypothèses de l'article | Portée exacte de ces propriétés à formaliser ; positivité, erreur d'approximation et choix du niveau à établir séparément |
| 4 | Calibration par assimilation | Assimilation rudimentaire (moindres carrés) : pas d'incertitudes, pas d'approche bayésienne |
| 5 | Multi-sources, sensibilité, identification de source | Identification de source non comparée aux méthodes STE qui se standardisent après 2010 |
| 6 | Intégration SIG documentée dès 2009 | Aucun dépôt public de code n'a été identifié dans le corpus consulté ; le dépôt GitHub examiné est resté vide. À confirmer auprès des auteurs avant de conclure à une absence générale de code. |
| 7 | Positionnement applicatif historique identifiable (pesticides, viticulture) | Corpus dispersé ; aucune synthèse de revue n'a été identifiée dans les recherches consignées, sans preuve d'absence exhaustive |

## 4. Dette technique et scientifique à la reprise

- **Dette code** : les publications et ressources examinées ne fournissent pas de dépôt de code exploitable ; il faut soit retrouver le code historique auprès des auteurs, soit reconstruire le prototype Drift-X (QGIS/Python) avec une traçabilité explicite.
- **Dette validation** : constituer dès maintenant un jeu de benchmarks public (validation croisée contre modèle gaussien de référence, données de campagnes de dérive publiées).
- **Dette formalisation** : écrire une définition autonome et auto-contenue de la métrique travel-time et de ses propriétés (une seule notation, une seule source de vérité).
- **Dette communication** : aucune synthèse en revue n'a été identifiée dans les recherches consignées ; cette absence de résultat n'établit pas qu'aucune publication de ce type n'existe. La reprise vise à produire une synthèse scientifique documentée (voir roadmap).

## 5. Ce qui a vieilli, ce qui n'a pas vieilli

**Hypothèses qui restent pertinentes à réévaluer** : combiner information physique et calibration par données ; exploiter une évaluation ponctuelle à faible coût ; étudier le far-field de la dérive et l'identification de source. Ni le coût négligeable, ni la validité hors domaine, ni l'utilité actuelle ne découlent de ces objectifs historiques : ils exigent des benchmarks et validations spécifiques.

**Le contexte a évolué** : ERA5/Copernicus, les MNT ouverts et certains capteurs à bas coût améliorent l'accès à des données, sans supprimer les problèmes de couverture, résolution, droits et qualité ; l'écosystème logiciel est passé des anciennes versions de QGIS aux versions actuelles ; les méthodes ROM/ML et les cadres réglementaires ont évolué et doivent être réexaminés à partir de sources datées.

## 6. Verdict de l'audit

Le corpus historique décrit une hypothèse méthodologique intéressante — réduction a priori fondée sur la similitude, métrique non symétrique de temps de transport et évaluation ponctuelle — mais ce dossier ne suffit pas à conclure que le cœur scientifique est correct, original au regard de toute la littérature, ou encore différenciant en 2026. Les lacunes ne sont pas seulement d'exécution : il reste à établir les hypothèses exactes, les propriétés mathématiques, les erreurs et le domaine de validité. **Recommandation : poursuivre sous forme d'hypothèses falsifiables**, avec formalisation et benchmarks reproductibles avant de revendiquer nouveauté ou supériorité.
