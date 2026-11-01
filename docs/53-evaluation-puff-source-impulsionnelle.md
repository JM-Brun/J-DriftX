# 53 — Évaluation dirigée d'une source impulsionnelle (puff)

**Statut.** Note d'expérience exécutant l'étape 6 de l'ordre confirmé de l'[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : porter l'évaluation dirigée, reconstruite à l'étape 4 (`experiences/baseline_uniforme.py`), sur une source impulsionnelle (puff), évaluée sur la grille du cas de référence S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2). Implémentation : [experiences/evaluation_puff.py](../src/jdriftx/experiences/evaluation_puff.py) ; tests : [tests/test_evaluation_puff.py](../tests/test_evaluation_puff.py).

**Date :** 29 octobre 2026. **Suivi :** [issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) (étape 6 sur 6) ; étiquetage héritage/reconstruction/extension conformément au [contrat minimal](47-contrat-minimal-baseline.md) §3.4.

## 1. Objectif et étiquetage

- **Héritage documentaire** : l'évaluation dirigée d'une source impulsionnelle est « annoncée seulement » dans le chapitre « Reduced-Order Modelling of Dispersion » (Brun & Mohammadi, 2008, DOI 10.1007/978-1-4020-8758-5_14). Aucun chiffre de l'ouvrage n'est utilisé comme cible.
- **Reconstruction** : temps dirigé τ par la pseudo-distance de référence uniforme ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.5, `jdriftx.metric`), concentration par la solution fermée du puff du package (`jdriftx.similitude`).
- **Extension** : porte l'évaluation dirigée au puff — première extension conditionnelle du [contrat minimal](47-contrat-minimal-baseline.md) §5, strictement hors périmètre de la baseline continue.

## 2. Méthodologie (quatre étapes)

1. **Temps dirigé** : τ = pseudo-distance uniforme de l'émission (x0, 0) au point (x, y) sous le vent (u, 0) — l'écart transversal n'est pas pénalisé, un point amont reçoit +inf.
2. **Concentration dirigée** : C(τ) au point de mesure, solution fermée du puff gaussien du package (σx = σy = σy(uτ), σz(uτ), sans réflexion au sol).
3. **Maximum temporel** : t_pic = argmax de C(t) sur une grille déterministe à deux niveaux (2 × 256 instants) couvrant ]0, τ] puis resserrée autour du maximum grossier — ce n'est pas le maximum temporel exact.
4. **Écarts** : écart relatif C(τ)/C(t_pic) − 1 (capture du pic) et retard (τ − t_pic)/τ (avance du pic sur le passage).

## 3. Paramètres

| Paramètre | Valeur |
|---|---|
| Masse émise | 1,0 kg |
| Vent uniforme | 3,0 m s⁻¹ |
| Classe de stabilité | C (Briggs rural) |
| Position d'émission x0 | 0 m |
| Altitude de mesure | z_m = 1,5 m (cas S0 figé) |
| Grille de prélèvements | 12 points : arcs 100/200/400/800 m × y ∈ {−50, 0, +50} m |
| Grille temporelle | 2 × 256 instants sur ]0, τ] (déterministe) |

## 4. Résultats

### 4.1 Axe (y = 0)

| Arc (m) | τ (s) | t_pic (s) | Retard (%) | C(τ) (kg m⁻³) | Écart (%) |
|---|---|---|---|---|---|
| 100 | 33,33 | 32,23 | 3,30 | 6,57 × 10⁻⁵ | −4,90 |
| 200 | 66,67 | 64,48 | 3,28 | 8,49 × 10⁻⁶ | −4,88 |
| 400 | 133,33 | 129,07 | 3,19 | 1,11 × 10⁻⁶ | −4,70 |
| 800 | 266,67 | 258,61 | 3,02 | 1,49 × 10⁻⁷ | −4,35 |

### 4.2 Grille complète (12 points)

- **Pire écart : −4,90 %** (arc 100, axe) : l'évaluation dirigée capture au moins **95,1 %** du pic temporel partout sur la grille.
- **Retard maximal : 3,30 %** (arc 100, axe) ; aucun point ne dépasse 5 %.
- **|y| = 50 m, arcs 100–200** : le pic tombe exactement au passage (t_pic = τ, écart nul).
- **|y| = 50 m, arcs 400–800** : retards 1,75 % et 2,67 %, écarts −1,42 % et −3,39 % (< 3,4 %).
- **Symétrie latérale exacte** : les paires ±50 partagent τ, t_pic, concentrations et écart à la précision machine (égalité bit à bit).

## 5. Limites explicites

**Établit** : la cohérence interne du package entre la métrique dirigée, la solution fermée du puff et la recherche déterministe du maximum temporel, sur le cas S0 figé.

**N'établit pas** : une validation physique (cas synthétique) ; le maximum temporel exact du puff (grille déterministe, pas une optimisation continue) ; une physique de l'isotropie longitudinale approchée (σx = σy est portée par la solution fermée du package) ; le traitement des points inaccessibles au-delà de la convention +inf en amont.


### Distinction avec le théorème GZ-1

Le [théorème GZ-1](../site/theorie/navigation-fronts-controllabilite.qmd) étudie un autre modèle : le noyau fondamental 3D isotrope à diffusivité constante \(K\), en espace libre, avec une commande vectorielle \(s\) bornée par la vitesse d'expansion du niveau gaussien. Il démontre une égalité entre un temps minimal de navigation contrôlée \(T_{\mathrm{nav}}\) et un temps de premier contact du front \(T_{\mathrm{front}}\).

La présente expérience ne met pas en œuvre ce problème de contrôle. Elle utilise la pseudo-distance uniforme \(\tau\), la solution paramétrée Briggs de \`concentration_puff\`, puis une recherche discrète du maximum temporel. Elle ne calcule ni \(T_{\mathrm{nav}}\), ni un front de contrôlabilité. La parenté « puff gaussien » ne suffit donc pas à transférer le théorème GZ-1 aux résultats de cette note ; les deux modèles et leurs observables doivent rester séparés.
## 6. Relations au code

| Objet du dépôt | Rôle |
|---|---|
| [experiences/evaluation_puff.py](../src/jdriftx/experiences/evaluation_puff.py) | Module étape 6 : évaluation dirigée, manifeste étiqueté |
| [tests/test_evaluation_puff.py](../tests/test_evaluation_puff.py) | 14 tests GWT : calibration, rejet amont, bande d'écart, retard, symétrie, pic au passage, manifeste, export JSON |
| [similitude.py](../src/jdriftx/similitude.py) | Solution fermée du puff gaussien (σ Briggs) |
| [metric.py](../src/jdriftx/metric.py) | Pseudo-distance uniforme (temps dirigé) |
| [benchmarks/cas.py](../src/jdriftx/benchmarks/cas.py) | Cas S0 figé : grille de 12 points |

**Écarts explicites : aucun** vis-à-vis des notes 47, 48 et 49 ; les statuts figés ne sont pas modifiés.

## Références internes

- [Cas de référence autonome](48-cas-reference-autonome-ecoulement-uniforme.md) ; [contrat minimal de la baseline](47-contrat-minimal-baseline.md) ; [matrice des revendications](49-matrice-revendications-baseline.md)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
