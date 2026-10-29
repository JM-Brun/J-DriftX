"""EDP transitoire du puff : marche en temps de la marginale transverse.

Cette étape reconstruit une seconde route de calcul pour la source
impulsionnelle de l'étape 6 : la marginale transverse Q(y, z, t) du puff
(intégrale longitudinale de la concentration, kg m⁻²) vérifie ∂Q/∂t =
Ky(t)·∂²Q/∂y² + Kz(t)·∂²Q/∂z², avec K = (u/2)·d(sigma²)/dx évalué à la
distance parcourue d = u·t (Briggs via le modèle injecté). La condition
d'entrée est la marginale fermée du package posée au premier instant de
passage ; la marche est explicite en temps (FTCS : Forward in Time,
Centred in Space), le sol est de type
miroir (Neumann : ∂Q/∂z = 0 au sol, exact ici car le noyau du puff est
pair en z), les bords latéraux et le sommet de fenêtre sont de Dirichlet
nul (la valeur y est imposée nulle). La structure longitudinale reste
analytique (carte travel-time de la
note 37, isotropie sigma_x = sigma_y du noyau fermé) : C(x, y, z, t) est
la marginale échantillonnée multipliée par le facteur gaussien
longitudinal évalué à d = u·t.

Architecture (séparation des considérations, une par module) :

- ``marginale`` : la marginale fermée et son bilan de masse sur la grille
  (``MarginaleFermee``), condition d'entrée du schéma et référence des
  écarts de masse.
- ``solveur`` : la géométrie des passages (``PassagesPuff``) et le schéma
  FTCS marché en temps (``SolveurTransitoire``) ; réutilise le pas
  longitudinal stable de l'étape 5 (``pas_longitudinal``, divisé par u :
  même nombre de Fourier) et la grille EDP partagée (``GrilleEdp``).
- ``routes`` : les deux routes mesurées séparément (note 35), chacune
  rendant sa mesure typée (``MesureFermeePuff``, ``MesureEdpPuff``), et
  la structure longitudinale injectable (``StructureLongitudinale``) ;
  l'échantillonnage bilinéaire et le bilan d'intégrale réutilisent
  ``EchantillonneurBilineaire`` (étape 5).
- ``comparaison`` : les modèles Pydantic gelés de la comparaison et du
  manifeste étiqueté ; ``comparer_transitoire`` orchestre les deux routes
  et ``assembler_comparaison`` assemble les mesures typées en métriques.
- cette façade re-exporte l'API publique du package, importable comme le
  module historique : ``jdriftx.experiences.transitoire_puff``.

Étiquetage explicite, conformément à l'ordre confirmé de l'issue #232 :

- Héritage documentaire : aucune source historique ; cette étape est la
  suite directe de l'évaluation dirigée du puff (note 53) et n'utilise
  aucun chiffre de l'ouvrage de 2008 comme cible.
- Reconstruction : marche explicite FTCS en temps (nombre de Fourier
  borné à 1/3 au dernier passage), entrée fermée au premier instant de
  passage, miroir au sol, Dirichlet aux bords de fenêtre, structure
  longitudinale analytique.
- Extension : seconde extension conditionnelle du contrat minimal
  (docs/47 §5) : la source impulsionnelle de la note 53 reçoit sa route
  EDP transitoire, sur la grille du cas S0 figé (docs/48 §2.2).

Garde-fous : la comparaison est un contrôle d'auto-cohérence entre deux
routes du même package sur un cas synthétique ; ce n'est pas une
validation physique. Le noyau du puff est symétrique en z autour du sol
(sans hauteur de source) : la moitié de la masse du noyau fermé est
formellement sous le sol, la grille porte la demi-colonne miroir, et les
écarts de masse sont comparés à la marginale analytique sur la même
grille, pas à la masse totale. Les ``dict`` restent confinés à la
frontière d'export JSON (``model_dump`` de Pydantic), conformément à la
charte du projet.
"""

from jdriftx.experiences.transitoire_puff.comparaison import (
    ComparaisonTransitoire,
    ManifesteTransitoire,
    PointComparaisonPuff,
    assembler_comparaison,
    comparer_transitoire,
    construire_manifeste,
)
from jdriftx.experiences.transitoire_puff.marginale import MarginaleFermee
from jdriftx.experiences.transitoire_puff.routes import (
    FacteurLongitudinalAnalytique,
    MesureEdpPuff,
    MesureFermeePuff,
    RouteEdpPuff,
    RouteFermeePuff,
    StructureLongitudinale,
)
from jdriftx.experiences.transitoire_puff.solveur import (
    InstantPuff,
    PassagesPuff,
    SolutionTransitoire,
    SolveurTransitoire,
    resoudre_transitoire,
)

__all__ = [
    "ComparaisonTransitoire",
    "FacteurLongitudinalAnalytique",
    "InstantPuff",
    "ManifesteTransitoire",
    "MarginaleFermee",
    "MesureEdpPuff",
    "MesureFermeePuff",
    "PassagesPuff",
    "PointComparaisonPuff",
    "RouteEdpPuff",
    "RouteFermeePuff",
    "SolutionTransitoire",
    "SolveurTransitoire",
    "StructureLongitudinale",
    "assembler_comparaison",
    "comparer_transitoire",
    "construire_manifeste",
    "resoudre_transitoire",
]
