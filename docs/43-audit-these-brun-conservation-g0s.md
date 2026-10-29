# Audit de la thèse de Brun — conservation du transport lointain (G0-S)

**État au 29 octobre 2026 :** le texte de la thèse et la page imprimée 129 (équations 7.12–7.13) ont été inspectés sur une copie miroir tierce ; la forme imprimée des deux alternatives de $c^+$ est donc vérifiée visuellement sur cette copie, pas seulement via OCR. Le chapitre Springer 2008 a également été inspecté dans une copie tierce du recueil et imprime la même alternative avec la même définition sans dimension de $u_l^+$. **L'identité binaire entre ces copies tierces, le PDF poussé dans la branche et le fichier servi par HAL n'est pas vérifiée.** Le diagnostic dimensionnel est néanmoins indépendant de l'identité binaire, car les deux textes consultés montrent la même formule.

## Sources et niveau de confiance

- Notice AGRIS/INRAE, titre *Modèles à complexité réduite de transport pour applications environnementales*, auteur J.-M. Brun, thèse, notice de 2007 : https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c
- Notice et fichier HAL liés par AGRIS : https://hal.inrae.fr/tel-02589999/document et https://hal.inrae.fr/tel-02589999/file/pub00023263.pdf
- Copie miroir consultée pour la lecture du texte : https://www.mcours.net/cours/pdf/yass2/yass2cllic260.pdf (PDF de 201 pages selon le lecteur web ; hébergeur tiers, non institutionnel).
- Le dépôt J-DriftX contient un PDF sous le chemin raw/Modèles à complexité réduite de transport pour applications environnementales - pub00023263.pdf. Son titre, sa pagination et son identité exacte avec les deux URL ci-dessus restent à contrôler sur le binaire lui-même.

La copie miroir présente le contenu de la thèse, mais l'extraction affichée commence aux remerciements, sans page de titre visible dans le texte récupéré. Le titre et l'année sont donc confirmés par la notice bibliographique, non par une inspection visuelle de la page de titre. Ne pas qualifier la copie miroir de « version HAL vérifiée ».

## Passages déterminants

### 1. Définition du temps de migration

Dans le chapitre 7, §7.1.3, pages imprimées 126–127, la distance orientée est définie de façon asymétrique. Si A est au vent de B, le texte définit le temps de migration par une intégrale le long de la caractéristique passant par A jusqu'à la projection B⊥, puis précise que la vitesse locale u est tangente à cette caractéristique. Le texte suppose la caractéristique unique, afin d'éviter les sources et points d'attraction du champ (équations (7.6)–(7.7), p. 127).

Ces pages décrivent un temps de migration construit par trajectoire et projection. Elles ne donnent pas à elles seules une carte globale régulière et bijective (τ, η₁, η₂) ↦ (x, y, z), ni son jacobien. Elles ne justifient donc pas de transposer automatiquement une conservation volumique vers chaque surface iso-τ.

### 2. Quantité d'entrée c⁺ et conservation revendiquée

Au chapitre 7, §7.3 « Long range transport », page imprimée 129, équation (7.12), deux constructions alternatives sont imprimées :

\[
 c^+(x,y)=\int_{z>H} c_{loc}(x,y,z)\,dz
 \qquad\text{ou}\qquad
 c^+(x,y)=u^+_{loc}\,c_{loc}.
\]

Le texte définit ensuite

\[
 M_C=\int_{\mathbb R^2} c^+(x,y)\,d\sigma
 \tag{7.13}
\]

et indique explicitement que cette quantité totale transportée « should be conserved » par le modèle de transport réduit, avec c⁺ comme condition d'entrée.

**Résultat nouveau :** la thèse confirme que la revendication de conservation de l'article de 2008 n'est pas simplement une extrapolation secondaire ; elle apparaît explicitement dans la formulation du modèle de transport lointain de la thèse, équations (7.12)–(7.13), p. 129. Elle ne fournit toutefois pas, dans ce passage, une démonstration de cette conservation.

### 3. Contrôle dimensionnel des deux branches de (7.12)

