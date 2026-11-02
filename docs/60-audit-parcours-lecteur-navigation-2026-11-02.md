# Audit du parcours lecteur et proposition de navigation — 2026-11-02

## Décision éditoriale

Le site contient déjà les contenus nécessaires à un parcours approfondi. Le défaut principal est la dispersion de ces contenus dans une barre latérale à plusieurs groupes imbriqués, avec des catégories qui mélangent parfois nature du contenu (théorie, annexes), fonction (découvrir, vérifier) et statut scientifique (hypothèses, validation).

La refonte regroupe les pages en cinq entrées de premier niveau, sans déplacer ni renommer les fichiers :

1. **Découvrir** — comprendre le problème, l'origine, l'objectif et la chaîne d'objets.
2. **Théorie & modélisation** — suivre la construction mathématique et les modèles de référence.
3. **Preuves & validation** — examiner ce qui est formulé, dérivé, testé, comparé ou validé.
4. **Limites & état de l'art** — situer le domaine de validité et les alternatives.
5. **Ressources** — retrouver les données, le glossaire, les sources et les documents complémentaires.

Le laboratoire interactif reste visible depuis « Découvrir » afin d'être immédiatement accessible ; il ne devient pas une promesse de validation. Le catalogue de données reste dans « Ressources » et est relié depuis les pages de validation.

## Trois axes à ne pas confondre

- **Profondeur de lecture** : découverte, compréhension, construction, vérification.
- **Chaîne de modélisation** : niveaux physiques et mathématiques N0–N6.
- **Statut épistémique** : défini/formulé, supposé, dérivé/démontré, testé, comparé, validé indépendamment.

Ces axes répondent à des questions différentes. La navigation ne doit pas transformer les niveaux N0–N6 en niveaux de difficulté, ni les statuts de preuve en catégories de menu.

## Cartographie des pages Quarto

| Entrée | Pages | Rôle principal |
|---|---|---|
| Découvrir | `index.qmd` | Problème, question de recherche, statut et portes d'entrée |
| Découvrir | `projet/heritage.qmd`, `projet/objectifs.qmd`, `projet/utilite-scientifique.qmd` | Origine, objectifs et justification des cas d'usage |
| Découvrir | `projet/carte-articulation.qmd`, `projet/niveaux-modelisation.qmd` | Panorama et chaîne des objets |
| Découvrir | `projet/laboratoire-interactif.qmd`, `projet/experiences-interactives.qmd` | Exploration synthétique et expériences interactives |
| Théorie & modélisation | `theorie/modele-direct.qmd`, `theorie/similitude.qmd`, `theorie/reduction-a-priori.qmd` | Modèle direct, solutions candidates et réduction |
| Théorie & modélisation | `theorie/metrique-travel-time.qmd`, `theorie/metriques-non-riemanniennes.qmd`, `theorie/navigation-fronts-controllabilite.qmd` | Temps de transport, géométrie et fronts |
| Théorie & modélisation | `theorie/contraintes-physiques.qmd`, `theorie/assimilation-identification.qmd`, `theorie/edp-et-maillage.qmd`, `theorie/comparaison-complexites.qmd`, `theorie/burgers-et-jdriftx.qmd` | Contraintes, calibration, modèles de référence et coût |
| Preuves & validation | `projet/registre-preuves.qmd`, `projet/qualite.qmd`, `projet/validation-scientifique.qmd` | Registre, tests logiciels et validation scientifique |
| Preuves & validation | `hypotheses/catalogue.qmd` | Hypothèses explicites et traçables |
| Limites & état de l'art | `hypotheses/limites.qmd` | Domaines de validité, contre-exemples et limites |
| Limites & état de l'art | `etat-art/panorama.qmd`, `etat-art/positionnement.qmd`, `etat-art/revue-mathematique.qmd` | Alternatives, positionnement et revue critique |
| Ressources | `projet/carte-connaissances.qmd`, `projet/catalogue-donnees.qmd` | Graphe de connaissances et données |
| Ressources | `projet/lectures.qmd`, `projet/audit.qmd`, `projet/modele-jouet.qmd` | Sources, audit historique et exemple jouet |
| Ressources | `glossaire.qmd`, `references.qmd` | Terminologie, notations et bibliographie |

Les 35 fichiers Quarto du site ont été inventoriés dans l'arbre Git ; les 34 pages de contenu (hors extension technique) sont toutes conservées dans cette cartographie. Aucun déplacement, renommage ou changement d'URL n'est requis.

## Parcours recommandés

### Découverte (non spécialiste)
Accueil → carte d'articulation → héritage / objectifs → expérience 2D → limites majeures.

### Compréhension et pratique (étudiant, ingénieur)
Accueil → niveaux de modélisation → modèle direct → similitude → réduction a priori → métrique travel-time → laboratoire et qualité/tests.

### Vérification (chercheur, relecteur)
Accueil → hypothèses → dérivations et conditions → registre des preuves → tests/reproductibilité → comparaison des complexités → validation scientifique → limites et état de l'art.

Ces parcours sont des suggestions transversales, pas des séquences imposées par l'ordre du menu. Les renvois locaux des pages théoriques restent la navigation de détail.

## Constats et décisions

- Le menu actuel possède déjà une navigation Quarto native (`page-navigation: true`) ; il n'est pas nécessaire d'ajouter un mécanisme JavaScript de breadcrumbs.
- Les liens internes entre pages centrales sont denses : la carte d'articulation renvoie vers le modèle direct, la similitude, la réduction, la métrique, le registre et les expériences ; les pages théoriques se renvoient mutuellement et renvoient aux hypothèses et au glossaire.
- Les pages de laboratoire distinguent déjà expérience navigateur et applications locales. Garder cette distinction visible pour ne pas laisser penser que tous les outils sont embarqués.
- La barre latérale actuelle imbrique « vérification » dans « découvrir », puis sépare théorie, hypothèses, état de l'art et annexes. Les cinq piliers rendent ces fonctions plus prévisibles sans modifier la structure des fichiers.
- Le glossaire et les références doivent rester directement accessibles depuis le menu, même s'ils sont rangés sous « Ressources ».

## Périmètre de cette tranche

- Modification limitée à l'organisation du menu dans `site/_quarto.yml`.
- Aucun contenu scientifique, équation, statut, URL de page ou nom de fichier n'est modifié.
- `page-navigation: true`, la recherche, le sommaire de page et les liens GitHub sont conservés.
- Les parcours séquentiels spécifiques et les tooltips sont différés : ils nécessitent une revue page par page et ne doivent pas être simulés par une navigation automatique mal adaptée aux dépendances scientifiques.

## Vérifications requises

- Construction complète Quarto.
- Vérification des liens internes, ancres et ressources.
- Vérification que chaque page Quarto est présente une fois dans le menu ou explicitement accessible par un lien d'entrée.
- Relecture du menu sur grand écran et mobile.
- Vérification du site publié après fusion.

## Sources de vérité

- `site/_quarto.yml` — menu effectif.
- `site/index.qmd` — parcours d'accueil.
- `site/projet/carte-articulation.qmd` — articulation scientifique et parcours.
- `site/projet/niveaux-modelisation.qmd` — chaîne N0–N6.
- Issues #456 et #457 — gouvernance et critères d'acceptation.
