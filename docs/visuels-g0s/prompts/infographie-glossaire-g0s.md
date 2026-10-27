# Prompt de l'infographie prototype

## Intention
Créer une infographie pédagogique en français sur le glossaire mathématique G0-S de J-DriftX : métrique/quasi-distance, propriété de semi-groupe et inégalité triangulaire dirigée, temps de première arrivée, contre-exemple d'absence d'unicité, composantes 1D sans stagnation, orbite circulaire en 2D, différence entre V1 et V2 et portée limitée du code/tests.

## Prompt utilisé (reconstitué pour archivage)
« Créer une infographie technique soignée en français intitulée “Le glossaire mathématique de J-DriftX – Notions clés, exemples et contre-exemples”. Organiser en panneaux lisibles : (1) métrique et variantes, (2) flot autonome, propriété de semi-groupe et inégalité triangulaire, avec points A-B-C et durées s et t, (3) temps de première arrivée, (4) composantes connexes sans stagnation en 1D, (5) orbite circulaire périodique du système dx/dt=-y, dy/dt=x, (6) comparaison V1 en 1D et V2 en champ uniforme 2D, (7) lien entre notions, code et portée des tests. Utiliser des diagrammes simples, des formules mathématiques, des légendes courtes, une hiérarchie typographique claire, fond clair, vert dominant pour les titres et les trajectoires, bleu limité aux éléments secondaires, rouge réservé aux contre-exemples et aux projections qui illustrent une dégénérescence. Montrer aussi les limites : x'=sqrt(x), x(0)=0 possède plusieurs solutions ; V2 par projection peut ne pas séparer deux points. Ne pas prétendre que les fonctions actuelles implémentent un solveur général de champ variable. »

## Limites connues
Le rendu ImageGen est un prototype raster : les textes petits et certaines formules peuvent être mal transcrits ou géométriquement approximatifs. Il n'est pas une source éditable ni une preuve mathématique. Le SVG `glossaire-g0s.svg` est le support éditable à privilégier pour les mises à jour rigoureuses.
