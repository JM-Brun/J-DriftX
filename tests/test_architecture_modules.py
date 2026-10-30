"""Vérifie la séparation des modules et la compatibilité des imports historiques."""

import importlib

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
from jdriftx.reliefs import (
    ReliefMntAscii as ModeleReliefMnt,
    ReliefPlat as ModeleReliefPlat,
    ReliefSynthetique as ModeleReliefSynthetique,
)
from jdriftx.vents import (
    VentDeChampPlan as ModeleVentChamp,
    VentProfilPuissance as ModeleVentProfil,
    VentUniforme as ModeleVentUniforme,
)

PACKAGE = importlib.import_module("jdriftx")


def test_facade_historique_reexporte_les_implementations_canoniques() -> None:
    """Les anciens imports restent des alias des classes définies par domaine."""
    assert ContratPanache is ModelePanache is PACKAGE.PanacheGaussien
    assert ContratSuperposition is PACKAGE.SuperpositionPanaches
    assert ContratReliefMnt is ModeleReliefMnt is PACKAGE.ReliefMntAscii
    assert ContratReliefPlat is ModeleReliefPlat is PACKAGE.ReliefPlat
    assert ContratReliefSynthetique is ModeleReliefSynthetique is PACKAGE.ReliefSynthetique
    assert ContratVentChamp is ModeleVentChamp is PACKAGE.VentDeChampPlan
    assert ContratVentProfil is ModeleVentProfil is PACKAGE.VentProfilPuissance
    assert ContratVentUniforme is ModeleVentUniforme is PACKAGE.VentUniforme


def test_protocoles_publics_reexportent_les_protocoles_canoniques() -> None:
    """Les protocoles conservent leur identité à travers les deux façades publiques."""
    assert ContratRelief is ProtocoleRelief is PACKAGE.Relief
    assert ContratVent is ProtocoleVent is PACKAGE.Vent
    assert ContratConcentration is ProtocoleConcentration is PACKAGE.ModeleConcentration
