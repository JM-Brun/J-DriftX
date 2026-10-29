# Fiche — Mohammadi & Brun 2006, C. R. Mécanique

## Fichier

- PDF actuellement présent : <code>../2006-mohammadi-brun-crmeca.pdf</code> (le renommage est déjà effectif ; l'ancien nom <code>CRMECA_2006__334_10_634_0.pdf</code> est historique).
- Extraction texte : <code>../extracts/2006-mohammadi-brun-crmeca.txt</code> (extraction automatique de 5 pages, avec formules dégradées ; ce fichier ne constitue pas à lui seul une preuve de lecture intégrale vérifiée).

## Référence

Mohammadi, B. & Brun, J.-M. (2006). « Similitude généralisée et modélisation géométrique à complexité réduite ». *C. R. Mécanique* 334(10), 634–638. DOI 10.1016/j.crme.2006.06.007. [PDF en accès libre](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) (archive ouverte de l'Académie des sciences).

## Revue — synthèse historique, statut de lecture à nuancer

**Statut de preuve.** Le PDF éditeur et une extraction automatique des cinq pages sont présents. Conformément à la correction de la [PR #143](https://github.com/JM-Brun/J-DriftX/pull/143), la documentation publique qualifie la lecture de partielle : la présence d'un texte extrait ne garantit pas que les formules, figures et conventions ont été vérifiées visuellement dans le PDF. Les détails ci-dessous doivent être lus comme une synthèse à contrôler sur la source originale, non comme une transcription certifiée.

- **Pseudo-distance** (éq. 3–5) : d(B,A) = ∞ si A est amont ; d(A,B) = temps de migration de A à B⊥ le long de la caractéristique ; aucun des axiomes d'une distance (identité, symétrie, triangle) n'est vérifié.
- **Vent complété** par écoulement potentiel u = ∇φ (éq. 4) ; alternative : grille de temps de migration + interpolation (temps infini si amont).
- **Conservation** au niveau du rang de culture ; hypothèse applicative : vent < 20 km/h.
- **Adjoint** par différentiation automatique inverse (Tapenade, INRIA) : coût du gradient indépendant du nombre de paramètres de contrôle.
- **Benchmark** : facteur ≈ 10³–10⁴ par point vs éléments finis stabilisés (~3000 points) ; croissance au moins quadratique en 2D, cubique en 3D.
- **Dimensions réalistes** : buse 10 cm, rangs 1,5 m, parcelle 1 ha dans un bassin de 400 km², dose 10 kg/km².
- Bibliographie interne : soumission IJNMF 2006 jamais retrouvée ; thèse Brun citée « 2007 » (discordance vs « 2006 » ailleurs).

## Valeur pour J-DriftX

Définition de référence de la métrique (contrat du module <code>metrique</code>, test non-symétrie) ; cible de performance 10³–10⁴ avec sa loi de croissance ; patron du benchmark M1 (validation par éléments finis) ; catalogue d'hypothèses (vent < 20 km/h, conservation au rang).

## Pour aller plus loin

Fiche source détaillée : [Mohammadi & Brun (2006), C. R. Mécanique](../../docs/bibliographie/sources/mohammadi-brun-2006-cr-mecanique.md). L'index général est [docs/04](../../docs/04-revues-papiers-sources.md).
