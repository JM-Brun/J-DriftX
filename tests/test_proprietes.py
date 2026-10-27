"""Propriétés générales des primitives, vérifiées sur des entrées générées.

Ces tests étendent aux entrées générées des propriétés déjà épinglées sur
des cas fixes (tests/test_metric.py : tests de propriétés analytiques des
PR #70 et #98). Chaque propriété reste énoncée sous les hypothèses exactes
de la primitive concernée : champ uniforme non nul pour la référence
dirigée, famille de similitude gaussienne pour le panache. Aucune de ces
propriétés ne constitue une validation physique.
"""

import math

import pytest

from hypothesis import given, settings
from hypothesis import strategies as st

from jdriftx.metric import pseudo_distance_uniforme
from jdriftx.similitude import concentration_panache


def _configurations_aval():
    """Génère (origine, vent, facteur) : b = a + facteur * vent est en aval.

    Le déplacement est construit colinéaire au vent : le produit scalaire
    (b - a) . u vaut facteur * ||u||^2, strictement positif et loin de la
    borne transversale (sensible à l'arrondi, voir contraintes-physiques).
    """
    return st.tuples(
        st.tuples(st.floats(-500.0, 500.0), st.floats(-500.0, 500.0)),
        st.tuples(st.floats(-10.0, 10.0), st.floats(-10.0, 10.0)).filter(
            lambda vent: abs(vent[0]) + abs(vent[1]) >= 0.5
        ),
        st.floats(0.1, 100.0),
    )


@settings(deadline=None)
@given(
    configuration=_configurations_aval(),
    translation=st.tuples(st.floats(-1000.0, 1000.0), st.floats(-1000.0, 1000.0)),
)
def test_pseudo_distance_invariante_par_translation(configuration, translation) -> None:
    """Translater la paire de points ne change pas le temps dirigé."""
    # Given — une paire aval b = a + facteur * vent.
    a, vent, facteur = configuration
    b = (a[0] + facteur * vent[0], a[1] + facteur * vent[1])
    # When — on translate les deux points du même vecteur.
    a_translate = (a[0] + translation[0], a[1] + translation[1])
    b_translate = (b[0] + translation[0], b[1] + translation[1])
    # Then — le temps dirigé est inchangé.
    direct = pseudo_distance_uniforme(a, b, vent)
    translate = pseudo_distance_uniforme(a_translate, b_translate, vent)
    assert direct == pytest.approx(translate)


@settings(deadline=None)
@given(configuration=_configurations_aval(), echelle=st.floats(0.5, 2.0))
def test_pseudo_distance_inverse_au_vent(configuration, echelle) -> None:
    """Multiplier le vent par c divise le temps dirigé par c."""
    # Given — une paire aval b = a + facteur * vent.
    a, vent, facteur = configuration
    b = (a[0] + facteur * vent[0], a[1] + facteur * vent[1])
    vent_fort = (vent[0] * echelle, vent[1] * echelle)
    # When — on renforce le vent d'un facteur c.
    reference = pseudo_distance_uniforme(a, b, vent)
    renforce = pseudo_distance_uniforme(a, b, vent_fort)
    # Then — le temps est divisé par c.
    assert renforce * echelle == pytest.approx(reference)


@settings(deadline=None)
@given(configuration=_configurations_aval())
def test_pseudo_distance_est_le_produit_adjoint(configuration) -> None:
    """Le temps dirigé vérifie l'identité de l'adjoint : tau = lambda . (b - a)."""
    # Given — une paire aval et l'adjoint exact lambda = u / ||u||^2.
    a, vent, facteur = configuration
    b = (a[0] + facteur * vent[0], a[1] + facteur * vent[1])
    norme2 = vent[0] ** 2 + vent[1] ** 2
    produit_adjoint = (vent[0] * (b[0] - a[0]) + vent[1] * (b[1] - a[1])) / norme2
    # When — on évalue la primitive.
    tau = pseudo_distance_uniforme(a, b, vent)
    # Then — l'identité de l'adjoint tient à la précision machine.
    assert tau == pytest.approx(produit_adjoint, rel=1e-12)


@settings(deadline=None)
@given(configuration=_configurations_aval())
def test_pseudo_distance_amont_est_infinie(configuration) -> None:
    """Une cible en amont reçoit le temps infini de la convention locale."""
    # Given — une cible amont b = a - facteur * vent.
    a, vent, facteur = configuration
    b_amont = (a[0] - facteur * vent[0], a[1] - facteur * vent[1])
    # When — on évalue la paire amont.
    tau = pseudo_distance_uniforme(a, b_amont, vent)
    # Then — la convention renvoie l'infini.
    assert math.isinf(tau)


@settings(deadline=None)
@given(q1=st.floats(0.01, 10.0), q2=st.floats(0.01, 10.0))
def test_panache_lineaire_en_debit(q1, q2) -> None:
    """La concentration du panache est linéaire en débit d'émission."""
    # Given — un point fixé du panache (classe D) et deux débits.
    # When — on évalue les deux débits et leur somme.
    c1 = concentration_panache(500.0, 30.0, 2.0, q1, 3.0, "D", 10.0)
    c2 = concentration_panache(500.0, 30.0, 2.0, q2, 3.0, "D", 10.0)
    c12 = concentration_panache(500.0, 30.0, 2.0, q1 + q2, 3.0, "D", 10.0)
    # Then — la superposition tient à la précision machine.
    assert float(c12) == pytest.approx(float(c1) + float(c2), rel=1e-12)


@settings(deadline=None)
@given(y=st.floats(-200.0, 200.0), classe=st.sampled_from(["A", "B", "C", "D", "E", "F"]))
def test_panache_positif_et_symetrique_en_y(y, classe) -> None:
    """Le panache est positif et symétrique par rapport à l'axe du vent."""
    # Given — un point latéral à la distance y de l'axe, pour chaque classe.
    # When — on évalue le point et son symétrique.
    c_y = concentration_panache(500.0, y, 2.0, 1.0, 3.0, classe, 10.0)
    c_symetrique = concentration_panache(500.0, -y, 2.0, 1.0, 3.0, classe, 10.0)
    # Then — les deux valeurs sont positives et identiques (y entre au carré).
    assert float(c_y) > 0.0
    assert float(c_y) == float(c_symetrique)
