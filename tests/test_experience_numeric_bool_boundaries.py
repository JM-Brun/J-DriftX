"""Régressions P0 : les booléens ne sont pas des paramètres physiques réels."""

from dataclasses import replace

import numpy as np
import pytest

from jdriftx.experiences.identification_source import (
    SCENARIO_DEFAUT as IDENTIFICATION_DEFAUT,
    concentration,
)
from jdriftx.experiences.modele_reduit_edp import SCENARIO_DEFAUT as EDP_DEFAUT
from jdriftx.experiences.relief import (
    COLLINE_1_DEFAUT,
    SCENARIO_DEFAUT as RELIEF_DEFAUT,
    CollineGaussienne,
    concentrations_au_point,
)
from jdriftx.experiences.superposition_sources import (
    SCENARIO_DEFAUT as SUPERPOSITION_DEFAUT,
    SourceGaussienne,
)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["hauteur", "echelle"])
def test_colline_refuse_les_parametres_booleens(booleen: bool | np.bool_, champ: str) -> None:
    """Les paramètres de la colline gaussienne excluent les booléens."""
    # Given — une colline valide dont une dimension reçoit un booléen.
    valeurs: dict[str, object] = {
        "centre": (1000.0, 1600.0),
        "hauteur": 40.0,
        "echelle": 90.0,
    }
    valeurs[champ] = booleen
    # When / Then — la construction est refusée avant l'évaluation du relief.
    with pytest.raises(ValueError, match="booléens exclus"):
        CollineGaussienne(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_colline_refuse_un_centre_booleen(booleen: bool | np.bool_) -> None:
    """Les coordonnées du centre d'une colline excluent les booléens."""
    # Given — un centre contenant une coordonnée booléenne.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        CollineGaussienne(centre=(booleen, 1600.0), hauteur=40.0, echelle=90.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["debit", "hauteur_source", "seuil", "hauteur_evaluation"])
def test_scenario_relief_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les paramètres physiques du scénario de relief excluent les booléens."""
    # Given — un paramètre physique du scénario remplacé par un booléen.
    # When / Then — la validation du scénario échoue à la construction.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(RELIEF_DEFAUT, **{champ: booleen})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["vent", "source"])
def test_scenario_relief_refuse_les_coordonnees_booleennes(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Le vent et la position source du scénario de relief excluent les booléens."""
    # Given — un vecteur ou point du scénario contenant une coordonnée booléenne.
    valeurs = (booleen, -3.0) if champ == "vent" else (1000.0, booleen)
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(RELIEF_DEFAUT, **{champ: valeurs})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["amplitude", "longueur"])
def test_source_gaussienne_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """L'amplitude et l'échelle d'une source gaussienne excluent les booléens."""
    # Given — un paramètre de source remplacé par un booléen.
    valeurs: dict[str, object] = {
        "position": (700.0, 1200.0),
        "amplitude": 1.0,
        "longueur": 300.0,
    }
    valeurs[champ] = booleen
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        SourceGaussienne(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_source_gaussienne_refuse_les_coordonnees_booleennes(booleen: bool | np.bool_) -> None:
    """La position d'une source gaussienne exclut les coordonnées booléennes."""
    # Given — une position contenant une coordonnée booléenne.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        SourceGaussienne(position=(booleen, 1200.0), amplitude=1.0, longueur=300.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_source_gaussienne_refuse_les_coordonnees_booleennes_a_levaluation(
    booleen: bool | np.bool_,
) -> None:
    """L'évaluation directe d'une source gaussienne exclut les coordonnées booléennes."""
    # Given — une source valide et un point d'évaluation booléen.
    source = SUPERPOSITION_DEFAUT.source_1
    # When / Then — l'évaluation est refusée avant le calcul gaussien.
    with pytest.raises(ValueError, match="booléens exclus"):
        source.concentration(booleen, 1200.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_rayon_affecte_refuse_un_seuil_booleen(booleen: bool | np.bool_) -> None:
    """Le seuil du rayon affecté exclut les booléens."""
    # Given — une source valide et un seuil booléen.
    source = SUPERPOSITION_DEFAUT.source_1
    # When / Then — le calcul du rayon est refusé.
    with pytest.raises(ValueError, match="booléens exclus"):
        source.rayon_affecte(booleen)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_scenario_superposition_refuse_un_seuil_booleen(booleen: bool | np.bool_) -> None:
    """Le seuil de concentration du scénario exclut les booléens."""
    # Given — le scénario de référence avec un seuil booléen.
    # When / Then — la construction est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(SUPERPOSITION_DEFAUT, seuil=booleen)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_scenario_identification_refuse_un_indice_booleen(booleen: bool | np.bool_) -> None:
    """L'indice de détection exclut bool malgré la sous-classe int de bool."""
    # Given — un indice de détection booléen.
    # When / Then — le contrôle d'index refuse la valeur.
    with pytest.raises(ValueError, match="indice de détection"):
        replace(IDENTIFICATION_DEFAUT, indice_detection=booleen)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["diffusivite", "debit_vrai"])
