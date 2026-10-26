# Protocole public de validation scientifique — J-DriftX

> **Statut :** protocole de validation, pas validation acquise. La cohérence mathématique, la fidélité physique, la performance prédictive et l'utilité applicative sont des niveaux de preuve distincts. Aucun avantage applicatif n'est établi par le présent document.

## 1. Principes

1. Formuler chaque affirmation avec son domaine de validité, ses hypothèses, ses unités et son niveau de preuve.
2. Distinguer les résultats analytiques, les expériences numériques synthétiques, les validations sur données physiques et les conclusions d'utilité décisionnelle.
3. Comparer les méthodes sur le même problème, les mêmes observations, le même découpage des données et un budget de calcul explicite.
4. Conserver les résultats négatifs, les incertitudes et les contre-exemples. Une propriété qui n'est pas démontrée doit être présentée comme hypothèse ou objectif, non comme garantie.
5. Ne pas employer le terme « revue systématique reproductible » tant que les bases, dates, requêtes, critères de sélection, dédoublonnage et décomptes ne sont pas documentés.

## 2. Étape A — définitions et cas analytiques

Pour chaque objet mathématique du modèle direct et de la métrique de temps de transport :

- définir les entrées, sorties, unités, hypothèses, conditions aux limites et domaine de validité ;
- tester les cas limites, les invariants et les contre-exemples attendus ;
- comparer les calculs du code à des solutions analytiques indépendantes ;
- expliciter quelles propriétés découlent de la définition, lesquelles exigent des hypothèses supplémentaires et lesquelles ne sont pas encore établies.

Le MVP-S 1D sert de premier cas de référence contrôlable. Sa réussite ne démontre ni la validité d'un champ de vent 2D variable, ni la conservation de masse d'un modèle de dispersion complet, ni la nouveauté scientifique.

Références de travail public : [revue mathématique ciblée](14-revue-mathematique-ciblee.md), [bilan du MVP-S 1D](21-bilan-mvp-s-1d.md), [modèle jouet et limites](09-fallback-modele-jouet.md).

## 3. Étape B — vérification numérique et implémentation

- Relier chaque propriété annoncée à une preuve mathématique, un test automatisé ou une expérience de vérification identifiée.
- Couvrir les unités, les cas limites, les comportements dégénérés, la stabilité numérique et la convergence lorsque ces notions s'appliquent.
- Distinguer les tests unitaires du code des validations indépendantes du modèle.
- Documenter versions, paramètres, graines aléatoires, scripts de génération, métriques et tolérances.
- Ne pas inférer une propriété globale à partir de quelques tests ponctuels.

Le code et les tests du dépôt constituent des éléments vérifiables, mais ne prouvent pas à eux seuls la fidélité empirique ni l'utilité applicative.

## 4. Étape C — données et benchmark indépendant

Avant tout benchmark sur données observées, vérifier et documenter :

- la source canonique, la licence et les conditions de réutilisation ;
- la structure des observations, les unités, les limites de détection, les valeurs manquantes et les métadonnées ;
- la correspondance entre chaque observation et son contexte physique ;
- l'indépendance entre données de calibration, choix de modèle/hyperparamètres et évaluation finale ;
- les risques de fuite d'information, de doublons et de dépendance entre observations d'une même campagne.

Définir les baselines, les métriques, les critères d'acceptation et l'analyse d'incertitude avant d'interpréter les résultats. L'absence de fichiers bruts vérifiés ou de partition indépendante bloque toute conclusion de performance.

Références : [protocole d'audit du corpus](14-protocole-audit-corpus-g0.md), [audit technique des jeux de données](20-audit-technique-jeux-donnees.md), [catalogue des données](12-catalogue-donnees-transport-dispersion.md).

## 5. Étape D — utilité et limites applicatives

Une méthode peut être mathématiquement cohérente et correctement implémentée sans être utile en pratique. L'utilité doit être évaluée pour un problème et une décision explicitement définis, face à des solutions de référence pertinentes, avec une précision et un coût comparables.

Ne pas présenter la dérive de pulvérisation en champ lointain comme un cas d'usage validé avant d'avoir vérifié les données, les conditions expérimentales, les baselines et les critères de succès. Une revue bibliographique ou un résultat synthétique ne constitue pas une validation physique.

Le cadre public de décision et de preuve est détaillé dans [Décider de l'utilité de J-DriftX](08-decision-utilite-et-preuve.md).

## 6. Critères de publication des résultats

Toute conclusion publique substantielle doit permettre au lecteur de retrouver :

- l'affirmation exacte et le niveau de preuve revendiqué ;
- les hypothèses et le domaine de validité ;
- les données, sources et licences, ou la procédure de génération synthétique ;
- le protocole, les baselines et les métriques ;
- les résultats positifs et négatifs, les incertitudes et les limites ;
- le code, les tests ou les références permettant une vérification indépendante.

Les jalons de planification, les arbitrages internes, les comptes rendus de séance et le suivi opérationnel sont conservés dans les notes privées associées. Ce document public ne remplace pas les résultats ni les preuves : il décrit les conditions minimales pour les produire et les présenter.
