# Identification de source et assimilation de données

## Rapport avec J-DriftX

L'identification de source (source-term estimation, STE) est le **problème inverse** : retrouver une ou plusieurs propriétés de la source à partir d'observations de concentration et d'un modèle de transport. C'est un axe historique de Drift-X, mais il doit être traité séparément de la précision du modèle direct. Un modèle direct rapide ne garantit pas à lui seul l'identifiabilité ou une estimation robuste.

### Hutchinson, Oh et al. (2017) — revue des méthodes STE

- **Type :** revue publiée dans *Information Fusion*.
- **Relation :** source de cadrage pour classer les méthodes concurrentes (optimisation, adjoint, approches probabilistes, capteurs statiques/mobiles).
- **Intuition commune :** exploiter un modèle direct et des observations pour remonter aux paramètres de source.
- **Conséquence :** choisir des baselines adaptées et expliciter les hypothèses d'observabilité, le bruit et la régularisation.
- [Article](https://www.sciencedirect.com/science/article/pii/S156625351630152X)

### Turbelin, Singh & Issartel (2016) — renormalisation pour reconstruire des sources

- **Type :** article de méthode dans *Journal of Advances in Modeling Earth Systems* (JAMES).
- **Relation :** approche alternative du problème inverse ; lien conceptuel avec l'opérateur de transport et son inverse généralisé.
- **Conséquence :** étudier la compatibilité mathématique avec la formulation travel-time et comparer les hypothèses plutôt que supposer l'équivalence.
- [Article](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014MS000385)

### NARAC / LLNL — Source Term Estimation

- **Type :** documentation institutionnelle d'un système opérationnel, pas article unique.
- **Relation :** contexte de méthodes et d'exigences opérationnelles à grande échelle.
- **Conséquence :** identifier les contraintes de latence, de robustesse et de validation ; ne pas traiter la page institutionnelle comme un benchmark quantitatif.
- [Documentation](https://narac.llnl.gov/research-and-development/source-term-estimation)

### Source Term Estimation for Atmospheric Pollutant Releases (Zenodo, 2025)

- **Type :** revue/prépublication ou rapport déposé sur Zenodo ; statut éditorial à confirmer.
- **Relation :** synthèse secondaire pour les méthodes adjointes, Tikhonov, bayésiennes et PINNs.
- **Conséquence :** vérifier les sources primaires citées et le statut de publication avant d'en tirer des conclusions.
- [Notice](https://zenodo.org/records/22914336)

## Questions et tests à prévoir

- Quels paramètres de source sont identifiables avec le nombre et la position de capteurs envisagés ?
- Comment le bruit et les erreurs de modèle se propagent-ils dans l'estimation ?
- Le gradient/adjointe est-il vérifié par différences finies ou tests de gradient ?
- Les données de calibration sont-elles séparées de celles de validation ?
- Comparer optimisation déterministe et méthode probabiliste uniquement avec un protocole et des hypothèses explicites.
