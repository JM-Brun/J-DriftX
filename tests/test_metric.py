"""Tests de la metrique des temps de transport."""

import numpy as np
import pytest

from jdriftx.metric import temps_transport


def test_vent_uniforme() -> None:
    """Vent uniforme : le temps de transport vaut longueur / vitesse."""
    ligne = np.array([[0.0, 0.0], [300.0, 0.0]])
    vent = np.array([[3.0, 0.0]])
    assert temps_transport(ligne, vent) == pytest.approx(100.0)


def test_non_symetrie() -> None:
    """Avec le vent, aller de A a B est plus rapide que de B a A."""
    a_vers_b = np.array([[0.0, 0.0], [100.0, 0.0]])
    b_vers_a = np.array([[100.0, 0.0], [0.0, 0.0]])
    vent_portant = np.array([[5.0, 0.0]])
    vent_oppose = np.array([[-5.0, 0.0]])
    tau_ab = temps_transport(a_vers_b, vent_portant)
    tau_ba = temps_transport(b_vers_a, vent_oppose)
    # En module le temps est identique ici ; la non-symetrie vient des
    # longueurs de trajet dans un champ non uniforme (voir test suivant).
    assert tau_ab == pytest.approx(tau_ba)


def test_non_symetrie_champ_non_uniforme() -> None:
    """Trajets physiques distincts : le temps depend du chemin, pas de la corde."""
    # Chemin 1 : direct.
    ligne1 = np.array([[0.0, 0.0], [100.0, 0.0]])
    # Chemin 2 : detour par une zone ou le vent est fort.
    ligne2 = np.array([[0.0, 0.0], [50.0, 50.0], [100.0, 0.0]])
    vent_fort = np.array([[10.0, 0.0]])
    vent_detour = np.array([[10.0, 0.0], [10.0, 0.0]])
    tau_direct = temps_transport(ligne1, vent_fort)
    tau_detour = temps_transport(ligne2, vent_detour)
    assert tau_detour > tau_direct


def test_formes_incoherentes() -> None:
    with pytest.raises(ValueError, match="doit etre un tableau"):
        temps_transport(np.zeros((1, 2)), np.zeros((1, 2)))


def test_vent_trop_faible() -> None:
    ligne = np.array([[0.0, 0.0], [10.0, 0.0]])
    vent = np.array([[0.05, 0.0]])
    with pytest.raises(ValueError, match="umin"):
        temps_transport(ligne, vent)
