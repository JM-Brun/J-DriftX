# 24 — Classes de stabilité de Pasquill : modèle objet et caractéristiques

**Date** : 26 octobre 2026. **Statut** : document de travail public.

## 1. Objet

Jusqu'ici, les six classes de stabilité de Pasquill étaient représentées dans le code par de simples chaînes `"A"`…`"F"`, avec deux tables `dict` internes (`_BRIGGS_SY`, `_BRIGGS_SZ`) dans `similitude.py` portant les coefficients des lois de Briggs, et un sélecteur de forme `"lin"/"sqrt"/"inv"` sans objet dédié. L'audit du package (docs/22, recommandation P3) avait signalé ce sélecteur comme candidat `Enum`.

Ce document décrit le modèle objet introduit pour rendre ce vocabulaire explicite, documenté et typé, conformément à la charte qualité (CONTRIBUTING.md : structures typées plutôt que `dict` internes ; objets seulement s'ils portent un invariant — ici, l'ensemble clos des classes et leurs caractéristiques).

## 2. Les objets

### `ClasseStabilite` (StrEnum, module `src/jdriftx/stabilite.py`)

Six membres `A` à `F`. C'est un `StrEnum` : chaque membre **est** la lettre (`ClasseStabilite.D == "D"`), donc tout code existant qui passait une chaîne continue de fonctionner. Contrat de chaque membre :

| Propriété | Type | Contenu |
|---|---|---|
| `regime` | `str` | régime de stabilité, de « très instable » (A) à « stable » (F) |
| `conditions_typiques` | `str` | conditions météorologiques typiques d'usage (classification d'origine, Pasquill 1961) |
| `coeff_sigma_y` | `(float, float)` | coefficients (a, d) de la loi Briggs rurale σ_y(x) = a·x/√(1 + d·x) |
| `coeff_sigma_z` | `(FormeSigmaZ, float, float)` | forme et coefficients (b, d) de la loi σ_z |

### `FormeSigmaZ` (StrEnum)

Les trois familles de lois verticales de Briggs (site rural) : `LINEAIRE` (`"lin"`, classes A et B), `RACINE` (`"sqrt"`, C et D), `INVERSE` (`"inv"`, E et F). Les valeurs reprennent les identifiants du sélecteur historique de `similitude.py`.

## 3. Caractéristiques documentées par classe

| Classe | Régime | Conditions typiques (Pasquill 1961) | σ_z (Briggs, site rural) |
|---|---|---|---|
| A | très instable | jour, insolation forte et vent faible (< 2 m/s) ; convection vigoureuse | linéaire : 0,20·x |
| B | modérément instable | jour, insolation modérée ou vent de 2 à 3 m/s | linéaire : 0,12·x |
| C | faiblement instable | jour nuageux ou insolation faible, vent de 3 à 5 m/s | racine : 0,08·x/√(1 + 0,0002·x) |
| D | neutre | couvert dense jour et nuit, ou vent > 6 m/s ; classe de référence | racine : 0,06·x/√(1 + 0,0015·x) |
| E | faiblement stable | nuit, vent de 3 à 5 m/s ou ciel partiellement couvert | inverse : 0,03·x/(1 + 0,0003·x) |
| F | stable | nuit claire et vent faible (< 3 m/s) ; inversion nocturne | inverse : 0,016·x/(1 + 0,0003·x) |

Loi σ_y commune à toutes les classes : a·x/√(1 + 0,0001·x), avec a = 0,22 (A), 0,16 (B), 0,11 (C), 0,08 (D), 0,06 (E), 0,04 (F).

Les conditions typiques décrivent la classification d'origine (Pasquill 1961 ; courbes de Gifford ; formules de Briggs 1973, reprises par Martin 1976) : ce sont des repères d'usage, **pas un diagnostic automatique** de la stabilité à partir de mesures. Aucun module ne détermine la classe depuis des données météorologiques.

## 4. Source unique de vérité et non-régression

`similitude.py` ne définit plus ses propres tables : `sigma_y` et `sigma_z` lisent leurs coefficients dans l'objet `ClasseStabilite`. Points de non-régression :

- expressions numériques inchangées (mêmes formules, même ordre d'opérations) ;
- message d'erreur d'une classe inconnue inchangé (`Classe de stabilite inconnue : ...`) ;
- `CLASSES` conserve le même contenu (tuple des six lettres) pour la compatibilité.

Garde : `tests/test_stabilite.py` épingle les coefficients exacts par classe (σ_y et σ_z), les formes par famille, les régimes, les identifiants de `FormeSigmaZ`, l'équivalence enum/lettre dans `sigma_y`/`sigma_z`, et le message d'erreur historique. Les tests existants de `similitude` (croissance des σ, bilans de masse, etc.) couvrent le comportement numérique inchangé.

## 5. Limites

- Les lois documentées sont celles du **site rural** ; aucune variante urbaine n'est fournie.
- Les conditions typiques sont indicatives (classification d'origine) ; le choix opérationnel de la classe reste une décision de modélisation (paramètre de segment, hypothèse H5).
- L'objet ne porte **aucune physique supplémentaire** : pas de dépendance en la rugosité, l'heure ou la saison.
- Références citées en prose (Pasquill 1961 ; Briggs 1973), sans entrée bibliographique ajoutée, conformément à la discipline anti-hallucination de docs/15.
