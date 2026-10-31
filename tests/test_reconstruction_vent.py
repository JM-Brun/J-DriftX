"""Tests de la reconstruction du vent à deux mesures (Fig. 1, étape B)."""

import json
import math
from dataclasses import FrozenInstanceError, replace

import numpy as np
import pytest

from jdriftx.champ_analytique import SuperpositionChamps
from jdriftx.experiences.reconstruction_vent import (
    CHAMP_CHOIX_1,
    PERTURBATION,
    SCENARIO_DEFAUT,
    Rectangle,
    ScenarioReconstruction,
    construire_manifeste,
    resoudre_scenario,
)


def _scenario_modifie(**changements: object) -> ScenarioReconstruction:
    """Renvoie le scénario par défaut avec les remplacements fournis."""
    return replace(SCENARIO_DEFAUT, **changements)


def test_le_scenario_exige_exactement_deux_mesures() -> None:
    """Un nombre de mesures différent de deux est refusé."""
    # Given — une seule mesure au lieu de deux.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="exactement deux mesures"):
        _scenario_modifie(mesures=((250.0, 500.0),))


def test_les_mesures_confondues_sont_rejetees() -> None:
    """Deux points de mesure confondus sont refusés."""
    # Given — deux mesures identiques.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="distincts"):
        _scenario_modifie(mesures=((250.0, 500.0), (250.0, 500.0)))


def test_une_mesure_hors_du_domaine_est_rejetee() -> None:
    """Une mesure située hors du domaine est refusée."""
    # Given — une seconde mesure à abscisse négative.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="dans le domaine"):
        _scenario_modifie(mesures=((250.0, 500.0), (-5.0, 500.0)))


def test_la_parcelle_doit_etre_entirement_contenue() -> None:
    """Une parcelle débordant du domaine est refusée."""
    # Given — une parcelle dont le coin droit dépasse le domaine.
    parcelle = Rectangle(coin=(19950.0, 550.0), largeur=100.0, hauteur=100.0)
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="entièrement contenue"):
        _scenario_modifie(parcelle=parcelle)


def test_les_dimensions_non_positives_sont_rejetees() -> None:
    """Largeur ou hauteur non strictement positive : construction refusée."""
    # Given — un rectangle de largeur nulle.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="strictement positives"):
        Rectangle(coin=(0.0, 0.0), largeur=0.0, hauteur=100.0)


def test_les_coordonnees_non_finies_sont_rejetees() -> None:
    """Une mesure à coordonnée non finie est refusée."""
    # Given — une mesure d'abscisse NaN.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="coordonnées finies"):
        _scenario_modifie(mesures=((float("nan"), 500.0), (750.0, 500.0)))


def test_la_trajectoire_exige_au_moins_deux_points() -> None:
    """Une trajectoire réduite à un point est refusée."""
    # Given — une trajectoire d'un seul point.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="au moins deux points"):
        _scenario_modifie(trajectoire=((150.0, 575.0),))


def test_les_points_hors_de_la_parcelle_sont_rejetes() -> None:
    """Un point de trajectoire hors de la parcelle est refusé."""
    # Given — un second point à l'extérieur de la parcelle.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="dans la parcelle"):
        _scenario_modifie(trajectoire=((150.0, 575.0), (350.0, 575.0)))


def test_les_points_consecutifs_confondus_sont_rejetes() -> None:
    """Deux points consécutifs confondus sont refusés."""
    # Given — une trajectoire qui répète son premier point.
    trajectoire = ((150.0, 575.0), (150.0, 575.0), (250.0, 625.0), (150.0, 625.0))
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="consécutifs"):
        _scenario_modifie(trajectoire=trajectoire)


def test_les_valeurs_mesurees_sont_analytiques() -> None:
    """Les vents mesurés du choix 1 valent ∓amplitude·k, composante v nulle."""
    # Given — le scénario par défaut et la valeur analytique A·k.
    k = 2.0 * math.pi / SCENARIO_DEFAUT.champ_choix_1.longueur
    attendu = SCENARIO_DEFAUT.champ_choix_1.amplitude * k
    # When — le scénario est résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # Then — les vents mesurés sont analytiques.
    assert resultat.vent_mesure_1[0] == pytest.approx(-attendu, rel=1e-9)
    assert resultat.vent_mesure_2[0] == pytest.approx(attendu, rel=1e-9)
    assert abs(resultat.vent_mesure_1[1]) < 1e-9
    assert abs(resultat.vent_mesure_2[1]) < 1e-9


def test_les_deux_choix_coincident_aux_mesures() -> None:
    """L'écart entre les deux choix aux mesures est inférieur à 1e-10 m/s."""
    # Given — le scénario par défaut résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # Then — les deux choix coïncident aux mesures à la précision machine près.
    assert resultat.ecart_entre_choix < 1e-10


def test_les_deux_champs_sont_distincts_hors_des_mesures() -> None:
    """Hors des mesures, les deux choix diffèrent de plus de 1 m/s."""
    # Given — un point quelconque éloigné des mesures.
    # When — les vitesses des deux choix sont évaluées.
    u_1, v_1 = SCENARIO_DEFAUT.champ_choix_1.vitesse(100.0, 100.0)
    u_2, v_2 = SCENARIO_DEFAUT.champ_choix_2.vitesse(100.0, 100.0)
    # Then — l'écart entre les deux champs est manifeste.
    assert math.hypot(u_1 - u_2, v_1 - v_2) > 1.0


def test_les_divergences_numeriques_sont_negligeables() -> None:
    """Les divergences estimées des deux champs restent sous 1e-12 s^-1."""
    # Given — le scénario par défaut résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # Then — chaque champ est incompressible aux erreurs d'arrondi près.
    assert resultat.divergence_max_choix_1 < 1e-12
    assert resultat.divergence_max_choix_2 < 1e-12


