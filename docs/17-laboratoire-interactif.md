# Laboratoire interactif J-DriftX — proposition de conception

> Statut : proposition d'architecture et de MVP pédagogique. Ce document ne décrit pas une application déjà déployée et ne constitue pas une validation du modèle physique.

## 1. Objectif

Permettre à un lecteur de modifier quelques paramètres, d'exécuter des calculs Python reproductibles et d'observer directement leurs effets sur des fonctions, champs, trajectoires et modèles simplifiés. L'outil doit aider à comprendre les hypothèses et à préparer des expériences scientifiques, sans confondre visualisation pédagogique et résultat validé.

Deux usages doivent être explicitement séparés :

1. **Explorer** : apprendre le comportement d'un objet mathématique ou physique dans un cas synthétique contrôlé.
2. **Évaluer** : confronter une formulation candidate à une référence analytique ou numérique, mesurer l'erreur et conserver un protocole reproductible.

Une jolie visualisation ne constitue ni une preuve mathématique ni une validation empirique.

## 2. Choix d'architecture

### Principe : un noyau Python, plusieurs interfaces possibles

Les calculs doivent rester dans des fonctions Python testables et indépendantes de l'interface. Les widgets ne doivent pas contenir la physique ou les formules elles-mêmes.

- **Cœur scientifique** : fonctions pures, paramètres typés, unités documentées, hypothèses et domaine de validité explicités.
- **Visualisation** : figures Matplotlib calculées à partir des sorties du cœur.
- **Interface initiale** : petite application Streamlit, exécutable localement, avec curseurs, choix de scénarios, légendes et explications.
- **Site Quarto** : pages explicatives qui intègrent des figures statiques vérifiées et renvoient vers l'application interactive. L'intégration embarquée sera étudiée seulement si l'hébergement et la maintenance sont fiables.
- **Tests** : cas analytiques, propriétés sous hypothèses explicites, tests des paramètres limites et tests de non-régression.

L'application est un outil de recherche/pédagogie distinct du package de calcul principal. Streamlit et Matplotlib ne doivent pas devenir des dépendances obligatoires du cœur `jdriftx`.

## 3. MVP proposé

### Module 1 — Champs de vecteurs

Scénarios initiaux : champ uniforme, cisaillement linéaire et champ radial synthétique. Contrôles : intensité, direction, gradient/cisaillement et taille de la grille. Vues : flèches, lignes de courant, norme, divergence et rotationnel en 2D.

Garde-fous : expliquer que les lignes de courant sont tangentes au champ instantané et ne sont pas automatiquement des trajectoires temporelles lorsque le champ dépend du temps. Les dérivées discrètes dépendent de la grille et du schéma numérique.

### Module 2 — Fonctions, reliefs et géométrie

Scénarios : plan, bosse gaussienne et vallée synthétique. Contrôles : hauteur, largeur et position. Vues : surface 3D, contours et gradient.

Garde-fous : ne pas déduire une modification du vent ou de la dispersion à partir du relief seul. Tout couplage relief–écoulement devra être défini séparément et justifié par un modèle physique.

### Module 3 — Transport et dispersion jouets

Commencer par des formulations à hypothèses visibles : advection uniforme, diffusion unidimensionnelle simple et solution gaussienne analytique lorsque ses hypothèses s'appliquent. Contrôles : vitesse, coefficient de diffusion, durée, largeur initiale et position de source. Vues : profils, cartes, bilans et comparaison à la référence.

Garde-fous : afficher unités, conditions initiales, conditions aux limites et hypothèses de dimension. Ne pas présenter une solution analytique simplifiée comme un modèle réglementaire ou une prévision de dispersion réelle.

### Module 4 — Expériences de validation

