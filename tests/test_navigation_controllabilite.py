"""Tests numériques de la page « Navigation de Zermelo, fronts et Hamilton-Jacobi ».

Chaque test suit la forme GWT (Given-When-Then) : son contexte, son
action et sa conséquence attendue.

Couverture (issue #437, note docs/59) : cinématique exacte du front
d'isoconcentration gaussien (rayon, vitesse d'expansion, temps du
maximum, réalité du rayon jusqu'à e·t*), singularité initiale
intégrable, ensemble atteignable et théorème GZ-1 (égalité du temps de
navigation et du temps de contact du front) par trajectoire analytique à
cap constant, rejet d'une cible hors de portée, identité de la jauge
sous-critique et de la forme de Randers, cône d'accessibilité
supercritique (frontière arcsin(c/|u|), convention +∞), résidu de
l'équation de Hamilton-Jacobi du front et de l'eikonale stationnaire.

Ces tests vérifient le modèle mathématique posé sur la page du site
(puff gaussien tridimensionnel, vent uniforme constant, borne isotrope)
au niveau de précision des formes fermées en float64. Ils n'établissent
aucune validité physique et ne portent pas sur le code applicatif.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

MASSE = 1.0e6
DIFFUSIVITE = 0.5
SEUIL = 1.0
VENT = np.array([2.0, 0.0, 0.0])
CIBLE_HORS_AXE = np.array([120.0, 20.0, 0.0])
CIBLE_SUR_AXE = np.array([80.0, 0.0, 0.0])
CIBLE_HORS_DE_PORTEE = np.array([120.0, 30.0, 0.0])


def _lambda(t: float) -> float:
    """Surdimensionnement Λ(t) du puff gaussien (page §2)."""
    denominateur = SEUIL * (4.0 * math.pi * DIFFUSIVITE * t) ** 1.5
    return math.log(MASSE / denominateur)


def _rayon(t: float) -> float:
    """Rayon d'isoconcentration R(t) = sqrt(4 K t Λ(t)) (page §2)."""
    return math.sqrt(max(0.0, 4.0 * DIFFUSIVITE * t * _lambda(t)))


def _vitesse(t: float) -> float:
    """Vitesse d'expansion c(t) = R'(t) = 2K(Λ(t) - 3/2)/R(t) (page §2)."""
    return (2.0 * DIFFUSIVITE / _rayon(t)) * (_lambda(t) - 1.5)


def _t_etoile() -> float:
    """Instant du maximum du rayon t* = (4πK)⁻¹(M/(C₀ e^{3/2}))^{2/3}."""
    return (1.0 / (4.0 * math.pi * DIFFUSIVITE)) * (MASSE / (SEUIL * math.e**1.5)) ** (2.0 / 3.0)


def _concentration(ecart: float, t: float) -> float:
    """Concentration du puff à distance transverse ecart du centre, au temps t."""
    prefacteur = MASSE / (4.0 * math.pi * DIFFUSIVITE * t) ** 1.5
    return prefacteur * math.exp(-(ecart**2) / (4.0 * DIFFUSIVITE * t))


def _ecart(cible: np.ndarray, t: float) -> float:
    """Distance entre la cible et le centre advecté x₀ + u t."""
    return float(np.linalg.norm(cible - VENT * t))


def _temps_front(cible: np.ndarray) -> float:
    """Premier contact T_front : balayage grossier puis bissection."""
    pas = 0.05
    bas = 0.0
    for i in range(1, int(_t_etoile() / pas) + 2):
        t = i * pas
        if _ecart(cible, t) <= _rayon(t):
            bas = t - pas
            break
    else:
        raise ValueError("cible jamais atteinte par le front")
    haut = bas + pas
    for _ in range(100):
        milieu = 0.5 * (bas + haut)
        if _ecart(cible, milieu) > _rayon(milieu):
            bas = milieu
        else:
            haut = milieu
    return 0.5 * (bas + haut)


