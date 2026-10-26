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


## Analyse approfondie — signification des niveaux et propriétés à préserver

Le terme « multi-niveaux » recouvre ici un **raffinement spatial emboîté**, distinct de la hiérarchie champ proche → transport lointain décrite par Brun & Mohammadi (2008).

- **Domaines** : `ω₀ = Ω` désigne le domaine global ; les `ωᵢ` sont des sous-domaines imbriqués, de taille décroissante. Le nombre de niveaux et leurs emprises sont choisis par l'utilisateur. Le manuscrit illustre une construction à trois niveaux, d'un domaine de l'ordre de 10 km² vers un domaine local de l'ordre de 10 m² ; les ordres de grandeur et les notations doivent être revérifiés sur la figure et les équations du PDF, l'extraction OCR étant imparfaite.
- **Passage du vent grossier au vent fin** : le champ du niveau précédent est prolongé/restrictionné dans le sous-domaine à partir de données aux quatre coins, avec une partition de l'unité. Les auteurs annoncent la préservation de la divergence nulle et la compatibilité du champ global, sous les conditions formulées dans le papier.
- **Passage de la concentration** : la concentration du niveau fin est construite avec une contrainte sur le flux / la masse entrant dans le sous-domaine. La conservation est donc une propriété d'interface à formuler et à vérifier, pas seulement une propriété locale de la formule gaussienne.
- **Relief** : une correction de vitesse dépendant de la topographie est ajoutée à chaque niveau ; les paramètres de dispersion sont ensuite corrigés sous contrainte de conservation. La topographie modifie aussi la symétrie de la dispersion transverse.
- **Sens des dépendances** : la méthode décrite est grossier-vers-fin, sans rétroaction générale du niveau fin vers le grossier. Une erreur au niveau grossier peut donc se propager vers les niveaux locaux.

### Traduction en exigences vérifiables pour une reprise

1. Définir précisément `Ω`, `ωᵢ`, leurs frontières, les opérateurs de restriction/prolongement et la convention de recouvrement.
2. Énoncer les hypothèses mathématiques nécessaires à la préservation de `∇·u = 0` et prouver la propriété pour l'opérateur retenu.
3. Définir le flux normal entrant à chaque interface et tester le bilan de masse, avec tolérances, pour terrain plat puis relief variable.
4. Mesurer l'erreur d'interpolation du vent, la sensibilité au nombre de niveaux et le coût induit par les raffinements.
5. Comparer séparément la construction spatiale et le couplage champ proche / transport lointain : elles répondent à des questions différentes.
6. Associer chaque propriété au code réellement existant. La présente fiche décrit l'architecture historique ; elle n'affirme pas que la réimplémentation Python actuelle la reproduit.

Voir aussi la [revue du corpus](../../docs/04-revues-papiers-sources.md#complment-danalyse--deux-sens-distincts-de-multi-niveaux) et la [carte conceptuelle N0–N6](../../site/projet/niveaux-modelisation.qmd).
