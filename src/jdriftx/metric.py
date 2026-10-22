"""Temps de parcours sur une polyligne : approximation géométrique provisoire.

La fonction \`temps_transport\` calcule la somme longueur / norme de vitesse sur
une polyligne fournie par l'appelant. Elle ne calcule pas la caractéristique
d'un champ de vitesse, ne projette pas le point cible sur une caractéristique
et ne reproduit donc pas la pseudo-distance historique de Mohammadi & Brun
(2006).

Comme le calcul utilise uniquement la norme de chaque vecteur vitesse, il ne
représente pas la direction du vent : inverser le signe des vecteurs vitesse
ne change pas le résultat. Le module ne doit donc pas être décrit comme une
métrique non symétrique ni comme une implémentation validée de Drift-X.

Cette fonction est conservée comme primitive géométrique simple; sa relation
avec la définition historique devra être décidée séparément avant le jalon M1.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

UMIN_PAR_DEFAUT = 0.1


def temps_transport(
    ligne: ArrayLike,
    vent: ArrayLike,
    umin: float = UMIN_PAR_DEFAUT,
) -> float:
    """Calcule un coût de parcours de polyligne en secondes.

    Args:
        ligne: points (N, 2) de la polyligne, dans l'ordre de parcours.
        vent: vecteur vitesse moyen (N-1, 2) associé à chaque segment (m s^-1).
        umin: norme minimale admissible pour chaque vecteur vitesse (m s^-1).

    Returns:
        Somme des longueurs de segments divisées par les normes de vitesse.
        Le calcul ne tient pas compte de l'orientation des vecteurs vitesse.

    Raises:
        ValueError: si les formes sont incohérentes ou si une vitesse est sous
            le seuil umin.
    """
    pts = np.asarray(ligne, dtype=float)
    u_seg = np.asarray(vent, dtype=float)

    if pts.ndim != 2 or pts.shape[1] != 2 or pts.shape[0] < 2:
        msg = "ligne doit etre un tableau (N, 2) avec N >= 2."
        raise ValueError(msg)
    if u_seg.shape != (pts.shape[0] - 1, 2):
        msg = "vent doit etre un tableau (N-1, 2) aligne sur les segments."
        raise ValueError(msg)

    segments = np.diff(pts, axis=0)
    longueurs = np.hypot(segments[:, 0], segments[:, 1])
    vitesses = np.hypot(u_seg[:, 0], u_seg[:, 1])
    if np.any(vitesses < umin):
        msg = f"Vent plus faible que umin ({umin} m/s) : temps de transport non defini."
        raise ValueError(msg)
    return float(np.sum(longueurs / vitesses))
