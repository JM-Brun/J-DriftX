"""Reconstruction de l'évaluation ponctuelle via le temps de transport dirigé.

Cette tranche réalise l'étape 4 de l'ordre confirmé de l'issue #232 sur le
cas de référence autonome (docs/48) : implémenter et tester la
reconstruction de l'évaluation ponctuelle du mécanisme, en séparant
l'héritage documentaire, la reconstruction corrigée et les extensions
modernes (stratégie de reprise, note 44 §2) :

- héritage documentaire : l'évaluation ponctuelle est annoncée par le
  chapitre de 2008 ; son statut est figé « annoncée seulement » par le
  contrat minimal de la baseline (docs/47 §3.4). Aucun code historique
  n'a été relu, aucune fidélité historique n'est revendiquée ;
- reconstruction : cette implémentation compose uniquement des primitives
  partagées et testées — le coût dirigé ``pseudo_distance_uniforme``
  (metric.py) et le contrat de concentration ``PanacheGaussien``
  (contrats.py, docs/42) — sans dupliquer aucune formule ; le cas consommé
  est défini par l'interface ``CasReferenceUniforme`` (PEP 544), pas par
  la classe concrète ``CasS0`` ;
- extension : aucune (ni champ multi-niveaux, ni assimilation).

Le mécanisme reconstruit sur le cas S0 figé (``CAS_S0_DEFAUT``, docs/48
§2.2) : pour un point cible à l'aval, le temps de transport dirigé τ est
évalué par le coût dirigé partagé (amont rejeté à +inf), l'abscisse aval
est reconstruite par la carte travel-time x = U·τ (note 37 : u·∇τ = 1
exact dans le cas uniforme), puis la concentration est évaluée par le
contrat de concentration au point reconstruit. Dans le cas uniforme, cette
évaluation coïncide avec la vérité du cas S0 (docs/48 §2.5) : c'est un
contrôle d'auto-cohérence du pipeline, pas une validation physique
(docs/21, issue #43) ni une reproduction du comportement historique en
champ variable. Tous les objets sont immuables et validés à la
construction ; les ``dict`` restent confinés à la frontière d'export JSON
(``ManifesteBaseline.vers_dict``, builtin Pydantic ``model_dump``),
conformément à la charte qualité.
"""

from __future__ import annotations

import math
from importlib import metadata
from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict

from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, CasS0, PointMesure
from jdriftx.contrats import PanacheGaussien
from jdriftx.metric import pseudo_distance_uniforme
from jdriftx.source import SourcePanache

__all__ = [
    "CAS_REFERENCE_DEFAUT",
    "CasReferenceUniforme",
    "EvaluationDirigee",
    "ManifesteBaseline",
    "NiveauFidelite",
    "construire_manifeste",
    "evaluer_grille",
    "evaluer_point",
    "temps_dirige",
]

NiveauFidelite = Literal["R0", "R1", "R2"]

ORIGINE: tuple[float, float] = (0.0, 0.0)


@runtime_checkable
class CasReferenceUniforme(Protocol):
    """Contrat du cas de référence uniforme consommé par la reconstruction.

    Interface PEP 544 : tout objet portant une source de panache validée
    (docs/41) et exposant une grille ordonnée de points de mesure satisfait
    le contrat, sans héritage. La reconstruction (temps dirigé, évaluation
    ponctuelle) ne dépend plus de la classe concrète ``CasS0`` : elle
    exige seulement ce contrat, conformément aux frontières stables de
    docs/42.
    """

    source: SourcePanache

    def points(self) -> tuple[PointMesure, ...]:
        """Grille ordonnée et non vide des points de mesure (m)."""
        ...


class EvaluationDirigee(BaseModel):
    """Évaluation ponctuelle reconstruite en un point de mesure.

    Modèle Pydantic gelé : types validés à la construction, immuabilité
    portée par la configuration gelée (charte qualité).

    Attributes:
        point: point cible de l'évaluation (m).
        tau: temps de transport dirigé origine → point (s) ; +inf si amont.
        x_aval: abscisse aval reconstruite U·τ (m), égale à point.x à la
            précision machine dans le cas uniforme.
        concentration: concentration (kg m^-3) évaluée au point reconstruit.
    """

    model_config = ConfigDict(frozen=True)

    point: PointMesure
    tau: float
    x_aval: float
    concentration: float


