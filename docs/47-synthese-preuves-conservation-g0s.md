# Synthèse des preuves — conservation G0-S et temps de transport

**État documentaire : 29 octobre 2026.** Cette synthèse consolide les résultats des audits, sans remplacer les sources primaires ni déclarer terminées les vérifications qui nécessitent un fac-similé authentifié.

Périmètre : conservation revendiquée pour le transport lointain (G0-S), définition du temps de migration, bilan physique et traçabilité des sources. Issue de suivi : [#123](https://github.com/JM-Brun/J-DriftX/issues/123). La reconstruction scientifique minimale et ses critères plus larges restent suivis dans [#232](https://github.com/JM-Brun/J-DriftX/issues/232).

## Résultat principal

La conservation de la quantité réduite est **affirmée par les sources historiques**, mais les éléments actuellement authentifiés ne démontrent pas une loi générale de flux constant sur chaque surface iso-temps.

Deux propositions différentes doivent rester séparées :

1. **Contrainte historique de masse globale** : l'article de 2006 présente dans l'extraction textuelle une intégrale de concentration sur le volume ℝ³ égale à la « quantité totale émise » (p. imprimée 636). L'extraction perd les symboles mathématiques ; la formule exacte doit encore être contrôlée sur le fac-similé.
2. **Conservation du modèle lointain** : la thèse et le chapitre Springer présentent une quantité réduite (M_C) à conserver, sans démonstration établie dans les passages audités. La définition de (c^+) contient deux branches dimensionnellement incompatibles sous les unités conventionnelles.

La loi de bilan en coordonnées régulières exposée dans [docs/32](32-conservation-coordonnees-travel-time.md) est un résultat mathématique conditionnel. Elle ne prouve pas que la construction historique définisse une carte globale régulière ni qu'elle satisfasse ses hypothèses.

## Tableau des niveaux de preuve

| Proposition | Statut | Base et limite |
|---|---|---|
| La pseudo-distance historique est orientée et peut manquer séparation, symétrie et inégalité triangulaire | **Affirmé dans la source** | Article de 2006, audit [docs/45](45-audit-article-mohammadi-brun-2006.md). Les auteurs reconnaissent ces limites. |
| L'article de 2006 impose une contrainte intégrale globale de concentration | **Affirmé dans l'extraction ; transcription exacte non vérifiée visuellement** | Extraction versionnée, passage p. 636. Le PDF éditeur n'a pas pu être inspecté visuellement lors de l'audit. |
| La thèse revendique la conservation de (M_C) | **Affirmé dans une copie tierce consultée** | Thèse, §7.3, p. imprimée 129, équations (7.12)–(7.13). Le PDF du dépôt n'est pas authentifié octet à octet contre HAL. |
| Les deux branches imprimées de (c^+) sont dimensionnellement équivalentes | **Réfuté sous les unités explicites** | Si (c_{loc}) est en kg·m⁻³ et (u^+_{loc}) sans dimension, (int c_{loc},dz) est en kg·m⁻² tandis que (u^+_{loc}c_{loc}) reste en kg·m⁻³. L'incompatibilité est visible dans les copies tierces du chapitre 2008 et de la thèse ; l'intention historique reste inconnue. |
| Une carte globale régulière ((\tau,\eta_1,\eta_2)\mapsto(x,y,z)) et son jacobien sont définis par les sources historiques auditées | **Non établi** | La définition par caractéristique et projection ne suffit pas à établir régularité, bijectivité ou jacobien global. |
| La construction projetée satisfait toujours (u\cdot\nabla\tau=1) en champ variable | **Réfuté pour la construction testée** | Le contre-exemple de cisaillement documenté dans [docs/33](33-test-contre-exemple-cisaillement.md) et ses tests réfutent cette propriété générale pour ce coût projeté ; cela ne réfute pas toutes les définitions possibles d'un temps de transport. |
| Le flux scalaire intégré est constant entre toutes les surfaces iso-τ | **Non établi pour le modèle historique** | Une telle conclusion exige un bilan, une carte admissible, et des hypothèses sur les sources/puits, les termes temporels et les flux latéraux. |
| Le cas uniforme possède un flux total constant sous hypothèses stationnaires et sans pertes | **Démontré analytiquement sous hypothèses** | [docs/37](37-transformation-tau-eta-cas-uniforme.md). Il s'agit d'un débit de scalaire [M/T], pas de l'inventaire [M]. |
| Des tests logiciels démontrent la conservation du modèle historique multi-niveaux | **Non** | Les tests présents couvrent des cas analytiques et des contre-exemples ciblés ; ils ne valident pas un solveur de production du modèle historique. |

## Reconstruction retenue pour J-DriftX

Le choix explicite est un **inventaire de masse**, pas un flux massique :

[
c^+(x,y)=\int_{H}^{z_{\max}}c_{loc}(x,y,z)\,dz,
\qquad
M_C=\int_{\Omega_{xy}}c^+(x,y)\,dx\,dy.
]

Avec (c_{loc}) en kg·m⁻³, (c^+) est en kg·m⁻² et (M_C) en kg, sous réserve d'un domaine d'intégration défini et d'une intégrale convergente. Cette définition conserve la première branche historique et minimise les changements conceptuels, mais **n'établit pas l'intention originale des auteurs**. La branche (u^+_{loc}c_{loc}) ne doit pas être utilisée comme définition équivalente de cette masse.

Un débit massique serait une grandeur différente, construite à partir d'un flux incluant une vitesse dimensionnée et mesurée en kg/s. Il ne faut pas alterner inventaire et débit au fil des démonstrations.

## Sources : état d'authentification

- **Article 2006** — référence bibliographique, URL officielle et extraction textuelle répertoriées dans [docs/45](45-audit-article-mohammadi-brun-2006.md) et la fiche de provenance. Le contrôle visuel des équations (1), (2), (4) et de la contrainte globale reste ouvert ; la formule OCR ne doit pas être traitée comme transcription exacte.
- **Thèse** — la PR [#261](https://github.com/JM-Brun/J-DriftX/pull/261) est fusionnée et documente les limites de provenance. Le PDF versionné n'a pas été comparé octet à octet avec le PDF HAL ; le téléchargement automatisé HAL a été bloqué. Les droits de redistribution ne sont pas établis.
- **Chapitre Springer 2008** — le recueil complet reste dans le dépôt conformément à la décision explicite du mainteneur ; voir [sa fiche de provenance](../raw/provenance/2008-glowinski-neittaanmaki-recueil-springer.pdf.md). La conservation du fichier est une décision opérationnelle, pas une conclusion juridique.
- **Manuscrit 2009 et article JESA 2010** — le manuscrit auteur HAL est identifié séparément. Le PDF final JESA (vol. 44, nos 4–5, pp. 445–461, DOI 10.3166/jesa.44.445-461) n'est pas obtenu/authentifié. Aucune comparaison de version ne doit être déclarée terminée.

## Travail restant, par ordre de dépendance

1. **Contrôle visuel de l'article 2006** : obtenir un fac-similé officiel accessible ; confirmer les symboles et signes des équations (1), (2), (4) et de la contrainte intégrale p. 636 ; consigner page imprimée et page PDF.
2. **Authentification de la thèse** : obtenir légalement le PDF HAL, comparer taille et SHA-256 calculés sur les octets des deux fichiers, puis comparer titre, pagination et contenu. Un SHA Git de blob n'est pas un SHA-256 du PDF.
3. **Comparaison 2009/2010** : obtenir la version de record JESA ou une copie dont l'identité éditoriale peut être établie ; comparer équations, unités, domaines, sources/puits et pagination avec le manuscrit HAL 2009.
4. **Bilan du modèle lointain** : à partir de formules authentifiées, spécifier le domaine, la grandeur conservée, le jacobien, les termes temporels, sources/puits, dépôt et frontières. Si les sources ne donnent pas une carte suffisante, conclure que la revendication n'est pas reconstructible à partir des éléments disponibles.
5. **Registre et matrice de traçabilité** : mettre à jour les statuts de [docs/46](46-registre-erreurs-incoherences-documentaires.md) et de l'issue #232 sans effacer l'historique ni créer des tests redondants.
6. **Clôture scientifique** : ne fermer l'issue #123 qu'une fois les étapes accessibles terminées ou explicitement classées comme bloquées par indisponibilité documentaire ; préserver les inconnues comme inconnues.

## Critère d'arrêt scientifique

En l'absence d'une source primaire lisible qui définit la transformation historique et les termes du bilan, la conclusion rigoureuse est : **la conservation est une contrainte annoncée historiquement ; la cohérence dimensionnelle de la première branche a été reconstruite pour J-DriftX ; la preuve de conservation du modèle historique général n'est pas établie**. Ne pas combler cette lacune par un solveur général, un benchmark ou une hypothèse géométrique non sourcée.
