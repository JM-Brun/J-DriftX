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
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

CLASSES: tuple[str, ...] = tuple(classe.value for classe in ClasseStabilite)

# Logarithme du plus grand float64 : en deca, exp() reste finie ; au-dela,
# la concentration theorique n'est pas representable et le contrat le refuse.
_LOG_FLOAT_MAX = log(1.7976931348623157e308)


def _reel_fini(valeur: object, nom: str) -> float:
    """Valide un scalaire reel fini et representable en float64."""
    if isinstance(valeur, bool) or not isinstance(valeur, Real):
        raise ValueError(f"{nom} doit etre un nombre reel (booleen exclu).")
    try:
        resultat = float(valeur)
    except (OverflowError, TypeError, ValueError) as err:
        raise ValueError(f"{nom} doit etre representable en float64 fini.") from err
    if not isfinite(resultat):
        raise ValueError(f"{nom} doit etre fini.")
    return resultat


def _tableau_reel_fini(valeur: ArrayLike, nom: str) -> np.ndarray:
    """Convertit un tableau numerique reel en float64 sans coercition textuelle."""
    try:
        brut = np.asarray(valeur)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} doit etre un tableau numerique reel.") from err
    if brut.dtype.kind not in "iuf":
        raise ValueError(f"{nom} doit etre un tableau numerique reel (booleens et complexes exclus).")
    try:
        with np.errstate(over="ignore", invalid="ignore"):
            resultat = np.asarray(brut, dtype=float)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} doit etre representable en float64.") from err
    if not np.all(np.isfinite(resultat)):
        raise ValueError(f"{nom} doit contenir uniquement des valeurs finies.")
    return resultat


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
    """Evalue la loi de Briggs rurale sans debordement intermediaire."""
    a, d = classe_stable.coeff_sigma_y
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        direct = a * x_arr / np.sqrt(1.0 + d * x_arr)
        stable = a * np.sqrt(x_arr) / np.sqrt(d + 1.0 / x_arr)
        resultat = np.where(x_arr > 1.0, stable, direct)
    if np.any((x_arr > 0.0) & (resultat == 0.0)) or not np.all(np.isfinite(resultat)):
        raise FloatingPointError("sigma_y n'est pas representable en float64.")
    return resultat


def _ecart_type_vertical(x_arr: np.ndarray, classe_stable: ClasseStabilite) -> np.ndarray:
    """Evalue sigma_z en conservant les trois formes de Briggs."""
    forme, b, d = classe_stable.coeff_sigma_z
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        if forme is FormeSigmaZ.LINEAIRE:
            resultat = b * x_arr
        elif forme is FormeSigmaZ.RACINE:
            direct = b * x_arr / np.sqrt(1.0 + d * x_arr)
            stable = b * np.sqrt(x_arr) / np.sqrt(d + 1.0 / x_arr)
            resultat = np.where(x_arr > 1.0, stable, direct)
        else:
            direct = b * x_arr / (1.0 + d * x_arr)
            stable = b / (d + 1.0 / x_arr)
            resultat = np.where(x_arr > 1.0, stable, direct)
    if np.any((x_arr > 0.0) & (resultat == 0.0)) or not np.all(np.isfinite(resultat)):
        raise FloatingPointError("sigma_z n'est pas representable en float64.")
    return resultat


def _rapport_difference(a: ArrayLike, b: ArrayLike, sigma: np.ndarray) -> np.ndarray:
    """Calcule (a-b)/sigma avec un intermédiaire étendu avant conversion float64.

    La précision et la plage de `np.longdouble` dépendent de la plateforme :
    certaines plateformes l'implémentent avec la même précision que float64.
    Les cas extrêmes ne sont donc pas garantis bit-identiques entre plateformes.
    """
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        difference = np.asarray(a, dtype=np.longdouble) - np.asarray(b, dtype=np.longdouble)
        return np.asarray(difference / np.asarray(sigma, dtype=np.longdouble), dtype=float)


def _exponentielle_log(log_valeur: ArrayLike) -> np.ndarray:
    """Exponentie en domaine logarithmique sans depassement silencieux.

    Les sous-debordements sont arrondis a zero selon IEEE-754 ; un depassement
    positif est refuse explicitement.
    """
    if np.any(np.asarray(log_valeur) > _LOG_FLOAT_MAX):
        raise ValueError("La concentration theorique n'est pas representable en float64.")
    try:
        with np.errstate(over="raise", under="ignore", invalid="raise"):
            return np.asarray(np.exp(log_valeur))
    except FloatingPointError as err:
        raise ValueError("La concentration theorique n'est pas representable en float64.") from err


