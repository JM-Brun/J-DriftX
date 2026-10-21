# J-DriftX

**Modélisation à complexité réduite de la dispersion atmosphérique de scalaires passifs** — reprise et modernisation open-source du projet **Drift-X** (J.-M. Brun & B. Mohammadi, 2006–2009).

J-DriftX prédit la dispersion (panaches, puffs, dérive de pulvérisation) via des **solutions de similitude généralisées dans une métrique non symétrique basée sur les temps de transport** — sans résoudre d'EDP ni construire de maillage — avec calibration par **assimilation de données partielles**, évaluation ponctuelle directe, analyse de sensibilité et identification de source.

## Héritage (2006–2009)

| Année | Référence | Support |
|---|---|---|
| 2006 | *Modélisation à complexité réduite de la dérive* — J.-M. Brun, thèse de doctorat, Université Montpellier II | — |
| 2006 | [Similitude généralisée et modélisation géométrique à complexité réduite](https://www.em-consulte.com/article/69927) — B. Mohammadi & J.-M. Brun | *C. R. Mécanique* 334(10), 634–638 |
| 2006 | *Reduced order modelling of dispersion* — B. Mohammadi, J.-M. Brun & O. Pironneau | Springer (non ouvert) |
| 2008 | [Reduced-Order Modelling of Dispersion](https://doi.org/10.1007/978-1-4020-8758-5_14) — J.-M. Brun & B. Mohammadi | Springer, CSM vol. 16, chap. 14, p. 245 et s. |
| 2008 | *Similitude and non symmetric geometry for dispersion modelling* — N. Bozon, B. Mohammadi & C. Sinfort | e-sta vol. 5 (STIC & Environnement'07) |
| 2009 | [A GIS-based atmospheric dispersion model — plateforme Drift-X](https://hal.science/hal-00468863) — N. Bozon, C. Sinfort & B. Mohammadi | HAL hal-00468863 |
| 2009 | [GIS-based atmospheric dispersion modelling](https://doi.org/10.1007/s12518-009-0006-0) — B. Mohammadi & N. Bozon | *Applied Geomatics* 1, 33–39 |

Détails : [docs/references.md](docs/references.md)

## Documentation

Le site documentaire (Quarto, publié sur GitHub Pages) présente le projet, ses fondements théoriques, les hypothèses et leurs limites, les théories mathématiques et la bibliographie :

📚 https://jm-brun.github.io/J-DriftX/

Sources du site : [site/](site/) — rendu local : <code>quarto preview site</code>

## Structure du dépôt

~~~
site/                 # Site Quarto (GitHub Pages)
src/jdriftx/          # Cœur Python (similitude, métrique, contraintes)
tests/                # Pytest (tests physiques + unitaires)
docs/                 # Documents de travail (audit, revue, roadmap, biblio)
.github/workflows/    # CI (ruff, pytest) + publication du site
~~~

## Développement

Le projet suit les pratiques Python modernes : gestion [uv](https://docs.astral.sh/uv/), packaging <code>pyproject.toml</code> (src-layout), lint/format [Ruff](https://docs.astral.sh/ruff/), [pre-commit](https://pre-commit.com), tests [pytest](https://pytest.org).

~~~
uv sync                        # installe le projet + les dépendances de dev
uv run pytest                  # tests
uv run ruff check .            # lint
uv run ruff format --check .   # format
uv run pre-commit run --all-files
~~~

## Statut

🚧 Phase 0 (documentation, audit, revue, roadmap) → M1 (noyau Python + benchmark gaussien). Voir [docs/03-roadmap-jdriftx-v2.md](docs/03-roadmap-jdriftx-v2.md).

## Licence

À définir (proposition : GPLv3 pour le code, CC BY 4.0 pour la documentation).
