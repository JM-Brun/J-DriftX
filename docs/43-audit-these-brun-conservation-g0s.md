# Audit de la thèse de Brun — conservation du transport lointain (G0-S)

> **Mise à jour du 8 novembre 2026 :** la page de titre et la page imprimée 129 (PDF 138) ont été vérifiées visuellement dans le PDF versionné ; celui-ci compte 204 pages. La soutenance est datée du 21 septembre 2007. L'empreinte et les limites d'identité sont précisées dans la [provenance](../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md) et la [fiche de lecture](bibliographie/sources/these-brun.md). Les paragraphes datés ci-dessous conservent leur contexte historique.

**État au 29 octobre 2026 :** le PDF de thèse associé à HAL `tel-02589999` a déjà été obtenu par une voie appropriée, et cette provenance est documentée dans [`raw/provenance`](../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md). Il ne faut pas recommencer l'acquisition. Le texte et la page imprimée 129 (équations 7.12–7.13) ont également été inspectés sur une copie miroir tierce ; la forme imprimée des deux alternatives de $c^+$ est vérifiée visuellement sur cette copie, pas seulement via OCR. Le chapitre Springer 2008 a été inspecté dans une copie tierce et imprime la même alternative avec la même définition sans dimension de $u_l^+$. **Le contrôle d'identité binaire entre le fichier HAL déjà obtenu, le PDF versionné et les copies tierces est une vérification distincte, dont le résultat doit être recherché dans les éléments de provenance existants avant de la déclarer manquante.** Le diagnostic dimensionnel est indépendant de cette identité binaire, car les deux textes consultés montrent la même formule.

## Sources et niveau de confiance

- Notice AGRIS/INRAE, titre *Modèles à complexité réduite de transport pour applications environnementales*, auteur J.-M. Brun, thèse, notice de 2007 : https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c
- Notice et fichier HAL liés par AGRIS : https://hal.inrae.fr/tel-02589999/document et https://hal.inrae.fr/tel-02589999/file/pub00023263.pdf
- Copie miroir consultée pour la lecture du texte : https://www.mcours.net/cours/pdf/yass2/yass2cllic260.pdf (PDF de 201 pages selon le lecteur web ; hébergeur tiers, non institutionnel).
- Le PDF présent dans `raw/` a été contrôlé : titre et soutenance en page PDF 2, 204 pages et empreinte consignés dans le [sidecar de provenance](../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md). Son identité avec les octets servis par HAL n'est pas établie par la notice ou le bandeau HAL.

La copie miroir a servi à une première lecture ; son extraction affichée commençait aux remerciements, sans page de titre visible. Depuis, la page de titre du **fichier versionné** a été inspectée visuellement. Ne pas qualifier pour autant la copie miroir ou le fichier versionné de « version HAL vérifiée » au sens d'une identité binaire indépendante.

## Passages déterminants

### 1. Définition du temps de migration

Dans le chapitre 7, §7.1.3, page imprimée 128 (PDF 137), la distance orientée est définie de façon asymétrique. Si A est au vent de B, le texte définit le temps de migration par une intégrale le long de la caractéristique passant par A jusqu'à la projection B⊥, puis précise que la vitesse locale u est tangente à cette caractéristique. Le texte suppose la caractéristique unique et indique comment départager des projections multiples (équations (7.6)–(7.7), p. 128).

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

Sous l'interprétation [c_loc] = M L⁻³, cette hypothèse est étayée par la thèse elle-même : au chapitre 5, §5.6.2 « Losses Calculation », pp. imprimées 101–103, les équations (5.54)–(5.55), p. 102 (PDF p. 111), donnent à la concentration liée au modèle local l'unité kg·m⁻³ et au coefficient de calibration l'unité s⁻¹. Les équations (5.61)–(5.63), p. 102, calculent les pertes par intégration volumique ; les équations (5.64)–(5.67), p. 103 (PDF p. 112), formulent le bilan alternatif par flux vertical intégré dans le temps. La section 5.6.3, p. 103, commence après ces équations et décrit l'implémentation numérique.