def _temps_navigation_cone(deplacement: np.ndarray, c: float) -> float | None:
    """Temps de navigation à borne isotrope constante c, |u| ≥ c (page §6.1).

    Renvoie None pour une direction hors du cône d'accessibilité
    (discriminant négatif ou dénominateur non positif) : convention +∞.
    """
    norme = float(np.linalg.norm(deplacement))
    direction = deplacement / norme
    k = float(VENT @ direction)
    discriminant = k * k + c * c - float(VENT @ VENT)
    if discriminant < -1.0e-12:
        return None
    denominateur = k + math.sqrt(max(0.0, discriminant))
    if denominateur <= 0.0:
        return None
    return norme / denominateur


def test_le_front_d_isoconcentration_est_exact() -> None:
    """Le rayon R(t) découpe exactement le niveau C = C₀ du puff."""
    # Given — le puff gaussien 3D et son seuil, à trois instants d'expansion.
    for t in (5.0, 50.0, 100.0):
        # Then — la concentration au bord du front vaut le seuil.
        assert _concentration(_rayon(t), t) == pytest.approx(SEUIL, rel=1e-12)
        # Then — à l'intérieur du front, la concentration dépasse le seuil.
        assert _concentration(0.9 * _rayon(t), t) > SEUIL
        # Then — à l'extérieur du front, elle reste sous le seuil.
        assert _concentration(1.1 * _rayon(t), t) < SEUIL


def test_la_vitesse_d_expansion_est_la_derivee_du_rayon() -> None:
    """La forme fermée c(t) coïncide avec la dérivée numérique de R(t)."""
    # Given — quatre instants dans la phase d'expansion 0 < t < t*.
    for t in (10.0, 50.0, 100.0, 300.0):
        pas = 1.0e-6 * t
        # When — la dérivée centrale de R est confrontée à la forme fermée.
        derivee = (_rayon(t + pas) - _rayon(t - pas)) / (2.0 * pas)
        # Then — les deux s'accordent à la précision des différences finies.
        assert derivee == pytest.approx(_vitesse(t), rel=1e-8)


def test_t_etoile_maximise_le_rayon() -> None:
    """R croît sur (0, t*), est maximal en t* où c(t*) = 0, puis décroît."""
    # Given — la forme fermée de t* et ses voisins.
    t_etoile = _t_etoile()
    # Then — la vitesse d'expansion s'annule en t*.
    assert abs(_vitesse(t_etoile)) < 1.0e-9
    # Then — le rayon croît avant t* et décroît après.
    assert _rayon(0.999 * t_etoile) < _rayon(t_etoile)
    assert _rayon(1.001 * t_etoile) < _rayon(t_etoile)
    # Then — R' décroît strictement pendant la phase d'expansion.
    vitesses = [_vitesse(t) for t in (10.0, 50.0, 100.0, 300.0)]
    assert all(a > b for a, b in zip(vitesses, vitesses[1:]))
    # Then — le rayon reste réel jusqu'à e·t* exactement : Λ(e t*) = 0.
    assert abs(_lambda(math.e * t_etoile)) < 1.0e-9
    assert _rayon(math.e * t_etoile * (1.0 - 1.0e-9)) > 0.0


def test_la_singularite_initiale_est_integrable() -> None:
    """c(t) diverge en 0 mais son intégrale redonne exactement R."""
    # Given — la borne de contrôle c(t) = R'(t) et la relation page §3.1.
    # Then — la vitesse diverge vers l'infini quand t → 0+.
    assert _vitesse(1.0e-2) > 0.0
    assert _vitesse(1.0e-3) > _vitesse(1.0e-2)
    assert _vitesse(1.0e-6) > _vitesse(1.0e-3)
    # When — c est intégrée au trapèze loin de la singularité, de 1 à 100.
    bas, haut = 1.0, 100.0
    mailles = 100000
    pas = (haut - bas) / mailles
    somme = sum(
        0.5 * (_vitesse(bas + i * pas) + _vitesse(bas + (i + 1) * pas)) * pas
        for i in range(mailles)
    )
    # Then — l'intégrale restitue exactement R(haut) - R(bas).
    assert somme == pytest.approx(_rayon(haut) - _rayon(bas), rel=1e-6)


