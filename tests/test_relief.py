"""Tests de la tranche verticale relief et dispersion (figure 5)."""

import json
import math
from dataclasses import FrozenInstanceError, replace

import pytest

from jdriftx.experiences.reconstruction_vent import Rectangle
from jdriftx.experiences.relief import (
    COLLINE_1_DEFAUT,
    COLLINE_2_DEFAUT,
    SCENARIO_DEFAUT,
    CollineGaussienne,
    ScenarioRelief,
    concentrations_au_point,
    construire_manifeste,
    resoudre_scenario,
)
from jdriftx.similitude import sigma_z


def _scenario_modifie(**changements: object) -> ScenarioRelief:
    """Renvoie le scénario par défaut avec des champs remplacés."""
    return replace(SCENARIO_DEFAUT, **changements)


def test_le_scenario_defaut_porte_deux_collines() -> None:
    """Le scénario par défaut est constructible avec deux collines distinctes."""
    assert len(SCENARIO_DEFAUT.collines) == 2
    assert SCENARIO_DEFAUT.collines[0].centre != SCENARIO_DEFAUT.collines[1].centre


def test_une_colline_rejette_une_hauteur_nulle() -> None:
    """Une colline d'amplitude nulle n'est pas un relief."""
    with pytest.raises(ValueError, match="strictement positive"):
        CollineGaussienne(centre=(1000.0, 1600.0), hauteur=0.0, echelle=90.0)


def test_le_scenario_rejette_trois_collines() -> None:
    """Plus ou moins deux collines est une erreur de configuration."""
    collines = (COLLINE_1_DEFAUT, COLLINE_1_DEFAUT, COLLINE_1_DEFAUT)
    with pytest.raises(ValueError, match="exactement deux collines"):
        _scenario_modifie(collines=collines)


def test_le_scenario_rejette_des_collines_confondues() -> None:
    """Deux collines au même centre ne forment pas un relief lisible."""
    with pytest.raises(ValueError, match="centres distincts"):
        _scenario_modifie(collines=(COLLINE_1_DEFAUT, COLLINE_1_DEFAUT))


def test_le_scenario_rejette_une_colline_hors_fenetre() -> None:
    """Une colline hors de la fenêtre d'affichage est une erreur de configuration."""
    colline = CollineGaussienne(centre=(2500.0, 1600.0), hauteur=40.0, echelle=90.0)
    with pytest.raises(ValueError, match="dans la fenêtre"):
        _scenario_modifie(collines=(colline, COLLINE_2_DEFAUT))


def test_le_scenario_rejette_une_colline_en_amont() -> None:
    """Une colline en amont de la source n'est pas balayée par le panache."""
    colline = CollineGaussienne(centre=(1000.0, 1950.0), hauteur=40.0, echelle=90.0)
    with pytest.raises(ValueError, match="sous le vent"):
        _scenario_modifie(collines=(colline, COLLINE_2_DEFAUT))


def test_le_scenario_rejette_un_vent_nul() -> None:
    """Un vent de norme nulle ne transporte rien."""
    with pytest.raises(ValueError, match="norme strictement positive"):
        _scenario_modifie(vent=(0.0, 0.0))


def test_le_scenario_rejette_un_debit_nul() -> None:
    """Un débit nul n'est pas une source."""
    with pytest.raises(ValueError, match="strictement positif"):
        _scenario_modifie(debit=0.0)


def test_le_scenario_rejette_une_classe_inconnue() -> None:
    """Une classe hors A-F est une erreur de configuration."""
    with pytest.raises(ValueError, match="Classe de stabilité inconnue"):
        _scenario_modifie(classe="Z")


def test_le_scenario_rejette_un_seuil_nul() -> None:
    """Un seuil non strictement positif est une erreur de configuration."""
    with pytest.raises(ValueError, match="strictement positif"):
        _scenario_modifie(seuil=0.0)


def test_le_scenario_rejette_une_source_hors_fenetre() -> None:
    """Une source hors de la fenêtre d'affichage est une erreur de configuration."""
    with pytest.raises(ValueError, match="dans la fenêtre"):
        _scenario_modifie(source=(2500.0, 1900.0))


def test_le_scenario_rejette_une_source_sur_une_colline() -> None:
    """Une source posée sur un relief marqué fausse la convention d'axe horizontal."""
    with pytest.raises(ValueError, match="sol quasi plat"):
        _scenario_modifie(source=(1000.0, 1600.0))


def test_le_scenario_rejette_une_fenetre_hors_domaine() -> None:
    """Une fenêtre qui déborde du domaine d'étude est une erreur de configuration."""
    fenetre = Rectangle(coin=(19000.0, 0.0), largeur=2000.0, hauteur=2000.0)
    with pytest.raises(ValueError, match="entièrement contenue"):
        _scenario_modifie(fenetre=fenetre)


