"""Tests du squelette de benchmark S0 (Given/When/Then)."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from jdriftx.benchmarks.reference import (
    CAS_S0_DEFAUT,
    CasS0,
    PointMesure,
    evaluer_prediction,
    fac2,
    grille_mesures,
    main,
    mesurer_cout_inference,
    nmse,
    verite_s0,
)
from jdriftx.similitude import concentration_panache


def _cas_valide() -> CasS0:
    """Cas S0 valide minimal pour les tests."""
    return CasS0(
        debit=2.0,
        u=3.0,
        classe="C",
        hauteur=1.0,
        arcs=(100.0, 200.0),
        positions_laterales=(-50.0, 0.0, 50.0),
        z_mesure=1.5,
    )


class TestCasS0:
    def test_refuse_vent_non_positif(self) -> None:
        """Given un vent nul, When construction, Then refus."""
        with pytest.raises(ValueError, match="vent"):
            replace(_cas_valide(), u=0.0)

    def test_refuse_debit_non_positif(self) -> None:
        """Given un debit nul, When construction, Then refus."""
        with pytest.raises(ValueError, match="debit"):
            replace(_cas_valide(), debit=0.0)

    def test_refuse_arc_non_positif(self) -> None:
        """Given un arc nul, When construction, Then refus."""
        with pytest.raises(ValueError, match="sous le vent"):
            replace(_cas_valide(), arcs=(0.0, 200.0))

    def test_refuse_arcs_non_croissants(self) -> None:
        """Given des arcs decroissants, When construction, Then refus."""
        with pytest.raises(ValueError, match="ordre croissant"):
            replace(_cas_valide(), arcs=(200.0, 100.0))

    def test_refuse_positions_laterales_vides(self) -> None:
        """Given aucune position laterale, When construction, Then refus."""
        with pytest.raises(ValueError, match="laterale"):
            replace(_cas_valide(), positions_laterales=())

    def test_refuse_arcs_vides(self) -> None:
        """Given aucun arc, When construction, Then refus."""
        with pytest.raises(ValueError, match="arc de mesure"):
            replace(_cas_valide(), arcs=())

    def test_refuse_classe_inconnue(self) -> None:
        """Given une classe inexistante, When construction, Then refus."""
        with pytest.raises(ValueError, match="Z"):
            replace(_cas_valide(), classe="Z")

    def test_refuse_hauteur_negative(self) -> None:
        """Given une hauteur negative, When construction, Then refus."""
        with pytest.raises(ValueError, match="hauteur"):
            replace(_cas_valide(), hauteur=-1.0)

    def test_refuse_z_mesure_negative(self) -> None:
        """Given une altitude de mesure negative, When construction, Then refus."""
        with pytest.raises(ValueError, match="altitude"):
            replace(_cas_valide(), z_mesure=-1.5)

    def test_immuable(self) -> None:
        """Given un cas valide, When affectation, Then refus."""
        cas = _cas_valide()
        with pytest.raises(AttributeError):
            cas.u = 5.0  # type: ignore[misc]


class TestGrilleEtVerite:
    def test_grille_croisee(self) -> None:
        """Given 2 arcs x 3 positions, When grille, Then 6 points ordonnes."""
        points = grille_mesures(_cas_valide())
        assert len(points) == 6
        assert points[0] == PointMesure(x=100.0, y=-50.0, z=1.5)
        assert points[5] == PointMesure(x=200.0, y=50.0, z=1.5)

    def test_verite_egal_solution_de_similitude(self) -> None:
        """Given la grille du cas, When verite, Then elle est exactement la solution."""
        cas = _cas_valide()
        points = grille_mesures(cas)
        attendu = concentration_panache(
            x=np.array([p.x for p in points]),
            y=np.array([p.y for p in points]),
            z=np.array([p.z for p in points]),
            debit=cas.debit,
            u=cas.u,
            classe=cas.classe,
            hauteur=cas.hauteur,
        )
        np.testing.assert_array_equal(verite_s0(cas, points), attendu)

    def test_verite_positive_et_decroissante_sur_l_axe(self) -> None:
        """Given des mesures sur l axe, When verite, Then positive decroissante."""
        cas = replace(_cas_valide(), arcs=(100.0, 200.0, 400.0, 800.0), positions_laterales=(0.0,))
        vrais = verite_s0(cas, grille_mesures(cas))
        assert np.all(vrais > 0.0)
        assert np.all(np.diff(vrais) < 0.0)

    def test_refuse_points_vides(self) -> None:
        """Given une grille vide, When verite, Then refus."""
        with pytest.raises(ValueError, match="point"):
            verite_s0(_cas_valide(), ())


class TestMetriques:
    def test_fac2_identite(self) -> None:
        """Given prediction = verite, When FAC2, Then 1."""
        vrais = np.array([1.0, 2.0, 4.0])
        assert fac2(vrais, vrais) == 1.0

    def test_fac2_bornes_incluses(self) -> None:
        """Given predictions aux bornes 0.5x et 2x, When FAC2, Then 1."""
        vrais = np.array([1.0, 1.0])
        assert fac2(vrais, np.array([0.5, 2.0])) == 1.0

    def test_fac2_hors_facteur(self) -> None:
        """Given une prediction a 2.1x, When FAC2, Then fraction attendue."""
        vrais = np.array([1.0, 1.0])
        assert fac2(vrais, np.array([2.1, 1.0])) == 0.5

    def test_nmse_identite(self) -> None:
        """Given prediction = verite, When NMSE, Then 0."""
        vrais = np.array([1.0, 2.0, 4.0])
        assert nmse(vrais, vrais) == 0.0

    def test_nmse_double(self) -> None:
        """Given prediction = 2x verite, When NMSE, Then 1."""
        vrais = np.array([1.0, 1.0])
        assert nmse(vrais, 2.0 * vrais) == 1.0

    def test_refuse_verite_non_positive(self) -> None:
        """Given une verite avec un zero, When metriques, Then refus."""
        vrais = np.array([1.0, 0.0])
        with pytest.raises(ValueError, match="positives"):
            fac2(vrais, vrais)
        with pytest.raises(ValueError, match="positives"):
            nmse(vrais, vrais)

    def test_refuse_tailles_differentes(self) -> None:
        """Given des tailles differentes, When metriques, Then refus."""
        with pytest.raises(ValueError, match="meme taille"):
            fac2(np.array([1.0]), np.array([1.0, 2.0]))
        with pytest.raises(ValueError, match="meme taille"):
            nmse(np.array([1.0]), np.array([1.0, 2.0]))

    def test_refuse_vecteurs_vides(self) -> None:
        """Given des vecteurs vides, When metriques, Then refus."""
        with pytest.raises(ValueError, match="requis"):
            fac2(np.array([]), np.array([]))
        with pytest.raises(ValueError, match="requis"):
            nmse(np.array([]), np.array([]))


class TestEvaluation:
    def test_evaluer_prediction_auto_coherence(self) -> None:
        """Given prediction = verite, When evaluation, Then FAC2 1 NMSE 0."""
        vrais = verite_s0(_cas_valide(), grille_mesures(_cas_valide()))
        resultat = evaluer_prediction(vrais, vrais)
        assert resultat.fac2 == 1.0
        assert resultat.nmse == 0.0
        assert resultat.effectif == 6

    def test_vers_dict(self) -> None:
        """Given un resultat, When export, Then dict a trois cles."""
        resultat = evaluer_prediction(np.array([1.0]), np.array([1.0]))
        assert resultat.vers_dict() == {"fac2": 1.0, "nmse": 0.0, "effectif": 1}


class TestCommande:
    def test_main_auto_coherence(self) -> None:
        """Given le cas par defaut, When commande, Then FAC2 1 NMSE 0."""
        effectif = len(CAS_S0_DEFAUT.arcs) * len(CAS_S0_DEFAUT.positions_laterales)
        assert main() == {"fac2": 1.0, "nmse": 0.0, "effectif": effectif}

    def test_cout_inference_positif(self) -> None:
        """Given la verite S0, When mesure de cout, Then positif et fini."""
        cas = CAS_S0_DEFAUT
        points = grille_mesures(cas)
        cout = mesurer_cout_inference(verite_s0, cas, points)
        assert cout >= 0.0
        assert np.isfinite(cout)
