"""Regressions de la validation stricte des entrees des fonctions de similitude."""

from collections.abc import Callable

import numpy as np
import pytest

from jdriftx.similitude import concentration_panache, concentration_puff, sigma_y, sigma_z


@pytest.mark.parametrize("fonction", [sigma_y, sigma_z])
@pytest.mark.parametrize("valeur", [[1.0, True], [False, 2.0], [[1.0, 2.0], [3.0, True]]])
def test_sigmas_rejettent_les_booleens_meles_aux_reels(
    fonction: Callable[..., np.ndarray], valeur: object
) -> None:
    """Un booleen mele n'est pas promu silencieusement en entier par NumPy."""
    # Given — une distance melant reels et booleens.
    # When / Then — l'appel est refuse avant toute promotion de type.
    with pytest.raises(ValueError, match="booleens exclus"):
        fonction(valeur, "D")


@pytest.mark.parametrize(
    ("fonction", "parametres"),
    [
        (
            concentration_panache,
            {"debit": 1.0, "u": 3.0, "classe": "D"},
        ),
        (
            concentration_puff,
            {"t": 300.0, "masse": 5.0, "u": 3.0, "classe": "D"},
        ),
    ],
)
@pytest.mark.parametrize("axe", ["x", "y", "z"])
def test_concentrations_rejettent_les_booleens_meles_aux_reels(
    fonction: Callable[..., np.ndarray], parametres: dict[str, object], axe: str
) -> None:
    """Les coordonnees preservent l'exclusion stricte des booleens avant promotion."""
    # Given — une coordonnee melant un reel et un booleen.
    coordonnees = {"x": 500.0, "y": 0.0, "z": 1.0}
    coordonnees[axe] = [1.0, True]
    # When / Then — l'appel est refuse avant toute promotion de type.
    with pytest.raises(ValueError, match="booleens exclus"):
        fonction(**coordonnees, **parametres)


def test_tableau_numpy_de_type_booleen_reste_refuse() -> None:
    """Un tableau NumPy homogene de booleens reste refuse."""
    # Given — un tableau de booleens homogenes.
    # When / Then — l'appel est refuse par le controle de dtype.
    with pytest.raises(ValueError, match="booleens"):
        sigma_y(np.array([True, False]), "D")
