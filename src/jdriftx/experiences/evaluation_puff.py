"""Évaluation dirigée d'une source impulsionnelle (puff) : étape 6.

Cette étape porte l'évaluation dirigée, reconstruite à l'étape 4 sur la
source continue du cas S0 (experiences/baseline_uniforme), sur une source
impulsionnelle (puff) évaluée sur la même grille de prélèvements. Le temps
dirigé τ est la pseudo-distance de référence uniforme (jdriftx.metric,
convention +inf en amont) ; la concentration est la solution fermée du
package (jdriftx.similitude.concentration_puff) ; le maximum temporel C(t)
est recherché sur une grille déterministe à deux niveaux, bornée à ]0, τ].

Étiquetage explicite, conformément à l'ordre confirmé de l'issue #232 :

- Héritage documentaire : l'évaluation dirigée d'une source impulsionnelle
  est « annoncée seulement » dans le chapitre « Reduced-Order Modelling of
  Dispersion » (Brun & Mohammadi, 2008, DOI 10.1007/978-1-4020-8758-5_14) ;
  aucun chiffre de l'ouvrage n'est utilisé comme cible.
- Reconstruction : temps dirigé par la pseudo-distance uniforme,
  concentration par la solution fermée du puff du package, maximum temporel
  sur deux grilles déterministes de 256 instants (couverture de ]0, τ], puis
  resserrage autour du maximum grossier).
- Extension : porte l'évaluation dirigée à une source impulsionnelle,
  première extension conditionnelle du contrat minimal (docs/47 §5),
  strictement hors périmètre de la baseline continue.

Garde-fous : l'évaluation est un contrôle de cohérence interne du package
sur un cas synthétique ; ce n'est pas une validation physique. Le maximum
temporel est évalué sur une grille déterministe : ce n'est pas le maximum
temporel exact du puff. Les ``dict`` restent confinés à la frontière
d'export JSON (``model_dump`` de Pydantic), conformément à la charte.
"""

from __future__ import annotations

import math
from importlib import metadata

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator

from jdriftx.benchmarks.cas import PointMesure
from jdriftx.metric import pseudo_distance_uniforme
from jdriftx.similitude import CLASSES, concentration_puff

__all__ = [
    "PUFF_DEFAUT",
    "EvaluationPuff",
    "ManifestePuff",
    "SourceImpulsionnelle",
    "construire_manifeste",
    "evaluer_grille",
    "evaluer_point",
    "temps_dirige",
    "temps_pic",
]

_TAILLE_GRILLE: int = 256
"""Taille de chaque niveau de la grille temporelle déterministe (2 × 256)."""


class SourceImpulsionnelle(BaseModel):
    """Source impulsionnelle (puff) : masse émise, vent uniforme, position.

    Attributs :
        masse : masse émise (kg), strictement positive.
        u : vitesse du vent uniforme (m s⁻¹), strictement positive.
        classe : classe de stabilité de Pasquill (A à F), partagée avec
            jdriftx.stabilite (source unique de vérité).
        x0 : position sous le vent de l'émission (m), positive ou nulle.
    """

    model_config = ConfigDict(frozen=True)

    masse: float = Field(gt=0.0)
    u: float = Field(gt=0.0)
    classe: str
    x0: float = Field(default=0.0, ge=0.0)

    @field_validator("classe")
    @classmethod
    def _classe_connue(cls, valeur: str) -> str:
        """Valide la classe contre le registre partagé, sinon ValueError."""
        if valeur not in CLASSES:
            msg = f"Classe de stabilité inconnue : {valeur!r} (attendu : {CLASSES})"
            raise ValueError(msg)
        return valeur


PUFF_DEFAUT: SourceImpulsionnelle = SourceImpulsionnelle(masse=1.0, u=3.0, classe="C", x0=0.0)
"""Puff de calibration : masse 1 kg, vent 3 m s⁻¹, classe C, émission en x0 = 0."""


class EvaluationPuff(BaseModel):
    """Évaluation dirigée du puff en un point de mesure.

    Attributs :
        point : point de mesure évalué (m).
        tau : temps dirigé τ du point (s), strictement positif.
        t_pic : instant du maximum temporel de grille (s).
        concentration_tau : concentration au temps dirigé C(τ) (kg m⁻³).
        concentration_pic : concentration au maximum de grille (kg m⁻³).
        ecart_relatif : écart C(τ)/C(t_pic) − 1, sans unité, négatif ou nul.
    """

    model_config = ConfigDict(frozen=True)

    point: PointMesure
    tau: float
    t_pic: float
    concentration_tau: float
    concentration_pic: float
    ecart_relatif: float


class ManifestePuff(BaseModel):
    """Manifeste de l'évaluation dirigée du puff (étape 6)."""

    model_config = ConfigDict(frozen=True)

    identifiant: str
    niveau_fidelite: str
    source: str
    heritage_documentaire: str
    reconstruction: str
    extension: str
    limites: tuple[str, ...]
    evaluations: tuple[EvaluationPuff, ...]
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


def _concentration(source: SourceImpulsionnelle, point: PointMesure, t: float) -> float:
    """Concentration du puff (kg m⁻³) au point de mesure, à l'instant t (s)."""
    valeur = concentration_puff(
        x=point.x,
        y=point.y,
        z=point.z,
        t=t,
        masse=source.masse,
        u=source.u,
        classe=source.classe,
        x0=source.x0,
    )
    return float(valeur)