**Précision sur le couplage local.** Les équations (5.56)–(5.57) donnent directement à $c_{loc}$ l'unité kg·m⁻³. Le taux volumique normalisé et le flux traversant le plan ont les mêmes unités intégrées mais ne sont pas identiques en général : les hypothèses de leur rapprochement en (5.67) sont analysées dans la [fiche de lecture](bibliographie/sources/these-brun.md) et suivies sous DRX-ERR-042. Cela ne modifie pas le contrôle dimensionnel de (7.12).

En appliquant ces unités à $c_{loc}$ dans (7.12), avec $z$ une coordonnée de longueur et $d\sigma$ une mesure surfacique :

- Branche intégrée en hauteur : [∫ c_loc dz] = M L⁻², donc [M_C] = M. Elle est dimensionnellement compatible avec un inventaire de masse.
- Branche produit : la thèse définit u⁺_loc = max(0, (u_loc·ẑ)/||u_loc||). Ce rapport est sans dimension. Ainsi [u⁺_loc c_loc] = M L⁻³, puis [M_C] = M L⁻¹ après intégration surfacique.

Les deux branches de (7.12) ne sont donc pas dimensionnellement équivalentes sous ces conventions. La deuxième ne représente pas une masse totale sans facteur ou normalisation supplémentaire. La section 1.2.4 mentionne par ailleurs une concentration sans dimension dans le cadre de la formulation de Fick, mais la partie applicative locale précise explicitement kg·m⁻³ pour $c_{loc}$ ; aucune relation ne redéfinit $c_{loc}$ comme une quantité sans dimension dans le chapitre 7.

La définition imprimée de $u^+_{loc}$ comporte également $\lVert u_{loc}\rVert$ au dénominateur : elle n'est pas définie aux points où $u_{loc}=0$. Une convention de stagnation serait nécessaire pour évaluer cette branche en ces points ; cette difficulté est distincte du désaccord d'unités et ne détermine pas le comportement du code historique.

### 3.1 Comparaison avec le chapitre Springer de 2008 : formule présente dans les deux sources

La copie consultée du chapitre 14, §2.2, p. imprimée 248, présente la même formule : $c^+(x,y)=\int_{z>H}c_l\,dz$ **ou** $c^+(x,y)=u_l^+c_l$, avec $u_l^+=\max(0,(u\cdot\hat z)/\|u\|)$, puis $C=\int_{\mathbb R^2}c^+\,d\sigma$ annoncé comme quantité à conserver. La thèse soutenue en 2007 imprime cette construction en équations (7.12)–(7.13), p. 129, avec les indices $loc$ et la quantité $M_C$. Le chapitre paraît en 2008, après la soutenance ; ces dates et la similitude des textes ne suffisent pas à établir le sens exact de filiation entre leurs versions de rédaction. La formule n'est pas une erreur d'OCR propre à la thèse.

Le diagnostic le plus fort justifié par les sources est une **incohérence dimensionnelle de la spécification publiée**, répétée dans le chapitre et la thèse. Cela constitue une erreur de formulation conceptuelle au niveau du modèle tel qu'il est écrit si les deux branches sont censées être des définitions alternatives de la même quantité conservée. On ne peut toutefois pas établir si la cause historique est une coquille répétée, une variable insuffisamment définie, ou une confusion entre une concentration pondérée par une direction et une quantité intégrée : les sources consultées ne donnent ni facteur de longueur manquant, ni autre convention dimensionnelle explicite. Il faut donc corriger la reconstruction de J-DriftX en choisissant et justifiant une définition cohérente, mais **ne pas modifier silencieusement la transcription historique ni affirmer que l'intention exacte des auteurs est connue**.

Une correction dimensionnellement possible dépend de la quantité physique visée :
- pour l'inventaire de masse d'une colonne située au-dessus d'un plan horizontal, $\int c_{loc}\,dz$ fournit une masse par aire, puis son intégrale surfacique fournit une masse ; cet inventaire ne mesure pas à lui seul la masse ayant traversé le plan ;
- pour un débit massique vertical, il faudrait un flux contenant la composante verticale dimensionnée $u_z$ (en m/s), puis une intégrale surfacique fournirait une masse par temps, à intégrer dans le temps pour obtenir une masse ;
- remplacer le cosinus directionnel $u_l^+$ par $u_z$ ne rendrait pas les deux branches équivalentes : cela définirait une autre grandeur physique. Aucune de ces réparations n'est confirmée comme intention des auteurs.

