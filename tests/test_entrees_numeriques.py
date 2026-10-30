"""Regressions des contrats numeriques de SourcePanache et des adaptateurs de vent."""

from typing import cast

import numpy as np
import pytest

from jdriftx._protocoles import Vent
from jdriftx.champ_analytique import ChampPlan
from jdriftx.source import SourcePanache
from jdriftx.vents import (
    AdaptateurTrajectoire2D,
    VentDeChampPlan,
    VentProfilPuissance,
    VentUniforme,
)


@pytest.mark.parametrize("valeur", ["1.0", None, 1 + 0j, True, object()])
@pytest.mark.parametrize("champ", ["debit", "u", "hauteur"])
def test_source_rejette_les_types_numeriques_non_contractuels(champ: str, valeur: object) -> None:
    """Les champs numeriques de source exigent un scalaire reel, hors booleen."""
    parametres: dict[str, object] = {
        "debit": 1.0,
        "u": 3.0,
        "classe": "D",
        "hauteur": 10.0,
    }
    parametres[champ] = valeur
    with pytest.raises(ValueError, match="nombre reel"):
        SourcePanache(**parametres)  # type: ignore[arg-type]


def test_source_normalise_les_scalaires_reels_en_float() -> None:
    """Les nombres reels acceptes sont stockes sous forme de float."""
    source = SourcePanache(debit=1, u=np.float64(3.0), classe="D", hauteur=10)
    assert type(source.debit) is float
    assert type(source.u) is float
    assert type(source.hauteur) is float


def test_source_normalise_le_debordement_de_conversion() -> None:
    """Un entier trop grand pour float produit ValueError, pas OverflowError."""
    with pytest.raises(ValueError, match="representable"):
        SourcePanache(debit=10**10000, u=3.0, classe="D", hauteur=10.0)


@pytest.mark.parametrize("valeur", [float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("champ", ["debit", "u", "hauteur"])
def test_source_rejette_les_reels_non_finis(champ: str, valeur: float) -> None:
    """Les conversions vers float ne doivent jamais laisser passer NaN ou infini."""
    parametres: dict[str, object] = {
        "debit": 1.0,
        "u": 3.0,
        "classe": "D",
        "hauteur": 10.0,
    }
    parametres[champ] = valeur
    with pytest.raises(ValueError, match="fini"):
        SourcePanache(**parametres)  # type: ignore[arg-type]


@pytest.mark.parametrize("classe", [None, 1, [], "Z"])
def test_source_normalise_les_erreurs_de_classe(classe: object) -> None:
    """Une classe non reconnue produit toujours ValueError."""
    with pytest.raises(ValueError, match="Classe de stabilite invalide"):
        SourcePanache(debit=1.0, u=3.0, classe=classe, hauteur=10.0)  # type: ignore[arg-type]


@pytest.mark.parametrize("valeur", ["2.0", None, 2 + 0j, True, float("nan"), float("inf")])
def test_vent_uniforme_rejette_les_composantes_invalides(valeur: object) -> None:
    """Les composantes constantes sont des scalaires reels finis, booleens exclus."""
    with pytest.raises(ValueError):
        VentUniforme(u=valeur, v=1.0)  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["u_reference", "z_reference", "exposant"])
@pytest.mark.parametrize("valeur", ["1.0", None, 1 + 0j, True, float("nan"), float("inf")])
def test_profil_puissance_rejette_les_parametres_non_reels(
    champ: str, valeur: object
) -> None:
    """Les parametres du profil exigent des scalaires reels finis."""
    parametres: dict[str, object] = {
        "u_reference": 5.0,
        "z_reference": 10.0,
        "exposant": 0.15,
    }
    parametres[champ] = valeur
    with pytest.raises(ValueError):
        VentProfilPuissance(**parametres)  # type: ignore[arg-type]


@pytest.mark.parametrize("z", ["10.0", None, 10 + 0j, True, float("nan"), float("inf")])
def test_profil_puissance_rejette_les_entrees_z_non_reelles(z: object) -> None:
    """La hauteur evaluee suit le meme contrat numerique que les parametres."""
    vent = VentProfilPuissance(u_reference=5.0, z_reference=10.0, exposant=0.15)
    with pytest.raises(ValueError):
        vent.vitesse(0.0, 0.0, z)  # type: ignore[arg-type]


def test_adaptateur_trajectoire_accepte_une_hauteur_negative_finie() -> None:
    """L'adaptateur impose la finitude, pas une borne physique non documentee."""
    adaptateur = AdaptateurTrajectoire2D(vent=VentUniforme(2.0, -1.0), hauteur=-5.0)
    assert adaptateur(0.0, 1.0, 2.0) == (2.0, -1.0)
    assert adaptateur.hauteur == -5.0


@pytest.mark.parametrize("hauteur", ["5.0", None, 5 + 0j, True, float("nan"), float("inf")])
def test_adaptateur_trajectoire_rejette_les_hauteurs_non_reelles(hauteur: object) -> None:
    """La hauteur doit etre un scalaire reel fini, mais peut etre negative."""
    with pytest.raises(ValueError):
        AdaptateurTrajectoire2D(vent=VentUniforme(1.0, 0.0), hauteur=hauteur)  # type: ignore[arg-type]


class _VentSortieInvalide:
    """Vent structurel de test qui viole le type de ses composantes."""

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        return ("2.0", 1.0, 0.0)  # type: ignore[return-value]


def test_adaptateur_trajectoire_normalise_les_sorties_non_numeriques() -> None:
    """Une sortie de vent mal typee produit ValueError a la frontiere adaptateur."""
    adaptateur = AdaptateurTrajectoire2D(vent=cast(Vent, _VentSortieInvalide()), hauteur=2.0)
    with pytest.raises(ValueError, match="nombre reel"):
        adaptateur(0.0, 1.0, 2.0)


class _ChampSortieInvalide:
    """Champ plan structurel de test qui viole le type de ses composantes."""

    def fonction_courant(self, x: float, y: float) -> float:
        return 0.0

    def vitesse(self, x: float, y: float) -> tuple[float, float]:
        return (1.0, complex(0.0, 1.0))  # type: ignore[return-value]


def test_adaptateur_champ_plan_normalise_les_sorties_complexes() -> None:
    """Une composante complexe ne doit pas traverser l'adaptateur de champ plan."""
    adaptateur = VentDeChampPlan(champ=cast(ChampPlan, _ChampSortieInvalide()))
    with pytest.raises(ValueError, match="nombre reel"):
        adaptateur.vitesse(0.0, 0.0, 0.0)


def test_adaptateur_trajectoire_refuse_un_tuple_de_taille_incorrecte() -> None:
    """Le contrat Vent attend exactement trois composantes dans un tuple."""

    class VentMalForme:
        def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
            return (1.0, 2.0)  # type: ignore[return-value]

    adaptateur = AdaptateurTrajectoire2D(vent=cast(Vent, VentMalForme()), hauteur=2.0)
    with pytest.raises(ValueError, match="tuple de 3 composantes"):
        adaptateur(0.0, 1.0, 2.0)