def test_le_theoreme_gz1_egalise_navigation_et_front() -> None:
    """T_nav = T_front : une trajectoire à cap constant atteint la cible
    exactement à l'instant du premier contact du front (page §3.2)."""
    # Given — une cible hors de l'axe du vent, et son instant de contact.
    t_contact = _temps_front(CIBLE_HORS_AXE)
    # When — la direction co-mobile du contact définit un cap constant.
    chapeau = (CIBLE_HORS_AXE - VENT * t_contact) / _rayon(t_contact)

    def position(t: float) -> np.ndarray:
        return VENT * t + _rayon(t) * chapeau

    # Then — la trajectoire atteint la cible exactement à l'instant du contact.
    assert float(np.linalg.norm(position(t_contact) - CIBLE_HORS_AXE)) < 1.0e-9
    # Then — elle ne l'atteint pas avant le contact.
    assert float(np.linalg.norm(position(t_contact - 0.5) - CIBLE_HORS_AXE)) > 1.0
    # Then — la concentration au point cible vaut le seuil au contact.
    assert _concentration(_ecart(CIBLE_HORS_AXE, t_contact), t_contact) == pytest.approx(
        SEUIL, rel=1e-12
    )
    # Then — la trajectoire résout l'EDO pointée : dX/dt = u + chapeau·c(t).
    for t in (10.0, 25.0, 40.0, 50.0):
        pas = 1.0e-6
        v = (position(t + pas) - position(t - pas)) / (2.0 * pas)
        np.testing.assert_allclose(v, VENT + chapeau * _vitesse(t), atol=1.0e-6)
        # Then — la commande reste dans la borne : |dX/dt - u| = c(t).
        assert float(np.linalg.norm(v - VENT)) == pytest.approx(_vitesse(t), rel=1e-6)
    # Then — même égalité pour une cible sur l'axe du vent.
    t_axe = _temps_front(CIBLE_SUR_AXE)
    assert _concentration(_ecart(CIBLE_SUR_AXE, t_axe), t_axe) == pytest.approx(SEUIL, rel=1e-12)


def test_la_commande_radiale_remplit_exactement_la_boule() -> None:
    """La commande radiale atteint chaque déplacement relatif de norme ≤ R(t)."""
    # Given — un instant d'expansion et une direction unitaire fixe.
    t = 50.0
    direction = np.array([0.6, 0.8, 0.0])
    rayon = _rayon(t)
    pas = 1.0e-6
    # When — on construit la commande associée à plusieurs points de la boule.
    for fraction in (0.0, 0.5, 1.0):
        z = fraction * rayon * direction

        def commande(tau: float, fraction: float = fraction, z: np.ndarray = z) -> np.ndarray:
            if fraction == 0.0:
                return np.zeros(3)
            return (z / rayon) * _vitesse(tau)

        def primitive(tau: float, z: np.ndarray = z) -> np.ndarray:
            return (z / rayon) * _rayon(tau)

        # Then — la commande respecte la borne et dérive bien de la primitive.
        for tau in (1.0, 10.0, 25.0, t):
            assert float(np.linalg.norm(commande(tau))) <= _vitesse(tau) + 1e-12
            derivee = (primitive(tau + pas) - primitive(tau - pas)) / (2.0 * pas)
            np.testing.assert_allclose(derivee, commande(tau), atol=1e-6)
        # Then — la primitive passe de zéro à z sur [0, t].
        np.testing.assert_allclose(primitive(t), z, atol=1e-12)
    # Then — un point extérieur demanderait une commande au-delà de la borne.
    z_exterieur = 1.1 * rayon * direction
    assert float(np.linalg.norm((z_exterieur / rayon) * _vitesse(10.0))) > _vitesse(10.0)


def test_une_cible_hors_de_portee_n_est_jamais_atteinte() -> None:
    """Une cible que le front n'englobe jamais n'a pas de temps de contact."""
    # Given — une cible dont l'écart minimal au centre dépasse le rayon atteint.
    # When — toute la phase d'expansion (0, t*] est balayée finement.
    t_etoile = _t_etoile()
    mailles = 20000
    # Then — aucun instant de contact n'existe : T_front = +∞.
    for i in range(1, mailles + 1):
        t = (i / mailles) * t_etoile
        assert _ecart(CIBLE_HORS_DE_PORTEE, t) > _rayon(t)