def sigma_y(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type horizontal du panache (m) a la distance sous le vent x (m).

    Raises:
        ValueError: si la classe ou la distance est invalide.
        FloatingPointError: si un ecart-type positif n'est pas representable en float64.
    """
    classe_stable = _valide_classe(classe)
    x_arr = _distance_sous_le_vent(_tableau_reel_fini(x, "La distance sous le vent"))
    if np.any(x_arr < 0.0):
        msg = "La distance sous le vent doit etre positive ou nulle."
        raise ValueError(msg)
    return _ecart_type_horizontal(x_arr, classe_stable)


def sigma_z(x: ArrayLike, classe: str | ClasseStabilite) -> np.ndarray:
    """Ecart-type vertical du panache (m) a la distance sous le vent x (m).

    Raises:
        ValueError: si la classe ou la distance est invalide.
        FloatingPointError: si un ecart-type positif n'est pas representable en float64.
    """
    classe_stable = _valide_classe(classe)
    x_arr = _distance_sous_le_vent(_tableau_reel_fini(x, "La distance sous le vent"))
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
    debit = _reel_fini(debit, "Le debit")
    u = _reel_fini(u, "La vitesse du vent")
    hauteur = _reel_fini(hauteur, "La hauteur de source")
    if u <= 0.0:
        raise ValueError("La vitesse du vent doit etre strictement positive.")
    if debit < 0.0:
        raise ValueError("Le debit d'emission doit etre positif ou nul.")
    x_arr = _distance_sous_le_vent(_tableau_reel_fini(x, "La distance sous le vent"))
    if np.any(x_arr <= 0.0):
        raise ValueError("La distance sous le vent doit etre strictement positive.")
    y_arr = _tableau_reel_fini(y, "La coordonnee y")
    z_arr = _tableau_reel_fini(z, "La coordonnee z")
    if debit == 0.0:
        return np.zeros(np.broadcast_shapes(x_arr.shape, y_arr.shape, z_arr.shape))

    sy = _ecart_type_horizontal(x_arr, classe_stable)
    sz = _ecart_type_vertical(x_arr, classe_stable)
    ry = _rapport_difference(y_arr, 0.0, sy)
    rz_source = _rapport_difference(z_arr, hauteur, sz)
    rz_image = _rapport_difference(z_arr, -hauteur, sz)
    with np.errstate(over="ignore", invalid="ignore"):
        exposant_lateral = -0.5 * np.square(ry)
        exposant_source = -0.5 * np.square(rz_source)
        exposant_image = -0.5 * np.square(rz_image)
        exposant_vertical = np.logaddexp(exposant_source, exposant_image)
        log_amplitude = np.log(debit) - np.log(2.0 * np.pi) - np.log(u) - np.log(sy) - np.log(sz)
        log_concentration = log_amplitude + exposant_lateral + exposant_vertical
    return _exponentielle_log(log_concentration)


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
        FloatingPointError: si un ecart-type positif n'est pas representable en float64.
    """
    classe_stable = _valide_classe(classe)
    t = _reel_fini(t, "Le temps")
    masse = _reel_fini(masse, "La masse emise")
    u = _reel_fini(u, "La vitesse du vent")
    x0 = _reel_fini(x0, "La position initiale")
    if t <= 0.0:
        raise ValueError("Le temps doit etre strictement positif.")
    if masse < 0.0:
        raise ValueError("La masse emise doit etre positive ou nulle.")
    if u <= 0.0:
        raise ValueError("La vitesse du vent doit etre strictement positive.")
    x_arr = _tableau_reel_fini(x, "La coordonnee x")
    y_arr = _tableau_reel_fini(y, "La coordonnee y")
    z_arr = _tableau_reel_fini(z, "La coordonnee z")
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
        log_normalisation = 1.5 * np.log(2.0 * np.pi)
        log_amplitude = np.log(masse) - log_normalisation - np.log(sx) - np.log(sy) - np.log(sz)
        log_concentration = log_amplitude + exposant
    return _exponentielle_log(log_concentration)