def temps_dirige(source: SourceImpulsionnelle, point: PointMesure) -> float:
    """Temps dirigé τ (s) du point : pseudo-distance uniforme de l'émission.

    Le temps dirigé ne pénalise pas l'écart transversal (jdriftx.metric) ;
    un point strictement en amont de l'émission reçoit +inf.
    """
    return pseudo_distance_uniforme(
        (source.x0, 0.0),
        (point.x, point.y),
        (source.u, 0.0),
    )


def _tau_aval(source: SourceImpulsionnelle, point: PointMesure) -> float:
    """Temps dirigé fini du point, sinon ValueError (aval strict requis)."""
    tau = temps_dirige(source, point)
    if not math.isfinite(tau):
        msg = "Le point doit être strictement à l'aval de l'émission."
        raise ValueError(msg)
    return tau


def temps_pic(source: SourceImpulsionnelle, point: PointMesure, tau: float) -> float:
    """Instant du maximum de C(t) sur la grille déterministe à deux niveaux.

    Premier niveau : 256 instants couvrant ]0, τ]. Second niveau : 256
    instants autour du maximum grossier, bornés à ]0, τ]. La recherche est
    déterministe (np.linspace puis argmax) : le résultat n'est pas le
    maximum temporel exact du puff (limite étiquetée dans le manifeste).
    """
    grossier = np.linspace(tau / _TAILLE_GRILLE, tau, _TAILLE_GRILLE)
    concentrations_grossier = np.asarray([_concentration(source, point, t) for t in grossier])
    t_grossier = float(grossier[int(np.argmax(concentrations_grossier))])
    pas = tau / _TAILLE_GRILLE
    borne_inferieure = max(t_grossier - pas, tau / (2.0 * _TAILLE_GRILLE))
    borne_superieure = min(t_grossier + pas, tau)
    fin = np.linspace(borne_inferieure, borne_superieure, _TAILLE_GRILLE)
    concentrations_fin = np.asarray([_concentration(source, point, t) for t in fin])
    return float(fin[int(np.argmax(concentrations_fin))])


def evaluer_point(source: SourceImpulsionnelle, point: PointMesure) -> EvaluationPuff:
    """Évalue le puff au point : temps dirigé, pic de grille et écart relatif."""
    tau = _tau_aval(source, point)
    concentration_tau = _concentration(source, point, tau)
    t_pic = temps_pic(source, point, tau)
    concentration_pic = _concentration(source, point, t_pic)
    return EvaluationPuff(
        point=point,
        tau=tau,
        t_pic=t_pic,
        concentration_tau=concentration_tau,
        concentration_pic=concentration_pic,
        ecart_relatif=concentration_tau / concentration_pic - 1.0,
    )


def evaluer_grille(
    source: SourceImpulsionnelle,
    points: tuple[PointMesure, ...],
) -> tuple[EvaluationPuff, ...]:
    """Évalue le puff sur une grille de points, dans l'ordre de la grille."""
    return tuple(evaluer_point(source, point) for point in points)


def construire_manifeste(evaluations: tuple[EvaluationPuff, ...]) -> ManifestePuff:
    """Construit le manifeste étiqueté de l'évaluation (statuts figés).

    Le manifeste porte l'étiquetage héritage/reconstruction/extension et
    les limites explicites ; la version du code est lue dans les
    métadonnées d'installation si disponible, « non-installe » sinon.
    """
    try:
        version = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version = "non-installe"
    return ManifestePuff(
        identifiant="jdriftx-evaluation-puff-001",
        niveau_fidelite="R1",
        source=(
            "Chapitre « Reduced-Order Modelling of Dispersion » (Brun & "
            "Mohammadi, 2008), DOI 10.1007/978-1-4020-8758-5_14"
        ),
        heritage_documentaire=(
            "Évaluation dirigée d'une source impulsionnelle « annoncée "
            "seulement » dans le chapitre de 2008 ; l'ordre d'exécution et "
            "l'étiquetage suivent le contrat minimal (docs/47 §3.4). Aucun "
            "chiffre de l'ouvrage n'est utilisé comme cible."
        ),
        reconstruction=(
            "Temps dirigé tau = pseudo-distance uniforme (jdriftx.metric) ; "
            "concentration par la solution fermée du puff du package "
            "(jdriftx.similitude) ; maximum temporel sur une grille "
            "déterministe à deux niveaux de 256 instants sur ]0, tau]."
        ),
        extension=(
            "Source impulsionnelle : porte l'évaluation dirigée au puff sur "
            "la grille du cas S0 figé (docs/48 §2.2), première extension "
            "conditionnelle du contrat minimal (docs/47 §5), hors périmètre "
            "de la baseline continue."
        ),
        limites=(
            "Contrôle de cohérence interne du package sur un cas "
            "synthétique : pas une validation physique.",
            "Le maximum temporel est évalué sur une grille déterministe : "
            "ce n'est pas le maximum temporel exact du puff.",
            "L'isotropie longitudinale approchée (sigma_x = sigma_y) est "
            "celle de la solution fermée du package ; elle n'est pas "
            "revendiquée comme une physique validée.",
        ),
        evaluations=evaluations,
        version_code=version,
        commande=(
            "uv run python -c 'from jdriftx.benchmarks.cas import "
            "CAS_S0_DEFAUT; from jdriftx.experiences.evaluation_puff import "
            "PUFF_DEFAUT, construire_manifeste, evaluer_grille; "
            "print(construire_manifeste(evaluer_grille(PUFF_DEFAUT, "
            "CAS_S0_DEFAUT.points())))'"
        ),
    )
