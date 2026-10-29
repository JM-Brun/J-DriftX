# 42 — Stratégie de reprise et d'élargissement scientifique de J-DriftX

**Statut :** principe directeur du projet, à appliquer aux décisions scientifiques, à la documentation, au code et aux benchmarks. Cette note ne constitue pas une validation du modèle.

## 1. Intention générale

J-DriftX reprend Drift-X comme **point de départ scientifique**, pas comme spécification intouchable. Le projet doit d'abord reconstruire une base fonctionnelle et conceptuelle à peu près équivalente à ce que l'approche historique cherchait à couvrir, avec des hypothèses et résultats désormais explicités et testables. Il pourra ensuite corriger les erreurs identifiées, remplacer des formulations insuffisantes, intégrer des méthodes plus récentes et élargir les cas d'usage si les preuves et les besoins le justifient.

L'objectif n'est ni de réécrire l'histoire pour rendre les publications cohérentes, ni de préserver une erreur par fidélité à une source. Une source historique documente une idée, une affirmation ou une expérience ; elle ne transforme pas cette affirmation en vérité établie.

## 2. Trois couches à garder distinctes

1. **Héritage documentaire.** Ce que les sources originales disent, avec citation, version, page, équation, contexte et niveau d'accès. Les erreurs, contradictions, ambiguïtés et limites doivent être conservées comme faits historiques et consignées dans un registre d'audit.
2. **Reconstruction de référence.** Une formulation autonome, dimensionnellement cohérente, mathématiquement définie et testable, qui vise à reproduire le périmètre et les objectifs principaux de l'approche historique. Toute divergence avec la source doit être explicitée ; aucune correction silencieuse.
3. **Extension de recherche.** Nouvelles formulations, algorithmes, données, domaines physiques ou cas d'usage. Ils sont évalués comme contributions nouvelles, comparées à la reconstruction de référence et à des baselines pertinentes.

Ne pas mélanger transcription, interprétation et proposition moderne dans une même équation ou un même résultat. Les étiquettes « source », « reconstruction », « correction proposée » et « extension » doivent être visibles là où elles sont utiles.

## 3. Première étape : établir une base comparable à l'original

Avant de chercher une généralisation ambitieuse, reconstituer une version minimale qui couvre, autant que les sources le permettent :

- les solutions de similitude / profils de panache utilisés par le projet historique ;
- la représentation non symétrique fondée sur le transport dirigé et les temps de transport ;
- la construction multi-niveaux, lorsque ses définitions et conditions d'entrée peuvent être récupérées ;
- l'évaluation ponctuelle ou réduite du champ, avec coût de préparation et coût d'évaluation mesurés séparément ;
- l'assimilation de données partielles et l'identification de paramètres ou de source, d'abord comme fonctionnalités candidates et non comme performances acquises ;
- le contexte applicatif historique de dispersion atmosphérique et de dérive de pulvérisation, avec une intégration SIG seulement si elle sert une démonstration reproductible.

Cette base n'a pas besoin de reproduire les erreurs, les hypothèses cachées, les limitations du logiciel d'origine ou ses choix d'implémentation. Elle doit préserver les **questions scientifiques et la portée fonctionnelle visées**, tout en indiquant ce qui est reconstruit, approximé, remplacé ou encore impossible à reproduire faute de sources.

## 4. Registre obligatoire des erreurs et écarts

Chaque erreur ou anomalie identifiée doit être inscrite dans une issue ou un registre versionné et contenir, au minimum :

- identifiant stable et source/version/page/équation ou fichier de code ;
- transcription exacte ou reproduction minimale du comportement observé ;
- type : erreur arithmétique, incohérence dimensionnelle, hypothèse manquante, contradiction entre sources, ambiguïté de notation, défaut algorithmique, défaut logiciel, donnée erronée ou affirmation non étayée ;
- conséquence démontrée et périmètre d'impact ; séparer impact prouvé et risque supposé ;
- correction proposée, alternatives possibles et justification ;
- test analytique, test de propriété, contre-exemple ou référence indépendante qui permet de vérifier la correction ;
- statut : observé, confirmé, correction proposée, corrigé dans le code/document, validé indépendamment, ou non résolu.

