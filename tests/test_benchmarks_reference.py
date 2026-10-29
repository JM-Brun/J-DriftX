"""Tests du squelette de benchmarks : cas, metriques et evaluation."""

from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

import numpy as np
import pytest

from jdriftx.benchmarks import (
    CAS_S0_DEFAUT,
    FAC2,
    METRIQUES,
    NMSE,
    CasS0,
    CasSynthetique,
    Metrique,
    PointMesure,
    calculer_metriques,
    construire_cas,
    enregistrer_cas,
    enregistrer_metrique,
    evaluer_prediction,
    fac2,
    lister_cas,
    main,
    mesurer_cout_inference,
    nmse,
    retirer_cas,
    retirer_metrique,
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


class _CasT(CasSynthetique):
    """Cas minimal valide, pour tester le registre."""

    identifiant: ClassVar[str] = "T1"
    libelle: ClassVar[str] = "cas de test"

    def points(self) -> tuple[PointMesure, ...]:
        """Un unique point sur l axe."""
        return (PointMesure(x=100.0, y=0.0, z=1.5),)

    def verite(self, points: tuple[PointMesure, ...]) -> np.ndarray:
        """Verite constante strictement positive."""
        return np.full(len(points), 1.0)


class _CasNegatif(_CasT):
    """Cas a verite non positive, pour tester les garde-fous du registre."""

    identifiant: ClassVar[str] = "T2"

    def verite(self, points: tuple[PointMesure, ...]) -> np.ndarray:
        """Verite strictement negative."""
        return np.full(len(points), -1.0)


class _CasVide(_CasT):
    """Cas a grille vide, pour tester les garde-fous du registre."""

    identifiant: ClassVar[str] = "T3"

    def points(self) -> tuple[PointMesure, ...]:
        """Grille vide."""
        return ()


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
        points = _cas_valide().points()
        assert len(points) == 6
        assert points[0] == PointMesure(x=100.0, y=-50.0, z=1.5)
        assert points[5] == PointMesure(x=200.0, y=50.0, z=1.5)

    def test_verite_egal_solution_de_similitude(self) -> None:
        """Given la grille du cas, When verite, Then exactement la solution."""
        cas = _cas_valide()
        points = cas.points()
        attendu = concentration_panache(
            x=np.array([p.x for p in points]),
            y=np.array([p.y for p in points]),
            z=np.array([p.z for p in points]),
            debit=cas.debit,
            u=cas.u,
            classe=cas.classe,
            hauteur=cas.hauteur,
        )
        np.testing.assert_array_equal(cas.verite(points), attendu)

    def test_verite_positive_et_decroissante_sur_l_axe(self) -> None:
        """Given des mesures sur l axe, When verite, Then positive decroissante."""
        cas = replace(_cas_valide(), arcs=(100.0, 200.0, 400.0, 800.0), positions_laterales=(0.0,))
        vrais = cas.verite(cas.points())
        assert np.all(vrais > 0.0)
        assert np.all(np.diff(vrais) < 0.0)

    def test_refuse_points_vides(self) -> None:
        """Given une grille vide, When verite, Then refus."""
        with pytest.raises(ValueError, match="point"):
            _cas_valide().verite(())


class TestRegistreCas:
    def test_s0_enregistre(self) -> None:
        """Given import du module, When lister, Then S0 seul present."""
        assert lister_cas() == ("S0",)

    def test_construire_s0(self) -> None:
        """Given l identifiant S0, When construire, Then cas par defaut."""
        assert construire_cas("S0") == CAS_S0_DEFAUT

    def test_refuse_cas_inconnu(self) -> None:
        """Given un identifiant inconnu, When construire, Then refus."""
        with pytest.raises(ValueError, match="enregistres"):
            construire_cas("ZZ")

    def test_enregistrement_puis_retrait(self) -> None:
        """Given un cas valide, When ajouter puis retirer, Then cycle complet."""
        enregistrer_cas(_CasT)
        assert lister_cas() == ("S0", "T1")
        retirer_cas("T1")
        assert lister_cas() == ("S0",)

    def test_refuse_doublon(self) -> None:
        """Given un identifiant deja pris, When ajouter, Then refus."""
        with pytest.raises(ValueError, match="deja enregistre"):
            enregistrer_cas(lambda: CAS_S0_DEFAUT)

    def test_refuse_verite_non_positive(self) -> None:
        """Given une verite negative, When ajouter, Then refus."""
        with pytest.raises(ValueError, match="strictement positive"):
            enregistrer_cas(_CasNegatif)

    def test_refuse_grille_vide(self) -> None:
        """Given une grille vide, When ajouter, Then refus."""
        with pytest.raises(ValueError, match="grille vide"):
            enregistrer_cas(_CasVide)

    def test_refuse_retrait_inconnu(self) -> None:
        """Given un identifiant absent, When retirer, Then refus."""
        with pytest.raises(ValueError, match="absent"):
            retirer_cas("ZZ")


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
        with pytest.raises(ValueError, match="positive"):
            fac2(vrais, vrais)
        with pytest.raises(ValueError, match="positive"):
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

    def test_calcul_par_defaut(self) -> None:
        """Given metriques par defaut, When calcul, Then fac2 et nmse."""
        vrais = np.array([1.0, 2.0])
        assert calculer_metriques(vrais, vrais) == {"fac2": 1.0, "nmse": 0.0}

    def test_calcul_sous_ensemble(self) -> None:
        """Given un sous-ensemble explicite, When calcul, Then lui seul."""
        vrais = np.array([1.0, 2.0])
        assert calculer_metriques(vrais, 2.0 * vrais, metriques=(NMSE,)) == {"nmse": 1.0}

    def test_refuse_doublon_de_metriques(self) -> None:
        """Given une metrique demandee deux fois, When calcul, Then refus."""
        vrais = np.array([1.0])
        with pytest.raises(ValueError, match="qu une seule fois"):
            calculer_metriques(vrais, vrais, metriques=(FAC2, FAC2))

    def test_refuse_aucune_metrique(self) -> None:
        """Given aucune metrique, When calcul, Then refus."""
        vrais = np.array([1.0])
        with pytest.raises(ValueError, match="Au moins une metrique"):
            calculer_metriques(vrais, vrais, metriques=())

    def test_enregistrement_puis_retrait(self) -> None:
        """Given une metrique valide, When ajouter puis retirer, Then cycle."""
        metrique = Metrique(nom="de_test", libelle="test", ancrage="test", calcul=fac2)
        enregistrer_metrique(metrique)
        assert METRIQUES["de_test"] is metrique
        retirer_metrique("de_test")
        assert "de_test" not in METRIQUES

    def test_refuse_metrique_doublon(self) -> None:
        """Given un nom deja pris, When ajouter, Then refus."""
        doublon = Metrique(nom="fac2", libelle="x", ancrage="x", calcul=fac2)
        with pytest.raises(ValueError, match="deja enregistree"):
            enregistrer_metrique(doublon)

    def test_refuse_retrait_metrique_inconnue(self) -> None:
        """Given un nom absent, When retirer, Then refus."""
        with pytest.raises(ValueError, match="absente"):
            retirer_metrique("zz")


class TestEvaluation:
    def test_auto_coherence(self) -> None:
        """Given prediction = verite, When evaluation, Then metriques parfaites."""
        cas = CAS_S0_DEFAUT
        vrais = cas.verite(cas.points())
        resultat = evaluer_prediction(vrais, vrais)
        assert resultat.metriques == {"fac2": 1.0, "nmse": 0.0}
        assert resultat.effectif == len(cas.points())

    def test_vers_dict(self) -> None:
        """Given un resultat, When export, Then dict avec effectif."""
        resultat = evaluer_prediction(np.array([1.0]), np.array([1.0]))
        assert resultat.vers_dict() == {"fac2": 1.0, "nmse": 0.0, "effectif": 1}

    def test_sous_ensemble_metriques(self) -> None:
        """Given un sous-ensemble demande, When evaluation, Then lui seul."""
        resultat = evaluer_prediction(np.array([1.0]), np.array([2.0]), metriques=(NMSE,))
        assert resultat.metriques == {"nmse": 1.0}


class TestCommande:
    def test_main_auto_coherence(self) -> None:
        """Given le cas par defaut, When commande, Then FAC2 1 NMSE 0."""
        effectif = len(CAS_S0_DEFAUT.arcs) * len(CAS_S0_DEFAUT.positions_laterales)
        assert main() == {"fac2": 1.0, "nmse": 0.0, "effectif": effectif}

    def test_main_cas_explicite(self) -> None:
        """Given l identifiant S0 explicite, When commande, Then meme resultat."""
        assert main("S0") == main()

    def test_refuse_cas_inconnu(self) -> None:
        """Given un identifiant inconnu, When commande, Then refus."""
        with pytest.raises(ValueError, match="enregistres"):
            main("ZZ")

    def test_cout_inference_positif(self) -> None:
        """Given la verite S0, When mesure de cout, Then positif et fini."""
        cas = CAS_S0_DEFAUT
        points = cas.points()
        cout = mesurer_cout_inference(cas.verite, points)
        assert cout >= 0.0
        assert np.isfinite(cout)