def test_scenario_identification_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """La diffusivité et le débit vrai excluent les booléens."""
    # Given — un paramètre physique remplacé par un booléen.
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(IDENTIFICATION_DEFAUT, **{champ: booleen})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize("champ", ["seuil_detection", "pas_candidats"])
def test_scenario_identification_refuse_les_seuils_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les seuils et pas de grille de l'identification excluent les booléens."""
    # Given — un seuil ou pas de grille remplacé par un booléen.
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(IDENTIFICATION_DEFAUT, **{champ: booleen})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    ["vent", "source_vrai", "mesures_vent", "capteurs", "candidat_decale"],
)
def test_scenario_identification_refuse_les_coordonnees_booleennes(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les coordonnées de toutes les familles de points excluent les booléens."""
    # Given — une coordonnée booléenne dans le champ géométrique ciblé.
    valeurs: dict[str, object] = {
        "vent": (3.0, -2.0),
        "source_vrai": (1500.0, 1500.0),
        "mesures_vent": IDENTIFICATION_DEFAUT.mesures_vent,
        "capteurs": IDENTIFICATION_DEFAUT.capteurs,
        "candidat_decale": IDENTIFICATION_DEFAUT.candidat_decale,
    }
    if champ in {"vent", "source_vrai", "candidat_decale"}:
        valeurs[champ] = (booleen, 1500.0)
    elif champ == "mesures_vent":
        valeurs[champ] = ((booleen, 1500.0), *IDENTIFICATION_DEFAUT.mesures_vent[1:])
    else:
        valeurs[champ] = ((booleen, 1500.0), *IDENTIFICATION_DEFAUT.capteurs[1:])
    # When / Then — la validation du scénario refuse la coordonnée booléenne.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(IDENTIFICATION_DEFAUT, **valeurs)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_fonction_concentration_refuse_un_debit_booleen(booleen: bool | np.bool_) -> None:
    """La fonction publique de concentration exclut un débit booléen."""
    # Given — un scénario valide et un débit booléen.
    # When / Then — l'évaluation est refusée avant le calcul.
    with pytest.raises(ValueError, match="booléens exclus"):
        concentration(IDENTIFICATION_DEFAUT, (1300.0, 1300.0), (1500.0, 1500.0), booleen)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_fonction_concentration_refuse_les_coordonnees_booleennes(
    booleen: bool | np.bool_,
) -> None:
    """La fonction publique de concentration exclut les coordonnées booléennes."""
    # Given — un point d'évaluation booléen et un scénario valide.
    # When / Then — l'évaluation est refusée avant le calcul.
    with pytest.raises(ValueError, match="booléens exclus"):
        concentration(IDENTIFICATION_DEFAUT, (booleen, 1300.0), (1500.0, 1500.0), 2.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
@pytest.mark.parametrize(
    "champ",
    [
        "vent",
        "diffusivite",
        "debit",
        "x_entree",
        "x_fin",
        "demi_largeur",
        "pas_transverse",
        "pas_tranche",
    ],
)
def test_scenario_edp_refuse_les_parametres_booleens(
    booleen: bool | np.bool_, champ: str
) -> None:
    """Les huit paramètres positifs du scénario EDP excluent les booléens."""
    # Given — un paramètre positif remplacé par un booléen.
    # When / Then — la construction du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(EDP_DEFAUT, **{champ: booleen})


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_colline_refuse_les_coordonnees_booleennes_a_levaluation(
    booleen: bool | np.bool_,
) -> None:
    """L'évaluation directe d'une colline exclut les coordonnées booléennes."""
    # Given — une colline valide et un point d'évaluation booléen.
    colline = COLLINE_1_DEFAUT
    # When / Then — l'évaluation du relief est refusée avant la conversion NumPy.
    with pytest.raises(ValueError, match="booléens exclus"):
        colline.altitude(booleen, 1600.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_concentrations_au_point_refuse_les_coordonnees_booleennes(
    booleen: bool | np.bool_,
) -> None:
    """L'évaluation publique des concentrations de relief exclut les booléens."""
    # Given — un scénario valide et un point d'évaluation booléen.
    # When / Then — l'évaluation est refusée avant les calculs de concentration.
    with pytest.raises(ValueError, match="booléens exclus"):
        concentrations_au_point(RELIEF_DEFAUT, booleen, 1600.0)


@pytest.mark.parametrize("booleen", [True, np.bool_(True)])
def test_scenario_superposition_refuse_les_mesures_booleennes(
    booleen: bool | np.bool_,
) -> None:
    """Les points de mesure du scénario de superposition excluent les booléens."""
    # Given — une mesure du scénario contenant une coordonnée booléenne.
    mesures = ((booleen, 400.0), *SUPERPOSITION_DEFAUT.mesures[1:])
    # When / Then — la validation du scénario est refusée.
    with pytest.raises(ValueError, match="booléens exclus"):
        replace(SUPERPOSITION_DEFAUT, mesures=mesures)
