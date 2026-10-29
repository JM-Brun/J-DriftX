# Synthèse des preuves — conservation G0-S et temps de transport

**État documentaire : 29 octobre 2026.** Cette note distingue les affirmations historiques, les résultats mathématiques conditionnels, les tests et les reconstructions du projet. Elle ne remplace pas les sources primaires.

Issue de suivi : [#123](https://github.com/JM-Brun/J-DriftX/issues/123). Reconstruction scientifique minimale : [#232](https://github.com/JM-Brun/J-DriftX/issues/232).

## Conclusion centrale

Les sources historiques affirment des contraintes de conservation, mais elles ne démontrent pas une loi générale de flux scalaire constant sur chaque surface iso-temps.

- **2006 — Mohammadi & Brun :** l'extraction de l'article indique une contrainte d'intégrale volumique globale de la concentration égale à la quantité totale émise. Ce n'est pas une affirmation de flux constant sur chaque surface iso-\tau. L'audit et la transcription sont déjà consignés dans [docs/32](32-conservation-coordonnees-travel-time.md) et [docs/45](45-audit-article-mohammadi-brun-2006.md). Il reste un contrôle visuel ciblé des glyphes des équations si une transcription typographique exacte est requise ; il ne faut pas requalifier la source comme introuvable.
- **2008 — chapitre Springer :** les deux branches imprimées de c⁺ sont dimensionnellement incompatibles sous les unités conventionnelles. Le volume Springer complet est conservé conformément à la décision du mainteneur ; cette décision ne préjuge pas des droits.
- **Thèse :** le PDF a été obtenu par une voie appropriée, déjà documentée dans le projet. La PR [#261](https://github.com/JM-Brun/J-DriftX/pull/261) a clarifié la provenance. Un blocage Anubis rencontré par un outil de consultation ne signifie pas que la source n'a pas été obtenue. Il faut distinguer obtention, inspection du fichier local, comparaison binaire et droits de redistribution.
- **JESA 2010 :** la notice HAL [hal-02594312](https://hal.inrae.fr/hal-02594312) est identifiée. Le manuscrit STIC & Environnement 2009 [hal-00468863](https://hal.science/hal-00468863) est une version distincte. Le manuscrit 2009 est dans `raw/`, mais le PDF JESA 2010 et son extraction ne sont pas actuellement versionnés dans `raw/`. La source HAL JESA doit être exploitée, sans relancer une recherche bibliographique générique et sans supposer que les versions sont identiques.

## Reconstruction retenue pour J-DriftX

Le choix explicite est un **inventaire de masse**, pas un flux massique :

\[
c^+(x,y)=\int_H^{z_{\max}}c_{loc}(x,y,z)\,dz,
\qquad
M_C=\int_{\Omega_{xy}}c^+(x,y)\,dx\,dy.
\]

Avec \([c_{loc}]=\mathrm{kg\,m^{-3}}\), on obtient \([c^+]=\mathrm{kg\,m^{-2}}\) et \([M_C]=\mathrm{kg}\), sous réserve de domaines et d'intégrales bien définis. Ce choix conserve la première branche imprimée et minimise les changements conceptuels ; il ne prouve pas l'intention historique. La branche \(u^+_{loc}c_{loc}\), où \(u^+_{loc}\) est sans dimension, ne peut pas être une définition dimensionnellement équivalente de la même masse.

## Niveaux de preuve

| Proposition | Statut | Limite |
|---|---|---|
| Les auteurs de 2006 imposent une intégrale globale de concentration | Affirmé dans l'extraction de la source | La formule n'établit pas un flux constant par surface iso-\tau. |
| La thèse et le chapitre 2008 revendiquent une quantité réduite à conserver | Affirmé dans les textes consultés | La formule imprimée de c⁺ contient une incompatibilité dimensionnelle. |
| Une carte globale régulière \((\tau,\eta_1,\eta_2)\mapsto(x,y,z)\) est définie par les sources historiques | Non établi | Caractéristique et projection ne prouvent pas régularité, bijectivité ni existence d'un jacobien global. |
| La construction projetée vérifie toujours \(u\cdot\nabla\tau=1\) en champ variable | Réfuté pour la construction testée | Le contre-exemple de cisaillement ne réfute pas toutes les définitions possibles d'un temps de transport. |
| Le flux total est constant dans le cas uniforme | Démontré sous hypothèses explicites | Voir [docs/37](37-transformation-tau-eta-cas-uniforme.md) ; débit [M/T], distinct d'un inventaire [M]. |
| La conservation générale du modèle historique est démontrée | Non | Le bilan complet et la transformation historique ne sont pas suffisamment spécifiés dans les sources auditées. |

La note générale [docs/32](32-conservation-coordonnees-travel-time.md) établit une loi de bilan conditionnelle pour une carte régulière et inversible. Ce résultat ne constitue pas une preuve rétroactive de la construction historique.

## Prochaines tâches utiles

1. **Thèse :** consulter les pièces de provenance déjà archivées avant toute action supplémentaire. Si une comparaison SHA-256 locale/HAL est déjà documentée, la citer et fermer ce point ; sinon, comparer les fichiers déjà obtenus. Ne pas refaire l'acquisition.
2. **JESA 2010 vs manuscrit 2009 :** exploiter le fichier associé à la notice HAL `hal-02594312` déjà identifiée ; créer une extraction versionnée si autorisé ; comparer les équations, définitions, domaines, unités, sources/puits et conditions aux limites, avec références de pages et numéros d'équations. Ne pas refaire une recherche générale de la source.
3. **2006 :** vérifier seulement les glyphes et signes incertains du PDF éditeur déjà présent, en particulier les équations (1), (2), (4) et la contrainte intégrale p. 636.
4. **Bilan G0-S :** à partir des formules authentifiées, établir un théorème sous hypothèses explicites, un contre-exemple ou un verdict d'inreconstructibilité historique. Ne pas dériver un jacobien spécifique si la transformation n'est pas définie.
5. **Registre :** répercuter les résultats dans [docs/46](46-registre-erreurs-incoherences-documentaires.md) et la matrice de [#232](https://github.com/JM-Brun/J-DriftX/issues/232), sans effacer l'historique ni dupliquer les tests.

## Critère d'arrêt

Si les sources primaires ne définissent pas la transformation historique ni les termes du bilan, la conclusion correcte est : **la conservation est affirmée historiquement ; la reconstruction retenue est dimensionnellement cohérente ; la preuve de conservation du modèle historique général n'est pas établie**. L'absence de preuve n'est pas, à elle seule, une preuve d'invalidité du modèle.
