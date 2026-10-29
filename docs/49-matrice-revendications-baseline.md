# 49 — Matrice initiale des revendications historiques pour la baseline

**Statut :** matrice initiale de traçabilité, non exhaustive. Elle opérationnalise l'étape 1 de l'[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) sans remplacer les audits source ni le [registre des anomalies](46-registre-erreurs-incoherences-documentaires.md). Les références de page sont celles relevées dans les audits ; lorsqu'une équation n'a pas été contrôlée visuellement sur le fac-similé, cela est indiqué explicitement.

**Règle de lecture :** « défini dans la source » ne signifie pas « démontré » ou « validé ». Les statuts de définition suivent le [contrat minimal de baseline](47-contrat-minimal-baseline.md). Les reconstructions du dépôt sont distinctes des revendications historiques.

## 1. Matrice des revendications

| ID | Revendication / objet | Source/version et localisation | Unités / hypothèses requises | Preuve actuellement disponible | Statut historique |
|---|---|---|---|---|---|
| CL-01 | Profil de similitude du panache : concentration en fonction de la distance et du profil transversal | Mohammadi & Brun (2006), version éditeur/extraction conservée dans le dépôt (binaire non comparé au PDF officiel), équation (2), p. 635 selon l'audit [45](45-audit-article-mohammadi-brun-2006.md) | Concentration kg·m⁻³ ; coordonnées et échelle de dispersion en m ; débit et vitesse dans la formule complète | Extraction texte disponible ; formule historique exacte non certifiée visuellement sur le fac-similé. Reconstruction gaussienne du dépôt testée séparément, avec oracle scalaire indépendant du chemin d'exécution (mais pas du modèle analytique) dans [tests/test_similitude.py](../tests/test_similitude.py) | **Partiellement définie** |
| CL-02 | Temps de transport / pseudo-distance dirigée par caractéristique issue de A et projection de B | Mohammadi & Brun (2006), version éditeur/extraction conservée dans le dépôt (binaire non authentifié), §3, pp. 635–636 selon [45](45-audit-article-mohammadi-brun-2006.md) ; thèse, §7.1.3, pp. 126–127, [43](43-audit-these-brun-conservation-g0s.md) | Champ, domaine, régularité, existence des caractéristiques, définition/unicité de projection ; le coût est temporel si l'intégrande est $ds/\lVert u\rVert$ | Cas uniforme et 1D constant testés ; contre-exemple de cisaillement testé ; existence/unicité générales et règle de départage non établies | **Partiellement définie** |
| CL-03 | Champ de vitesse reconstruit par optimisation à partir d'un potentiel | Mohammadi & Brun (2006), version éditeur/extraction conservée dans le dépôt (binaire non authentifié), équation (4), p. 636 selon [45](45-audit-article-mohammadi-brun-2006.md) | Vitesse m·s⁻¹ ; potentiel, fonctionnel, contraintes et conditions aux limites à expliciter | Extraction insuffisante pour certifier opérateurs, signes, fonctionnel et conditions aux limites ; transcription visuelle non confirmée | **Annoncée seulement** |
| CL-04 | Assimilation des paramètres à partir d'observations de vitesse et de concentration | Mohammadi & Brun (2006), version éditeur/extraction conservée dans le dépôt (binaire non authentifié), équation (1), p. 635 selon [45](45-audit-article-mohammadi-brun-2006.md) | Unités/nature des paramètres et observations, fonction de coût, bruit et identifiabilité | Formule non certifiable depuis l'extraction ; identifiabilité non établie dans les sources accessibles | **Annoncée seulement** |
| CL-05 | Réduction du coût d'une évaluation ponctuelle d'environ 10³–10⁴ par rapport à un calcul sur maillage | Mohammadi & Brun (2006), version éditeur/extraction conservée dans le dépôt (binaire non authentifié), résumé et §5, pp. 637–638 selon [45](45-audit-article-mohammadi-brun-2006.md) | Précision comparable ; taille du maillage, préparation, calibration, coût par requête, coût total et mémoire à distinguer | Chiffre rapporté ; protocole complet et coûts de préparation récupérables non établis | **Annoncée seulement** |
| CL-06 | Contrainte intégrale globale reliant concentration volumique et quantité émise | Mohammadi & Brun (2006), §3, p. 636 selon [45](45-audit-article-mohammadi-brun-2006.md) | Concentration kg·m⁻³, volume m³ ; durée/source, puits, dépôt et frontières à préciser | Un bilan global ne prouve pas un flux conservé sur chaque surface iso-temps ; formule non certifiée visuellement | **Partiellement définie** |
| CL-07 | Quantité $C=\int c^+\,d\sigma$ annoncée comme conservée, avec deux alternatives imprimées pour $c^+$ | Brun & Mohammadi (2008), chapitre Springer (extraction partielle, scan non vérifié), équation (2.2), p. imprimée 248 ; thèse, PDF versionné obtenu par une voie appropriée déjà documentée (identité binaire avec le fichier HAL déjà obtenu à vérifier si ce contrôle n'est pas consigné), équations (7.12)–(7.13), p. 129 ; [43](43-audit-these-brun-conservation-g0s.md), [46](46-registre-erreurs-incoherences-documentaires.md) | Sous $[c_l]=M L^{-3}$, les deux branches ne sont pas dimensionnellement équivalentes ; la branche produit intégrée sur une aire donne $M L^{-1}$, pas une masse | Incompatibilité établie sous l'interprétation conventionnelle ; convention alternative ou facteur omis non exclus ; scan à vérifier | **Non reproductible avec les sources disponibles** |
| CL-08 | Bilans entrée/sortie en coordonnées de transport | Bozon & Mohammadi (2009), manuscrit auteur HAL `hal-00468863`, équation (28), puis équations (29)–(31) ; article JESA 2010, notice HAL distincte `hal-02594312` ; [32](32-conservation-coordonnees-travel-time.md), [46](46-registre-erreurs-incoherences-documentaires.md) | Unités volumiques et de bord cohérentes ; transformation, jacobien, normales, sources/puits et frontières explicités | Incompatibilités dimensionnelles sous les unités conventionnelles ; le manuscrit 2009 et l'article JESA 2010 sont des objets bibliographiques distincts. La notice et le PDF JESA ont été identifiés/obtenus par HAL, mais le contenu du PDF associé à `hal-02594312` n'a pas encore été comparé aux équations du manuscrit | **Non reproductible avec les sources disponibles** |
| CL-09 | Champ multi-niveaux construit par restriction/interpolation sur des domaines emboîtés | Manuscrit auteur HAL 2009 (ne pas assimiler à JESA 2010), §2.1.1 ; [31](31-investigation-champ-multiniveaux.md) | Domaine de chaque niveau, données aux coins, base de reconstruction, continuité et bilan de flux par niveau | Lecture bilinéaire contredite par un contre-exemple ; potentiel harmonique cohérent mais non unique, base non fixée | **Partiellement définie** |
| CL-10 | Bilan local à partir de $\nabla\cdot u_l=0$ et $u_l\cdot\nabla c_l=0$ | [32](32-conservation-coordonnees-travel-time.md) et DRX-ERR-014 dans [46](46-registre-erreurs-incoherences-documentaires.md) | Un bilan complet exige sources, dépôt, frontières et flux ; divergence nulle seule ne suffit pas | Dérivation conditionnelle avec jacobien disponible ; transformation historique générale non reconstituée | **Partiellement définie** |

## 2. Interprétation des statuts

- **Définie :** aucune revendication générale du périmètre historique n'atteint actuellement ce statut.
- **Partiellement définie :** l'objet est identifiable, mais des hypothèses, choix ou preuves manquent ; une reconstruction peut être testée sous conditions explicites.
- **Annoncée seulement :** la capacité ou le résultat est revendiqué, mais la définition ou le protocole nécessaire à sa reproduction manque.
- **Non reproductible avec les sources disponibles :** les formulations accessibles ne peuvent être implémentées fidèlement tant que les incompatibilités ou conventions non identifiées persistent. Cela ne prouve pas que toute reconstruction moderne soit impossible.

Ces statuts décrivent la reproductibilité documentaire, pas l'utilité de la méthode ni la validité globale de Drift-X.

## 3.1 Registre de comparaison des versions (JESA 2010 / manuscrit 2009)

**État au 29 octobre 2026 : comparaison non effectuée sur les deux fac-similés dans cette session.** La source publiée JESA est identifiée par HAL `hal-02594312` et DOI `10.3166/jesa.44.445-461`. Le manuscrit auteur de 17 pages identifié par HAL `hal-00468863` est un document distinct. Son extraction texte versionnée ne constitue pas une preuve du contenu de l'article final.

Le PDF JESA a déjà été obtenu par le mainteneur par une voie appropriée : **ne pas relancer l'acquisition**. Le fichier n'est pas présent dans le corpus `raw/` répertorié par le README, et le PDF local déjà obtenu n'était pas accessible dans l'environnement d'exécution de cette session. En conséquence, aucun verdict de différence entre les versions n'est attribué ci-dessous.

| Domaine | Manuscrit 2009 : repère existant | Contrôle requis sur JESA 2010 | Verdict actuel |
|---|---|---|---|
| Identité/version | Front matter de l'extraction : `hal-00468863, version 1`; STIC & Environnement 2009 | Vérifier page de titre, pagination imprimée, revue, volume, pages et DOI sur le PDF déjà obtenu | Versions bibliographiquement distinctes ; identité du binaire JESA non vérifiée ici |
| Temps de migration/projection | §2, équations (1)–(3) selon la pagination de l'extraction | Relever équation, orientation, intégrande, hypothèses sur champ et projection | Non comparé |
| Concentration/similitude | §2.1, équations (4)–(7) | Comparer expression exacte, variables, coefficients et dimensions | Non comparé |
| Champ multi-niveaux | §2.1.1, équations (4)–(8) dans l'extraction ; vérifier la numérotation sur le fac-similé | Comparer restrictions, interpolation, corrections de vitesse et conservation locale revendiquée | Non comparé |
| Sources/puits et quantité injectée | §2.1.2 : quantité injectée intégrée sur `[0,T]`, dépôt au sol et quantité atmosphérique résiduelle | Vérifier si les termes, domaines et définitions sont identiques ou révisés | Non comparé |
| Conditions aux limites | Flux entrant/sortant aux sous-domaines et normales dans §2.1.1–2.2 | Relever toutes les frontières, normales, hypothèses d'entrée/sortie et conditions au sol | Non comparé |
| Unités | L'extraction dégradée ne suffit pas à certifier toutes les dimensions | Refaire l'analyse dimensionnelle sur les équations lisibles et les définitions associées | Non certifié |

### Procédure de clôture

Pour chaque ligne, enregistrer les deux transcriptions, page imprimée, numéro d'équation, unités, hypothèses et catégorie de différence : **identique**, **changement éditorial**, **changement mathématique**, **ambiguïté** ou **non vérifiable**. Toute formule extraite par OCR doit être contrôlée sur le fac-similé. Si la page imprimée diffère de la page PDF, conserver les deux repères. Les écarts affectant le bilan de masse doivent pointer vers [32](32-conservation-coordonnees-travel-time.md), [43](43-audit-these-brun-conservation-g0s.md) et [46](46-registre-erreurs-incoherences-documentaires.md), sans dupliquer leur raisonnement.

Ce registre est un protocole de preuve, pas un résultat de comparaison. Les statuts CL-08 et les conclusions de conservation ne doivent pas être relevés avant l'inspection du PDF JESA.

## 3. Incertitudes prioritaires

1. Contrôler visuellement les équations 2006 (1), (2) et (4) depuis le PDF éditeur déjà versionné ; enregistrer la transcription exacte et les incertitudes de lecture. Ne pas relancer l'acquisition du document ni inférer les équations depuis le code actuel.
2. Exploiter le PDF JESA 2010 déjà obtenu via la notice HAL distincte `hal-02594312` et le comparer au manuscrit HAL 2009. L'objectif est de vérifier le contenu et les différences de version, pas de relancer la recherche ou l'acquisition bibliographique.
3. Borner le premier cas exécutable à la reconstruction déjà testée en champ uniforme ; reporter assimilation et conservation historique tant que leurs définitions ne sont pas établies.
4. Ajouter ici toute nouvelle revendication, et un pointeur dans le registre 46 seulement si une anomalie distincte le justifie. Ne pas recopier l'analyse détaillée.

## 4. Frontières des documents

- **Cette matrice (49) :** revendication, source/version/localisation, unités/hypothèses, preuve et statut.
- **Contrat minimal (47) :** décision synthétique par capacité et périmètre de la première reconstruction exécutable.
- **Registre des anomalies (46) :** identifiant stable, qualification, impact, action et historique de résolution.
- **Notes d'audit et d'investigation :** transcription et raisonnement détaillés par source ou question.
- **Issue [#232](https://github.com/JM-Brun/J-DriftX/issues/232) :** suivi des critères d'acceptation et de la baseline implémentée.

Cette matrice est une première version : une ligne dont la source primaire n'a pas été inspectée reste non certifiée ; les statuts ne sont relevés que sur preuve nouvelle et traçable.