### 3.2 Correction recommandée pour une reconstruction cohérente, avec impact minimal sur la thèse

**Reconstruction proposée pour J-DriftX : retenir un inventaire de masse.** Cette option conserve la première branche de (7.12), la définition surfacique de (7.13), le symbole $M_C$ et l'objectif annoncé de conservation d'une quantité totale. Elle ne prouve pas que cette interprétation était l'intention des auteurs, ni qu'un choix a déjà été implémenté ou validé dans le noyau scientifique.

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
6. **Ajouter une note d'errata traçable** : signaler que la formule présente dans la thèse de 2007 et le chapitre de 2008 contient deux branches dimensionnellement incompatibles sous les unités explicites ; indiquer que l'édition corrigée retient l'inventaire de masse par intégration verticale, sans prétendre établir l'intention historique.
7. **Ne pas revendiquer une preuve du modèle lointain par cette correction** : la cohérence dimensionnelle répare la définition de la grandeur, mais la conservation effective doit encore être démontrée à partir des équations d'évolution, du domaine, des sources/puits et des conditions aux limites.

**Pourquoi ce choix minimise l'impact :** il conserve l'intégrale verticale déjà imprimée, l'intégration horizontale déjà imprimée et le symbole de masse $M_C$ ; il retire seulement l'alternative non équivalente et précise les hypothèses de conservation. La correction est donc locale à la définition et à la portée de l'affirmation. Elle reste une recommandation pour une édition corrigée, pas une affirmation sur l'intention des auteurs ni une preuve que le modèle historique satisfait le bilan.

### 4. Ce que la thèse établit — et ce qu'elle n'établit pas

| Proposition | Verdict documentaire |
|---|---|
| Le modèle lointain introduit c⁺ par deux expressions alternatives | Explicitement imprimé, Eq. (7.12), p. 129 |
| Le modèle vise à conserver M_C = ∫ c⁺ dσ | Explicitement affirmé, Eq. (7.13), p. 129 |
| Les deux expressions de c⁺ sont équivalentes dimensionnellement | Non, sous les unités conventionnelles ci-dessus ; la même incohérence est imprimée dans la thèse de 2007 et le chapitre de 2008 |
| Une masse globale est conservée sur chaque surface iso-temps de transport | Non démontré dans ce passage |
| Le modèle historique définit une transformation globale régulière avec jacobien calculable | Non établi par les passages consultés |
| L'affirmation de conservation est prouvée pour le modèle réduit général | Non : « should be conserved » est un objectif/propriété attendue, sans preuve dans ce passage |

### 5. Contrôle croisé de conservation dans la thèse

**Recherche effectuée le 9 novembre 2026.** L'extraction textuelle des 204 pages du fichier versionné a été parcourue par recherche des radicaux `conserv`, `jacob`, `coordonn`, `coordinate`, `projection`, `isochron` et `characteristic` ; toutes les pages produisent du texte. Cette recherche sert au repérage : l'extraction peut perdre des symboles, des caractères et des arguments placés dans les figures, donc l'absence de résultat pour un mot n'est pas une preuve d'absence. Les passages décisifs ci-dessous ont été rapprochés du fac-similé et des lectures ciblées déjà consignées.

