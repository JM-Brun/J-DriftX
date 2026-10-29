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


def sigma_y(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type horizontal du panache (m) a la distance sous le vent x (m)."""
    classe_stable = _valide_classe(classe)
    x_arr = np.asarray(x, dtype=float)
    if np.any(x_arr < 0.0):
        msg = "La distance sous le vent doit etre positive ou nulle."
        raise ValueError(msg)
    a, d = classe_stable.coeff_sigma_y
    return a * x_arr / np.sqrt(1.0 + d * x_arr)


def sigma_z(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type vertical du panache (m) a la distance sous le vent x (m)."""
    classe_stable = _valide_classe(classe)
    x_arr = np.asarray(x, dtype=float)
    if np.any(x_arr < 0.0):
        msg = "La distance sous le vent doit etre positive ou nulle."
        raise ValueError(msg)
    forme, b, d = classe_stable.coeff_sigma_z
    if forme is FormeSigmaZ.LINEAIRE:
        return b * x_arr
    if forme is FormeSigmaZ.RACINE:
        return b * x_arr / np.sqrt(1.0 + d * x_arr)
    return b * x_arr / (1.0 + d * x_arr)


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

    Args:
        x: distance sous le vent (m), strictement positive.
        y: coordonnee laterale (m).
        z: altitude du point de calcul (m).
        debit: emission massique (kg s^-1).
        u: vitesse du vent (m s^-1), strictement positive.
        classe: classe de stabilite de Pasquill (A a F), lettre ou ClasseStabilite.
        hauteur: hauteur effective de la source (m).

    Returns:
        Concentration au point demande (reflection au sol incluse).
    """
    if u <= 0.0:
        msg = "La vitesse du vent doit etre strictement positive."
        raise ValueError(msg)
    if debit < 0.0:
        msg = "Le debit d'emission doit etre positif ou nul."
        raise ValueError(msg)
    x_arr = np.asarray(x, dtype=float)
    if np.any(x_arr <= 0.0):
        msg = "La distance sous le vent doit etre strictement positive."
        raise ValueError(msg)
    y_arr = np.asarray(y, dtype=float)
    z_arr = np.asarray(z, dtype=float)

    sy = sigma_y(x_arr, classe)
    sz = sigma_z(x_arr, classe)

    terme_lateral = np.exp(-(y_arr**2) / (2.0 * sy**2))
    terme_vertical = np.exp(-((z_arr - hauteur) ** 2) / (2.0 * sz**2)) + np.exp(
        -((z_arr + hauteur) ** 2) / (2.0 * sz**2)
    )
    return np.asarray(debit / (2.0 * np.pi * u * sy * sz) * terme_lateral * terme_vertical)


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
    """Concentration (kg m^-3) d'un puff gaussien au point (x, y, z) et a l'instant t.

    Args:
        x: coordonnee sous le vent du point (m).
        y: coordonnee laterale (m).
        z: altitude (m).
        t: temps ecoule depuis l'emission (s), strictement positif.
        masse: masse emise (kg).
        u: vitesse du vent (m s^-1), strictement positive.
        classe: classe de stabilite de Pasquill (A a F), lettre ou ClasseStabilite.
        x0: position sous le vent de l'emission (m).

    Returns:
        Concentration du puff, avec isotropie longitudinale approchee
        (sigma_x de l'ordre de sigma_y a distance egale du parcours).
    """
    if t <= 0.0:
        msg = "Le temps doit etre strictement positif."
        raise ValueError(msg)
    if masse < 0.0:
        msg = "La masse emise doit etre positive ou nulle."
        raise ValueError(msg)
    if u <= 0.0:
        msg = "La vitesse du vent doit etre strictement positive."
        raise ValueError(msg)

    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    z_arr = np.asarray(z, dtype=float)

    distance = u * t
    if distance <= 0.0:
        msg = "La distance parcourue doit etre strictement positive."
        raise ValueError(msg)

    sx = sigma_y(distance, classe)
    sy = sigma_y(distance, classe)
    sz = sigma_z(distance, classe)

    denom = (2.0 * np.pi) ** 1.5 * sx * sy * sz
    exponentiel = (
        np.exp(-((x_arr - x0 - distance) ** 2) / (2.0 * sx**2))
        * np.exp(-(y_arr**2) / (2.0 * sy**2))
        * np.exp(-(z_arr**2) / (2.0 * sz**2))
    )
    return np.asarray(masse / denom * exponentiel)