Sous l'interprétation [c_loc] = M L⁻³, cette hypothèse est étayée par la thèse elle-même : au chapitre 5, §5.6.3, p. 101, les équations (5.54)–(5.55) donnent à la concentration liée au modèle local l'unité kg·m⁻³ et au coefficient de calibration l'unité s⁻¹ ; les équations (5.61)–(5.64), pp. 101–102, calculent ensuite des pertes de masse par intégration volumique ou par flux vertical intégré dans le temps. En appliquant ces unités à c_loc dans (7.12), avec z une coordonnée de longueur et dσ une mesure surfacique :

- Branche intégrée en hauteur : [∫ c_loc dz] = M L⁻², donc [M_C] = M. Elle est dimensionnellement compatible avec un inventaire de masse.
- Branche produit : la thèse définit u⁺_loc = max(0, (u_loc·ẑ)/||u_loc||). Ce rapport est sans dimension. Ainsi [u⁺_loc c_loc] = M L⁻³, puis [M_C] = M L⁻¹ après intégration surfacique.

Les deux branches de (7.12) ne sont donc pas dimensionnellement équivalentes sous ces conventions. La deuxième ne représente pas une masse totale sans facteur ou normalisation supplémentaire. La section 1.2.4 mentionne par ailleurs une concentration sans dimension dans le cadre de la formulation de Fick, mais la partie applicative locale précise explicitement kg·m⁻³ pour $c_{loc}$ ; aucune relation ne redéfinit $c_{loc}$ comme une quantité sans dimension dans le chapitre 7.

### 3.1 Comparaison avec le chapitre Springer de 2008 : l'ambiguïté est antérieure à la thèse

La copie consultée du chapitre 14, §2.2, p. imprimée 248, présente déjà la même formule : $c^+(x,y)=\int_{z>H}c_l\,dz$ **ou** $c^+(x,y)=u_l^+c_l$, avec $u_l^+=\max(0,(u\cdot\hat z)/\|u\|)$, puis $C=\int_{\mathbb R^2}c^+\,d\sigma$ annoncé comme quantité à conserver. La thèse reprend cette construction en équations (7.12)–(7.13), p. 129, en changeant les indices en $loc$ et en nommant la quantité $M_C$. La formule est donc **déjà présente dans le chapitre de 2008** ; elle n'est ni une erreur d'OCR propre à la thèse, ni une faute isolée que l'on peut attribuer avec preuve à la rédaction de la thèse.

Le diagnostic le plus fort justifié par les sources est une **incohérence dimensionnelle de la spécification publiée**, répétée dans le chapitre et la thèse. Cela constitue une erreur de formulation conceptuelle au niveau du modèle tel qu'il est écrit si les deux branches sont censées être des définitions alternatives de la même quantité conservée. On ne peut toutefois pas établir si la cause historique est une coquille répétée, une variable insuffisamment définie, ou une confusion entre une concentration pondérée par une direction et une quantité intégrée : les sources consultées ne donnent ni facteur de longueur manquant, ni autre convention dimensionnelle explicite. Il faut donc corriger la reconstruction de J-DriftX en choisissant et justifiant une définition cohérente, mais **ne pas modifier silencieusement la transcription historique ni affirmer que l'intention exacte des auteurs est connue**.

Une correction dimensionnellement possible dépend de la quantité physique visée :
- pour un inventaire de masse traversant un plan horizontal, $\int c_{loc}\,dz$ fournit une masse par aire, puis son intégrale surfacique fournit une masse ;
- pour un débit massique vertical, il faudrait un flux contenant la composante verticale dimensionnée $u_z$ (en m/s), puis une intégrale surfacique fournirait une masse par temps, à intégrer dans le temps pour obtenir une masse ;
- remplacer le cosinus directionnel $u_l^+$ par $u_z$ ne rendrait pas les deux branches équivalentes : cela définirait une autre grandeur physique. Aucune de ces réparations n'est confirmée comme intention des auteurs.

### 4. Ce que la thèse établit — et ce qu'elle n'établit pas

