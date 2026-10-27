"""Famille S0 : jeux synthétiques à vérité exacte pour la famille de similitude.

Cadre défini dans docs/21 (seconde vague de jeux de données et cas
synthétiques). Un cas S0 produit un jeu de données reproductible dont les
concentrations attendues sont exactes pour la famille de similitude du
panache gaussien. Les règles de docs/21 y sont respectées : générateur
versionné (VERSION_GENERATEUR), graine fixée par cas, partitions figées à
la construction, clause explicite de non-validation physique.

Un jeu S0 ne constitue PAS une validation physique : les vérités sont
exactes pour le modèle, pas pour l'atmosphère réelle. Les cas S0 servent
de socle reproductible aux familles S1 (vérités bruitées), S2 et S3
définies dans docs/21 ; ils ne valident aucune propriété physique.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from jdriftx.similitude import concentration_panache

VERSION_GENERATEUR = "s0-1"

CLAUSE_NON_VALIDATION = (
    "Jeu synthétique S0 : vérités exactes pour la famille de similitude du "
    "panache gaussien ; ceci n'est pas une validation physique."
)

FRACTION_CALIBRATION = 0.7


@dataclass(frozen=True)
class CasSynthetiqueS0:
    """Configuration figée d'un cas S0 (panache gaussien en champ uniforme).

    Attributes:
        identifiant: identifiant stable du cas, repris dans le manifeste.
        classe: classe de stabilité de Pasquill (A à F).
        debit: émission massique (kg s^-1), strictement positive.
        u: vitesse du vent (m s^-1), strictement positive.
        hauteur: hauteur effective de la source (m), positive ou nulle.
        altitude: altitude du plan de mesure (m).
        graine: graine du générateur, figée par cas.
        nombre_points: nombre de points du jeu, au moins 2.
        x_min: borne minimale des distances sous le vent (m), strictement positive.
        x_max: borne maximale des distances sous le vent (m), au-delà de x_min.
        y_max: demi-largeur latérale du domaine (m), strictement positive.
    """

    identifiant: str
    classe: str
    debit: float
    u: float
    hauteur: float
    altitude: float
    graine: int
    nombre_points: int
    x_min: float
    x_max: float
    y_max: float

    def __post_init__(self) -> None:
        """Valide les invariants du cas à la construction."""
        if not self.identifiant:
            msg = "L'identifiant du cas doit être non vide."
            raise ValueError(msg)
        if self.debit <= 0.0:
            msg = "Le débit doit être strictement positif."
            raise ValueError(msg)
        if self.u <= 0.0:
            msg = "La vitesse du vent doit être strictement positive."
            raise ValueError(msg)
        if self.hauteur < 0.0:
            msg = "La hauteur de la source doit être positive ou nulle."
            raise ValueError(msg)
        if self.nombre_points < 2:
            msg = "Le cas doit contenir au moins 2 points."
            raise ValueError(msg)
        if not 0.0 < self.x_min < self.x_max:
            msg = "Les bornes doivent vérifier 0 < x_min < x_max."
            raise ValueError(msg)
        if self.y_max <= 0.0:
            msg = "y_max doit être strictement positif."
            raise ValueError(msg)


@dataclass(frozen=True)
class PartitionS0:
    """Partition figée des indices d'un jeu S0.

    Invariants : calibration et evaluation sont disjointes et leur réunion
    couvre tous les indices du jeu.
    """

    calibration: tuple[int, ...]
    evaluation: tuple[int, ...]


@dataclass(frozen=True)
class DatasetS0:
    """Jeu de données S0 reproductible : points, vérités exactes, partition.

    Les concentrations sont les valeurs exactes de la famille de similitude
    aux points tirés : elles constituent une vérité exacte POUR LE MODÈLE,
    pas pour l'atmosphère réelle (voir CLAUSE_NON_VALIDATION).
    """

    cas: CasSynthetiqueS0
    points_x: np.ndarray
    points_y: np.ndarray
    concentrations: np.ndarray
    partition: PartitionS0

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste du jeu (frontière JSON uniquement)."""
        return {
            "identifiant": self.cas.identifiant,
            "version_generateur": VERSION_GENERATEUR,
            "clause": CLAUSE_NON_VALIDATION,
            "cas": {
                "classe": self.cas.classe,
                "debit": self.cas.debit,
                "u": self.cas.u,
                "hauteur": self.cas.hauteur,
                "altitude": self.cas.altitude,
                "graine": self.cas.graine,
                "nombre_points": self.cas.nombre_points,
                "x_min": self.cas.x_min,
                "x_max": self.cas.x_max,
                "y_max": self.cas.y_max,
            },
            "partition": {
                "calibration": list(self.partition.calibration),
                "evaluation": list(self.partition.evaluation),
            },
        }


def construire_partition(nombre_points: int, graine: int) -> PartitionS0:
    """Construit la partition figée : 70 % calibration, 30 % évaluation.

    La permutation des indices est déterminée par la graine ; le tri rend
    la partition indépendante de l'ordre de tirage.
    """
    generateur = np.random.default_rng(graine)
    permutation = generateur.permutation(nombre_points)
    taille_calibration = int(FRACTION_CALIBRATION * nombre_points)
    return PartitionS0(
        calibration=tuple(sorted(int(i) for i in permutation[:taille_calibration])),
        evaluation=tuple(sorted(int(i) for i in permutation[taille_calibration:])),
    )


def generer_dataset_s0(cas: CasSynthetiqueS0) -> DatasetS0:
    """Génère le jeu S0 : points déterministes et vérités exactes du modèle.

    Les points sont tirés uniformément dans le rectangle [x_min, x_max] x
    [-y_max, y_max] par le générateur versionné piloté par la graine du
    cas ; les concentrations attendues sont les valeurs exactes du
    panache gaussien (famille de similitude), pas des mesures.
    """
    generateur = np.random.default_rng(cas.graine)
    points_x = generateur.uniform(cas.x_min, cas.x_max, cas.nombre_points)
    points_y = generateur.uniform(-cas.y_max, cas.y_max, cas.nombre_points)
    concentrations = concentration_panache(
        points_x,
        points_y,
        cas.altitude,
        cas.debit,
        cas.u,
        cas.classe,
        cas.hauteur,
    )
    partition = construire_partition(cas.nombre_points, cas.graine)
    return DatasetS0(
        cas=cas,
        points_x=points_x,
        points_y=points_y,
        concentrations=np.asarray(concentrations, dtype=float),
        partition=partition,
    )


CAS_S0_DEFAUT = CasSynthetiqueS0(
    identifiant="jdriftx-s0-panache-d-001",
    classe="D",
    debit=1.0,
    u=3.0,
    hauteur=10.0,
    altitude=2.0,
    graine=20261027,
    nombre_points=200,
    x_min=50.0,
    x_max=5000.0,
    y_max=200.0,
)
