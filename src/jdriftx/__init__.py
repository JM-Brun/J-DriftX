"""J-DriftX : dispersion atmospherique a complexite reduite.

Reprise open-source du projet Drift-X (J.-M. Brun et B. Mohammadi,
2006-2009) : solutions de similitude generalisees dans une metrique non
symetrique basee sur les temps de transport, sans resolution d'EDP ni
maillage, calibrees par assimilation de donnees partielles.
"""

from jdriftx.constraints import linearite, positivite
from jdriftx.metric import temps_transport
from jdriftx.similitude import concentration_panache, concentration_puff, sigma_y, sigma_z

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "concentration_panache",
    "concentration_puff",
    "linearite",
    "positivite",
    "sigma_y",
    "sigma_z",
    "temps_transport",
]