| Proposition | Verdict documentaire |
|---|---|
| Le modèle lointain introduit c⁺ par deux expressions alternatives | Explicitement imprimé, Eq. (7.12), p. 129 |
| Le modèle vise à conserver M_C = ∫ c⁺ dσ | Explicitement affirmé, Eq. (7.13), p. 129 |
| Les deux expressions de c⁺ sont équivalentes dimensionnellement | Non, sous les unités conventionnelles ci-dessus ; la même incohérence est imprimée dans le chapitre 2008 et reprise par la thèse |
| Une masse globale est conservée sur chaque surface iso-temps de transport | Non démontré dans ce passage |
| Le modèle historique définit une transformation globale régulière avec jacobien calculable | Non établi par les passages consultés |
| L'affirmation de conservation est prouvée pour le modèle réduit général | Non : « should be conserved » est un objectif/propriété attendue, sans preuve dans ce passage |

## Conséquence pour l'audit G0-S

Le contrôle croisé de la thèse et du chapitre 2008 clôt l'ambiguïté sur l'origine de l'écart : la formule problématique est imprimée dans les deux sources, avec la même définition sans dimension de $u^+$. Le verdict est donc **incohérence dimensionnelle publiée et reproduite dans la thèse**, pas artefact OCR. L'intention corrective exacte reste non déterminable à partir de ces sources. Cela ne clôt pas l'issue #123, car le bilan de conservation du modèle lointain reste à démontrer. Conserver trois objets distincts :

1. **Inventaire global de masse** du scalaire dans un volume ;
2. **Quantité d'entrée M_C** du modèle réduit, construite à partir de c⁺ sur le plan horizontal ;
3. **Flux à travers une surface iso-temps de transport**, qui exigerait une définition de surface, une transformation de coordonnées et un bilan incluant sources, puits et flux latéraux.

Le théorème conditionnel dans [la note de conservation](32-conservation-coordonnees-travel-time.md) et le cas uniforme explicite dans [la note de transformation τ-η](37-transformation-tau-eta-cas-uniforme.md) restent des résultats séparés. Ils ne constituent pas une preuve rétroactive pour le champ variable historique.

## Contrôles restant à effectuer sur le binaire versionné

- [ ] Ouvrir le PDF poussé dans la PR et confirmer visuellement la page de titre.
- [ ] Confirmer le nombre de pages, les numéros de pages imprimées et la présence des pages 126–129.
- [ ] Comparer le binaire à la copie miroir et au fichier HAL (empreinte SHA-256, puis comparaison du texte ou du PDF si les fichiers sont disponibles localement).
- [ ] Vérifier les droits de redistribution du binaire présent dans Git.
- [x] Vérifier visuellement sur la copie miroir la page imprimée 129 et les équations (7.12)–(7.13) ; comparer la forme de (7.12) au chapitre 2008 p. 248. Résultat : formule identique et incohérence dimensionnelle présente dans les deux sources. Cette vérification ne certifie pas l'identité du PDF versionné avec HAL.
- [ ] Poursuivre la recherche d'une définition explicite de la transformation de coordonnées et d'une preuve de conservation dans la thèse, sans présumer qu'elle existe.

## Références

- Brun, J.-M. (2007 selon les notices et les références citées), *Modèles à complexité réduite de transport pour applications environnementales*, thèse, Université Montpellier II. Notice : https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c.
- Copie miroir consultée : https://www.mcours.net/cours/pdf/yass2/yass2cllic260.pdf.
- Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », chap. 14, pp. 245–256, DOI https://doi.org/10.1007/978-1-4020-8758-5_14. Copie tierce consultée pour le contrôle de l'équation p. 248 : https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf (ce lien atteste le fichier consulté, pas une autorisation de redistribution).
- Mohammadi, B. & Brun, J.-M. (2006), « Similitude généralisée et modélisation géométrique à complexité réduite », *Comptes Rendus Mécanique*, 334(10), 634–638, DOI https://doi.org/10.1016/j.crme.2006.06.007.
