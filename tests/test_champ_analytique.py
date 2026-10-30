"""Tests du champ plan incompressible à fonction de courant (phase 2, Fig. 1)."""

import math
from dataclasses import FrozenInstanceError

import pytest

from jdriftx.champ_analytique import ChampFonctionCourant, SuperpositionChamps
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
    # When — la trajectoire est intégrée avec RK4 ; l'erreur de phase résiduelle
    # de RK4 décroît en dt⁴, d'où un pas assez fin pour ~13 tours d'orbite.
    _, x, y = integrate_trajectory(_vitesse_stationnaire, x0, y0, 0.0, 2.0, 0.0025, "rk4")
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


def test_la_superposition_vide_est_rejetee() -> None:
    """L'invariant « au moins un champ » est vérifié à la construction."""
    # Given — un tuple de champs vide.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="au moins un champ"):
        SuperpositionChamps(())


def test_la_superposition_est_la_somme_exacte_des_champs() -> None:
    """Fonction de courant et vitesses d'une superposition : sommes exactes."""
    # Given — deux champs d'échelles différentes et un point quelconque.
    champ_1 = ChampFonctionCourant(amplitude=800.0, longueur=1000.0)
    champ_2 = ChampFonctionCourant(amplitude=400.0, longueur=500.0)
    superposition = SuperpositionChamps((champ_1, champ_2))
    x, y = 137.0, 643.0
    # When — la superposition est évaluée au point.
    psi = superposition.fonction_courant(x, y)
    u, v = superposition.vitesse(x, y)
    u_1, v_1 = champ_1.vitesse(x, y)
    u_2, v_2 = champ_2.vitesse(x, y)
    # Then — les valeurs sont exactement les sommes accumulées champ par champ.
    assert psi == champ_1.fonction_courant(x, y) + champ_2.fonction_courant(x, y)
    assert (u, v) == (u_1 + u_2, v_1 + v_2)


def test_la_superposition_est_aussi_a_divergence_nulle() -> None:
    """La superposition de champs incompressibles reste incompressible (∇·u = 0)."""
    # Given — deux champs d'échelles différentes superposés, des points dispersés.
    champ_1 = ChampFonctionCourant(amplitude=800.0, longueur=1000.0)
    champ_2 = ChampFonctionCourant(amplitude=400.0, longueur=500.0)
    superposition = SuperpositionChamps((champ_1, champ_2))
    h = 1e-6
    points = [(137.0, 643.0), (500.0, 250.0), (-320.0, 90.0), (750.0, 125.0)]
    # When — la divergence numérique maximale est estimée par différences centrées.
    divergence_max = 0.0
    for x, y in points:
        du_dx = (superposition.vitesse(x + h, y)[0] - superposition.vitesse(x - h, y)[0]) / (
            2.0 * h
        )
        dv_dy = (superposition.vitesse(x, y + h)[1] - superposition.vitesse(x, y - h)[1]) / (
            2.0 * h
        )
        divergence_max = max(divergence_max, abs(du_dx + dv_dy))
    # Then — elle est nulle à la précision de différenciation près.
    assert divergence_max < 1e-6


@pytest.mark.parametrize("longueur", [1e-308, 5e-324])
def test_le_nombre_d_onde_debordant_est_rejete_a_la_construction(longueur: float) -> None:
    """Étant donné une longueur si petite que k déborde, la construction est refusée.

    Le nombre d'onde k = 2π/longueur peut déborder vers l'infini alors que
    la longueur est finie et strictement positive : le contrat refuse la
    construction plutôt que d'évaluer silencieusement en NaN.
    """
    # Given — une longueur positive sous la limite de débordement de k.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="nombre d'onde"):
        ChampFonctionCourant(amplitude=1.0, longueur=longueur)


@pytest.mark.parametrize(("x", "y"), [(float("nan"), 0.0), (0.0, float("inf"))])
def test_les_coordonnees_non_finies_sont_rejetees(x: float, y: float) -> None:
    """Les évaluations du champ refusent les coordonnées non finies avant tout calcul."""
    # Given — un champ valide et une coordonnée non finie.
    champ = ChampFonctionCourant(amplitude=1.0, longueur=1.0)
    # When / Then — la fonction de courant et la vitesse refusent l'évaluation.
    with pytest.raises(ValueError, match="coordonnées doivent être finies"):
        champ.fonction_courant(x, y)
    with pytest.raises(ValueError, match="coordonnées doivent être finies"):
        champ.vitesse(x, y)


def test_la_vitesse_debordante_est_rejetee() -> None:
    """Étant donné des paramètres finis valides, une vitesse infinie est refusée.

    Le produit amplitude · k peut déborder vers l'infini alors que chaque
    paramètre est fini et valide : l'évaluation lève ValueError plutôt que
    de retourner une composante infinie silencieuse.
    """
    # Given — un champ dont amplitude · k dépasse le plus grand float64.
    champ = ChampFonctionCourant(amplitude=1e200, longueur=6.283e-201)
    # un point où sin(k·x) et cos(k·y) sont non nuls.
    point = (math.pi / 4.0) / champ.nombre_donde
    # When / Then — l'évaluation de la vitesse est refusée.
    with pytest.raises(ValueError, match="vitesse du champ doit rester finie"):
        champ.vitesse(point, point)


def test_la_superposition_debordante_est_rejetee() -> None:
    """Étant donné des vitesses finies extrêmes, la somme ne déborde pas en silence.

    Chaque champ retourne des composantes finies, mais leur somme dépasse
    le plus grand float64 : la superposition lève ValueError au lieu de
    retourner +inf, comme la superposition de panaches.
    """
    # Given — deux champs identiques de vitesse 1,5e308 au point choisi.
    champ = ChampFonctionCourant(amplitude=1.5e308 / (2.0 * math.pi), longueur=1.0)
    superposition = SuperpositionChamps((champ, champ))
    # When / Then — la somme déborde au point où sin(k·x) et cos(k·y) valent 1.
    with pytest.raises(ValueError, match="superposition doit rester finie"):
        superposition.vitesse(0.25, 0.0)
    # Et la somme des fonctions de courant déborde au centre des cellules.
    champ_psi = ChampFonctionCourant(amplitude=1.5e308, longueur=1.0)
    superposition_psi = SuperpositionChamps((champ_psi, champ_psi))
    with pytest.raises(ValueError, match="superposition doit rester finie"):
        superposition_psi.fonction_courant(0.25, 0.25)