def test_la_longueur_de_trajectoire_est_exacte() -> None:
    """La polyligne relevée au sol mesure exactement 250 m."""
    # Given — le scénario par défaut résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # Then — la longueur est exacte (segments alignés sur les axes).
    assert resultat.longueur_trajectoire == 250.0


def test_les_surfaces_et_le_rapport_sont_coherents() -> None:
    """Parcelle de 1 ha, domaine de 400 km², rapport de surfaces 40 000."""
    # Given — le scénario par défaut.
    # When / Then — les surfaces et leur rapport sont exacts.
    assert SCENARIO_DEFAUT.parcelle.surface == 10_000.0
    assert SCENARIO_DEFAUT.domaine.surface == 400_000_000.0
    rapport = SCENARIO_DEFAUT.domaine.surface / SCENARIO_DEFAUT.parcelle.surface
    assert rapport == 40_000.0


def test_le_rectangle_contient_sa_frontiere() -> None:
    """L'appartenance inclut la frontière et exclut l'extérieur strict."""
    # Given — la parcelle par défaut.
    parcelle = SCENARIO_DEFAUT.parcelle
    # When / Then — le coin est contenu, le point voisin ne l'est pas.
    assert parcelle.contient((250.0, 650.0))
    assert not parcelle.contient((250.1, 600.0))


def test_le_resultat_est_immuable() -> None:
    """Les résultats ne peuvent pas être modifiés après construction."""
    # Given — un résultat résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # When / Then — toute mutation est refusée.
    with pytest.raises(FrozenInstanceError):
        resultat.longueur_trajectoire = 1.0


def test_le_manifeste_documente_source_niveau_et_limites() -> None:
    """Le manifeste relie l'expérience à sa source, son niveau R1 et ses limites."""
    # Given — un scénario résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # When — le manifeste est construit.
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resultat)
    # Then — les métadonnées requises sont présentes et explicites.
    assert manifeste.identifiant == "jdriftx-reconstruction-vent-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert "p. 253" in manifeste.source
    assert manifeste.hypothese
    assert manifeste.limites
    assert manifeste.scenario is SCENARIO_DEFAUT
    assert manifeste.version_code != ""
    assert "uv run" in manifeste.commande


def test_le_manifeste_exporte_un_dict_serialisable() -> None:
    """vers_dict produit un export JSON sérialisable sans objet du domaine."""
    # Given — un manifeste construit.
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resoudre_scenario(SCENARIO_DEFAUT))
    # When — l'export frontière est produit et sérialisé.
    export = manifeste.vers_dict()
    charge = json.dumps(export)
    # Then — l'export est sérialisable et sans objet du domaine imbriqué.
    assert "jdriftx-reconstruction-vent-001" in charge
    assert isinstance(export["limites"], list)
    for valeur in export.values():
        assert not isinstance(valeur, (Rectangle, ScenarioReconstruction))


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["coin", "largeur", "hauteur"])
def test_le_rectangle_refuse_les_parametres_booleens(booleen: bool | np.bool_, champ: str) -> None:
    """Le coin et les dimensions du rectangle excluent les booléens."""
    # Given — un champ géométrique remplacé par un booléen.
    valeurs: dict[str, object] = {
        "coin": (0.0, 0.0),
        "largeur": 100.0,
        "hauteur": 100.0,
    }
    valeurs[champ] = (booleen, 0.0) if champ == "coin" else booleen
    # When / Then — la construction du rectangle est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        Rectangle(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_le_rectangle_contient_refuse_un_point_booleen(booleen: bool | np.bool_) -> None:
    """Le prédicat d'appartenance refuse lui aussi les coordonnées booléennes."""
    # Given — un rectangle valide et un point booléen.
    rectangle = SCENARIO_DEFAUT.domaine
    # When / Then — l'évaluation du prédicat est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        rectangle.contient((booleen, 1.0))


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["mesures", "trajectoire"])
def test_le_scenario_refuse_les_points_booleens(booleen: bool | np.bool_, champ: str) -> None:
    """Les mesures et points de trajectoire excluent les coordonnées booléennes."""
    # Given — une mesure ou un point de trajectoire booléen.
    valeurs: dict[str, object] = {
        "mesures": ((250.0, 500.0), (750.0, 500.0)),
        "trajectoire": ((150.0, 575.0), (250.0, 575.0), (250.0, 625.0), (150.0, 625.0)),
    }
    if champ == "mesures":
        valeurs[champ] = ((booleen, 500.0), (750.0, 500.0))
    else:
        valeurs[champ] = ((150.0, booleen), (250.0, 575.0))
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        _scenario_modifie(**valeurs)


def test_le_manifeste_exporte_une_superposition_imbriquee_sans_inventer_de_parametres() -> None:
    """Un champ du protocole hors classe cellulaire est exporté par son type."""
    # Given — un scénario dont le choix 2 imbrique une superposition.
    champ_choix_2 = SuperpositionChamps((CHAMP_CHOIX_1, SuperpositionChamps((PERTURBATION,))))
    scenario = _scenario_modifie(champ_choix_2=champ_choix_2)
    manifeste = construire_manifeste(scenario, resoudre_scenario(scenario))
    # When — l'export frontière est produit.
    export = manifeste.vers_dict()
    # Then — le champ cellulaire garde ses paramètres, l'imbriquée est exportée par type.
    parametres = json.loads(json.dumps(export))["parametres"]
    champs = parametres["champs_choix_2"]
    assert champs[0] == {"amplitude": 800.0, "longueur": 1000.0}
    assert champs[1] == {"type": "SuperpositionChamps"}