| Passage | Grandeur / construction trouvée | Portée pour G0-S |
|---|---|---|
| Chapitre 1, (1.56)–(1.57), p. 31 (PDF 40) | Approximation de panache mince puis flux $M_f=\int_{-\infty}^{\infty}\int_0^\infty \bar u\,\bar c\,dz\,dy$, en kg/s, sur une section $y,z$ normale au vent. | C'est un **débit massique de section** sous hypothèses de panache ; il n'est ni l'inventaire $M_C$ en kg, ni une démonstration sur des surfaces iso-temps en champ variable. La formule et l'approximation ont été contrôlées visuellement. |
| Chapitre 7, (7.6)–(7.7), pp. 127–128 (PDF 136–137) et fig. 7.4, p. 132 (PDF 141) | Temps le long d'une caractéristique vers une projection et repère local $(s,n)$ illustré autour d'une caractéristique. | Ces objets ne spécifient pas à eux seuls une transformation globale, son domaine, son inverse et son jacobien. Le repère de la figure est local, et non une preuve de bijectivité globale. |
| Chapitre 7, (7.12)–(7.15) et (7.20), pp. 129–131 (PDF 138–140) | Entrée $c^+$, quantité $M_C$ annoncée conservée et famille de profils généralisés. | La condition de conservation est revendiquée ; les passages consultés ne dérivent pas un bilan pour cette famille avec jacobien, sources et frontières. Le contrôle ci-dessous donne une condition supplémentaire même en vent uniforme. |
| Annexe B.2, (B.55)–(B.56), pp. 155–156 (PDF 164–165) ; annexe F, pp. 173–175 (PDF 182–184) | L'annexe B impose un bilan de section dans son exemple de similitude ; l'annexe F étudie des coûts de trajet. | Le premier résultat est conditionnel au cas simplifié de B.2 ; le second ne fournit pas à lui seul un bilan du scalaire ou une transformation globale. Voir la [fiche de lecture](bibliographie/sources/these-brun.md). |

**Bilan de référence.** Pour une concentration $c$, un flux massique total $J$, une source $s$ et un puits $\ell$, la conservation locale $\partial_t c+\nabla\!\cdot J=s-\ell$ donne, sur un volume fixe $\Omega$ et pour la normale sortante $n$,

$$
\frac{d}{dt}\int_\Omega c\,dV
=\int_\Omega(s-\ell)\,dV-\int_{\partial\Omega}J\cdot n\,dS.
$$

La masse du volume n'est constante que si le bilan net sources, puits et frontière s'annule. Pour un volume au-dessus de $H$, la contribution du plan inférieur fait partie de cette frontière ; elle ne disparaît pas du seul fait que l'on a défini l'intégrale verticale de (7.12). Dans un tube de courant stationnaire sans source ni puits, si le flux total à travers les parois latérales est nul, le théorème de divergence relie les flux à ses deux sections. Cette proposition conditionnelle ne démontre pas que les iso-temps historiques sont ces sections ni que leurs parois satisfont cette condition, notamment en présence de diffusion.

**Contrôle analytique en vent uniforme.** La thèse donne en (7.15) une forme axiale exponentielle et une forme radiale exponentielle. Pour tester une reconstruction particulière, prenons ces formes comme des égalités avec $C_0>0$, $a>0$, $b(x)>0$, $U>0$ et $r=\sqrt{y^2+z^2}$ :

$$
c(x,y,z)=C_0e^{-ax}e^{-b(x)r},\qquad
Q(x)=\int_{-\infty}^{\infty}\int_0^\infty Uc\,dz\,dy
=\frac{\pi U C_0e^{-ax}}{b(x)^2}.
$$

Le facteur $\pi$ correspond à la section demi-plane $z\ge0$. Là où $b$ est dérivable, la constance de $Q$ exige $b'(x)/b(x)=-a/2$. Pour $a=1/L$ et $b(x)=b_0/(1+x/L)$ avec $L,b_0>0$, le profil s'élargit mais $Q(L)/Q(0)=4/e\simeq1{,}47$ : le débit de section n'est pas conservé. Cet exemple reconstruit ne prétend pas reproduire les paramètres ou la sortie historique ; il montre que les **formes seules** n'imposent pas le bilan sans relation supplémentaire entre amplitude et largeur. Une variation de débit exigerait un bilan compatible avec des sources, puits ou autres contributions de flux ; elle ne prouve pas une erreur de la simulation historique.

**Verdict de recherche.** Le repérage et les passages examinés ne mettent pas en évidence de preuve complète de conservation du modèle lointain à champ variable ni de carte globale avec jacobien. Cela ne prouve pas qu'aucune preuve n'existe dans un autre document ou qu'elle serait impossible. La recherche documentaire est effectuée ; la preuve mathématique et la reconstruction du modèle restent ouvertes dans [docs/32](32-conservation-coordonnees-travel-time.md) et [#123](https://github.com/JM-Brun/J-DriftX/issues/123).

## Conséquence pour l'audit G0-S

