# Audit adversarial — méthode, statut documentaire et qualité des preuves

> **Périmètre :** conserver les règles de niveau de preuve et les constats portant sur la méthode de recherche, les statuts de projet, les checklists périmées et la qualité documentaire. Cette note ne remplace pas les issues propriétaires.

> Le registre d'entrée est [`docs/15-audit-adversarial-hallucinations.md`](../15-audit-adversarial-hallucinations.md). Les constats bibliographiques sont dans [l'audit des références](15a-audit-bibliographique.md), et les constats de portée scientifique dans [l'audit des affirmations](15b-audit-portee-scientifique.md).

## Registre des constats


## Échelle de confiance à utiliser dans les futures fiches

- **Vérifié sur source primaire :** notice officielle ou texte intégral consulté ; localiser l'affirmation (page, section, équation).
- **Métadonnées vérifiées, contenu non lu :** DOI/éditeur/catalogue confirmé, mais pas de conclusion sur le contenu.
- **Rapporté par une source secondaire :** attribuer explicitement l'information à cette source ; ne pas la traiter comme vérification indépendante.
- **Non localisé / non confirmé au [date] :** indique l'état de la recherche, jamais une preuve d'inexistence.
- **Hypothèse de J-DriftX :** proposition à tester, non résultat.
- **Résultat reproduit :** protocole, code, données, métrique, baseline et sortie vérifiables.
- **Réfuté / erroné :** réserver ce statut à une contradiction positive démontrée.


## Protocole de traque continue

Pour chaque référence ou affirmation non triviale :
1. Vérifier titre, auteurs, année, support, volume/pages et DOI/URL dans une source bibliographique primaire ou un catalogue institutionnel.
2. Résoudre DOI/URL et comparer les métadonnées de la page cible avec la citation.
3. Lire le texte primaire pertinent ; enregistrer pages, équations, conditions et limites.
4. Rechercher les versions (prépublication, manuscrit auteur, article final) et éviter le double comptage.
5. Pour les affirmations quantitatives, retrouver le tableau/figure/protocole exact et conserver les conditions de comparaison.
6. Pour les affirmations mathématiques, vérifier les hypothèses et tenter un contre-exemple ; ne pas confondre propriété du champ historique et propriété de l'implémentation actuelle.
7. Vérifier les liens internes, les citations de pages Quarto, les extraits OCR et les fichiers PDF associés.
8. Marquer explicitement les points ouverts et la preuve attendue pour fermer chacun.


## Limites de cet audit

Cet audit est une première passe ciblée sur les références historiques et les revendications scientifiques les plus susceptibles d'être amplifiées. Les contrôles web n'ont pas établi l'inexistence des références non retrouvées. Les PDF de revue systématique, l'intégralité des pages Quarto, les métadonnées de chaque entrée de bibliographie et tous les liens du dépôt doivent encore être examinés systématiquement. Les conclusions doivent donc rester proportionnées aux preuves effectivement consultées.

## Deuxième passe — vérification bibliographique externe (2026-10-22)

Cette seconde passe a comparé environ 45 références et affirmations du dépôt à des sources externes (Crossref, OpenAlex, HAL, Zenodo, Persée, Federal Register, sites éditeur et institutionnels). Elle complète la première passe : les constats A-xx portaient sur le risque de sur-affirmation ; les constats B-xx ci-dessous portent sur des erreurs bibliographiques ou des associations source-affirmation. Conformément à l'échelle du § 3, « erroné » désigne ici une contradiction positive démontrée avec la source primaire.


## Couverture et limites de la deuxième passe

- **Vérifié :** environ 45 références/affirmations, principalement sur les métadonnées (DOI, notices Crossref/OpenAlex/Springer/HAL/Zenodo, Federal Register, Persée, pages institutionnelles) et, pour quelques affirmations chiffrées, sur le contenu des documents.
- **Non couvert :** fiches `raw/fiches/*` page à page, PDF de `raw/reviews/*`, pages Quarto individuelles, liens institutionnels individuels (MODISAFE, R-LINE, Cefas, barrières near-road EPA, HARMO, Hamburg EWTL).
- **Prudence :** « erroné » doit être réservé aux contradictions positives (B-01, B-02, B-04, B-05, B-07) ou à une association démontrée (B-03). B-06 est désormais classé non vérifié ; B-08 est une imprécision ; B-09 précise que l'existence d'une citation secondaire ne valide pas toutes les métadonnées. Les entrées non couvertes ne sont ni vraies ni fausses : elles restent à contrôler.



### A-11 — Statut G0 contradictoire dans la documentation

- **Statut :** incohérence de statut confirmée ; formulation corrigée dans cette PR.
- **Emplacement :** `docs/11-g0-evidence-externe.md` et `docs/14-seance-validation-experimentale.md`.
- **Constat :** `docs/11` déclarait d'abord « G0 n'est pas franchi », puis plus loin « G0 est franchi ». La séance de validation utilisait en parallèle G0-S/G0-A sans distinguer clairement ces pistes du jalon documentaire G0. Le lecteur pouvait conclure à tort que le cadrage global restait bloqué, ou au contraire que la validation applicative était autorisée.
- **Correction effectuée dans cette PR :** le premier statut est désormais explicitement historique et remplacé par la mise à jour ; la séance distingue le jalon G0 déclaré franchi des travaux scientifiques encore ouverts et des prérequis G1 sur les fichiers bruts.
- **Réserve :** « G0 franchi » signifie que le cadrage documentaire est rempli selon les critères du projet ; cela ne signifie pas que les données ont été validées au niveau des fichiers, que la licence DIFLU est confirmée ou qu'un benchmark a été exécuté.


## Modifications réalisées dans la PR de suivi

Cette PR de suivi ne se limite donc plus au registre initial. Elle :
- ajoute le registre d'audit et conserve les constats A-01 à A-14 ainsi que B-01 à B-28 avec leur niveau de preuve ;
- corrige des affirmations excessives dans la revue d'état de l'art et distingue les hypothèses J-DriftX des résultats établis ;
- corrige la relation DATEM/ETEX dans le catalogue de données et clarifie le statut G0 par rapport aux prérequis G1 ;
- corrige les métadonnées Turbelin et al. (2014), Bozon & Mohammadi (2009), Arcucci et al. (2023) et la date de la ressource Zenodo (2026) ;
- sépare la source CAREA sur les sources complexes (Teggi et al., 2018) de l'étude d'exposition aux pesticides (Costanzini et al., 2018) ;
- requalifie la référence ScienceDirect PII S2666449621000372 comme non vérifiée (les métadonnées et l'association à POD+RBF ne sont pas confirmées), distingue l'année de publication en ligne de l'année de volume pour l'article Seveso, complète des métadonnées bibliographiques et borne l'interprétation du speed-up U-FNO ×4000 et des ratios de performance du ROM Vervecken et al. (2015) ;
- retire les affirmations non étayées sur l'absence de dépôt de la thèse et précise que l'année officielle doit être vérifiée sur la page de titre.

Les changements n'établissent pas encore la validité de chaque référence du corpus. Les PDF de revue exécutive, les métadonnées bibliographiques complètes et les fichiers bruts de données restent à auditer. Le `main` actuel inclut une étape CI qui installe Quarto et rend le site ; elle a réussi sur le contenu du site de cette PR lors du contrôle disponible. Ce succès de compilation ne remplace pas la revue du contenu scientifique.



### B-20 — Scores de « crédibilité » sans barème et colonne de date ambiguë

- **Statut :** précision méthodologique non justifiée, corrigée.
- **Emplacement :** tableau « Notes de sources » de `docs/02-revue-etat-art-2026.md`.
- **Constat :** les valeurs 2/5 à 5/5 n'étaient accompagnées d'aucun barème observable (type de source, revue par les pairs, accès au texte, indépendance, risque de biais). Elles donnaient donc une apparence de quantification sans procédure reproductible. La colonne « Dernière mise à jour » mélangeait en outre années de publication, dates de version et mises à jour de pages web.
- **Correction effectuée :** les notes numériques ont été remplacées par une description du type de source et de ses limites de lecture ; l'en-tête devient « Année de publication ou version », avec les cas de dates distinctes explicités.
- **Preuve de clôture :** si un score de qualité documentaire est réintroduit, définir des critères, des ancrages observables et une procédure de double-évaluation avant de noter les sources.


### B-28 — Roadmap et revue G0 : statut de porte obsolète après la décision documentaire

- **Statut :** contradiction de statut corrigée.
- **Emplacements :** `site/projet/roadmap.qmd`, `docs/10-revue-adversariale-g0.md`.
- **Constat :** après la décision du 22 octobre 2026, qui a fait franchir G0 au niveau documentaire sur la base du cadrage et de l'audit de corpus, certaines pages continuaient à dire que G0 « reste bloqué » ou à présenter le prochain test comme conditionné à un franchissement futur de G0. Cela confondait le jalon documentaire G0 avec G0-A (utilité applicative) et G1 (audit des fichiers/licences).
- **Correction effectuée :** les pages précisent désormais que G0 documentaire est franchi, que G0-A reste non démontré et que G1/benchmark restent bloqués jusqu'à la vérification des fichiers bruts et des licences.
- **Preuve de clôture :** garder les statuts synchronisés dans la roadmap, la fiche G0, l'audit des corpus et les pages publiques ; ne pas traiter le franchissement documentaire comme une autorisation de benchmark.


### B-29 — Plan de validation et roadmap interne : statut G0 périmé et prochaine action obsolète

- **Statut :** contradiction documentaire confirmée et corrigée.
- **Emplacements :** `docs/03-roadmap-jdriftx-v2.md`, `docs/05-plan-validation-et-integration.md`, `docs/08-decision-utilite-et-preuve.md`.
- **Constat :** ces documents continuaient à présenter G0 comme le jalon immédiat à franchir ou à demander la rédaction future de la fiche G0, alors que la fiche et l'audit des corpus actent un franchissement documentaire le 22 octobre 2026. Un passage de `docs/08` disait également que la distinction G0-S/G0-A ne signifiait pas que G0 était franchi, ce qui contredisait le statut documentaire enregistré ailleurs.
- **Correction effectuée :** la roadmap distingue désormais G0 documentaire (franchi), G0-A (utilité applicative non démontrée), G1 (cohérence théorique et vérification des fichiers bruts) et G2 (valeur différentielle non évaluée). Le plan de validation nomme DIFLU comme corpus candidat au test discriminant, sous réserve de l'audit G1. La prochaine action demande de vérifier les fichiers bruts et de préparer un protocole, non de refaire le cadrage G0.
- **Limite :** ces corrections harmonisent le statut documentaire ; elles ne valident pas les fichiers, les licences, la pertinence physique du corpus ni la performance de J-DriftX.
- **Preuve de clôture :** vérifier après chaque décision que les statuts des documents de gouvernance restent cohérents et qu'aucun benchmark n'est annoncé avant le contrôle G1.


### B-32 — Liens internes Quarto non résolus détectés par la CI

- **Statut :** deux liens internes cassés confirmés et corrigés dans cette PR.
- **Emplacements :** `site/projet/utilite-scientifique.qmd`, `site/etat-art/revue-mathematique.qmd`.
- **Constat :** le rendu Quarto de la CI signalait `projet/15-audit-corpus-g0-resultats.md` et `etat-art/mvp-scientifique.qmd` comme cible introuvable. Les documents visés existaient, mais les chemins relatifs étaient erronés depuis les pages sources. Le rendu réussissait malgré ces avertissements : un rendu vert seul ne prouve donc pas que tous les liens internes sont résolus.
- **Correction effectuée :** les liens pointent désormais respectivement vers `../../docs/15-audit-corpus-g0-resultats.md` et `../projet/mvp-scientifique.qmd`.
- **Preuve de clôture :** nouveau rendu Quarto sans ces avertissements. À terme, ajouter un contrôle de liens internes explicite au workflow plutôt que compter uniquement sur le succès de `quarto render`.
