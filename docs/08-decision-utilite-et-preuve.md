# Décider de l'utilité de J-DriftX et construire une preuve

> **Statut :** cadre de décision et plan de validation proposés. Ce document ne conclut ni à l'utilité ni à l'inutilité de J-DriftX. Il définit les éléments nécessaires pour prendre cette décision sur des preuves explicites.

## 1. Première question : pourquoi ce modèle devrait-il être utile ?

Avant d'étendre l'implémentation ou de démontrer toutes les propriétés théoriques, il faut établir si l'approche répond à un besoin réel mieux que les solutions déjà disponibles.

La question prioritaire n'est donc pas seulement « le modèle fonctionne-t-il ? », mais :

> **Pour quel utilisateur, quelle décision ou quel problème scientifique J-DriftX apporte-t-il une valeur mesurable que les méthodes existantes ne fournissent pas suffisamment bien ?**

Une méthode peut être mathématiquement cohérente et correctement implémentée sans présenter d'avantage pratique. Inversement, un avantage local peut être utile même si la méthode ne remplace pas les modèles généraux existants.

L'utilité doit être étudiée à trois niveaux distincts :

1. **Utilité scientifique :** l'approche formalise-t-elle un phénomène, une propriété ou une famille de problèmes d'une manière nouvelle, explicative ou vérifiable ?
2. **Utilité méthodologique :** obtient-elle, sur un problème précisément défini, une meilleure combinaison de précision, de coût de calcul, de stabilité, d'interprétabilité ou de données requises ?
3. **Utilité applicative :** améliore-t-elle effectivement une décision ou une analyse de dispersion, dans un domaine de validité explicite, par rapport aux outils accessibles aux utilisateurs visés ?

Ces niveaux ne sont pas interchangeables. Une contribution théorique n'implique pas automatiquement un avantage opérationnel ; un gain de vitesse ne démontre pas une meilleure prédiction.

## 2. Définir un besoin concret avant de choisir la méthode

Le premier travail consiste à écrire une fiche de problème indépendante de la solution J-DriftX.

Elle doit répondre aux questions suivantes :

- **Phénomène et cible :** quelle quantité cherche-t-on à prédire ou à reconstruire (concentration, dépôt, exposition, trajectoire, source) ?
- **Contexte physique :** dispersion atmosphérique, dérive de pulvérisation en champ lointain (*far-field*), relief, végétation, vent non uniforme ou autre contexte précisément délimité ?
- **Utilisateur et décision :** qui utilisera le résultat, et quelle décision ce résultat peut-il modifier ?
- **Limites des pratiques actuelles :** où les modèles ou données de référence sont-ils insuffisants ? L'insuffisance est-elle documentée par des sources et des observations, ou seulement supposée ?
- **Contraintes :** précision nécessaire, latence, ressources, données disponibles, interprétabilité, incertitude et exigences réglementaires éventuelles.
- **Conditions de succès :** quel changement mesurable justifierait l'emploi de J-DriftX ?
- **Conditions d'échec :** quel résultat conduirait à conclure que l'approche n'est pas utile pour ce cas ?

Ne pas présumer que le *far-field* de dérive de pulvérisation est le meilleur cas d'usage simplement parce qu'il est historiquement lié à Drift-X. Il constitue un candidat à comparer aux autres besoins plausibles, à l'aide de critères explicites.

## 3. Hypothèses à distinguer

Les propositions suivantes sont des hypothèses à instruire, et non des résultats établis.

