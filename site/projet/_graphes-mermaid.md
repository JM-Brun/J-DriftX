<!-- Ne pas éditer à la main : fichier généré par -->
<!-- src/jdriftx.graphe_connaissances.py depuis site/data/graphe-connaissances.toml -->

## Légende

<span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#bfe0ff;vertical-align:baseline"></span> Hypothèse · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#ddd0f0;vertical-align:baseline"></span> Niveau de modélisation · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#c9ecd9;vertical-align:baseline"></span> Concept · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#ffd9b3;vertical-align:baseline"></span> Propriété (visée ou testée) · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#d7f0a1;vertical-align:baseline"></span> Module de code · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#e9ecef;vertical-align:baseline"></span> Test (CI) · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#fff1a6;vertical-align:baseline"></span> Jeu de données candidat · <span style="display:inline-block;width:0.85em;height:0.85em;border:1px solid #495057;border-radius:3px;background:#e6dccb;vertical-align:baseline"></span> Référence bibliographique

## Théorie et hypothèses

La chaîne conceptuelle N0-N6, les hypothèses H1-H8 qui la contraignent et les objets mathématiques que chaque hypothèse fait exister. Le détail de chaque hypothèse (justification, limite, ancrage dans le code) reste dans le catalogue des hypothèses.

```{mermaid}
graph LR
  subgraph niv["Niveaux de modélisation (N0-N6)"]
    n0["N0 — contexte physique"]::niveau
    n1["N1 — équations aux dérivées partielles"]::niveau
    n2["N2 — discrétisation et maillage"]::niveau
    n3["N3 — solveurs et schémas numériques"]::niveau
    n4["N4 — modèles réduits"]::niveau
    n5["N5 — expériences et données de terrain"]::niveau
    n6["N6 — calibration et aide à la décision"]::niveau
  end
  subgraph hyp["Hypothèses (H1-H8)"]
    h1["H1 — scalaire passif"]::hypothese
    h2["H2 — régime auto-similaire établi"]::hypothese
    h3["H3 — quasi-stationnarité du vent"]::hypothese
    h4["H4 — transport advectif dominant dans la métrique"]::hypothese
    h5["H5 — homogénéité horizontale par morceaux"]::hypothese
    h6["H6 — domaine de validité local du modèle réduit"]::hypothese
    h7["H7 — données d'assimilation représentatives"]::hypothese
    h8["H8 — superposition des sources"]::hypothese
  end
  subgraph cpt["Concepts"]
    c_transport["Équation de transport (advection-diffusion)"]::concept
    c_champ["Champ de vent stationnaire"]::concept
    c_courant["Ligne de courant et caractéristique"]::concept
    c_fcourant["Fonction de courant"]::concept
    c_tau["Temps de transport"]::concept
    c_polyligne["Coût dirigé sur polyligne"]::concept
    c_tpa["Temps de première arrivée (cas 1D exact)"]::concept
    c_pdist["Pseudo-distance dirigée (référence uniforme)"]::concept
    c_panache["Panache gaussien (similitude)"]::concept
    c_stabilite["Classes de Pasquill et lois de Briggs"]::concept
    c_multiniveaux["Champ multi-niveaux historique (non reconstruit)"]::concept
    c_reduction["Modèle approché v(p) (réduction a priori)"]::concept
    c_assimilation["Assimilation et calibration"]::concept
  end
  n0 -->|"alimente"| n1
  n1 -->|"alimente"| n2
  n2 -->|"alimente"| n3
  n3 -->|"alimente"| n4
  n4 -->|"alimente"| n5
  n5 -->|"alimente"| n6
  h1 -->|"s'applique à"| n4
  h1 -->|"s'applique à"| n5
  h2 -->|"s'applique à"| n4
  h3 -->|"s'applique à"| n1
  h3 -->|"s'applique à"| n3
  h4 -->|"s'applique à"| n3
  h5 -->|"s'applique à"| n0
  h5 -->|"s'applique à"| n3
  h6 -->|"s'applique à"| n4
  h7 -->|"s'applique à"| n6
  h8 -->|"s'applique à"| n5
  h1 -->|"traduite en"| c_transport
  h2 -->|"traduite en"| c_panache
  h3 -->|"traduite en"| c_champ
  h4 -->|"traduite en"| c_tau
  h5 -->|"traduite en"| c_polyligne
  h6 -->|"traduite en"| c_reduction
  h7 -->|"traduite en"| c_assimilation
  h8 -->|"traduite en"| c_panache
  h1 -->|"fonde"| h8
  c_fcourant -->|"construit"| c_champ
  c_courant -->|"dépend de"| c_champ
  c_tau -->|"dépend de"| c_courant
  c_transport -->|"dépend de"| c_champ
  c_panache -->|"dépend de"| c_transport
  c_panache -->|"dépend de"| c_stabilite
  c_assimilation -->|"utilise"| c_reduction
  c_multiniveaux -->|"construit"| c_champ
  classDef hypothese fill:#bfe0ff,stroke:#495057,color:#212529;
  classDef niveau fill:#ddd0f0,stroke:#495057,color:#212529;
  classDef concept fill:#c9ecd9,stroke:#495057,color:#212529;
```

**Nœuds et destinations**

