"""Tests de cohérence de l'oracle analytique GZ-1 (issue #448).

Ces tests vérifient l'implémentation des formules fermées ; ils ne prouvent
pas le théorème de contrôlabilité et ne constituent pas une validation physique.
"""

from __future__ import annotations

from math import erf, pi, sqrt

import numpy as np
import pytest

from jdriftx.experiences.zermelo_gaussien import ModeleGZ1


@pytest.fixture
def modele() -> ModeleGZ1:
    """Cas de référence dimensionné, avec vent uniforme non nul."""
    return ModeleGZ1(
        masse=1.0e6,
        seuil=1.0,
        diffusivite=0.5,
        vent=(2.0, 0.0, 0.0),
        origine=(10.0, -5.0, 2.0),
    )


def test_parametres_et_domaines_sont_valides() -> None:
    """Les scalaires non positifs et coordonnées non réelles sont refusés."""
    with pytest.raises(ValueError, match="Masse"):
        ModeleGZ1(masse=0.0, seuil=1.0, diffusivite=1.0)
    with pytest.raises(ValueError, match="Seuil"):
        ModeleGZ1(masse=1.0, seuil=float("nan"), diffusivite=1.0)
    with pytest.raises(ValueError, match="vent"):
        ModeleGZ1(masse=1.0, seuil=1.0, diffusivite=1.0, vent=(1.0, 2.0, float("inf")))
    modele_invalide = ModeleGZ1(masse=1.0, seuil=1.0, diffusivite=1.0)
    with pytest.raises(ValueError, match="Temps"):
        modele_invalide.rayon(0.0)


def test_t_etoile_et_extinction_sont_coherents(modele: ModeleGZ1) -> None:
    """R(t*) est maximal et R(e t*) s'annule."""
    t_star = modele.t_etoile
    assert modele.rayon(t_star) == pytest.approx(modele.rayon_maximal)
    assert modele.vitesse_expansion(t_star) == pytest.approx(0.0, abs=1e-14)
    assert modele.rayon(modele.t_extinction) == pytest.approx(0.0, abs=1e-12)
    assert modele.rayon(0.9 * t_star) < modele.rayon_maximal
    assert modele.rayon(1.1 * t_star) < modele.rayon_maximal
    with pytest.raises(ValueError, match="expansion"):
        modele.vitesse_expansion(1.01 * t_star)
    with pytest.raises(ValueError, match="atteignable"):
        modele.ensemble_atteignable((0.0, 0.0, 0.0), 1.01 * t_star)


def test_deux_formes_du_rayon_et_derivee(modele: ModeleGZ1) -> None:
    """La forme explicite de R et R' coïncide avec les expressions dérivées."""
    t = 0.37 * modele.t_etoile
    lam = np.log(modele.masse / (modele.seuil * (4.0 * pi * modele.diffusivite * t) ** 1.5))
    rayon_direct = sqrt(4.0 * modele.diffusivite * t * float(lam))
    assert modele.rayon(t) == pytest.approx(rayon_direct, rel=1e-13)
    pas = 1e-5 * t
    derivee_centrale = (modele.rayon(t + pas) - modele.rayon(t - pas)) / (2.0 * pas)
    assert modele.vitesse_expansion(t) == pytest.approx(derivee_centrale, rel=1e-8)


def test_noyau_gaussien_et_conservation_de_masse_tronquee(modele: ModeleGZ1) -> None:
    """La quadrature 3D retrouve M à l'erreur de troncature près."""
    t = 25.0
    centre = np.asarray(modele.origine) + np.asarray(modele.vent) * t
    demi_cote = 5.0 * sqrt(4.0 * modele.diffusivite * t)
    noeuds, poids = np.polynomial.legendre.leggauss(28)
    axe = demi_cote * noeuds
    poids_axe = demi_cote * poids
    x, y, z = np.meshgrid(axe, axe, axe, indexing="ij")
    wx, wy, wz = np.meshgrid(poids_axe, poids_axe, poids_axe, indexing="ij")
    positions = np.stack((x, y, z), axis=-1) + centre
    valeurs = np.empty(x.shape)
    for index in np.ndindex(x.shape):
        valeurs[index] = modele.concentration(positions[index], t)
    masse_quadrature = float(np.sum(valeurs * wx * wy * wz))
    fraction_theorique = erf(demi_cote / sqrt(4.0 * modele.diffusivite * t)) ** 3
    masse_tronquee_attendue = modele.masse * fraction_theorique
    assert masse_quadrature == pytest.approx(masse_tronquee_attendue, rel=2e-9)
    assert modele.concentration(tuple(centre), t) == pytest.approx(
        modele.masse / (4.0 * pi * modele.diffusivite * t) ** 1.5
    )
    assert 0.0 < modele.masse - masse_tronquee_attendue < 1e-5 * modele.masse


