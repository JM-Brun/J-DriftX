# Synthèse et état historique de l'accès aux sources — corpus Drift-X

> **Document historique.** Les tableaux de disponibilité et la liste d'extraction proviennent d'octobre 2026. Ils préservent le raisonnement bibliographique d'origine, mais ne font pas foi comme backlog ni comme état actuel des accès. Les décisions courantes sont portées par les issues publiques propriétaires et l'index des sources.
>
> Pour les fiches individuelles, voir l'[index des revues par source](../04-revues-papiers-sources.md). Les synthèses thématiques se trouvent dans [`docs/bibliographie/`](../bibliographie/).

## Vue d'ensemble et accès aux sources (instantané d'octobre 2026)

| # | Source | Accès en ligne (oct. 2026) | Information extraite dans cette revue |
|---|---|---|---|
| 1 | Brun, *Modélisation à complexité réduite de la dérive* (référence primaire citée en 2006 comme thèse Université Montpellier II, 2007) | Texte intégral non localisé dans les sources consultées ; statut de dépôt/numérisation non établi | Citation bibliographique primaire confirmée ; page de titre et année de soutenance non vérifiées |
| 2 | Mohammadi & Brun 2006 (C. R. Mécanique) | PDF éditeur et extraction automatique des cinq pages présents dans `raw/`; selon la correction de la PR #143, accès direct au PDF non vérifié dans l'environnement de relecture et lecture publique qualifiée de partielle | Synthèse des sections et extraction texte disponibles ; formules, figures et conventions historiques à recontrôler visuellement sur le PDF original |
| 3 | Mohammadi, Brun & Pironneau 2006 (chapitre) | Non localisé | Citation exacte via bibliographie du papier n° 7 |
| 4 | Brun & Mohammadi 2008 (Springer, chap. 14) | Chapitre fourni par l'auteur ; relais public ResearchGate | Résumé + pages 245–246 (OCR) : introduction et début de la section ROM |
| 5 | Bozon, Mohammadi & Sinfort 2008 (e-sta) | Non localisé (archives introuvables) ; métadonnées attestées : vol. 5, n° 2, p. 182–192 | Citation exacte via bibliographie des papiers n° 6 et 7 |
| 6 | Bozon, Sinfort & Mohammadi 2009 (STIC & Env. / HAL) + version journal JESA 2010 | Manuscrit auteur de 17 pages et extraction automatique présents dans `raw/`; provenance HAL hal-00468863, fichier HAL d'origine `MO2009-PUB00026817.pdf`, extraction récupérée via relais ResearchGate ; version JESA 2010 distincte, DOI 10.3166/jesa.44.445-461 | Synthèse fondée sur le manuscrit et son extraction ; équations et figures doivent être vérifiées sur le PDF. Ne pas traiter le manuscrit HAL et l'article JESA comme deux sources indépendantes sans comparaison de versions |
| 7 | Bozon & Mohammadi 2009 (Applied Geomatics) | Résumé libre ; texte intégral sur abonnement | Résumé verbatim, extraits d'introduction et bibliographie |

Points notables de cette campagne de relecture : la source n° 6 s'est révélée la plus riche — le manuscrit auteur complet est accessible et documente l'architecture logicielle historique (cœur Fortran + plugin QGIS) et la construction multi-niveaux. Une **version journal inédite dans notre bibliographie** a été identifiée et vérifiée (JESA 2010, DOI valide). Détail en section 8.



## Découvertes bibliographiques

1. **Version journal JESA 2010 du papier plateforme** : *Journal Européen des Systèmes Automatisés* 44(4-5), 445–461, DOI 10.3166/jesa.44.445-461 — DOI vérifié (il résout vers la page revue, accès réservé) ; vol/pages/année confirmés par la notice ResearchGate de la publication. Ajoutée à <code>references.md</code> et <code>site/references.qmd</code>.
2. **Référence de la thèse.** L'article primaire de 2006 cite le titre « Modélisation à complexité réduite de la dérive », l'Université Montpellier II et l'année 2007 (voir §1). Des sources secondaires divergent ; la citation primaire ne remplace pas la vérification de la page de titre.
3. **Lignée méthodologique confirmée** : les bibliographies des sources 4, 6 et 7 pointent toutes vers Borouchaki–George–Mohammadi 1997 (métriques de maillage), Mohammadi–Pironneau (k-epsilon, Applied Shape Optimization 2001) — la matrice intellectuelle « métrique + optimisation de forme + sensibilité » du projet est ainsi traçable dans les sources elles-mêmes.
4. **Commanditaires académiques du papier plateforme** : affiliations Cemagref–UMR ITAP, Montpellier SupAgro–UMR ITAP et Université Montpellier 2–UMR5149 (I3M) — documentées pour la fiche « héritage » du site.

5. **Soumission IJNMF jamais retrouvée** : la bibliographie du CR 2006 cite « B. Mohammadi, J.-M. Brun, Reduced-order geometrical modelling of dispersion, Int. J. Num. Meth. Fluids, 2006, submitted for publication » — aucune trace d'une publication sous ce titre n'a été trouvée (publication abandonnée, retitrée, ou jamais parue ?). À clarifier de mémoire d'auteur ; ce serait une huitième source potentielle du corpus.
6. **Année de la thèse — discordance entre sources** : l'article primaire de 2006 cite **2007**, tandis que certaines bibliographies secondaires indiquent 2006. Traiter 2007 comme l'année de la référence bibliographique citée, pas comme année de soutenance indépendamment vérifiée ; vérifier la page de titre ou une notice institutionnelle avant de figer cette dernière.
7. **Chaîne adjointe historique** : en 2006, le gradient était produit par différentiation automatique inverse via **Tapenade** (INRIA) — l'adjoint « analytique et gratuit » revendiqué ensuite s'est construit sur cette base.
8. **Meilleur accès au CR 2006** : le PDF de l'article est en accès libre sur l'archive ouverte de l'Académie des sciences (comptes-rendus.academie-sciences.fr) — lien ajouté aux bibliographies et extraction texte brute archivée dans <code>raw/extracts/</code>.