| Nœud | Type | Où approfondir |
|---|---|---|
| N0 — contexte physique | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N1 — équations aux dérivées partielles | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N2 — discrétisation et maillage | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N3 — solveurs et schémas numériques | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N4 — modèles réduits | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N5 — expériences et données de terrain | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N6 — calibration et aide à la décision | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| H1 — scalaire passif | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H2 — régime auto-similaire établi | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H3 — quasi-stationnarité du vent | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H4 — transport advectif dominant dans la métrique | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H5 — homogénéité horizontale par morceaux | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H6 — domaine de validité local du modèle réduit | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H7 — données d'assimilation représentatives | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| H8 — superposition des sources | Hypothèse | [hypotheses/catalogue.qmd](../hypotheses/catalogue.qmd) |
| Équation de transport (advection-diffusion) | Concept | [theorie/modele-direct.qmd](../theorie/modele-direct.qmd) |
| Champ de vent stationnaire | Concept | [glossaire.qmd](../glossaire.qmd) |
| Ligne de courant et caractéristique | Concept | [glossaire.qmd](../glossaire.qmd) |
| Fonction de courant | Concept | [glossaire.qmd](../glossaire.qmd) |
| Temps de transport | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Coût dirigé sur polyligne | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Temps de première arrivée (cas 1D exact) | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Pseudo-distance dirigée (référence uniforme) | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Panache gaussien (similitude) | Concept | [theorie/similitude.qmd](../theorie/similitude.qmd) |
| Classes de Pasquill et lois de Briggs | Concept | [glossaire.qmd](../glossaire.qmd) |
| Champ multi-niveaux historique (non reconstruit) | Concept | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| Modèle approché v(p) (réduction a priori) | Concept | [theorie/reduction-a-priori.qmd](../theorie/reduction-a-priori.qmd) |
| Assimilation et calibration | Concept | [theorie/assimilation-identification.qmd](../theorie/assimilation-identification.qmd) |

## Code, propriétés et preuves

Les modules du paquet, les concepts qu'ils implémentent, les tests de la CI et les propriétés qu'ils établissent, dans les limites documentées sur la page Contraintes physiques. Un concept sans arête « implémenté par » — le champ multi-niveaux historique — signale une capacité non reconstruite, pas un lien manquant.

