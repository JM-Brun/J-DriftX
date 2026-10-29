# 54 — EDP transitoire du puff (marche en temps de la marginale transverse)

**Statut.** Note d'expérience ouvrant la route EDP transitoire de la source impulsionnelle de l'[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : la marginale transverse Q(y, z, t) du puff est marchée en temps par un schéma FTCS, route indépendante de la solution fermée, comparée à celle-ci sur la grille du cas de référence S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2). Suite directe de l'évaluation dirigée ([note 53](53-evaluation-puff-source-impulsionnelle.md)). Implémentation : [experiences/transitoire_puff.py](../src/jdriftx/experiences/transitoire_puff.py) ; tests : [tests/test_transitoire_puff.py](../tests/test_transitoire_puff.py).

**Date :** 29 octobre 2026. **Suivi :** [issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) ; étiquetage héritage/reconstruction/extension conformément au [contrat minimal](47-contrat-minimal-baseline.md) §3.4.

## 1. Objectif et étiquetage

- **Héritage documentaire** : aucune source historique — l'EDP transitoire du puff est la suite directe de l'étape 6 (note 53). Aucun chiffre de l'ouvrage de 2008 n'est utilisé comme cible.
- **Reconstruction** : marche explicite FTCS en temps de la marginale transverse ∂Q/∂t = Ky ∂²Q/∂y² + Kz ∂²Q/∂z², avec K = (u/2)·dσ²/dx évalué à la distance parcourue d = u·t ; entrée fermée au premier instant de passage, miroir au sol, Dirichlet aux bords ; structure longitudinale analytique (carte travel-time de la note 37, isotropie σx = σy du noyau fermé).
- **Extension** : seconde extension conditionnelle du [contrat minimal](47-contrat-minimal-baseline.md) §5 — la source impulsionnelle (note 53) reçoit sa route EDP transitoire, hors périmètre de la baseline continue.

## 2. Méthodologie (quatre étapes)

1. **Marginale transverse** : Q(y, z, t) = ∫ C(x, y, z, t) dx vérifie l'EDP de diffusion 2D en temps (le vent uniforme transporte, la diffusion transverse étale) ; K = (u/2)·dσ²/dx à la distance parcourue d = u·t.
2. **Entrée fermée** : au premier instant de passage (t_e = 100/u), la marginale analytique du package est posée sur la grille ; bords latéraux et sommet mis à zéro.
3. **Marche FTCS** : pas de temps t_e/2^k (k = 10 sur la grille fine, nombre de Fourier 0,235 au dernier passage ≤ 1/3) ; sol miroir (Neumann — exact car le noyau du puff est pair en z) ; instantanés prélevés aux instants de passage (pas 1024/3072/7168).
4. **Comparaison dirigée** : C(x, y, z, t) = Q(y, z, t)·exp(−(x − x0 − u·t)²/2σx²)/(√(2π)σx), σx = σy ; les points du cas S0 sont aux arcs, où le facteur gaussien longitudinal est évalué au passage.

## 3. Paramètres

| Paramètre | Valeur |
|---|---|
| Puff | masse 1,0 kg, vent 3,0 m s⁻¹, classe C, x0 = 0 (note 53) |
| Grille fine | pas 2,5 m / 2,0 m, fenêtre 340 m / 240 m (273 × 121 nœuds) |
| Grille grossière | pas 5,0 m / 4,0 m, fenêtre 340 m / 240 m (137 × 61 nœuds) |
| Pas de temps fin | (100/3)/1024 s ≈ 3,26 × 10⁻² s, 7168 pas |
| Pas de temps grossier | (100/3)/256 s ≈ 1,30 × 10⁻¹ s, 1792 pas |
| Instants de passage | t = x/u : 33,3 / 66,7 / 133,3 / 266,7 s (arcs 100/200/400/800 m) |
| Grille de prélèvements | 12 points du cas S0 figé ([note 48](48-cas-reference-autonome-ecoulement-uniforme.md) §2.2) |

## 4. Résultats

### 4.1 Grille fine

- **NMSE ≈ 3,4 × 10⁻⁵** (< 10⁻⁴), **FAC2 = 1,0**.
- **Écart relatif maximal ≈ 5,9 × 10⁻³** (arc 100, entrée partagée : pur effet de l'interpolation bilinéaire en z) ; arcs 200–800 : écarts ≤ 6,5 × 10⁻⁴.
- **Écarts de masse** vs marginale analytique sur la même grille : 0 à l'entrée, ~10⁻¹⁶ à 200 s, ~2 × 10⁻¹⁴ à 400 s, −1,1 × 10⁻⁴ à 800 s (troncature de la fenêtre 4σ).

### 4.2 Grille grossière (contrôle de convergence)

- **NMSE ≈ 7,5 × 10⁻⁴** : environ **22 fois** la grille fine — le même taux de convergence que l'étape 5 ; écart relatif maximal ≈ 2,8 × 10⁻².

## 5. Limites explicites

**Établit** : la cohérence interne du package entre la marche FTCS en temps de la marginale transverse et la solution fermée du puff, sur le cas S0 figé.

**N'établit pas** : une validation physique (cas synthétique) ; une résolution numérique de la structure longitudinale (analytique : carte travel-time + isotropie du noyau fermé) ; le traitement du noyau symétrique en z autour du sol (moitié de la masse du noyau fermé formellement sous le sol ; la grille porte la demi-colonne miroir et les écarts de masse comparent la marginale analytique sur la même grille) ; une physique de l'isotropie σx = σy (portée par la solution fermée du package).

## 6. Relations au code

| Objet du dépôt | Rôle |
|---|---|
| [experiences/transitoire_puff.py](../src/jdriftx/experiences/transitoire_puff.py) | Module : marche FTCS en temps, routes mesurées séparément, manifeste étiqueté |
| [tests/test_transitoire_puff.py](../tests/test_transitoire_puff.py) | 17 tests GWT : calibration, entrée partagée, seuils, convergence, rejets, temps dirigé, coûts, manifeste, export JSON |
| [experiences/reference_independante.py](../src/jdriftx/experiences/reference_independante.py) | Grille EDP, modèle de diffusion injectable, seuil de Fourier (étape 5) |
| [experiences/evaluation_puff.py](../src/jdriftx/experiences/evaluation_puff.py) | Source impulsionnelle et temps dirigé (étape 6) |
| [similitude.py](../src/jdriftx/similitude.py) | Solution fermée du puff et σ de Briggs |

**Écarts explicites : aucun** vis-à-vis des notes 47, 48, 49 et 53 ; les statuts figés ne sont pas modifiés.

## Références internes

- [Évaluation dirigée du puff](53-evaluation-puff-source-impulsionnelle.md) ; [comparaison à référence indépendante](51-reference-independante-cas-s0.md) ; [cas de référence autonome](48-cas-reference-autonome-ecoulement-uniforme.md)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
