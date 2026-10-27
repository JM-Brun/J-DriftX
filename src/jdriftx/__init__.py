"""J-DriftX : reprise de recherche sur la dispersion atmosphérique à complexité réduite.

Le projet étudie les formulations historiques de Drift-X (J.-M. Brun et
B. Mohammadi, 2006-2009). La primitive actuelle de temps de parcours calcule
un coût sur une polyligne fournie; elle ne reproduit pas encore la
pseudo-distance historique ni un modèle de dispersion validé.
"""

from jdriftx.champ_analytique import ChampFonctionCourant, ChampPlan, SuperpositionChamps
from jdriftx.constraints import linearite, linearite_panache, positivite
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
    "Rectangle",
    "ResultatDirige",
    "ResultatReconstruction",
    "ScenarioReconstruction",
    "ScenarioUniforme",
    "SuperpositionChamps",
    "__version__",
    "concentration_panache",
    "concentration_puff",
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
