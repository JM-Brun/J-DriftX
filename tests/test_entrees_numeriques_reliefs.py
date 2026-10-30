"""Regressions des contrats numeriques des reliefs et concentrations."""

import numpy as np
import pytest

from jdriftx.concentrations import PanacheGaussien
from jdriftx.reliefs import ReliefMntAscii, ReliefSynthetique
from jdriftx.source import SourcePanache


@pytest.mark.parametrize("valeur", ["1.0", None, 1 + 0j, True, float("nan"), float("inf")])
@pytest.mark.parametrize("champ", ["height", "width", "center_x", "center_y"])
def test_relief_synthetique_rejette_les_parametres_invalides(
    champ: str, valeur: object
) -> None:
    """Les paramètres de relief exigent des scalaires reels finis."""
    parametres: dict[str, object] = {
        "kind": "hill",
        "height": 1.0,
        "width": 1.5,
        "center_x": 0.0,
        "center_y": 0.0,
    }
    parametres[champ] = valeur
    with pytest.raises(ValueError, match=r"nombre reel|fini"):
        ReliefSynthetique(**parametres)  # type: ignore[arg-type]


def test_relief_synthetique_normalise_les_parametres_reels() -> None:
    relief = ReliefSynthetique(kind="hill", height=-2, width=3, center_x=1, center_y=0)
    assert type(relief.height) is float
    assert relief.height == -2.0
    assert type(relief.width) is float


@pytest.mark.parametrize("altitudes", [["1", "2"], [[True, False]], [[1 + 0j]], [[object()]]])
def test_mnt_rejette_les_grilles_non_reelles(altitudes: object) -> None:
    with pytest.raises(ValueError, match="tableau numerique reel"):
        ReliefMntAscii(altitudes=altitudes, x0=0.0, y0=0.0, pas=1.0)  # type: ignore[arg-type]


def test_mnt_normalise_la_geometrie_et_la_grille() -> None:
    mnt = ReliefMntAscii(altitudes=[[1, 2], [3, 4]], x0=0, y0=0, pas=1)
    assert mnt.altitudes.dtype == np.float64
    assert type(mnt.x0) is float
    assert type(mnt.y0) is float
    assert type(mnt.pas) is float


@pytest.mark.parametrize("champ", ["x0", "y0", "pas", "sans_donnee"])
@pytest.mark.parametrize("valeur", ["1.0", 1 + 0j, True, float("nan"), float("inf")])
def test_mnt_rejette_les_parametres_geometriques_invalides(champ: str, valeur: object) -> None:
    parametres: dict[str, object] = {
        "altitudes": [[1.0, 2.0], [3.0, 4.0]],
        "x0": 0.0,
        "y0": 0.0,
        "pas": 1.0,
        "sans_donnee": None,
    }
    parametres[champ] = valeur
    with pytest.raises(ValueError, match=r"nombre reel|fini"):
        ReliefMntAscii(**parametres)  # type: ignore[arg-type]


@pytest.mark.parametrize("coordonnees", ["1.0", [1 + 0j], [True], [float("nan")]])
def test_altitude_rejette_les_coordonnees_non_reelles(coordonnees: object) -> None:
    relief = ReliefSynthetique(kind="hill")
    with pytest.raises(ValueError, match=r"tableau numerique reel|valeurs finies"):
        relief.altitude(coordonnees, [0.0])  # type: ignore[arg-type]


@pytest.mark.parametrize("coordonnees", ["1.0", [1 + 0j], [True], [float("nan")]])
def test_mnt_altitude_rejette_les_coordonnees_non_reelles(coordonnees: object) -> None:
    mnt = ReliefMntAscii(altitudes=[[1.0, 2.0], [3.0, 4.0]], x0=0.0, y0=0.0, pas=1.0)
    with pytest.raises(ValueError, match=r"tableau numerique reel|valeurs finies"):
        mnt.altitude(coordonnees, [0.0])  # type: ignore[arg-type]


def test_panache_gaussien_refuse_une_source_de_mauvais_type_a_la_construction() -> None:
    with pytest.raises(TypeError, match="instance de SourcePanache"):
        PanacheGaussien(source=object())  # type: ignore[arg-type]


def test_panache_gaussien_accepte_une_source_valide() -> None:
    source = SourcePanache(debit=1.0, u=3.0, classe="D", hauteur=10.0)
    assert isinstance(PanacheGaussien(source=source), PanacheGaussien)
