# Gouvernance documentaire et frontières des sources

> **Rôle :** définir les responsabilités documentaires, les sources canoniques et les règles de maintenance. Ce document ne porte ni résultat scientifique, ni statut opérationnel courant, ni backlog.

## Frontière public / privé

- **Dépôt public `JM-Brun/J-DriftX`** : définitions mathématiques, hypothèses, dérivations, transcriptions de sources primaires utiles à la vérification, code/tests, résultats reproductibles, limites et références destinés à un lecteur externe.
- **Dépôt privé `JM-Brun/career-knowledge/projects/jdriftx`** : coordination interne, arbitrages en cours, notes exploratoires non stabilisées, analyse de faisabilité, suivi de travail et matériaux dont les droits ou la pertinence publique restent à clarifier.
- Un résultat exploratoire privé nécessaire à une conclusion publique doit être vérifié, reformulé avec ses hypothèses et limites, puis intégré au document public propriétaire. Une note privée ne constitue pas par elle-même une preuve publique.
- Les sources primaires et les fichiers nécessaires à la reproductibilité ne sont pas supprimés au motif qu'une synthèse existe.

## Sources canoniques par type d'information

| Information | Source canonique | Règle pour les autres documents |
|---|---|---|
| État courant et prochaine action | Issue propriétaire ; coordination globale privée dans [career-knowledge #125](https://github.com/JM-Brun/career-knowledge/issues/125) | Ne pas recopier le statut courant dans les notes ou roadmaps. |
| Vision et critères de décision à long terme | [Roadmap stratégique privée](https://github.com/JM-Brun/career-knowledge/blob/main/projects/jdriftx/notes/roadmap.md) | Ne pas y tenir une checklist opérationnelle. |
| Ordre des portes et dépendances | [Roadmap opérationnelle privée](https://github.com/JM-Brun/career-knowledge/blob/main/projects/jdriftx/notes/roadmap-operationnelle-et-faisabilite.md) | Pointer vers les issues propriétaires pour les actions détaillées. |
| Définition / preuve / code / tests MVP-S | [Matrice publique docs/27](27-matrice-tracabilite-mvp-s.md) | Les notes privées ne sont que des pointeurs, sauf matériau exploratoire explicitement signalé. |
| Conservation dans les coordonnées travel-time | [Dérivation publique docs/32](32-conservation-coordonnees-travel-time.md), issue [#123](https://github.com/JM-Brun/J-DriftX/issues/123) pour la question et les travaux restants | Séparer dérivation conditionnelle, reconstruction historique, contre-exemples et statut de résolution. |
| Revendications historiques et baseline | [Matrice docs/49](49-matrice-revendications-baseline.md) et issue [#232](https://github.com/JM-Brun/J-DriftX/issues/232) | Les fiches de sources restent les preuves de provenance ; ne pas recopier la matrice dans le registre d'anomalies. |
| Anomalies documentaires et résolution | [Registre docs/46](46-registre-erreurs-incoherences-documentaires.md) et issue [#233](https://github.com/JM-Brun/J-DriftX/issues/233) | Chaque anomalie renvoie à l'emplacement affecté, à sa preuve et à son identifiant stable si disponible. |
| Admissibilité des corpus et droits tiers | Issues privées [#24](https://github.com/JM-Brun/career-knowledge/issues/24) et [#144](https://github.com/JM-Brun/career-knowledge/issues/144), plus issues techniques publiques par corpus | Distinguer admissibilité scientifique, reproductibilité technique et droits de redistribution. |
| Rôle et disposition des notes privées | [Registre de triage privé](https://github.com/JM-Brun/career-knowledge/blob/main/projects/jdriftx/notes/triage-detaille-et-consolidation-2026-10-28.md) | Ce registre ne doit pas recopier les résultats ni le backlog. |

## Contrat minimal de chaque document actif

Tout document actif doit rendre explicites, dans son en-tête ou ses premières lignes :

1. **Rôle** : la question précise à laquelle il répond.
2. **Statut épistémique** : source primaire, transcription, dérivation démontrée sous hypothèses, résultat numérique fini, hypothèse, exploration, décision ou archive historique.
3. **Périmètre et limites** : ce que le document n'établit pas.
4. **Source canonique / propriétaire** : document ou issue qui fait autorité pour le type d'information.
5. **Liens amont/aval** : sources utilisées et issues ou livrables qui consomment ce contenu.

Un document historique peut être conservé sans être actif, à condition d'être daté et explicitement interdit comme source de statut courant. Un document exploratoire ne doit pas employer « démontré », « validé » ou « supérieur » sans preuve correspondant à cette portée.

## Règles anti-redondance

- Une même information mutable (statut, prochaine action, verdict courant) n'a qu'une source canonique.
- Les résumés peuvent rester s'ils servent un public distinct, mais doivent être plus courts que la source et pointer vers elle.
- Des documents aux rôles distincts peuvent partager un thème : une source primaire, sa fiche de lecture, une dérivation, un test et un registre d'anomalies ne sont pas des doublons par défaut.
- Lorsqu'un passage est copié, vérifier ses références entrantes, transférer tout élément unique, puis remplacer la copie par un lien. Ne jamais supprimer sur la seule base d'un titre proche.
- Les instantanés datés et notes de séance sont historiques, pas des backlogs. L'historique Git est la première archive ; ne pas créer de copies d'archives concurrentes sans besoin démontré.

## Numérotation et références

- Les six collisions historiques de numérotation (14, 15, 16, 17, 21, 33) restent documentées dans [l'index docs/00](00-index.md). Ne pas renuméroter en masse sans inventaire des liens entrants, ancres, références de code et pages du site.
- Dans les liens, utiliser le **nom de fichier complet** plutôt qu'un numéro seul.
- Chaque changement de nom ou suppression exige une recherche des références internes, du site, des tests, des issues et des PR.
- Les chemins locaux, ancres et URL externes sont des catégories de validation distinctes ; la réussite d'un contrôle de chemins ne prouve pas la validité des autres.

## Limites

Cette politique améliore la navigation et la maintenabilité ; elle ne prouve ni la validité mathématique, ni la validité physique, ni l'admissibilité d'un corpus, ni la nouveauté du projet. Ces décisions restent dans leurs documents et issues propriétaires.
