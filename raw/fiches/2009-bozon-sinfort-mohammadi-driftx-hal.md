# Fiche — Bozon, Sinfort & Mohammadi 2009, plateforme Drift-X (HAL)

## Fichier

- Actuel : <code>MO2009-PUB00026817.pdf</code> → renommage recommandé : <code>2009-bozon-sinfort-mohammadi-driftx-hal.pdf</code> (manuscrit auteur, 17 pages)
- Extraction texte : <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> (texte intégral)

## Référence

Bozon, N., Sinfort, C. & Mohammadi, B. (2009). « A GIS-based atmospheric dispersion model ». Actes de STIC & Environnement, Calais. [HAL hal-00468863](https://hal.science/hal-00468863). Version journal : *JESA* 44(4-5), 445–461, 2010, DOI 10.3166/jesa.44.445-461.

## Revue — l'essentiel

- **Forme gaussienne** : c(x,y,z) = c_c(x) · f(r, δ(x)) avec c_c ~ exp(−a(U)x) et f ~ exp(−b(U,δ)r) ; monotonies documentées (a décroissante en U ; b croissante en U, décroissante en δ).
- **Multi-niveaux** : rectangles homothétiques emboîtés, vent interpolé aux 4 coins (partition de l'unité) — garanties : divergence nulle et conservation de la masse dans chaque sous-domaine ; 3 niveaux en pratique (Ω ≈ 10 km² → ω_2 ≈ 10 m²), échantillonnage type 20×20 par niveau.
- **Correction topographique** de type Bernoulli-Newton ; fonctions a/b corrigées sous contrainte de conservation de la masse entrante ; la topographie brise la symétrie de la cross-diffusion.
- **Architecture historique** : cœur Fortran + plugin QGIS (bindings Python), échange CSV, MNT extrait via GDAL, sorties shapefiles et raster (gdal_grid, inverse-distance).
- **Limites assumées** : tendances moyennes à très bas coût ; erreurs dupliquées dans le SIG ; incertitudes supplémentaires des traitements automatisés.

## Valeur pour J-DriftX

La source la plus opérationnelle du corpus : forme gaussienne exacte et ses monotonies (testables), construction multi-niveaux à réimplémenter en Python, correction topographique, interface CSV à conserver pour compatibilité, spécification des sorties raster/vecteur.

## Pour aller plus loin

Fiche détaillée : <code>docs/04-revues-papiers-sources.md</code>, section 6.
