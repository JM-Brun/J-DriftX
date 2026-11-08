# Note de recherche — équation de Burgers et J-DriftX

**Statut :** lien historique direct au modèle de vitesse 1D dans la canopée de la thèse ; aucune équivalence avec le modèle de dispersion lointaine ou validation physique générale démontrée.

**Date de la note :** 2026-10-22.

**Rôle éditorial :** note de recherche courte, centrée sur le verdict de pertinence et les limites de la piste Burgers. Pour l'explication développée destinée au lecteur du site, voir la [page Quarto « Équation de Burgers : lien avec J-DriftX »](../site/theorie/burgers-et-jdriftx.qmd). La page du site expose les notions et exemples ; cette note conserve le cadrage et les décisions conditionnelles.

## Question

L'équation de Burgers est-elle pertinente pour la modélisation de la dispersion atmosphérique et, en particulier, pour l'exploration travel-time / similitude de J-DriftX ?

## Résultat synthétique

La thèse de Brun utilise explicitement une équation de Burgers visqueuse forcée pour modéliser une vitesse le long d'une ligne pénétrant la canopée, et une équation distincte pour le scalaire transporté (chapitre 4, équations 4.8–4.9, pp. 66–67 ; [fiche de lecture](bibliographie/sources/these-brun.md)). C'est un lien direct avec l'héritage, absent du cadrage initial de cette note. Il ne démontre ni que Burgers décrit la concentration atmosphérique ou la dérive de gouttelettes, ni que le modèle canopée est validé ou implémenté dans J-DriftX.

Équation scalaire visqueuse :

\[
\partial_t u + u\partial_x u = \nu\partial_{xx}u
\]

Forme conservative :

\[
\partial_t u + \partial_x(u^2/2)=\nu\partial_{xx}u.
\]

Transport de concentration, sous une forme usuelle sans source ni puits :

\[
\partial_t c + \nabla\cdot(\mathbf{v}c)=\nabla\cdot(\mathbf{K}\nabla c).
\]

La distinction fondamentale est que Burgers fait transporter l'inconnue par elle-même, tandis que le vent transporte généralement une concentration passive.

Pour le modèle historique local, un cas analytique distinct de la résolution visqueuse est dérivé dans la [fiche de thèse](bibliographie/sources/these-brun.md) : en régime stationnaire, sans viscosité, pour une vitesse positive et une traînée constante $k=C_Da_{LAD}$, la vitesse décroît comme $e^{-kr/2}$. Cette référence conditionnelle aide à vérifier les conventions et les futurs solveurs ; elle ne reproduit pas les résultats inverses historiques.

## Classement du lien

- **Modèle historique de vitesse locale :** oui, explicitement au chapitre 4 de la thèse ; application idéalisée et conditions à préciser.
- **Analogie mathématique avec le transport de concentration :** oui, avec inconnues et bilan distincts.
- **Benchmark numérique complémentaire :** envisageable, mais non encore construit.
- **Dérivation de la formulation travel-time :** non établie.
- **Remplacement du modèle physique de dispersion :** non justifié.
- **Effet de la végétation ou du relief :** ne crée pas à lui seul une non-linéarité de Burgers ; il faut spécifier comment ces effets entrent dans le vent, la fermeture, les conditions aux limites ou les coefficients.

Garbaczewski, Kondrat et Olkiewicz (1997) étudient une connexion entre écoulements de Burgers et processus de diffusion markoviens, en lien conceptuel avec les contaminants passifs. Cette source justifie une piste de lecture, pas une équivalence avec Drift-X.

## Proposition de suite conditionnelle

Si un test numérique général est nécessaire, documenter séparément :
1. advection-diffusion linéaire à vitesse prescrite ;
2. Burgers visqueuse avec une solution de référence ;
3. modèle réduit J-DriftX dans son domaine défini.

Comparer uniquement les propriétés réellement communes, en spécifiant inconnues, unités, conditions initiales et aux limites, flux conservés, erreurs et limites d'interprétation. Ne pas assimiler la vitesse locale 1D historique à la concentration ou au champ de vent atmosphérique général de J-DriftX.

## Références

- Garbaczewski, P., Kondrat, G. et Olkiewicz, R. (1997). “Burgers' flows as Markovian diffusion processes.” *Physical Review E*, 55, 1401. https://doi.org/10.1103/PhysRevE.55.1401
- Documentation Firedrake, “Burgers equation”: https://www.firedrakeproject.org/firedrake/demos/burgers.py.html
- Brun, J.-M. et Mohammadi, B. (2008). “Reduced-Order Modelling of Dispersion.” https://doi.org/10.1007/978-1-4020-8758-5_14
- Mohammadi, B. et Brun, J.-M. (2006). “Similitude généralisée et modélisation géométrique à complexité réduite.” https://doi.org/10.1016/j.crme.2006.06.007
- Brun, J.-M. (2007), thèse, chapitre 4 et annexe C ; [fiche de source](bibliographie/sources/these-brun.md).

## Limites de la revue

Cette note est un cadrage conceptuel ciblé, pas une revue systématique de l'équation de Burgers ni une vérification exhaustive du texte intégral de Garbaczewski et al. Aucun calcul ni benchmark n'a été exécuté dans le cadre de cette note.