```{mermaid}
graph TD
  subgraph prm["Primitives de la métrique"]
    metric["metric.py"]::module
    c_polyligne["Coût dirigé sur polyligne"]::concept
    c_tpa["Temps de première arrivée (cas 1D exact)"]::concept
    c_pdist["Pseudo-distance dirigée (référence uniforme)"]::concept
  end
  subgraph chp["Champs, expériences et rendu"]
    champ_analytique["champ_analytique.py"]::module
    experiences_uniforme["experiences/uniforme.py"]::module
    experiences_reconstruction_vent["experiences/reconstruction_vent.py"]::module
    experiences_cas_synthetiques["experiences/cas_synthetiques.py"]::module
    experiences_superposition_sources["experiences/superposition_sources.py"]::module
    experiences_relief["experiences/relief.py"]::module
    experiences_modele_reduit_edp["experiences/modele_reduit_edp.py"]::module
    experiences_identification_source["experiences/identification_source.py"]::module
    fields["fields.py"]::module
    terrain["terrain.py"]::module
    trajectories["trajectories.py"]::module
    figures_figure_01["figures/figure_01.py"]::module
    figures_figure_02["figures/figure_02.py"]::module
    figures_figure_03["figures/figure_03.py"]::module
    figures_figure_04["figures/figure_04.py"]::module
    figures_figure_05["figures/figure_05.py"]::module
    figures_figure_06["figures/figure_06.py"]::module
    figures_wind_field_explorer["figures/wind_field_explorer.py"]::module
    c_fcourant["Fonction de courant"]::concept
    c_champ["Champ de vent stationnaire"]::concept
    c_courant["Ligne de courant et caractéristique"]::concept
    c_assimilation["Assimilation et calibration"]::concept
    c_multiniveaux["Champ multi-niveaux historique (non reconstruit)"]::concept
    n0["N0 — contexte physique"]::niveau
  end
  subgraph sol["Socle gaussien"]
    similitude["similitude.py"]::module
    similitude_objets["similitude_objets.py"]::module
    stabilite["stabilite.py"]::module
    source["source.py"]::module
    c_panache["Panache gaussien (similitude)"]::concept
    c_stabilite["Classes de Pasquill et lois de Briggs"]::concept
  end
  subgraph ctr["Contrats d'interface (docs/42)"]
    contrats["contrats.py"]::module
  end
  subgraph rfs["Solveurs de référence"]
    periodic_transport["periodic_transport.py"]::module
    advection_diffusion["advection_diffusion.py"]::module
    c_transport["Équation de transport (advection-diffusion)"]::concept
  end
  subgraph carte["Carte des connaissances"]
    graphe_connaissances["graphe_connaissances.py"]::module
    extraction_graphe["extraction_graphe.py"]::module
    diagnostic_graphe["diagnostic_graphe.py"]::module
    t_graphe["test_graphe_connaissances.py"]::test
    t_extraction["test_extraction_graphe.py"]::test
    t_diagnostic["test_diagnostic_graphe.py"]::test
  end
  subgraph prp["Propriétés et tests"]
    p_positivite["Positivité (famille gaussienne)"]::propriete
    p_superposition["Superposition et linéarité en débit"]::propriete
    p_conservation["Bilan de masse (famille gaussienne)"]::propriete
    p_divergence["Divergence nulle (champs analytiques)"]::propriete
    p_nonsym["Non-symétrie (métrique dirigée)"]::propriete
    p_adjoint["Adjoint : gradient exact (référence uniforme et cas 1D)"]::propriete
    constraints["constraints.py"]::module
    t_metric["test_metric.py"]::test
    t_similitude["test_similitude.py"]::test
    t_constraints["test_constraints.py"]::test
    t_champ["test_champ_analytique.py"]::test
    t_recon["test_reconstruction_vent.py"]::test
    t_uniforme["test_experience_uniforme.py"]::test
    t_advection["test_advection_diffusion.py"]::test
    t_fields["test_fields.py"]::test
    t_periodic["test_periodic_transport.py"]::test
    t_stabilite["test_stabilite.py"]::test
    t_terrain["test_terrain.py"]::test
    t_trajectories["test_trajectories.py"]::test
    t_figure_01["test_figure_01.py"]::test
    t_figure_02["test_figure_02.py"]::test
    t_superposition["test_superposition_sources.py"]::test
    t_figure_04["test_figure_04.py"]::test
    t_relief["test_relief.py"]::test
    t_figure_05["test_figure_05.py"]::test
    t_modele_reduit_edp["test_modele_reduit_edp.py"]::test
    t_figure_03["test_figure_03.py"]::test
    t_identification["test_identification_source.py"]::test
    t_figure_06["test_figure_06.py"]::test
    t_wind_field["test_wind_field_explorer.py"]::test
    t_interactif["test_interactive_wind_page.py"]::test
    t_cas_synthetiques["test_cas_synthetiques.py"]::test
  end
  subgraph ben["Benchmarks de référence"]
    benchmarks_cas["benchmarks/cas.py"]::module
    benchmarks_metriques["benchmarks/metriques.py"]::module
    benchmarks_reference["benchmarks/reference.py"]::module
    t_benchmarks["test_benchmarks_reference.py"]::test
  end
  c_fcourant -->|"construit"| c_champ
  c_courant -->|"dépend de"| c_champ
  c_transport -->|"dépend de"| c_champ
  c_panache -->|"dépend de"| c_transport
  c_panache -->|"dépend de"| c_stabilite
  c_multiniveaux -->|"construit"| c_champ
  c_polyligne -->|"implémenté par"| metric
  c_tpa -->|"implémenté par"| metric
  c_pdist -->|"implémenté par"| metric
  c_fcourant -->|"implémenté par"| champ_analytique
  c_champ -->|"implémenté par"| champ_analytique
  c_champ -->|"implémenté par"| experiences_uniforme
  c_panache -->|"implémenté par"| similitude
  c_stabilite -->|"implémenté par"| stabilite
  c_courant -->|"implémenté par"| trajectories
  similitude -->|"utilise"| stabilite
  c_multiniveaux -->|"non couvert par"| p_divergence
  experiences_uniforme -->|"utilise"| c_pdist
  experiences_reconstruction_vent -->|"utilise"| c_fcourant
  figures_figure_01 -->|"utilise"| experiences_reconstruction_vent
  figures_figure_02 -->|"utilise"| experiences_uniforme
  experiences_superposition_sources -->|"utilise"| c_fcourant
  figures_figure_04 -->|"utilise"| experiences_superposition_sources
  experiences_relief -->|"utilise"| c_panache
  experiences_relief -->|"utilise"| terrain
  figures_figure_05 -->|"utilise"| experiences_relief
  experiences_modele_reduit_edp -->|"utilise"| c_panache
  experiences_modele_reduit_edp -->|"utilise"| c_transport
  figures_figure_03 -->|"utilise"| experiences_modele_reduit_edp
  experiences_identification_source -->|"utilise"| c_panache
  experiences_identification_source -->|"utilise"| c_assimilation
  figures_figure_06 -->|"utilise"| experiences_identification_source
  figures_wind_field_explorer -->|"utilise"| fields
  fields -->|"contexte"| c_champ
  terrain -->|"contexte"| n0
  periodic_transport -->|"contexte"| c_transport
  advection_diffusion -->|"contexte"| c_transport
  constraints -->|"teste"| p_positivite
  constraints -->|"teste"| p_superposition
  p_positivite -->|"testée par"| t_similitude
  p_positivite -->|"testée par"| t_constraints
  p_superposition -->|"testée par"| t_constraints
  p_superposition -->|"testée par"| t_similitude
  p_conservation -->|"testée par"| t_similitude
  p_divergence -->|"testée par"| t_champ
  p_divergence -->|"testée par"| t_recon
  p_nonsym -->|"testée par"| t_metric
  p_adjoint -->|"testée par"| t_metric
  t_metric -->|"couvre"| metric
  t_similitude -->|"couvre"| similitude
  t_constraints -->|"couvre"| constraints
  t_champ -->|"couvre"| champ_analytique
  t_recon -->|"couvre"| experiences_reconstruction_vent
  t_uniforme -->|"couvre"| experiences_uniforme
  t_advection -->|"couvre"| advection_diffusion
  t_fields -->|"couvre"| fields
  t_periodic -->|"couvre"| periodic_transport
  t_stabilite -->|"couvre"| stabilite
  t_terrain -->|"couvre"| terrain
  t_trajectories -->|"couvre"| trajectories
  t_figure_01 -->|"couvre"| figures_figure_01
  t_figure_02 -->|"couvre"| figures_figure_02
  t_superposition -->|"couvre"| experiences_superposition_sources
  t_figure_04 -->|"couvre"| figures_figure_04
  t_relief -->|"couvre"| experiences_relief
  t_figure_05 -->|"couvre"| figures_figure_05
  t_modele_reduit_edp -->|"couvre"| experiences_modele_reduit_edp
  t_figure_03 -->|"couvre"| figures_figure_03
  t_identification -->|"couvre"| experiences_identification_source
  t_figure_06 -->|"couvre"| figures_figure_06
  t_wind_field -->|"couvre"| figures_wind_field_explorer
  t_interactif -->|"couvre"| figures_wind_field_explorer
  t_graphe -->|"couvre"| graphe_connaissances
  t_extraction -->|"couvre"| extraction_graphe
  t_diagnostic -->|"couvre"| diagnostic_graphe
  experiences_cas_synthetiques -->|"utilise"| c_panache
  t_cas_synthetiques -->|"couvre"| experiences_cas_synthetiques
  benchmarks_cas -->|"utilise"| similitude
  t_benchmarks -->|"couvre"| benchmarks_reference
  t_benchmarks -->|"couvre"| benchmarks_cas
  t_benchmarks -->|"couvre"| benchmarks_metriques
  benchmarks_reference -->|"utilise"| benchmarks_cas
  benchmarks_reference -->|"utilise"| benchmarks_metriques
  source -->|"utilise"| stabilite
  benchmarks_cas -->|"utilise"| source
  experiences_cas_synthetiques -->|"utilise"| source
  contrats -->|"utilise"| terrain
  contrats -->|"utilise"| champ_analytique
  contrats -->|"utilise"| source
  contrats -->|"utilise"| similitude
  classDef niveau fill:#ddd0f0,stroke:#495057,color:#212529;
  classDef concept fill:#c9ecd9,stroke:#495057,color:#212529;
  classDef propriete fill:#ffd9b3,stroke:#495057,color:#212529;
  classDef module fill:#d7f0a1,stroke:#495057,color:#212529;
  classDef test fill:#e9ecef,stroke:#495057,color:#212529;
```

