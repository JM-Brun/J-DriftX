"""Tests de l'expérience d'identification de source (figure 6)."""

import math
from dataclasses import replace

import pytest

from jdriftx.experiences.identification_source import (
    SCENARIO_DEFAUT,
    concentration,
    construire_manifeste,
    resoudre_scenario,
)


def test_le_capteur_de_detection_depasse_le_seul_seuil() -> None:
    """Un seul capteur détecte, celui du coin inférieur gauche."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.concentration_detection >= SCENARIO_DEFAUT.seuil_detection
    au_dessus = [
        c >= SCENARIO_DEFAUT.seuil_detection for c in resultat.concentrations_observees
    ]
    assert sum(au_dessus) == 1
    assert au_dessus[SCENARIO_DEFAUT.indice_detection]


def test_le_panache_est_nul_en_amont() -> None:
    """Transport advectif dominant : aucune concentration en amont."""
    amont = concentration(SCENARIO_DEFAUT, (1700.0, 1700.0), SCENARIO_DEFAUT.source_vrai, 2.0)
    aval = concentration(SCENARIO_DEFAUT, (1300.0, 1300.0), SCENARIO_DEFAUT.source_vrai, 2.0)
    assert amont == 0.0
    assert aval > 0.0


def test_linearite_exacte_en_debit() -> None:
    """Le modèle direct est exactement linéaire en débit."""
    point = SCENARIO_DEFAUT.capteurs[0]
    unite = concentration(SCENARIO_DEFAUT, point, SCENARIO_DEFAUT.source_vrai, 1.0)
    double = concentration(SCENARIO_DEFAUT, point, SCENARIO_DEFAUT.source_vrai, 2.0)
    assert double == 2.0 * unite


def test_symetrie_transverse_du_panache() -> None:
    """Le scénario est symétrique par rapport à l'axe du vent."""
    haut = concentration(SCENARIO_DEFAUT, (400.0, 200.0), SCENARIO_DEFAUT.source_vrai, 2.0)
    bas = concentration(SCENARIO_DEFAUT, (200.0, 400.0), SCENARIO_DEFAUT.source_vrai, 2.0)
    assert haut == bas


def test_le_minimum_est_exact_a_la_source_vraie() -> None:
    """Observations sans bruit : coût nul, position et débit retrouvés."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert resultat.cout_minimum == 0.0
    assert resultat.position_estimee == SCENARIO_DEFAUT.source_vrai
    assert abs(resultat.debit_etoile - SCENARIO_DEFAUT.debit_vrai) <= 1e-12


def test_la_vallee_est_etroite_et_allongee() -> None:
    """La vallée du coût est quantifiée : longue d'un seul côté, étroite."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert 5 <= resultat.nombre_cellules_vallee <= 9
    assert resultat.largeur_vallee == SCENARIO_DEFAUT.pas_candidats
    assert resultat.etendue_vallee >= 6.0 * resultat.largeur_vallee


def test_le_candidat_decale_montre_une_ambiguite_reelle() -> None:
    """Décaler la source au vent et ajuster le débit laisse le coût bas."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert 1e-4 <= resultat.cout_relatif_decale <= 1e-2
    assert resultat.debit_etoile_decale > SCENARIO_DEFAUT.debit_vrai
    attendu = math.sqrt(2.0) * 300.0
    assert resultat.decalage_vent == pytest.approx(attendu, abs=0.01)


def test_la_grille_des_couts_est_coherente() -> None:
    """La carte couvre la grille, reste sous J0, plateau exact en aval."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    nombre = int(SCENARIO_DEFAUT.fenetre.largeur / SCENARIO_DEFAUT.pas_candidats) + 1
    assert len(resultat.couts_grille) == nombre * nombre
    assert max(resultat.couts_grille) <= resultat.cout_nul
    indice_source = 15 * nombre + 15
    assert resultat.couts_grille[indice_source] == 0.0
    indice_aval = 0
    assert resultat.couts_grille[indice_aval] == resultat.cout_nul
    indice_amont = 20 * nombre + 20
    assert resultat.couts_grille[indice_amont] < resultat.cout_nul


def test_les_cellules_detectees_sont_lisibles() -> None:
    """Le champ dépasse le seuil sur un nombre lisible de cellules."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    assert 30 <= resultat.cellules_detectees <= 50
    assert resultat.concentration_maximale > SCENARIO_DEFAUT.seuil_detection
    assert (
        resultat.concentration_detection
        == resultat.concentrations_observees[SCENARIO_DEFAUT.indice_detection]
    )


def test_le_rendu_est_deterministe() -> None:
    """Deux résolutions consécutives produisent le même résultat."""
    assert resoudre_scenario(SCENARIO_DEFAUT) == resoudre_scenario(SCENARIO_DEFAUT)


def test_le_manifeste_qualifie_le_livrable() -> None:
    """Le manifeste porte l'identifiant, le niveau R1 et la référence."""
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resultat)
    assert manifeste.identifiant == "jdriftx-identification-source-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "p. 255" in manifeste.source
    assert any("probabilité" in limite for limite in manifeste.limites)
    export = manifeste.vers_dict()
    assert len(export["parametres"]["capteurs"]) == 5
    assert "couts_grille" not in export["resultats"]


def test_rejette_un_vent_nul() -> None:
    """Un vent nul ne définit ni axe ni panache."""
    with pytest.raises(ValueError, match="vent doit être un vecteur non nul"):
        replace(SCENARIO_DEFAUT, vent=(0.0, 0.0))


def test_rejette_quatre_capteurs() -> None:
    """Le scénario exige exactement cinq capteurs."""
    with pytest.raises(ValueError, match="exactement cinq capteurs"):
        replace(SCENARIO_DEFAUT, capteurs=SCENARIO_DEFAUT.capteurs[:4])


def test_rejette_un_indice_hors_capteurs() -> None:
    """L'indice de détection doit désigner un capteur existant."""
    with pytest.raises(ValueError, match="indice de détection"):
        replace(SCENARIO_DEFAUT, indice_detection=5)


def test_rejette_un_seuil_que_rien_ne_depasse() -> None:
    """Un seuil trop haut vide la détection."""
    with pytest.raises(ValueError, match="Seul le capteur de détection"):
        replace(SCENARIO_DEFAUT, seuil_detection=1.0)


def test_rejette_un_pas_qui_ne_divise_pas_la_fenetre() -> None:
    """La grille des candidats doit paver exactement la fenêtre."""
    with pytest.raises(ValueError, match="diviser la largeur"):
        replace(SCENARIO_DEFAUT, pas_candidats=70.0)


def test_rejette_un_candidat_decale_hors_grille() -> None:
    """Le candidat décalé doit être un nœud de la grille."""
    with pytest.raises(ValueError, match="nœud de la grille"):
        replace(SCENARIO_DEFAUT, candidat_decale=(1750.0, 1800.0))


def test_rejette_un_candidat_decale_aval() -> None:
    """Le candidat décalé doit être strictement amont de la source."""
    with pytest.raises(ValueError, match="strictement amont"):
        replace(SCENARIO_DEFAUT, candidat_decale=(1200.0, 1200.0))
