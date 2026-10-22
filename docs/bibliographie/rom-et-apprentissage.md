# Modèles réduits, surrogates et apprentissage

## Rapport avec J-DriftX

Ces méthodes peuvent être **concurrentes sur la vitesse d'évaluation** et **complémentaires pour la calibration**, mais elles ne sont pas interchangeables par définition. Beaucoup de ROM construisent une base réduite à partir de simulations haute fidélité ; J-DriftX vise historiquement une réduction a priori fondée sur la similitude et une géométrie de transport. Cette distinction est une hypothèse de positionnement à vérifier sur des sources primaires et des benchmarks comparables.

### Vervecken, Camps & Meyers (2015) — *Stable reduced-order models for pollutant dispersion in the built environment*

- **Méthode attestée par le résumé éditeur :** projection d'un modèle CFD résolvant l'équation instationnaire d'advection-diffusion sur un champ de vitesse de fond stationnaire vers un sous-espace de Krylov construit par l'algorithme d'Arnoldi. Le champ d'écoulement est pré-calculé ; la méthode ne supprime donc pas le coût initial du calcul CFD.
- **Cas étudié :** rejet temporel d'un gaz neutre dans l'environnement bâti de la centrale de Doel, avec géométrie du site et vent de fond connus. Ce n'est pas un test de dérive de gouttelettes agricoles.
- **Résultats rapportés par les auteurs :** environ 2500× de réduction du temps de calcul par rapport au modèle CFD après initialisation ; le ROM tourne environ 25× plus vite que le temps réel dans les cas étudiés. Les auteurs rapportent aussi un coût de calcul environ 10⁵ fois inférieur dans leur configuration. Ces ratios ont des dénominateurs et périmètres différents : ne pas les fusionner ni les présenter comme des garanties générales.
- **Relation :** baseline concurrente sur le coût d'évaluation, mais famille de réduction différente de la similitude a priori de J-DriftX.
- **Différence à tester :** coût de construction/initialisation, dépendance au champ CFD pré-calculé, régimes physiques couverts, stabilité, erreur hors des cas étudiés et capacité d'extrapolation.
- [Notice éditeur et résumé](https://doi.org/10.1016/j.buildenv.2015.05.008)

### POD-GPR pour la dispersion atmosphérique microscopique (HAL, 2024)

- **Méthode :** base POD et régression de processus gaussien à partir de snapshots LES, d'après la description recensée.
- **Relation :** baseline concurrente pour prédiction rapide après phase coûteuse de génération des snapshots.
- **Conséquence :** comparer séparément coût de préparation, coût d'inférence et erreur sur des cas hors échantillon.
- [Document](https://hal.science/hal-04310899/document)

### ROM physique POD-NN pour la pollution urbaine (CMAME, 2024)

- **Méthode :** ROM fondée sur POD et réseau neuronal.
- **Relation :** approche hybride physique/apprentissage ; potentiellement concurrente pour monitoring temps réel.
- **Conséquence :** comparer sur le même cas de dispersion, et ne pas assimiler la présence d'un prior physique à une preuve de conservation ou de robustesse.
- [Article](https://www.sciencedirect.com/science/article/abs/pii/S0045782523005406)

### ROM avec assimilation de données (2023, *Computers & Fluids*)

- **Relation :** méthode complémentaire ou concurrente selon que la question principale est la prédiction directe ou l'estimation d'état.
- **Intuition commune :** réduire les coûts tout en exploitant des observations.
- **Conséquence :** comparer la manière dont les observations entrent dans le modèle et évaluer l'identifiabilité.
- [Article, *Computers & Fluids* 257, 105862](https://doi.org/10.1016/j.compfluid.2023.105862)

### Référence ScienceDirect PII S2666449621000372 — métadonnées à confirmer

- **Statut bibliographique :** non vérifié dans cette passe. La page éditeur a refusé l'accès automatisé (HTTP 403) et les recherches exactes sur le PII n'ont pas permis de confirmer titre, auteurs, méthode POD+RBF, année ou revue.
- **Précaution :** ne pas utiliser cette référence comme preuve d'un surrogate POD+RBF urbain tant que le titre et le résumé n'ont pas été contrôlés dans une notice éditeur, Crossref ou un dépôt institutionnel.
- [Lien éditeur à vérifier](https://www.sciencedirect.com/science/article/pii/S2666449621000372)

### Fourier Neural Operator pour les panaches radioactifs (Ayoub et al., 2024)

- **Relation :** analogue méthodologique pour la prévision rapide de transport/dispersion ; concurrent potentiel sur l'inférence, mais dans un autre domaine source et avec entraînement.
- **Intuition commune :** approximer une application entre champs ou conditions physiques et champs de concentration.
- **Protocole effectivement rapporté :** le surrogate U-FNO émule les sorties du simulateur WSPEEDI à partir d'un corpus de 616 simulations, séparé en 85 % entraînement et 15 % test. Les auteurs rapportent environ 17 minutes d'entraînement sur GPU A100, puis 1,26 s par inférence sur CPU, contre environ 82 minutes pour une simulation WSPEEDI de six heures sur un CPU Intel Xeon Gold 6240 ; le facteur annoncé est donc une comparaison **simulation physique unique vs inférence après préparation et entraînement**, pas un coût total de bout en bout.
- **Limites importantes :** la cible d'évaluation est le simulateur WSPEEDI, non une vérité terrain indépendante. Les auteurs décrivent l'étude comme une preuve de concept et indiquent que la méthode doit encore être testée/validée sur des données réelles. La formulation « tout scénario de rejet » dans le résumé ne démontre pas une généralisation hors distribution : elle doit être lue à la lumière du corpus fini, du protocole de séparation et des limites observées, notamment la sous-estimation de certains taux de dose lors de dépôts humides.
- **Conséquence pour J-DriftX :** ne pas citer « ×4000 » comme une performance directement comparable sans reproduire un protocole comparable ; publier séparément coût de génération des données, entraînement, inférence, erreur sur un test indépendant, extrapolation et validation terrain. Ne pas transférer directement les résultats au spray drift.
- [Article et texte intégral éditeur](https://link.springer.com/article/10.1007/s00477-024-02738-8)

### Architecture MCxM 3D pour la dispersion de pollution atmosphérique (CEA/HAL, 2024)

- **Relation :** méthode d'apprentissage avec priors physiques/opérateurs neuronaux ; approche apparentée par l'objectif de prédiction et l'utilisation d'information physique.
- **Différence :** architecture apprise sur des données, contre l'hypothèse d'une solution de similitude explicite.
- [Document](https://cea.hal.science/cea-04810109/document)

### Surrogate ML pour les émissions industrielles (2025) et accidents de type Seveso (numéro 2023, publication en ligne 2022)

- **Relation :** analogues applicatifs de dispersion rapide, mais avec sources et régimes différents.
- **Conséquence :** utiles pour définir métriques de précision, protocoles de validation et exigences de décision en situation d'urgence ; ne pas les considérer comme validation directe de J-DriftX.
- [Émissions industrielles (2025)](https://link.springer.com/chapter/10.1007/978-3-032-02728-3_53)
- [Accidents Seveso (numéro 2023 ; en ligne en 2022)](https://link.springer.com/article/10.1007/s00477-022-02288-x)

## Protocole minimal de comparaison

1. Définir une question physique et un domaine de validité communs.
2. Utiliser les mêmes entrées, observations, unités, conditions initiales et données de test.
3. Séparer coût de préparation/entraînement, coût d'inférence et coût de calibration.
4. Mesurer erreur, robustesse, conservation/positivité si pertinentes, sensibilité et comportement hors domaine.
5. Publier scripts, versions, graines aléatoires et limites connues.
