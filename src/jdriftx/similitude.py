"""Solutions de similitude gaussiennes : panache et puff.

Ce module implemente les solutions classiques de similitude (metrique
cartesienne, vent uniforme) qui forment l'espace de recherche du modele
J-DriftX. Les ecarts-types de dispersion suivent les formules de Briggs
(site rural), indicices par classe de stabilite de Pasquill ; les classes,
leurs caracteristiques et leurs coefficients sont definis comme objets dans
`jdriftx.stabilite`, source unique de verite.

References : chapitre "Reduced-Order Modelling of Dispersion" (Brun &
Mohammadi, 2008) ; formules de Briggs reprises par Martin (1976).
"""

from __future__ import annotations

from math import isfinite

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

CLASSES: tuple[str, ...] = tuple(classe.value for classe in ClasseStabilite)


def _valide_classe(classe: str | ClasseStabilite) -> ClasseStabilite:
    """Retourne la classe de stabilite correspondante ou leve une ValueError."""
    try:
        return ClasseStabilite(classe)
    except ValueError as err:
        msg = f"Classe de stabilite inconnue : {classe!r} (attendu : {CLASSES})"
        raise ValueError(msg) from err


def _distance_sous_le_vent(x_arr: np.ndarray) -> np.ndarray:
    """Verifie que la distance sous le vent ne contient que des valeurs finies."""
    if not np.all(np.isfinite(x_arr)):
        msg = "La distance sous le vent doit etre finie."
        raise ValueError(msg)
    return x_arr


def _ecart_type_horizontal(x_arr: np.ndarray, classe_stable: ClasseStabilite) -> np.ndarray:
    """Evalue sigma_y sans debordement intermediaire de d*x.

    Pour x > 0, a*x/sqrt(1+d*x) est reecrit
    a*sqrt(x)/sqrt(d+1/x). La loi de Briggs reste inchangee.
    """
    a, d = classe_stable.coeff_sigma_y
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        resultat = a * np.sqrt(x_arr) / np.sqrt(d + 1.0 / x_arr)
    if np.any((x_arr > 0.0) & (resultat == 0.0)):
        raise FloatingPointError("sigma_y n'est pas representable en float64.")
    if not np.all(np.isfinite(resultat)):
        raise FloatingPointError("sigma_y n'est pas representable en float64.")
    return resultat


def _ecart_type_vertical(x_arr: np.ndarray, classe_stable: ClasseStabilite) -> np.ndarray:
    """Evalue sigma_z en limitant les debordements intermediaires."""
    forme, b, d = classe_stable.coeff_sigma_z
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        if forme is FormeSigmaZ.LINEAIRE:
            resultat = b * x_arr
        elif forme is FormeSigmaZ.RACINE:
            resultat = b * np.sqrt(x_arr) / np.sqrt(d + 1.0 / x_arr)
        else:
            # b*x/(1+d*x) = b/(d + 1/x), forme stable pour x > 0.
            resultat = b / (d + 1.0 / x_arr)
    if np.any((x_arr > 0.0) & (resultat == 0.0)):
        raise FloatingPointError("sigma_z n'est pas representable en float64.")
    if not np.all(np.isfinite(resultat)):
        raise FloatingPointError("sigma_z n'est pas representable en float64.")
    return resultat


def _rapport_difference(a: ArrayLike, b: ArrayLike, sigma: np.ndarray) -> np.ndarray:
    """Calcule (a-b)/sigma avec une soustraction et une division elargies."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        difference = np.asarray(a, dtype=np.longdouble) - np.asarray(b, dtype=np.longdouble)
        rapport = difference / np.asarray(sigma, dtype=np.longdouble)
        return np.asarray(rapport, dtype=float)


def _exponentielle_log(log_valeur: ArrayLike) -> np.ndarray:
    """Exponentie un logarithme, en refusant tout depassement de float64.

    Le sous-debordement est arrondi a zero selon les regles IEEE-754 ; c'est
    le comportement numerique attendu pour les queues gaussiennes non resolues.
    """
    limite = np.log(np.finfo(float).max)
    if np.any(log_valeur > limite):
        raise FloatingPointError("La concentration depasse la plage representable en float64.")
    with np.errstate(over="raise", under="ignore", invalid="raise"):
        return np.asarray(np.exp(log_valeur))

def sigma_y(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type horizontal du panache (m) a la distance sous le vent x (m)."""
    classe_stable = _valide_classe(classe)
    x_arr = _distance_sous_le_vent(np.asarray(x, dtype=float))
    if np.any(x_arr < 0.0):
        msg = "La distance sous le vent doit etre positive ou nulle."
        raise ValueError(msg)
    return _ecart_type_horizontal(x_arr, classe_stable)


