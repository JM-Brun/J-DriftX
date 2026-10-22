# Revue adversariale de J-DriftX — porte G0

> **Statut : audit de cadrage, pas validation du modèle.** Ce document cherche activement les raisons pour lesquelles le projet pourrait ne pas être utile, nouveau ou compétitif. Les points ci-dessous sont des objections à résoudre, non des conclusions définitives.

## Décision actuelle

**Ne pas lancer de développement scientifique substantiel sur le cas d'usage far-field avant d'avoir formulé un besoin indépendant de la solution et un test qui peut réfuter l'hypothèse.** Le corpus disponible justifie d'étudier ce cas, pas de le sélectionner d'office ni d'affirmer qu'il existe une niche vacante.

L'état actuel ne permet pas encore de conclure :
- qu'une métrique de temps de transport apporte une information prédictive supplémentaire ;
- que cette information améliore les estimations de dépôt ou d'exposition ;
- que l'approche surpasse une baseline physique pertinente ;
- que le gain de coût persiste en comptant la préparation des données et la calibration ;
- que le bénéfice répond à une décision concrète d'un utilisateur identifié.

## 1. Hypothèses nulles et modes d'échec à tester

| ID | Hypothèse sceptique | Pourquoi elle est plausible | Observation qui la réfuterait |
|---|---|---|---|
| A1 | La métrique de temps de transport est une reparamétrisation sans gain prédictif | Une transformation de coordonnées ou de temps de parcours peut réexprimer un modèle sans ajouter d'information sur le phénomène | Sur un cas défini à l'avance, une ablation contrôlée montre un gain robuste sur une baseline équivalente, attribuable à la métrique |
| A2 | Le modèle analytique omet des mécanismes dominants | Turbulence, sédimentation, évaporation, dépôt, variation verticale du vent et interactions avec la canopée peuvent dominer selon le régime | Le domaine visé est borné par des hypothèses physiques explicites et les erreurs restent acceptables sur des données indépendantes couvrant ce domaine |
| A3 | « Sans maillage » n'implique pas « moins coûteux au total » | Préparation météo/terrain, résolution des paramètres, calibration, répétition de calculs et contrôle qualité peuvent dominer le coût | Mesure comparative complète du coût, avec même précision cible et mêmes informations disponibles |
| A4 | La limite des outils existants ne correspond pas à un besoin réel non satisfait | Une estimation conservatrice peut être intentionnelle pour la protection réglementaire ; l'incertitude n'implique pas que l'alternative proposée soit meilleure | Un utilisateur et une décision sont identifiés, et une erreur moins conservatrice ou plus précise est explicitement préférable selon un critère documenté |
| A5 | La niche far-field n'est pas vide et peut se réduire | L'écosystème AGDISP/AgDRIFT évolue ; d'autres modèles ou jeux de données peuvent couvrir une partie du problème | Une comparaison récente des capacités, domaines de validité, licences, données et performances met en évidence un besoin résiduel concret |
| A6 | Les avantages hors domaine sont une intuition, pas une propriété | Des contraintes physiques partielles ne garantissent ni l'exactitude ni une meilleure extrapolation | Une proposition mathématique établit une garantie précise, ou une évaluation hors domaine préenregistrée montre un avantage reproductible |
| A7 | La contribution est une réactivation d'une idée historique, sans nouveauté actuelle | Les notions de distance-temps, géométrie asymétrique, transport et modèles réduits ont des littératures connexes | La revue traçable délimite exactement le résultat antérieur et identifie la différence technique ou théorique de J-DriftX |

**Règle :** un échec à réfuter une hypothèse sceptique ne doit pas être reformulé comme une « piste à développer » sans coût, échéance et test de sortie.

## 2. Ce que les sources établissent — et ce qu'elles n'établissent pas

### Dérive de pulvérisation et AGDISP

La page de l'EPA sur l'extension gaussienne AGDISP indique une incertitude importante au-delà de 0,5 mile, des limites concernant les barrières physiques et la météorologie, ainsi qu'une validation limitée au-delà de 2 miles. Elle qualifie les estimations de très conservatrices **dans le contexte d'évaluation discuté**. Source : [EPA — Guidance on the linked AGDISP-Gaussian Extension Models](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/guidance-use-linked-agdisp-gaussian-extension).

