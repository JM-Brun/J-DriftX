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

import numpy as np
from numpy.typing import ArrayLike


def positivite(concentration: ArrayLike, tol: float = 1e-12) -> bool:
    """Verifie qu'un champ de concentration est positif (a tol pres)."""
    c = np.asarray(concentration, dtype=float)
    return bool(np.all(c >= -tol))


def linearite(
    modele: Callable[..., np.ndarray],
    point: tuple[float, float, float],
    q1: float,
    q2: float,
    **kwargs: float,
) -> bool:
    """Verifie la superposition : modele(q1 + q2) = modele(q1) + modele(q2).

    Args:
        modele: fonction concentration(x, y, z, debit, ...) etc.
        point: triplet (x, y, z) du point d'evaluation.
        q1: premiere emission.
        q2: seconde emission.
        **kwargs: arguments supplementaires (u, classe, hauteur...).

    Returns:
        True si la superposition est verifiee a precision machine pres.
    """
    x, y, z = point
    c1 = modele(x, y, z, q1, **kwargs)
    c2 = modele(x, y, z, q2, **kwargs)
    c12 = modele(x, y, z, q1 + q2, **kwargs)
    return bool(np.isclose(c12, c1 + c2, rtol=1e-10, atol=1e-14))
