"""Tests de la condition de réflexion au sol pour les puffs gaussiens."""

import numpy as np
import pytest

from jdriftx.similitude import concentration_puff, sigma_y, sigma_z


def test_puff_sans_reflexion_preserve_le_comportement_historique() -> None:
    """Le défaut reste le puff en espace libre, sans source image."""
    args = (1000.0, 0.0, 0.0)
    kwargs = {"t": 300.0, "masse": 2.0, "u": 3.0, "classe": "D"}
    historique = concentration_puff(*args, **kwargs)
    explicite = concentration_puff(*args, **kwargs, reflexion_sol=False)
    assert explicite == historique


def test_puff_reflechi_double_la_concentration_au_sol_pour_une_source_au_sol() -> None:
    """Pour h=0, les deux images coïncident et doublent la valeur à z=0."""
    args = (1000.0, 0.0, 0.0)
    kwargs = {"t": 300.0, "masse": 2.0, "u": 3.0, "classe": "D"}
    libre = concentration_puff(*args, **kwargs)
    reflechi = concentration_puff(*args, **kwargs, reflexion_sol=True)
    assert reflechi == pytest.approx(2.0 * libre, rel=1e-14)


def test_puff_reflechi_est_symetrique_par_rapport_au_sol() -> None:
    """La source image impose une dérivée verticale nulle à z=0."""
    z = np.array([-20.0, -5.0, 0.0, 5.0, 20.0])
    valeurs = concentration_puff(
        1000.0,
        0.0,
        z,
        t=300.0,
        masse=2.0,
        u=3.0,
        classe="D",
        hauteur=15.0,
        reflexion_sol=True,
    )
    np.testing.assert_allclose(valeurs, valeurs[::-1], rtol=1e-14, atol=0.0)


@pytest.mark.parametrize("hauteur", [0.0, 20.0])
def test_puff_reflechi_conserve_la_masse_sur_le_demi_espace(hauteur: float) -> None:
    """L'intégrale sur z>=0 restitue la masse, à l'erreur de troncature près."""
    masse, u, t, classe = 2.0, 3.0, 300.0, "D"
    distance = u * t
    sx = float(sigma_y(distance, classe))
    sy = sx
    sz = float(sigma_z(distance, classe))
    centre_x = distance

    x = np.linspace(centre_x - 4.0 * sx, centre_x + 4.0 * sx, 81)
    y = np.linspace(-4.0 * sy, 4.0 * sy, 81)
    z = np.linspace(0.0, hauteur + 4.0 * sz, 81)
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")

    concentration = concentration_puff(
        xx,
        yy,
        zz,
        t=t,
        masse=masse,
        u=u,
        classe=classe,
        hauteur=hauteur,
        reflexion_sol=True,
    )
    integral_z = np.trapezoid(concentration, z, axis=2)
    integral_y = np.trapezoid(integral_z, y, axis=1)
    integral = np.trapezoid(integral_y, x)
    assert integral == pytest.approx(masse, rel=2e-4)


@pytest.mark.parametrize("valeur", [0, 1, "yes", None])
def test_reflexion_sol_exige_un_booleen(valeur: object) -> None:
    """Le paramètre de condition limite est explicitement typé."""
    with pytest.raises(ValueError, match="booleen"):
        concentration_puff(
            1000.0,
            0.0,
            0.0,
            t=300.0,
            masse=2.0,
            u=3.0,
            classe="D",
            reflexion_sol=valeur,  # type: ignore[arg-type]
        )
