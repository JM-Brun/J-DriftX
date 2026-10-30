# Audit P0 — frontières numériques publiques (30 octobre 2026)

## 1. Objet et périmètre

Poursuivre l'audit des frontières numériques du package, en ciblant les fonctions publiques qui reçoivent directement des coordonnées, tableaux ou paramètres physiques sans configuration validée préalable.

L'objectif est de vérifier les contrats effectifs avant toute modification. Cet audit ne constitue ni une refonte générale des validateurs ni une invitation à répéter les contrôles déjà garantis par une configuration immuable.

État examiné : branche `main` du 30 octobre 2026.

Périmètre inspecté :
- modules d'enseignement et d'expérimentation : `fields.py`, `terrain.py`, `trajectories.py`, `advection_diffusion.py`, `periodic_transport.py` ;
- interfaces et adaptateurs : `_protocoles.py`, `champ_analytique.py`, `vents.py` ;
- contrats existants : `source.py`, `reliefs.py`, `similitude.py`, `similitude_objets.py`, `metric.py` ;
- cas d'utilisation d'échantillonnage dans `experiences/reference_independante.py`.

Les modules d'enseignement ne sont pas ré-exportés à la racine de `jdriftx`, conformément à l'intention documentée dans `__init__.py`. Ils exposent néanmoins des fonctions appelables directement depuis leurs sous-modules : leur contrat d'entrée reste à définir et à respecter.

## 2. Règle de lecture

Un contrôle n'est pas redondant si la fonction est une frontière publique autonome et accepte des valeurs brutes. En revanche, un contrôle répété en aval peut être inutile lorsque l'appelant reçoit déjà une valeur issue d'un objet validé et immuable.

Avant de corriger un cas, préciser :
1. le contrat de la fonction publique (types, formes, finitude, domaine physique) ;
2. si les entrées sont brutes ou garanties par une configuration ;
3. si le contrôle doit appartenir au constructeur, à la fonction appelée ou à l'adaptateur ;
4. les comportements historiques et messages d'erreur à préserver ;
5. les tests existants qui couvrent déjà le même invariant.

Convention déjà établie dans `source.py`, `vents.py`, `similitude.py` et `reliefs.py` : les booléens ne sont pas des scalaires physiques et ne doivent pas être acceptés silencieusement par coercition en 0/1.

## 3. Écarts confirmés sur les fonctions autonomes

### 3.1 `fields.vector_field`

Contrat explicite :
- `x` et `y` ont des formes identiques ;
- les coordonnées sont finies ;
- `speed`, `angle_deg`, `shear` et `radial_strength` sont finis ;
- `kind` appartient à `uniform | shear | radial`.

Écart observé : les tableaux sont convertis immédiatement avec `np.asarray(..., dtype=float)`. Une entrée booléenne ou une séquence contenant des booléens peut donc être convertie en 0/1 avant le contrôle de finitude. Les contrôles `np.isfinite` des paramètres scalaires acceptent également les booléens.

Le signe des paramètres `speed`, `shear` et `radial_strength` n'est pas restreint par la formule actuelle ; ne pas ajouter de contrainte de positivité sans décision physique/documentée.

### 3.2 `terrain.terrain_surface`

Contrat explicite :
- formes identiques pour `x` et `y`, sans broadcasting ;
- coordonnées et paramètres finis ;
- `width > 0` ;
- `kind` dans `flat | hill | valley | ridge`.

Écart observé : même coercition booléenne que dans `fields.vector_field`, pour les coordonnées comme pour les paramètres scalaires. Le contrôle `width <= 0` ne corrige pas ce défaut de type.

Attention à la couche `ReliefSynthetique.altitude` : elle valide déjà ses coordonnées avec le helper de `reliefs.py` avant de déléguer à `terrain_surface`. Il ne faut pas ajouter une deuxième validation spécifique dans ce wrapper. La fonction autonome `terrain_surface`, elle, reste une frontière indépendante.

### 3.3 `trajectories.integrate_trajectory`

Contrat explicite :
- `x0`, `y0`, `t0`, `t_end`, `dt` sont finis ;
- `dt > 0` et `t_end >= t0` ;
- méthode `euler | rk4` ;
- le callback retourne un tuple de deux composantes réelles finies ; les booléens sont déjà exclus pour les composantes retournées.

