# Cadrage G0-A : utilisateur, décision, observable, baseline et limites CAPRIV

> **Statut — note de cadrage, pas une décision.** Cette note documente les éléments du besoin applicatif exigés par [#43](https://github.com/JM-Brun/J-DriftX/issues/43) (utilisateur cible, décision, observable, baseline, limites du corpus CAPRIV). Elle ne déclare **pas** la porte G0-A franchie, ne démarre aucun benchmark, ne modifie aucun seuil préenregistré, et ne revendique aucune utilité démontrée. La décision explicite (lancer / poursuivre / reformuler / arrêter) appartient au propriétaire et reste bloquée par l'inspection fichier par fichier de DIFLU ([#204](https://github.com/JM-Brun/J-DriftX/issues/204), déléguée).

## 1. Utilisateur cible et décision à soutenir

Le besoin applicatif du corpus historique (lignée Sinfort : *C. R. Mécanique* 2006, *Applied Geomatics* 2009, JESA 2010 — viticulture, dérive de pulvérisation) désigne un utilisateur et une décision cohérents avec l'héritage :

- **Utilisateur cible :** le conseiller agricole ou l'agriculteur/viticulteur planifiant un traitement, secondairement le bureau d'études évaluant l'exposition des riverains.
- **Décision à soutenir :** (a) choisir une fenêtre de traitement météorologiquement compatible avec un objectif d'exposition des riverains (retraiter ou reporter) ; (b) dimensionner les moyens de réduction de dérive (distance non traitée, technologie de réduction, haie) pour un objectif d'exposition donné.
- **Grandeurs d'appui de la décision :** niveau estimé d'exposition des riverains au voisinage de la parcelle (proxy : concentration aérienne et dépôt aux distances réglementaires, typiquement 5 à 20 m en France selon le produit et la culture).

Ces éléments cadrent le cas d'usage **candidat**. Ils ne prouvent ni que J-DriftX sert mieux cette décision qu'un outil existant, ni que les données disponibles permettent l'évaluation : c'est précisément l'objet de la porte G0-A et des critères déjà préenregistrés dans #43.

## 2. Observable et régime physique : compatibilité avec les hypothèses

- **Observable :** concentration aérienne (conformément à #43).
- **Régime :** champ proche advectif dominant, distances de l'ordre de $10^2$ à $10^3$ m, fenêtre temporelle courte (l'ordre de grandeur des essais de référence est le lâcher de 10 min, cf. Prairie Grass dans [docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md)).
- **Compatibilités (documentées, pas démontrées prédictivement) :** linéarité du transport (H1), stationnarité sur la fenêtre (H3), homogénéité par morceaux parcelle/riverains (H5) — voir le catalogue des hypothèses du site et la carte des niveaux N0–N6.
- **Incompatibilités et garde-fous :** un rejet de pulvérisation n'est pas un scalaire passif idéal (distribution de tailles de gouttelettes, dépôt, éjection à vitesse propre). Le test discriminant DIFLU teste donc une **hypothèse de méthode sur un scalaire**, pas la dérive de pulvérisation elle-même ; J-DriftX ne se substitue pas aux modèles dédiés à la dérive (AGDISP, Silsoe, DAD-drift — cf. docs/20 et docs/21). Toute extrapolation du résultat DIFLU vers l'application viticole devra être justifiée séparément.

## 3. Baseline équitable

Conformément à #43, sans redéfinition : **panache gaussien simple** (solution de similitude du dépôt, tables de Briggs/Pasquill déjà implémentées et testées dans le package), **mêmes entrées** (terme source et météorologie du même essai DIFLU), **même observable** (concentration aérienne), métriques **FAC2 et NMSE évaluées par essai indépendant**, seuils de succès G2/G3 et critères d'arrêt **tels que préenregistrés dans #43**. La comparaison est à coût total documenté des deux côtés (préparation des entrées, calcul, post-traitement).

## 4. Examen du corpus CAPRIV

Le projet CAPRIV (« Concilier l'application des PPP et la protection des riverains », Ministère de l'Agriculture, essais 2021–2022, trois secteurs : grandes cultures, viticulture, arboriculture) a produit des jeux de données publics sur Recherche Data Gouv (DOI [10.57745/Z8OJ3A](https://doi.org/10.57745/Z8OJ3A)) avec des data papers par secteur (grandes cultures : [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11016980/) ; viticulture : [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11404078/) ; arboriculture : [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12603692/)).

**Apports pour G0-A :** CAPRIV documente le besoin applicatif réel (exposition des riverains, mannequins, efficacité des technologies de réduction de dérive et des haies) et fournit un cadre de référence pour l'observable « exposition au voisinage ».

**Limites déterminantes, telles qu'exigées par la checklist de cadrage :**

1. **Grandeur mesurée :** dérive sédimentaire (dépôt de traceur fluorescent sur collecteurs), dérive aérienne et dépôt sur mannequins, à des distances de quelques mètres à quelques dizaines de mètres du bord de parcelle. Le dépôt proche champ (environ 1–25 m) **ne valide pas à lui seul** le transport d'un scalaire passif à plusieurs centaines de mètres ou kilomètres.
2. **Conditions d'essai :** viticulture sur banc EoleDrift (végétation artificielle, vent artificiel), conformité aux standards d'essai documentée mais conditions normalisées, non représentatives de la météorologie libre à l'échelle du paysage.
3. **Objet physique :** gouttelettes de traceur avec spectre de tailles, pas un scalaire passif.

**Conclusion CAPRIV :** inutilisable comme corpus principal du test discriminant (qui reste DIFLU, #43) ; pertinent comme **contexte applicatif** (définition de l'exposition riverains, distances réglementaires) et comme **bornage indépendant** pour l'observable dépôt proche champ, à ne jamais mélanger avec l'évaluation scalaire. Aucune donnée CAPRIV n'est utilisée à ce stade.

## 5. État de la porte G0-A après cette note

| Élément de cadrage | Statut |
|---|---|
| Utilisateur cible et décision | **Documenté** (section 1, candidat lié à l'héritage) |
| Observable et régime, compatibilité hypothèses | **Documenté** (section 2, compatibilités documentées / garde-fous) |
| Baseline équitable, entrées et observable communs | **Documenté** (section 3, seuils inchangés de #43) |
| Métriques, seuils G2/G3, critères d'arrêt | **Préenregistrés dans #43** — non modifiés ici |
| Limites CAPRIV | **Examinées** (section 4) |
| Vérification manuelle des données candidates (disponibilité, provenance, licence, unités, métadonnées) | **Non fait** — bloqué par #204 (DIFLU, inspection fichier par fichier, déléguée) |
| Séparation par essai effectivement vérifiée sur fichiers | **Non fait** — même blocage |
| Décision explicite G0-A (lancer / poursuivre / reformuler / arrêter) | **Non prise** — au propriétaire, après #204 |

G0-A reste **bloquée**. Cette note ne crée aucune présomption d'utilité ni de supériorité prédictive ; un verdict négatif reste une issue acceptable conformément à #43.

## Références

- Porte G0-A et critères préenregistrés : [#43](https://github.com/JM-Brun/J-DriftX/issues/43).
- Cadrage privé miroir (checklist) : career-knowledge #23 (accès restreint).
- Audit des corpus : [docs/20](20-audit-technique-jeux-donnees.md) ; seconde vague et cas synthétiques : [docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md).
- CAPRIV : DOI [10.57745/Z8OJ3A](https://doi.org/10.57745/Z8OJ3A) et data papers par secteur (liens section 4).
