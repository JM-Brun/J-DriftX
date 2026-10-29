# Audit du projet historique Drift-X (2006–2009)

> Audit établi en octobre 2026 dans le cadre de la reprise du projet sous le nom **J-DriftX**.
> Sources : chapitre Springer 2008 (fourni par l'auteur), notices CR Mécanique, HAL, Applied Geomatics, extraits bibliographiques publics.

## 1. Corpus historique du projet

Le projet **Drift-X** (modèle de dispersion atmosphérique de pesticides couplé à un SIG, développé à Cemagref/ITAP et I3M Montpellier) repose sur le corpus suivant :

1. **Brun, J.-M.**, *Modèles à complexité réduite de transport pour applications environnementales*, thèse. Le PDF est déjà versionné dans `raw/` et associé aux notices [AGRIS/INRAE](https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c) et [HAL](https://hal.inrae.fr/tel-02589999/document). Le titre, la pagination, l'année exacte et l'identité du binaire avec le fichier HAL restent à authentifier ; ne plus décrire la thèse comme non localisée. La thèse est une source historique à auditer, non une autorité qui rendrait ses équations infaillibles.
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

## 6. Principe de reprise : reconstruire, corriger, puis élargir

Le projet historique est un point de départ scientifique et fonctionnel, pas un carcan. La première cible de J-DriftX est de reconstruire une base à peu près équivalente quant aux idées et aux questions couvertes — similitude, transport dirigé, construction multi-niveaux, évaluation réduite, assimilation et dispersion atmosphérique — avec des définitions explicites et des tests indépendants. Cela ne signifie pas reproduire des erreurs de calcul, des incohérences dimensionnelles, des hypothèses implicites ou des défauts de logiciel.

Toute erreur trouvée dans une source doit être enregistrée avec sa page/équation, sa transcription exacte, son type, son impact démontré, une correction proposée et un test de vérification. La source historique reste citée fidèlement ; la correction est portée par une reconstruction ou une implémentation distincte. Si l'intention des auteurs ne peut être établie, conserver plusieurs interprétations possibles au lieu d'en inventer une.

Le périmètre historique pesticides/viticulture sert de cas de référence. Une fois une base comparable reproduite, J-DriftX pourra étudier d'autres pollutions atmosphériques ou autres scalaires transportés : rejets industriels, pollution urbaine, contaminants chimiques, scénarios radiologiques ou nucléaires, etc. Chaque extension doit cependant examiner les mécanismes propres au domaine (réactivité, dépôt, décroissance, aérosols, sources/puits, flottabilité, turbulence) et être validée contre des baselines adaptées. L'objectif est une généralisation justifiée par les équations et les données, pas l'application aveugle d'un modèle unique à toutes les substances.

Les méthodes récentes — modèles physiques, solveurs EDP, ROM, statistiques, apprentissage automatique, opérateurs neuronaux ou méthodes hybrides — peuvent compléter ou remplacer une partie de l'approche historique si une comparaison reproductible démontre un intérêt. Une hypothèse historique réfutée doit pouvoir être restreinte ou abandonnée.

Le protocole détaillé et la séquence de travail sont définis dans [la stratégie de reprise et d'élargissement](44-strategie-reprise-et-elargissement-scientifique.md).

## 7. Verdict de l'audit

Le corpus historique décrit une hypothèse méthodologique intéressante — réduction a priori fondée sur la similitude, métrique non symétrique de temps de transport et évaluation ponctuelle — mais ce dossier ne suffit pas à conclure que le cœur scientifique est correct, original au regard de toute la littérature, ou encore différenciant en 2026. Les lacunes ne sont pas seulement d'exécution : il reste à établir les hypothèses exactes, les propriétés mathématiques, les erreurs et le domaine de validité. **Recommandation : poursuivre sous forme d'hypothèses falsifiables**, avec formalisation et benchmarks reproductibles avant de revendiquer nouveauté ou supériorité.
