# Matrice initiale de traçabilité des revendications historiques

**État :** version initiale partielle — 29 octobre 2026. Cette matrice sépare ce que les sources disent, les vérifications réellement faites et ce qui reste nécessaire pour une baseline reproductible. Elle ne valide pas le modèle historique dans son ensemble.

## Statuts

- **Partiellement défini** : la structure est connue, mais des hypothèses, détails ou cas limites manquent.
- **Annoncé seulement** : résultat rapporté, sans protocole suffisant pour le reproduire.
- **Non reproductible en l'état** : transcription, paramètres ou conditions insuffisants pour une implémentation fidèle.
- **Vérifié** qualifie uniquement la preuve mentionnée dans la ligne, pas toutes les affirmations d'une source.

Le registre des anomalies et leurs identifiants sont centralisés dans le [registre DRX-ERR](46-registre-erreurs-incoherences-documentaires.md). La conservation est analysée dans [docs/32](32-conservation-coordonnees-travel-time.md), [docs/37](37-transformation-tau-eta-cas-uniforme.md) et [l'issue #123](https://github.com/JM-Brun/J-DriftX/issues/123).

## Matrice

| ID | Revendication / capacité | Source exacte | Hypothèses et unités | Preuve actuelle | Statut | Travail restant |
|---|---|---|---|---|---|---|
| CLM-2006-01 | Profil de similitude d'un scalaire passif | Mohammadi & Brun (2006), §2, équation (2), p. imprimée 635 | Cas décrit : émission à l'origine, écoulement plan uniforme (U). Fonctions (a(U)), (b(U,\delta)) contraintes par monotonies ; unités et expressions doivent être confirmées sur le fac-similé. | L'extraction versionnée donne la structure et les contraintes qualitatives, mais n'est pas une transcription typographique fiable. | **Partiellement défini** | Vérifier exposants, paramètres et unités ; établir un test analytique uniforme. |
| CLM-2006-02 | Pseudo-distance / temps de migration dirigé | Mohammadi & Brun (2006), §3, équation (3), p. 635 ; [audit 45](45-audit-article-mohammadi-brun-2006.md) | Caractéristique supposée unique, sources et puits écartés ; projection de la cible. Les auteurs reconnaissent l'échec possible de séparation, symétrie et inégalité triangulaire. | Ces limites métriques sont explicites. Le contre-exemple de cisaillement teste une construction projetée particulière, pas toute définition de temps de transport. | **Partiellement défini** | Formaliser existence/unicité, projection multiple, stagnation, points amont, sorties du domaine et échecs de trajectoire ; comparer à une implémentation fidèle. |
| CLM-2006-03 | Conservation de la quantité émise | Mohammadi & Brun (2006), §3, p. 636, contrainte intégrale globale sur (mathbb R^3) | Sous (c) concentration massique volumique, l'intégrale volumique est une masse ; émission, durée, dépôt, sources/puits et frontières doivent être cohérents. | Une intégrale globale est liée à la quantité totale émise. Cela ne prouve pas un flux constant sur chaque surface iso-temps. Les glyphes doivent encore être vérifiés visuellement. | **Partiellement défini** | Vérifier l'équation sur le PDF éditeur versionné et reconstruire le bilan avec unités et hypothèses explicites. |
| CLM-2006-04 | Reconstruction du champ de vitesse par potentiel | Mohammadi & Brun (2006), §3, équation (4), p. 636 | L'extraction suggère (mathbf u=\nablaphi) et une optimisation à partir de (n_{obs}) observations, mais préserve mal fonctionnel, signe/opérateur et contraintes. Un potentiel régulier impose un champ irrotationnel. | L'extraction ne permet pas de certifier l'équation. | **Non reproductible en l'état** | Transcrire l'équation (4) depuis le fac-similé ; préciser conditions aux limites, contraintes et identifiabilité. |
| CLM-2006-05 | Gain de coût annoncé de (10^3)–(10^4) par évaluation ponctuelle | Mohammadi & Brun (2006), §5, pp. 636–638 | Comparaison rapportée à une EDP éléments finis, environ 3 000 points et même champ de vitesse ; précision et coût de préparation insuffisamment décrits. | Chiffre rapporté par la source, sans benchmark exécutable équivalent dans le dépôt. | **Annoncé seulement** | Comparer à précision égale ; mesurer préparation, calibration, requête, champ complet, mémoire et erreur. |
| CLM-2008-TH-01 | (c^+) et conservation du transport lointain | Brun & Mohammadi (2008), §2.2, p. imprimée 248 ; thèse, §7.3, équations (7.12)–(7.13), p. 129 | Avec ([c_{loc}]=\mathrm{kg\,m^{-3}}), l'intégrale verticale donne kg·m⁻² et son intégrale surfacique kg. Le produit (u^+_{loc}c_{loc}), avec (u^+_{loc}) sans dimension, donne kg·m⁻³ puis kg·m⁻¹ après intégration surfacique. | Incompatibilité dimensionnelle confirmée sous ces unités ; l'intention historique demeure inconnue. La reconstruction choisit l'inventaire de masse issu de l'intégrale verticale. | **Diagnostic vérifié ; conservation historique non démontrée** | Ne pas réécrire la source ; tester l'inventaire retenu et distinguer masse, flux massique et concentration pondérée. |
| CLM-2009-01 | Bilan de conservation du modèle GIS / Drift-X | Manuscrit STIC & Environnement 2009, HAL `hal-00468863`, équations (28)–(31), pages imprimées à réancrer | Le diagnostic dimensionnel suppose (c_i) concentration volumique et (K=\int c_{inj}(t)dt) masse émise. Ce manuscrit n'est pas la version JESA 2010. | Des incompatibilités sous ces interprétations sont consignées dans DRX-ERR-008/009 ; la correction voulue n'est pas établie. | **Partiellement défini** | Réancrer les équations et comparer au fichier associé à la notice HAL JESA `hal-02594312`, sans substituer le manuscrit 2009. |
| CLM-2009-02 | Construction multi-niveaux et restriction des champs | Manuscrit auteur 2009 ; [fiche technique détaillée](bibliographie/sources/bozon-sinfort-mohammadi-2009-driftx.md) | Le manuscrit décrit des rectangles emboîtés et une restriction du vent et de la concentration entre niveaux. Les conditions suffisantes de conservation aux interfaces ne sont pas établies ici. | Description textuelle disponible ; reproduction moderne indépendante non démontrée. | **Partiellement défini** | Formaliser les opérateurs, hypothèses et erreurs ; tester les bilans à chaque interface. |
| CLM-CODE-01 | Primitive Python `temps_transport` | [README](../README.md) et glossaire G0-S | Somme longueur/norme de vitesse sur une polyligne fournie ; ne calcule ni caractéristiques ni projection et ignore le signe de la vitesse. | Le README précise qu'il ne s'agit pas de la pseudo-distance historique. | **Primitive limitée définie ; non équivalente à l'algorithme historique** | Maintenir cette distinction dans les API, tests et documentation. |
| CLM-TEST-01 | Contre-exemple analytique de cisaillement | [docs/33](33-test-contre-exemple-cisaillement.md), [test](../tests/test_shear_projected_cost.py), issue #123 | Pour (mathbf u=(v(y),0)), (d_A=(x-x_A)/v(y_A)), on obtient (mathbf u\cdot\nabla d_A=v(y)/v(y_A)). | Avec (v(y)=1+y^2), (y_A=0), (y=1), le résidu vaut 2, pas 1. | **Vérifié pour ce champ et cette construction** | Garder le test de régression ; ne pas généraliser à toutes les constructions de temps de transport. |

## Limites et règles

1. Les pages mentionnées sont les **pages imprimées** lorsque cela est indiqué ; la pagination PDF doit être ajoutée après vérification.
2. Les diagnostics dimensionnels sont conditionnels aux unités explicitées et ne révèlent pas l'intention des auteurs.
3. « Partiellement défini » ne signifie pas que la méthode est fausse : la spécification exécutable demeure incomplète.
4. Le manuscrit HAL 2009 et l'article JESA 2010 sont des objets bibliographiques distincts. Leur équivalence n'est pas présumée ; la comparaison des équations de la version JESA reste ouverte.
5. Les gains historiques ne sont pas des résultats reproductibles sans protocole, données, précision et coût total.
6. Cette première matrice ne couvre pas encore exhaustivement toutes les capacités historiques.

## Prochaines entrées

- Vérifier visuellement les équations (1), (2) et (4) de 2006 sur le PDF versionné.
- Comparer les équations de conservation du manuscrit 2009 et de l'article JESA 2010.
- Formaliser le modèle multi-niveaux et les bilans aux interfaces.
- Définir le protocole de benchmark de la baseline.

## Sources de vérité

- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
- [Issue #123 — conservation G0-S](https://github.com/JM-Brun/J-DriftX/issues/123)
- [Issue #233 — registre d'anomalies](https://github.com/JM-Brun/J-DriftX/issues/233)
- [Audit 2006](45-audit-article-mohammadi-brun-2006.md)
- [Audit de la thèse](43-audit-these-brun-conservation-g0s.md)
- [Registre DRX-ERR](46-registre-erreurs-incoherences-documentaires.md)