| Hypothèse | Valeur potentielle | Preuve requise |
|---|---|---|
| H1. Les solutions de similitude généralisées représentent adéquatement certains régimes de dispersion | Modèle compact et interprétable | Analyse des hypothèses, cas analytiques et comparaison aux solutions de référence |
| H2. La métrique de temps de transport représente utilement certaines asymétries du transport | Meilleure représentation dans des écoulements ciblés | Définition mathématique, propriétés, cas limites et ablation de la métrique |
| H3. L'évaluation sans maillage réduit le coût pour une précision acceptable | Calcul ponctuel moins coûteux | Mesure du temps et de la mémoire, à précision et problème comparables |
| H4. Une calibration à partir de données partielles est identifiable et robuste | Besoin réduit en observations ou adaptation facilitée | Étude d'identifiabilité, bruit, données manquantes et validation indépendante |
| H5. L'approche apporte un avantage pour la dérive en champ lointain | Meilleure estimation dans un domaine applicatif important | Données ou cas physiques pertinents, baselines adaptées et analyse d'incertitude |
| H6. Le modèle généralise mieux que certaines approximations apprises hors domaine | Moins de dégradation en extrapolation | Comparaison sur des scénarios hors domaine définis avant l'évaluation |

Une hypothèse peut être partiellement confirmée, limitée à un sous-domaine ou réfutée. Les résultats doivent rester attribuables au composant effectivement testé.

## 4. Protocole pour démontrer — ou réfuter — l'utilité

### Étape A — Établir l'état de référence

1. Décrire le problème et les scénarios cibles sans faire référence à la solution proposée.
2. Identifier les méthodes actuellement utilisées et les baselines les plus pertinentes, à partir de la revue de littérature et des pratiques applicatives documentées.
3. Définir le niveau de preuve de chaque source et vérifier la comparabilité des problèmes.
4. Établir les métriques et seuils de succès avant de consulter les résultats du benchmark.
5. Documenter les données indisponibles, les incertitudes et les biais possibles.

### Étape B — Choisir le test le plus discriminant et le moins coûteux

Commencer par un cas réduit, mais scientifiquement pertinent, qui permet de distinguer les hypothèses concurrentes.

Ordre recommandé :

1. **Cas analytique connu :** vérifier la cohérence mathématique et l'implémentation.
2. **Cas contrôlé synthétique :** faire varier un facteur à la fois et inclure des cas limites.
3. **Ablation :** comparer le modèle complet à des variantes sans métrique non symétrique, sans généralisation de similitude ou sans calibration, lorsque ces variantes sont définies mathématiquement.
4. **Benchmark contre des baselines :** comparer sur les mêmes scénarios, données, conditions d'entrée et budgets de calcul.
5. **Validation indépendante :** tester sur des observations ou simulations qui n'ont pas servi à choisir la méthode ni à calibrer ses paramètres.

Le cas analytique vérifie des propriétés, mais ne suffit pas à établir l'utilité physique. Les tests synthétiques révèlent les mécanismes, mais ne remplacent pas une validation indépendante.

### Étape C — Mesurer plusieurs dimensions de valeur

Ne pas réduire l'utilité à une seule métrique.

| Dimension | Mesures possibles | Précaution |
|---|---|---|
| Précision | MAE, RMSE, erreur relative, biais, quantiles d'erreur | Adapter la métrique à la grandeur physique et à sa distribution |
| Validité physique | Bilan de masse, positivité, symétries attendues, cohérence dimensionnelle | Ne tester que les propriétés garanties par les hypothèses |
| Coût | Temps d'exécution, mémoire, coût de préparation/calibration | Comparer à environnement et budget comparables |
| Robustesse | Sensibilité aux paramètres, au bruit et aux données manquantes | Définir les perturbations à l'avance |
| Généralisation | Erreur sur des régimes non vus, changement de météo ou de topographie | Délimiter précisément le domaine hors distribution |
| Calibration et incertitude | Couverture, largeur des intervalles, stabilité et identifiabilité | Distinguer incertitude paramétrique et erreur de modèle |
| Utilité décisionnelle | Impact sur une décision ou sur une contrainte métier | Définir la décision et le coût des erreurs avec les utilisateurs |

Les métriques doivent être sélectionnées selon le problème. Il ne faut pas utiliser toutes les métriques par défaut ni agréger des dimensions incompatibles dans un score arbitraire.

### Étape D — Rendre la comparaison équitable

Pour chaque baseline :

