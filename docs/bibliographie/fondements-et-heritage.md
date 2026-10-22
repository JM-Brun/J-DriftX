# Sources fondatrices et héritage Drift-X

## Synthèse du lien avec le projet

Cette famille constitue le noyau historique directement lié à J-DriftX. Elle documente la modélisation à complexité réduite, les solutions de similitude généralisées, l'assimilation de données partielles et la pseudo-distance non symétrique fondée sur les temps de transport. Elle permet de préserver l'antériorité et de formuler fidèlement les hypothèses historiques avant toute modernisation.

## Références

### Thèse de J.-M. Brun — titre et année à confirmer

- **Lien :** source scientifique fondatrice, directement liée.
- **Référence :** *Comptes Rendus Mécanique*, 334(10), 634–638. DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007). [PDF éditeur/archives ouvertes](https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf).
- **Idées pertinentes :** similitude généralisée, modèle géométrique de transport d'un scalaire passif, pseudo-distance non symétrique fondée sur le temps de migration, assimilation d'observations partielles, calcul ponctuel sans résolution complète d'EDP.
- **Conséquence pour J-DriftX :** formaliser les définitions et hypothèses originales, reproduire au moins un cas historique et transformer les propriétés annoncées en tests analytiques et numériques.
- **Limites à conserver :** le papier est court ; les hypothèses sur l'écoulement et la structure du panache sont spécifiques. La pseudo-distance ne satisfait pas nécessairement les axiomes d'une distance métrique.
- **Statut de lecture indiqué dans le dépôt :** texte intégral relu.

### Brun — *Modélisation à complexité réduite de la dérive* (thèse ; année à confirmer)

- **Lien :** source fondatrice attendue, directement liée mais non consultée intégralement dans le corpus actuel.
- **Référence :** thèse de doctorat, Université Montpellier II. L'article primaire de Mohammadi & Brun (2006) la cite comme 2007 ; certaines bibliographies secondaires indiquent 2006. Elle n'a pas été localisée dans les recherches consignées, ce qui ne prouve pas l'absence de dépôt ou de numérisation.
- **Idées pertinentes :** contexte plus large du modèle multi-échelle et des applications à la dérive.
- **Conséquence :** retrouver, numériser et déposer une version partageable si les droits le permettent ; ne pas inférer son contenu détaillé à partir des seuls articles citants.
- **Statut :** métadonnées et contenu partiel connus par recoupement ; texte intégral à relire.

### Mohammadi, Brun & Pironneau (2006) — *Reduced order modelling of dispersion*

- **Lien :** source historique annoncée dans la bibliographie, directement pertinente.
- **Référence :** entrée bibliographique citée sous le titre *Reduced order modelling of dispersion* et associée à *Numerical Analysis and Scientific Computing with PDE and their Challenging Applications* ; le recueil et le statut éditorial n'ont pas été confirmés par une notice primaire.
- **Idées pertinentes :** modélisation réduite de dispersion ; détails à confirmer à partir du chapitre lui-même.
- **Conséquence :** retrouver le chapitre pour vérifier les recouvrements, les différences de formulation et la chronologie scientifique.
- **Statut :** citation secondaire attestée, mais source primaire et métadonnées du recueil non confirmées ; ne pas lui attribuer de résultats ni la présenter comme chapitre Springer établi.

### Brun & Mohammadi (2008) — *Reduced-Order Modelling of Dispersion*

- **Lien :** développement historique direct de la méthode.
- **Référence :** chapitre 14, *Computational Science and Engineering / Partial Differential Equations: Modelling and Numerical Simulation*, Springer. [DOI 10.1007/978-1-4020-8758-5_14](https://doi.org/10.1007/978-1-4020-8758-5_14).
- **Idées pertinentes :** modèle réduit, hiérarchie multi-échelle et applications de dispersion.
- **Conséquence :** distinguer les résultats établis dans le chapitre des hypothèses qui restent à revalider avec le code et les données actuels.
- **Statut :** accès partiel/extrait selon les notes du dépôt ; chapitre complet à vérifier.

### Bozon, Mohammadi & Sinfort (2008) — *Similitude and non symmetric geometry for dispersion modelling*

- **Lien :** publication historique directement liée, mais référence et texte à retrouver.
- **Référence :** *e-sta*, vol. 5, numéro spécial STIC & Environnement'07.
- **Idées pertinentes :** similitude et géométrie non symétrique appliquées à la dispersion.
- **Conséquence :** retrouver l'archive et comparer les formulations avec les papiers de 2006 et 2009 pour éviter de perdre une contribution intermédiaire.
- **Statut :** référence connue par citations ; texte intégral non localisé.

### Bozon, Sinfort & Mohammadi (2009) — *A GIS-based atmospheric dispersion model*

- **Lien :** source directe sur l'implémentation historique Drift-X et son couplage SIG.
- **Référence :** manuscrit auteur disponible sur [HAL, hal-00468863](https://hal.science/hal-00468863) ; une version journal est publiée en 2010 dans JESA.
- **Idées pertinentes :** architecture logicielle, intégration GIS/QGIS, modèle de dispersion et construction multi-niveaux.
- **Conséquence :** réutiliser les choix historiques comme référence de conception, mais séparer noyau scientifique, interfaces et données géographiques.
- **Statut :** manuscrit auteur indiqué comme relu intégralement dans le dépôt.

### Bozon & Mohammadi (2009) — *GIS-based atmospheric dispersion modelling*

- **Lien :** publication directe sur l'application SIG de Drift-X.
- **Référence :** *Applied Geomatics*, 1, 59–74. [DOI 10.1007/s12518-009-0006-0](https://doi.org/10.1007/s12518-009-0006-0).
- **Idées pertinentes :** représentation SIG et application du modèle à la dispersion atmosphérique.
- **Conséquence :** éclairer l'héritage applicatif ; ne pas considérer le SIG seul comme un différenciateur scientifique actuel.
- **Statut :** résumé accessible, texte intégral signalé comme sous abonnement.

### Bozon, Sinfort & Mohammadi (2010) — *A GIS-based atmospheric dispersion model*

- **Lien :** version journal liée au manuscrit historique de 2009.
- **Référence :** *Journal Européen des Systèmes Automatisés*, 44(4–5), 445–461. [DOI 10.3166/jesa.44.445-461](https://doi.org/10.3166/jesa.44.445-461).
- **Idées pertinentes :** version étendue/éditoriale du travail sur le modèle et le SIG.
- **Conséquence :** comparer précisément le manuscrit HAL et la version publiée avant de traiter ces documents comme deux contributions indépendantes.
- **Statut :** DOI recensé ; texte intégral à vérifier.

## Questions de travail

- Quelle formulation complète de la métrique est donnée dans la thèse et les chapitres ?
- Quelles hypothèses sont nécessaires pour l'unicité des caractéristiques, la conservation et l'identification de source ?
- Quelles parties du code historique sont reproductibles avec les données actuelles ?
- Les papiers 2009 et 2010 se recouvrent-ils largement, et comment les citer sans double-compter la même contribution ?
