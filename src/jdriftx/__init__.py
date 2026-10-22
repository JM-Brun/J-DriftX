"""J-DriftX : reprise de recherche sur la dispersion atmosphérique à complexité réduite.

Le projet étudie les formulations historiques de Drift-X (J.-M. Brun et
B. Mohammadi, 2006-2009). La primitive actuelle de temps de parcours calcule
un coût sur une polyligne fournie; elle ne reproduit pas encore la
pseudo-distance historique ni un modèle de dispersion validé.
"""

from jdriftx.constraints import linearite, positivite
from jdriftx.metric import pseudo_distance_uniforme, temps_transport
from jdriftx.similitude import concentration_panache, concentration_puff, sigma_y, sigma_z

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "concentration_panache",
    "concentration_puff",
    "linearite",
    "positivite",
    "pseudo_distance_uniforme",
    "sigma_y",
    "sigma_z",
    "temps_transport",
]
