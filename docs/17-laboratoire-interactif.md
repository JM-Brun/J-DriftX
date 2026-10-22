# Laboratoire interactif J-DriftX — proposition de conception

> Statut : prototype pédagogique et numérique en développement. Aucune validation physique ou applicative n'est revendiquée.

## 1. Objectif et séparation des usages

Le laboratoire doit distinguer **exploration** (comprendre le comportement d'une équation dans un cas contrôlé) et **vérification numérique** (comparer un calcul à une solution connue, mesurer l'erreur et conserver les paramètres). Une visualisation n'est ni une preuve mathématique ni une validation empirique.

## 2. Architecture

- **Cœur scientifique** : fonctions Python pures, testées et indépendantes de l'interface.
- **Visualisation** : Plotly pour les courbes, champs et surfaces interactives.
- **Interface** : applications Streamlit optionnelles.
- **Documentation** : pages Quarto qui explicitent les équations, hypothèses, unités et limites.
- **Vérification** : solutions analytiques et propriétés testables, cas limites, erreurs et tests de non-régression.

Streamlit et Plotly sont optionnels ; ils ne deviennent pas des dépendances obligatoires du cœur de calcul.

## 3. Expériences disponibles dans la branche

### Champs et reliefs synthétiques

L'application `apps/interactive_lab.py` propose des champs uniforme, cisaillement et radial, plus des reliefs plats, gaussiens et en crête. Les dérivées spatiales et pentes sont estimées sur une grille. Ces objets sont sans dimension et ne simulent pas le vent, la turbulence ni la dispersion. Aucun couplage relief–écoulement n'est supposé.

### Trajectoires de particules dans un champ prescrit

Le module `src/jdriftx/trajectories.py` intègre le système cinématique

\[
\frac{dx}{dt}=u(x,y,t),\qquad \frac{dy}{dt}=v(x,y,t)
\]

par Euler explicite ou Runge–Kutta classique d'ordre 4 (RK4). Le dernier pas est raccourci si nécessaire pour atteindre exactement la fin de l'intervalle. Les tests couvrent le champ constant, où les deux méthodes sont exactes à l'arrondi près, et un champ rotationnel avec solution analytique, où RK4 doit présenter une erreur finale inférieure à Euler pour le pas de test.

**Limites :** la trajectoire est celle d'un point advecté par le champ prescrit. Elle ne modélise pas l'inertie des gouttelettes, la turbulence stochastique, le dépôt, la sédimentation ni le rétro-couplage des particules sur l'écoulement. L'exemple rotationnel est un cas de vérification mathématique, pas un champ de vent réaliste.

### Référence analytique d'advection-diffusion 1D

Le module `src/jdriftx/advection_diffusion.py` fournit la solution gaussienne de

\[
\frac{\partial c}{\partial t}
+u\frac{\partial c}{\partial x}
=K\frac{\partial^2 c}{\partial x^2},
\qquad K\geq 0
\]

sur la droite réelle, pour une vitesse constante, une diffusivité constante et un profil initial gaussien d'écart-type \(\sigma_0>0\). Le centre évolue comme \(x_c(t)=x_0+ut\), et la variance comme \(\sigma^2(t)=\sigma_0^2+2Kt\). L'intégrale de la concentration sur la droite réelle est la masse \(M\).

Les tests vérifient le cas sans diffusion, l'intégrale numérique de la masse sur un domaine assez large et la variance théorique. L'intégrale sur un intervalle fini peut être inférieure à \(M\) lorsque des queues gaussiennes sortent du domaine ; ce n'est pas en soi une violation de la conservation sur la droite réelle.

**Limites :** ce cas n'inclut ni source continue, ni réaction, ni dépôt, ni conditions aux limites finies, ni vitesse ou diffusivité variables. Il ne constitue pas une prévision atmosphérique.

## 4. Expériences et critères de vérification

L'application `apps/scientific_validation.py` expose les deux expériences précédentes et compare visuellement Euler/RK4 à la trajectoire exacte, puis le profil initial au profil advecté-diffusé. Elle affiche l'erreur de position finale, une courbe de convergence en fonction du pas de temps et la masse intégrée sur le domaine tracé.