Cela soutient une question de recherche sur certains scénarios lointains, mais ne prouve pas :
- que le conservatisme est indésirable pour l'usage réglementaire visé ;
- que le même diagnostic s'applique à toutes les versions, tous les types de pulvérisation ou toutes les distances ;
- que la métrique de J-DriftX représente correctement les mécanismes omis ;
- qu'une prédiction plus précise serait plus utile ou acceptable pour la décision.

L'évaluation de 161 essais publiée en 2002 montre qu'AgDRIFT reproduit plusieurs tendances observées, avec une surestimation en champ lointain dans certaines conditions d'évaporation, et une bonne concordance pour certaines zones tampons de champ proche : [Bird et al. (2002), DOI 10.1002/etc.5620210328](https://doi.org/10.1002/etc.5620210328). Ce résultat interdit de décrire simplement le concurrent comme « mauvais ».

La modernisation d'AGDISP annonce un programme open source et des objectifs de modélisation plus riches, notamment en 3D et pour les drones : [AGDISP Modernization Project — résumé de mars 2026](https://www.agaviation.org/wp-content/uploads/2026/03/AGDISP-Modernization-Project-Summary-20260304f.pdf). Il s'agit d'une annonce de projet, pas d'une preuve que les capacités annoncées sont déjà livrées ou validées. Elle rend néanmoins indispensable la comparaison de périmètre avant d'affirmer qu'un besoin est vacant.