def test_front_et_fonction_de_valeur_hj_ont_le_plateau_nul(modele: ModeleGZ1) -> None:
    """Le zéro HJ remplit la boule ; le front est sa frontière."""
    t = 0.4 * modele.t_etoile
    centre = np.asarray(modele.origine) + np.asarray(modele.vent) * t
    rayon = modele.rayon(t)
    assert modele.valeur_hj(tuple(centre), t) == 0.0
    assert modele.valeur_hj(tuple(centre + 0.5 * rayon * np.array([1.0, 0.0, 0.0])), t) == 0.0
    assert modele.valeur_hj(
        tuple(centre + rayon * np.array([1.0, 0.0, 0.0])), t
    ) == pytest.approx(0.0)
    assert modele.valeur_hj(
        tuple(centre + 2.0 * rayon * np.array([1.0, 0.0, 0.0])), t
    ) == pytest.approx(rayon)
    assert modele.ensemble_atteignable(tuple(centre + rayon * np.array([1.0, 0.0, 0.0])), t)
    assert not modele.ensemble_atteignable(
        tuple(centre + 1.01 * rayon * np.array([1.0, 0.0, 0.0])), t
    )


def test_commande_radiale_respecte_la_borne_et_atteint_la_cible(modele: ModeleGZ1) -> None:
    """La commande radiale réalise exactement le déplacement relatif prescrit."""
    temps_final = 0.45 * modele.t_etoile
    z = 0.7 * modele.rayon(temps_final) * np.array([0.6, 0.8, 0.0])
    for temps in (0.1 * temps_final, 0.5 * temps_final, temps_final):
        commande = np.asarray(modele.commande_radiale(tuple(z), temps_final, temps))
        assert np.linalg.norm(commande) <= modele.vitesse_expansion(temps) + 1e-12
        pas = 1e-6 * temps
        primitive_plus = z / modele.rayon(temps_final) * modele.rayon(temps + pas)
        primitive_moins = z / modele.rayon(temps_final) * modele.rayon(temps - pas)
        derivee = (primitive_plus - primitive_moins) / (2.0 * pas)
        np.testing.assert_allclose(commande, derivee, rtol=2e-8, atol=1e-9)
    assert np.linalg.norm(z / modele.rayon(temps_final) * modele.rayon(temps_final) - z) < 1e-12
    with pytest.raises(ValueError, match="hors de la boule"):
        modele.commande_radiale(
            (2.0 * modele.rayon(temps_final), 0.0, 0.0), temps_final, temps_final
        )


def test_randers_est_restreint_au_regime_sous_critique(modele: ModeleGZ1) -> None:
    """L'identité de la jauge est vérifiée seulement si c(t)>||u||."""
    temps = 1.0e-3 * modele.t_etoile
    deplacement = np.array([3.0, 1.0, -0.5])
    jauge = modele.jauge_randers(tuple(deplacement), temps)
    vent = np.asarray(modele.vent)
    c = modele.vitesse_expansion(temps)
    assert np.linalg.norm(deplacement / jauge - vent) == pytest.approx(c, rel=1e-12)
    t_z = None
    bas, haut = temps, modele.t_etoile
    if modele.vitesse_expansion(haut) < np.linalg.norm(vent):
        for _ in range(80):
            milieu = 0.5 * (bas + haut)
            if modele.vitesse_expansion(milieu) > np.linalg.norm(vent):
                bas = milieu
            else:
                haut = milieu
        t_z = 0.5 * (bas + haut)
    assert t_z is not None
    with pytest.raises(ValueError, match="Randers régulier"):
        modele.jauge_randers(tuple(deplacement), t_z * (1.0 + 1e-8))
    with pytest.raises(ValueError, match="Randers"):
        modele.jauge_randers(tuple(deplacement), 0.9 * modele.t_etoile)