def test_la_jauge_sous_critique_est_une_randers() -> None:
    """La jauge fermée de Zermelo et la forme de Randers coïncident (page §6)."""
    # Given — un régime sous-critique c = 3 > |u| = 2, donc A = 5 > 0.
    c = 3.0
    aire = c * c - float(VENT @ VENT)
    assert aire > 0.0
    a = (aire * np.eye(3) + np.outer(VENT, VENT)) / aire**2
    b = -VENT / aire
    a_inverse = aire * np.eye(3) - (aire / c**2) * np.outer(VENT, VENT)
    norme_duale_b = float(b @ a_inverse @ b)
    assert norme_duale_b == pytest.approx(float(VENT @ VENT) / c**2, rel=1e-12)
    assert norme_duale_b < 1.0
    # When — la jauge fermée et la forme de Randers sont confrontées.
    for coordonnees in (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (3.0, -2.0, 1.0),
        (-2.0, 1.0, 0.5),
    ):
        v = np.array(coordonnees)
        produit = float(VENT @ v)
        fermee = (math.sqrt(produit**2 + aire * float(v @ v)) - produit) / aire
        a = (aire * np.eye(3) + np.outer(VENT, VENT)) / aire**2
        b = -VENT / aire
        randers = math.sqrt(float(v @ a @ v)) + float(b @ v)
        # Then — les deux formes coïncident à la précision machine.
        assert fermee == pytest.approx(randers, rel=1e-12)
    # Then — sur l'axe aval, la jauge redonne |dx|/(|u| + c).
    deplacement_axe = np.array([10.0, 0.0, 0.0])
    produit = float(VENT @ deplacement_axe)
    jauge_axe = (
        math.sqrt(produit**2 + aire * float(deplacement_axe @ deplacement_axe)) - produit
    ) / aire
    assert jauge_axe == pytest.approx(10.0 / (2.0 + c), rel=1e-12)
    # Then — la jauge est homogène de degré 1.
    v = np.array([2.0, 1.0, 0.0])
    produit = float(VENT @ v)
    jauge_v = (math.sqrt(produit**2 + aire * float(v @ v)) - produit) / aire
    produit3 = float(VENT @ (3.0 * v))
    jauge_3v = (math.sqrt(produit3**2 + aire * float((3.0 * v) @ (3.0 * v))) - produit3) / aire
    assert jauge_3v == pytest.approx(3.0 * jauge_v, rel=1e-12)


def test_le_regime_supercritique_definit_un_cone() -> None:
    """À borne constante c < |u|, les directions atteignables forment un cône
    de demi-angle arcsin(c/|u|) ; hors du cône, le temps est infini."""
    # Given — un régime supercritique c = 1 < |u| = 2.
    c = 1.0
    demi_angle = math.asin(c / float(np.linalg.norm(VENT)))
    # Then — une direction intérieure au cône est atteignable en temps fini.
    dedans = np.array([math.cos(0.9 * demi_angle), math.sin(0.9 * demi_angle), 0.0]) * 10.0
    assert _temps_navigation_cone(dedans, c) is not None
    # Then — la frontière exacte du cône sépare le fini de l'infini.
    sur_la_frontiere = np.array([math.cos(demi_angle), math.sin(demi_angle), 0.0]) * 10.0
    assert _temps_navigation_cone(sur_la_frontiere, c) is not None
    juste_dehors = (
        np.array(
            [math.cos(demi_angle * (1.0 + 1.0e-9)), math.sin(demi_angle * (1.0 + 1.0e-9)), 0.0]
        )
        * 10.0
    )
    assert _temps_navigation_cone(juste_dehors, c) is None
    # Then — sur l'axe aval, le temps vaut |dx|/(|u| + c).
    axe = np.array([10.0, 0.0, 0.0])
    assert _temps_navigation_cone(axe, c) == pytest.approx(10.0 / 3.0, rel=1e-12)
    # Then — remonter le vent est impossible : convention +∞.
    assert _temps_navigation_cone(-axe, c) is None
    # Then — le cône amont opposé est rejeté, même si son sinus est petit.
    amont_oblique = np.array([-math.cos(0.1), math.sin(0.1), 0.0]) * 10.0
    assert _temps_navigation_cone(amont_oblique, c) is None
    # Given — au seuil critique c = |u|, les directions aval restent accessibles.
    critique = float(np.linalg.norm(VENT))
    assert _temps_navigation_cone(axe, critique) is not None
    # Then — la direction exactement transverse est seulement limite, pas atteinte.
    transverse = np.array([0.0, 10.0, 0.0])
    assert _temps_navigation_cone(transverse, critique) is None