- employer les mêmes données, scénarios et informations disponibles ;
- séparer les données de calibration des données de validation ;
- comparer des modèles configurés raisonnablement, sans désavantager artificiellement les concurrents ;
- inclure le coût complet nécessaire pour atteindre la précision rapportée ;
- rapporter la variabilité et l'incertitude, pas seulement le meilleur résultat ;
- publier les échecs, les cas où la baseline gagne et les différences inexpliquées ;
- conserver les scripts, paramètres, versions et identifiants de données nécessaires à la reproduction.

Une comparaison entre méthodes évaluées sur des jeux de données ou des conditions physiques différents ne permet pas de conclure à une supériorité.

## 5. Critères de décision à fixer avant l'expérience

Pour chaque hypothèse, renseigner avant le benchmark :

- le résultat primaire et sa métrique ;
- la baseline principale ;
- le seuil d'amélioration jugé utile, justifié par le besoin applicatif ;
- les critères de non-infériorité lorsque le gain attendu porte surtout sur le coût ;
- les analyses de sensibilité et sous-groupes prévus ;
- les conditions d'abandon, de restriction ou de révision de l'hypothèse.

Il n'existe pas de seuil universel d'amélioration. Il doit être motivé par les exigences du problème et le niveau d'incertitude. Si le seuil ne peut pas être justifié, cette lacune doit être résolue avant de prétendre démontrer une utilité pratique.

## 6. Jalons avec portes de décision

### G0 — Besoin et valeur potentielle

**Question :** le problème est-il réel, suffisamment important et mal couvert par les méthodes disponibles ?

Livrables :
- fiche de problème indépendante de la solution ;
- utilisateurs, décisions et contraintes identifiés ;
- synthèse des alternatives existantes ;
- hypothèse d'utilité et critères de succès préenregistrés dans le dépôt.

**Décision :** poursuivre si un besoin étayé et un avantage testable sont identifiés ; sinon, revoir le cas d'usage avant d'investir dans le développement.

### G1 — Cohérence et faisabilité théoriques

**Question :** la formulation peut-elle représenter le problème cible sous des hypothèses explicites ?

Livrables :
- définition des variables, unités, hypothèses et conditions aux limites ;
- propriétés démontrées, conjectures et limites séparées ;
- cas analytique minimal reproductible.

**Décision :** poursuivre, restreindre le domaine ou corriger la formulation selon les résultats.

### G2 — Valeur différentielle en environnement contrôlé

**Question :** quel composant apporte quel bénéfice par rapport aux baselines ?

Livrables :
- benchmark reproductible ;
- comparaisons équitables et ablations ;
- erreurs, coût, robustesse et résultats négatifs documentés.

**Décision :** continuer uniquement les composants qui démontrent une contribution pertinente, ou réviser les hypothèses si les résultats sont ambigus.

### G3 — Validité sur données indépendantes

**Question :** le bénéfice résiste-t-il à des données et conditions non utilisées pendant le développement ?

Livrables :
- provenance et licence des données ;
- protocole de validation indépendant ;
- analyse d'incertitude, d'échecs et de domaine de validité.

**Décision :** revendiquer seulement le niveau de validité effectivement démontré ; ne pas extrapoler à la conformité réglementaire sans évaluation dédiée.

### G4 — Pertinence applicative et diffusion

**Question :** le bénéfice mesuré change-t-il réellement une décision ou ouvre-t-il une capacité scientifique utile ?

Livrables :
- évaluation avec le contexte d'usage visé ;
- limites, coûts de déploiement et conditions de maintenance ;
- article ou rapport reproductible, si les résultats le justifient.

**Décision :** publier, poursuivre sur un sous-domaine, transférer ou arrêter la piste.

## 7. Place de la feuille de route technique

Les modules logiciels ne sont pas des fins en soi. Leur priorité dépend de leur contribution à une hypothèse et à une expérience :