**Nœuds et destinations**

| Nœud | Type | Où approfondir |
|---|---|---|
| metric.py | Module de code | [metric.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/metric.py) |
| champ_analytique.py | Module de code | [champ_analytique.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/champ_analytique.py) |
| experiences/uniforme.py | Module de code | [uniforme.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/uniforme.py) |
| experiences/reconstruction_vent.py | Module de code | [reconstruction_vent.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/reconstruction_vent.py) |
| experiences/cas_synthetiques.py | Module de code | [cas_synthetiques.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/cas_synthetiques.py) |
| experiences/superposition_sources.py | Module de code | [superposition_sources.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/superposition_sources.py) |
| experiences/relief.py | Module de code | [relief.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/relief.py) |
| experiences/modele_reduit_edp.py | Module de code | [modele_reduit_edp.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/modele_reduit_edp.py) |
| experiences/identification_source.py | Module de code | [identification_source.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/experiences/identification_source.py) |
| similitude.py | Module de code | [similitude.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/similitude.py) |
| similitude_objets.py | Module de code | [similitude_objets.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/similitude_objets.py) |
| stabilite.py | Module de code | [stabilite.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/stabilite.py) |
| source.py | Module de code | [source.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/source.py) |
| contrats.py | Module de code | [contrats.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/contrats.py) |
| constraints.py | Module de code | [constraints.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/constraints.py) |
| periodic_transport.py | Module de code | [periodic_transport.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/periodic_transport.py) |
| advection_diffusion.py | Module de code | [advection_diffusion.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/advection_diffusion.py) |
| trajectories.py | Module de code | [trajectories.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/trajectories.py) |
| fields.py | Module de code | [fields.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/fields.py) |
| terrain.py | Module de code | [terrain.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/terrain.py) |
| figures/figure_01.py | Module de code | [figure_01.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_01.py) |
| figures/figure_02.py | Module de code | [figure_02.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_02.py) |
| figures/figure_03.py | Module de code | [figure_03.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_03.py) |
| figures/figure_04.py | Module de code | [figure_04.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_04.py) |
| figures/figure_05.py | Module de code | [figure_05.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_05.py) |
| figures/figure_06.py | Module de code | [figure_06.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/figure_06.py) |
| figures/wind_field_explorer.py | Module de code | [wind_field_explorer.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/figures/wind_field_explorer.py) |
| Coût dirigé sur polyligne | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Temps de première arrivée (cas 1D exact) | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Pseudo-distance dirigée (référence uniforme) | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Fonction de courant | Concept | [glossaire.qmd](../glossaire.qmd) |
| Champ de vent stationnaire | Concept | [glossaire.qmd](../glossaire.qmd) |
| Ligne de courant et caractéristique | Concept | [glossaire.qmd](../glossaire.qmd) |
| Panache gaussien (similitude) | Concept | [theorie/similitude.qmd](../theorie/similitude.qmd) |
| Classes de Pasquill et lois de Briggs | Concept | [glossaire.qmd](../glossaire.qmd) |
| Équation de transport (advection-diffusion) | Concept | [theorie/modele-direct.qmd](../theorie/modele-direct.qmd) |
| Assimilation et calibration | Concept | [theorie/assimilation-identification.qmd](../theorie/assimilation-identification.qmd) |
| Champ multi-niveaux historique (non reconstruit) | Concept | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N0 — contexte physique | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| Positivité (famille gaussienne) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| Superposition et linéarité en débit | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| Bilan de masse (famille gaussienne) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| Divergence nulle (champs analytiques) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| Non-symétrie (métrique dirigée) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| Adjoint : gradient exact (référence uniforme et cas 1D) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |
| test_metric.py | Test (CI) | [test_metric.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_metric.py) |
| test_similitude.py | Test (CI) | [test_similitude.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_similitude.py) |
| test_constraints.py | Test (CI) | [test_constraints.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_constraints.py) |
| test_champ_analytique.py | Test (CI) | [test_champ_analytique.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_champ_analytique.py) |
| test_reconstruction_vent.py | Test (CI) | [test_reconstruction_vent.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_reconstruction_vent.py) |
| test_experience_uniforme.py | Test (CI) | [test_experience_uniforme.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_experience_uniforme.py) |
| test_advection_diffusion.py | Test (CI) | [test_advection_diffusion.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_advection_diffusion.py) |
| test_fields.py | Test (CI) | [test_fields.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_fields.py) |
| test_periodic_transport.py | Test (CI) | [test_periodic_transport.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_periodic_transport.py) |
| test_stabilite.py | Test (CI) | [test_stabilite.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_stabilite.py) |
| test_terrain.py | Test (CI) | [test_terrain.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_terrain.py) |
| test_trajectories.py | Test (CI) | [test_trajectories.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_trajectories.py) |
| test_figure_01.py | Test (CI) | [test_figure_01.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_01.py) |
| test_figure_02.py | Test (CI) | [test_figure_02.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_02.py) |
| test_superposition_sources.py | Test (CI) | [test_superposition_sources.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_superposition_sources.py) |
| test_figure_04.py | Test (CI) | [test_figure_04.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_04.py) |
| test_relief.py | Test (CI) | [test_relief.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_relief.py) |
| test_figure_05.py | Test (CI) | [test_figure_05.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_05.py) |
| test_modele_reduit_edp.py | Test (CI) | [test_modele_reduit_edp.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_modele_reduit_edp.py) |
| test_figure_03.py | Test (CI) | [test_figure_03.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_03.py) |
| test_identification_source.py | Test (CI) | [test_identification_source.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_identification_source.py) |
| test_figure_06.py | Test (CI) | [test_figure_06.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_figure_06.py) |
| test_wind_field_explorer.py | Test (CI) | [test_wind_field_explorer.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_wind_field_explorer.py) |
| test_interactive_wind_page.py | Test (CI) | [test_interactive_wind_page.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_interactive_wind_page.py) |
| test_cas_synthetiques.py | Test (CI) | [test_cas_synthetiques.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_cas_synthetiques.py) |
| graphe_connaissances.py | Module de code | [graphe_connaissances.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/graphe_connaissances.py) |
| extraction_graphe.py | Module de code | [src/jdriftx/extraction_graphe.py](../../src/jdriftx/extraction_graphe.py) |
| diagnostic_graphe.py | Module de code | [src/jdriftx/diagnostic_graphe.py](../../src/jdriftx/diagnostic_graphe.py) |
| test_graphe_connaissances.py | Test (CI) | [test_graphe_connaissances.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_graphe_connaissances.py) |
| test_extraction_graphe.py | Test (CI) | [tests/test_extraction_graphe.py](../../tests/test_extraction_graphe.py) |
| test_diagnostic_graphe.py | Test (CI) | [tests/test_diagnostic_graphe.py](../../tests/test_diagnostic_graphe.py) |
| benchmarks/cas.py | Module de code | [cas.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/benchmarks/cas.py) |
| benchmarks/metriques.py | Module de code | [metriques.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/benchmarks/metriques.py) |
| benchmarks/reference.py | Module de code | [reference.py](https://github.com/JM-Brun/J-DriftX/blob/main/src/jdriftx/benchmarks/reference.py) |
| test_benchmarks_reference.py | Test (CI) | [test_benchmarks_reference.py](https://github.com/JM-Brun/J-DriftX/blob/main/tests/test_benchmarks_reference.py) |

## Références et corpus

Les vingt-deux entrées de references.bib, regroupées par rôle, et les objets qu'elles décrivent ou fondent. La table en fin de page indique, pour chaque référence, les pages du site qui la citent réellement (extraction automatique).

```{mermaid}
graph LR
  subgraph cor["Corpus historique (2006-2009)"]
    mohammadi2006crmeca["Mohammadi et Brun 2006 — C. R. Mécanique"]::reference
    mohammadi2006pironneau["Mohammadi, Brun et Pironneau — reduced order modelling (référence non confirmée)"]::reference
    brun2008["Brun et Mohammadi 2008 — chapitre Springer"]::reference
    bozon2008esta["Bozon, Mohammadi et Sinfort 2008 — e-sta"]::reference
    bozon2009driftx["Bozon, Sinfort et Mohammadi 2009 — Drift-X (HAL)"]::reference
    mohammadi2009gis["Bozon et Mohammadi 2009 — Applied Geomatics"]::reference
    brun2006these["Brun 2006 — thèse de doctorat (métadonnées à confirmer)"]::reference
  end
  subgraph art["État de l'art et contextes"]
    muller1979persee["Muller 1979 — cartographie des distances-temps"]::reference
    mohammadi2001shape["Mohammadi et Pironneau 2001 — Applied Shape Optimization"]::reference
    borouchaki1997delaunay["Borouchaki et al. 1997 — maillage de Delaunay"]::reference
    raupach1981canopy["Raupach et Thom 1981 — turbulence de canopée"]::reference
    simpson1997gravity["Simpson 1997 — courants de gravité"]::reference
    hutchinson2017ste["Hutchinson et al. 2017 — estimation de terme source"]::reference
    renormalization2014["Turbelin et al. 2014 — renormalisation en champ moyen"]::reference
    vervecken2015rom["Vervecken et al. 2015 — ROM de panache urbain"]::reference
    fno2024plume["Ayoub et al. 2024 — plume FNO (WSPEEDI)"]::reference
    trindade2021urban["Trindade da Silva et al. 2021 — dispersion urbaine"]::reference
    mahmud2026symmetry["Mahmud et al. 2026 — dispersion urbaine par ML"]::reference
    epa2024appendixw["EPA 2024 — Appendix W (AERMOD)"]::reference
    bonicelli2012cigr["Bonicelli et al. 2012 — dérive des pesticides"]::reference
    defra2011ps2024["Defra 2011 — PS2024 (exposition des riverains)"]::reference
    garbaczewski1997burgers["Garbaczewski et al. 1997 — équation de Burgers"]::reference
  end
  subgraph obj["Objets décrits ou fondés"]
    c_pdist["Pseudo-distance dirigée (référence uniforme)"]::concept
    c_tau["Temps de transport"]::concept
    c_multiniveaux["Champ multi-niveaux historique (non reconstruit)"]::concept
    c_panache["Panache gaussien (similitude)"]::concept
    c_reduction["Modèle approché v(p) (réduction a priori)"]::concept
    c_assimilation["Assimilation et calibration"]::concept
    c_maillage["Maillage gouverné par métrique"]::concept
    c_burgers["Équation de Burgers"]::concept
    c_champ["Champ de vent stationnaire"]::concept
    c_transport["Équation de transport (advection-diffusion)"]::concept
    p_nonsym["Non-symétrie (métrique dirigée)"]::propriete
  end
  c_transport -->|"dépend de"| c_champ
  c_panache -->|"dépend de"| c_transport
  c_assimilation -->|"utilise"| c_reduction
  c_multiniveaux -->|"construit"| c_champ
  mohammadi2006crmeca -->|"fonde"| c_pdist
  mohammadi2006crmeca -->|"fonde"| c_tau
  mohammadi2006pironneau -->|"décrit"| c_reduction
  brun2008 -->|"décrit"| c_multiniveaux
  brun2008 -->|"décrit"| c_panache
  bozon2008esta -->|"décrit"| p_nonsym
  bozon2009driftx -->|"décrit"| c_multiniveaux
  mohammadi2009gis -->|"décrit"| c_multiniveaux
  brun2006these -->|"contexte"| c_tau
  muller1979persee -->|"contexte"| c_tau
  mohammadi2001shape -->|"décrit"| c_reduction
  borouchaki1997delaunay -->|"décrit"| c_maillage
  raupach1981canopy -->|"contexte"| c_panache
  simpson1997gravity -->|"contexte"| c_panache
  hutchinson2017ste -->|"décrit"| c_assimilation
  renormalization2014 -->|"décrit"| c_assimilation
  vervecken2015rom -->|"contexte"| c_reduction
  fno2024plume -->|"contexte"| c_reduction
  trindade2021urban -->|"contexte"| c_champ
  mahmud2026symmetry -->|"contexte"| c_reduction
  epa2024appendixw -->|"contexte"| c_panache
  bonicelli2012cigr -->|"contexte"| c_panache
  defra2011ps2024 -->|"contexte"| c_panache
  garbaczewski1997burgers -->|"décrit"| c_burgers
  c_burgers -->|"contexte"| c_tau
  classDef concept fill:#c9ecd9,stroke:#495057,color:#212529;
  classDef propriete fill:#ffd9b3,stroke:#495057,color:#212529;
  classDef reference fill:#e6dccb,stroke:#495057,color:#212529;
```

**Nœuds et destinations**

| Nœud | Type | Où approfondir |
|---|---|---|
| Mohammadi et Brun 2006 — C. R. Mécanique | Référence bibliographique | [references.qmd](../references.qmd) |
| Mohammadi, Brun et Pironneau — reduced order modelling (référence non confirmée) | Référence bibliographique | [references.qmd](../references.qmd) |
| Brun et Mohammadi 2008 — chapitre Springer | Référence bibliographique | [references.qmd](../references.qmd) |
| Bozon, Mohammadi et Sinfort 2008 — e-sta | Référence bibliographique | [references.qmd](../references.qmd) |
| Bozon, Sinfort et Mohammadi 2009 — Drift-X (HAL) | Référence bibliographique | [references.qmd](../references.qmd) |
| Bozon et Mohammadi 2009 — Applied Geomatics | Référence bibliographique | [references.qmd](../references.qmd) |
| Brun 2006 — thèse de doctorat (métadonnées à confirmer) | Référence bibliographique | [references.qmd](../references.qmd) |
| Muller 1979 — cartographie des distances-temps | Référence bibliographique | [references.qmd](../references.qmd) |
| Mohammadi et Pironneau 2001 — Applied Shape Optimization | Référence bibliographique | [references.qmd](../references.qmd) |
| Borouchaki et al. 1997 — maillage de Delaunay | Référence bibliographique | [references.qmd](../references.qmd) |
| Raupach et Thom 1981 — turbulence de canopée | Référence bibliographique | [references.qmd](../references.qmd) |
| Simpson 1997 — courants de gravité | Référence bibliographique | [references.qmd](../references.qmd) |
| Hutchinson et al. 2017 — estimation de terme source | Référence bibliographique | [references.qmd](../references.qmd) |
| Turbelin et al. 2014 — renormalisation en champ moyen | Référence bibliographique | [references.qmd](../references.qmd) |
| Vervecken et al. 2015 — ROM de panache urbain | Référence bibliographique | [references.qmd](../references.qmd) |
| Ayoub et al. 2024 — plume FNO (WSPEEDI) | Référence bibliographique | [references.qmd](../references.qmd) |
| Trindade da Silva et al. 2021 — dispersion urbaine | Référence bibliographique | [references.qmd](../references.qmd) |
| Mahmud et al. 2026 — dispersion urbaine par ML | Référence bibliographique | [references.qmd](../references.qmd) |
| EPA 2024 — Appendix W (AERMOD) | Référence bibliographique | [references.qmd](../references.qmd) |
| Bonicelli et al. 2012 — dérive des pesticides | Référence bibliographique | [references.qmd](../references.qmd) |
| Defra 2011 — PS2024 (exposition des riverains) | Référence bibliographique | [references.qmd](../references.qmd) |
| Garbaczewski et al. 1997 — équation de Burgers | Référence bibliographique | [references.qmd](../references.qmd) |
| Pseudo-distance dirigée (référence uniforme) | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Temps de transport | Concept | [theorie/metrique-travel-time.qmd](../theorie/metrique-travel-time.qmd) |
| Champ multi-niveaux historique (non reconstruit) | Concept | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| Panache gaussien (similitude) | Concept | [theorie/similitude.qmd](../theorie/similitude.qmd) |
| Modèle approché v(p) (réduction a priori) | Concept | [theorie/reduction-a-priori.qmd](../theorie/reduction-a-priori.qmd) |
| Assimilation et calibration | Concept | [theorie/assimilation-identification.qmd](../theorie/assimilation-identification.qmd) |
| Maillage gouverné par métrique | Concept | [theorie/edp-et-maillage.qmd](../theorie/edp-et-maillage.qmd) |
| Équation de Burgers | Concept | [theorie/burgers-et-jdriftx.qmd](../theorie/burgers-et-jdriftx.qmd) |
| Champ de vent stationnaire | Concept | [glossaire.qmd](../glossaire.qmd) |
| Équation de transport (advection-diffusion) | Concept | [theorie/modele-direct.qmd](../theorie/modele-direct.qmd) |
| Non-symétrie (métrique dirigée) | Propriété (visée ou testée) | [theorie/contraintes-physiques.qmd](../theorie/contraintes-physiques.qmd) |

## Jeux de données candidats

Les corpus examinés par les audits docs/20 et docs/21, et les niveaux de la chaîne N0-N6 qu'ils permettraient de contraindre. « Candidat » ne signifie pas validé : licences, observables et indépendance des essais sont suivis dans l'issue d'audit des données.

```{mermaid}
graph LR
  subgraph proche["Champ proche et installations"]
    d_diflu["DIFLU — hélium, arrêté préfectoral"]::donnees
    d_prairie["Prairie Grass (1956) — rejets de terrain"]::donnees
    d_eries["ERIES — soufflerie urbaine"]::donnees
    d_cedval["CEDVAL / CODASC — données de vent"]::donnees
  end
  subgraph loin["Longue distance"]
    d_datem["DATEM (NOAA) — traces longue distance"]::donnees
    d_etex["ETEX (JRC) — rejets atmosphériques européens"]::donnees
  end
  subgraph meth["Méthodologie et jumeaux numériques"]
    d_mvk["Model Validation Kit — rejets de terrain"]::donnees
    d_dad["DAD-drift — modèle mécaniste ouvert"]::donnees
  end
  subgraph der["Dérive de pulvérisation"]
    d_uav["UAV vignoble — dépôt de pesticide"]::donnees
    d_knapsack["Pulvérisateur knapsack — dépôt"]::donnees
  end
  subgraph cible["Niveaux visés"]
    n5["N5 — expériences et données de terrain"]::niveau
    n6["N6 — calibration et aide à la décision"]::niveau
  end
  n5 -->|"alimente"| n6
  d_datem -->|"candidat pour"| n5
  d_etex -->|"candidat pour"| n5
  d_diflu -->|"candidat pour"| n5
  d_eries -->|"candidat pour"| n5
  d_prairie -->|"candidat pour"| n5
  d_cedval -->|"candidat pour"| n5
  d_mvk -->|"candidat pour"| n6
  d_dad -->|"candidat pour"| n6
  d_uav -->|"candidat pour"| n6
  d_knapsack -->|"candidat pour"| n6
  classDef niveau fill:#ddd0f0,stroke:#495057,color:#212529;
  classDef donnees fill:#fff1a6,stroke:#495057,color:#212529;
```

**Nœuds et destinations**

| Nœud | Type | Où approfondir |
|---|---|---|
| DATEM (NOAA) — traces longue distance | Jeu de données candidat | [20-audit-technique-jeux-donnees.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/20-audit-technique-jeux-donnees.md) |
| ETEX (JRC) — rejets atmosphériques européens | Jeu de données candidat | [20-audit-technique-jeux-donnees.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/20-audit-technique-jeux-donnees.md) |
| DIFLU — hélium, arrêté préfectoral | Jeu de données candidat | [20-audit-technique-jeux-donnees.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/20-audit-technique-jeux-donnees.md) |
| ERIES — soufflerie urbaine | Jeu de données candidat | [20-audit-technique-jeux-donnees.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/20-audit-technique-jeux-donnees.md) |
| Prairie Grass (1956) — rejets de terrain | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| CEDVAL / CODASC — données de vent | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| Model Validation Kit — rejets de terrain | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| DAD-drift — modèle mécaniste ouvert | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| UAV vignoble — dépôt de pesticide | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| Pulvérisateur knapsack — dépôt | Jeu de données candidat | [21-jeux-donnees-seconde-vague-et-cas-synthetiques.md](https://github.com/JM-Brun/J-DriftX/blob/main/docs/21-jeux-donnees-seconde-vague-et-cas-synthetiques.md) |
| N5 — expériences et données de terrain | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |
| N6 — calibration et aide à la décision | Niveau de modélisation | [projet/niveaux-modelisation.qmd](niveaux-modelisation.qmd) |

## Où chaque référence est citée

| Référence | Citée dans les pages du site |
|---|---|
| [Mohammadi et Brun 2006 — C. R. Mécanique](../references.qmd) | [Glossaire](../glossaire.qmd) · [J-DriftX — dispersion atmosphérique à complexité réduite](../index.qmd) · [Héritage Drift-X (2006–2009)](heritage.qmd) · [Métrique travel-time](../theorie/metrique-travel-time.qmd) |
| [Mohammadi, Brun et Pironneau — reduced order modelling (référence non confirmée)](../references.qmd) | [Héritage Drift-X (2006–2009)](heritage.qmd) |
| [Brun et Mohammadi 2008 — chapitre Springer](../references.qmd) | [Glossaire](../glossaire.qmd) · [Limites et domaines de validité](../hypotheses/limites.qmd) · [J-DriftX — dispersion atmosphérique à complexité réduite](../index.qmd) · [Héritage Drift-X (2006–2009)](heritage.qmd) · [Métrique travel-time](../theorie/metrique-travel-time.qmd) · [Modèle direct](../theorie/modele-direct.qmd) · [Réduction a priori](../theorie/reduction-a-priori.qmd) · [Solutions de similitude](../theorie/similitude.qmd) |
| [Bozon, Mohammadi et Sinfort 2008 — e-sta](../references.qmd) | [Héritage Drift-X (2006–2009)](heritage.qmd) |
| [Bozon, Sinfort et Mohammadi 2009 — Drift-X (HAL)](../references.qmd) | [J-DriftX — dispersion atmosphérique à complexité réduite](../index.qmd) · [Héritage Drift-X (2006–2009)](heritage.qmd) |
| [Bozon et Mohammadi 2009 — Applied Geomatics](../references.qmd) | [J-DriftX — dispersion atmosphérique à complexité réduite](../index.qmd) · [Héritage Drift-X (2006–2009)](heritage.qmd) |
| [Brun 2006 — thèse de doctorat (métadonnées à confirmer)](../references.qmd) | [Héritage Drift-X (2006–2009)](heritage.qmd) · [Métrique travel-time](../theorie/metrique-travel-time.qmd) |
| [Muller 1979 — cartographie des distances-temps](../references.qmd) | [Glossaire](../glossaire.qmd) · [Pseudo-distances, coûts orientés et géométries non riemanniennes](../theorie/metriques-non-riemanniennes.qmd) |
| [Mohammadi et Pironneau 2001 — Applied Shape Optimization](../references.qmd) | [Réduction a priori](../theorie/reduction-a-priori.qmd) |
| [Borouchaki et al. 1997 — maillage de Delaunay](../references.qmd) | [EDP & maillage](../theorie/edp-et-maillage.qmd) · [Métrique travel-time](../theorie/metrique-travel-time.qmd) · [Pseudo-distances, coûts orientés et géométries non riemanniennes](../theorie/metriques-non-riemanniennes.qmd) |
| [Raupach et Thom 1981 — turbulence de canopée](../references.qmd) | [Solutions de similitude](../theorie/similitude.qmd) |
| [Simpson 1997 — courants de gravité](../references.qmd) | [Solutions de similitude](../theorie/similitude.qmd) |
| [Hutchinson et al. 2017 — estimation de terme source](../references.qmd) | [Limites et domaines de validité](../hypotheses/limites.qmd) · [Assimilation & identification](../theorie/assimilation-identification.qmd) |
| [Turbelin et al. 2014 — renormalisation en champ moyen](../references.qmd) | [Assimilation & identification](../theorie/assimilation-identification.qmd) |
| [Vervecken et al. 2015 — ROM de panache urbain](../references.qmd) | [liste manuelle](../references.qmd) |
| [Ayoub et al. 2024 — plume FNO (WSPEEDI)](../references.qmd) | [liste manuelle](../references.qmd) |
| [Trindade da Silva et al. 2021 — dispersion urbaine](../references.qmd) | [liste manuelle](../references.qmd) |
| [Mahmud et al. 2026 — dispersion urbaine par ML](../references.qmd) | [liste manuelle](../references.qmd) |
| [EPA 2024 — Appendix W (AERMOD)](../references.qmd) | [liste manuelle](../references.qmd) |
| [Bonicelli et al. 2012 — dérive des pesticides](../references.qmd) | [liste manuelle](../references.qmd) |
| [Defra 2011 — PS2024 (exposition des riverains)](../references.qmd) | [liste manuelle](../references.qmd) |
| [Garbaczewski et al. 1997 — équation de Burgers](../references.qmd) | [Équation de Burgers : lien avec J-DriftX](../theorie/burgers-et-jdriftx.qmd) |
