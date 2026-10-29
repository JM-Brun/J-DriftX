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

### 3.2 Correction recommandée pour une reconstruction cohérente, avec impact minimal sur la thèse

**Choix retenu pour J-DriftX : conserver un inventaire de masse, et non un flux massique.** C'est l'option qui demande le moins de changements conceptuels au passage historique : elle conserve la première branche de (7.12), la définition surfacique de (7.13), le symbole $M_C$ et l'objectif annoncé de conservation d'une quantité totale. Elle ne prouve pas que cette interprétation était l'intention des auteurs ; c'est une décision explicite de reconstruction.

Avec $[c_{loc}]=\mathrm{kg\,m^{-3}}$, définir
\[
 c^+(x,y) := \int_H^{z_{\max}} c_{loc}(x,y,z)\,dz
 \quad\text{(ou }\int_{z>H}c_{loc}\,dz\text{ si le domaine vertical est non borné),}
\]
où $H$ est la hauteur de référence et $z_{\max}$ la limite supérieure du domaine lorsqu'elle existe. Alors $[c^+]=\mathrm{kg\,m^{-2}}$ et
\[
 M_C := \int_{\Omega_{xy}} c^+(x,y)\,dx\,dy
\]
est une masse en kg, à condition que $\Omega_{xy}$ soit le domaine horizontal pertinent et que l'intégrale converge. Cette quantité est l'inventaire de masse dans la colonne verticale au-dessus de $H$ sur le domaine horizontal considéré. **Ce n'est pas, à elle seule, un débit traversant une surface** : un débit massique exige un flux avec vitesse dimensionnée et une intégration sur une surface, en kg/s.

La branche $u^+_{loc}c_{loc}$ doit donc être retirée de la définition de $c^+$ dans la reconstruction, ou présentée séparément comme une autre grandeur sans lui attribuer la même masse conservée. Puisque $u^+_{loc}=\max(0,(u\cdot\hat z)/\|u\|)$ est un cosinus directionnel sans dimension, elle ne peut pas remplacer l'intégration verticale sans introduire une échelle dimensionnelle supplémentaire et une justification physique indépendante.

#### Corrections éditoriales recommandées dans le texte de la thèse

Ces propositions sont des corrections à apporter dans une édition corrigée ou une note d'errata, pas des modifications à appliquer silencieusement à la transcription historique :

1. **Équation (7.12), p. 129 — supprimer l'alternative dimensionnellement incompatible** pour la définition retenue : garder l'intégrale verticale et définir explicitement ses bornes/domaine ; ne pas conserver « ou $u^+_{loc}c_{loc}$ » comme égalité alternative.
2. **Définir les unités à la première occurrence** : $c_{loc}$ en kg·m⁻³, $c^+$ en kg·m⁻², $d\sigma=dx\,dy$ en m², et $M_C$ en kg. Si les auteurs souhaitaient une concentration normalisée ou une autre variable, cette convention devrait être explicitée et toutes les unités réconciliées ; les sources consultées ne justifient pas cette hypothèse.
3. **Équation (7.13) — préciser le domaine d'intégration** : remplacer $\mathbb R^2$ par $\Omega_{xy}$ si le domaine physique/calcul est fini, et indiquer les conditions de décroissance/intégrabilité si $\mathbb R^2$ est conservé.
4. **Remplacer la phrase « should be conserved » par une proposition conditionnelle vérifiable** : annoncer que la masse totale est conservée seulement pour un bilan fermé sans sources/puits nets, sans dépôt/pertes non comptabilisés, avec conditions aux limites compatibles et sans fuite nette par les frontières latérales/verticales. Si le modèle est censé conserver la masse malgré des sources, puits ou sorties, expliciter le terme de bilan correspondant. La conservation de $M_C$ ne découle pas de la seule définition de $c^+$.
5. **Séparer inventaire et flux** : ne pas appeler $M_C$ « flux » ou « masse traversant le plan » sans définition supplémentaire. Si la grandeur visée est en réalité un débit massique, définir un flux physique adapté à la concentration massique, par exemple $\mathbf F=c_{loc}\mathbf u-D\nabla c_{loc}$, d'unités kg·m⁻²·s⁻¹, puis $\dot M=\int_S\mathbf F\cdot\mathbf n\,dS$ en kg/s ; la masse transférée s'obtient en intégrant ce débit dans le temps.
6. **Ajouter une note d'errata traçable** : signaler que la formule publiée en 2008 et reprise en thèse contient deux branches dimensionnellement incompatibles sous les unités explicites ; indiquer que l'édition corrigée retient l'inventaire de masse par intégration verticale, sans prétendre établir l'intention historique.
7. **Ne pas revendiquer une preuve du modèle lointain par cette correction** : la cohérence dimensionnelle répare la définition de la grandeur, mais la conservation effective doit encore être démontrée à partir des équations d'évolution, du domaine, des sources/puits et des conditions aux limites.

**Pourquoi ce choix minimise l'impact :** il conserve l'intégrale verticale déjà imprimée, l'intégration horizontale déjà imprimée et le symbole de masse $M_C$ ; il retire seulement l'alternative non équivalente et précise les hypothèses de conservation. La correction est donc locale à la définition et à la portée de l'affirmation. Elle reste une recommandation pour une édition corrigée, pas une affirmation sur l'intention des auteurs ni une preuve que le modèle historique satisfait le bilan.

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
