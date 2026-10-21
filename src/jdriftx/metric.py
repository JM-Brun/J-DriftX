"""Metrique non symetrique basee sur les temps de transport.

La coordonnee naturelle du modele J-DriftX n'est pas la distance euclidienne
mais le temps de transport : l'integrale de ds / |u(s)| le long de la ligne
de courant entre la source et le point considere. Cette metrique est non
symetrique : aller de A vers B avec le vent ne coute pas le meme temps que
venir de B vers A des que le champ de vent n'est pas uniforme. Les solutions
de similitude classiques, connues en metrique cartesienne, y sont ensuite
generalisees (Mohammadi & Brun, C. R. Mecanique 334, 2006).

Ce module fournit l'evaluation de la metrique ; la transformation complete
des solutions de similitude dans cette metrique est livree au jalon M1.
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
    """Temps de transport (s) le long d'une polyligne dans un champ de vent.

    Args:
        ligne: points (N, 2) de la polyligne, depuis la source.
        vent: vitesse moyenne du vent (N-1, 2) sur chaque segment (m s^-1).
        umin: vitesse minimale admissible avant declenchement d'une erreur
            (conditions de vent faible : la metrique diverge).

    Returns:
        tau = somme_i |L_i| / |u_i|, ou L_i est le i-eme segment.

    Raises:
        ValueError: formes incoherentes, ligne trop courte ou vent sous umin.
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