def sigma_z(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type vertical du panache (m) a la distance sous le vent x (m)."""
    classe_stable = _valide_classe(classe)
    x_arr = _distance_sous_le_vent(np.asarray(x, dtype=float))
    if np.any(x_arr < 0.0):
        msg = "La distance sous le vent doit etre positive ou nulle."
        raise ValueError(msg)
    return _ecart_type_vertical(x_arr, classe_stable)


def concentration_panache(
    x: ArrayLike,
    y: ArrayLike,
    z: ArrayLike,
    debit: float,
    u: float,
    classe: str | ClasseStabilite,
    hauteur: float = 0.0,
) -> np.ndarray:
    """Concentration (kg m^-3) du panache gaussien au point (x, y, z).

    Les tableaux sont combines selon les regles de diffusion NumPy. Les
    equations gaussiennes et la reflexion au sol sont conservees ; leur
    evaluation utilise des rapports normalises et un pre-facteur logarithmique.

    Raises:
        ValueError: pour les entrees invalides.
        FloatingPointError: si un ecart-type ou la concentration depasse la
            plage representable en float64.
    """
    classe_stable = _valide_classe(classe)
    if not all(isfinite(valeur) for valeur in (debit, u, hauteur)):
        raise ValueError("debit, u et hauteur doivent etre finis.")
    if u <= 0.0:
        raise ValueError("La vitesse du vent doit etre strictement positive.")
    if debit < 0.0:
        raise ValueError("Le debit d'emission doit etre positif ou nul.")
    x_arr = _distance_sous_le_vent(np.asarray(x, dtype=float))
    if np.any(x_arr <= 0.0):
        raise ValueError("La distance sous le vent doit etre strictement positive.")
    y_arr, z_arr = np.asarray(y, dtype=float), np.asarray(z, dtype=float)
    if not np.all(np.isfinite(y_arr)) or not np.all(np.isfinite(z_arr)):
        raise ValueError("y et z doivent contenir uniquement des coordonnees finies.")
    if debit == 0.0:
        return np.zeros(np.broadcast_shapes(x_arr.shape, y_arr.shape, z_arr.shape))

    sy = _ecart_type_horizontal(x_arr, classe_stable)
    sz = _ecart_type_vertical(x_arr, classe_stable)
    ry = _rapport_difference(y_arr, 0.0, sy)
    rz_haut = _rapport_difference(z_arr, hauteur, sz)
    rz_bas = _rapport_difference(z_arr, -hauteur, sz)
    with np.errstate(over="ignore", invalid="ignore"):
        exposant_lateral = -0.5 * np.square(ry)
        exposant_haut = -0.5 * np.square(rz_haut)
        exposant_bas = -0.5 * np.square(rz_bas)
        exposant_vertical = np.logaddexp(exposant_haut, exposant_bas)
        log_prefacteur = (
            np.log(debit) - np.log(2.0 * np.pi) - np.log(u) - np.log(sy) - np.log(sz)
        )
        log_concentration = log_prefacteur + exposant_lateral + exposant_vertical
    return np.asarray(_exponentielle_log(log_concentration))


def concentration_puff(
    x: ArrayLike,
    y: ArrayLike,
    z: ArrayLike,
    t: float,
    masse: float,
    u: float,
    classe: str | ClasseStabilite,
    x0: float = 0.0,
) -> np.ndarray:
    """Concentration (kg m^-3) du puff gaussien au point (x, y, z).

    L'equation gaussienne tridimensionnelle et l'approximation sigma_x=sigma_y
    sont conservees. Les ecarts sont normalises avant elevation au carre.

    Raises:
        ValueError: pour les entrees invalides ou une distance u*t non finie.
        FloatingPointError: si un ecart-type ou la concentration depasse la
            plage representable en float64.
    """
    classe_stable = _valide_classe(classe)
    if not all(isfinite(valeur) for valeur in (t, masse, u, x0)):
        raise ValueError("t, masse, u et x0 doivent etre finis.")
    if t <= 0.0:
        raise ValueError("Le temps doit etre strictement positif.")
    if masse < 0.0:
        raise ValueError("La masse emise doit etre positive ou nulle.")
    if u <= 0.0:
        raise ValueError("La vitesse du vent doit etre strictement positive.")
    x_arr, y_arr, z_arr = (np.asarray(v, dtype=float) for v in (x, y, z))
    if not all(np.all(np.isfinite(axe)) for axe in (x_arr, y_arr, z_arr)):
        raise ValueError("x, y et z doivent contenir uniquement des coordonnees finies.")
    distance = u * t
    if not isfinite(distance) or distance <= 0.0:
        raise ValueError("La distance parcourue doit rester finie et strictement positive.")
    if masse == 0.0:
        return np.zeros(np.broadcast_shapes(x_arr.shape, y_arr.shape, z_arr.shape))

    distance_arr = np.asarray(distance, dtype=float)
    sx = _ecart_type_horizontal(distance_arr, classe_stable)
    sy = sx
    sz = _ecart_type_vertical(distance_arr, classe_stable)
    centre_x = np.asarray(x0, dtype=np.longdouble) + np.longdouble(distance)
    rx = _rapport_difference(x_arr, centre_x, sx)
    ry = _rapport_difference(y_arr, 0.0, sy)
    rz = _rapport_difference(z_arr, 0.0, sz)
    with np.errstate(over="ignore", invalid="ignore"):
        exposant = -0.5 * (np.square(rx) + np.square(ry) + np.square(rz))
        log_prefacteur = (
            np.log(masse)
            - 1.5 * np.log(2.0 * np.pi)
            - np.log(sx)
            - np.log(sy)
            - np.log(sz)
        )
        log_concentration = log_prefacteur + exposant
    return np.asarray(_exponentielle_log(log_concentration))
