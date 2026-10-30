"""Tests des contraintes physiques."""

import numpy as np
import pytest

from jdriftx.constraints import linearite, linearite_panache, positivite
from jdriftx.similitude import concentration_panache
from jdriftx.stabilite import ClasseStabilite


def test_positivite_ok() -> None:
    """Un champ partout positif satisfait la contrainte de positivité."""
    # Given — un champ de concentration partout positif.
    champ = np.linspace(0.0, 1.0, 10)
    # When / Then — la contrainte est satisfaite.
    assert positivite(champ)


def test_positivite_echouee() -> None:
    """Un champ prenant des valeurs négatives viole la contrainte."""
    # Given — un champ prenant des valeurs négatives.
    champ = np.linspace(-1.0, 1.0, 10)
    # When / Then — la contrainte est violée.
    assert not positivite(champ)


def test_superposition_panache() -> None:
    """Le panache gaussien est lineaire en debit : multi-sources garanti."""
    # Given — un point du domaine et deux débits d'émission différents.
    point = (500.0, 25.0, 2.0)
    # When / Then — la linéarité en débit est vérifiée au point donné.
    assert linearite(
        concentration_panache,
        point,
        q1=1.0,
        q2=2.5,
        u=3.0,
        classe="D",
        hauteur=10.0,
    )


def test_linearite_panache_typee_verifie_la_superposition() -> None:
    """La variante typée linearite_panache établit la même linéarité en débit."""
    # Given — un point du domaine et deux débits d'émission différents.
    point = (500.0, 25.0, 2.0)
    # When / Then — la linéarité en débit est vérifiée via la signature typée.
    assert linearite_panache(point, 1.0, 2.5, u=3.0, classe="D", hauteur=10.0)


def test_linearite_panache_accepte_enum() -> None:
    """ClasseStabilite.D est accepté en place de la lettre "D"."""
    # Given — un point du domaine et la classe D passée comme objet.
    point = (500.0, 25.0, 2.0)
    # When / Then — la superposition est vérifiée avec l'enum.
    assert linearite_panache(point, 1.0, 2.0, u=3.0, classe=ClasseStabilite.D)


def test_linearite_panache_rejette_classe_inconnue() -> None:
    """Une classe inconnue propage l'erreur historique de concentration_panache."""
    # Given — une classe de stabilité inexistante.
    point = (500.0, 25.0, 2.0)
    # When / Then — l'erreur historique est levée à l'évaluation du modèle.
    with pytest.raises(ValueError, match="Classe de stabilite inconnue"):
        linearite_panache(point, 1.0, 2.5, u=3.0, classe="X")


@pytest.mark.parametrize("tolerance", [-1e-12, float("inf"), float("nan")])
def test_positivite_rejette_une_tolerance_invalide(tolerance: float) -> None:
    """Une tolérance négative ou non finie est refusée."""
    # Given — un champ positif et une tolérance invalide.
    champ = np.linspace(0.0, 1.0, 10)
    # When / Then — l'appel est refusé avant la vérification.
    with pytest.raises(ValueError, match="tolerance"):
        positivite(champ, tol=tolerance)


def test_positivite_rejette_une_tolerance_booleenne() -> None:
    """Un booléen en tolérance est refusé, conformément à la charte qualité."""
    # Given — un champ positif et la valeur True.
    champ = np.linspace(0.0, 1.0, 10)
    # When / Then — l'appel est refusé avant la vérification.
    with pytest.raises(ValueError, match="booleen exclu"):
        positivite(champ, tol=True)
