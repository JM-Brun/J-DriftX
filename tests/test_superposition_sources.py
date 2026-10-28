"""Tests de la tranche verticale superposition de deux sources (figure 4)."""

import json
import math
from dataclasses import FrozenInstanceError, replace

import pytest

from jdriftx.experiences.reconstruction_vent import Rectangle
from jdriftx.experiences.superposition_sources import (
    SCENARIO_DEFAUT,
    ScenarioSuperposition,
    SourceGaussienne,
    construire_manifeste,
    resoudre_scenario,
)


def _scenario_modifie(**changements: object) -> ScenarioSuperposition:
    """Renvoie le scénario par défaut avec des champs remplacés."""
    return replace(SCENARIO_DEFAUT, **changements)


def test_le_scenario_defaut_exige_trois_mesures() -> None:
    """Le scénario par défaut est constructible avec exactement trois mesures."""
    assert len(SCENARIO_DEFAUT.mesures) == 3
    assert SCENARIO_DEFAUT.source_1.position != SCENARIO_DEFAUT.source_2.position


def test_le_scenario_rejette_deux_mesures() -> None:
    """Moins de trois mesures est une erreur de configuration."""
    mesures = ((400.0, 400.0), (1000.0, 400.0))
    with pytest.raises(ValueError, match="exactement trois mesures"):
        _scenario_modifie(mesures=mesures)


def test_le_scenario_rejette_des_mesures_confondues() -> None:
    """Deux mesures au même point ne sont pas une redondance exploitable."""
    mesures = ((400.0, 400.0), (400.0, 400.0), (1600.0, 400.0))
    with pytest.raises(ValueError, match="distincts"):
        _scenario_modifie(mesures=mesures)


def test_le_scenario_rejette_une_mesure_hors_fenetre() -> None:
    """Une mesure hors de la fenêtre d'affichage est une erreur de configuration."""
    mesures = ((400.0, 400.0), (1000.0, 400.0), (2600.0, 400.0))
    with pytest.raises(ValueError, match="dans la fenêtre"):
        _scenario_modifie(mesures=mesures)


def test_le_scenario_rejette_un_seuil_nul() -> None:
    """Un seuil non strictement positif est une erreur de configuration."""
    with pytest.raises(ValueError, match="strictement positif"):
        _scenario_modifie(seuil=0.0)


def test_le_scenario_rejette_un_seuil_trop_grand() -> None:
    """Un seuil au-dessus de la plus petite amplitude vide les régions."""
    with pytest.raises(ValueError, match="plus petite amplitude"):
        _scenario_modifie(seuil=1.5)


def test_le_scenario_rejette_des_sources_confondues() -> None:
    """Deux sources au même point ne forment pas une superposition."""
    source = SourceGaussienne(position=(700.0, 1200.0), amplitude=1.0, longueur=300.0)
    with pytest.raises(ValueError, match="positions distinctes"):
        _scenario_modifie(source_2=source)


def test_le_scenario_rejette_une_source_hors_fenetre() -> None:
    """Une source hors de la fenêtre d'affichage est une erreur de configuration."""
    source = SourceGaussienne(position=(2200.0, 1200.0), amplitude=1.0, longueur=300.0)
    with pytest.raises(ValueError, match="dans la fenêtre"):
        _scenario_modifie(source_2=source)


def test_le_scenario_rejette_un_disque_debordant() -> None:
    """Un disque affecté qui déborde de la fenêtre est une erreur de configuration."""
    source = SourceGaussienne(position=(1950.0, 1200.0), amplitude=1.0, longueur=300.0)
    with pytest.raises(ValueError, match="rester dans la fenêtre"):
        _scenario_modifie(source_2=source)


def test_le_scenario_rejette_une_fenetre_hors_domaine() -> None:
    """Une fenêtre qui déborde du domaine d'étude est une erreur de configuration."""
    fenetre = Rectangle(coin=(19000.0, 0.0), largeur=2000.0, hauteur=2000.0)
    with pytest.raises(ValueError, match="entièrement contenue"):
        _scenario_modifie(fenetre=fenetre)


def test_le_rayon_exige_un_seuil_valide() -> None:
    """Le rayon du disque affecté exige un seuil dans (0, amplitude]."""
    with pytest.raises(ValueError, match="strictement positif"):
        SCENARIO_DEFAUT.source_1.rayon_affecte(0.0)
    with pytest.raises(ValueError, match="au plus égal"):
        SCENARIO_DEFAUT.source_1.rayon_affecte(2.0)


def test_rayons_et_surfaces_sont_analytiques() -> None:
    """Le rayon du disque affecté et sa surface suivent les formules fermées."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    attendu = 300.0 * math.sqrt(math.log(2.0))
    assert resultat.rayon_affecte_1 == pytest.approx(attendu)
    assert resultat.rayon_affecte_2 == pytest.approx(attendu)
    assert resultat.surface_affectee_1 == pytest.approx(math.pi * attendu**2)
    assert resultat.surface_affectee_2 == pytest.approx(math.pi * attendu**2)


def test_les_vents_mesures_proviennent_du_champ_analytique() -> None:
    """Les trois vents évalués sont exactement le champ aux points de mesure."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    champ = SCENARIO_DEFAUT.champ_vent
    attendus = tuple(champ.vitesse(*mesure) for mesure in SCENARIO_DEFAUT.mesures)
    attendus = tuple(attendus)  # type: ignore[redundant-cast]
    assert (resultat.vent_mesure_1, resultat.vent_mesure_2, resultat.vent_mesure_3) == attendus
    for vent in attendus:
        assert math.hypot(vent[0], vent[1]) > 1.0


def test_la_divergence_numerique_est_negligeable() -> None:
    """Le champ de vent est incompressible à la précision de la grille."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.divergence_max < 1e-12


def test_la_region_totale_depasse_la_somme_des_regions() -> None:
    """Les régions affectées ne s'ajoutent pas : pont sous le seuil."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.surface_affectee_1 > 0.0
    assert resultat.surface_affectee_2 > 0.0
    assert resultat.surface_affectee_totale > resultat.surface_affectee_1 + resultat.surface_affectee_2


def test_les_contributions_croisees_et_le_maximum_sont_coherents() -> None:
    """La somme dépasse chaque amplitude ; les contributions croisées décroissent."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.contribution_croisee_1 == pytest.approx(math.exp(-4.0))
    assert resultat.contribution_croisee_2 == pytest.approx(math.exp(-4.0))
    assert resultat.concentration_max_totale == pytest.approx(1.0 + math.exp(-4.0))


def test_les_objets_sont_immuables() -> None:
    """La configuration est figée : aucune mutation silencieuse possible."""
    with pytest.raises(FrozenInstanceError):
        SCENARIO_DEFAUT.seuil = 0.9


def test_le_manifeste_est_reproductible_et_exportable() -> None:
    """Le manifeste consigne le niveau R1, la source et s'exporte en JSON."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resultat)
    assert manifeste.identifiant == "jdriftx-superposition-sources-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert manifeste.hypothese
    assert manifeste.limites
    assert "uv run" in manifeste.commande
    export = json.loads(json.dumps(manifeste.vers_dict()))
    assert export["identifiant"] == "jdriftx-superposition-sources-001"
    assert export["parametres"]["seuil"] == 0.5
    assert export["resultats"]["surface_affectee_totale"] > 0.0
