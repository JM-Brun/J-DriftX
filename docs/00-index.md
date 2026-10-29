# 00 — Index de navigation des notes techniques

Index de navigation de `docs/`, établi le 27 octobre 2026 et maintenu pour orienter vers les documents de référence. Il ne remplace pas les documents référencés. La gouvernance des scopes, des sources canoniques et des règles anti-redondance est définie dans [52 — Gouvernance documentaire](52-gouvernance-documentaire.md). Cet index est un parcours de navigation ; il ne constitue pas à lui seul l'inventaire de disposition fichier par fichier demandé par l'audit croisé.

## Règle de numérotation

Avant de créer une note `docs/NN-…`, **lister le dossier `docs/` et prendre le
plus petit numéro libre**. Les numéros 14, 15, 16, 17, 21 et 33 existent en double
(tableau ci-dessous) et de nombreux fichiers référencent d'autres notes par
numéro ; la collision a déjà exigé une renumérotation (la matrice de
traçabilité MVP-S, initialement numérotée 22, est devenue la note 27).
Le numéro 50 est désormais attribué à `50-protocole-oracle-couts-baseline-uniforme.md` (oracle indépendant et protocole de coûts S0 uniforme) et le numéro 51 à `51-reference-independante-cas-s0.md` (comparaison à référence indépendante EDP du cas S0) et le numéro 53 à `53-evaluation-puff-source-impulsionnelle.md` (évaluation dirigée d'une source impulsionnelle) et le numéro 54 à `54-transitoire-puff-edp-transitoire-marginale.md` (EDP transitoire du puff : marche en temps de la marginale transverse). Prochain numéro disponible après cette attribution : 55. Les notes 43 à 49 couvrent l’audit de la thèse, la stratégie de reprise, l’audit de l’article de 2006, le registre des anomalies, le contrat minimal de la baseline, le cas de référence autonome à écoulement uniforme et la matrice initiale des revendications historiques.

## Numéros en double

| Numéro | Fichier | Sujet |
|---|---|---|
| 14 | `14-protocole-audit-corpus-g0.md` | Protocole de l'audit du corpus historique G0 |
| 14 | `14-revue-mathematique-ciblee.md` | Revue mathématique ciblée de la métrique |
| 15 | `15-audit-adversarial-hallucinations.md` | Index de l'audit adversarial ; constats détaillés répartis dans `docs/audits/` |
| 15 | `15-audit-corpus-g0-resultats.md` | Résultats de l'audit du corpus G0 |
| 16 | `16-chapitre-2008-reconstruction-figures.md` | Reconstruction des figures du chapitre 2008 |
| 16 | `16-note-burgers-jdriftx.md` | Note Burgers appliquée à J-DriftX |
| 17 | `17-figure-02-geometries.md` | Figure 2 (géométries, scénario jouet) |
| 17 | `17-laboratoire-interactif.md` | Laboratoire interactif |
| 21 | `21-bilan-mvp-s-1d.md` | Bilan de reproductibilité du MVP-S 1D |
| 21 | `21-jeux-donnees-seconde-vague-et-cas-synthetiques.md` | Seconde vague de jeux de données et cas synthétiques S0-S3 |
| 33 | `33-test-contre-exemple-cisaillement.md` | Test du contre-exemple de cisaillement (coût projeté) |
| 33 | `33-figure-04-superposition-sources.md` | Figure 4 du chapitre 2008 : superposition de deux sources |

## Notes et ressources de référence

| Fichier | Sujet |
|---|---|
| `01-audit-heritage-driftx.md` | Audit de l'héritage Drift-X (2006-2009) |
| `02-revue-etat-art-2026.md` | Revue de l'état de l'art (2026) |
| `04-revues-papiers-sources.md` | Index des fiches de lecture source par source |
| `15-audit-adversarial-hallucinations.md` | Index des constats adversariaux et liens vers les dossiers spécialisés |
| `audits/15a-audit-bibliographique.md` | Constats bibliographiques, versions et métadonnées |
| `audits/15b-audit-portee-scientifique.md` | Constats sur la portée scientifique, hypothèses et revendications |
| `audits/15c-audit-methodologie-et-coherence.md` | Méthodologie de l'audit, niveau de preuve et cohérence documentaire |
| `05-plan-validation-et-integration.md` | Protocole public de validation et d'intégration |
| `06-choix-methode-revue-systematique.md` | Choix de la méthode de revue systématique |
| `08-decision-utilite-et-preuve.md` | Cadre de décision et de preuve |
| `09-fallback-modele-jouet.md` | Fallback « modèle jouet » |
| `12-catalogue-donnees-transport-dispersion.md` | Catalogue de jeux de données transport/dispersion |
| `18-carte-articulation-scientifique.md` | Carte d'articulation scientifique |
| `19-investigation-g0s-temps-de-parcours.md` | Investigation G0-S : temps de parcours dirigé ($T_{\mathrm{arr}}$/$T_{\mathrm{proj}}$) |
| `20-audit-technique-jeux-donnees.md` | Audit technique des jeux de données (ERIES, DIFLU, DATEM, ETEX) |
| `22-audit-package-code.md` | Audit du package au regard de la charte qualité |
| `23-figure-01-reconstruction-vent.md` | Figure 1 : reconstruction du vent à deux mesures |
| `24-classes-stabilite-pasquill-objet.md` | Objets ClasseStabilite et FormeSigmaZ |
| `25-audit-harmonisation-oop-2026.md` | Audit d'harmonisation OOP du package (P1-P3) |
| `26-investigation-adjoint-temps-transport.md` | Investigation de l'adjoint du temps de transport |
| `27-matrice-tracabilite-mvp-s.md` | Matrice de traçabilité MVP-S |
| `28-revue-ciblage-graphe-2026-10-27.md` | Revue du ciblage du graphe de connaissances (27/10/2026) |
| `29-audit-tracabilite-mvp-s-2026-10-27.md` | Audit de la traçabilité MVP-S (27/10/2026) |
| `30-glossaire-mathematique-autonome-g0s.md` | Glossaire mathématique autonome G0-S |
| `31-investigation-champ-multiniveaux.md` | Investigation du champ de vent multi-niveaux historique |
| `32-conservation-coordonnees-travel-time.md` | Bilan de conservation dans des coordonnées travel-time : dérivation conditionnelle et transcriptions des sources (2006, 2008, 2009) |
| `33-figure-04-superposition-sources.md` | Figure 4 du chapitre 2008 : superposition de deux sources, champ à trois mesures |
| `34-figure-05-relief.md` | Figure 5 du chapitre 2008 : relief synthétique, correction du point de calcul |
| `35-figure-03-modele-reduit-edp.md` | Figure 3 du chapitre 2008 : modèle réduit vs EDP, deux résolutions indépendantes |
| `36-identification-source.md` | Figure 6 du chapitre 2008 : identification de source, carte de sensibilité du coût |
| `37-transformation-tau-eta-cas-uniforme.md` | Carte travel-time explicite pour le champ uniforme de référence : jacobien, théorème conditionnel d'égalité des flux, verdict sur les affirmations historiques |
| `38-cadrage-g0a-besoin-applicatif.md` | Cadrage G0-A : utilisateur cible, décision, observable, baseline équitable et limites du corpus CAPRIV |
| `39-squelette-benchmarks-s0.md` | Squelette de benchmarks : cas analytique S0, registres de cas et de métriques, évaluation reproductible, standards (MVK, ASTM D6589, CF, PDEBench) |
| `40-standards-qualite-tests-proprietes.md` | Standards qualité : tests de propriété (Hypothesis), objet et domaine (OOP/DDD), diagnostic architecture et recommandations |
| `41-unification-source-panache.md` | Unification de la source du panache : objet SourcePanache partagé par les familles S0, carte concepts-modules et recommandations P2/P3 |
| `42-contrats-interoperabilite.md` | Contrats d'interopérabilité : protocoles PEP 544 (relief, vent 2D/3D, concentrations), MNT ESRI ASCII Grid, profil de vent en loi de puissance |
| `43-audit-these-brun-conservation-g0s.md` | Audit de la thèse de Brun : équations (7.12)–(7.13), conservation du transport lointain et contrôle dimensionnel |
| `44-strategie-reprise-et-elargissement-scientifique.md` | Stratégie : reconstruire la base historique, corriger les erreurs de façon traçable, puis élargir les méthodes et domaines applicatifs |
| `45-audit-article-mohammadi-brun-2006.md` | Audit critique de la source fondatrice 2006 : pseudo-distance orientée, conservation globale, assimilation et coûts rapportés |
| `46-registre-erreurs-incoherences-documentaires.md` | Registre central des erreurs, anomalies, ambiguïtés et incohérences entre documents |
| `47-contrat-minimal-baseline.md` | Contrat minimal de la baseline : statut figé par capacité historique (définie / partiellement définie / annoncée seulement / non reproductible) |
| `48-cas-reference-autonome-ecoulement-uniforme.md` | Cas de référence autonome : écoulement uniforme (unités, domaine, conditions aux limites, solution de référence, observable, limites ; cisaillement en contre-exemple distinct) |
| `49-matrice-revendications-baseline.md` | Matrice initiale des revendications historiques : source/version/localisation, unités, hypothèses, preuves et statut de définition |
| `50-protocole-oracle-couts-baseline-uniforme.md` | Oracle indépendant et protocole de coûts pour le cas S0 uniforme ; protocole implémenté, mesures à exécuter |
| `51-reference-independante-cas-s0.md` | Comparaison EDP/solution fermée du cas S0, convergence, métriques et limites |
| `52-gouvernance-documentaire.md` | Frontière public/privé, sources canoniques, scopes, règles anti-redondance et validation des références |
| `53-evaluation-puff-source-impulsionnelle.md` | Évaluation dirigée d'une source impulsionnelle (puff) : temps dirigé t = τ, maximum temporel C(t), écart quantifié |
| `54-transitoire-puff-edp-transitoire-marginale.md` | EDP transitoire du puff : marche en temps de la marginale transverse, structure longitudinale analytique, écarts calibrés |
| `bibliographie/fondements-et-heritage.md` | Synthèse bibliographique : fondements et héritage |
| `bibliographie/identification-source-assimilation.md` | Bibliographie thématique : identification de source et assimilation |
| `bibliographie/metriques-et-analogies.md` | Bibliographie thématique : métriques et analogies |
| `bibliographie/rom-et-apprentissage.md` | Bibliographie thématique : modèles réduits et apprentissage |
| `bibliographie/sig-exposition-applications.md` | Bibliographie thématique : SIG, exposition et applications |
| `bibliographie/spray-drift-et-modeles-operationnels.md` | Bibliographie thématique : dérive de pulvérisation et modèles opérationnels |
| `bibliographie/sources/these-brun.md` | Fiche source : thèse de J.-M. Brun (année/titre à confirmer sur la page de titre) |
| `bibliographie/sources/mohammadi-brun-2006-cr-mecanique.md` | Fiche source : Mohammadi & Brun (2006), C. R. Mécanique |
| `bibliographie/sources/mohammadi-brun-pironneau-2006.md` | Fiche de traçabilité d'une référence non retrouvée |
| `bibliographie/sources/brun-mohammadi-2008-chapitre.md` | Fiche source : chapitre Springer 2008 |
| `bibliographie/sources/bozon-mohammadi-sinfort-2008-esta.md` | Fiche source : e-sta 2008 |
| `bibliographie/sources/bozon-sinfort-mohammadi-2009-driftx.md` | Fiche source : plateforme Drift-X 2009 / manuscrit HAL |
| `bibliographie/sources/bozon-mohammadi-2009-applied-geomatics.md` | Fiche source : Applied Geomatics 2009 |
| `bibliographie/synthese-acces-sources-historique-2026-10.md` | Découvertes bibliographiques et instantané historique d'accès aux sources |
| `references.md` | Références et sources du projet |
| `bibliographie-annotee-jdriftx.md` | Bibliographie annotée |
| `bibliographie/` | Synthèses thématiques et fiches source par source sous `bibliographie/sources/` |
| `visuels-g0s/README.md` | Index et conventions des visuels G0-S |
| `visuels-g0s/prompts/infographie-glossaire-g0s.md` | Prompt source de l'infographie du glossaire G0-S |
| `visuels-g0s/` | Visuels G0-S (SVG source et générés) |

Les notes numérotées en double figurent dans le tableau dédié ci-dessus. L'audit adversarial a été découpé par rôle : son fichier numéroté est désormais un index ; les constats restent dans `docs/audits/`. Pour décider si un document est canonique, redondant ou historique, appliquer [la gouvernance documentaire](52-gouvernance-documentaire.md). Le registre détaillé de disposition et le suivi opérationnel sont maintenus dans l'espace interne du projet ; ils ne sont pas exposés depuis cet index public.
