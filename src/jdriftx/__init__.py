"""J-DriftX : reprise de recherche sur la dispersion atmosphérique à complexité réduite.

Le projet étudie les formulations historiques de Drift-X (J.-M. Brun et
B. Mohammadi, 2006-2009). La primitive actuelle de temps de parcours calcule
un coût sur une polyligne fournie; elle ne reproduit pas encore la
pseudo-distance historique ni un modèle de dispersion validé.

Les modules d'enseignement (`trajectories`, `fields`, `terrain`,
`periodic_transport`, `advection_diffusion`) ne sont pas exportés à la racine :
ils servent aux applications interactives et aux tests, pas à l'API publique du
package (audit docs/25, recommandation 7).
"""

from jdriftx.champ_analytique import ChampFonctionCourant, ChampPlan, SuperpositionChamps
from jdriftx.constraints import linearite, linearite_panache, positivite
from jdriftx._protocoles import ModeleConcentration, Relief, Vent
from jdriftx.concentrations import PanacheGaussien, SuperpositionPanaches
from jdriftx.reliefs import ReliefMntAscii, ReliefPlat, ReliefSynthetique
from jdriftx.vents import VentDeChampPlan, VentProfilPuissance, VentUniforme
from jdriftx.experiences import (
    ChampUniforme,
    ManifesteReconstruction,
    ManifesteScenario,
    Rectangle,
    ResultatDirige,
    ResultatReconstruction,
    ScenarioReconstruction,
    ScenarioUniforme,
    construire_manifeste,
    resoudre_scenario,
)
from jdriftx.metric import pseudo_distance_uniforme, temps_transport
from jdriftx.similitude import concentration_panache, concentration_puff, sigma_y, sigma_z
from jdriftx.similitude_objets import (
    ParametresPuff,
    Point3D,
    concentration_panache_au_point,
    concentration_puff_au_point,
)
from jdriftx.source import SourcePanache
from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

__version__ = "0.1.0"

__all__ = [
    "ChampFonctionCourant",
    "ChampPlan",
    "ChampUniforme",
    "ClasseStabilite",
    "FormeSigmaZ",
    "ManifesteReconstruction",
    "ManifesteScenario",
    "ModeleConcentration",
    "PanacheGaussien",
    "ParametresPuff",
    "Point3D",
    "Rectangle",
    "Relief",
    "ReliefMntAscii",
    "ReliefPlat",
    "ReliefSynthetique",
    "ResultatDirige",
    "ResultatReconstruction",
    "ScenarioReconstruction",
    "ScenarioUniforme",
    "SourcePanache",
    "SuperpositionChamps",
    "SuperpositionPanaches",
    "Vent",
    "VentDeChampPlan",
    "VentProfilPuissance",
    "VentUniforme",
    "__version__",
    "concentration_panache",
    "concentration_panache_au_point",
    "concentration_puff",
    "concentration_puff_au_point",
    "construire_manifeste",
    "linearite",
    "linearite_panache",
    "positivite",
    "pseudo_distance_uniforme",
    "resoudre_scenario",
    "sigma_y",
    "sigma_z",
    "temps_transport",
]
