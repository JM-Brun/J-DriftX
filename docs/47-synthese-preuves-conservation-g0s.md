# Synthèse des preuves — conservation G0-S et temps de transport

**État documentaire : 29 octobre 2026.** Cette note distingue les affirmations historiques, les résultats mathématiques conditionnels, les tests et les reconstructions du projet.

Issue de suivi : [#123](https://github.com/JM-Brun/J-DriftX/issues/123). Reconstruction scientifique minimale : [#232](https://github.com/JM-Brun/J-DriftX/issues/232).

**Rôle éditorial :** synthèse courte des niveaux de preuve et des décisions ouvertes. La dérivation conditionnelle détaillée et les transcriptions de sources sont dans [docs/32](32-conservation-coordonnees-travel-time.md) ; cette synthèse ne la remplace pas et ne recopie pas sa démonstration.

## Conclusion centrale

Les sources historiques affirment des contraintes de conservation, mais elles ne démontrent pas une loi générale de flux scalaire constant sur chaque surface iso-temps.

- **2006 — Mohammadi & Brun :** l'extraction indique une contrainte d'intégrale volumique globale de concentration égale à la quantité totale émise. Ce n'est pas une affirmation de flux constant sur chaque surface iso-temps. L'audit est déjà consigné dans [docs/32](32-conservation-coordonnees-travel-time.md) et [docs/45](45-audit-article-mohammadi-brun-2006.md). Le contrôle visuel ciblé des glyphes reste distinct de la disponibilité de la source : le PDF éditeur est déjà présent dans `raw/`.
- **2008 — chapitre Springer :** les deux branches imprimées de c⁺ sont dimensionnellement incompatibles sous les unités conventionnelles. Le volume Springer complet reste conservé conformément à la décision du mainteneur.
- **Thèse :** le PDF a été obtenu par une voie appropriée, déjà documentée dans le projet. La PR [#261](https://github.com/JM-Brun/J-DriftX/pull/261) a clarifié la provenance. Le blocage Anubis rencontré par un outil de consultation ne signifie pas que la source n'a pas été obtenue. Obtention, inspection du fichier local, comparaison binaire et droits de redistribution sont des questions distinctes.
- **JESA 2010 :** la notice HAL [hal-02594312](https://hal.inrae.fr/hal-02594312) est identifiée. Le manuscrit STIC & Environnement 2009 [hal-00468863](https://hal.science/hal-00468863) est une version distincte. Le manuscrit 2009 est présent dans `raw/`, mais le PDF JESA 2010 et son extraction ne sont pas actuellement versionnés dans `raw/`. La copie ResearchGate candidate examinée affiche bien les métadonnées JESA, mais son front matter l'identifie explicitement comme `hal-00468863`, version 1, manuscrit auteur STIC 2009 : elle ne peut donc pas servir de substitut à l'article JESA. Il faut exploiter le fichier associé à la notice HAL JESA déjà identifiée, sans relancer une recherche bibliographique générique ni supposer que les versions sont identiques.

## Reconstruction retenue pour J-DriftX

Le choix explicite est un **inventaire de masse**, pas un flux massique :

`c⁺(x,y) = ∫_H^zmax c_loc(x,y,z) dz`

`M_C = ∫_{Ωxy} c⁺(x,y) dx dy`

Avec c_loc en kg·m⁻³, c⁺ est en kg·m⁻² et M_C en kg, sous réserve de domaines et d'intégrales bien définis. Ce choix conserve la première branche imprimée et minimise les changements conceptuels ; il ne prouve pas l'intention historique. La branche u⁺_loc c_loc, où u⁺_loc est sans dimension, ne peut pas être une définition dimensionnellement équivalente de la même masse.

## Niveaux de preuve

| Proposition | Statut | Limite |
|---|---|---|
| L'article de 2006 impose une intégrale globale de concentration | Affirmé dans l'extraction de la source | N'établit pas un flux constant par surface iso-temps. |
| La thèse et le chapitre 2008 revendiquent une quantité réduite à conserver | Affirmé dans les textes consultés | La formule imprimée de c⁺ contient une incompatibilité dimensionnelle. |
| Une carte globale régulière (τ, η₁, η₂) → (x, y, z) est définie par les sources historiques | Non établi | Caractéristique et projection ne prouvent pas régularité, bijectivité ni jacobien global. |
| La construction projetée vérifie toujours u·∇τ = 1 en champ variable | Réfuté pour la construction testée | Le contre-exemple de cisaillement ne réfute pas toutes les définitions possibles d'un temps de transport. |
| Le flux total est constant dans le cas uniforme | Démontré sous hypothèses explicites | Voir [docs/37](37-transformation-tau-eta-cas-uniforme.md) ; débit [M/T], distinct d'un inventaire [M]. |
| La conservation générale du modèle historique est démontrée | Non | Le bilan complet et la transformation historique ne sont pas suffisamment spécifiés. |

La note générale [docs/32](32-conservation-coordonnees-travel-time.md) établit une loi de bilan conditionnelle pour une carte régulière et inversible. Ce résultat ne constitue pas une preuve rétroactive de la construction historique.

## Prochaines tâches utiles

1. **Thèse :** consulter les pièces de provenance déjà archivées. Si une comparaison SHA-256 locale/HAL est déjà documentée, la citer et fermer ce point ; sinon, comparer les fichiers déjà obtenus. Ne pas refaire l'acquisition.
2. **JESA 2010 vs manuscrit 2009 :** exploiter le fichier associé à la notice HAL `hal-02594312` déjà identifiée ; créer une extraction versionnée si autorisé ; comparer équations, définitions, domaines, unités, sources/puits et conditions aux limites, avec pages et numéros d'équations. Ne pas refaire une recherche générale de la source.
3. **2006 :** vérifier seulement les glyphes et signes incertains du PDF éditeur déjà présent, en particulier les équations (1), (2), (4) et la contrainte intégrale p. 636.
4. **Bilan G0-S :** établir un théorème sous hypothèses explicites, un contre-exemple ou un verdict d'inreconstructibilité historique. Ne pas dériver un jacobien spécifique si la transformation n'est pas définie.
5. **Registre :** répercuter les résultats dans [docs/46](46-registre-erreurs-incoherences-documentaires.md) et la matrice de [#232](https://github.com/JM-Brun/J-DriftX/issues/232), sans effacer l'historique ni dupliquer les tests.

## Critère d'arrêt

Si les sources primaires ne définissent pas la transformation historique ni les termes du bilan, la conclusion correcte est : **la conservation est affirmée historiquement ; la reconstruction retenue est dimensionnellement cohérente ; la preuve de conservation du modèle historique général n'est pas établie**. L'absence de preuve n'est pas, à elle seule, une preuve d'invalidité du modèle.


La vérification de la copie ResearchGate est consignée dans la fiche de provenance JESA : son texte intégral porte la mention « hal-00468863, version 1 — 31 Mar 2010 » et « Author manuscript, published in STIC & Environnement, Calais : France (2009) ». Cette source candidate est écartée comme preuve de la version de record JESA, sans écarter la notice HAL JESA elle-même.