"""Vérifie la séparation des modules et la compatibilité des imports historiques."""

import importlib

import jdriftx._protocoles as protocoles
from jdriftx import concentrations, contrats, reliefs, vents

PACKAGE = importlib.import_module("jdriftx")


def test_facade_historique_reexporte_les_implementations_canoniques() -> None:
    """Les anciens imports restent des alias des classes définies par domaine."""
    assert contrats.PanacheGaussien is concentrations.PanacheGaussien is PACKAGE.PanacheGaussien
    assert contrats.SuperpositionPanaches is concentrations.SuperpositionPanaches
    assert contrats.ReliefMntAscii is reliefs.ReliefMntAscii is PACKAGE.ReliefMntAscii
    assert contrats.ReliefPlat is reliefs.ReliefPlat is PACKAGE.ReliefPlat
    assert contrats.ReliefSynthetique is reliefs.ReliefSynthetique is PACKAGE.ReliefSynthetique
    assert contrats.VentDeChampPlan is vents.VentDeChampPlan is PACKAGE.VentDeChampPlan
    assert contrats.VentProfilPuissance is vents.VentProfilPuissance is PACKAGE.VentProfilPuissance
    assert contrats.VentUniforme is vents.VentUniforme is PACKAGE.VentUniforme


def test_protocoles_publics_reexportent_les_protocoles_canoniques() -> None:
    """Les protocoles conservent leur identité à travers les deux façades publiques."""
    assert contrats.Relief is protocoles.Relief is PACKAGE.Relief
    assert contrats.Vent is protocoles.Vent is PACKAGE.Vent
    assert (
        contrats.ModeleConcentration
        is protocoles.ModeleConcentration
        is PACKAGE.ModeleConcentration
    )
