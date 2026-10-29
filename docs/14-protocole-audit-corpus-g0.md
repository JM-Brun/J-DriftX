# Protocole d'audit des corpus de validation G0

> **Statut : protocole historique, à ne pas utiliser comme backlog actif.** L'issue #13 est close comme remplacée ; le suivi opérationnel est réparti entre [#204 (DIFLU)](https://github.com/JM-Brun/J-DriftX/issues/204), [#205 (ETEX/DATEM)](https://github.com/JM-Brun/J-DriftX/issues/205), [#206 (ERIES)](https://github.com/JM-Brun/J-DriftX/issues/206) et [#207 (priorisation et stratégie)](https://github.com/JM-Brun/J-DriftX/issues/207). Ce document conserve les critères d'audit de référence : aucun benchmark avant conclusion sur les fichiers, les licences et l'indépendance des essais.

## 1. Règles communes

Pour chaque corpus, vérifier neuf points ([catalogue des données](12-catalogue-donnees-transport-dispersion.md) et [cadrage G0-A](38-cadrage-g0a-besoin-applicatif.md)) :

1. **Accès et licence** — URL stable, droits de réutilisation, citation attendue.
2. **Terme source** — position, hauteur, débit d'émission, durée du lâcher documentés.
3. **Coordonnées et temps** — géoréférence et horodatage des mesures, fusable/UTC explicite.
4. **Météorologie** — vent, stabilité, champ météo reconstruisible et cohérent avec les mesures.
5. **Observable et unités** — concentration aérienne (observable primaire ratifié), unités non ambiguës.
6. **Limites de détection** — seuils, censures, incertitudes de mesure.
7. **Données manquantes** — complétude, trous, périodes invalidées.
8. **Essais indépendants** — nombre réel d'expériences indépendantes (pas le nombre de capteurs) ; structure de regroupement identifiable pour éviter les fuites.
9. **Reproductibilité des entrées** — un tiers peut-il reconstruire les entrées du modèle à partir des seules métadonnées publiques ?

## 2. Verdicts et règle de décision

| Verdict | Signification | Conséquence |
|---|---|---|
| **V** | Validation directe potentielle : les neuf points passent, essais indépendants isolables | Candidat pour le test discriminant G0 (§8 de la fiche) |
| **A** | Analogie méthodologique : physique partiellement transposable, entrées non reconstruites | Utilisable en illustration, jamais en preuve |
| **R** | Référence bibliographique uniquement | Classer, ne pas utiliser |

**Règle :** si le terme source ou la météo ne sont pas reconstruisibles, ou si aucun essai indépendant n'est isolable, le verdict est **R**, sans exception.

## 3. DIFLU — lâchers d'hélium contrôlés en champ proche

| Point | Vérification | Résultat |
|---|---|---|
| 1–9 | À instruire sur les fichiers bruts | — |

À trancher : adéquation au régime physique (scalaire passif, champ proche) ; nombre d'essais indépendants ; disponibilité de la météo co-localisée. Candidat prioritaire de la piste champ proche.

## 4. DATEM/ETEX — traceur à longue distance

| Point | Vérification | Résultat |
|---|---|---|
| 1–9 | À instruire sur les fichiers bruts | — |

À trancher : adéquation au far-field (distances, durées) ; reconstitution des champs météo historiques ; nombre de lâchers indépendants réellement exploitables. Candidat prioritaire de la piste far-field.

## 5. Données de surveillance régionales (Nantes / Pays de la Loire)

Pré-tri effectué le 22 octobre 2026 pour répondre à la question « existe-t-il des données ouvertes nantaises utiles ? ». Ces jeux sont des **données de surveillance**, pas des corpus de validation : aucun lâcher contrôlé, aucun terme source reconstruisible. Ils ne peuvent pas servir au test discriminant G0, mais peuvent alimenter des usages aval (G4) : cas d'étude applicatif, identification de source, caractérisation du fond urbain.

| Jeu | Nature | Usage possible pour J-DriftX |
|---|---|---|
| [Indice ATMO Nantes Métropole](https://data.nantesmetropole.fr/explore/dataset/323266205_indice-atmo-nantes-metropole/custom/) | Indice agrégé de communication (SO2, NO2, O3, PM10, PM2.5) | Aucun pour la validation ; contexte applicatif au mieux |
| [Indice ATMO Pays de la Loire par commune](https://www.data.gouv.fr/datasets/qualite-de-lair-indice-atmo-pays-de-la-loire-par-communes) | Indice journalier par agglomération | Idem |
| [Épisodes de pollution en Loire-Atlantique](https://data.nantesmetropole.fr/explore/dataset/323266205_episodes-pollution-air-loire-atlantique/) | Prévisions et constats d'épisodes réglementaires | Ciblage de périodes d'étude ; pas de validation |
| [PM2.5 en Pays de la Loire](https://www.data.gouv.fr/datasets/qualite-de-lair-niveau-de-particules-fines-de-diametre-inferieur-a-2-5-um-pm2-5-en-pays-de-la-loire) et [O3](https://www.data.gouv.fr/datasets/qualite-de-lair-niveau-de-ozone-o3-en-pays-de-la-loire) — Air Pays de la Loire | Moyennes horaires/journalières par station du réseau permanent | Séries temporelles réelles ; identification de source ou cas near-road **uniquement avec un inventaire d'émissions reconstructible** (trafic) |
| [Données temps réel nationales (Geod'air)](https://www.data.gouv.fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1) et [API Geod'air](https://www.geodair.fr/donnees/api) | Concentrations horaires réglementées, toutes AASQA | Idem ; stations urbaines nantaises incluses |

**Conclusion régionale :** aucune donnée nantaise ouverte ne fournit de lâcher contrôlé ; la classification « surveillance » du [catalogue](12-catalogue-donnees-transport-dispersion.md) s'applique. Un cas applicatif near-road sur Nantes (pairage stations Air Pays de la Loire + inventaire d'émissions routières) reste possible en aval (G3–G4), mais ne remplace pas l'audit DIFLU / DATEM-ETEX.

## 6. Livrables et décision

1. Un tableau rempli par corpus (verdict V/A/R + justification point par point), commité dans docs/.
2. Mise à jour du critère (e) dans l'issue de cadrage [#43](https://github.com/JM-Brun/J-DriftX/issues/43) et renvoi vers le [cadrage G0-A](38-cadrage-g0a-besoin-applicatif.md).
3. Décision : au moins un verdict **V** → sortie G0 instruisable ; tous **R** → activation du critère d'arrêt n°1 (fiche G0, §7) et repli sur le [fallback](09-fallback-modele-jouet.md).