Écart observé : le contrôle initial `np.isfinite` accepte les booléens pour les coordonnées et les paramètres temporels. La validation des sorties du callback est plus stricte que celle des entrées.

Ne pas ajouter une seconde validation des coordonnées à chaque étape si l'intégrateur garantit déjà que l'état accepté est fini ; conserver les contrôles d'avancement temporel et de finitude après intégration, qui protègent des débordements calculés.

### 3.4 `advection_diffusion.gaussian_advection_diffusion`

Contrat explicite :
- `time >= 0`, `mass >= 0`, `diffusivity >= 0`, `initial_sigma > 0` ;
- `initial_center`, `velocity` et les autres paramètres sont finis ;
- `x` est un tableau numérique réel fini.

Écart observé : `np.isfinite` accepte les booléens dans les paramètres scalaires et `np.asarray(x, dtype=float)` les convertit silencieusement dans les coordonnées. La fonction est autonome et ne reçoit pas de configuration validée.

Les éventuels débordements de `initial_sigma**2`, `diffusivity*time`, `velocity*time` ou de l'évaluation gaussienne sont un sujet distinct : ne pas les confondre avec la validation de type et les traiter seulement après analyse numérique dédiée.

### 3.5 `periodic_transport.periodic_sine_solution`

Contrat explicite :
- paramètres scalaires finis ;
- `time >= 0`, `length > 0`, `mean_concentration >= amplitude >= 0`, `diffusivity >= 0` ;
- coordonnées réelles finies.

Écart observé : les booléens passent les contrôles `np.isfinite` des paramètres et peuvent être convertis en flottants dans `x`.

Les deux solveurs (`solve_periodic_sine_transport`, `solve_periodic_upwind_euler`) passent par `_validate_periodic_parameters`, partagé depuis la PR #82. Ne pas dupliquer cette validation dans chaque solveur. L'audit doit cependant vérifier le contrat de type de ce helper partagé et de `periodic_sine_solution`, qui est aussi appelable seule.

Point à vérifier séparément : `isinstance(n_cells, int)` rejette certains scalaires entiers NumPy ; `bool` est actuellement rejeté indirectement car inférieur à 8, mais sans règle explicite « booléens exclus ». Toute évolution doit définir le contrat entier (entier Python seulement ou `numbers.Integral`), préserver les messages attendus et couvrir les deux solveurs.

## 4. Adaptateurs et méthodes ponctuelles : contrat à clarifier avant correction

### 4.1 `VentDeChampPlan.vitesse` et `AdaptateurTrajectoire2D.__call__`

Ces adaptateurs transmettent des coordonnées à une implémentation fournie par l'appelant. `ChampFonctionCourant` valide ses coordonnées, mais le protocole structurel `ChampPlan` ne peut pas garantir que toute implémentation tierce le fasse.

Décision nécessaire : le contrat `ChampPlan` exige-t-il explicitement des coordonnées finies et numériques, et l'adaptateur doit-il les faire respecter avant délégation ? Ne pas dupliquer un contrôle si l'appelant est déjà `integrate_trajectory`, mais ne pas supposer que l'adaptateur n'est jamais appelé directement.

### 4.2 `VentUniforme.vitesse` et `VentProfilPuissance.vitesse`

Le premier ignore les coordonnées par définition d'un champ uniforme ; le second n'utilise que `z`. L'audit ne qualifie pas l'absence de validation de `x` et `y` de défaut établi : il faut décider si le contrat `Vent.vitesse(x,y,z)` exige la validité de toutes les coordonnées même lorsque le modèle est indépendant de certaines d'entre elles.

### 4.3 `EchantillonneurBilineaire.concentration`

La méthode reçoit directement `y` et `z`, puis calcule des indices et vérifie les bornes. Contrairement aux points `PointMesure` utilisés par les routes de comparaison, un appel direct à cette méthode n'est pas nécessairement protégé par un modèle de données validé.

Vérifier explicitement le comportement pour booléens, NaN et infinis avant toute conversion en indice. La correction éventuelle doit rester locale à cette frontière, sans répéter la validation des objets `PointMesure` dans `RouteEdp`.