Pour toute nouvelle formulation :
- comparer à une solution analytique lorsque disponible ;
- préciser les unités, conditions initiales, conditions aux limites et domaine de validité ;
- distinguer erreur absolue et relative, et signaler les zones où l'erreur relative est mal conditionnée ;
- vérifier les cas limites et invariants uniquement sous les hypothèses qui les garantissent ;
- tester les paramètres invalides et conserver les résultats négatifs ;
- séparer erreur de discrétisation, erreur de modèle et incertitude des données.

Les tests unitaires démontrent que certaines propriétés du code tiennent sur des cas précis ; ils ne démontrent pas que le modèle représente fidèlement un phénomène physique.

## 5. Lancer les applications

Avec Python 3.12 et uv, depuis la racine du dépôt :

```bash
uv sync --group app
uv run streamlit run apps/interactive_lab.py
```

Pour les expériences de trajectoire et d'advection-diffusion :

```bash
uv run streamlit run apps/scientific_validation.py
```

## 6. Publication et intégration dans Quarto

Le site GitHub Pages est statique : Python exécuté au rendu Quarto produit des sorties, mais ne maintient pas un noyau Python actif dans le navigateur.

| Option | Atout | Contrainte |
|---|---|---|
| Figures Plotly dans Quarto | Zoom et survol des données calculées | Pas de recalcul Python arbitraire côté serveur |
| Streamlit par iframe | Interface Python interactive complète via serveur distant | Hébergement, maintenance, disponibilité et test mobile/intégration |
| Quarto + Shiny for Python | Callbacks Python côté serveur | Nécessite un serveur ; GitHub Pages seul ne suffit pas |
| JavaScript/Observable | Interaction statique native | La logique doit être écrite en JavaScript ou portée dans un runtime navigateur |

**Recommandation :** garder un seul cœur de calcul Python ; publier des figures Plotly dans les pages pour les cas de référence ; déployer Streamlit séparément seulement si une interaction distante est souhaitée. Ne pas ajouter d'iframe avant de disposer d'une URL réellement déployée et vérifiée. La documentation doit rester utile même si le service interactif est indisponible.

## 7. Convergence spatiale et temporelle

L'application `apps/convergence_lab.py` introduit un cas de vérification distinct : advection-diffusion 1D périodique d'une sinusoïde. Elle utilise un solveur numérique par différences finies centrées et RK4, séparé de la solution analytique

\[
c(x,t)=\bar c+A e^{-K(2\pi/L)^2t}\sin\left(\frac{2\pi}{L}(x-ut)\right).
\]

Le cas est périodique sur une longueur $L$, avec vitesse $u$ et diffusivité $K$ constantes. L'interface affiche les erreurs $L^2$ et maximale, la conservation de la moyenne et deux diagnostics :

- **Convergence spatiale** : raffinement du nombre de cellules ; le pas de temps est réduit comme $\Delta x^2$ pour minimiser l'influence temporelle.
- **Convergence temporelle** : grille fixe, comparaison à une solution numérique calculée avec le même opérateur spatial et un pas temporel beaucoup plus fin.

Le code vérifie la stabilité linéaire du pas choisi pour l'opérateur discret. Les tests automatisés vérifient l'accord avec la solution analytique, la conservation de la moyenne, la diminution des erreurs avec le raffinement et le rejet d'un pas instable. La pente observée reste un diagnostic empirique : la référence temporelle fine est approchée et les résultats dépendent du régime d'erreur et de l'arrondi.

Lancer :

```bash
uv run streamlit run apps/convergence_lab.py
```

Ce cas périodique lisse ne représente pas des conditions aux limites atmosphériques, une source localisée, des coefficients variables ou la dynamique des gouttelettes.

## 8. Hors périmètre

- ingestion de données météorologiques ou topographiques réelles ;
- simulation CFD ou solveur général d'EDP ;
- assimilation, identification de source ou entraînement ML ;
- reproduction affirmée de l'intégralité du Drift-X historique ;
- affirmation de validité applicative ou réglementaire sans données, protocole et validation appropriés.

Le laboratoire pédagogique peut soutenir la compréhension et la vérification de composants mathématiques ; il ne suffit pas à démontrer l'utilité applicative ni la validité scientifique de J-DriftX.