Ne jamais « réparer » une source primaire. La transcription doit rester fidèle ; la correction appartient à la reconstruction ou à l'implémentation et doit être traçable. Lorsqu'il subsiste plusieurs interprétations, documenter les hypothèses et comparer les variantes au lieu de choisir arbitrairement.

## 5. Domaine historique et élargissement des applications

Le cas historique — dispersion atmosphérique de pesticides et dérive de pulvérisation, notamment en viticulture — est un **cas de référence et un point de comparaison**, pas une limite permanente du projet.

Les domaines possibles à instruire incluent notamment :

- pollution industrielle et rejets accidentels ;
- pollution urbaine et qualité de l'air ;
- dispersion de substances chimiques et de contaminants ;
- scénarios radiologiques ou nucléaires, uniquement après examen des phénomènes et exigences propres à ces cas ;
- autres scalaires passifs ou transportés, si leurs mécanismes sont effectivement compatibles avec les hypothèses du modèle.

Ces domaines ne sont pas interchangeables. Gaz réactifs, aérosols, dépôts, décroissance radioactive, flottabilité thermique, particules, chimie atmosphérique, turbulence et interactions avec les surfaces peuvent nécessiter des termes ou modèles supplémentaires. « Généraliser » ne signifie donc pas appliquer le même modèle sans modification à toutes les substances.

Chaque nouveau domaine doit passer par une fiche de problème indépendante de la méthode : phénomène, scalaire cible, échelles spatiales et temporelles, mécanismes dominants, sources/puits, données, décision ou usage, baselines existantes, contraintes de sécurité/réglementation et critères d'échec. Choisir ensuite les cas par valeur scientifique, données accessibles, faisabilité de validation et potentiel différentiel — pas uniquement par proximité avec le projet historique.

## 6. Intégrer les méthodes nouvelles sans perdre le fil

Les méthodes contemporaines (modèles de dispersion physiques, solveurs EDP, ROM, méthodes d'ordre réduit, modèles statistiques, apprentissage automatique, opérateurs neuronaux, assimilation, méthodes hybrides) doivent être étudiées comme options ou références, pas ajoutées par effet de mode.

Pour chaque extension, préciser :
- le défaut ou besoin qu'elle adresse ;
- ce qu'elle conserve et ce qu'elle abandonne de l'approche historique ;
- les hypothèses supplémentaires et le coût de données/calcul ;
- la baseline pertinente et l'expérience d'ablation ;
- le critère quantitatif qui permet de conclure à un gain, une équivalence ou une régression.

Le projet peut conclure qu'une idée historique doit être abandonnée, restreinte ou remplacée. Un résultat négatif correctement établi est un résultat utile.

## 7. Séquence de travail

1. **Inventorier et authentifier** les sources, les versions, les données, le code et les droits de réutilisation.
2. **Extraire fidèlement** les objets, équations, algorithmes, exemples et revendications historiques, avec pages et unités.
3. **Auditer** cohérence dimensionnelle, hypothèses, existence/unicité, invariants, cas limites et contre-exemples.
4. **Définir une reconstruction minimale** et des tests analytiques indépendants, sans masquer les divergences avec les sources.
5. **Reproduire le périmètre de référence** sur des cas simples, en mesurant coût total, erreur et limites.
6. **Comparer aux baselines actuelles** sur un problème précis et un protocole équitable.
7. **Élargir progressivement** à des champs variables, sources multiples, relief, mécanismes supplémentaires et domaines applicatifs distincts, seulement lorsque les étapes précédentes le justifient.

Chaque étape peut révéler qu'une hypothèse doit être reformulée ou qu'un sous-objectif ne vaut pas la peine d'être poursuivi. La séquence guide les décisions ; elle n'oblige pas à conserver une hypothèse réfutée.

## 8. Critère de réussite

J-DriftX doit devenir une base de recherche reproductible qui permet de distinguer clairement : ce que les auteurs historiques ont proposé, ce que le projet a pu reproduire, ce qu'il a corrigé, ce qu'il a réfuté et ce qu'il apporte de nouveau. Le succès ne se mesure pas au nombre de pages ou de fonctionnalités, mais à la solidité des définitions, à la traçabilité des preuves, à la qualité des comparaisons et à la clarté des domaines de validité.