Pour chaque formulation implémentée :
- comparer à une solution analytique lorsque disponible ;
- tracer l'erreur absolue et relative avec une définition explicite des zones où l'erreur relative est pertinente ;
- vérifier les limites et les invariants seulement sous les hypothèses qui les garantissent ;
- proposer des cas de contre-exemple ;
- permettre d'exporter les paramètres, le scénario et les résultats tabulaires pour reproduction.

Le module J-DriftX ne doit exposer comme « modèle » que des fonctions réellement présentes et documentées dans `src/jdriftx/`. Les formulations historiques encore non implémentées doivent être étiquetées comme telles.

## 4. Ergonomie attendue

Chaque expérience doit contenir :

1. **Contrôles** : curseurs avec unités, bornes raisonnables et valeurs par défaut explicites.
2. **Visualisation** : titre, axes, unités, légende, échelle de couleur et indication de la grille.
3. **Explication** : équation affichée, définition des variables et interprétation qualitative.
4. **Hypothèses et limites** : ce qui est supposé, ce qui est calculé et ce que le résultat ne permet pas de conclure.
5. **Reproductibilité** : paramètres affichés/exportables et graine aléatoire lorsque nécessaire.
6. **Performance** : domaine de calcul et résolution bornés pour garder une interaction fluide.

Les paramètres doivent être regroupés en paramètres physiques, paramètres numériques et paramètres d'affichage. Modifier uniquement la résolution d'affichage ne doit pas être présenté comme une modification du modèle physique.

## 5. Déploiement : décision progressive

Commencer par une application Streamlit exécutable localement ; cela permet de valider l'expérience sans ajouter immédiatement une infrastructure de service au site statique GitHub Pages.

Une publication distante ne sera proposée qu'après :
- installation reproductible et tests automatisés ;
- revue des dépendances et des risques de sécurité ;
- limites explicites sur la taille des grilles et le coût des calculs ;
- décision sur l'hébergement, la maintenance et les versions ;
- vérification qu'aucune donnée sensible n'est demandée ou enregistrée.

Les pages Quarto restent accessibles sans l'application. L'absence du service interactif ne doit pas casser la documentation.

## 6. Dépendances et qualité

Les dépendances d'interface doivent être optionnelles, par exemple dans un groupe `app` séparé. Le noyau reste NumPy et Python compatible avec la configuration du projet. Matplotlib et Streamlit sont réservés à l'interface ; tests du cœur et tests de l'interface doivent être distingués.

Critères minimaux :
- tests numériques comparés à des valeurs analytiques connues ;
- tests des paramètres limites et de validation des entrées ;
- absence de calculs physiques dans les callbacks de présentation ;
- lint, typage et tests exécutables par commandes documentées ;
- rendu Quarto vérifié avant fusion ;
- statut scientifique visible sur chaque page et dans l'application.

## 7. Hors périmètre du premier MVP

- ingestion de données météorologiques ou topographiques réelles ;
- simulation CFD ou solveur d'EDP général ;
- assimilation, identification de source ou entraînement ML ;
- prétention à reproduire l'intégralité du Drift-X historique ;
- comparaison de performances sans protocole, baseline et données de référence ;
- promesse d'hébergement public permanent avant décision d'exploitation.

## 8. Plan de réalisation

1. Valider cette architecture et l'inventaire des objets mathématiques déjà implémentés.
2. Construire le module « champs de vecteurs » avec trois champs synthétiques et tests.
3. Ajouter les reliefs synthétiques, en gardant le relief découplé de la dynamique du vent.
4. Ajouter un cas d'advection-diffusion analytique et ses tests.
5. Créer les expériences de comparaison et d'export reproductible.
6. Relier les pages Quarto à l'application, puis décider séparément d'un hébergement public.

Chaque étape doit être livrée par une PR de taille limitée, avec vérifications réellement exécutées et résultats négatifs conservés. L'explorateur pédagogique peut avancer indépendamment du jalon G0 applicatif ; il ne débloque pas, à lui seul, les revendications de validité ou d'utilité de J-DriftX.
