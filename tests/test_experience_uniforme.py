"""Tests de la tranche verticale « champ uniforme » (configuration → manifeste)."""

import math
from dataclasses import FrozenInstanceError
from importlib import metadata

import pytest
import numpy as np

import jdriftx.experiences.uniforme as module_uniforme
from jdriftx.experiences.uniforme import (
    SCENARIO_DEFAUT,
    ChampUniforme,
    ResultatDirige,
    ScenarioUniforme,
    construire_manifeste,
    resoudre_scenario,
)


def test_champ_uniforme_rejette_un_vent_nul() -> None:
    """L'invariant ‖u‖ > 0 est vérifié à la construction."""
    # Given — un vent rigoureusement nul.
    vent = (0.0, 0.0)
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="non nul"):
        ChampUniforme(vent=vent)


def test_champ_uniforme_rejette_une_composante_non_finie() -> None:
    """Une composante non finie est refusée à la construction."""
    # Given — un vent avec une composante NaN.
    vent = (float("nan"), 0.0)
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="finies"):
        ChampUniforme(vent=vent)


def test_scenario_rejette_un_point_mal_forme() -> None:
    """Les points doivent être des couples de coordonnées finies."""
    # Given — un champ valide et une cible mal formée.
    champ = ChampUniforme(vent=(2.0, 0.0))
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="cible"):
        ScenarioUniforme(champ=champ, origine=(0.0, 0.0), cible=(300.0,))


def test_scenario_jouet_reproduit_les_valeurs_analytiques() -> None:
    """Le scénario par défaut donne τ(A,B) = 150 s, τ(B,A) = +inf, dE ≈ 307 m, écart 65 m."""
    # Given — le scénario jouet documenté (vent 2 m/s selon +x, cible en aval).
    scenario = SCENARIO_DEFAUT
    # When — le scénario est résolu par l'implémentation partagée.
    resultat = resoudre_scenario(scenario)
    # Then — les valeurs analytiques attendues sont restituées.
    assert resultat.tau_origine_cible == pytest.approx(150.0)
    assert math.isinf(resultat.tau_cible_origine)
    assert resultat.distance_euclidienne == pytest.approx(math.hypot(300.0, 65.0))
    assert resultat.ecart_transversal == pytest.approx(65.0)


def test_cible_sur_la_ligne_de_vent_n_est_pas_penalisee_transversalement() -> None:
    """Un écart transversal nul ne change pas le coût longitudinal."""
    # Given — une cible exactement sur la ligne de vent passant par l'origine.
    scenario = ScenarioUniforme(
        champ=ChampUniforme(vent=(2.0, 0.0)),
        origine=(0.0, 0.0),
        cible=(300.0, 0.0),
    )
    # When — le scénario est résolu.
    resultat = resoudre_scenario(scenario)
    # Then — l'écart transversal est nul et le coût vaut 150 s.
    assert resultat.ecart_transversal == pytest.approx(0.0)
    assert resultat.tau_origine_cible == pytest.approx(150.0)


def test_points_confondus_donnent_un_cout_nul() -> None:
    """Deux points confondus ont un coût nul dans les deux sens (pathologie documentée)."""
    # Given — origine et cible confondues.
    scenario = ScenarioUniforme(
        champ=ChampUniforme(vent=(2.0, 0.0)),
        origine=(50.0, 25.0),
        cible=(50.0, 25.0),
    )
    # When — le scénario est résolu.
    resultat = resoudre_scenario(scenario)
    # Then — les coûts sont nuls dans les deux sens.
    assert resultat.tau_origine_cible == pytest.approx(0.0)
    assert resultat.tau_cible_origine == pytest.approx(0.0)


def test_cible_en_amont_recoit_un_cout_infini() -> None:
    """Lu de la cible vers l'origine, le scénario jouet est amont : coût infini."""
    # Given — le scénario jouet inversé (origine = cible initiale).
    scenario = ScenarioUniforme(
        champ=SCENARIO_DEFAUT.champ,
        origine=SCENARIO_DEFAUT.cible,
        cible=SCENARIO_DEFAUT.origine,
    )
    # When — le scénario est résolu.
    resultat = resoudre_scenario(scenario)
    # Then — l'aller est infini (amont) et le retour est fini.
    assert math.isinf(resultat.tau_origine_cible)
    assert resultat.tau_cible_origine == pytest.approx(150.0)


