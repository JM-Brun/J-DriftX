# J-DriftX

**Modélisation à complexité réduite de la dispersion atmosphérique de scalaires passifs** — reprise et modernisation open-source du projet **Drift-X** (J.-M. Brun & B. Mohammadi, 2006–2009).

J-DriftX prédit la dispersion (panaches, puffs, dérive de pulvérisation) via des **solutions de similitude généralisées dans une métrique non symétrique basée sur les temps de transport** — sans résoudre d'EDP ni construire de maillage — avec calibration par **assimilation de données partielles**, évaluation ponctuelle directe, analyse de sensibilité et identification de source.

![Schéma de principe : panache gaussien généralisé dans la métrique des temps de transport τ.](site/images/panache-travel-time.svg)

## Héritage (2006–2009)

| Année | Référence | Support |
|---|---|---|
| 2006 | *Modélisation à complexité réduite de la dérive* — J.-M. Brun, thèse de doctorat, Université Montpellier II | — (non déposée en ligne à ce jour) |
| 2006 | [Similitude généralisée et modélisation géométrique à complexité réduite](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) — B. Mohammadi & J.-M. Brun | *C. R. Mécanique* 334(10), 634–638 (PDF libre, Académie des sciences) |
| 2006 | *Reduced order modelling of dispersion* — B. Mohammadi, J.-M. Brun & O. Pironneau | Springer (non ouvert) |
| 2008 | [Reduced-Order Modelling of Dispersion](https://doi.org/10.1007/978-1-4020-8758-5_14) — J.-M. Brun & B. Mohammadi | Springer, CSM vol. 16, chap. 14, p. 245 et s. |
| 2008 | *Similitude and non symmetric geometry for dispersion modelling* — N. Bozon, B. Mohammadi & C. Sinfort | e-sta vol. 5 (STIC & Environnement'07) |
| 2009 | [A GIS-based atmospheric dispersion model — plateforme Drift-X](https://hal.science/hal-00468863) — N. Bozon, C. Sinfort & B. Mohammadi | Actes STIC & Environnement, HAL hal-00468863 |
| 2009 | [GIS-based atmospheric dispersion modelling](https://doi.org/10.1007/s12518-009-0006-0) — B. Mohammadi & N. Bozon | *Applied Geomatics* 1, 33–39 |
| 2010 | [A GIS-based atmospheric dispersion model](https://doi.org/10.3166/jesa.44.445-461) — N. Bozon, C. Sinfort & B. Mohammadi | *JESA* 44(4-5), 445–461 (version journal) |

Détails : [docs/references.md](docs/references.md) — **fiches de lecture par papier source** (contenus extraits, équations, statuts d'accès) : [docs/04-revues-papiers-sources.md](docs/04-revues-papiers-sources.md) — PDF et extractions texte des sources primaires : [raw/](raw/)

## Documentation

Le site documentaire (Quarto, publié sur GitHub Pages) présente le projet, ses fondements théoriques, les hypothèses et leurs limites, les théories mathématiques et la bibliographie :

📚 https://jm-brun.github.io/J-DriftX/

Pages à lire en priorité : [Lectures des sources](https://jm-brun.github.io/J-DriftX/projet/lectures.html) (revue par papier du corpus historique) et le [Glossaire](https://jm-brun.github.io/J-DriftX/glossaire.html) (les notions clés expliquées simplement).

Sources du site : [site/](site/) — rendu local : <code>quarto preview site</code>

## Structure du dépôt

~~~
site/                 # Site Quarto (GitHub Pages)
src/jdriftx/          # Cœur Python (similitude, métrique, contraintes)
tests/                # Pytest (tests physiques + unitaires)
docs/                 # Documents de travail (audit, revues, roadmap, biblio)
raw/                  # Sources primaires : PDF du corpus + extractions texte brutes
.github/workflows/    # CI (ruff, pytest) + publication du site
~~~

## Développement

Le projet suit les pratiques Python modernes : gestion [uv](https://docs.astral.sh/uv/), packaging <code>pyproject.toml</code> (src-layout), lint/format [Ruff](https://docs.astral.sh/ruff/), [pre-commit](https://pre-commit.com), tests [pytest](https://pytest.org).

### Tests : la physique comme oracle

Sans EDP ni maillage, il n'y a pas de valeur de référence précalculée : les tests unitaires encodent des **propriétés physiques** — conservation de la masse, symétrie latérale, superposition, non-symétrie de la métrique τ — sous la forme **Given / When / Then** :

![Tests unitaires Given/When/Then — la physique comme oracle](site/images/tests-given-when-then.svg)

Détails : page [Qualité & tests](https://jm-brun.github.io/J-DriftX/projet/qualite.html) du site.

~~~
uv sync                        # installe le projet + les dépendances de dev
uv run pytest                  # tests
uv run ruff check .            # lint
uv run ruff format --check .   # format
uv run pre-commit run --all-files
~~~

## Statut

🚧 Phase 0 (documentation, audit, revues, roadmap) → M1 (noyau Python + benchmark gaussien). Voir [docs/03-roadmap-jdriftx-v2.md](docs/03-roadmap-jdriftx-v2.md).

## Licence

À définir (proposition : GPLv3 pour le code, CC BY 4.0 pour la documentation).
