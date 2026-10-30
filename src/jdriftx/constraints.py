"""Helpers de vérification pour quelques propriétés de champs de concentration.

Ce module fournit deux vérifications numériques génériques : positivité d'un
array et superposition d'un modèle évalué en un point. Il ne démontre pas que
le modèle complet respecte toutes les contraintes physiques. En particulier,
il n'implémente pas de test de divergence du champ de vent, et la conservation
de masse est testée séparément uniquement pour un panache gaussien sur une
grille finie et avec une tolérance numérique. La couverture CI est donc un
ensemble de tests ciblés, pas une preuve générale de conformité physique.
"""

from __future__ import annotations

from collections.abc import Callable
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike

from jdriftx.similitude import concentration_panache
from jdriftx.stabilite import ClasseStabilite


def _contient_valeur_non_reelle(valeur: object) -> bool:
    """Détecte booléens et complexes avant promotion numérique NumPy."""
    if isinstance(valeur, np.ndarray):
        if valeur.dtype.kind in {"b", "c"}:
            return True
        if valeur.dtype.kind != "O":
            return False
        valeurs = valeur
    else:
        valeurs = np.asarray(valeur, dtype=object)
    return any(
        isinstance(element, (bool, np.bool_, complex, np.complexfloating))
        for element in valeurs.flat
    )


def positivite(concentration: ArrayLike, tol: float = 1e-12) -> bool:
    """Verifie qu'un champ de concentration est positif (a tol pres).

    Args:
        concentration: champ de concentration a verifier.
        tol: tolerance, reel fini positif ou nul (booleen exclu).

    Returns:
        True si toutes les valeurs sont superieures ou egales a -tol.

    Raises:
        ValueError: si la tolerance n'est pas un reel fini positif ou nul.
    """
    if isinstance(tol, bool) or not isinstance(tol, Real):
        msg = "La tolerance doit etre un nombre reel (booleen exclu)."
        raise ValueError(msg)
    tolerance = float(tol)
    if not np.isfinite(tolerance) or tolerance < 0.0:
        msg = "La tolerance doit etre finie et positive ou nulle."
        raise ValueError(msg)
    if _contient_valeur_non_reelle(concentration):
        msg = (
            "La concentration doit contenir des valeurs reelles "
            "(booleens exclus; complexes exclus)."
        )
        raise ValueError(msg)
    c = np.asarray(concentration, dtype=float)
    return bool(np.all(c >= -tolerance))


def linearite(
    modele: Callable[..., np.ndarray],
    point: tuple[float, float, float],
    q1: float,
    q2: float,
    **kwargs: object,
) -> bool:
    """Verifie la superposition : modele(q1 + q2) = modele(q1) + modele(q2).

    Args:
        modele: fonction concentration(x, y, z, debit, ...) etc.
        point: triplet (x, y, z) du point d'evaluation.
        q1: premiere emission.
        q2: seconde emission.
        **kwargs: arguments supplementaires transmis tels quels au modele,
            non verifies ici ; preferer "linearite_panache" pour le panache.

    Returns:
        True si la superposition est verifiee a precision machine pres.
    """
    x, y, z = point
    c1 = modele(x, y, z, q1, **kwargs)
    c2 = modele(x, y, z, q2, **kwargs)
    c12 = modele(x, y, z, q1 + q2, **kwargs)
    return bool(np.isclose(c12, c1 + c2, rtol=1e-10, atol=1e-14))


def linearite_panache(
    point: tuple[float, float, float],
    q1: float,
    q2: float,
    *,
    u: float,
    classe: str | ClasseStabilite,
    hauteur: float = 0.0,
) -> bool:
    """Vérifie la linéarité en débit du panache gaussien en un point.

    Variante intégralement typée de "linearite" pour le cas nominal du
    panache (audit docs/25, recommandation 1, option A) : le contrat est
    explicite de bout en bout, sans kwargs non vérifiés.

    Args:
        point: triplet (x, y, z) du point d'evaluation.
        q1: première émission (kg s^-1).
        q2: seconde émission (kg s^-1).
        u: vitesse du vent (m s^-1), strictement positive.
        classe: classe de stabilite de Pasquill (lettre ou ClasseStabilite).
        hauteur: hauteur effective de la source (m).

    Returns:
        True si la superposition est verifiee a precision machine pres.
    """
    return linearite(
        concentration_panache,
        point,
        q1,
        q2,
        u=u,
        classe=classe,
        hauteur=hauteur,
    )
