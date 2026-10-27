"""Propriétés générales vérifiées sur des entrées générées (hypothesis).

Ces tests étendent aux entrées générées des propriétés déjà épinglées sur
des cas fixes — tests/test_metric.py (propriétés analytiques des PR #70 et
#98, adjoint de docs/26) et tests/test_similitude.py (superposition,
symétrie latérale, bilans de masse). Ils évaluent les objets réellement
exposés par le package — ChampUniforme et ScenarioUniforme (expérience
« champ uniforme », action 5 de la feuille de route) et ClasseStabilite
(docs/24, source unique de vérité) — plutôt que des tuples et des chaînes
littérales : la propriété tient sur l'objet si et seulement si elle tient
sur la primitive, puisque l'expérience délègue à pseudo_distance_uniforme
sans recalcul local.

Chaque propriété reste énoncée sous les hypothèses exactes de l'objet
concerné : champ uniforme non nul pour la référence dirigée, famille de
similitude gaussienne (Briggs, site rural) pour le panache. La carte
notions / documentation / code est tenue dans docs/30 (section 9, « Carte
explicite ») et la matrice de traçabilité docs/27 ; pourquoi tester chaque
propriété séparément : docs/30, section 2. Aucune de ces propriétés ne
constitue une validation physique.
"""

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from jdriftx.experiences.uniforme import ChampUniforme, ScenarioUniforme, resoudre_scenario
from jdriftx.similitude import concentration_panache
from jdriftx.stabilite import ClasseStabilite


def _vents_non_nuls():
    """Vents 2D de composantes bornées, de norme strictement positive.

    La borne en norme 1 (au moins 0.5) écarte le régime |u| -> 0 et la
    borne transversale, où la convention logicielle n'est pas
    différentiable (docs/26, section 3.3 ; site/theorie/contraintes-physiques.qmd).
    """
    return st.tuples(st.floats(-10.0, 10.0), st.floats(-10.0, 10.0)).filter(
        lambda composantes: abs(composantes[0]) + abs(composantes[1]) >= 0.5
    )


@st.composite
def _scenarios_aval(draw):
    """Génère des ScenarioUniforme dont la cible est en aval de l'origine.

    Le déplacement est construit colinéaire au vent : (cible - origine) . vent
    vaut facteur * ||vent||^2, strictement positif et loin de la borne
    transversale (sensible à l'arrondi, voir contraintes-physiques.qmd).
    """
    origine = draw(st.tuples(st.floats(-500.0, 500.0), st.floats(-500.0, 500.0)))
    champ = ChampUniforme(vent=draw(_vents_non_nuls()))
    facteur = draw(st.floats(0.1, 100.0))
    cible = (origine[0] + facteur * champ.vent[0], origine[1] + facteur * champ.vent[1])
    return ScenarioUniforme(champ=champ, origine=origine, cible=cible)


@settings(deadline=None)
@given(
    scenario=_scenarios_aval(),
    translation=st.tuples(st.floats(-1000.0, 1000.0), st.floats(-1000.0, 1000.0)),
)
def test_temps_dirige_invariant_par_translation(scenario, translation) -> None:
    """Translater origine et cible ne change pas le temps dirigé.

    Référence : docs/30, section 1 — la V2 uniforme projetée ne dépend que
    du déplacement cible - origine (carte de la section 9). Cas fixé
    voisin : test_uniform_pseudodistance_is_rotation_invariant dans
    tests/test_metric.py. Hypothèse : champ uniforme indépendant du temps.
    """
    # Given — un scénario validé, dont la cible est en aval.
    # When — on translate origine et cible du même vecteur.
    dx, dy = translation
    scenario_translate = ScenarioUniforme(
        champ=scenario.champ,
        origine=(scenario.origine[0] + dx, scenario.origine[1] + dy),
        cible=(scenario.cible[0] + dx, scenario.cible[1] + dy),
    )
    # Then — le temps dirigé origine -> cible est inchangé.
    direct = resoudre_scenario(scenario).tau_origine_cible
    translate = resoudre_scenario(scenario_translate).tau_origine_cible
    assert direct == pytest.approx(translate)


@settings(deadline=None)
@given(scenario=_scenarios_aval(), echelle=st.floats(0.5, 2.0))
def test_temps_dirige_inverse_au_vent(scenario, echelle) -> None:
    """Multiplier le vent par c > 0 divise le temps dirigé par c.

    Référence : docs/26, section 3.2 (contrôle d'homogénéité :
    tau(a, b, alpha * u) = tau(a, b, u) / alpha). Cas fixé voisin :
    test_uniform_pseudodistance_scales_inversely_with_wind_magnitude dans
    tests/test_metric.py. Hypothèse : une homothétie positive du vent
    préserve l'aval.
    """
    # Given — un scénario aval et le même champ renforcé d'un facteur c.
    vent_renforce = (scenario.champ.vent[0] * echelle, scenario.champ.vent[1] * echelle)
    scenario_renforce = ScenarioUniforme(
        champ=ChampUniforme(vent=vent_renforce),
        origine=scenario.origine,
        cible=scenario.cible,
    )
    # When — on évalue les deux champs.
    reference = resoudre_scenario(scenario).tau_origine_cible
    renforce = resoudre_scenario(scenario_renforce).tau_origine_cible
    # Then — le temps est divisé par c.
    assert renforce * echelle == pytest.approx(reference)