def test_l_altitude_du_mnt_est_maximale_au_sommet_a() -> None:
    """L'altitude maximale sur la grille est atteinte au sommet de la colline A."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    attendu = SCENARIO_DEFAUT.altitude_sol(1000.0, 1600.0)
    assert resultat.altitude_max_mnt == pytest.approx(attendu)
    assert resultat.altitude_axe == pytest.approx(50.0, abs=0.5)


def test_le_panache_ne_remonte_pas_au_vent() -> None:
    """En amont de la source, la concentration est nulle dans les deux conventions."""
    c_sans, c_avec = concentrations_au_point(SCENARIO_DEFAUT, 1000.0, 1950.0)
    assert c_sans == 0.0
    assert c_avec == 0.0


def test_les_deux_calculs_coincident_hors_du_relief() -> None:
    """Hors du relief, la correction ne change rien au point de calcul."""
    c_sans, c_avec = concentrations_au_point(SCENARIO_DEFAUT, 0.0, 0.0)
    assert c_sans > 0.0
    assert c_sans == c_avec


def test_la_region_avec_contient_la_region_sans() -> None:
    """Sur la grille 50 m, la correction n'enlève aucune cellule affectée."""
    scenario = SCENARIO_DEFAUT
    pas = 50.0
    nombre = int(scenario.fenetre.largeur / pas) + 1
    for i in range(nombre):
        x = scenario.fenetre.coin[0] + i * pas
        for j in range(nombre):
            y = scenario.fenetre.coin[1] + j * pas
            c_sans, c_avec = concentrations_au_point(scenario, x, y)
            if c_sans >= scenario.seuil:
                assert c_avec >= scenario.seuil


def test_la_grille_respecte_une_fenetre_non_carree(monkeypatch: pytest.MonkeyPatch) -> None:
    """Le nombre de cellules suit séparément largeur et hauteur de la fenêtre."""
    scenario = replace(
        SCENARIO_DEFAUT,
        collines=(
            CollineGaussienne(centre=(1000.0, 600.0), hauteur=40.0, echelle=90.0),
            CollineGaussienne(centre=(1000.0, 400.0), hauteur=35.0, echelle=60.0),
        ),
        source=(1000.0, 900.0),
        fenetre=Rectangle(coin=(0.0, 0.0), largeur=2000.0, hauteur=1000.0),
    )
    monkeypatch.setattr(
        "jdriftx.experiences.relief.concentrations_au_point",
        lambda _scenario, _x, _y: (1.0, 1.0),
    )

    resultat = resoudre_scenario(scenario)

    nombre_x = int(scenario.fenetre.largeur / 50.0) + 1
    nombre_y = int(scenario.fenetre.hauteur / 50.0) + 1
    assert resultat.cellules_sans == nombre_x * nombre_y
    assert resultat.cellules_avec == nombre_x * nombre_y


def test_les_valeurs_du_scenario_defaut_sont_reproductibles() -> None:
    """Les agrégats du scénario par défaut sont déterministes et documentés."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.cellules_sans == 40
    assert resultat.cellules_avec == 48
    assert resultat.surface_region_sans == 40 * 50.0 * 50.0
    assert resultat.surface_region_avec == 48 * 50.0 * 50.0
    assert resultat.ratio_sommet_1 == pytest.approx(4.697, rel=1e-3)
    assert resultat.ratio_sommet_2 == pytest.approx(1.22, rel=1e-2)
    assert resultat.concentration_max_avec > resultat.concentration_max_sans


def test_le_ratio_au_sommet_est_analytique() -> None:
    """Le rapport au sommet suit le profil vertical gaussien de similitude."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    scenario = SCENARIO_DEFAUT
    u, v = scenario.vent
    norme = math.hypot(u, v)
    colline = scenario.collines[0]
    dx = colline.centre[0] - scenario.source[0]
    dy = colline.centre[1] - scenario.source[1]
    sous_vent = (dx * u + dy * v) / norme
    sz = sigma_z(sous_vent, scenario.classe)
    axe = resultat.altitude_axe
    hauteur = scenario.hauteur_evaluation
    z_reel = scenario.altitude_sol(*colline.centre) + hauteur
    numerateur = math.exp(-((z_reel - axe) ** 2) / (2 * sz**2)) + math.exp(
        -((z_reel + axe) ** 2) / (2 * sz**2)
    )
    denominateur = math.exp(-((hauteur - axe) ** 2) / (2 * sz**2)) + math.exp(
        -((hauteur + axe) ** 2) / (2 * sz**2)
    )
    attendu = numerateur / denominateur
    assert resultat.ratio_sommet_1 == pytest.approx(attendu, rel=1e-12)


def test_les_objets_sont_immuables() -> None:
    """La configuration est figée : aucune mutation silencieuse possible."""
    with pytest.raises(FrozenInstanceError):
        SCENARIO_DEFAUT.seuil = 1e-5


def test_le_manifeste_est_reproductible_et_exportable() -> None:
    """Le manifeste consigne le niveau R1, la source et s'exporte en JSON."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resultat)
    assert manifeste.identifiant == "jdriftx-relief-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert manifeste.hypothese
    assert manifeste.limites
    assert "uv run" in manifeste.commande
    export = json.loads(json.dumps(manifeste.vers_dict()))
    assert export["identifiant"] == "jdriftx-relief-001"
    assert export["parametres"]["seuil"] == 2e-5
    assert export["resultats"]["cellules_avec"] == 48