**Résultat de l'audit (#367).** L'appel direct acceptait effectivement `bool`/`numpy.bool_` comme coordonnées et laissait NaN atteindre la conversion en indice. Les coordonnées sont désormais contrôlées localement comme scalaires réels finis avant le calcul des indices ; chaînes, complexes, tableaux non scalaires et valeurs non finies sont rejetés. Les points finis hors grille conservent le message de domaine historique. Aucune validation n'est ajoutée dans `RouteEdp`, qui transmet des `PointMesure` déjà validés. Les tests caractérisent un contrat logiciel, pas une propriété physique.

## 5. Composants déjà conformes — ne pas réintroduire de validations

- `SourcePanache` : `_reel_fini` refuse les booléens, normalise les valeurs en `float` et vérifie les domaines physiques.
- `vents.py` : les valeurs portées par les dataclasses sont validées et normalisées à la construction ; les composantes de vitesse déléguées sont vérifiées.
- `similitude.py` : `_reel_fini` et `_tableau_reel_fini` excluent les booléens, les complexes, les valeurs non finies et les coercitions textuelles ; les formes sont ensuite vérifiées par les opérations concernées.
- `reliefs.py` : les tableaux sont validés avant conversion, les booléens masqués par promotion de listes sont détectés, et les grilles MNT sont figées sur stockage immuable.
- `metric.py` : les formes, finitudes, vitesses minimales et représentabilités des coûts sont contrôlées ; les coordonnées et vecteurs sont convertis avant les opérations géométriques avec contrôles de débordement.
- `Point3D`, `ParametresPuff`, `CasS0`, `PointMesure` et les configurations Pydantic des expériences : les tests de frontière booléenne existent déjà dans `tests/test_numeric_scalar_bool_boundaries.py`.

Ces composants doivent servir de référence de comportement. Éviter de créer des validateurs locaux divergents.

## 6. Stratégie de correction proposée

1. Fixer le contrat commun des scalaires réels et des tableaux réels : booléens exclus, complexes exclus, valeurs finies, coercition textuelle interdite, conversion float64 représentable.
2. Examiner si les helpers équivalents de `similitude.py` et `reliefs.py` peuvent être extraits dans un module interne commun sans modifier les messages publics ni les comportements acceptés. Ne pas créer cette abstraction avant d'avoir comparé précisément leurs contrats et leurs usages.
3. Appliquer les validations uniquement aux fonctions autonomes qui en ont besoin ; laisser les wrappers s'appuyer sur les objets validés lorsqu'ils garantissent déjà les invariants.
4. Préserver les domaines physiques existants : ne pas transformer un paramètre signé en paramètre positif sans justification mathématique.
5. Ajouter les tests de non-régression au niveau de chaque frontière publique : `bool`, `np.bool_`, tableau booléen, séquence mixte nombre/bool, NaN, infini, forme incorrecte et valeurs numériques valides usuelles.
6. Exécuter tests ciblés, suite complète, Ruff et mypy strict avant de considérer les corrections terminées.

## 7. Ordre de traitement

| Ordre | Cible | État | Motif |
|---|---|---|---|
| 1 | `fields.vector_field`, `terrain.terrain_surface` | Écart confirmé | Frontières directes, coercition booléenne |
| 2 | `integrate_trajectory`, `gaussian_advection_diffusion` | Écart confirmé | Contrôles scalaires permissifs et/ou coercition booléenne des tableaux |
| 3 | `periodic_sine_solution`, helper périodique partagé | Écart confirmé | Cohérence du contrat commun et des fonctions publiques |
| 4 | Adaptateurs `vents.py` | Contrat à clarifier | Délégation à des protocoles structurels |
| 5 | `EchantillonneurBilineaire.concentration` | Contrat à vérifier par tests ciblés | Entrées ponctuelles sans configuration obligatoire |

## 8. Hors périmètre de cette étape

- Harmonisation `Literal` / `StrEnum` : sujet de typage et de cohérence, pas une correction P0 de frontière numérique.
- Remplacement des tuples de résultats par des dataclasses : changement d'API potentiellement cassant.
- Refonte générale OOP ou factorisation des solveurs numériques.
- Modification des équations, des hypothèses physiques ou des unités.
- Toute affirmation de validation physique du modèle.

**Conclusion :** les écarts confirmés concernent d'abord les fonctions autonomes des modules pédagogiques. Les composants de configuration et les validateurs de `similitude.py` / `reliefs.py` sont déjà plus stricts. La prochaine PR de correction doit donc s'appuyer sur les contrats ci-dessus et les tests de frontière, sans ajouter de validation redondante aux objets déjà validés.
