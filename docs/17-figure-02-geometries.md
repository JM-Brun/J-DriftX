# Figure 2 — Distance euclidienne et coût de migration dirigé

![Schéma original comparant la distance euclidienne et le coût de migration dans un champ uniforme](../site/images/figure-02-geometries.svg)

## Statut

**R0/R1 — schéma explicatif dans un champ uniforme 2D.** Cette illustration est créée pour J-DriftX ; elle ne copie pas l'image Springer et ne constitue pas une reproduction quantitative des données historiques.

La distance euclidienne est symétrique. Le coût dirigé dépend du sens du vent : pour le cas uniforme retenu, seule la projection longitudinale positive est facturée et la séparation transversale est ignorée. Selon la convention documentée par `pseudo_distance_uniforme`, une cible située en amont reçoit un coût infini. Le coût peut aussi être nul pour deux points distincts partageant la même coordonnée longitudinale : il ne s'agit donc pas d'une métrique au sens strict.

Les valeurs affichées par le schéma (distance euclidienne, coût dirigé aval et coût amont infini) sont produites par la tranche verticale « champ uniforme » du module `jdriftx.experiences.uniforme` : une configuration typée (`ScenarioUniforme`, dont le champ `ChampUniforme` porte l'invariant « vecteur fini et non nul »), résolue par `resoudre_scenario` via `pseudo_distance_uniforme`, avec résultats immuables (`ResultatDirige`) et manifeste (`ManifesteScenario`). La figure consomme ces résultats calculés : elle ne duplique pas la formule et ne peut pas diverger silencieusement de l'implémentation testée. Le scénario jouet (vent uniforme selon +x, cible en aval avec un écart transversal) est `SCENARIO_DEFAUT`.

La formule schématisée est limitée à un champ constant non nul :

\[
\tau(A,B)=\begin{cases}
\frac{(B-A)\cdot\hat{u}}{\|u\|}, & (B-A)\cdot\hat{u}\geq 0,\\
+\infty, & (B-A)\cdot\hat{u}<0.
\end{cases}
\]

Ici \(\hat{u}=u/\|u\|\). Les unités sont cohérentes si les coordonnées sont en mètres et la vitesse en mètres par seconde ; le résultat est alors en secondes. La formule ne modélise ni les caractéristiques d'un champ variable, ni une projection sur des trajectoires courbes, ni la dispersion/diffusion.

## Génération, manifeste et tests

Le SVG est généré par `jdriftx.figures.figure_02.render_figure_02_svg`, sans dépendance de rendu externe ; les coûts affichés proviennent de `resoudre_scenario(SCENARIO_DEFAUT)` (module `jdriftx.experiences.uniforme`). Le manifeste de l'expérience est assemblé par `construire_manifeste` : identifiant `jdriftx-uniforme-001`, niveau R1, source (DOI du chapitre), hypothèses, limites, version du package et commande de reproduction ; son export JSON est confiné à la frontière (`ManifesteScenario.vers_dict`). Les tests vérifient la validation des invariants (vent nul, composante non finie, point mal formé), les valeurs analytiques du scénario jouet (τ(A, B) = 150 s, τ(B, A) = +∞, dE ≈ 307 m, écart transversal 65 m), l'immuabilité des résultats, le manifeste, la stabilité du générateur SVG et la cohérence des valeurs affichées avec l'implémentation partagée. Les nouveaux tests suivent le format Given/When/Then de la charte qualité. Pour régénérer localement :

```bash
uv run python -c 'from pathlib import Path; from jdriftx.figures.figure_02 import render_figure_02_svg; Path("site/images/figure-02-geometries.svg").write_text(render_figure_02_svg(), encoding="utf-8")'
uv run pytest tests/test_experience_uniforme.py tests/test_figure_02.py
```

La copie versionnée du SVG doit rester strictement synchronisée avec la sortie du générateur. Ce livrable ne valide ni l'utilité applicative G0-A, ni la formulation générale historique.

## Référence

Brun, J.-M. & Mohammadi, B. (2008), “Reduced-Order Modelling of Dispersion”, chapitre 14, p. 253, dans *Partial Differential Equations: Modelling and Numerical Simulation*, https://doi.org/10.1007/978-1-4020-8758-5_14.
