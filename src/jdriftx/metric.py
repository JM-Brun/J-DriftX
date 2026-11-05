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

from decimal import Decimal, localcontext
from fractions import Fraction
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike

UMIN_PAR_DEFAUT = 0.1


def _contient_booleen(valeur: object) -> bool:
    """Détecte les booléens avant toute conversion numérique avec NumPy."""
    if isinstance(valeur, np.ndarray):
        if valeur.dtype.kind == "b":
            return True
        return valeur.dtype.kind == "O" and any(
            isinstance(element, (bool, np.bool_)) for element in valeur.flat
        )
    brut = np.asarray(valeur, dtype=object)
    return any(isinstance(element, (bool, np.bool_)) for element in brut.flat)


def _temps_float64(valeur: np.longdouble, contexte: str) -> float:
    """Convertit un temps positif en float64 sans overflow ni underflow silencieux."""
    if not np.isfinite(valeur) or valeur > np.finfo(float).max:
        raise ValueError(f"{contexte} n'est pas representable en float64.")
    resultat = float(valeur)
    if valeur > 0.0 and resultat == 0.0:
        raise ValueError(f"{contexte} n'est pas representable en float64.")
    return resultat


def _temps_precision(valeur: Decimal | Fraction, contexte: str) -> float:
    """Convertit un résultat positif de précision étendue sans perte de domaine."""
    try:
        resultat = float(valeur)
    except OverflowError as exc:
        raise ValueError(f"{contexte} n'est pas representable en float64.") from exc
    if not isfinite(resultat) or (valeur > 0 and resultat == 0.0):
        raise ValueError(f"{contexte} n'est pas representable en float64.")
    return resultat


def _projection_precision(deplacement: np.ndarray, vitesse: np.ndarray) -> float:
    """Calcule exactement la projection des entrées float64 lorsque nécessaire."""
    d = [Fraction.from_float(float(x)) for x in deplacement]
    u = [Fraction.from_float(float(x)) for x in vitesse]
    norme_carre = sum(x * x for x in u)
    if norme_carre == 0:
        raise ValueError("Le champ uniforme doit avoir une vitesse non nulle.")
    avance = sum(x * y for x, y in zip(d, u, strict=True))
    if avance < 0:
        return float("inf")
    return _temps_precision(avance / norme_carre, "Le cout longitudinal")


def _transport_precision(segments: np.ndarray, vent: np.ndarray, umin: float) -> float:
    """Évalue les normes extrêmes en décimal, puis arrondit la somme en float64."""
    with localcontext() as contexte:
        contexte.prec = 80
        cout_total = Decimal(0)
        seuil = Decimal.from_float(float(umin))
        for segment, vitesse in zip(segments, vent, strict=True):
            dx, dy = (Decimal.from_float(float(x)) for x in segment)
            ux, uy = (Decimal.from_float(float(x)) for x in vitesse)
            longueur = (dx * dx + dy * dy).sqrt()
            norme = (ux * ux + uy * uy).sqrt()
            if norme < seuil:
                msg = f"Vent plus faible que umin ({umin} m/s) : temps de transport non defini."
                raise ValueError(msg)
            cout_total += longueur / norme
        return _temps_precision(cout_total, "Le cout total")


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
        ValueError: si une entrée est non finie ou si le temps positif
            n'est pas representable en float64.
    """
    if any(isinstance(value, (bool, np.bool_)) for value in (a, b, vitesse)):
        msg = "a, b et vitesse doivent etre reels (booleens exclus)."
        raise ValueError(msg)
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
    with np.errstate(over="ignore", under="ignore"):
        temps = abs(np.longdouble(deplacement) / np.longdouble(vitesse))
    if temps == 0.0:
        raise ValueError("Le temps de premiere arrivee n'est pas representable en float64.")
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
            float64 ou s'arrondit a zero.
    """
    if _contient_booleen(ligne) or _contient_booleen(vent):
        msg = "ligne et vent doivent contenir des valeurs reelles (booleens exclus)."
        raise ValueError(msg)
    if isinstance(umin, (bool, np.bool_)):
        msg = "umin doit etre reel (booleens exclus)."
        raise ValueError(msg)
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
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        longueurs = np.hypot(segments_etendus[:, 0], segments_etendus[:, 1])
        vitesses = np.hypot(vent_etendu[:, 0], vent_etendu[:, 1])
        couts = longueurs / vitesses
        cout_total = np.sum(couts, dtype=np.longdouble)
    # Selon la plateforme, longdouble n'a pas toujours une plage plus large.
    # Recalculer aussi les coûts sous-normaux avant leur somme : plusieurs
    # contributions arrondies à zéro peuvent former un résultat représentable.
    if (
        not np.all(np.isfinite(longueurs))
        or not np.all(np.isfinite(vitesses))
        or not np.isfinite(cout_total)
        or np.any((longueurs > 0) & (couts < np.finfo(np.longdouble).tiny))
    ):
        return _transport_precision(segments, u_seg, umin)
    if np.any(vitesses < np.longdouble(umin)):
        msg = f"Vent plus faible que umin ({umin} m/s) : temps de transport non defini."
        raise ValueError(msg)
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
    if any(_contient_booleen(valeur) for valeur in (a, b, vent)):
        msg = "a, b et vent doivent contenir des valeurs reelles (booleens exclus)."
        raise ValueError(msg)
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

    if not np.any(vitesse):
        raise ValueError("Le champ uniforme doit avoir une vitesse non nulle.")
    deplacement_etendu = np.asarray(deplacement, dtype=np.longdouble)
    vitesse_etendue = np.asarray(vitesse, dtype=np.longdouble)
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        produits = deplacement_etendu * vitesse_etendue
        carres = vitesse_etendue * vitesse_etendue
        avance = np.sum(produits, dtype=np.longdouble)
        norme_carre = np.sum(carres, dtype=np.longdouble)
        cout = avance / norme_carre
    # Les produits extrêmes et les annulations peuvent perdre leur signe ou
    # leur amplitude ; les fractions exploitent exactement les entrées float64.
    petit = np.finfo(np.longdouble).tiny
    if (
        not np.isfinite(avance)
        or not np.isfinite(norme_carre)
        or norme_carre == 0.0
        or np.any((vitesse_etendue != 0) & (carres < petit))
        or np.any((deplacement_etendu != 0) & (vitesse_etendue != 0) & (np.abs(produits) < petit))
        or (np.any(produits > 0) and np.any(produits < 0))
        or (avance > 0 and (not np.isfinite(cout) or cout == 0.0))
    ):
        return _projection_precision(deplacement, vitesse)
    if avance < 0.0:
        return float("inf")
    if avance == 0.0:
        return 0.0
    return _temps_float64(cout, "Le cout longitudinal")
