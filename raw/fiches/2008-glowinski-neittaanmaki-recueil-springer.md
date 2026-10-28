# Fiche de lecture — Glowinski & Neittaanmäki (dir.), 2008

## Identification du fichier

- **État vérifié sur `main` après fusion de la PR #67 (28 octobre 2026)** : le PDF intégral a été retiré du dépôt. Cette fiche est conservée comme référence bibliographique et trace de provenance de la copie consultée historiquement ; le binaire n'est plus distribué dans ce dépôt.
- **Décision de dépôt** : la PR [#67](https://github.com/JM-Brun/J-DriftX/pull/67) a été fusionnée. Le PDF éditeur complet n'est pas conservé faute d'autorisation de redistribution établie. La référence bibliographique et cette fiche de provenance sont conservées.
- **Nature** : recueil éditorial complet, et non tiré-à-part du seul chapitre utile au projet.
- **Contrôle documentaire** : une copie consultée antérieurement a servi à contrôler la page de titre, l'ISBN, la table des matières et le texte du chapitre 14. Cela étaye l'identification bibliographique et la lecture scientifique initiale, mais ne signifie pas que le PDF intégral est redistribuable.
- **Matériaux conservés** : le dépôt contient aussi `raw/2008-brun-mohammadi-springer-chap14-extrait-p245-246.pdf` (pages 245–246 seulement) et `raw/extracts/2008-brun-mohammadi-springer-chap14-notes.txt` (notes analytiques, pas OCR intégral). Ils ne remplacent pas une vérification des équations et figures sur le chapitre original.

## Référence bibliographique

Glowinski, R. & Neittaanmäki, P. (dir.) (2008). *Partial Differential Equations: Modelling and Numerical Simulation*. Computational Methods in Applied Sciences, vol. 16. Springer, Dordrecht. DOI : [10.1007/978-1-4020-8758-5](https://doi.org/10.1007/978-1-4020-8758-5). eISBN : 978-1-4020-8758-5 ; ISBN imprimé : 978-1-4020-8757-8. Le volume compte XVI + 292 pages.

**Chapitre pertinent pour J-DriftX**

Brun, J.-M. & Mohammadi, B. (2008). “Reduced-Order Modelling of Dispersion”. Dans Glowinski & Neittaanmäki (dir.), *Partial Differential Equations: Modelling and Numerical Simulation*, p. 245–256. DOI : [10.1007/978-1-4020-8758-5_14](https://doi.org/10.1007/978-1-4020-8758-5_14). [Notice Springer du recueil](https://link.springer.com/book/10.1007/978-1-4020-8758-5) · [notice ResearchGate du chapitre](https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion).

## Résumé critique du chapitre 14

### Problème et objectif

Le chapitre vise la prédiction à faible coût de la dispersion atmosphérique d'un scalaire passif, notamment de produits phytosanitaires, dans un contexte environnemental où les observations sont rares, hétérogènes et incertaines. Plutôt que de résoudre systématiquement les équations aux dérivées partielles (EDP) sur tout le domaine, les auteurs construisent un modèle réduit à partir de connaissances physiques a priori, de formes paramétriques et de l'assimilation des données.

Le terme « reduced-order » doit ici être interprété précisément : il ne s'agit pas simplement de projeter des solutions préalablement calculées sur une base de snapshots. Les auteurs soulignent qu'ils cherchent à éviter le calcul de ces snapshots en construisant directement une approximation adaptée au phénomène et à un domaine de validité local.

### Architecture multi-niveaux

1. **Champ proche** : une forme paramétrique décrit l'écoulement et la concentration à proximité du dispositif d'injection. Ses fonctions et paramètres sont ajustés à partir d'observations expérimentales et de caractéristiques du dispositif et de la végétation.
2. **Passage vers le transport à longue distance** : la quantité de scalaire susceptible de quitter la sous-couche atmosphérique proche du sol fournit la donnée d'entrée du niveau supérieur.
3. **Champ lointain** : des profils de similitude inspirés des couches de mélange et des panaches sont généralisés à un champ de vent non uniforme au moyen d'une géométrie fondée sur les temps de migration.
4. **Assimilation et analyse inverse** : les données servent à construire le champ de vent et à identifier les paramètres du modèle. L'analyse de sensibilité est mobilisée pour étudier le risque et rechercher les sources possibles d'une pollution observée.

Chaque niveau fournit donc une condition d'entrée au suivant. Cette décomposition traduit une hypothèse de modélisation : il est possible d'isoler des régimes physiques distincts et de les coupler via des quantités résumées, plutôt que de résoudre un modèle détaillé unique partout.

### Hypothèses et contraintes physiques explicites

Le modèle de champ proche suppose notamment deux échelles de temps distinctes : la vitesse d'injection est considérée comme nettement supérieure à celle du déplacement du dispositif. L'écoulement local d'injection est alors traité comme instantané et supposé ne pas modifier la circulation atmosphérique globale ; il sert surtout à estimer la fraction du polluant pouvant être transportée à longue distance. Les auteurs qualifient eux-mêmes ces hypothèses de fortes.

Les champs paramétriques sont soumis à des contraintes destinées à préserver des propriétés du modèle direct :

- champ de vitesse sans divergence, \\(\\nabla\\cdot u=0\\) ;
- conservation de la quantité de scalaire transportée ;
- positivité de la concentration ;
- compatibilité avec l'équation d'advection du scalaire passif.

Ces conditions ne sont pas des détails accessoires : elles bornent l'espace des approximations admissibles et empêchent de réduire le problème au seul ajustement statistique des observations.

### Géométrie non symétrique fondée sur le temps de transport

Dans une distance euclidienne, la distance de A à B est identique à celle de B à A. Ce n'est généralement pas le cas pour le temps de transport dans un champ de vent : atteindre B depuis A peut être rapide dans le sens du vent et très lent, voire impossible dans le modèle idéalisé, dans le sens opposé.

Les auteurs définissent donc une distance orientée à partir du temps de migration le long d'une caractéristique du champ de vitesse. Le profil de panache est ensuite exprimé en fonction de cette distance de transport et d'une distance transverse euclidienne locale. La géométrie n'est pas ici un simple changement graphique : elle encode l'asymétrie induite par l'advection et permet d'étendre des profils de similitude construits initialement pour des écoulements plus simples.

**Limites de cette construction à garder visibles :**

- le calcul s'appuie sur des caractéristiques suffisamment bien définies ; le texte suppose notamment une caractéristique unique et évite les sources et points d'attraction du champ ;
- le calcul du temps de migration et de la distance transverse repose sur des approximations numériques et géométriques ;
- les auteurs indiquent que l'approche vise des champs atmosphériques lisses, cohérents avec le contexte d'application envisagé. Elle ne doit donc pas être présentée comme une méthode générale pour tout champ de vitesse, notamment en présence de séparatrices, de recirculations ou de topologies complexes.

### Résultats rapportés et portée de la validation

La section numérique présente des configurations mono-source et multi-sources, des champs de vent reconstruits à partir d'un petit nombre de mesures, l'effet du relief et un exemple d'identification de source. Une comparaison est montrée entre le profil généralisé et une simulation directe fondée sur un modèle EDP de transport-diffusion ; le modèle réduit est évalué sur les nœuds du maillage de référence pour rendre la comparaison possible.

Le chapitre établit ainsi une **preuve de faisabilité sur des cas illustratifs**, pas une validation universelle. Les éléments à ne pas surinterpréter :

- les exemples numériques ne suffisent pas à démontrer une précision garantie sur des terrains, météorologies ou régimes de dispersion arbitraires ;
- l'identification dépend de la qualité et de la couverture des observations, ainsi que de l'identifiabilité des paramètres ;
- l'analyse de sensibilité peut proposer des sources compatibles avec une observation, mais ne garantit pas à elle seule une localisation unique ;
- l'intérêt du faible coût de calcul pour des simulations Monte-Carlo et des cartes de risque est avancé comme perspective applicative ; il ne constitue pas, à lui seul, une validation statistique de ces cartes.

## Apport direct pour J-DriftX

| Élément du chapitre | Réutilisation possible dans J-DriftX | Précaution |
|---|---|---|
| Décomposition champ proche / champ lointain | Architecture multi-niveaux et interfaces entre sous-modèles | Documenter les hypothèses et les variables transmises entre niveaux |
| Profils de similitude paramétriques | Baseline physique peu coûteuse pour la dispersion | Délimiter le domaine de validité des profils |
| Distance orientée par le temps de migration | Représentation de l'asymétrie amont/aval dans un champ de vent | Ne pas confondre cette construction avec une métrique symétrique ou une distance euclidienne |
| Contraintes de divergence et de conservation | Tests de cohérence physique des champs et des prédictions | Les contraintes doivent être vérifiées numériquement, pas seulement citées |
| Assimilation des observations | Identification du champ de vent et des paramètres | Traçabilité des données, incertitudes et problème d'identifiabilité |
| Sensibilité et reconstruction de source | Analyse inverse, hiérarchisation des sources candidates, étude de risque | Une carte de sensibilité n'est pas automatiquement une probabilité de source |

Ce chapitre est une source primaire particulièrement importante pour le noyau historique de J-DriftX : il décrit explicitement le couplage multi-niveaux, la métrique de temps de transport non symétrique, les contraintes physiques et les usages en analyse inverse. Il complète les pages déjà disponibles du chapitre sans remplacer les articles et manuscrits connexes du corpus.

## Statut de revue et actions restantes

- [x] Identité du livre, éditeurs, année, collection, ISBN et pagination contrôlés.
- [x] Présence et pagination du chapitre 14 confirmées dans la table des matières : p. 245–256.
- [x] Première lecture du texte du chapitre 14 : objectif, architecture, hypothèses, contraintes, géométrie, exemples et limites consignés ci-dessus.
- [x] Documenter la provenance historique de la copie consultée ; le binaire complet n'est plus conservé dans le dépôt.
- [x] Ajouter une extraction analytique structurée dans `raw/extracts/2008-brun-mohammadi-springer-chap14-notes.txt`, avec provenance, pagination, limites et note de droits. Il ne s'agit pas d'une transcription OCR intégrale.
- [ ] Si une transcription OCR intégrale est nécessaire, la produire localement à partir du PDF autorisé, puis vérifier les équations, figures et légendes sur le document original ; ne pas confondre texte OCR non relu et extraction validée.
- [ ] Reporter les constats utiles dans la fiche dédiée du chapitre `raw/fiches/2008-brun-mohammadi-springer-chap14.md` et dans la synthèse documentaire `docs/04-revues-papiers-sources.md` si ces pages ne les intègrent pas déjà.

## Droits et conservation

La copie historiquement consultée était une version éditeur du recueil complet. La page de copyright encadre la reproduction ou la transmission. Le dépôt ne conserve plus ce binaire ; il conserve la référence, les DOI et une analyse explicitement limitée par la source consultée. Pour toute reprise de lecture, privilégier une source légalement accessible ou une version auteur autorisée.

## Sources de contrôle

- Springer Nature, notice et table des matières du recueil : https://link.springer.com/book/10.1007/978-1-4020-8758-5
- Copie consultée historiquement pour le contrôle bibliographique et la lecture du chapitre 14 : miroir tiers, URL non reproduite ici ; cette consultation historique n'établit pas un droit de redistribution.
- Notice du chapitre : https://www.researchgate.net/publication/226478979_Reduced-Order_Modelling_of_Dispersion
