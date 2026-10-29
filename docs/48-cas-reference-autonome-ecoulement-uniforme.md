# 48 — Cas de référence autonome : écoulement uniforme

**Statut.** Note de définition exécutant l’étape 3 de l’ordre confirmé de l’[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : formaliser un cas de référence autonome — écoulement uniforme — avec unités, domaine, conditions aux limites, solution de référence, observable et limites explicites ; le cisaillement reste un contre-exemple distinct à la construction projetée. Définition avant implémentation, sur le même principe que la [note 31](31-investigation-champ-multiniveaux.md) ; cette note ne modifie aucun code. Elle réalise l’item 3 du premier sous-ensemble exécutable figé par le [contrat minimal de la baseline](47-contrat-minimal-baseline.md) §5.

**Date :** 29 octobre 2026. **Suivi :** [issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) (étapes 3 puis 4) ; squelette de benchmarks S0 : [note 39](39-squelette-benchmarks-s0.md).

## 1. Ce que « autonome » exige

Le cas de référence est autonome au sens suivant : un lecteur disposant du dépôt et de cette note peut (a) reconstruire la géométrie et les paramètres sans renvoi implicite, (b) vérifier les unités de chaque terme, (c) reproduire la solution de référence et (d) savoir précisément ce que le cas établit et ne établit pas. Il sert de socle aux étapes 4 (reconstruction implémentée et testée) et 5 (comparaison à référence indépendante) de l’ordre #232.

## 2. Définition physique figée

### 2.1 Hypothèses (toutes étiquetées « reconstruction », [note 44](44-strategie-reprise-et-elargissement-scientifique.md) §2)

- **Linéarité (H1)** : scalaire passif, aucune réaction, aucun dépôt, aucune perte ; la superposition de sources est permise.
- **Stationnarité (H3)** : régime établi sur la fenêtre d’évaluation ; la source est continue, la durée d’émission n’entre pas dans le cas.
- **Homogénéité du segment (H5)** : terrain rural plat, paramètres de similitude constants — une seule classe de Pasquill sur tout le segment.
- **Vent** : uniforme horizontal, u = (U, 0, 0) avec U > 0 strictement ; divergence nulle triviale, aucune composante verticale. La garde de vitesse minimale du coût (convention algorithmique du dépôt) ne s’active pas : le vent est uniforme et non nul.
- **Turbulence** : représentée par les écarts-types de Briggs (site rural) indexés par classe de Pasquill ; aucune EDP résolue, aucun maillage.

### 2.2 Paramètres du cas (figés, alignés sur CAS_S0_DEFAUT)

| Paramètre | Symbole | Valeur | Unité |
|---|---|---|---|
| Vent (selon +x) | U | 3,0 | m s⁻¹ |
| Débit massique d’émission | Q | 2,0 | kg s⁻¹ |
| Classe de stabilité (Briggs rural) | — | C | — |
| Hauteur effective de source | H | 1,0 | m |
| Altitude de mesure | z_m | 1,5 | m |
| Arcs sous le vent | x | 100, 200, 400, 800 | m |
| Positions latérales | y | −50, 0, +50 | m |

La grille de prélèvements est le croisement arcs × positions latérales à z_m (12 points), conforme au contrat CasSynthetique : grille ordonnée non vide, vérité strictement positive, invariants vérifiés à l’enregistrement ([note 39](39-squelette-benchmarks-s0.md) §1).

### 2.3 Domaine et fenêtre d’évaluation

Domaine mathématique : demi-espace z ≥ 0, x > 0 strictement (la solution est singulière à la source). Fenêtre d’évaluation : arcs 100–800 m, |y| ≤ 50 m, z = z_m. Le choix x ≥ 100 m exclut la singularité de la source et le champ proche de la buse (hors périmètre de la reconstruction de similitude, [contrat](47-contrat-minimal-baseline.md) §3.1). La fenêtre est un choix d’échantillonnage, pas une frontière physique : la solution est définie sur tout le demi-espace.

### 2.4 Conditions aux limites et conventions

- **Sol z = 0** : réflexion totale par la méthode des images — aucune perte, aucun dépôt ; le terme vertical est la somme de deux gaussiennes en (z − H) et (z + H).
- **Aucune autre frontière** : décroissance exponentielle loin de l’axe ; pas de condition latérale ou amont imposée, la solution analytique la détermine partout.
- **Amont** : la source ponctuelle continue en (0, 0, H) est la seule entrée du bilan du cas.

### 2.5 Solution de référence

La solution de référence est le panache gaussien en métrique cartésienne tel qu’implémenté par le package ([similitude.py](../src/jdriftx/similitude.py), fonction concentration_panache) ; la classe de stabilité ([note 24](24-classes-stabilite-pasquill-objet.md)) reste la source unique de vérité des coefficients de Briggs :

~~~text
C(x,y,z) = Q / (2π U σ_y(x) σ_z(x))
          · exp(−y² / (2σ_y(x)²))
          · [ exp(−(z−H)² / (2σ_z(x)²)) + exp(−(z+H)² / (2σ_z(x)²)) ]
~~~

avec σ_y(x) = a·x/√(1+d·x) et σ_z(x) selon la forme de la classe (linéaire, racine ou inverse), coefficients de Briggs site rural indexés par classe de Pasquill. Le domaine d’implémentation impose x > 0 strictement, U > 0, Q ≥ 0, H ≥ 0.

**Contrôle dimensionnel** (discipline du [registre](46-registre-erreurs-incoherences-documentaires.md) §4 règle 4) : [Q/(U σ_y σ_z)] = (kg s⁻¹)/((m s⁻¹)·m·m) = kg m⁻³, cohérent avec une concentration massique volumique ; les exposants des exponentielles sont sans dimension.

**Statut de la solution** : reconstruction (famille classique, « connue en métrique cartésienne » selon le chapitre 2008). Dans le cas uniforme, la généralisation travel-time coïncide avec τ = x/U ([note 37](37-transformation-tau-eta-cas-uniforme.md) : u·∇τ = 1 exact, jacobien U constant) — la solution de référence ne revendique aucune propriété du modèle réduit au-delà de ce cas exact.

### 2.6 Transport dirigé dans le cas uniforme (deuxième volet du sous-ensemble figé)

- **Temps de transport dirigé** : pour B à l’aval de A, T(A→B) = (x_B − x_A)/U ; coût +∞ en amont et pour les composantes latérales strictes. Implémenté et testé (pseudo_distance_uniforme ; [note 19](19-investigation-g0s-temps-de-parcours.md)).
- **Cas exact 1D à vitesse constante** : temps de première arrivée en forme fermée, implémenté et testé (temps_premiere_arrivee_1d ; reproductibilité documentée dans le [bilan MVP-S](21-bilan-mvp-s-1d.md)).
- **Carte travel-time explicite** : χ(τ, η₁, η₂) = (Uτ, η₁, η₂), difféomorphisme C∞ de jacobien U, u·∇τ = 1 exact, théorème conditionnel d’égalité des flux ([note 37](37-transformation-tau-eta-cas-uniforme.md)) : le cas uniforme est le seul champ où tous les objets (temps d’arrivée, temps projeté, coût dirigé) coïncident.

## 3. Observable et métriques

- **Observable** : concentration aérienne C (kg m⁻³) aux 12 points de la grille — conforme à l’[issue #43](https://github.com/JM-Brun/J-DriftX/issues/43) (observable = concentration aérienne).
- **Métriques préenregistrées, inchangées** ([note 39](39-squelette-benchmarks-s0.md) §3) : FAC2 (0,5 ≤ prédiction/vérité ≤ 2, bornes incluses), NMSE (dénominateur Σ(vérité)²) ; évaluation par essai indépendant, jamais par point isolé.
- **Coûts (étape 5)** : préparation, calibration, coût par requête, coût de champ complet, mémoire et erreur rapportés séparément. Le facteur historique 10³–10⁴ ne sera pas « retrouvé » : il sera recalculé sur ce protocole, sans être présenté comme validation du chiffre historique ([contrat](47-contrat-minimal-baseline.md) §3.4 : statut « annoncée seulement »).
- **Clause** ([docs/21](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md)) : cas synthétique, générateur déterministe, aucune donnée observée — « pas une validation physique ».

## 4. Limites explicites — ce que le cas établit et ne établit pas

**Établit** : cohérence dimensionnelle de la solution de référence ; reproductibilité (commande du squelette S0) ; pipeline grille → vérité → métriques ; conservation du panache gaussien sur les cas et grilles testés du dépôt ; exactitude des temps de transport au cas uniforme.

**N’établit pas** : toute propriété en champ variable (champ multi-niveaux, relief, divergence entre niveaux) ; dépôt et pertes au sol ; cisaillement ; non-stationnarité ; champ proche de la buse ; validation terrain (porte G1, DIFLU délégué) ; et aucune revendication de coût héritée des sources.

Dans le cas S0, la vérité analytique **est** la baseline gaussienne ([note 39](39-squelette-benchmarks-s0.md) §5) : une comparaison à cette vérité valide un pipeline ou une reconstruction, jamais une source historique et jamais une supériorité.

## 5. Contre-exemple distinct : cisaillement

Le contre-exemple de cisaillement reste **distinct** du cas de référence, conformément à l’ordre #232. Champ u = (v(y), 0) avec v non constante : la construction projetée d_A = (x − x_A)/v(y_A) donne u·∇d_A = v(y)/v(y_A), non identiquement égal à 1 dès que v varie (DRX-ERR-015 ; démonstration et tests : [note 33](33-test-contre-exemple-cisaillement.md), [tests/test_shear_projected_cost.py](../tests/test_shear_projected_cost.py) ; dérivation conditionnelle : [note 32](32-conservation-coordonnees-travel-time.md)).

Rôles du contre-exemple :

1. **garde-fou de régression** : le coût projeté ne doit jamais être traité comme une coordonnée travel-time régulière en champ cisaillé ;
2. **rappel de périmètre** : le cas uniforme est le seul où projection et temps d’arrivée coïncident ; toute extension en champ variable (S0-b en loi de puissance, [note 39](39-squelette-benchmarks-s0.md) §6) devra être définie comme cas distinct, avec sa propre vérité et ses propres tests.

Aucune fusion du contre-exemple dans le cas de référence ; les statuts figés ([contrat](47-contrat-minimal-baseline.md) §3.2) ne sont pas modifiés.

## 6. Relations au code existant et écarts

| Objet du dépôt | Rôle vis-à-vis du cas de référence |
|---|---|
| CAS_S0_DEFAUT ([benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py)) | **Le cas de référence est le cas S0 figé** : paramètres identiques ; la note fige son contrat, le code reste l’implémentation |
| concentration_panache ([similitude.py](../src/jdriftx/similitude.py)) | Solution de référence ; aucun développement mathématique dupliqué |
| SCENARIO_DEFAUT (experiences/uniforme.py) | Scénario jouet de coût dirigé (vent 2 m/s, A=(0,0), B=(300,65), τ = 150 s, +∞ au retour) : objet distinct, sans contradiction — il illustre le volet transport avec ses propres valeurs |
| benchmarks/metriques.py | Métriques FAC2/NMSE, conventions figées [note 39](39-squelette-benchmarks-s0.md) §3 |
| tests/test_shear_projected_cost.py | Contre-exemple distinct (section 5) |

**Écarts explicites : aucun.** La note ne change aucune valeur du code ; si le code évoluait, le contrat devra être révisé de façon visible, pas par glissement silencieux.

## 7. Ce que cette définition débloque

- **Étape 4** : implémentation et tests de la reconstruction sur ce cas, en distinguant héritage documentaire, reconstruction corrigée et extensions, étiquetées.
- **Étape 5** : comparaison à une référence indépendante — la méthodologie des deux résolutions indépendantes (fermée vs EDP) existe déjà pour le modèle réduit ([note 35](35-figure-03-modele-reduit-edp.md)) ; les coûts seront rapportés séparément.
- **Extensions conditionnelles** (jamais par défaut, [contrat](47-contrat-minimal-baseline.md) §5) : champ multi-niveaux R3 après arbitrages ; source impulsionnelle (la solution puff existe, cas à spécifier) ; S0-b cisaillement (vérité à définir).

## Références internes

- [Contrat minimal de la baseline](47-contrat-minimal-baseline.md)
- [Squelette de benchmarks S0](39-squelette-benchmarks-s0.md)
- [Cas synthétiques S0–S3](21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) ; [bilan MVP-S 1D](21-bilan-mvp-s-1d.md)
- [Investigation G0-S](19-investigation-g0s-temps-de-parcours.md) ; [conservation en coordonnées travel-time](32-conservation-coordonnees-travel-time.md) ; [transformation τ-η : cas uniforme](37-transformation-tau-eta-cas-uniforme.md)
- [Test du contre-exemple de cisaillement](33-test-contre-exemple-cisaillement.md)
- [Registre des erreurs](46-registre-erreurs-incoherences-documentaires.md) ; [audit de l’article 2006](45-audit-article-mohammadi-brun-2006.md)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232) ; [issue #43 — critères](https://github.com/JM-Brun/J-DriftX/issues/43) ; [issue #42 — propriétés](https://github.com/JM-Brun/J-DriftX/issues/42)
