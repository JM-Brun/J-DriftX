# Lecture ciblée — rapport InVS sur l'exposition aérienne aux pesticides (2009)

## Provenance et statut

- **Document analysé :** Christine Ricoux, *Évaluation de l’exposition aérienne aux pesticides de la population générale — Étude en air extérieur dans quatre sites de l’Hérault en 2006*, Institut de veille sanitaire, publié le 1 mars 2009.
- **Notice source :** https://www.santepubliquefrance.fr/regions-et-territoires/occitanie/rapportsynthese/evaluation-de-lexposition-aerienne-aux-pesticides-de-la-population-generale-etude-en-air-exterieur
- **PDF officiel dont le texte a été consulté :** https://www.santepubliquefrance.fr/sites/default/files/rdd/document/82748_9958-9958-ps.pdf
- **Fichier local concerné :** `raw/2009-invs-exposition-aerienne-pesticides-herault.pdf`, ancien nom `82748_9958-9958-ps.pdf`.
- **Méthode :** lecture du texte rendu par le parseur PDF de la page officielle (pages PDF 0–23, soit couverture/sommaire et corps du rapport jusqu'à la conclusion). Ce fichier est une synthèse ciblée et paraphrasée, pas une extraction OCR intégrale du binaire local.
- **Pagination :** la notice officielle annonce 55 pages. Le parseur expose 58 pages physiques, avec pagination imprimée du rapport allant jusqu'à p. 55. La correspondance binaire entre le PDF en ligne et celui versionné localement n'a pas été vérifiée par empreinte.
- **Date de rédaction de la note :** 2026-10-28.

## Protocole rapporté

L'étude vise à caractériser l'exposition par inhalation aux pesticides dans quatre sites de l'Hérault. Les prélèvements ont été organisés en deux campagnes : janvier/février 2006 hors période de traitement, puis juin 2006 pendant la période de traitement. Un site fixe en milieu agricole (Mas du Piquet, Grabels) est comparé à des sites mobiles urbain, périurbain et rural, avec des données d'épandage et météorologiques.

## Résultats quantitatifs utiles pour une vérification ultérieure

Valeurs ci-dessous reprises des tableaux 2 et 3 et de la synthèse narrative du rapport ; elles ne constituent pas une série complète :

| Période | Site | Substance | Concentration rapportée |
|---|---|---|---:|
| Janvier 2006, hors traitement | Prés d'Arènes (urbain) | Folpel | 28 ng/m³ |
| Janvier 2006, hors traitement | Prés d'Arènes (urbain) | Procymidone | 19 ng/m³ |
| Janvier 2006, hors traitement | Saint-Gély-du-Fesc (semi-rural) | Folpel | 15 ng/m³ |
| Janvier 2006, hors traitement | Saint-Gély-du-Fesc (semi-rural) | Procymidone | 14 ng/m³ |
| Juin 2006, période de traitement | Mas du Piquet (agricole) | Chlorpyrifos éthyl | 33 ng/m³ |
| Juin 2006, période de traitement | Prés d'Arènes (urbain) | Chlorpyrifos éthyl | 5 ng/m³ |
| Juin 2006, période de traitement | Pic Saint-Loup (rural) | Chlorpyrifos éthyl | 0,6 ng/m³ |
| Juin 2006, période de traitement | Mas du Piquet (agricole) | Flusilazole | 2 ng/m³ |

Sources précises : tableau 2, p. imprimée 12 (parseur PDF page 12) ; tableau 3, p. imprimée 13 (parseur PDF page 13) ; discussion des résultats, pp. imprimées 14–18 (parseur PDF pages 14–18).

## Interprétation et limites

- Les concentrations totales les plus importantes de folpel et procymidone sont observées en janvier, hors période de traitement, dans les sites urbain et semi-rural. Le rapport indique qu'aucun épandage local recensé n'explique directement ces observations.
- En juin, le chlorpyrifos éthyl domine les mesures et la valeur maximale indiquée dans le tableau 3 est 33 ng/m³ au Mas du Piquet.
- Le rapport examine la cohérence entre mesures, épandages, calendrier et météo ; une simple correspondance entre une valeur observée et une émission modélisée serait insuffisante.
- Les mesures sont ponctuelles, propres à certaines molécules et fenêtres de prélèvement. Elles ne forment pas, en l'état, un benchmark générique de dispersion atmosphérique ni une vérité terrain directement comparable à la sortie d'un modèle sans reconstruire le protocole, la géométrie des sites, les conditions météo et les incertitudes.
- Les résultats sanitaires/toxicologiques ne sont pas repris ici ; cette note porte uniquement sur le protocole de mesure et les valeurs de concentration utiles à l'audit scientifique.

## Suite recommandée

1. Comparer par SHA-256 le PDF local et le téléchargement officiel avant de qualifier la copie locale d'identique.
2. Extraire l'intégralité du PDF local avec un outil déterministe, puis vérifier manuellement les tableaux et unités.
3. Décider si les métadonnées disponibles suffisent pour une étude de cas de plausibilité, sans prétendre à une validation quantitative complète de J-DriftX.