Le contrôle croisé de la thèse et du chapitre 2008 établit que la formule problématique est imprimée dans les deux sources, avec la même définition sans dimension de $u^+$ ; il ne démontre pas la filiation de leurs rédactions. Le verdict est une **incohérence dimensionnelle présente dans les deux sources**, pas un artefact OCR. L'intention corrective exacte reste non déterminable à partir de ces sources. Cela ne clôt pas l'issue #123, car le bilan de conservation du modèle lointain reste à démontrer. Conserver trois objets distincts :

1. **Inventaire global de masse** du scalaire dans un volume ;
2. **Quantité d'entrée M_C** du modèle réduit, construite à partir de c⁺ sur le plan horizontal ;
3. **Flux à travers une surface iso-temps de transport**, qui exigerait une définition de surface, une transformation de coordonnées et un bilan incluant sources, puits et flux latéraux.

Le théorème conditionnel dans [la note de conservation](32-conservation-coordonnees-travel-time.md) et le cas uniforme explicite dans [la note de transformation τ-η](37-transformation-tau-eta-cas-uniforme.md) restent des résultats séparés. Ils ne constituent pas une preuve rétroactive pour le champ variable historique.

## État des contrôles sur le binaire et la conservation

- [x] Confirmer visuellement la page de titre du PDF versionné.
- [x] Vérifier les pages imprimées 126–129 sur le PDF versionné : pages PDF 135–138 ; le fichier compte 204 pages PDF.
- [x] Consulter les éléments de provenance archivés et comparer les copies locales repérées : le fichier joint et le binaire versionné ont la même empreinte ; une autre copie locale diffère uniquement par dix octets de dates PDF. Les détails et limites sont consignés dans le [sidecar](../raw/provenance/Modèles%20à%20complexité%20réduite%20de%20transport%20pour%20applications%20environnementales%20-%20pub00023263.pdf.md). Aucune copie identifiée comme octets originaux HAL n'a été retrouvée dans ce périmètre ; ne pas relancer l'acquisition.
- [ ] Établir une comparaison binaire indépendante avec les octets originaux HAL si une copie dont la provenance est prouvée ou une empreinte archivée devient disponible. Les copies locales ne permettent pas de clore cette identité.
- [ ] Établir les droits de redistribution du binaire présent dans Git : la notice bibliographique et les éléments examinés n'établissent pas une autorisation ou licence de redistribution pour ce fichier. Une preuve du titulaire des droits ou des conditions applicables reste nécessaire.
- [x] Vérifier visuellement sur la copie miroir la page imprimée 129 et les équations (7.12)–(7.13) ; comparer la forme de (7.12) au chapitre 2008 p. 248. Résultat : formule identique et incohérence dimensionnelle présente dans les deux sources. Cette vérification ne certifie pas l'identité du PDF versionné avec HAL.
- [x] Vérifier visuellement les équations (7.12)–(7.13) sur le PDF versionné, p. 138.
- [x] Rechercher dans le texte extrait de la thèse et examiner les passages pertinents pour la transformation et la conservation ; méthode, résultats et limites figurent au §5 ci-dessus. Ce contrôle n'établit ni une preuve générale ni l'impossibilité d'en construire une.
- [ ] Démontrer ou réfuter la conservation pour une formulation complètement spécifiée du modèle lointain à champ variable, avec domaine, transformation, jacobien, sources/puits et frontières ; ce travail mathématique n'est pas clos par la recherche documentaire.

## Références

- Brun, J.-M. (2007 selon les notices et les références citées), *Modèles à complexité réduite de transport pour applications environnementales*, thèse, Université Montpellier II. Notice : https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c.
- Copie miroir consultée : https://www.mcours.net/cours/pdf/yass2/yass2cllic260.pdf.
- Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », chap. 14, pp. 245–256, DOI https://doi.org/10.1007/978-1-4020-8758-5_14. Copie tierce consultée pour le contrôle de l'équation p. 248 : https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf (ce lien atteste le fichier consulté, pas une autorisation de redistribution).
- Mohammadi, B. & Brun, J.-M. (2006), « Similitude généralisée et modélisation géométrique à complexité réduite », *Comptes Rendus Mécanique*, 334(10), 634–638, DOI https://doi.org/10.1016/j.crme.2006.06.007.