def test_les_resultats_sont_immuables() -> None:
    """Les résultats ne peuvent pas être modifiés après construction."""
    # Given — un résultat résolu.
    resultat = resoudre_scenario(SCENARIO_DEFAUT)
    # When / Then — toute mutation est refusée.
    with pytest.raises(FrozenInstanceError):
        resultat.tau_origine_cible = 1.0


def test_le_manifeste_documente_source_niveau_et_limites() -> None:
    """Le manifeste relie l'expérience à sa source, son niveau R1 et ses limites."""
    # Given — un scénario résolu.
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    # When — le manifeste est construit.
    manifeste = construire_manifeste(scenario, resultat)
    # Then — les métadonnées requises sont présentes et explicites.
    assert manifeste.identifiant == "jdriftx-uniforme-001"
    assert manifeste.niveau_fidelite == "R1"
    assert "10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert manifeste.hypothese
    assert manifeste.limites
    assert manifeste.scenario is scenario
    assert manifeste.resultat is resultat
    assert manifeste.version_code != ""
    assert "uv run" in manifeste.commande


def test_le_manifeste_exporte_un_dict_pour_la_frontiere_json() -> None:
    """vers_dict produit un export plat sans objet du domaine imbriqué."""
    # Given — un manifeste construit.
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resoudre_scenario(SCENARIO_DEFAUT))
    # When — l'export frontière est produit.
    export = manifeste.vers_dict()
    # Then — les clés et valeurs attendues sont présentes.
    assert export["identifiant"] == "jdriftx-uniforme-001"
    assert export["parametres"]["vent"] == [2.0, 0.0]
    assert export["resultats"]["tau_origine_cible"] == pytest.approx(150.0)
    assert isinstance(export["limites"], list)
    for valeur in export.values():
        assert not isinstance(valeur, (ChampUniforme, ScenarioUniforme, ResultatDirige))


def test_le_manifeste_signale_une_version_non_installee(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Si le paquet n'est pas installé, le manifeste le dit au lieu d'échouer."""
    # Given — un environnement où importlib.metadata ne trouve pas « jdriftx ».

    def _version_introuvable(nom: str) -> str:
        raise metadata.PackageNotFoundError(nom)

    monkeypatch.setattr(module_uniforme.metadata, "version", _version_introuvable)
    # When — le manifeste est construit dans cet environnement.
    manifeste = construire_manifeste(SCENARIO_DEFAUT, resoudre_scenario(SCENARIO_DEFAUT))
    # Then — la version est explicitement marquée « non-installe ».
    assert manifeste.version_code == "non-installe"


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("axe", [0, 1])
def test_le_champ_uniforme_refuse_les_composantes_booleennes(
    booleen: bool | np.bool_, axe: int
) -> None:
    """Les composantes du vecteur de vent excluent les booléens."""
    # Given — un vecteur de vent avec une composante booléenne.
    vent = [2.0, 0.0]
    vent[axe] = booleen
    # When / Then — la construction du champ est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        ChampUniforme(vent=tuple(vent))


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("point", ["origine", "cible"])
def test_le_scenario_refuse_les_coordonnees_booleennes(
    booleen: bool | np.bool_, point: str
) -> None:
    """Les coordonnées des points du scénario excluent les booléens."""
    # Given — un point du scénario dont une coordonnée est booléenne.
    origine = (0.0, 0.0)
    cible = (300.0, 65.0)
    valeurs = [origine, cible]
    indice = 0 if point == "origine" else 1
    coordonnees = list(valeurs[indice])
    coordonnees[0] = booleen
    valeurs[indice] = tuple(coordonnees)
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        ScenarioUniforme(champ=SCENARIO_DEFAUT.champ, origine=valeurs[0], cible=valeurs[1])
