# 44 — Registre des erreurs et incohérences documentaires

**Statut :** registre initial, incomplet et évolutif. Les entrées ci-dessous reprennent des anomalies déjà relevées dans les audits disponibles ; elles ne remplacent pas la vérification des sources primaires. Une anomalie signalée n'est pas nécessairement une erreur démontrée.

**Règle de conservation :** ne jamais corriger silencieusement une transcription historique. Conserver la forme publiée ou manuscrite, identifier la version exacte, puis documenter séparément l'analyse, la correction proposée et la reconstruction retenue pour J-DriftX.

**Suivi :** [issue #233 — registre central](https://github.com/JM-Brun/J-DriftX/issues/233). La [matrice de l'issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) suit les revendications et leur vérification ; ce registre suit les problèmes documentaires, leurs preuves, impacts et résolutions.

## 1. Statuts et niveaux de preuve

- **Confirmé** : l'erreur ou l'incompatibilité est démontrée sous les définitions explicitement indiquées.
- **Probable** : les indices sont forts, mais une source ou hypothèse reste à vérifier.
- **Ambigu / non tranché** : plusieurs interprétations demeurent possibles ; l'intention des auteurs n'est pas établie.
- **Réfuté** : l'anomalie supposée ne tient pas après vérification.
- **Résolu** : une correction ou décision est justifiée par une preuve vérifiable ; préciser s'il s'agit d'une résolution documentaire, mathématique ou numérique.

Impact : **critique** (conclusion centrale ou bilan physique potentiellement invalide), **majeur** (résultats ou reproductibilité affectés), **modéré** (interprétation/comparaison affectée), **mineur** (erreur locale sans impact établi). La sévérité décrit l'impact potentiel, pas le degré de certitude.

## 2. Registre initial

| ID | Source / localisation | Observation | Qualification actuelle | Impact potentiel et action |
|---|---|---|---|---|
| DRX-ERR-001 | Mohammadi & Brun (2006), pp. 635–636, pseudo-distance ; [audit note 43](43-audit-article-mohammadi-brun-2006.md) | La pseudo-distance orientée peut ne pas vérifier séparation, symétrie ni inégalité triangulaire. | Limite structurelle explicitement reconnue par les auteurs, pas une erreur démontrée. | Modéré. Préserver l'orientation et ne pas imposer artificiellement les axiomes d'une métrique standard. |
| DRX-ERR-002 | Mohammadi & Brun (2006), caractéristiques et projection ; [audit note 43](43-audit-article-mohammadi-brun-2006.md) | Existence/unicité des caractéristiques et unicité de projection sont supposées ou traitées par heuristique sans spécification complète dans le texte accessible. | Hypothèses insuffisamment formalisées ; erreur de source non établie. | Majeur. Transcrire le fac-similé, formaliser domaine/régularité et tester stagnation, projections multiples, trajectoires inatteignables et sorties de domaine. |
| DRX-ERR-003 | Mohammadi & Brun (2006), p. 636, contrainte intégrale globale ; [notes 43](43-audit-article-mohammadi-brun-2006.md) et [32](32-conservation-coordonnees-travel-time.md) | L'intégrale globale de concentration sur le volume, associée à la quantité émise, ne démontre pas à elle seule la constance du flux sur chaque surface iso-temps. | Distinction logique confirmée ; validité du bilan physique historique à reconstruire. La formule doit être contrôlée visuellement, le PDF éditeur ayant été inaccessible lors de l'audit. | Critique. Vérifier la transcription, unités, durée d'émission, sources/puits, dépôt et frontières ; tester des cas analytiques. |
| DRX-ERR-004 | Mohammadi & Brun (2006), p. 636, équation (4) sur le champ de vitesse ; [audit note 43](43-audit-article-mohammadi-brun-2006.md) | L'extraction texte ne permet pas de certifier opérateur, signes, fonctionnel d'optimisation, contraintes et conditions aux limites. | Incertitude de transcription, pas une erreur de l'article établie. | Majeur. Transcrire depuis le fac-similé avant implémentation et contrôler unités et conditions aux limites. |
| DRX-ERR-005 | Mohammadi & Brun (2006), pp. 636–638 ; [audit note 43](43-audit-article-mohammadi-brun-2006.md) | Le facteur de réduction annoncé, environ 10³–10⁴ par évaluation ponctuelle, dépend du protocole et des tailles de problème rapportés. | Résultat historique contextuel ; généralisation non démontrée, ce n'est pas en soi une erreur. | Majeur si présenté comme accélération universelle. Reproduire à précision comparable et séparer coût de préparation, calibration, coût par requête, champ complet, mémoire et erreur. |
| DRX-ERR-006 | Mohammadi & Brun (2006), pp. 637–638 ; [audit note 43](43-audit-article-mohammadi-brun-2006.md) | Le texte indique que les campagnes de mesure de terrain nécessaires à la validation sont prévues ultérieurement. | Limite de preuve explicitement documentée, pas une erreur. | Majeur si des simulations sont présentées comme validation terrain indépendante. Distinguer résultats synthétiques et validation empirique. |
| DRX-ERR-007 | Brun & Mohammadi (2008), §2.2, équation (2.2), p. imprimée 248 ; [note 32](32-conservation-coordonnees-travel-time.md) | Deux alternatives sont imprimées pour c⁺ : intégrale verticale de cₗ ou produit uₗ⁺cₗ, puis C = ∫ c⁺ dσ est présenté comme quantité à conserver. Sous [cₗ] = M L⁻³ et uₗ⁺ sans dimension, les deux alternatives ne sont pas dimensionnellement équivalentes ; la seconde intégrée sur une aire donne M L⁻¹, pas M. | Incompatibilité dimensionnelle confirmée sous l'interprétation conventionnelle ; convention différente ou facteur omis non exclus. Intention des auteurs ambiguë. | Critique. Vérifier le scan et les conventions de notation ; ne pas corriger la formule publiée sans preuve. |
| DRX-ERR-008 | Bozon & Mohammadi (2009), équation (28) ; [note 32](32-conservation-coordonnees-travel-time.md) | Une intégrale volumique de concentration est égalée à une intégrale de bord de concentration multipliée par une direction de vitesse normalisée et une normale ; sous l'interprétation volumique conventionnelle, les unités diffèrent d'un facteur de longueur. | Incompatibilité dimensionnelle confirmée sous l'interprétation indiquée ; omission ou convention alternative non établie. | Critique. Comparer article publié et manuscrit auteur, et déterminer si un facteur manque sans inférer l'intention. |
| DRX-ERR-009 | Bozon & Mohammadi (2009), équations (29)–(31) ; [note 32](32-conservation-coordonnees-travel-time.md) | Si c_inj est un débit massique, K = ∫ c_inj dt est une masse ; C_g = ∫ c dz a les unités M L⁻², mais l'équation (31) intègre C_g dV, donnant M L, incompatible avec K. | Incompatibilité dimensionnelle confirmée sous cette interprétation. Remplacer dV par dx dy est une correction possible, mais l'intention n'est pas établie. | Critique. Comparer les versions, vérifier la mesure d'intégration attendue et consigner les unités de chaque terme. |
| DRX-ERR-010 | Bozon & Mohammadi (2009), occurrence « 2/3 = 0.636 » rapportée dans l'audit du corpus | 2/3 ≈ 0,667 ; 0,636 est proche de 2/π ≈ 0,637. | Erreur arithmétique confirmée dans la transcription rapportée ; expression voulue inconnue. Page et contexte exacts à ré-ancrer à la source. | Modéré à majeur selon l'usage. Vérifier le fac-similé, retrouver les calculs dépendants et corriger uniquement la reconstruction. |
| DRX-ERR-011 | Thèse de Brun, équations (7.12)–(7.13), p. 129 selon [audit note 41](41-audit-these-brun-conservation-g0s.md) | M_C = ∫ c⁺ dσ est présenté comme devant être conservé ; contexte, unités et hypothèses doivent être comparés aux articles. | Question ouverte ; ne pas classer comme erreur sans examiner le passage source. | Critique si la propriété est supposée sans hypothèses dans la baseline. Vérifier PDF, pagination, définitions et comparaison avec 2006/2008. |
| DRX-ERR-012 | Manuscrit HAL hal-00468863 (2009) vs article JESA 44(4–5), 445–461 (2010) ; [références](references.md) | Les versions sont des objets bibliographiques distincts ; la version finale JESA n'est pas encore authentifiée dans le corpus de l'audit. | Provenance partiellement établie ; ne pas traiter le manuscrit comme identique à la version finale. | Majeur. Obtenir et authentifier la version de record puis comparer pagination, équations, figures et formulations avant d'attribuer une anomalie aux deux versions. |
| DRX-ERR-013 | PDF de thèse présent sur une branche de travail | Titre de page, pagination, identité avec le fichier HAL et droits de redistribution restent à vérifier. | Provenance non entièrement vérifiée ; pas une erreur scientifique établie. | Majeur pour la citation et la reproductibilité. Vérifier page de titre, métadonnées, concordance et droits. |
| DRX-ERR-014 | Brun & Mohammadi (2008), §2.1 ; [note 32](32-conservation-coordonnees-travel-time.md) | ∇·uₗ = 0 et uₗ·∇cₗ = 0 ne constituent pas, à eux seuls, un bilan complet avec sources, dépôt et pertes aux frontières. | Limite de portée mathématique confirmée ; les équations peuvent rester cohérentes pour le modèle local idéal annoncé. | Majeur si elles sont interprétées comme modèle physique complet avec pertes. Définir le domaine de validité avant extension. |
| DRX-ERR-015 | Construction projetée en cisaillement ; [issue #123](https://github.com/JM-Brun/J-DriftX/issues/123) et [note 32](32-conservation-coordonnees-travel-time.md) | Pour u(x,y) = (v(y),0), v(y)>0, d_A = (x−x_A)/v(y_A) donne u·∇d_A = v(y)/v(y_A), non identiquement égal à 1 si v varie. | Contre-exemple analytique confirmé pour cette construction et ce champ ; il ne réfute pas toutes les méthodes de temps de parcours. | Critique si le coût projeté est traité automatiquement comme coordonnée travel-time régulière. Garder le test de régression et distinguer les deux objets. |

## 3. Comparaisons inter-documents prioritaires

### 3.1 Conservation : objets distincts

| Source | Quantité ou affirmation | État actuel |
|---|---|---|
| Mohammadi & Brun (2006) | Intégrale globale de concentration sur le volume associée à la quantité émise | Ne prouve pas à elle seule un flux constant sur chaque surface iso-temps ; transcription visuelle à confirmer. |
| Brun & Mohammadi (2008) | C = ∫ c⁺ dσ, « devrait être conservé », avec deux définitions imprimées de c⁺ | Les alternatives ne sont pas dimensionnellement équivalentes sous la convention volumique standard. |
| Thèse de Brun, équations (7.12)–(7.13) | M_C = ∫ c⁺ dσ, conservation revendiquée | Contexte, unités et hypothèses à vérifier ; équivalence avec les articles non établie. |
| Bozon & Mohammadi (2009) | Bilans d'entrée/sortie dans les équations (28)–(31) | Plusieurs incompatibilités dimensionnelles sous les unités conventionnelles ; intention de correction inconnue. |
| Note mathématique actuelle, §4 | Égalité de flux sous transformation de coordonnées régulière et bilan conditionnel | Résultat conditionnel ; ne valide pas automatiquement la construction historique. |

### 3.2 Versions et provenance

- **Article de 2006 :** l'extraction texte permet une première analyse, mais formules et figures ne sont pas toutes vérifiées visuellement. Ne pas classer un problème de transcription comme erreur de la source avant accès au fac-similé.
- **Chapitre Springer de 2008 :** conserver la pagination imprimée (notamment p. 248 pour l'équation (2.2)) et distinguer la pagination du PDF.
- **Manuscrit HAL 2009 et article JESA 2010 :** ne pas fusionner leurs anomalies tant que la version de record n'est pas authentifiée et comparée.
- **Thèse :** l'audit de la note 41 est partiel ; l'identité du binaire, les métadonnées et les droits restent à vérifier.

## 4. Règles de mise à jour

1. Attribuer un identifiant DRX-ERR-NNN stable ; ne jamais réutiliser un identifiant retiré.
2. Indiquer document, version, page imprimée et page PDF si différentes, section, équation/figure ou lignes de code.
3. Séparer observation, raisonnement, hypothèse, impact, correction proposée et preuve restante.
4. Expliciter les définitions et unités supposées dans toute conclusion dimensionnelle.
5. Ne pas qualifier d'erreur une propriété volontairement reconnue par les auteurs, par exemple la non-symétrie de la pseudo-distance.
6. Ne déclarer une anomalie résolue qu'avec preuve, test ou décision argumentée liée à une issue/PR.
7. Conserver l'identifiant et l'historique après résolution ; ajouter la preuve au lieu d'effacer l'entrée.
8. Distinguer correction de transcription, correction mathématique, changement de modèle et validation empirique.
9. Lier les audits spécialisés plutôt que copier leurs analyses en plusieurs endroits.
10. Les sources historiques ne sont jamais réécrites silencieusement ; la reconstruction moderne doit indiquer ses écarts.

## 5. Travaux restants

- [ ] Vérifier visuellement équations et figures de l'article 2006 à partir d'un fac-similé lisible.
- [ ] Comparer systématiquement les bilans de conservation de la thèse, du chapitre 2008, de l'article 2009 et de la version JESA 2010 authentifiée.
- [ ] Ré-ancrer sur la source primaire l'occurrence « 2/3 = 0.636 » avec page, contexte et dépendances.
- [ ] Ajouter les anomalies d'autres rapports après lecture, sans extrapoler à partir de sources non consultées.
- [ ] Relier les anomalies mathématiques à un test analytique, un test dimensionnel ou une preuve explicite lorsque possible.
- [ ] Réviser statuts et impacts lorsque les sources manquantes seront disponibles.

## Références internes

- [Audit de l'article Mohammadi & Brun (2006)](43-audit-article-mohammadi-brun-2006.md)
- [Audit de la thèse : conservation G0-S](41-audit-these-brun-conservation-g0s.md)
- [Conservation en coordonnées travel-time](32-conservation-coordonnees-travel-time.md)
- [Transformation tau-eta : cas uniforme](37-transformation-tau-eta-cas-uniforme.md)
- [Références bibliographiques](references.md)
- [Issue #233 — registre central](https://github.com/JM-Brun/J-DriftX/issues/233)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
- [Issue #123 — conservation G0-S](https://github.com/JM-Brun/J-DriftX/issues/123)
