# Plan d'intégration des résultats de la revue dans J-DriftX

> **Statut :** deux PDF de résumé exécutif sont maintenant présents dans `raw/reviews/`. Le présent plan organise leur traduction en décisions vérifiables ; il ne suppose pas que les résumés remplacent le protocole complet, les données de sélection ou les textes primaires.

## Objectif

Transformer la revue déposée sous `raw/` en décisions explicites pour le code, les tests, les benchmarks, la documentation et la feuille de route, tout en conservant la traçabilité entre une source et chaque modification du projet.

Le rapport brut est une **entrée documentaire**, pas une autorisation automatique à changer le modèle : les conclusions doivent être vérifiées dans les sources citées et confrontées aux hypothèses, à l'implémentation et aux tests de J-DriftX.

## Règles d'intégration

1. **Ne pas écraser le rapport brut.** Le fichier de revue ajouté sous `raw/` reste la source fournie par son auteur. Les synthèses et décisions dérivées sont éditées dans `docs/` et `site/`.
2. **Tracer chaque décision.** Chaque changement scientifique important doit pointer vers une section/page du rapport, les références primaires correspondantes et, si pertinent, une expérience ou un test.
3. **Séparer preuve et hypothèse.** Une affirmation issue d'un résumé ou d'une revue secondaire est marquée comme telle jusqu'à vérification. L'absence de méthode dans le corpus n'est pas une preuve de nouveauté.
4. **Ne pas introduire de dépendance méthodologique par effet de mode.** ROM, POD, PINNs, opérateurs neuronaux ou divergences directionnelles ne seront ajoutés que si leur rôle et leur comparaison sont justifiés par le problème physique.
5. **Faire passer les changements par des critères d'acceptation.** Une modification du noyau exige tests de propriétés, benchmark reproductible et analyse des limites. Une nouvelle baseline doit être comparable sur le même problème, les mêmes observations et un protocole documenté.
6. **Conserver les résultats négatifs et les incertitudes.** Les résultats qui ne soutiennent pas l'hypothèse initiale doivent rester visibles.

## Matrice de décision provisoire

Cette matrice est une **priorisation de travail**, fondée sur l'état actuel du dépôt et ses hypothèses explicites. Elle devra être confirmée, corrigée ou rejetée après examen de la revue systématique finale.

| Sujet | Décision provisoire | Modification autorisée maintenant | Preuve nécessaire avant de conclure |
|---|---|---|---|
| Métrique de temps de transport non symétrique | Priorité de recherche centrale, pas avantage démontré | Formaliser les définitions, hypothèses, domaine de validité et cas limites ; ajouter des tests mathématiques | Sources primaires vérifiées, propriétés théoriques et benchmarks discriminants |
| Solutions de similitude / réduction a priori | Conserver comme hypothèse principale | Prioriser un cas de référence analytique reproductible et documenter le coût par évaluation | Comparaison avec baselines pertinentes, erreurs et domaine de validité |
| POD/ROM et modèles substituts | Baselines de comparaison, non adversaires génériques | Définir un protocole équitable sur un cas commun ; éviter toute affirmation universelle | Même données, même découpage, budget de calcul explicite, métriques et incertitude |
| Réseaux de neurones, PINNs et opérateurs neuronaux | Pistes à évaluer si pertinentes, sans intégration prématurée au cœur | Ajouter au plan de benchmark les conditions de comparaison et les risques d'extrapolation | Corpus directement pertinent, implémentation reproductible et validation hors domaine |
| Calibration / identification de source (STE) | Après le noyau et le cas de référence | Préparer la séparation calibration-validation et les métriques d'identifiabilité | Données et baselines adaptées, analyse de sensibilité/incertitude |
| Terrain, topographie, SIG et cas réglementaires | Ne pas les laisser supplanter la validation fondamentale | Documenter les sources de données et les limites de licence ; différer les fonctionnalités aval | Cas de validation indépendant, provenance des données et cadre d'utilisation vérifié |
| Conservation, positivité, divergence nulle | Propriétés à prouver ou tester, jamais présumées | Lier chaque propriété à une hypothèse, un test ou une preuve clairement identifiée | Démonstration analytique et/ou tests couvrant le domaine annoncé |

