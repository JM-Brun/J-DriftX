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

from math import isfinite, log

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

CLASSES: tuple[str, ...] = tuple(classe.value for classe in ClasseStabilite)

# Logarithme du plus grand float64 : en deca, exp() reste finie ; au-dela,
# la concentration theorique n'est pas representable et le contrat le refuse.
_LOG_FLOAT_MAX = log(1.7976931348623157e308)


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
    """Evalue la loi de Briggs rurale de sigma_y sur des distances validees.

    Les coefficients sont lus depuis l'objet ClasseStabilite, source unique de
    verite ; la classe et la distance ne sont pas revalidees ici.
    """
    a, d = classe_stable.coeff_sigma_y
    return a * x_arr / np.sqrt(1.0 + d * x_arr)


def _ecart_type_vertical(x_arr: np.ndarray, classe_stable: ClasseStabilite) -> np.ndarray:
    """Evalue la loi de Briggs rurale de sigma_z sur des distances validees.

    La forme et les coefficients sont lus depuis l'objet ClasseStabilite,
    source unique de verite ; la classe et la distance ne sont pas revalidees.
    """
    forme, b, d = classe_stable.coeff_sigma_z
    if forme is FormeSigmaZ.LINEAIRE:
        return b * x_arr
    if forme is FormeSigmaZ.RACINE:
        return b * x_arr / np.sqrt(1.0 + d * x_arr)
    return b * x_arr / (1.0 + d * x_arr)


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

    Les tableaux x, y et z sont combines selon les regles de diffusion de
    NumPy (broadcasting) ; la forme du resultat est la forme diffusee commune.
    Les exposants sont evalues par rapports normalises (coordonnee divisee
    par ecart-type) : les limites nulles restent exactes meme lorsque les
    carres debordent. Si la forme diffusee contient des valeurs non
    representables, le departage entre zero et singularite est fait en
    domaine logarithmique.

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

    Raises:
        ValueError: si la classe de stabilite est inconnue, si un parametre
            scalaire n'est pas fini, si la distance sous le vent n'est pas
            strictement positive, si y ou z contient une coordonnee non
            finie, ou si la concentration theorique n'est pas representable
            en float64 (singularite pres de la source).
    """
    classe_stable = _valide_classe(classe)
    if not all(isfinite(valeur) for valeur in (debit, u, hauteur)):
        msg = "debit, u et hauteur doivent etre finis."
        raise ValueError(msg)
    if u <= 0.0:
        msg = "La vitesse du vent doit etre strictement positive."
        raise ValueError(msg)
    if debit < 0.0:
        msg = "Le debit d'emission doit etre positif ou nul."
        raise ValueError(msg)
    x_arr = _distance_sous_le_vent(np.asarray(x, dtype=float))
    if np.any(x_arr <= 0.0):
        msg = "La distance sous le vent doit etre strictement positive."
        raise ValueError(msg)
    y_arr = np.asarray(y, dtype=float)
    z_arr = np.asarray(z, dtype=float)
    if not np.all(np.isfinite(y_arr)) or not np.all(np.isfinite(z_arr)):
        msg = "y et z doivent contenir uniquement des coordonnees finies."
        raise ValueError(msg)

    sy = _ecart_type_horizontal(x_arr, classe_stable)
    sz = _ecart_type_vertical(x_arr, classe_stable)

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        u_y = y_arr / sy
        u_z_source = (z_arr - hauteur) / sz
        u_z_image = (z_arr + hauteur) / sz
        terme_lateral = np.exp(-0.5 * u_y**2)
        terme_vertical = np.exp(-0.5 * u_z_source**2) + np.exp(-0.5 * u_z_image**2)
        concentration = debit / (2.0 * np.pi * u * sy * sz) * terme_lateral * terme_vertical
        if np.all(np.isfinite(concentration)):
            return np.asarray(concentration)
        log_exposant = -0.5 * u_y**2 + np.logaddexp(-0.5 * u_z_source**2, -0.5 * u_z_image**2)
        log_amplitude = np.log(debit) - np.log(2.0 * np.pi * u) - np.log(sy) - np.log(sz)
        # Un exposant -infini impose la limite nulle, meme si l'amplitude deborde.
        log_concentration = np.where(
            np.equal(log_exposant, -np.inf), -np.inf, log_amplitude + log_exposant
        )
        if np.any(np.isnan(log_concentration)) or np.any(log_concentration > _LOG_FLOAT_MAX):
            msg = "La concentration n'est pas representable en float64 pres de la source."
            raise ValueError(msg)
        return np.asarray(np.exp(log_concentration))


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

    Les tableaux x, y et z sont combines selon les regles de diffusion de
    NumPy (broadcasting) ; la forme du resultat est la forme diffusee commune.
    Les exposants sont evalues par rapports normalises (coordonnee divisee
    par ecart-type) : les limites nulles restent exactes meme lorsque les
    carres debordent. Si la forme diffusee contient des valeurs non
    representables, le departage entre zero et singularite est fait en
    domaine logarithmique.

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

    Raises:
        ValueError: si la classe de stabilite est inconnue, si un parametre
            scalaire n'est pas fini, si une coordonnee du point n'est pas
            finie, si la distance parcourue u*t n'est pas representable, ou
            si la concentration theorique n'est pas representable en float64
            (singularite pres de la source).
    """
    classe_stable = _valide_classe(classe)
    if not all(isfinite(valeur) for valeur in (t, masse, u, x0)):
        msg = "t, masse, u et x0 doivent etre finis."
        raise ValueError(msg)
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
    axes = (x_arr, y_arr, z_arr)
    if not all(np.all(np.isfinite(axe)) for axe in axes):
        msg = "x, y et z doivent contenir uniquement des coordonnees finies."
        raise ValueError(msg)

    distance = u * t
    if not isfinite(distance):
        msg = "La distance parcourue doit rester finie."
        raise ValueError(msg)
    if distance <= 0.0:
        msg = "La distance parcourue doit etre strictement positive."
        raise ValueError(msg)

    distance_arr = np.asarray(distance, dtype=float)
    sx = _ecart_type_horizontal(distance_arr, classe_stable)
    sy = _ecart_type_horizontal(distance_arr, classe_stable)
    sz = _ecart_type_vertical(distance_arr, classe_stable)

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        u_x = (x_arr - x0 - distance) / sx
        u_y = y_arr / sy
        u_z = z_arr / sz
        denom = (2.0 * np.pi) ** 1.5 * sx * sy * sz
        exponentiel = np.exp(-0.5 * u_x**2) * np.exp(-0.5 * u_y**2) * np.exp(-0.5 * u_z**2)
        concentration = masse / denom * exponentiel
        if np.all(np.isfinite(concentration)):
            return np.asarray(concentration)
        log_exposant = -0.5 * u_x**2 - 0.5 * u_y**2 - 0.5 * u_z**2
        log_amplitude = (
            np.log(masse) - 1.5 * np.log(2.0 * np.pi) - np.log(sx) - np.log(sy) - np.log(sz)
        )
        # Un exposant -infini impose la limite nulle, meme si l'amplitude deborde.
        log_concentration = np.where(
            np.equal(log_exposant, -np.inf), -np.inf, log_amplitude + log_exposant
        )
        if np.any(np.isnan(log_concentration)) or np.any(log_concentration > _LOG_FLOAT_MAX):
            msg = "La concentration n'est pas representable en float64 pres de la source."
            raise ValueError(msg)
        return np.asarray(np.exp(log_concentration))
