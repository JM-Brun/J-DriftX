# Fiche — Brun & Mohammadi 2008, chapitre Springer CSM 16

## Fichier

- Actuel : <code>PDF.js viewer.pdf</code> → renommage recommandé : <code>2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf</code>
- Attention : **extrait de 2 pages seulement** (p. 245–246), généré depuis un visualiseur PDF ; le chapitre complet reste à ajouter sous <code>2008-brun-mohammadi-springer-chap14.pdf</code>
- Extraction texte : pages océrisées (résumé, introduction, début de la section 2) ; revue intégrée dans cette fiche et dans la fiche 4 de <code>docs/04-revues-papiers-sources.md</code>

## Référence

Brun, J.-M. & Mohammadi, B. (2008). « Reduced-Order Modelling of Dispersion ». In Glowinski, R. & Neittaanmäki, P. (eds), *Partial Differential Equations: Modelling and Numerical Simulation*, Computational Methods in Applied Sciences vol. 16, Springer, chap. 14, p. 245 et s. DOI 10.1007/978-1-4020-8758-5_14. Relais public : [page ResearchGate](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion).

## Revue — pages 245–246 (extrait disponible)

- **Résumé** : transport de scalaire passif à faible complexité ; analyse multi-niveaux avec réduction de dimension de l'espace des solutions à chaque niveau ; solutions de similitude dans une métrique non symétrique pour le transport longue distance ; identification des paramètres par assimilation de données ; sans EDP donc sans maillage ; évaluation ponctuelle sans calculer partout ; analyse de sensibilité pour l'analyse de risque et l'identification de sources d'une pollution observée.
- **Objectif chiffré implicite** : un coût de calcul si bas que « assimilation-simulation » et analyse de risque statistique par simulations Monte Carlo deviennent réalistes.
- **Multi-niveaux** : « a given level provides the inlet condition for the level above » — chaque niveau fournit la condition d'entrée du niveau supérieur.
- **Champ proche** : construit à partir d'observations expérimentales ; la quantité d'espèce quittant la sous-couche atmosphérique est ensuite estimée et devient candidate au transport longue distance (similitude couches de mélange et panaches [Sim97], connues en métrique cartésienne).
- **Verrou central** : généralisation de ces solutions dans une métrique non symétrique basée sur les temps de transport, pour les vents non uniformes.
- **Contraintes physiques** : divergence nulle du vent généré, conservation, positivité, linéarité de l'équation de transport.
- **Section 2 (ROM)** : approche classique = projection sur un sous-espace de snapshots (n ≪ N, [VP05]) ; ici on vise à **supprimer le calcul des snapshots** : le modèle direct est remplacé par un modèle approché plus facile à évaluer, suffisant car le modèle réduit n'a besoin que d'un **domaine de validation local** ; lien explicite avec la **sensibilité incomplète** [MP01] (linéarisation sur une équation d'état approchée, pas sur le modèle direct).
- **Bibliographie visible** : thèse Brun 2006 ; Borouchaki, George & Mohammadi 1997 (métriques de maillage) ; Mohammadi & Pironneau (k-epsilon, Applied Shape Optimization) ; Ivorra 2006 (optimisation globale semi-déterministe) — la matrice intellectuelle « métrique + optimisation de forme + sensibilité ».

## Valeur pour J-DriftX

Cahier des charges scientifique du noyau : multi-niveaux avec entrée/sortie de sous-couche, métrique τ non symétrique, quatre contraintes physiques (deux déjà testées dans le socle : conservation, non-symétrie), sensibilité/identification de source. Les pages restantes (exemples numériques, analyse de sensibilité) sont la prochaine extraction à faire sur le chapitre complet.

## Pour aller plus loin

Fiche détaillée : <code>docs/04-revues-papiers-sources.md</code>, section 4.