def test_premier_contact_sans_vent_et_cas_limites() -> None:
    """La formule de contact sélectionne la racine d'expansion et son tangentiel."""
    modele = ModeleGZ1(masse=1.0e6, seuil=1.0, diffusivite=0.5)
    t_star = modele.t_etoile
    distance = 0.5 * modele.rayon_maximal
    cible = (distance, 0.0, 0.0)
    contact = modele.premier_contact(cible)
    assert contact is not None
    assert 0.0 < contact < t_star
    assert modele.fonction_contact(cible, contact) == pytest.approx(0.0, abs=1e-9)
    cible_tangente = (modele.rayon_maximal, 0.0, 0.0)
    assert modele.premier_contact(cible_tangente) == pytest.approx(t_star, rel=1e-9)
    cible_hors = (1.001 * modele.rayon_maximal, 0.0, 0.0)
    assert modele.premier_contact(cible_hors) is None


def test_premier_contact_vent_non_nul_selectionne_la_premiere_racine() -> None:
    """La convexité de g_B permet de distinguer les deux contacts possibles."""
    modele = ModeleGZ1(masse=1.0e6, seuil=1.0, diffusivite=0.5, vent=(10.0, 0.0, 0.0))
    temps_intermediaire = 0.8 * modele.t_etoile
    cible = (10.0 * temps_intermediaire, 0.0, 0.0)
    assert modele.fonction_contact(cible, temps_intermediaire) < 0.0
    assert modele.fonction_contact(cible, modele.t_etoile) > 0.0
    premier = modele.premier_contact(cible)
    assert premier is not None
    assert 0.0 < premier < temps_intermediaire
    assert modele.fonction_contact(cible, premier) == pytest.approx(0.0, abs=1e-8)


def test_validation_expresse_des_domaines_randers_et_contact(modele: ModeleGZ1) -> None:
    """Les domaines hors hypothèses ne sont pas silencieusement extrapolés."""
    with pytest.raises(ValueError, match="Temps"):
        modele.jauge_randers((1.0, 0.0, 0.0), 0.0)
    with pytest.raises(ValueError, match="contact"):
        modele.fonction_contact((1.0, 0.0, 0.0), modele.t_etoile * 1.01)
    with pytest.raises(ValueError, match="valeur HJ"):
        modele.valeur_hj((1.0, 0.0, 0.0), modele.t_etoile * 1.01)


def test_residu_hj_sur_les_regions_lisses(modele: ModeleGZ1) -> None:
    """Le résidu classique s'annule hors du coin ; le plateau intérieur est constant."""
    t = 0.4 * modele.t_etoile
    rayon = modele.rayon(t)
    vent = np.asarray(modele.vent)
    direction = np.array([1.0, 2.0, -1.0])
    direction /= np.linalg.norm(direction)
    centre = np.asarray(modele.origine) + vent * t
    point = centre + 2.0 * rayon * direction
    pas_t = 1e-5 * t
    pas_x = 1e-5 * rayon
    derivee_t = (
        modele.valeur_hj(tuple(point), t + pas_t) - modele.valeur_hj(tuple(point), t - pas_t)
    ) / (2.0 * pas_t)
    gradient = np.empty(3)
    for axe in range(3):
        decalage = np.zeros(3)
        decalage[axe] = pas_x
        gradient[axe] = (
            modele.valeur_hj(tuple(point + decalage), t)
            - modele.valeur_hj(tuple(point - decalage), t)
        ) / (2.0 * pas_x)
    residu = (
        derivee_t
        + float(vent @ gradient)
        + modele.vitesse_expansion(t) * float(np.linalg.norm(gradient))
    )
    assert residu == pytest.approx(0.0, abs=2e-7)

    point_interieur = centre + 0.25 * rayon * direction
    assert modele.valeur_hj(tuple(point_interieur), t + pas_t) == 0.0
    assert modele.valeur_hj(tuple(point_interieur), t - pas_t) == 0.0
