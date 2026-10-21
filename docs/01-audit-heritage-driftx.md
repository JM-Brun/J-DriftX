# Audit du projet historique Drift-X (2006–2009)

> Audit établi en octobre 2026 dans le cadre de la reprise du projet sous le nom **J-DriftX**.
> Sources : chapitre Springer 2008 (fourni par l'auteur), notices CR Mécanique, HAL, Applied Geomatics, extraits bibliographiques publics.

## 1. Corpus historique du projet

Le projet **Drift-X** (modèle de dispersion atmosphérique de pesticides couplé à un SIG, développé à Cemagref/ITAP et I3M Montpellier) repose sur le corpus suivant :

1. **Brun, J.-M. (2006)**. *Modélisation à complexité réduite de la dérive*. Thèse de doctorat, Université Montpellier II.
2. **Mohammadi, B. & Brun, J.-M. (2006)**. « Similitude généralisée et modélisation géométrique à complexité réduite ». *C. R. Mécanique* 334(10), 634–638. DOI 10.1016/j.crme.2006.06.007 — première formulation publique : assimilation de données partielles, solutions de similitude dans une métrique non symétrique basée sur les temps de transport, sans EDP ni maillage, évaluation ponctuelle.
3. **Mohammadi, B., Brun, J.-M. & Pironneau, O. (2006)**. « Reduced order modelling of dispersion ». In *Numerical Analysis and Scientific Computing with PDE and their challenging applications*, Springer.
4. **Brun, J.-M. & Mohammadi, B. (2008)**. « Reduced-Order Modelling of Dispersion ». In Glowinski, R. & Neittaanmäki, P. (eds), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, Dordrecht, chap. 14, p. 245 et s. — version longue de référence : approche multi-niveaux, similitude généralisée, contraintes physiques (incompressibilité du vent généré, conservation, positivité, linéarité), exemples numériques multi-sources, analyse de sensibilité pour l'identification de source et l'analyse de risque.
5. **Bozon, N., Mohammadi, B. & Sinfort, C. (2008)**. « Similitude and non symmetric geometry for dispersion modelling ». e-sta vol. 5, numéro spécial STIC et Environnement'07.
6. **Bozon, N., Sinfort, C. & Mohammadi, B. (2009)**. « A GIS-based atmospheric dispersion model » — la plateforme **Drift-X** proprement dite : panache gaussien spatialisé, MNT, sorties raster géoréférencées, plugin **QGIS**. Dépôt HAL : https://hal.science/hal-00468863 (fichier : MO2009-PUB00026817).
7. **Mohammadi, B. & Bozon, N. (2009)**. « GIS-based atmospheric dispersion modelling ». *Applied Geomatics* 1, 33–39. DOI 10.1007/s12518-009-0006-0 — déclinaison journal de la plateforme.

## 2. Fond scientifique : ce que le projet affirmait

1. **Réduction a priori** : l'espace de recherche de la solution est construit à partir d'information physique (solutions de similitude de jets/panaches), et non à partir de snapshots coûteux d'un modèle complet (différence revendiquée avec les ROM-POD).
2. **Métrique non symétrique de transport** : généralisation des solutions de similitude connues en métrique cartésienne vers une métrique basée sur les **temps de transport**, pour représenter des vents non uniformes — verrou conceptuel central du projet.
3. **Sans EDP, sans maillage** : pas de résolution d'équations aux dérivées partielles ; la solution s'évalue en tout point isolé, sans calculer le champ entier. Coût marginal quasi nul, compatible Monte Carlo massif pour l'analyse de risque.
4. **Contraintes physiques** : le modèle approché est contraint à être solution du modèle direct (incompressibilité/divergence nulle du vent généré, conservation de la masse, positivité, linéarité).
5. **Approche multi-niveaux** : chaque niveau fournit la condition d'entrée du niveau supérieur (champ proche de la buse → couche limite → transport longue distance).
6. **Assimilation de données partielles** pour l'identification des paramètres du modèle.
7. **Analyse de sensibilité** à double usage : analyse de risque et identification de source d'une pollution observée (problème inverse).
8. **Intégration SIG** : couplage à QGIS, MNT, raster géoréférencé, multi-échelles (parcelle → bassin versant), appliqué à la dérive de pulvérisation en viticulture.

## 3. Bilan forces / faiblesses

| # | Forces | Faiblesses héritées |
|---|---|---|
| 1 | Réduction a priori : coût indépendant de la taille du domaine, évaluable en un point | Validation quantitative limitée face à des références CFD/LES ou campagnes de terrain ; peu de benchmarks chiffrés publiés |
| 2 | Idée de métrique travel-time originale, transposable | Formalisation mathématique de la métrique non symétrique dispersée entre plusieurs publications |
| 3 | Contraintes physiques (conservation, positivité, divergence nulle) | Hiérarchie multi-niveaux sans estimateur d'erreur ni critère de choix du niveau |
| 4 | Calibration par assimilation | Assimilation rudimentaire (moindres carrés) : pas d'incertitudes, pas d'approche bayésienne |
| 5 | Multi-sources, sensibilité, identification de source | Identification de source non comparée aux méthodes STE qui se standardisent après 2010 |
| 6 | Avant-garde SIG : plugin QGIS dès 2009 | Code du plugin non versionné/publié — dette technique directe (le dépôt GitHub est resté vide) |
| 7 | Positionnement applicatif clair (pesticides, viticulture) | Anglais de publication perfectible, corpus dispersé, pas d'article de synthèse en revue |

## 4. Dette technique et scientifique à la reprise

- **Dette code** : aucun dépôt de code n'a accompagné les publications ; le prototype Drift-X (QGIS/Python) doit être reconstruit proprement.
- **Dette validation** : constituer dès maintenant un jeu de benchmarks public (validation croisée contre modèle gaussien de référence, données de campagnes de dérive publiées).
- **Dette formalisation** : écrire une définition autonome et auto-contenue de la métrique travel-time et de ses propriétés (une seule notation, une seule source de vérité).
- **Dette communication** : l'ensemble n'a jamais été consolidé en un article de revue ; c'est l'objectif scientifique principal de la reprise (voir roadmap).

## 5. Ce qui a vieilli, ce qui n'a pas vieilli

**N'a pas vieilli** : le paradigme réduction a priori + calibration par données (aujourd'hui nommé *physics + data* ou *hybrid modelling*) ; la contrainte de coût nul par évaluation ponctuelle ; l'application far-field de la dérive ; le besoin d'identification de source.

**A vieilli** : les données disponibles (en 2006, MNT et météo difficiles d'accès — aujourd'hui ERA5/Copernicus, IGN RGE Alti, capteurs météo low-cost) ; la cible logicielle (QGIS 0.x → QGIS 3.x/4 avec traitement Python natif) ; l'état de l'art ROM/ML (voir revue 2026) ; le contexte réglementaire (Directive 2009/128/CE, révision EPA Appendix W 2024).

## 6. Verdict de l'audit

Le cœur scientifique est **sain, original et toujours différenciant**. Les faiblesses sont toutes des faiblesses d'exécution (code, validation, consolidation), corrigeables dans une reprise open-source structurée. **Recommandation : reprendre.** Conditions : benchmarks publics d'abord, code moderne ensuite, article de synthèse enfin.
