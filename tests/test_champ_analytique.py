"""Tests du champ plan incompressible à fonction de courant (phase 2, Fig. 1)."""

import math
from dataclasses import FrozenInstanceError

import pytest

from jdriftx.champ_analytique import ChampFonctionCourant
from jdriftx.trajectories import integrate_trajectory

CHAMP = ChampFonctionCourant(amplitude=1.0, longueur=1.0)


def _vitesse_stationnaire(_temps: float, x: float, y: float) -> tuple[float, float]:
    return CHAMP.vitesse(x, y)


def test_amplitude_nulle_est_rejetee() -> None:
    """L'invariant « amplitude non nulle » est vérifié à la construction."""
    # Given — une amplitude rigoureusement nulle.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="non nulle"):
        ChampFonctionCourant(amplitude=0.0, longueur=1.0)


def test_longueur_non_positive_est_rejetee() -> None:
    """L'invariant « longueur strictement positive » est vérifié à la construction."""
    # Given — une longueur d'onde nulle.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="strictement positive"):
        ChampFonctionCourant(amplitude=1.0, longueur=0.0)


def test_les_vitesses_sont_les_derivees_de_la_fonction_de_courant() -> None:
    """u = ∂ψ/∂y et v = -∂ψ/∂x pour le champ cellulaire sinusoïdal."""
    # Given — un point du champ où k·x = k·y = π/4.
    x = y = CHAMP.longueur / 8
    # When — la fonction de courant et les vitesses sont évaluées.
    psi = CHAMP.fonction_courant(x, y)
    u, v = CHAMP.vitesse(x, y)
    # Then — les valeurs analytiques exactes sont restituées.
    assert psi == pytest.approx(0.5)
    assert u == pytest.approx(math.pi)
    assert v == pytest.approx(-math.pi)


def test_la_divergence_est_nulle_par_construction() -> None:
    """∇·u = 0 : vérifié par différences finies centrées en plusieurs points."""
    # Given — un pas de différenciation et des points dispersés.
    h = 1e-6
    points = [(0.1, 0.2), (0.37, 0.11), (-0.5, 1.3), (0.25, 0.9)]
    # When — la divergence numérique maximale est estimée.
    divergence_max = 0.0
    for x, y in points:
        du_dx = (CHAMP.vitesse(x + h, y)[0] - CHAMP.vitesse(x - h, y)[0]) / (2.0 * h)
        dv_dy = (CHAMP.vitesse(x, y + h)[1] - CHAMP.vitesse(x, y - h)[1]) / (2.0 * h)
        divergence_max = max(divergence_max, abs(du_dx + dv_dy))
    # Then — elle est nulle à la précision de différenciation près.
    assert divergence_max < 1e-6


def test_les_trajectoires_conservent_la_fonction_de_courant() -> None:
    """En champ stationnaire, ψ est conservé le long d'une trajectoire intégrée en RK4."""
    # Given — une particule lâchée dans une cellule de recirculation.
    x0 = y0 = CHAMP.longueur / 8
    psi0 = CHAMP.fonction_courant(x0, y0)
    # When — la trajectoire est intégrée avec RK4.
    _, x, y = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 2.0, 0.01, "rk4")
    # Then — la ligne de courant ψ = psi0 est suivie.
    assert CHAMP.fonction_courant(x[-1], y[-1]) == pytest.approx(psi0, abs=1e-5)


def test_l_erreur_rk4_decroit_avec_le_pas() -> None:
    """Le défaut de conservation de ψ décroît quand le pas de temps est raffiné."""
    # Given — une particule et trois pas de temps raffinés.
    x0 = y0 = CHAMP.longueur / 8
    psi0 = CHAMP.fonction_courant(x0, y0)
    # When — l'erreur de conservation finale est mesurée pour chaque pas.
    erreurs = []
    for dt in (0.04, 0.02, 0.01):
        _, x, y = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 2.0, dt, "rk4")
        erreurs.append(abs(CHAMP.fonction_courant(x[-1], y[-1]) - psi0))
    # Then — l'erreur décroît strictement avec le raffinement du pas.
    assert erreurs[2] < erreurs[1] < erreurs[0]


def test_rk4_est_plus_precis_que_euler_au_meme_pas() -> None:
    """À pas égal, RK4 conserve mieux ψ qu'Euler explicite."""
    # Given — une particule et un pas de temps commun aux deux méthodes.
    x0 = y0 = CHAMP.longueur / 8
    psi0 = CHAMP.fonction_courant(x0, y0)
    # When — les deux méthodes intègrent au même pas.
    _, x_e, y_e = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 2.0, 0.01, "euler")
    _, x_r, y_r = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 2.0, 0.01, "rk4")
    erreur_euler = abs(CHAMP.fonction_courant(x_e[-1], y_e[-1]) - psi0)
    erreur_rk4 = abs(CHAMP.fonction_courant(x_r[-1], y_r[-1]) - psi0)
    # Then — RK4 est nettement plus précis.
    assert erreur_rk4 < erreur_euler


def test_le_centre_de_cellule_est_un_point_de_stagnation() -> None:
    """Le centre d'une cellule est un point de stagnation : vitesse nulle, particule fixe."""
    # Given — le centre d'une cellule de recirculation.
    x0 = y0 = CHAMP.longueur / 4
    # When — la vitesse locale et la trajectoire sont évaluées.
    u, v = CHAMP.vitesse(x0, y0)
    _, x, y = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 1.0, 0.1, "rk4")
    # Then — la vitesse est nulle et la particule reste au centre.
    assert u == pytest.approx(0.0)
    assert v == pytest.approx(0.0)
    assert x[-1] == pytest.approx(x0)
    assert y[-1] == pytest.approx(y0)


def test_le_champ_est_immuable() -> None:
    """Un champ construit ne peut pas être modifié."""
    # Given — un champ valide.
    # When / Then — toute mutation est refusée.
    with pytest.raises(FrozenInstanceError):
        CHAMP.amplitude = 2.0