@settings(deadline=None)
@given(scenario=_scenarios_aval())
def test_temps_dirige_est_le_produit_adjoint(scenario) -> None:
    """Le temps dirigé vérifie l'identité de l'adjoint : tau = lambda . d.

    Référence : docs/26, sections 3.1 et 3.2 — l'adjoint exact de la
    référence uniforme est lambda = u / (u . u) et tau = lambda . d sur
    le demi-plan aval ouvert. Cas fixé voisin :
    test_uniform_pseudodistance_is_adjoint_vector_dot_displacement dans
    tests/test_metric.py (différences finies : docs/26, section 3.4).
    """
    # Given — un scénario aval et l'adjoint exact lambda = u / ||u||^2.
    vent = scenario.champ.vent
    dx = scenario.cible[0] - scenario.origine[0]
    dy = scenario.cible[1] - scenario.origine[1]
    produit_adjoint = (vent[0] * dx + vent[1] * dy) / scenario.champ.norme**2
    # When — on évalue le scénario (norme : propriété de ChampUniforme).
    tau = resoudre_scenario(scenario).tau_origine_cible
    # Then — l'identité de l'adjoint tient à la précision machine.
    assert tau == pytest.approx(produit_adjoint, rel=1e-12)


@settings(deadline=None)
@given(scenario=_scenarios_aval())
def test_cible_amont_temps_infini(scenario) -> None:
    """Une cible en amont reçoit le temps infini de la convention locale.

    Référence : docs/30, section 9 (« Atteignabilité et temps infini ») —
    V2 n'est pas symétrique ; la convention amont +inf est une limite
    documentée du manifeste de l'expérience champ uniforme. Cas fixé
    voisin : test_uniform_pseudodistance_is_infinite_upwind dans
    tests/test_metric.py.
    """
    # Given — un scénario aval : l'origine est en amont de la cible.
    # When — on évalue le sens cible -> origine.
    resultat = resoudre_scenario(scenario)
    # Then — la convention renvoie l'infini.
    assert math.isinf(resultat.tau_cible_origine)


@settings(deadline=None)
@given(q1=st.floats(0.01, 10.0), q2=st.floats(0.01, 10.0))
def test_panache_lineaire_en_debit(q1, q2) -> None:
    """La concentration du panache est linéaire en débit d'émission.

    Référence : le débit d'émission entre linéairement dans la solution de
    similitude (src/jdriftx/similitude.py) ; superposition épinglée dans
    tests/test_similitude.py et tests/test_constraints.py (bilans de masse
    multi-configurations). La classe D est l'objet ClasseStabilite.D
    (docs/24, section 4 : source unique de vérité).
    """
    # Given — un point fixé du panache (objet ClasseStabilite.D) et deux débits.
    # When — on évalue les deux débits et leur somme.
    c1 = concentration_panache(500.0, 30.0, 2.0, q1, 3.0, ClasseStabilite.D, 10.0)
    c2 = concentration_panache(500.0, 30.0, 2.0, q2, 3.0, ClasseStabilite.D, 10.0)
    c12 = concentration_panache(500.0, 30.0, 2.0, q1 + q2, 3.0, ClasseStabilite.D, 10.0)
    # Then — la superposition tient à la précision machine.
    assert float(c12) == pytest.approx(float(c1) + float(c2), rel=1e-12)


@settings(deadline=None)
@given(
    y=st.floats(-200.0, 200.0),
    classe=st.sampled_from(tuple(ClasseStabilite)),
)
def test_panache_positif_et_symetrique_en_y(y, classe) -> None:
    """Le panache est positif et symétrique par rapport à l'axe du vent.

    Référence : la coordonnée latérale n'entre que par son carré dans la
    solution gaussienne (src/jdriftx/similitude.py) ; cas fixé voisin :
    test_symetrie_laterale dans tests/test_similitude.py. Les classes
    sont tirées des membres de l'objet ClasseStabilite (docs/24,
    sections 2 et 4), pas de chaînes littérales.
    """
    # Given — un point latéral à la distance y de l'axe, pour chaque objet classe.
    # When — on évalue le point et son symétrique.
    c_y = concentration_panache(500.0, y, 2.0, 1.0, 3.0, classe, 10.0)
    c_symetrique = concentration_panache(500.0, -y, 2.0, 1.0, 3.0, classe, 10.0)
    # Then — les deux valeurs sont positives et identiques (y entre au carré).
    assert float(c_y) > 0.0
    assert float(c_y) == float(c_symetrique)
