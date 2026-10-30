"""Vérifie la séparation des modules et la compatibilité des imports historiques."""

from jdriftx import (
    ModeleConcentration,
    PanacheGaussien,
    Relief,
    ReliefMntAscii,
    ReliefPlat,
    ReliefSynthetique,
    SuperpositionPanaches,
    Vent,
    VentDeChampPlan,
    VentProfilPuissance,
    VentUniforme,
)
from jdriftx._protocoles import (
    ModeleConcentration as ProtocoleConcentration,
    Relief as ProtocoleRelief,
    Vent as ProtocoleVent,
)
from jdriftx.concentrations import PanacheGaussien as ModelePanache
from jdriftx.contrats import (
    ModeleConcentration as ContratConcentration,
    PanacheGaussien as ContratPanache,
    Relief as ContratRelief,
    ReliefMntAscii as ContratReliefMnt,
    ReliefPlat as ContratReliefPlat,
    ReliefSynthetique as ContratReliefSynthetique,
    SuperpositionPanaches as ContratSuperposition,
    Vent as ContratVent,
    VentDeChampPlan as ContratVentChamp,
    VentProfilPuissance as ContratVentProfil,
    VentUniforme as ContratVentUniforme,
)
from jdriftx.reliefs import ReliefMntAscii as ModeleReliefMnt
from jdriftx.reliefs import ReliefPlat as ModeleReliefPlat
from jdriftx.reliefs import ReliefSynthetique as ModeleReliefSynthetique
from jdriftx.vents import VentDeChampPlan as ModeleVentChamp
from jdriftx.vents import VentProfilPuissance as ModeleVentProfil
from jdriftx.vents import VentUniforme as ModeleVentUniforme


def test_facade_historique_reexporte_les_implementations_canoniques() -> None:
    """Les anciens imports restent des alias des classes définies par domaine."""
    assert ContratPanache is ModelePanache is PanacheGaussien
    assert ContratSuperposition is SuperpositionPanaches
    assert ContratReliefMnt is ModeleReliefMnt is ReliefMntAscii
    assert ContratReliefPlat is ModeleReliefPlat is ReliefPlat
    assert ContratReliefSynthetique is ModeleReliefSynthetique is ReliefSynthetique
    assert ContratVentChamp is ModeleVentChamp is VentDeChampPlan
    assert ContratVentProfil is ModeleVentProfil is VentProfilPuissance
    assert ContratVentUniforme is ModeleVentUniforme is VentUniforme


def test_protocoles_publics_reexportent_les_protocoles_canoniques() -> None:
    """Les protocoles conservent leur identité à travers les deux façades publiques."""
    assert ContratRelief is ProtocoleRelief is Relief
    assert ContratVent is ProtocoleVent is Vent
    assert ContratConcentration is ProtocoleConcentration is ModeleConcentration
