# Fiche — Bozon, Sinfort & Mohammadi 2009, plateforme Drift-X (HAL)

## Fichier

- Actuel : <code>MO2009-PUB00026817.pdf</code> → renommage recommandé : <code>2009-bozon-sinfort-mohammadi-driftx-hal.pdf</code> (manuscrit auteur, 17 pages)
- Extraction texte : <code>extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt</code> (texte intégral)

## Référence

Bozon, N., Sinfort, C. & Mohammadi, B. (2009). « A GIS-based atmospheric dispersion model ». Actes de STIC & Environnement, Calais. [HAL hal-00468863](https://hal.science/hal-00468863). Version journal : *JESA* 44(4-5), 445–461, 2010, DOI 10.3166/jesa.44.445-461.

## Revue — l'essentiel

- **Forme gaussienne** : c(x,y,z) = c_c(x) · f(r, δ(x)) avec c_c ~ exp(−a(U)x) et f ~ exp(−b(U,δ)r) ; monotonies documentées (a décroissante en U ; b croissante en U, décroissante en δ).
- **Multi-niveaux (propriétés rapportées par les auteurs)** : rectangles homothétiques emboîtés, restriction du vent à partir des valeurs aux 4 coins (partition de l'unité). Le texte affirme que la restriction préserve la divergence nulle si le champ précédent est à divergence nulle, et que la restriction de concentration satisfait le bilan de masse entrant dans le sous-domaine. Ce ne sont pas des garanties vérifiées indépendamment pour une implémentation moderne : hypothèses, intégration et erreurs numériques restent à formaliser et tester. Le manuscrit décrit 3 niveaux (Ω ≈ 10 km² → ω₂ ≈ 10 m²), avec échantillonnage type 20×20 par niveau.
- **Correction topographique** de type Bernoulli-Newton ; fonctions a/b corrigées sous contrainte de conservation de la masse entrante ; la topographie brise la symétrie de la cross-diffusion.
- **Architecture historique** : cœur Fortran + plugin QGIS (bindings Python), échange CSV, MNT extrait via GDAL, sorties shapefiles et raster (gdal_grid, inverse-distance).
- **Limites assumées** : tendances moyennes à très bas coût ; erreurs dupliquées dans le SIG ; incertitudes supplémentaires des traitements automatisés.

## Valeur pour J-DriftX

Source riche en détails d'implémentation historique : forme de panache, restriction multi-niveaux, correction topographique, échange CSV et sorties SIG. Ces éléments sont des pistes de réimplémentation et de tests, pas une spécification normative ; les propriétés mathématiques et les choix d'interpolation doivent être validés avant d'être repris.

## Pour aller plus loin

Fiche détaillée : <code>docs/04-revues-papiers-sources.md</code>, section 6.