def test_le_front_satisfait_l_equation_hamilton_jacobi() -> None:
    """La valeur de Hopf-Lax max(|x - u t| - R(t), 0) résout HJ
    hors du coin du front ; le plateau intérieur est également vérifié."""
    # Given — trois points extérieurs au front au temps t = 40.
    t = 40.0
    points = (
        np.array([50.0, 20.0, 5.0]),
        np.array([80.0, 0.0, 30.0]),
        np.array([100.0, -15.0, 8.0]),
    )

    def phi(x: np.ndarray, temps: float) -> float:
        # Valeur de Hopf-Lax : plateau nul dans toute la boule atteignable.
        return max(float(np.linalg.norm(x - VENT * temps)) - _rayon(temps), 0.0)

    pas = 1.0e-6
    directions = (
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    )
    points += (VENT * t,)  # point intérieur : gradient et dérivée nuls.
    for x in points:
        # When — les dérivées de φ sont prises par différences finies centrées.
        grad = np.array(
            [(phi(x + pas * e, t) - phi(x - pas * e, t)) / (2.0 * pas) for e in directions]
        )
        phi_t = (phi(x, t + pas) - phi(x, t - pas)) / (2.0 * pas)
        residu = phi_t + float(VENT @ grad) + _vitesse(t) * float(np.linalg.norm(grad))
        # Then — le résidu de l'équation HJ est nul à la précision du schéma.
        assert abs(residu) < 1.0e-6


def test_l_eikonale_stationnaire_en_champ_uniforme() -> None:
    """La jauge fermée du problème stationnaire résout l'eikonale
    u·∇T + c|∇T| = 1 du temps minimal de navigation (page §5.2)."""
    # Given — le régime sous-critique c = 3 > |u| = 2 et sa jauge fermée.
    c = 3.0

    def temps_minimal(deplacement: np.ndarray) -> float:
        norme = float(np.linalg.norm(deplacement))
        direction = deplacement / norme
        k = float(VENT @ direction)
        return norme / (k + math.sqrt(k * k + c * c - float(VENT @ VENT)))

    pas = 1.0e-6
    for coordonnees in ((4.0, 1.0), (10.0, -3.0), (-2.0, 5.0), (7.0, 7.0)):
        # When — le gradient de la forme fermée est pris par différences finies.
        gx = (
            temps_minimal(np.array([coordonnees[0] + pas, coordonnees[1], 0.0]))
            - temps_minimal(np.array([coordonnees[0] - pas, coordonnees[1], 0.0]))
        ) / (2.0 * pas)
        gy = (
            temps_minimal(np.array([coordonnees[0], coordonnees[1] + pas, 0.0]))
            - temps_minimal(np.array([coordonnees[0], coordonnees[1] - pas, 0.0]))
        ) / (2.0 * pas)
        residu = VENT[0] * gx + VENT[1] * gy + c * math.hypot(gx, gy) - 1.0
        # Then — le résidu de l'eikonale stationnaire est nul à la précision du schéma.
        assert abs(residu) < 1.0e-6
    # Then — sur l'axe aval, le temps minimal redonne |dx|/(|u| + c).
    assert temps_minimal(np.array([10.0, 0.0, 0.0])) == pytest.approx(2.0, rel=1e-12)