## Ancienne liste d'extraction documentaire — historique, non backlog courant

| Priorité | Action | Verrou |
|---|---|---|
| Clôturée | Thèse : pas de dépôt HAL (décision du 23/10/2026) — ajout ultérieur au corpus par l’auteur, année à arbitrer sur la page de titre à cette occasion | Document en possession de l’auteur ; relecture après ajout |
| Haute | Compléter l'analyse du chapitre 2008 au-delà des pages 245–246 (exemples numériques, analyse de sensibilité, identification de source) | Recueil complet non distribué ; utiliser une source légalement accessible et vérifier les droits avant toute extraction intégrale |
| Clôturée | e-sta 2008 : pas de dépôt HAL (décision du 23/10/2026) ; métadonnées attestées (vol. 5, n° 2, p. 182–192) = référence bibliographique complète | Texte intégral introuvable en ligne — état définitif (section 10) |
| Moyenne | Localiser le recueil Springer 2006 du chapitre Mohammadi–Brun–Pironneau | Recueil introuvable en accès ouvert |
| ~~Moyenne~~ | ~~Obtenir le texte intégral CR Mécanique 2006~~ — **fait** (archive ouverte Académie) | Reste Applied Geomatics 2009 (abonnement / tiré-à-part auteur) |
| Moyenne | Statut de la soumission IJNMF 2006 (« Reduced-order geometrical modelling of dispersion ») | Publication non retrouvée — mémoire d'auteur |
| Moyenne | Ajouter les PDF originaux dans <code>raw/</code> (voir <code>raw/README.md</code>) | Manuscrits auteurs en possession de l'auteur |
| Basse | Obtenir l'exemplaire JESA 2010 de la source n° 6 pour vérifier les éventuelles évolutions vs le manuscrit HAL | Accès réservé |



## Instantané M0 des dépôts ouverts — 22 octobre 2026 (historique)

Objectif de l’issue #44 : vérifier, source par source, si le corpus historique est archivé en accès ouvert (HAL en priorité) et documenter les actions restantes. **Limite de méthode :** l’absence de résultat dans HAL, theses.fr, Sudoc ou les moteurs généraux n’est pas une preuve d’absence de dépôt ; les autodépôts listés ne peuvent être effectués que par les auteurs (versions définitives et droits).

| Source | Dépôt ouvert | État (oct. 2026) et action restante |
|---|---|---|
| Mohammadi & Brun 2006 (*C. R. Mécanique*) | HAL : non | PDF en accès libre et pérenne sur l’archive ouverte de l’Académie des sciences (§2) ; archivage satisfaisant, dépôt HAL optionnel |
| Brun & Mohammadi 2008 (chapitre Springer) | HAL : non | Chapitre fourni par l’auteur ; vérifier la politique d’autodépôt Springer puis déposer la version auteur si le contrat le permet |
| Bozon, Mohammadi & Sinfort 2008 (e-sta) | HAL : non | **Prioritaire.** Métadonnées attestées (vol. 5, n° 2, p. 182–192 — fiche 5) mais texte introuvable ; autodépôt par les auteurs |
| Bozon, Sinfort & Mohammadi 2009 (plateforme STIC & Env.) | **HAL : oui** — [hal-00468863](https://hal.science/hal-00468863) | Rien à faire : manuscrit auteur déposé et relu intégralement (fiche 6) |
| Bozon & Mohammadi 2009 (*Applied Geomatics*) | HAL : non | Autodépôt de la version auteur selon la politique Springer ; texte intégral encore sur abonnement |
| Bozon, Sinfort & Mohammadi 2010 (*JESA*) | HAL : non | DOI 10.3166/jesa.44.445-461 valide mais accès réservé ; autodépôt selon la politique Lavoisier, sinon le manuscrit HAL 2009 sert d’archive ouverte |
| Thèse Brun (2006/2007, §1) | HAL : non (introuvable aussi sur theses.fr et Sudoc) | Année discordante à arbitrer sur la page de titre ; document en possession de l’auteur — **le dépôt HAL est le prérequis de sa relecture** |

Bilan : sur sept sources, une seule est déposée sur HAL (la plus réutilisée, la plateforme 2009) ; l’article e-sta 2008 et la thèse sont les deux autodépôts à plus fort effet de levier documentaire.

**Décision du 23 octobre 2026 (issue #44).** Aucun nouvel autodépôt HAL ne sera effectué : l’état des lieux ci-dessus est définitif. La thèse sera ajoutée ultérieurement au corpus par l’auteur (l’année 2006/2007 sera arbitrée sur la page de titre à cette occasion) ; les métadonnées e-sta attestées restent la référence bibliographique complète de l’article, et le PDF libre de l’Académie des sciences (§2) comme le manuscrit hal-00468863 demeurent les deux archives ouvertes de référence du corpus.

---

*Fiches établies uniquement à partir de contenus extraits et vérifiables ; extractions texte brutes archivées dans <code>raw/extracts/</code> ; les passages verbatim sont en anglais ou français d'origine, non reformulés silencieusement. Sources d'accès consultées en octobre 2026 : EM-consulte (notice CR Mécanique), HAL hal-00468863 via relais ResearchGate, notice Springer/Applied Geomatics, OCR du chapitre Springer 2008 fourni par l'auteur.*