class ManifesteBaseline(BaseModel):
    """Manifeste immuable reliant la reconstruction à ses statuts et limites.

    Modèle Pydantic gelé : la validation des types et l'export JSON
    (builtin ``model_dump``) sont fournis par le modèle, l'immuabilité par
    la configuration gelée — aucune logique d'export écrite à la main.

    Attributes:
        identifiant: identifiant stable de l'expérience.
        niveau_fidelite: niveau de fidélité (R1 = reconstruction).
        source: référence documentée de la définition.
        heritage_documentaire: revendication historique, avec son statut figé.
        reconstruction: ce que cette implémentation reconstruit.
        extension: extensions modernes incluses (aucune ici).
        hypothese: hypothèses explicites de l'expérience.
        limites: limites explicites du livrable.
        cas: cas de référence évalué (docs/48 §2.2).
        evaluations: évaluations dirigées sur la grille du cas.
        version_code: version du package au moment de la construction.
        commande: commande de reproduction.
    """

    model_config = ConfigDict(frozen=True)

    identifiant: str
    niveau_fidelite: NiveauFidelite
    source: str
    heritage_documentaire: str
    reconstruction: str
    extension: str
    hypothese: tuple[str, ...]
    limites: tuple[str, ...]
    cas: CasS0
    evaluations: tuple[EvaluationDirigee, ...]
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire (frontière JSON uniquement)."""
        return self.model_dump()


CAS_REFERENCE_DEFAUT: CasS0 = CAS_S0_DEFAUT


def temps_dirige(cas: CasReferenceUniforme, point: PointMesure) -> float:
    """Temps de transport dirigé origine → point, par le coût partagé.

    Args:
        cas: cas satisfaisant le contrat ``CasReferenceUniforme`` (source
            validée, jamais revalidée ici).
        point: point cible de l'évaluation (m).

    Returns:
        τ en secondes (docs/48 §2.6), ou +inf si le point est en amont :
        convention explicite du coût dirigé partagé (metric.py).
    """
    return pseudo_distance_uniforme(ORIGINE, (point.x, point.y), (cas.source.u, 0.0))


def evaluer_point(cas: CasReferenceUniforme, point: PointMesure) -> EvaluationDirigee:
    """Évalue le mécanisme reconstruit au point cible.

    Args:
        cas: cas satisfaisant le contrat ``CasReferenceUniforme``.
        point: point cible, strictement à l'aval (x > 0).

    Returns:
        L'évaluation dirigée : τ, abscisse reconstruite et concentration.

    Raises:
        ValueError: si le point est en amont (τ non fini) : le mécanisme
            dirigé ne l'atteint pas, la reconstruction refuse d'évaluer.
    """
    tau = temps_dirige(cas, point)
    if not math.isfinite(tau):
        msg = "Le point est en amont : le mécanisme dirigé ne l'atteint pas (tau = +inf)."
        raise ValueError(msg)
    x_aval = cas.source.u * tau
    panache = PanacheGaussien(source=cas.source)
    valeur = panache.concentration(x_aval, point.y, point.z)
    return EvaluationDirigee(point=point, tau=tau, x_aval=x_aval, concentration=float(valeur))


def evaluer_grille(cas: CasReferenceUniforme) -> tuple[EvaluationDirigee, ...]:
    """Évalue le mécanisme reconstruit sur la grille de prélèvements du cas.

    Args:
        cas: cas satisfaisant le contrat ``CasReferenceUniforme``.

    Returns:
        Une évaluation dirigée par point de la grille, dans l'ordre du cas.
    """
    return tuple(evaluer_point(cas, point) for point in cas.points())


def construire_manifeste(
    cas: CasS0,
    evaluations: tuple[EvaluationDirigee, ...],
) -> ManifesteBaseline:
    """Assemble le manifeste de la reconstruction (métadonnées fixes).

    Args:
        cas: cas de référence évalué.
        evaluations: évaluations dirigées produites par ``evaluer_grille``.

    Returns:
        Le manifeste immuable, prêt pour l'export ou l'archivage.
    """
    try:
        version_code = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version_code = "non-installe"
    return ManifesteBaseline(
        identifiant="jdriftx-baseline-uniforme-001",
        niveau_fidelite="R1",
        source=(
            "Cas de référence autonome docs/48 §2.5-2.6 ; "
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, p. 253, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        heritage_documentaire=(
            "Évaluation ponctuelle annoncée par le chapitre de 2008 : statut « annoncée "
            "seulement » (contrat docs/47 §3.4) ; aucun code historique relu, aucune "
            "revendication de fidélité historique."
        ),
        reconstruction=(
            "Cette implémentation : coût dirigé partagé pseudo_distance_uniforme "
            "(τ = x/U, rejet amont à +inf), carte travel-time x = U·τ (note 37), évaluation "
            "par le contrat de concentration PanacheGaussien (contrats.py, docs/42) sur la "
            "grille du cas S0 figé ; le cas consommé est défini par l'interface "
            "CasReferenceUniforme (PEP 544)."
        ),
        extension=(
            "Aucune : ni champ multi-niveaux, ni évaluation réduite revendiquée, ni assimilation."
        ),
        hypothese=(
            "Vent uniforme horizontal (U, 0, 0), U > 0 strictement (docs/48 §2.1).",
            "Scalaire passif, stationnaire, sans réaction ni dépôt (H1, H3, H5).",
            "Source ponctuelle continue à l'origine, hauteur H (docs/48 §2.2).",
            "Points cibles strictement à l'aval de la source (x > 0).",
        ),
        limites=(
            "Cas uniforme uniquement : la coïncidence τ-évaluation est propre à ce cas "
            "(note 37 ; contre-exemple du cisaillement distinct, docs/48 §5).",
            "Contrôle d'auto-cohérence du pipeline, pas une validation physique "
            "(docs/21, issue #43).",
            "Pas une reproduction du comportement historique en champ variable.",
            "Le coût dirigé partagé est une référence analytique limitée au champ uniforme "
            "(metric.py), pas une implémentation générale des caractéristiques.",
            "Aucune comparaison à référence indépendante (étape 5) ni revendication de coût.",
        ),
        cas=cas,
        evaluations=evaluations,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.baseline_uniforme import "
            "CAS_REFERENCE_DEFAUT, evaluer_grille; print(evaluer_grille(CAS_REFERENCE_DEFAUT))'"
        ),
    )
