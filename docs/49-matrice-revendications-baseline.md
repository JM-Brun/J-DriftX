# 49 — Matrice initiale des revendications historiques pour la baseline

**Statut :** matrice initiale de traçabilité, non exhaustive. Elle opérationnalise l'étape 1 de l'[issue #232](https://github.com/JM-Brun/J-DriftX/issues/232) sans remplacer les audits source ni le [registre des anomalies](46-registre-erreurs-incoherences-documentaires.md). Les références de page sont celles relevées dans les audits ; lorsqu'une équation n'a pas été contrôlée visuellement sur le fac-similé, cela est indiqué explicitement.

**Règle de lecture :** « défini dans la source » ne signifie pas « démontré » ou « validé ». Les statuts de définition suivent le [contrat minimal de baseline](47-contrat-minimal-baseline.md). Les reconstructions du dépôt sont distinctes des revendications historiques.

## 1. Matrice des revendications

| ID | Revendication / objet | Source et localisation | Unités / hypothèses requises | Preuve actuellement disponible | Statut historique |
|---|---|---|---|---|---|
| CL-01 | Profil de similitude du panache : concentration en fonction de la distance et du profil transversal | Mohammadi & Brun (2006), équation (2), p. 635 selon l'audit [45](45-audit-article-mohammadi-brun-2006.md) | Concentration kg·m⁻³ ; coordonnées et échelle de dispersion en m ; débit et vitesse dans la formule complète | Extraction texte disponible ; formule exacte non certifiée visuellement sur le fac-similé. Reconstruction gaussienne du dépôt testée séparément | **Partiellement définie** |
| CL-02 | Temps de transport / pseudo-distance dirigée par caractéristique issue de A et projection de B | Mohammadi & Brun (2006), §3, pp. 635–636 selon [45](45-audit-article-mohammadi-brun-2006.md) ; thèse, §7.1.3, pp. 126–127, [43](43-audit-these-brun-conservation-g0s.md) | Champ, domaine, régularité, existence des caractéristiques, définition/unicité de projection ; le coût est temporel si l'intégrande est (ds/\|u\|) | Cas uniforme et 1D constant testés ; contre-exemple de cisaillement testé ; existence/unicité générales et règle de départage non établies | **Partiellement définie** |
| CL-03 | Champ de vitesse reconstruit par optimisation à partir d'un potentiel | Mohammadi & Brun (2006), équation (4), p. 636 selon [45](45-audit-article-mohammadi-brun-2006.md) | Vitesse m·s⁻¹ ; potentiel, fonctionnel, contraintes et conditions aux limites à expliciter | Extraction insuffisante pour certifier opérateurs, signes, fonctionnel et conditions aux limites ; transcription visuelle non confirmée | **Annoncée seulement** |
| CL-04 | Assimilation des paramètres à partir d'observations de vitesse et de concentration | Mohammadi & Brun (2006), équation (1), p. 635 selon [45](45-audit-article-mohammadi-brun-2006.md) | Unités/nature des paramètres et observations, fonction de coût, bruit et identifiabilité | Formule non certifiable depuis l'extraction ; identifiabilité non établie dans les sources accessibles | **Annoncée seulement** |
| CL-05 | Réduction du coût d'une évaluation ponctuelle d'environ 10³–10⁴ par rapport à un calcul sur maillage | Mohammadi & Brun (2006), résumé et §5, pp. 637–638 selon [45](45-audit-article-mohammadi-brun-2006.md) | Précision comparable ; taille du maillage, préparation, calibration, coût par requête, coût total et mémoire à distinguer | Chiffre rapporté ; protocole complet et coûts de préparation récupérables non établis | **Annoncée seulement** |
| CL-06 | Contrainte intégrale globale reliant concentration volumique et quantité émise | Mohammadi & Brun (2006), §3, p. 636 selon [45](45-audit-article-mohammadi-brun-2006.md) | Concentration kg·m⁻³, volume m³ ; durée/source, puits, dépôt et frontières à préciser | Un bilan global ne prouve pas un flux conservé sur chaque surface iso-temps ; formule non certifiée visuellement | **Partiellement définie** |
| CL-07 | Quantité (C=\int c^+\,d\sigma) annoncée comme conservée, avec deux alternatives imprimées pour (c^+) | Brun & Mohammadi (2008), équation (2.2), p. imprimée 248 ; thèse, équations (7.12)–(7.13), p. 129 ; [43](43-audit-these-brun-conservation-g0s.md), [46](46-registre-erreurs-incoherences-documentaires.md) | Sous ([c_l]=M L^{-3}), les deux branches ne sont pas dimensionnellement équivalentes ; la branche produit intégrée sur une aire donne (M L^{-1}), pas une masse | Incompatibilité établie sous l'interprétation conventionnelle ; convention alternative ou facteur omis non exclus ; scan à vérifier | **Non reproductible avec les sources disponibles** |
| CL-08 | Bilans entrée/sortie en coordonnées de transport | Bozon & Mohammadi (2009), équation (28), puis équations (29)–(31) ; [32](32-conservation-coordonnees-travel-time.md), [46](46-registre-erreurs-incoherences-documentaires.md) | Unités volumiques et de bord cohérentes ; transformation, jacobien, normales, sources/puits et frontières explicités | Incompatibilités dimensionnelles sous les unités conventionnelles ; manuscrit 2009 distinct de JESA 2010, version de record non authentifiée | **Non reproductible avec les sources disponibles** |
| CL-09 | Champ multi-niveaux construit par restriction/interpolation sur des domaines emboîtés | Manuscrit HAL 2009, §2.1.1 ; [31](31-investigation-champ-multiniveaux.md) | Domaine de chaque niveau, données aux coins, base de reconstruction, continuité et bilan de flux par niveau | Lecture bilinéaire contredite par un contre-exemple ; potentiel harmonique cohérent mais non unique, base non fixée | **Partiellement définie** |
| CL-10 | Bilan local à partir de (\nabla\cdot u_l=0) et (u_l\cdot\nabla c_l=0) | [32](32-conservation-coordonnees-travel-time.md) et DRX-ERR-014 dans [46](46-registre-erreurs-incoherences-documentaires.md) | Un bilan complet exige sources, dépôt, frontières et flux ; divergence nulle seule ne suffit pas | Dérivation conditionnelle avec jacobien disponible ; transformation historique générale non reconstituée | **Partiellement définie** |

## 2. Interprétation des statuts

- **Définie :** aucune revendication générale du périmètre historique n'atteint actuellement ce statut.
- **Partiellement définie :** l'objet est identifiable, mais des hypothèses, choix ou preuves manquent ; une reconstruction peut être testée sous conditions explicites.
- **Annoncée seulement :** la capacité ou le résultat est revendiqué, mais la définition ou le protocole nécessaire à sa reproduction manque.
- **Non reproductible avec les sources disponibles :** les formulations accessibles ne peuvent être implémentées fidèlement tant que les incompatibilités ou conventions non identifiées persistent. Cela ne prouve pas que toute reconstruction moderne soit impossible.

Ces statuts décrivent la reproductibilité documentaire, pas l'utilité de la méthode ni la validité globale de Drift-X.

## 3. Incertitudes prioritaires

1. Contrôler visuellement les équations 2006 (1), (2) et (4) sur le fac-similé éditeur ; enregistrer la transcription exacte, la version du fichier et les incertitudes de lecture. Ne pas inférer les équations depuis le code actuel.
2. Authentifier la version finale JESA 2010 et la comparer au manuscrit HAL 2009 avant d'attribuer à la version publiée les anomalies du manuscrit.
3. Borner le premier cas exécutable à la reconstruction déjà testée en champ uniforme ; reporter assimilation et conservation historique tant que leurs définitions ne sont pas établies.
4. Ajouter ici toute nouvelle revendication, et un pointeur dans le registre 46 seulement si une anomalie distincte le justifie. Ne pas recopier l'analyse détaillée.

## 4. Frontières des documents

- **Cette matrice (49) :** revendication, source/version/localisation, unités/hypothèses, preuve et statut.
- **Contrat minimal (47) :** décision synthétique par capacité et périmètre de la première reconstruction exécutable.
- **Registre des anomalies (46) :** identifiant stable, qualification, impact, action et historique de résolution.
- **Notes d'audit et d'investigation :** transcription et raisonnement détaillés par source ou question.
- **Issue [#232](https://github.com/JM-Brun/J-DriftX/issues/232) :** suivi des critères d'acceptation et de la baseline implémentée.

Cette matrice est une première version : une ligne dont la source primaire n'a pas été inspectée reste non certifiée ; les statuts ne sont relevés que sur preuve nouvelle et traçable.
