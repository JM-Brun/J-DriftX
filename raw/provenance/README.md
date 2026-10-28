# Index de provenance des sources — J-DriftX

**Audit du 28 octobre 2026.** Ce fichier complète [le README du dossier raw](../README.md) et indexe les sidecars de provenance. Il est séparé de raw/README.md pour ne pas entrer en conflit avec la PR publique #67, qui reste différée et n'est pas modifiée par cette opération.

## PDF présents et sidecars

| Fichier binaire | Provenance documentée | État / limite de vérification |
|---|---|---|
| [2006-mohammadi-brun-crmeca.pdf](../2006-mohammadi-brun-crmeca.pdf) | [Sidecar](2006-mohammadi-brun-crmeca.pdf.md) · [archive ouverte officielle C. R. Mécanique](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) | Article éditeur, 5 pages imprimées 634–638. URL officielle identifiée, mais le chemin de téléchargement ayant produit le binaire versionné n'est pas démontré. La lecture scientifique est qualifiée de partielle. |
| [2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf](../2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf) | [Sidecar](2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf.md) · [page ResearchGate du chapitre](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion) | Extrait de deux pages seulement (p. 245–246). URL directe du fichier téléchargé et date exacte non conservées. |
| [Recueil Springer 2008 complet](../Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski,%20P.%20Neittaanmaki%20(Springer,%202008)%20WW.pdf) | [Sidecar](2008-glowinski-neittaanmaki-recueil-springer.pdf.md) · [notice officielle Springer](https://link.springer.com/book/10.1007/978-1-4020-8758-5) · [copie effectivement consultée sur SGO/J. Baylie](https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf) | Le binaire est le recueil éditeur complet, pas un tiré-à-part. Le site du fichier consulté est un miroir tiers ; la notice Springer établit la référence bibliographique, pas l'origine du binaire. Droits de redistribution non arbitrés. |
| [2009-bozon-sinfort-mohammadi-driftx-hal.pdf](../2009-bozon-sinfort-mohammadi-driftx-hal.pdf) | [Sidecar](2009-bozon-sinfort-mohammadi-driftx-hal.pdf.md) · [notice HAL](https://hal.science/hal-00468863) · [PDF HAL](https://hal.science/hal-00468863/file/MO2009-PUB00026817.pdf) | Manuscrit auteur de 17 pages. L'extraction texte associée a été récupérée via ResearchGate ; cette provenance est distincte de celle du PDF HAL. La version journal JESA 2010 n'est pas le même fichier. |
| [2009-invs-exposition-aerienne-pesticides-herault.pdf](../2009-invs-exposition-aerienne-pesticides-herault.pdf) | [Sidecar](2009-invs-exposition-aerienne-pesticides-herault.pdf.md) · [URL officielle Santé publique France](https://www.santepubliquefrance.fr/content/download/186474/document_file/82748_9958-9958-ps.pdf) | Rapport d'agence ; identité du binaire du dépôt avec la version officielle et pagination à vérifier directement. Aucune extraction texte n'est présente. |
| [Résumé exécutif, partie 1](../reviews/2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf) | [Sidecar](2026-revue-systematique-jdriftx-resume-executif-partie-1.pdf.md) · [revue publique](../../docs/02-revue-etat-art-2026.md) · [revues des sources](../../docs/04-revues-papiers-sources.md) | Document interne produit pour le projet ; pas de source externe directe. La date exacte de génération n'est pas enregistrée. |
| [Résumé exécutif, partie 2](../reviews/2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf) | [Sidecar](2026-revue-systematique-jdriftx-resume-executif-partie-2.pdf.md) · [revue publique](../../docs/02-revue-etat-art-2026.md) · [revues des sources](../../docs/04-revues-papiers-sources.md) | Document interne produit pour le projet ; pas de source externe directe. La date exacte de génération n'est pas enregistrée. |

## Fichiers textuels dérivés

| Fichier | Source effectivement consultée | Périmètre / méthode |
|---|---|---|
| [extracts/2006-mohammadi-brun-crmeca.txt](../extracts/2006-mohammadi-brun-crmeca.txt) | [Archive ouverte de l'Académie des sciences](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) | Texte du papier, 5 pages imprimées 634–638 ; extraction automatique en octobre 2026. Formules à vérifier sur le PDF. |
| [extracts/2008-brun-mohammadi-springer-chap14-notes.txt](../extracts/2008-brun-mohammadi-springer-chap14-notes.txt) | Copie du recueil consultée sur SGO/J. Baylie, [notice bibliographique Springer](https://link.springer.com/book/10.1007/978-1-4020-8758-5) | Notes analytiques portant sur les pages imprimées 245–256 ; ce n'est pas un OCR verbatim. |
| [extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt](../extracts/2009-bozon-sinfort-mohammadi-driftx-hal.txt) | [Notice HAL](https://hal.science/hal-00468863), texte récupéré via le relais public ResearchGate | Manuscrit auteur complet, 17 pages selon la fiche ; extraction automatique en octobre 2026. URL directe du téléchargement ResearchGate non conservée. |

Le rapport InVS 2009 n'a pas encore d'extraction texte versionnée. Pour les trois extractions disponibles, les en-têtes indiquent la source, le périmètre de pages et la méthode connue ; les formules, figures et équations doivent être contrôlées sur les originaux.

## Version JESA 2010 — texte final non obtenu

La référence publiée est confirmée par la [notice AGRIS/INRAE](https://agris.fao.org/search/en/providers/122439/records/6798c27ed6a63682f045645d) : Bozon, Sinfort & Mohammadi, *A GIS-based atmospheric dispersion model*, *Journal Européen des Systèmes Automatisés*, 44(4), 445–461, DOI [10.3166/jesa.44.445-461](https://doi.org/10.3166/jesa.44.445-461). La notice HAL [hal-02594312](https://hal.inrae.fr/hal-02594312) est distincte du manuscrit auteur de communication [hal-00468863](https://hal.science/hal-00468863), dont le PDF porte l'en-tête STIC & Environnement 2009.

La version éditée finale JESA **n'a pas été obtenue ni authentifiée** au 28 octobre 2026. Une piste d'accès institutionnel via [ISTEX/Mir@bel](https://reseau-mirabel.info/revue/4637/Journal-europeen-des-systemes-automatises-JESA) reste à essayer avec un accès autorisé. Ne pas traiter le manuscrit HAL 2009 comme la version finale JESA et ne pas prétendre à une comparaison ligne à ligne avant récupération du bon fichier.

## Règles et limites

- Distinguer systématiquement **notice bibliographique**, **site réellement consulté**, **binaire présent dans Git**, **fichier dérivé** et **droits de redistribution**.
- Une URL officielle ou une politique générale de revue ne prouve pas que le binaire versionné est identique à la version officielle, ni que sa redistribution est autorisée.
- Les PDF n'ont pas été ajoutés, remplacés ou supprimés par cet audit. Aucun droit de redistribution n'est arbitré ici.
- La PR publique [#67](https://github.com/JM-Brun/J-DriftX/pull/67) reste différée et n'a pas été modifiée directement. Le recueil Springer complet demeure présent dans raw/ jusqu'à décision distincte sur son maintien/retrait.
