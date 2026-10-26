# Bibliographie annotée — liens entre la littérature et J-DriftX

> **Document de travail éditable.** Cette cartographie relie les références identifiées dans le dépôt aux hypothèses et décisions de J-DriftX. Elle ne remplace ni la lecture des textes intégraux ni le protocole de revue systématique. Les relations sont des hypothèses de pertinence, pas des conclusions de supériorité ou de nouveauté.

## Comment lire les relations

- **Fondatrice / directement liée** : source historique de Drift-X/J-DriftX ou description directe de son approche.
- **Concurrente / baseline** : méthode qui peut répondre à une partie du même besoin et doit être comparée sur un problème commun.
- **Complémentaire** : méthode pouvant compléter J-DriftX, par exemple pour l'assimilation, l'identification de source ou la calibration.
- **Analogie conceptuelle / autre domaine** : idée mathématique proche ou application transférable, sans équivalence démontrée.
- **Contexte applicatif / opérationnel** : décrit les besoins, les pratiques ou les exigences d'usage, sans être nécessairement une méthode concurrente.
- **Contexte logiciel / SIG** : référence utile pour l'intégration et l'interopérabilité, pas une preuve de différenciation scientifique.

## Documents de synthèse de la revue

- [Résumé exécutif — partie 1](../raw/reviews/2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf)
- [Résumé exécutif — partie 2](../raw/reviews/2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf)

Les fichiers PDF sont conservés comme documents de synthèse. Les fiches ci-dessous sont les sources Markdown éditables pour la classification et les notes de lecture.

## Cartographie par famille

| Famille | Fiche éditable | Rapport à J-DriftX |
|---|---|---|
| Héritage Drift-X et fondements de la métrique | [Fondements et corpus historique](bibliographie/fondements-et-heritage.md) | Sources directes, antériorité, formalisation et limites |
| Dérive de pulvérisation et modèles réglementaires | [Spray drift et modèles opérationnels](bibliographie/spray-drift-et-modeles-operationnels.md) | Concurrents applicatifs, baselines, besoins de validation |
| ROM, surrogates et apprentissage | [ROM et apprentissage](bibliographie/rom-et-apprentissage.md) | Baselines concurrentes ou approches complémentaires |
| Identification de source et assimilation | [Source-term estimation et assimilation](bibliographie/identification-source-assimilation.md) | Méthodes complémentaires et alternatives pour le problème inverse |
| SIG, exposition et applications | [SIG, exposition et applications](bibliographie/sig-exposition-applications.md) | Contexte d'usage, validations terrain et intégration logicielle |
| Métriques et analogies transverses | [Métriques et analogies](bibliographie/metriques-et-analogies.md) | Intuition mathématique transférable, sans équivalence présumée |

## Champs à compléter pour chaque source

1. Référence bibliographique vérifiée et DOI/URL pérenne.
2. Statut d'accès : texte intégral relu, extrait relu, résumé/notice seulement, ou référence secondaire.
3. Problème traité, hypothèses, domaine de validité et variables observées.
4. Relation précise avec J-DriftX et ce qui est **similaire / différent**.
5. Limites, résultats négatifs et incertitudes.
6. Conséquence testable : théorie, baseline, jeu de données, test, benchmark, ou décision de ne pas intégrer.
7. Emplacement dans le rapport de revue (page/section) et statut de décision dans les notes internes de suivi (dépôt privé).

## Garde-fous

- Une méthode n'est concurrente que si le problème, les observables, le régime physique et le protocole de comparaison sont suffisamment proches.
- Une méthode fondée sur CFD/LES puis réduite a posteriori n'est pas directement équivalente à une réduction analytique a priori ; elle demeure une baseline utile si les cas comparés sont adaptés.
- Une application à un autre domaine peut inspirer une formalisation, mais ne valide pas automatiquement sa pertinence pour la dispersion atmosphérique.
- Une référence trouvée dans un résumé ou une bibliographie n'est pas considérée comme lue intégralement.
- Les affirmations « inédit », « supérieur », « coût quasi nul », « extrapolation par construction » et les facteurs d'accélération doivent être reliés à des preuves et à des benchmarks vérifiables avant publication.
