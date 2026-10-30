"""Temps de parcours sur une polyligne : approximation géométrique provisoire.

La fonction temps_transport calcule la somme longueur / norme de vitesse sur
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

from math import isfinite

import numpy as np
from numpy.typing import ArrayLike

UMIN_PAR_DEFAUT = 0.1


def _temps_float64(valeur: np.longdouble, contexte: str) -> float:
    """Convertit un temps positif en float64 sans overflow ni underflow silencieux."""
    if not np.isfinite(valeur) or valeur > np.finfo(float).max:
        raise ValueError(f"{contexte} n'est pas representable en float64.")
    resultat = float(valeur)
    if valeur > 0.0 and resultat == 0.0:
        raise ValueError(f"{contexte} n'est pas representable en float64.")
    return resultat


def temps_premiere_arrivee_1d(a: float, b: float, vitesse: float) -> float:
    """Calcule le temps de première arrivée pour une vitesse constante en 1D.

    Le modèle est l'EDO stationnaire dx/dt = vitesse sur la droite réelle.
    Une cible inaccessible reçoit +inf ; si vitesse vaut zéro, seule la
    source elle-même est atteinte, au temps zéro.

    Args:
        a: position initiale (m).
        b: position cible (m).
        vitesse: vitesse signée constante (m s^-1).

    Returns:
        Temps de première arrivée en secondes, ou +inf si la cible est
        inaccessible sous la dynamique constante spécifiée.

    Raises:
        ValueError: si une entrée est non finie.
    """
    if not all(isfinite(value) for value in (a, b, vitesse)):
        msg = "a, b et vitesse doivent etre finis."
        raise ValueError(msg)

    deplacement = b - a
    if not isfinite(deplacement):
        msg = "Le deplacement b - a doit etre fini."
        raise ValueError(msg)
    if deplacement == 0.0:
        return 0.0
    if vitesse == 0.0 or ((deplacement > 0.0) != (vitesse > 0.0)):
        return float("inf")
    temps = abs(np.longdouble(deplacement) / np.longdouble(vitesse))
    return _temps_float64(temps, "Le temps de premiere arrivee")


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
        ValueError: si les formes sont incohérentes, si une vitesse est sous
            le seuil umin, ou si le coût total n'est pas représentable en
            float64.
    """
    pts = np.asarray(ligne, dtype=float)
    u_seg = np.asarray(vent, dtype=float)

    if pts.ndim != 2 or pts.shape[1] != 2 or pts.shape[0] < 2:
        msg = "ligne doit etre un tableau (N, 2) avec N >= 2."
        raise ValueError(msg)
    if u_seg.shape != (pts.shape[0] - 1, 2):
        msg = "vent doit etre un tableau (N-1, 2) aligne sur les segments."
        raise ValueError(msg)
    if not np.isfinite(umin) or umin <= 0.0:
        msg = "umin doit etre fini et strictement positif."
        raise ValueError(msg)
    if not np.all(np.isfinite(pts)):
        msg = "ligne doit contenir uniquement des coordonnees finies."
        raise ValueError(msg)
    if not np.all(np.isfinite(u_seg)):
        msg = "vent doit contenir uniquement des vitesses finies."
        raise ValueError(msg)

    # Finite endpoints can still overflow when subtracted (e.g. -1e308 to 1e308).
    # Reject an unrepresentable segment rather than returning an infinite cost.
    with np.errstate(over="ignore", invalid="ignore"):
        segments = np.diff(pts, axis=0)
    if not np.all(np.isfinite(segments)):
        msg = "Les deplacements des segments doivent rester finis."
        raise ValueError(msg)

    segments_etendus = np.asarray(segments, dtype=np.longdouble)
    vent_etendu = np.asarray(u_seg, dtype=np.longdouble)
    longueurs = np.hypot(segments_etendus[:, 0], segments_etendus[:, 1])
    vitesses = np.hypot(vent_etendu[:, 0], vent_etendu[:, 1])
    if np.any(vitesses < np.longdouble(umin)):
        msg = f"Vent plus faible que umin ({umin} m/s) : temps de transport non defini."
        raise ValueError(msg)
    couts = longueurs / vitesses
    cout_total = np.sum(couts, dtype=np.longdouble)
    return _temps_float64(cout_total, "Le cout total")


def pseudo_distance_uniforme(
    a: ArrayLike,
    b: ArrayLike,
    vent: ArrayLike,
) -> float:
    """Évalue la pseudo-distance de référence définie ici pour un champ uniforme 2D.

    Le champ est constant et non nul. Le coût est le temps longitudinal entre
    les projections de a et b sur une ligne de courant parallèle au vent.
    L'écart transversal n'est pas pénalisé. La convention +inf pour les points
    en amont est une convention locale explicite ; elle ne permet pas, à elle
    seule, d'établir le traitement des points inaccessibles dans la formulation
    historique.

    Cette fonction est une référence analytique limitée au champ uniforme,
    pas une implémentation générale des caractéristiques d'un champ variable.

    Args:
        a: point de départ (x, y).
        b: point cible (x, y).
        vent: vecteur vitesse constant (ux, uy), non nul.

    Returns:
        Temps longitudinal (dans les unités cohérentes des entrées), ou inf si b est
        en amont de a selon la convention explicite de cette fonction.

    Raises:
        ValueError: si un point ou le vecteur vitesse n'a pas la forme (2,),
            si la vitesse est nulle, ou si le déplacement ou le coût déborde
            du format flottant.
    """
    point_a = np.asarray(a, dtype=float)
    point_b = np.asarray(b, dtype=float)
    vitesse = np.asarray(vent, dtype=float)

    if point_a.shape != (2,) or point_b.shape != (2,) or vitesse.shape != (2,):
        msg = "a, b et vent doivent etre des vecteurs de forme (2,)."
        raise ValueError(msg)
    if not np.all(np.isfinite(point_a)) or not np.all(np.isfinite(point_b)):
        msg = "a et b doivent contenir uniquement des coordonnees finies."
        raise ValueError(msg)
    if not np.all(np.isfinite(vitesse)):
        msg = "vent doit contenir uniquement des vitesses finies."
        raise ValueError(msg)

    with np.errstate(over="ignore", invalid="ignore"):
        deplacement = point_b - point_a
    if not np.all(np.isfinite(deplacement)):
        msg = "Le deplacement b - a doit rester fini."
        raise ValueError(msg)

    # Le quotient (d . u) / (u . u) peut rester representable alors que
    # chacun des produits scalaires deborde en float64. L'intermediaire etendu
    # preserve ce rapport sans changer la formule analytique.
    deplacement_etendu = np.asarray(deplacement, dtype=np.longdouble)
    vitesse_etendue = np.asarray(vitesse, dtype=np.longdouble)
    avance = np.sum(deplacement_etendu * vitesse_etendue, dtype=np.longdouble)
    norme_carre = np.sum(vitesse_etendue * vitesse_etendue, dtype=np.longdouble)
    if norme_carre == 0.0:
        msg = "Le champ uniforme doit avoir une vitesse non nulle."
        raise ValueError(msg)
    if avance < 0.0:
        return float("inf")
    if avance == 0.0:
        return 0.0
    cout = avance / norme_carre
    return _temps_float64(cout, "Le cout longitudinal")
