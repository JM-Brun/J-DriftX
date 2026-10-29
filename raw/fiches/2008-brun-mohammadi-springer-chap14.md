# Fiche — Brun & Mohammadi 2008, chapitre Springer CSM 16

## Fichier

- PDF intégral du recueil actuellement présent : <code>../Partial Differential Equations - Modelling and Numerical Simulation - R. Glowinski, P. Neittaanmaki (Springer, 2008) WW.pdf</code> ; il est conservé conformément à la décision explicite du mainteneur (restauration exacte via PR #264). Ne pas ouvrir de PR de suppression sans demande explicite.
- Extrait distinct : <code>../2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf</code>, **2 pages seulement** (p. 245–246), généré depuis un visualiseur PDF. Il ne remplace pas le recueil complet.
- Extraction : pas de transcription OCR intégrale vérifiée du chapitre. Des notes analytiques existent dans <code>../extracts/2008-brun-mohammadi-springer-chap14-notes.txt</code> et couvrent les pages 245–256, mais elles ne sont pas verbatim. Les équations et figures restent à contrôler sur le fac-similé du PDF conservé ; droits de redistribution non résolus.

## Référence

Brun, J.-M. & Mohammadi, B. (2008). « Reduced-Order Modelling of Dispersion ». In Glowinski, R. & Neittaanmäki, P. (eds), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, chap. 14, p. 245 et s. DOI 10.1007/978-1-4020-8758-5_14. Relais public : [page ResearchGate](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion).

## Revue — pages 245–246 (extrait disponible)

- **Résumé** : transport de scalaire passif à faible complexité ; analyse multi-niveaux avec réduction de dimension de l'espace des solutions à chaque niveau ; solutions de similitude dans une métrique non symétrique pour le transport longue distance ; identification des paramètres par assimilation de données ; sans EDP donc sans maillage ; évaluation ponctuelle sans calculer partout ; analyse de sensibilité pour l'analyse de risque et l'identification des sources d'une pollution observée.
- **Objectif chiffré implicite** : un coût de calcul si bas que « assimilation-simulation » et analyse de risque statistique par simulations Monte Carlo deviennent réalistes.
- **Multi-niveaux** : « a given level provides the inlet condition for the level above » — chaque niveau fournit la condition d'entrée du niveau supérieur.
- **Champ proche** : construit à partir d'observations expérimentales ; la quantité d'espèce quittant la sous-couche atmosphérique est ensuite estimée et devient candidate au transport longue distance (similitude couches de mélange et panaches [Sim97], connues en métrique cartésienne).
- **Verrou central** : généralisation de ces solutions dans une métrique non symétrique basée sur les temps de transport, pour les vents non uniformes.
- **Contraintes physiques** : divergence nulle du vent généré, conservation, positivité, linéarité de l'équation de transport.
- **Section 2 (ROM)** : approche classique = projection sur un sous-espace de snapshots (n ≪ N, [VP05]) ; ici on vise à **supprimer le calcul des snapshots** : le modèle direct est remplacé par un modèle approché plus facile à évaluer, suffisant car le modèle réduit n'a besoin que d'un **domaine de validation local** ; lien explicite avec la **sensibilité incomplète** [MP01] (linéarisation sur une équation d'état approchée, pas sur le modèle direct).
- **Bibliographie visible** : thèse Brun 2006 ; Borouchaki, George & Mohammadi 1997 (métriques de maillage) ; Mohammadi & Pironneau (k-epsilon, Applied Shape Optimization) ; Ivorra 2006 (optimisation globale semi-déterministe) — la matrice intellectuelle « métrique + optimisation de forme + sensibilité ».

## Valeur pour J-DriftX

Cahier des charges scientifique du noyau : multi-niveaux avec entrée/sortie de sous-couche, métrique τ non symétrique, quatre contraintes physiques (deux déjà testées dans le socle : conservation, non-symétrie), sensibilité/identification de source. Les pages restantes (exemples numériques, analyse de sensibilité) peuvent être examinées à partir du recueil complet conservé dans `raw/`, sous réserve des droits applicables ; les équations et figures ne sont pas toutes vérifiées visuellement.

## Pour aller plus loin

Fiche source détaillée : [Brun & Mohammadi (2008), chapitre Springer](../../docs/bibliographie/sources/brun-mohammadi-2008-chapitre.md). L'index général est [docs/04](../../docs/04-revues-papiers-sources.md).


## Complément d'analyse — sens de la hiérarchie multi-niveaux

La phrase du chapitre « a given level provides the inlet condition for the level above » décrit un **couplage de régimes physiques** : le modèle de champ proche, qui représente l'émission et la distribution initiale près du dispositif, fournit une quantité d'entrée au modèle de transport à longue distance. Chaque niveau réduit l'espace des solutions en s'appuyant sur une famille paramétrée et sur des connaissances physiques a priori. L'assimilation de données sert à identifier des paramètres de cette représentation.

Cette hiérarchie ne doit pas être confondue avec les **niveaux spatiaux emboîtés** `Ω = ω₀, ωᵢ` du manuscrit Drift-X 2009. Dans ce second cas, les niveaux correspondent à des emprises spatiales et à des résolutions différentes, utilisées pour raffiner le champ de vent et corriger les effets du relief. Les deux mécanismes peuvent se combiner conceptuellement, mais ils répondent à des questions distinctes : *quel régime physique alimente le suivant ?* versus *à quelle résolution spatiale le champ est-il représenté ?*

### Hypothèses et conséquences à garder explicites

- Le champ proche est paramétré à partir de caractéristiques du dispositif, de la végétation et d'observations expérimentales ; ce n'est pas un champ CFD détaillé garanti.
- La séparation d'échelles suppose notamment que la vitesse d'injection domine le déplacement du dispositif et que l'écoulement local ne modifie pas la circulation atmosphérique globale. La note analytique du chapitre signale que les auteurs eux-mêmes qualifient ces hypothèses de fortes.
- La quantité de scalaire quittant la couche proche du sol devient une entrée du modèle lointain : cette interface impose de préciser unités, bilan de masse, convention d'intégration et domaine de validité.
- Le modèle lointain généralise les profils de similitude à une géométrie dirigée par le temps de migration le long d'une caractéristique. Cela suppose une caractéristique pertinente et une règle de sélection en cas de non-unicité ; les champs avec recirculation ou topologie complexe peuvent invalider ou compliquer cette construction.
- Les figures numériques du chapitre sont des démonstrations sur des configurations sélectionnées, pas un benchmark exhaustif de tous les régimes météorologiques, terrains, sources et niveaux de bruit.

La note conservée dans [l'extraction analytique du chapitre](../extracts/2008-brun-mohammadi-springer-chap14-notes.txt) complète l'extrait des pages 245–246 ; elle ne remplace pas la vérification des équations et figures sur le PDF éditeur.

Lien avec la reprise : [carte N0–N6](../../site/projet/niveaux-modelisation.qmd), [revue croisée des architectures multi-niveaux](../../docs/04-revues-papiers-sources.md), [fiche source de la plateforme Drift-X 2009](2009-bozon-sinfort-mohammadi-driftx-hal.md).