Une validation publiée en 2025 évalue AGDISPpro pour des applications par drones et rapporte des performances variables selon les buses/scénarios : [Science of the Total Environment (2025)](https://doi.org/10.1016/j.scitotenv.2025.178725). Cela confirme que la situation est plus nuancée qu'une opposition générale « modèle mécaniste ancien contre méthode nouvelle ».

### Réduction de modèle et calcul sans maillage

La revue interne présente les ROM comme principalement construites à partir de snapshots haute fidélité. Cette généralisation doit être vérifiée référence par référence : les méthodes réduites ne constituent pas une classe homogène et les coûts de génération du modèle, de calibration et d'inférence doivent être séparés.

Le fait que J-DriftX n'utilise pas de maillage ne suffit pas à établir :
- une complexité asymptotique avantageuse ;
- un coût inférieur pour la même précision ;
- une meilleure robustesse aux changements de régime ;
- une conservation physique ou une extrapolation garanties.

Ces propositions exigent une définition du problème, une baseline et une mesure équitable.

## 3. Fiche G0 — questions auxquelles il manque encore des réponses

Le cas far-field doit être défini **sans employer le vocabulaire de la solution**.

1. **Observable :** dépôt au sol, concentration dans l'air, fraction transportée, exposition ou autre quantité ? Une seule cible primaire doit être choisie pour le premier test.
2. **Scénario :** application aérienne, terrestre ou par drone ? Taille des gouttelettes, hauteur, vent, stabilité atmosphérique, relief et végétation ? Ne pas fusionner ces régimes dans un benchmark unique.
3. **Utilisateur :** organisme réglementaire, évaluateur de risque, agronome, chercheur ou développeur d'un autre modèle ? Les pertes associées aux erreurs sont différentes.
4. **Décision :** quelle décision changerait si la prédiction était plus rapide ou plus précise ? Quelle erreur est coûteuse, et dans quel sens ?
5. **Baseline :** quelle méthode est réellement utilisée dans ce scénario et quelle version est disponible ? Comparer au moins une baseline pertinente, pas seulement un cas gaussien choisi pour être facile.
6. **Données :** quelles données indépendantes, sous licence utilisable, sont disponibles pour calibrer puis évaluer ? Les données de validation ne doivent pas servir à choisir la formulation.
7. **Seuil de succès :** quel compromis précision/coût/robustesse serait assez important pour changer la décision ? Le seuil doit être justifié par l'usage, pas choisi après lecture des résultats.
8. **Critère d'arrêt :** quel résultat ferait abandonner le cas far-field au profit d'un autre cas ou du fallback théorique ?

Tant que les réponses 1–4 et 6 ne sont pas renseignées avec des éléments vérifiables, le choix du cas d'usage reste provisoire.

## 4. Comparer les cas candidats sans les classer artificiellement

| Candidat | Intérêt potentiel | Objection principale | Preuve minimale requise |
|---|---|---|---|
| Far-field de dérive de pulvérisation | Incertitudes documentées dans certains scénarios ; lien historique direct | L'utilité d'une prédiction moins conservatrice n'est pas universelle ; les modèles évoluent | Décision utilisateur identifiée, scénario borné, données indépendantes et baseline à jour |
| Dispersion atmosphérique à faible coût | Besoin possible de calcul rapide ou d'évaluations répétées | Domaine trop vaste ; comparaison à AERMOD/CALPUFF ou autres outils peut ne pas être pertinente sans régime précis | Un cas physique étroit avec observable et contraintes de calcul définis |
| Identification de source (STE) | Intérêt méthodologique de modèles directs rapides | Problème inverse mal posé ; identifiabilité et incertitude peuvent dominer le coût du modèle direct | Cas inverse analytique, étude d'identifiabilité, baseline inverse et observations simulées avec bruit |
| Modèle jouet théorique | Permet d'isoler les propriétés de la géométrie/du transport | Risque élevé de résultat connu ou purement illustratif | Définition précise, proposition non triviale, preuve, contre-exemples et revue de nouveauté |

Aucune option ne peut être déclarée gagnante sur les informations présentes. La prochaine action n'est pas de calculer un score composite arbitraire : il faut d'abord recueillir les informations manquantes qui changent réellement la décision.

## 5. Protocole du prochain test, si G0 est franchi

1. Geler une définition du problème et un observable primaire.
2. Écrire les hypothèses physiques et le domaine de validité avant de coder.
3. Choisir une baseline reconnue pour le même régime, avec entrées et informations comparables.
4. Définir le protocole, les métriques, le seuil de succès et les conditions d'arrêt avant d'observer les résultats.
5. Commencer par un cas analytique servant à vérifier le code, sans le présenter comme preuve d'utilité applicative.
6. Ajouter un cas contrôlé qui isole l'effet de la métrique de temps de transport par ablation.
7. Ne passer à une validation indépendante qu'après avoir évité les erreurs conceptuelles et vérifié la comparabilité.
8. Publier aussi les résultats nuls, les cas où la baseline gagne et les coûts complets.

## 6. Décision provisoire et critères d'abandon

- **Poursuivre G0** si un utilisateur, une décision, un observable et un jeu de validation indépendant peuvent être nommés et justifiés.
- **Restreindre le domaine** si le bénéfice potentiel ne concerne qu'un régime physique étroit.
- **Basculer vers G1 théorique** si le besoin pratique échoue mais qu'une propriété mathématique précise reste intéressante.
- **Conserver comme ressource pédagogique** si l'idée est connue mais fournit une explication claire et reproductible.
- **Archiver/arrêter** si ni besoin mesurable, ni résultat théorique non trivial, ni valeur pédagogique suffisante ne subsistent.

## Liens de traçabilité

- [Cadre de décision et de preuve](08-decision-utilite-et-preuve.md)
- [Fallback modèle jouet](09-fallback-modele-jouet.md)
- [Revue structurée de l'état de l'art](02-revue-etat-art-2026.md)
- [Plan d'intégration de la revue systématique](07-plan-integration-revue-systematique.md)


## Résultat de la recherche externe G0

La recherche externe a identifié le jeu de données ouvert [CAPRIV](https://doi.org/10.57745/Z8OJ3A), dont la table de cultures de plein champ contient 3 792 collecteurs. Les distances décrites sont de l'ordre de 1–25 m pour les collecteurs de dépôt et de 5 m pour les fils de mesure aérienne : ces données ne valident pas le far-field à plusieurs kilomètres. Le dépôt de gouttelettes n'est pas automatiquement équivalent au transport d'un scalaire passif. Le ministère français documente aussi une décision réglementaire concrète liée aux ZNT et à la réduction de dérive, mais cela ne prouve pas que J-DriftX est adapté à cette décision.

**Conclusion : G0 reste bloqué.** Ne pas utiliser CAPRIV comme validation far-field ni lancer un benchmark avant d'avoir défini utilisateur, décision, observable, régime physique et baseline. Voir la [fiche G0 fondée sur les preuves externes](11-g0-evidence-externe.md) pour la matrice complète et les références.
