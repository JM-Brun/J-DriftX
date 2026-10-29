# 47 — Contrat minimal de la baseline : statut des capacités historiques

**Statut.** Note de cadrage exécutant l’étape 2 de l’ordre confirmé de l’[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : figer, pour chaque capacité historique du périmètre Drift-X, un statut de définition parmi **définie**, **partiellement définie**, **annoncée seulement** et **non reproductible avec les sources disponibles**. Ce contrat ne modifie aucun code, ne crée aucune entrée de registre et ne clôt aucune issue ; chaque statut est amendable uniquement par décision explicite du propriétaire, appuyée sur une preuve, une transcription ou une authentification nouvelle.

**Date :** 29 octobre 2026. **Base documentaire :** notes [43](43-audit-these-brun-conservation-g0s.md), [44](44-strategie-reprise-et-elargissement-scientifique.md), [45](45-audit-article-mohammadi-brun-2006.md) et [46](46-registre-erreurs-incoherences-documentaires.md) (intégrées via la PR #229), investigations [19](19-investigation-g0s-temps-de-parcours.md), [31](31-investigation-champ-multiniveaux.md), [32](32-conservation-coordonnees-travel-time.md) et [37](37-transformation-tau-eta-cas-uniforme.md), fiches de bibliographie/sources, tests du dépôt.

## 1. Définitions des statuts

Les définitions suivantes figent le vocabulaire de l’étape 2. Elles qualifient la capacité **historique telle que les sources la définissent**, jamais la reconstruction moderne du dépôt, qui est suivie séparément (couche « reconstruction » de la [note 44](44-strategie-reprise-et-elargissement-scientifique.md) §2) :

- **Définie.** Les sources accessibles impriment la capacité de façon complète et vérifiable : objets, équations, unités, domaine, conditions d’entrée et cas limites, sans choix laissé au lecteur. Une implémentation fidèle est possible sans invention.
- **Partiellement définie.** L’objet principal est imprimé et transcrit, mais des choix restent nécessaires avant implémentation : lecture à arbitrer entre formulations non équivalentes, base à fixer, heuristique à spécifier, ou formule exacte à certifier sur fac-similé. Une reconstruction étiquetée est possible sous hypothèses explicites.
- **Annoncée seulement.** La capacité est revendiquée ou décrite dans les sources, mais la définition nécessaire à une implémentation (équations certifiées, protocole, paramètres, identifiabilité) n’est pas disponible dans le corpus accessible.
- **Non reproductible avec les sources disponibles.** Des transcriptions existent mais sont incohérentes entre elles ou dimensionnellement incompatibles sous les unités explicites des sources, sans convention identifiée qui résolve l’écart. Aucune implémentation fidèle n’est possible ; seule une reconstruction explicitement divergente peut être construite et testée.

**Règle de progression (ordre #232) :** une incertitude historique ne bloque que la partie qui en dépend. Elle n’empêche pas d’implémenter et de vérifier une reconstruction clairement étiquetée sous des hypothèses explicites.

## 2. Synthèse — statuts figés

| Capacité historique | Statut figé | Verrou principal | Références |
|---|---|---|---|
| Similitude (profils de panache) | Partiellement définie | Équation (2) de 2006 certifiée visuellement (PR #277, 29/10/2026) ; champ proche lié aux mesures non intégralement transcrit ; interprétation des paramètres de (2) non précisée dans la source | [note 45](45-audit-article-mohammadi-brun-2006.md) §1 ; [note 43](43-audit-these-brun-conservation-g0s.md) §3 |
| Transport dirigé (temps de transport, pseudo-distance) | Partiellement définie | Existence/unicité des caractéristiques et règle de départage des projections non formalisées dans les sources | [note 45](45-audit-article-mohammadi-brun-2006.md) §2 ; [note 19](19-investigation-g0s-temps-de-parcours.md) ; DRX-ERR-001/002/015 |
| Champ multi-niveaux | Partiellement définie | Lecture R3 arbitrée mais base non fixée ; formulation non vérifiée entre les versions 2009–2010 | [note 31](31-investigation-champ-multiniveaux.md) ; DRX-ERR-012 |
| Évaluation réduite (coût ponctuel) | Annoncée seulement | Facteur 10³–10⁴ rapporté sans protocole récupérable | [note 45](45-audit-article-mohammadi-brun-2006.md) §5 ; DRX-ERR-005 |
| Assimilation (calibration, identification) | Partiellement définie (requalifiée le 29/10/2026, cf. §7) | Équations (1) et (4) transcrites visuellement (PR #277), mais l’équation (4) imprimée reste ambiguë et sous-spécifiée (DRX-ERR-016) ; identifiabilité non établie | [note 45](45-audit-article-mohammadi-brun-2006.md) §1 et §4 ; DRX-ERR-004/016 |
| Bilan sources/puits (conservation, diffusion, dépôt) | Non reproductible avec les sources disponibles | Incompatibilités dimensionnelles confirmées dans les bilans imprimés ; aucun bilan complet source–diffusion–dépôt–frontières | [note 46](46-registre-erreurs-incoherences-documentaires.md) ; DRX-ERR-003/007/008/009/011/014 |

**Constat central : aucune capacité historique n’atteint le statut « définie ».** La baseline est donc entièrement une reconstruction au sens de la [note 44](44-strategie-reprise-et-elargissement-scientifique.md) §2 ; les cas exacts déjà implémentés et testés (champ uniforme, 1D à vitesse constante) sont des reconstructions vérifiées, pas des transcriptions.

## 3. Détail par capacité

### 3.1 Similitude — partiellement définie

Ce que les sources impriment :

- 2006, équation (2) : profil c(x,y) = c_c(x) f(y, δ(x)), avec décroissance axiale et profil transversal dépendant de l’épaisseur δ(x) ; la formule exacte a été certifiée visuellement sur le fac-similé versionné le 29/10/2026 (PR #277 : c(x,y) = c_c(x) f(y, δ(x)) avec décroissances exponentielles imprimées) ; l’interprétation des paramètres reste à préciser ([note 45](45-audit-article-mohammadi-brun-2006.md) §1).
- Thèse, chapitre 5 (§5.6.3, p. 101) : le modèle local fixe les unités (concentration kg·m⁻³, coefficient de calibration s⁻¹) et calcule des pertes de masse par intégration volumique ou par flux vertical intégré dans le temps ([note 43](43-audit-these-brun-conservation-g0s.md) §3).
- 2008, p. 245–246 (OCR) : le champ proche de la buse est construit sur des observations expérimentales ; les solutions de similitude pour couches de mélange et panaches sont « connues en métrique cartésienne », la contribution originale étant leur généralisation en métrique travel-time ([fiche chapitre 2008](bibliographie/sources/brun-mohammadi-2008-chapitre.md)).

Ce qui est vérifié côté dépôt : une famille de profils reconstruite (panache gaussien, classes de Pasquill, formes de Briggs, réflexion au sol) est implémentée et testée, bilan de masse compris ([tests/test_similitude.py](../tests/test_similitude.py)). Ces tests valident la reconstruction moderne, pas une transcription historique.

Verrous : transcription visuelle de l’équation (2) de 2006 levée le 29/10/2026 (PR #277) ; transcription intégrale du chapitre 5 de la thèse (seuls les passages dimensionnels ont été audités) ; le champ proche « construit sur mesures » n’est pas défini précisément dans le corpus accessible.

Premier sous-ensemble exécutable : la reconstruction gaussienne existante, étiquetée reconstruction, sur le cas de référence à champ uniforme (étape 3 de l’ordre #232).

### 3.2 Transport dirigé — partiellement définie

Ce que les sources impriment : 2006, §3, définit la pseudo-distance orientée par caractéristique issue de A et projection de B, avec avertissements explicites — séparation, symétrie et inégalité triangulaire peuvent échouer ; caractéristique unique supposée ; projection possiblement non unique, départage heuristique par une relation de type u·∇c = 0. La thèse, §7.1.3 (p. 126–127), reprend la construction par trajectoire et projection en supposant la caractéristique unique ([note 43](43-audit-these-brun-conservation-g0s.md) §1).

Ce qui est formalisé et vérifié : la [note 19](19-investigation-g0s-temps-de-parcours.md) distingue les objets (temps d’arrivée, temps projeté) ; le cas exact 1D à vitesse constante, la forme fermée du champ uniforme et le coût de polyligne sont implémentés et testés ([tests/test_metric.py](../tests/test_metric.py), [tests/test_experience_uniforme.py](../tests/test_experience_uniforme.py)) ; le contre-exemple de cisaillement démontre que le coût projeté n’est pas une coordonnée travel-time régulière ([tests/test_shear_projected_cost.py](../tests/test_shear_projected_cost.py), [note 32](32-conservation-coordonnees-travel-time.md)).

Verrous : existence/unicité des caractéristiques et des projections non formalisées dans les sources (DRX-ERR-002) ; règle de départage heuristique à spécifier et tester ; cas de stagnation, projections multiples et sortie de domaine non traités dans la source. La non-symétrie et l’échec de l’inégalité triangulaire sont des limites reconnues par les auteurs, pas des erreurs (DRX-ERR-001, [note 46](46-registre-erreurs-incoherences-documentaires.md) §4 règle 5).

Justification du statut : la capacité est définie dans les cas exacts restreints (1D à vitesse constante, champ uniforme) et partiellement définie pour la construction générale ; le statut global figé est « partiellement définie ».

### 3.3 Champ multi-niveaux — partiellement définie

Ce que la source imprime : le manuscrit HAL 2009 (§2.1.1), transcrit dans la [note 31](31-investigation-champ-multiniveaux.md) — cascade de domaines rectangulaires emboîtés, champ total [S2], restriction de vitesse [S3] sous deux formulations non équivalentes, identité de flux, restriction de concentration [S4] et règle des quatre points.

Ce qui est démontré ([note 31](31-investigation-champ-multiniveaux.md) §2) : la lecture R1 (égalité des potentiels aux coins) est sous-déterminée ; la lecture R2 (interpolation bilinéaire des vitesses de coins) contredit l’identité de flux annoncée par la source (contre-exemple explicite) ; la lecture R3 (potentiel harmonique ajusté aux vitesses de coins) est cohérente mais non unique — la base reste à fixer. Le champ total est discontinu aux frontières de niveaux ; la garantie historique se lit comme un bilan de flux par niveau, pas comme une divergence ponctuelle du champ total.

Arbitrage enregistré : R3 retenue par le propriétaire sur l’[issue #42](https://github.com/JM-Brun/J-DriftX/issues/42) le 28/10/2026. Restent ouverts : choix de la base harmonique (proposition dans la [note 31](31-investigation-champ-multiniveaux.md) §4) et comparaison différentielle du PDF éditeur JESA 2010 avec le manuscrit auteur HAL 2009. Ce dernier a désormais été transcrit et contrôlé visuellement sur les pages PDF 5–10 dans la [note 55](55-releve-equations-manuscrit-2009-comparaison-jesa.md) ; cette transcription ne certifie pas l’identité avec la version de record JESA et ne remplace pas la comparaison éditeur. Le contrat d’implémentation est prêt ([note 31](31-investigation-champ-multiniveaux.md) §4–5) ; la capacité n’est pas implémentée.

Verrous : base non arbitrée ; comparaison inter-versions non faite ; construction exacte du champ grossier ũ_0 = ũ_H renvoyée par la source aux travaux antérieurs sans définition complète.

### 3.4 Évaluation réduite — annoncée seulement

Ce que les sources impriment : 2006 (résumé et §5) revendique le calcul de la solution en un point sans résoudre d’EDP et rapporte un facteur de réduction d’environ 10³ à 10⁴ par évaluation ponctuelle, face à un maillage d’environ 3 000 points, croissant avec la taille du problème ; 2008 (résumé) revendique l’accès à la solution en un point sans calcul sur tout le domaine.

Ce qui manque : paramètres, code, tailles exactes, tolérances, coûts de préparation et de calibration du protocole historique — le facteur rapporté est contextuel et non généralisable (DRX-ERR-005, [note 45](45-audit-article-mohammadi-brun-2006.md) §5).

Distinction de contrat : le mécanisme (évaluer un profil de similitude en un point via le coût dirigé) est exécutable comme reconstruction et sera mesuré par le benchmark de l’étape 5 de l’ordre #232, avec coûts de préparation, calibration, coût par requête, coût de champ complet, mémoire et erreur rapportés séparément. La revendication historique de coût, elle, reste « annoncée seulement » : le benchmark mesurera la reconstruction, il ne validera pas le chiffre historique.

### 3.5 Assimilation — partiellement définie (requalifiée le 29/10/2026, cf. §7)

Ce que les sources impriment : 2006 présente l’équation (1) comme un problème d’assimilation des paramètres du modèle à partir d’observations de vitesse et de concentration, et l’équation (4) comme reconstruction du champ de vitesse dérivé d’un potentiel avec formulation d’optimisation ; 2008 (résumé) : l’identification des paramètres est fondée sur l’assimilation de données, avec renvoi à la sensibilité incomplète ; Applied Geomatics 2009 (résumé) reprend la même revendication.

Ce qui manque : les équations (1) et (4) sont désormais transcrites visuellement (PR #277, 29/10/2026) — (1) comme somme de deux normes sans pondération visible ; mais l’équation (4) imprimée reste ambiguë et sous-spécifiée : indice d’observation absent sous la somme, incompatibilité dimensionnelle conditionnelle et divergence non nulle en général (DRX-ERR-016, [note 45](45-audit-article-mohammadi-brun-2006.md) §1 et §4) ; conditions aux limites, espaces fonctionnels et identifiabilité des objectifs et paramètres ne sont établis nulle part dans le corpus accessible.

Distinction de contrat : le module d’identification de source du dépôt (forme fermée sur cas synthétique, [note 36](36-identification-source.md)) est une extension R1 du projet, pas une reconstruction de l’assimilation historique ; il ne peut pas être cité comme reproduction de cette capacité.

Verrous : formulation mathématique non ambiguë de l’équation (4) (toute correction est une hypothèse distincte, DRX-ERR-016) ; définition des objectifs et paramètres identifiables — condition préalable à toute reconstruction.

### 3.6 Bilan sources/puits — non reproductible avec les sources disponibles

Ce que les sources impriment : 2006 lie une intégrale globale de concentration sur le volume à la quantité totale émise, sans démonstration complète (DRX-ERR-003) ; 2008 (équation (2.2), p. 248) et la thèse (équations (7.12)–(7.13), p. 129) présentent deux branches alternatives pour c⁺ puis une quantité C = ∫ c⁺ dσ « devant être conservée » ; le manuscrit auteur HAL 2009 `hal-00468863` imprime en §2.1.1 une identité de masse après l’équation [4] et en §2.1.2 une définition de C_a avec l’élément dV (note 55 ; DRX-ERR-017/018). Les équations (28)–(31) mentionnées dans des transcriptions antérieures sont absentes de ce manuscrit désigné et restent non attribuées (DRX-ERR-008/009). Le terme de dépôt de 2006 est calibré dans le cas à vitesse uniforme pour retrouver la solution analytique.

Anomalies confirmées (registre [note 46](46-registre-erreurs-incoherences-documentaires.md), sous les unités conventionnelles explicites de chaque audit) : les deux branches de c⁺ ne sont pas dimensionnellement équivalentes (DRX-ERR-007, DRX-ERR-011 — la branche intégrée en hauteur donne une masse, la branche produit donne M L⁻¹) ; l’identité de masse imprimée après l’équation [4] du manuscrit auteur HAL 2009 présente une incompatibilité dimensionnelle conditionnelle (DRX-ERR-017), de même que la définition de C_a avec dV (DRX-ERR-018). Les équations (28) et (29)–(31) de transcriptions antérieures sont absentes du manuscrit désigné et restent non attribuées (DRX-ERR-008, DRX-ERR-009) ; elles ne doivent pas lui être attribuées. L’occurrence « 2/3 = 0.636 » est arithmétiquement incohérente (DRX-ERR-010) ; les équations locales ∇·uₗ = 0 et uₗ·∇cₗ = 0 ne forment pas un bilan complet avec sources, dépôt et frontières (DRX-ERR-014). Aucune source accessible n’identifie une convention ou un facteur manquant qui résoudrait ces écarts. La comparaison exacte avec la version de record JESA 2010 reste à effectuer (DRX-ERR-012) ; cela ne remet pas en cause l’audit du manuscrit HAL désigné.

Conséquence de contrat : le bilan historique n’entre pas dans la baseline comme capacité héritée. Une reconstruction reste possible en choisissant et documentant des conventions explicites — par exemple la branche intégrée en hauteur, seule dimensionnellement compatible avec un inventaire de masse ([note 43](43-audit-these-brun-conservation-g0s.md) §3). Les tests de conservation existants ([tests/test_similitude.py](../tests/test_similitude.py)) et les tests dimensionnels ([tests/test_documentary_dimensional_audit.py](../tests/test_documentary_dimensional_audit.py)) valident cette reconstruction, jamais les formulations imprimées. Toute convergence future entre versions authentifiées pourra requalifier ce statut.

## 4. Instantané d’accès aux sources

| Source | Accès | État de vérification |
|---|---|---|
| Mohammadi & Brun (2006), C. R. Mécanique | Texte intégral via le site de l’éditeur ; extraction versionnée dans le dépôt | Équations (1), (2) p. 635 et (4) p. 636 vérifiées visuellement sur le binaire versionné le 29/10/2026 (PR #277) ; autres équations non certifiées ; empreinte du binaire non comparée au PDF officiel ([note 45](45-audit-article-mohammadi-brun-2006.md) §8) |
| Thèse de Brun | Texte consulté via une copie miroir tierce ; PDF présent dans le dépôt | Page de titre, pagination, identité binaire avec HAL et droits non vérifiés (DRX-ERR-013) ; métadonnées divergentes entre notices ([fiche thèse](bibliographie/sources/these-brun.md)) |
| Brun & Mohammadi (2008), chapitre Springer | OCR des p. 245–246 uniquement | p. 247–256 non transcrites ; accès légal à une transcription intégrale à établir ([fiche chapitre 2008](bibliographie/sources/brun-mohammadi-2008-chapitre.md)) |
| Manuscrit auteur HAL 2009 (Bozon, Sinfort, Mohammadi), `hal-00468863` | PDF versionné dans `raw/` et contrôlé visuellement | Pages PDF 5–10 contrôlées visuellement ; équations [1]–[7], hypothèses, sources/puits et conditions aux limites relevés dans la [note 55](55-releve-equations-manuscrit-2009-comparaison-jesa.md). L’identité ligne à ligne avec la version éditeur JESA n’est pas certifiée |
| Bozon & Mohammadi (2009), Applied Geomatics | Résumé et extraits uniquement | Texte intégral sur abonnement ([fiche Applied Geomatics](bibliographie/sources/bozon-mohammadi-2009-applied-geomatics.md)) |
| JESA 2010 | PDF déjà obtenu par une voie appropriée, non versionné dans `raw/` ; notice HAL `hal-02594312` et DOI `10.3166/jesa.44.445-461` identifiés | La [note 55](55-releve-equations-manuscrit-2009-comparaison-jesa.md) fixe le relevé du manuscrit HAL 2009 et le protocole différentiel. Le contrôle direct du PDF éditeur et la comparaison équation par équation restent à documenter ; réutiliser exclusivement le fichier déjà obtenu, sans relancer l’acquisition (DRX-ERR-012) |

Cet instantané justifie la règle de progression : la baseline ne peut pas attendre l’authentification parfaite de toutes les sources.

## 5. Premier sous-ensemble exécutable

Conformément à l’ordre #232 (choisir un premier sous-ensemble exécutable plutôt que d’attendre l’authentification parfaite), la baseline gèle le périmètre suivant, entièrement étiqueté reconstruction :

1. **Similitude reconstruite** : panache gaussien, classes de Pasquill, formes de Briggs, réflexion au sol (existant, testé).
2. **Transport dirigé** : cas exacts 1D à vitesse constante et champ uniforme, coût de polyligne, contre-exemple de cisaillement comme garde-fou (existant, testé).
3. **Évaluation ponctuelle du mécanisme** reconstruit, sur le cas de référence autonome de l’étape 3 (écoulement uniforme : unités, domaine, conditions aux limites, observable, limites ; cisaillement en contre-exemple distinct).
4. **Champ multi-niveaux R3** : première extension conditionnelle, après arbitrage de la base et comparaison des versions.
5. **Assimilation et bilan sources/puits** : reconstructions explicitement divergentes après la baseline (étapes 5–6), jamais présentées comme capacités héritées.

La matrice ligne par ligne des revendications, versions, unités, hypothèses et preuves est maintenue séparément dans la [note 49](49-matrice-revendications-baseline.md). Elle complète ce contrat synthétique sans dupliquer les fiches d'anomalies de la note 46.

## 6. Ce que ce contrat ne fait pas

- Il ne modifie aucune transcription, aucun code, aucun test.
- Il n’ajoute aucune entrée au registre ([note 46](46-registre-erreurs-incoherences-documentaires.md)) : aucun fait nouveau n’y est consigné.
- Il ne clôt pas l’[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) : les critères d’acceptation (matrice de traçabilité versionnée, cas analytique reproductible, comparaison à référence indépendante) restent à produire dans les étapes 3 à 6.
- Les statuts figés peuvent être requalifiés par le propriétaire sur preuve (transcription fac-similé, authentification de version, démonstration), avec trace dans cette note et, le cas échéant, dans le registre.

## 7. Trace de requalification (29 octobre 2026)

Conformément à la section 6, les statuts et verrous ci-dessus sont amendés par décision du propriétaire, sur preuve :

- **Preuve.** Contrôle visuel du PDF éditeur 2006 versionné (équations (1), (2) p. 635 et (4) p. 636) et du texte JESA de comparaison désigné (HAL `hal-00468863`, équations [1]–[7]), intégré par la PR #277 (fusionnée), transcription littérale et sans réparation conjecturale.
- **Décision du propriétaire.** La même PR relève CL-03 et CL-04 de la [note 49](49-matrice-revendications-baseline.md) à « partiellement définie » ; le registre enregistre les anomalies conditionnelles nouvelles (DRX-ERR-016/017/018, PR #278) et requalifie DRX-ERR-004/008/009/012.
- **Amendements de cette note.** (a) similitude : le verrou de transcription visuelle de l’équation (2) est levé, le statut « partiellement définie » est inchangé (champ proche et interprétation des paramètres restent ouverts) ; (b) assimilation : « annoncée seulement » devient « partiellement définie » — les équations sont transcrites, mais la formulation imprimée de (4) reste ambiguë (DRX-ERR-016) et l’identifiabilité n’est pas établie ; (c) instantané de la section 4 actualisé (fac-similé partiellement vérifié, texte JESA désigné).
- Les statuts « annoncée seulement » de l’évaluation réduite et « non reproductible » du bilan sources/puits sont inchangés.

## Références internes

- [Audit de la thèse : conservation G0-S](43-audit-these-brun-conservation-g0s.md)
- [Stratégie de reprise et d’élargissement](44-strategie-reprise-et-elargissement-scientifique.md)
- [Audit de l’article Mohammadi & Brun (2006)](45-audit-article-mohammadi-brun-2006.md)
- [Registre des erreurs et incohérences](46-registre-erreurs-incoherences-documentaires.md)
- [Investigation du champ multi-niveaux](31-investigation-champ-multiniveaux.md)
- [Conservation en coordonnées travel-time](32-conservation-coordonnees-travel-time.md)
- [Transformation tau-eta : cas uniforme](37-transformation-tau-eta-cas-uniforme.md)
- [Issue #232 — baseline scientifique](https://github.com/JM-Brun/J-DriftX/issues/232)
- [Issue #233 — registre central](https://github.com/JM-Brun/J-DriftX/issues/233)
- [Issue #42 — qualification des propriétés](https://github.com/JM-Brun/J-DriftX/issues/42)
- [Issue #123 — conservation G0-S](https://github.com/JM-Brun/J-DriftX/issues/123)
