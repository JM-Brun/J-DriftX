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
similitude gaussienne (Briggs, site rural) pour le panache.

L'extension du 29 octobre 2026 étend ces propriétés générées aux zones
couvertes jusque-là seulement par des cas fixes : métriques FAC2/NMSE et
cas S0 du registre de benchmarks (docs/39), partition 70/30 des jeux
synthétiques (docs/21), temps de première arrivée 1D (docs/27 et
docs/30), écarts-types de Briggs (docs/24) et solutions exactes de
référence (advection-diffusion 1D, transport périodique). Les standards
de test correspondants — ISO/IEC/IEEE 29119 pour le test logiciel,
Hypothesis pour les tests de propriété en Python — sont passés en revue
dans docs/40. La carte
notions / documentation / code est tenue dans docs/30 (section 9, « Carte
explicite ») et la matrice de traçabilité docs/27 ; pourquoi tester chaque
propriété séparément : docs/30, section 2. Aucune de ces propriétés ne
constitue une validation physique.

L'extension du 29 octobre (2e série) porte sur les objets d'exploration
interactifs de terrain.py et fields.py (recommandation P3 de la note 41) :
bornes, symétries et invariances de leurs formes fermées.
"""

import math

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from jdriftx.advection_diffusion import gaussian_advection_diffusion
from jdriftx.benchmarks.cas import CasS0
from jdriftx.benchmarks.metriques import fac2, nmse
from jdriftx.experiences.cas_synthetiques import FRACTION_CALIBRATION, construire_partition
from jdriftx.experiences.uniforme import ChampUniforme, ScenarioUniforme, resoudre_scenario
from jdriftx.fields import vector_field
from jdriftx.metric import temps_premiere_arrivee_1d
from jdriftx.periodic_transport import periodic_sine_solution
from jdriftx.similitude import concentration_panache, sigma_y, sigma_z
from jdriftx.source import SourcePanache
from jdriftx.stabilite import ClasseStabilite
from jdriftx.terrain import terrain_surface


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

    Référence : docs/30, section 1 — la construction T_proj uniforme ne dépend que
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
    T_proj n'est pas symétrique ; la convention amont +inf est une limite
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


@st.composite
def _verites_et_predictions(draw):
    """Génère un couple (vérité, prédiction) de même taille, vérité positive.

    La prédiction reste positive (ce sont des concentrations) mais sans
    lien imposé avec la vérité : les ratios visitent les deux côtés des
    bornes FAC2 (0,5 et 2).
    """
    taille = draw(st.integers(min_value=1, max_value=20))
    verite = draw(st.lists(st.floats(0.1, 10.0), min_size=taille, max_size=taille))
    prediction = draw(st.lists(st.floats(0.01, 20.0), min_size=taille, max_size=taille))
    return verite, prediction


@settings(deadline=None)
@given(verite=st.lists(st.floats(0.1, 10.0), min_size=1, max_size=20))
def test_fac2_nmse_identite_sur_prediction_parfaite(verite) -> None:
    """Une prédiction confondue avec la vérité reçoit FAC2 = 1 et NMSE = 0.

    Référence : contrôle d'auto-cohérence du pipeline de benchmarks (docs/39,
    section 4). Cas fixé voisin : le passage à vide de la commande dans
    tests/test_benchmarks_reference.py. Hypothèse : vérité strictement
    positive (conventions de l'issue #43).
    """
    # Given — une vérité positive et sa copie exacte.
    prediction = list(verite)
    # When — on évalue les deux métriques préenregistrées.
    # Then — FAC2 vaut 1 et NMSE vaut 0.
    assert fac2(verite, prediction) == pytest.approx(1.0)
    assert nmse(verite, prediction) == pytest.approx(0.0)


@settings(deadline=None)
@given(couple=_verites_et_predictions())
def test_fac2_nmse_restant_dans_leurs_bornes(couple) -> None:
    """FAC2 reste une fraction et NMSE reste positif ou nul, sans autre hypothèse.

    Référence : définitions préenregistrées (docs/39, section 3) : FAC2
    compte des points (fraction dans [0, 1]), NMSE est un rapport de carrés.
    Aucun rapport de qualité n'est affirmé ici.
    """
    verite, prediction = couple
    # Given — une vérité positive et une prédiction positive de même taille.
    # When — on évalue les deux métriques.
    valeur_fac2 = fac2(verite, prediction)
    valeur_nmse = nmse(verite, prediction)
    # Then — FAC2 est dans [0, 1] et NMSE est positif ou nul.
    assert 0.0 <= valeur_fac2 <= 1.0
    assert valeur_nmse >= 0.0


@settings(deadline=None)
@given(verite=st.lists(st.floats(0.1, 10.0), min_size=1, max_size=20))
def test_nmse_vaut_un_pour_le_double_exact(verite) -> None:
    """Prédire exactement le double de la vérité donne NMSE = 1 et FAC2 = 1.

    Référence : NMSE = somme((p - v)^2)/somme(v^2) (docs/39, section 3) :
    p = 2v donne numérateur = dénominateur. Le ratio 2v/v est exact en
    virgule flottante (2v est exact), donc la borne FAC2 incluse (ratio 2)
    ne dépend pas de l'arrondi.
    """
    # Given — une vérité positive et sa prédiction au double exact.
    prediction = [2.0 * v for v in verite]
    # When — on évalue les deux métriques.
    # Then — NMSE vaut exactement 1 et FAC2 vaut 1 (borne 2 incluse).
    assert nmse(verite, prediction) == pytest.approx(1.0)
    assert fac2(verite, prediction) == pytest.approx(1.0)


@st.composite
def _verites_et_ratios(draw):
    """Génère une vérité positive et des ratios prédiction/vérité bornés.

    Les ratios évitent une bande autour des bornes FAC2 (0,5 et 2) : une
    homothétie commune ne fait alors franchir aucune borne par arrondi,
    et FAC2 peut visiter 0 comme 1.
    """
    taille = draw(st.integers(min_value=1, max_value=20))
    plage_ratios = st.one_of(st.floats(0.3, 0.45), st.floats(0.55, 1.9), st.floats(2.1, 3.0))
    verite = draw(st.lists(st.floats(0.1, 10.0), min_size=taille, max_size=taille))
    ratios = draw(st.lists(plage_ratios, min_size=taille, max_size=taille))
    return verite, ratios


@settings(deadline=None)
@given(couple=_verites_et_ratios(), echelle=st.floats(0.5, 2.0))
def test_fac2_nmse_invariants_par_homothetie_commune(couple, echelle) -> None:
    """Mettre vérité et prédiction à la même échelle ne change ni FAC2 ni NMSE.

    Référence : FAC2 est un ratio point à point et NMSE un rapport de carrés
    (docs/39, section 3) : un changement d'unités commun ne doit rien
    changer. Les ratios évitent une bande autour des bornes FAC2 pour que
    la comparaison ne dépende pas d'un arrondi à la borne.
    """
    verite, ratios = couple
    # Given — une vérité, sa prédiction à ratios bornés, une échelle commune.
    prediction = [v * r for v, r in zip(verite, ratios, strict=True)]
    # When — on évalue les métriques, puis après homothétie commune.
    fac2_reference = fac2(verite, prediction)
    nmse_reference = nmse(verite, prediction)
    verite_echelle = [v * echelle for v in verite]
    prediction_echelle = [p * echelle for p in prediction]
    # Then — les deux métriques sont inchangées.
    assert fac2(verite_echelle, prediction_echelle) == pytest.approx(fac2_reference)
    assert nmse(verite_echelle, prediction_echelle) == pytest.approx(nmse_reference, rel=1e-9)


@st.composite
def _cas_s0(draw):
    """Génère des CasS0 valides : arcs croissants, positions et physiques bornées.

    Les arcs sont tirés comme un ensemble (unicité) puis triés (ordre
    croissant strict du contrat) ; les plages bornées contiennent le coût
    de la CI.
    """
    nombre_arcs = draw(st.integers(min_value=1, max_value=6))
    arcs_tires = draw(st.sets(st.floats(100.0, 2000.0), min_size=nombre_arcs, max_size=nombre_arcs))
    positions = draw(st.lists(st.floats(-100.0, 100.0), min_size=1, max_size=5))
    return CasS0(
        source=SourcePanache(
            debit=draw(st.floats(0.1, 5.0)),
            u=draw(st.floats(0.5, 10.0)),
            classe=draw(st.sampled_from(tuple(ClasseStabilite))),
            hauteur=draw(st.floats(0.0, 50.0)),
        ),
        arcs=tuple(sorted(arcs_tires)),
        positions_laterales=tuple(positions),
        z_mesure=draw(st.floats(0.0, 20.0)),
    )


@settings(deadline=None)
@given(cas=_cas_s0())
def test_cas_s0_grille_croisee_et_verite_positive(cas) -> None:
    """Tout cas S0 valide expose la grille croisée et une vérité strictement positive.

    Référence : contrat CasSynthetique (docs/39, section 1) — grille non
    vide, vérité strictement positive. Le cas n'est ici pas enregistré :
    la propriété porte sur l'objet lui-même, l'enregistrement ne fait que
    la vérifier une fois de plus.
    """
    # Given — un cas S0 valide généré (arcs croissants, positions libres).
    # When — on construit la grille et la vérité du cas.
    points = cas.points()
    verite = cas.verite(points)
    # Then — la grille est le produit arcs x positions et la vérité est positive.
    assert len(points) == len(cas.arcs) * len(cas.positions_laterales)
    assert all(p.z == cas.z_mesure for p in points)
    assert np.all(verite > 0.0)


@settings(deadline=None)
@given(
    nombre_points=st.integers(min_value=2, max_value=300),
    graine=st.integers(min_value=0, max_value=10**9),
)
def test_partition_s0_couvrante_et_disjointe(nombre_points, graine) -> None:
    """La partition S0 est couvrante et disjointe pour toute taille et graine.

    Référence : invariants de PartitionS0 (docs/21, famille S0) :
    calibration et évaluation sont disjointes et couvrent tous les
    indices. Cas fixé voisin : tests/test_cas_synthetiques.py.
    """
    # Given — un jeu de n points et une graine quelconques.
    # When — on construit la partition figée 70/30.
    partition = construire_partition(nombre_points, graine)
    # Then — la réunion couvre tous les indices, sans recouvrement.
    reunion = partition.calibration + partition.evaluation
    assert sorted(reunion) == list(range(nombre_points))
    assert not set(partition.calibration) & set(partition.evaluation)
    assert len(partition.calibration) == int(FRACTION_CALIBRATION * nombre_points)


@settings(deadline=None)
@given(a=st.floats(-1000.0, 1000.0), b=st.floats(-1000.0, 1000.0), vitesse=st.floats(-10.0, 10.0))
def test_temps_premiere_arrivee_symetrique_par_inversion(a, b, vitesse) -> None:
    """Inverser le trajet et la vitesse échange aval et amont sans changer le temps.

    Référence : la dynamique constante dx/dt = v (docs/27, ligne T_arr 1D)
    donne t(a, b, v) = t(b, a, -v), l'infini compris : les conventions
    d'inaccessibilité se correspondent. Cas fixé voisin : les propriétés
    analytiques de tests/test_metric.py (PR #70 et #98).
    """
    # Given — un trajet a -> b et la même dynamique inversée.
    # When — on évalue les deux sens de parcours.
    direct = temps_premiere_arrivee_1d(a, b, vitesse)
    inverse = temps_premiere_arrivee_1d(b, a, -vitesse)
    # Then — les deux temps coïncident (l'infini compris).
    assert direct == pytest.approx(inverse)


@settings(deadline=None)
@given(a=st.floats(-1000.0, 1000.0), b=st.floats(-1000.0, 1000.0), vitesse=st.floats(0.01, 10.0))
def test_temps_premiere_arrivee_exact_en_aval(a, b, vitesse) -> None:
    """En vent algébrique positif : temps exact en aval, infini en amont, zéro à la source.

    Référence : docs/27 (ligne T_arr 1D) et la convention d'inaccessibilité
    du module metric (docstring). Hypothèse : vitesse strictement
    positive ; le trajet est en aval ou en amont selon le signe du
    déplacement.
    """
    # Given — un trajet et un vent algébrique strictement positifs.
    deplacement = b - a
    # When — on évalue le temps de première arrivée.
    temps = temps_premiere_arrivee_1d(a, b, vitesse)
    # Then — aval : distance sur vitesse ; amont : infini ; source : zéro.
    if deplacement > 0.0:
        assert temps == pytest.approx(deplacement / vitesse)
    elif deplacement < 0.0:
        assert math.isinf(temps)
    else:
        assert temps == 0.0


@settings(deadline=None)
@given(x=st.floats(1.0, 10000.0), classe=st.sampled_from(tuple(ClasseStabilite)))
def test_sigma_strictement_positifs(x, classe) -> None:
    """Les écarts-types de Briggs sont strictement positifs à toute distance utile.

    Référence : les trois formes de docs/24 (linéaire, racine, rationnel)
    multiplient la distance par des coefficients strictement positifs
    (ClasseStabilite, source unique de vérité). Cas fixé voisin :
    tests/test_stabilite.py et tests/test_similitude.py.
    """
    # Given — une distance sous le vent strictement positive, pour chaque classe.
    # When — on évalue les deux écarts-types.
    # Then — chacun est strictement positif.
    assert float(sigma_y(x, classe)) > 0.0
    assert float(sigma_z(x, classe)) > 0.0


@settings(deadline=None)
@given(
    x1=st.floats(1.0, 5000.0),
    avancee=st.floats(1.0, 5000.0),
    classe=st.sampled_from(tuple(ClasseStabilite)),
)
def test_sigma_strictement_croissants(x1, avancee, classe) -> None:
    """Le panache s'élargit : les écarts-types croissent strictement avec la distance.

    Référence : les trois formes de docs/24 dérivent en des expressions
    strictement positives (coefficients strictement positifs) ; l'avancée
    d'au moins 1 m écarte les deux distances au-delà de l'arrondi. Cas
    fixé voisin : tests/test_stabilite.py.
    """
    # Given — deux distances sous le vent séparées d'au moins 1 m.
    x2 = x1 + avancee
    # When — on évalue les écarts-types aux deux distances.
    # Then — chacun croît strictement.
    assert sigma_y(x1, classe) < sigma_y(x2, classe)
    assert sigma_z(x1, classe) < sigma_z(x2, classe)


@settings(deadline=None)
@given(
    temps=st.floats(0.0, 100.0),
    centre_initial=st.floats(-50.0, 50.0),
    vitesse=st.floats(-5.0, 5.0),
    diffusivite=st.floats(0.0, 1.0),
    sigma_initial=st.floats(0.1, 2.0),
)
def test_gaussienne_1d_pic_central_et_symetrie(
    temps, centre_initial, vitesse, diffusivite, sigma_initial
) -> None:
    """La gaussienne 1D garde son pic au centre advecté et sa symétrie autour de lui.

    Référence : solution exacte de advection_diffusion (docstring du
    module) : centre = x0 + u·t et variance = sigma0² + 2·K·t ; le pic
    vaut masse sur racine de (2·pi·variance). Cas fixé voisin :
    tests/test_advection_diffusion.py.
    """
    # Given — les paramètres, le centre advecté et la variance attendue.
    centre = centre_initial + vitesse * temps
    variance = sigma_initial**2 + 2.0 * diffusivite * temps
    abcisses = np.asarray([centre - 1.0, centre, centre + 1.0])
    # When — on évalue la solution exacte aux trois points.
    concentrations = gaussian_advection_diffusion(
        abcisses,
        temps,
        mass=2.0,
        initial_center=centre_initial,
        velocity=vitesse,
        diffusivity=diffusivite,
        initial_sigma=sigma_initial,
    )
    # Then — le pic est au centre, symétrique, à la valeur attendue.
    assert concentrations[1] > concentrations[0]
    assert concentrations[0] == pytest.approx(concentrations[2], rel=1e-9)
    assert concentrations[1] == pytest.approx(2.0 / math.sqrt(2.0 * math.pi * variance), rel=1e-9)


@st.composite
def _parametres_periodiques(draw):
    """Génère (moyenne, amplitude) avec moyenne positive et amplitude dans [0, moyenne].

    Le profil reste ainsi non négatif, condition d'admission de la solution
    exacte (docstring du module periodic_transport).
    """
    moyenne = draw(st.floats(1.0, 10.0))
    fraction = draw(st.floats(0.0, 1.0))
    return moyenne, fraction * moyenne


@settings(deadline=None)
@given(
    couple=_parametres_periodiques(),
    temps=st.floats(0.0, 50.0),
    longueur=st.floats(1.0, 100.0),
    vitesse=st.floats(-5.0, 5.0),
    diffusivite=st.floats(0.0, 1.0),
)
def test_sine_periodique_bornee_et_periodique(
    couple, temps, longueur, vitesse, diffusivite
) -> None:
    """La solution sinusoïdale périodique reste dans son enveloppe et est périodique en espace.

    Référence : moyenne + amplitude·exp(-K k² t)·sin(k (x - u t)), k = 2
    pi / L (docstring du module periodic_transport) : l'enveloppe est
    [moyenne - amplitude·amortissement, moyenne + amplitude·amortissement]
    et la solution est L-périodique en espace. Les solveurs itératifs du
    module restent exclus : leur stabilité numérique n'est pas une
    propriété de la solution exacte.
    """
    moyenne, amplitude = couple
    # Given — une grille couvrant un domaine périodique complet [0, L].
    abcisses = np.linspace(0.0, longueur, 41)
    # When — on évalue la solution exacte et son amortissement attendu.
    concentrations = periodic_sine_solution(
        abcisses,
        temps,
        length=longueur,
        mean_concentration=moyenne,
        amplitude=amplitude,
        velocity=vitesse,
        diffusivity=diffusivite,
    )
    nombre_d_onde = 2.0 * math.pi / longueur
    amortissement = math.exp(-diffusivite * nombre_d_onde**2 * temps)
    # Then — l'enveloppe tient et les extrémités du domaine coïncident.
    assert np.all(concentrations >= moyenne - amplitude * amortissement - 1e-9)
    assert np.all(concentrations <= moyenne + amplitude * amortissement + 1e-9)
    assert concentrations[0] == pytest.approx(concentrations[-1], abs=1e-9)


@settings(deadline=None)
@given(
    deplacements=st.lists(st.floats(-20.0, 20.0), min_size=1, max_size=8),
    hauteur=st.floats(-10.0, 10.0),
    largeur=st.floats(0.1, 5.0),
    centre_x=st.floats(-50.0, 50.0),
    centre_y=st.floats(-50.0, 50.0),
)
def test_terrain_plat_est_nul(deplacements, hauteur, largeur, centre_x, centre_y) -> None:
    """Le terrain plat est identiquement nul, quels que soient ses paramètres.

    Référence : la forme "flat" de terrain_surface (src/jdriftx/terrain.py)
    ne dépend ni de la hauteur ni de la largeur. Cas fixé voisin :
    tests/test_terrain.py. Ces surfaces sont des exemples d'enseignement,
    pas de la topographie mesurée.
    """
    # Given — des points quelconques autour du centre, paramètres libres.
    abcisses = np.asarray([centre_x + valeur for valeur in deplacements])
    ordonnees = np.asarray([centre_y - valeur for valeur in deplacements])
    # When — on évalue la surface plate.
    surface = terrain_surface(
        abcisses,
        ordonnees,
        "flat",
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    # Then — toutes les valeurs sont exactement nulles.
    assert np.all(surface == 0.0)


@settings(deadline=None)
@given(
    forme=st.sampled_from(["hill", "valley", "ridge"]),
    hauteur=st.floats(-10.0, 10.0),
    largeur=st.floats(0.1, 5.0),
    dx=st.floats(-30.0, 30.0),
    dy=st.floats(-30.0, 30.0),
    centre_x=st.floats(-50.0, 50.0),
    centre_y=st.floats(-50.0, 50.0),
)
def test_terrain_borne_par_hauteur(forme, hauteur, largeur, dx, dy, centre_x, centre_y) -> None:
    """Toute surface synthétique non plate est bornée par la hauteur absolue.

    Référence : les formes "hill", "valley" et "ridge" de terrain_surface
    multiplient la hauteur par une exponentielle d'un réel négatif : la
    valeur absolue de l'altitude reste sous la valeur absolue de la hauteur.
    """
    # Given — un point quelconque et des paramètres finis.
    abcisses = np.asarray([centre_x + dx])
    ordonnees = np.asarray([centre_y + dy])
    # When — on évalue la surface.
    surface = terrain_surface(
        abcisses,
        ordonnees,
        forme,
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    # Then — l'altitude est bornée par la valeur absolue de la hauteur.
    assert np.all(np.abs(surface) <= abs(hauteur))


@settings(deadline=None)
@given(
    hauteur=st.floats(-10.0, 10.0),
    largeur=st.floats(0.1, 5.0),
    dx=st.floats(-30.0, 30.0),
    dy=st.floats(-30.0, 30.0),
    centre_x=st.floats(-50.0, 50.0),
    centre_y=st.floats(-50.0, 50.0),
)
def test_terrain_colline_symetrique(hauteur, largeur, dx, dy, centre_x, centre_y) -> None:
    """La colline est symétrique par rapport à son centre en x et en y.

    Référence : la forme "hill" ne dépend que de la somme des carrés des
    écarts au centre ; le point symétrique a la même altitude à
    l'arrondi près : l'écart recalculé (centre + déplacement) - centre
    n'est pas exact en virgule flottante, l'égalité est donc relative.
    """
    # Given — un point et son symétrique par rapport au centre.
    x_plus = np.asarray([centre_x + dx])
    y_plus = np.asarray([centre_y + dy])
    x_moins = np.asarray([centre_x - dx])
    y_moins = np.asarray([centre_y - dy])
    # When — on évalue la colline aux deux points.
    altitude_plus = terrain_surface(
        x_plus,
        y_plus,
        "hill",
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    altitude_moins = terrain_surface(
        x_moins,
        y_moins,
        "hill",
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    # Then — les deux altitudes coïncident à l'arrondi près.
    assert altitude_plus[0] == pytest.approx(altitude_moins[0], rel=1e-12)


@settings(deadline=None)
@given(
    hauteur=st.floats(1.0, 10.0),
    largeur=st.floats(0.1, 5.0),
    x1=st.floats(-50.0, 50.0),
    x2=st.floats(-50.0, 50.0),
    y=st.floats(-50.0, 50.0),
    centre_x=st.floats(-20.0, 20.0),
    centre_y=st.floats(-20.0, 20.0),
)
def test_terrain_crete_invariante_en_x(hauteur, largeur, x1, x2, y, centre_x, centre_y) -> None:
    """La crête ne dépend pas de la coordonnée longitudinale.

    Référence : la forme "ridge" ne dépend que de l'écart transversal au
    carré : deux points de même ordonnée ont la même altitude, quelle que
    soit leur abscisse.
    """
    # Given — deux abscisses quelconques et une même ordonnée.
    # When — on évalue la crête aux deux points.
    altitude_1 = terrain_surface(
        np.asarray([x1]),
        np.asarray([y]),
        "ridge",
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    altitude_2 = terrain_surface(
        np.asarray([x2]),
        np.asarray([y]),
        "ridge",
        height=hauteur,
        width=largeur,
        center_x=centre_x,
        center_y=centre_y,
    )
    # Then — les deux altitudes coïncident exactement.
    assert altitude_1[0] == altitude_2[0]


@settings(deadline=None)
@given(
    vitesse=st.floats(-5.0, 5.0).filter(lambda valeur: abs(valeur) >= 0.1),
    angle_degres=st.floats(-180.0, 180.0),
)
def test_champ_uniforme_est_constant(vitesse, angle_degres) -> None:
    """Le champ uniforme a les mêmes composantes exactes en tout point.

    Référence : la forme "uniform" de vector_field (src/jdriftx/fields.py) :
    u = vitesse*cos(angle) et v = vitesse*sin(angle), indépendants du point
    évalué. Cas fixé voisin : tests/test_fields.py.
    """
    # Given — deux points éloignés de la grille.
    u_proche, v_proche = vector_field(
        np.asarray([0.0]), np.asarray([0.0]), "uniform", speed=vitesse, angle_deg=angle_degres
    )
    u_loin, v_loin = vector_field(
        np.asarray([123.4]), np.asarray([-456.7]), "uniform", speed=vitesse, angle_deg=angle_degres
    )
    # When — on forme les composantes attendues.
    angle = math.radians(angle_degres)
    # Then — le champ est constant et égal aux composantes attendues.
    assert u_proche[0] == u_loin[0]
    assert v_proche[0] == v_loin[0]
    assert u_proche[0] == pytest.approx(vitesse * math.cos(angle), rel=1e-12)
    assert v_proche[0] == pytest.approx(vitesse * math.sin(angle), rel=1e-12)


@settings(deadline=None)
@given(
    vitesse=st.floats(-5.0, 5.0).filter(lambda valeur: abs(valeur) >= 0.1),
    angle_degres=st.floats(-180.0, 180.0),
    cisaillement=st.floats(-2.0, 2.0).filter(lambda valeur: abs(valeur) >= 0.05),
    y1=st.floats(-50.0, 50.0),
    y2=st.floats(-50.0, 50.0),
)
def test_champ_cisaille_est_lineaire_en_y(vitesse, angle_degres, cisaillement, y1, y2) -> None:
    """Le champ cisaillé garde v constant et u linéaire en ordonnée.

    Référence : la forme "shear" : u = vitesse*cos(angle) + cisaillement*y
    et v = vitesse*sin(angle). Entre deux points de même abscisse,
    u(y2) - u(y1) vaut exactement cisaillement*(y2 - y1).
    """
    # Given — deux points de même abscisse à des ordonnées quelconques.
    u1, v1 = vector_field(
        np.asarray([10.0]),
        np.asarray([y1]),
        "shear",
        speed=vitesse,
        angle_deg=angle_degres,
        shear=cisaillement,
    )
    u2, v2 = vector_field(
        np.asarray([10.0]),
        np.asarray([y2]),
        "shear",
        speed=vitesse,
        angle_deg=angle_degres,
        shear=cisaillement,
    )
    # When — on compare les deux évaluations.
    # Then — v est identique et u croît du gradient attendu.
    assert v1[0] == v2[0]
    assert (u2[0] - u1[0]) == pytest.approx(cisaillement * (y2 - y1), rel=1e-9, abs=1e-12)


@settings(deadline=None)
@given(
    force=st.floats(-3.0, 3.0).filter(lambda valeur: abs(valeur) >= 0.05),
    x=st.floats(-50.0, 50.0),
    y=st.floats(-50.0, 50.0),
)
def test_champ_radial_est_colineaire_au_rayon(force, x, y) -> None:
    """Le champ radial est partout colinéaire au rayon vecteur.

    Référence : la forme "radial" : (u, v) = force*(x, y) : le produit
    vectoriel u*y - v*x est nul et la norme du champ vaut |force| fois la
    norme du rayon. Le sens (source ou puits) suit le signe de force.
    """
    # Given — un point quelconque du plan.
    u, v = vector_field(np.asarray([x]), np.asarray([y]), "radial", radial_strength=force)
    # When — on forme le produit vectoriel et la norme du champ.
    produit_vectoriel = float(u[0]) * y - float(v[0]) * x
    norme_champ = math.hypot(float(u[0]), float(v[0]))
    # Then — colinéarité et norme attendue, au sens près.
    assert produit_vectoriel == pytest.approx(0.0, abs=1e-9)
    assert norme_champ == pytest.approx(abs(force) * math.hypot(x, y), rel=1e-9)
