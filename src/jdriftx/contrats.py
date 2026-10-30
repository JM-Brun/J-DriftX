"""Contrats et implémentations interopérables des composants du modèle.

Ce module conserve les chemins d'import historiques. Les protocoles et les
implémentations sont définis dans des modules dédiés pour séparer les
responsabilités sans casser l'API publique existante.
"""

from jdriftx._protocoles import ModeleConcentration, Relief, Vent
from jdriftx.concentrations import PanacheGaussien, SuperpositionPanaches
from jdriftx.reliefs import ReliefMntAscii, ReliefPlat, ReliefSynthetique
from jdriftx.vents import VentDeChampPlan, VentProfilPuissance, VentUniforme

__all__ = [
    "ModeleConcentration",
    "PanacheGaussien",
    "Relief",
    "ReliefMntAscii",
    "ReliefPlat",
    "ReliefSynthetique",
    "SuperpositionPanaches",
    "Vent",
    "VentDeChampPlan",
    "VentProfilPuissance",
    "VentUniforme",
]