- **Noyau de similitude et métrique :** uniquement ce qui est nécessaire pour tester la formulation centrale.
- **Contraintes physiques :** propriétés explicitement justifiées par le modèle, avec tests dans leur domaine de validité.
- **Benchmarks et baselines :** prioritaires dès le départ ; ils font partie de la preuve, pas d'une étape de finition.
- **Calibration et problème inverse :** après définition d'un cas direct crédible et étude de l'identifiabilité.
- **POD, surrogates ou apprentissage :** concurrents ou composants à tester selon la question, sans présumer qu'ils sont meilleurs ou moins bons.
- **SIG, plugin QGIS, API et ergonomie :** après démonstration d'un noyau utile pour éviter de transformer une hypothèse non validée en produit.
- **Publication :** fondée sur les résultats, y compris si ceux-ci sont négatifs ou restreignent fortement l'ambition initiale.

## 8. Risques d'inférence à éviter

- **Confondre nouveauté et utilité :** une méthode peut être originale sans résoudre un problème important.
- **Confondre cohérence et précision :** satisfaire une propriété mathématique ne garantit pas des prédictions exactes.
- **Confondre vitesse et avantage global :** mesurer la précision au même budget et le coût total.
- **Choisir le benchmark après coup :** fixer les critères avant d'examiner les résultats pour limiter le biais de sélection.
- **Surinterpréter un cas favorable :** rapporter aussi les régimes où la méthode échoue.
- **Traiter l'absence de référence trouvée comme preuve de nouveauté :** borner toute conclusion par la couverture réelle de la revue.
- **Construire une application avant de prouver sa valeur :** retarder les fonctionnalités périphériques tant que le besoin et le bénéfice ne sont pas établis.
- **Promettre une conformité réglementaire :** celle-ci exige une évaluation spécifique, indépendante et adaptée au cadre d'usage.

## 9. Prochaine action concrète

La prochaine tâche scientifique est de rédiger une **fiche de décision G0** pour le cas d'usage candidat « dérive de pulvérisation en champ lointain », puis de la confronter à au moins une autre formulation possible du besoin si la revue suggère des alternatives crédibles.

Cette fiche devra contenir :

1. le problème physique et la décision visée ;
2. les utilisateurs et contraintes ;
3. les limites documentées des solutions existantes ;
4. la valeur ajoutée supposée de J-DriftX ;
5. les baselines à comparer et la justification de leur choix ;
6. les données accessibles et les lacunes ;
7. les critères de succès et d'abandon ;
8. le test discriminant le moins coûteux ;
9. les sources et le niveau de preuve de chaque affirmation.

**Règle de gouvernance :** aucune nouvelle fonctionnalité importante ne doit être priorisée uniquement parce qu'elle figure dans l'architecture cible. Elle doit être reliée à un besoin, une hypothèse, une expérience et une décision qu'elle permettra de prendre.

## Documents liés

- [Audit de l'héritage Drift-X](01-audit-heritage-driftx.md)
- [Revue de l'état de l'art 2026](02-revue-etat-art-2026.md)
- [Feuille de route J-DriftX v2](03-roadmap-jdriftx-v2.md)
- [Plan d'intégration scientifique et de validation](05-plan-validation-et-integration.md)
- [Choix de la méthode de revue systématique](06-choix-methode-revue-systematique.md)


## 7. Deux voies distinctes pour éviter un blocage artificiel

Le projet distingue maintenant :

- **G0-S — valeur scientifique exploratoire :** autorise un modèle jouet mathématique précisément défini, avec preuves, contre-exemples et tests. Il peut avancer sans jeu de données réel, car il ne prétend pas valider une prédiction physique.
- **G0-A — utilité applicative :** reste obligatoire avant toute revendication de valeur applicative, benchmark réel, sélection de domaine industriel ou développement d'une chaîne opérationnelle.

Cette séparation n'est pas une façon de déclarer G0 franchi. Elle permet seulement de produire un résultat scientifique de portée limitée sans prétendre avoir résolu le besoin utilisateur. Le [MVP scientifique minimal et la trajectoire maximale](13-mvp-scientifique-et-g0.md) définissent le périmètre autorisé et les portes d'extension.

Le MVP ne peut conclure qu'à des propriétés mathématiques ou à une valeur pédagogique. Toute conclusion sur concentration, dépôt, exposition, coût applicatif ou utilité décisionnelle requiert une formulation physique et une validation distinctes.