## Séquence après ajout du rapport sous `raw/`

### 1. Enregistrer et identifier la revue

- Les deux résumés exécutifs présents sont `raw/reviews/2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf` et `raw/reviews/2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf` ; leurs liens sont documentés dans `raw/README.md`.
- Vérifier si un protocole complet, les requêtes exactes, les exports bibliographiques et les tableaux de sélection sont disponibles en complément ; ne pas inférer leur existence à partir des résumés.
- Noter la date/version du rapport, son périmètre, les bases réellement interrogées et ses limites d'accès.
- Ne pas confondre la revue finale avec les notes historiques déjà présentes dans `docs/02-revue-etat-art-2026.md`.

### 2. Extraire les décisions candidates

Pour chaque conclusion exploitable, enregistrer dans une matrice d'intégration :
- identifiant stable ;
- conclusion exacte et emplacement dans le rapport ;
- références primaires et statut de lecture (texte intégral, résumé, notice) ;
- axe A/B/C/D ;
- conséquence envisagée pour J-DriftX ;
- niveau de confiance et limites ;
- type de changement (théorie, code, tests, benchmark, documentation, roadmap) ;
- test ou critère d'acceptation ;
- décision : **retenu**, **à expérimenter**, **reporté**, ou **rejeté**, avec justification.

### 3. Vérifier les implications scientifiques

- Comparer les conclusions aux équations, hypothèses et implémentations existantes.
- Vérifier si les méthodes dites concurrentes répondent au même problème physique, aux mêmes observables et au même régime.
- Distinguer le coût de construction/entraînement du coût d'inférence ; publier les deux lorsqu'ils sont pertinents.
- Examiner l'extrapolation, la sensibilité aux conditions aux limites, l'incertitude et la reproductibilité.
- Ne pas généraliser les résultats d'un cas numérique à la dispersion atmosphérique entière.

### 4. Traduire les décisions en changements isolés

Créer des PR ciblées plutôt qu'une refonte opaque :
- **théorie et notation** : définitions, hypothèses, propositions et limites ;
- **noyau** : une modification scientifique à la fois, avec tests ;
- **benchmarks** : données versionnées ou scripts de génération, baselines, métriques et coûts ;
- **documentation publique** : positionnement aligné sur les preuves réellement disponibles ;
- **roadmap** : jalons et critères d'acceptation révisés, avec justification liée à la revue.

Chaque PR doit expliquer quelles conclusions elle applique, quelles conclusions elle n'applique pas et pourquoi.

## Critères de sortie de l'intégration

L'intégration ne sera considérée comme terminée que lorsque :

- [ ] la revue est présente dans `raw/` et son emplacement exact est référencé ;
- [ ] les conclusions qui modifient la stratégie ont été reliées à des sources vérifiables ;
- [ ] une matrice décisionnelle conserve les conclusions acceptées, différées et rejetées ;
- [ ] la feuille de route et le positionnement public ne contiennent pas de revendication plus forte que les preuves ;
- [ ] les changements du noyau sont couverts par des tests et benchmarks reproductibles ;
- [ ] Quarto, Ruff et pytest passent, ou chaque échec restant est explicitement documenté.

## Bibliographie annotée

La [bibliographie annotée J-DriftX](bibliographie-annotee-jdriftx.md) fournit des fiches Markdown éditables par famille : héritage historique, dérive de pulvérisation, ROM/apprentissage, identification de source, SIG/applications et analogies autour des métriques. Les fiches qualifient chaque référence comme source directe, baseline concurrente, complément, analogie ou contexte, et signalent les limites d'accès.

## Liens internes

- [Revue structurée actuelle](02-revue-etat-art-2026.md)
- [Choix de la méthode de revue systématique](06-choix-methode-revue-systematique.md)
- [Plan d'intégration scientifique et de validation](05-plan-validation-et-integration.md)
- [Questions scientifiques et techniques ouvertes](https://github.com/JM-Brun/J-DriftX/issues)
- [Sources primaires et documents bruts](../raw/README.md)
