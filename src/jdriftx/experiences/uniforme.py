"""Tranche verticale « champ uniforme » : configuration, coût dirigé, résultats, manifeste.

Cette expérience relie les étapes de l'action 5 de la feuille de route
d'architecture : configuration typée → champ uniforme → coût dirigé →
résultats numériques → manifeste. Le coût dirigé est évalué par
``pseudo_distance_uniforme`` (l'implémentation partagée et testée), jamais
recalculé localement. Tous les objets sont immuables et validés à la
construction ; les ``dict`` restent confinés à la frontière d'export JSON
(``ManifesteScenario.vers_dict``), conformément à la charte qualité.

Le scénario par défaut est un cas jouet documenté : vent uniforme selon +x,
cible en aval avec un écart transversal. Ce livrable ne valide pas la
pseudo-distance dans un champ variable et ne constitue pas une reproduction
quantitative du chapitre de 2008 (cf. docs/17 et CONTRIBUTING.md).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

import numpy as np

from jdriftx.metric import pseudo_distance_uniforme

NiveauFidelite = Literal["R0", "R1", "R2"]


def _valide_point(nom: str, point: tuple[float, float]) -> None:
    """Lève ValueError si le point n'est pas un couple de coordonnées finies."""
    coordonnees = tuple(point)
    if len(coordonnees) != 2 or any(
        isinstance(valeur, (bool, np.bool_)) for valeur in coordonnees
    ):
        msg = f"Le point {nom} doit être un couple (x, y) numérique (booléens exclus)."
        raise ValueError(msg)
    if not all(math.isfinite(c) for c in coordonnees):
        msg = f"Le point {nom} doit être un couple (x, y) de coordonnées finies."
        raise ValueError(msg)


@dataclass(frozen=True)
class ChampUniforme:
    """Champ de vitesse constant 2D ; invariant : vecteur fini et non nul.

    Attributes:
        vent: composantes (ux, uy) en m s^-1, avec ‖u‖ > 0.
    """

    vent: tuple[float, float]

    def __post_init__(self) -> None:
        """Valide l'invariant : composantes finies et norme strictement positive."""
        vent = tuple(self.vent)
        if len(vent) != 2 or any(
            isinstance(composante, (bool, np.bool_)) for composante in vent
        ):
            msg = "Le vent doit contenir deux composantes numériques (booléens exclus)."
            raise ValueError(msg)
        if not all(math.isfinite(composante) for composante in vent):
            msg = "Le vent doit être un couple (ux, uy) de composantes finies."
            raise ValueError(msg)
        if math.hypot(vent[0], vent[1]) == 0.0:
            msg = "Le champ uniforme doit avoir une vitesse non nulle."
            raise ValueError(msg)

    @property
    def norme(self) -> float:
        """Norme du vent en m s^-1, strictement positive par invariant."""
        return math.hypot(self.vent[0], self.vent[1])


@dataclass(frozen=True)
class ScenarioUniforme:
    """Configuration immuable d'une expérience de coût dirigé en champ uniforme.

    Attributes:
        champ: champ de vitesse uniforme (m s^-1).
        origine: point de départ (x, y) en m.
        cible: point cible (x, y) en m.
    """

    champ: ChampUniforme
    origine: tuple[float, float]
    cible: tuple[float, float]

    def __post_init__(self) -> None:
        """Valide les points : couples de coordonnées finies."""
        _valide_point("origine", self.origine)
        _valide_point("cible", self.cible)


@dataclass(frozen=True)
class ResultatDirige:
    """Résultats numériques immuables d'un scénario en champ uniforme.

    Attributes:
        tau_origine_cible: coût dirigé origine → cible en s ; +inf si la cible est en amont.
        tau_cible_origine: coût dirigé cible → origine en s ; +inf si l'origine est en amont.
        distance_euclidienne: distance géométrique symétrique entre les deux points (m).
        ecart_transversal: distance perpendiculaire de la cible à la ligne de vent (m).
    """

    tau_origine_cible: float
    tau_cible_origine: float
    distance_euclidienne: float
    ecart_transversal: float


SCENARIO_DEFAUT = ScenarioUniforme(
    champ=ChampUniforme(vent=(2.0, 0.0)),
    origine=(0.0, 0.0),
    cible=(300.0, 65.0),
)


def resoudre_scenario(scenario: ScenarioUniforme) -> ResultatDirige:
    """Évalue un scénario de coût dirigé avec l'implémentation partagée.

    Args:
        scenario: configuration immuable (champ, origine, cible).

    Returns:
        Les coûts dirigés dans les deux sens, la distance euclidienne et
        l'écart transversal (produit vectoriel divisé par la norme du vent).
    """
    champ = scenario.champ
    dx = scenario.cible[0] - scenario.origine[0]
    dy = scenario.cible[1] - scenario.origine[1]
    return ResultatDirige(
        tau_origine_cible=pseudo_distance_uniforme(scenario.origine, scenario.cible, champ.vent),
        tau_cible_origine=pseudo_distance_uniforme(scenario.cible, scenario.origine, champ.vent),
        distance_euclidienne=math.hypot(dx, dy),
        ecart_transversal=abs(dx * champ.vent[1] - dy * champ.vent[0]) / champ.norme,
    )


@dataclass(frozen=True)
class ManifesteScenario:
    """Manifeste immuable reliant une expérience à sa spécification et ses limites.

    Attributes:
        identifiant: identifiant stable de l'expérience.
        niveau_fidelite: niveau de fidélité (R0 schéma, R1 reconstruction, R2 reproduction).
        source: référence documentée de la définition (DOI, page).
        description: objet de l'expérience en une phrase.
        hypothese: hypothèses explicites de l'expérience.
        limites: limites explicites du livrable.
        scenario: configuration typée de l'expérience.
        resultat: résultats numériques typés de l'expérience.
        version_code: version du package au moment de la construction.
        commande: commande de reproduction.
    """

    identifiant: str
    niveau_fidelite: NiveauFidelite
    source: str
    description: str
    hypothese: tuple[str, ...]
    limites: tuple[str, ...]
    scenario: ScenarioUniforme
    resultat: ResultatDirige
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire (frontière JSON uniquement)."""
        return {
            "identifiant": self.identifiant,
            "niveau_fidelite": self.niveau_fidelite,
            "source": self.source,
            "description": self.description,
            "hypothese": list(self.hypothese),
            "limites": list(self.limites),
            "version_code": self.version_code,
            "commande": self.commande,
            "parametres": {
                "vent": list(self.scenario.champ.vent),
                "origine": list(self.scenario.origine),
                "cible": list(self.scenario.cible),
            },
            "resultats": {
                "tau_origine_cible": self.resultat.tau_origine_cible,
                "tau_cible_origine": self.resultat.tau_cible_origine,
                "distance_euclidienne": self.resultat.distance_euclidienne,
                "ecart_transversal": self.resultat.ecart_transversal,
            },
        }


def construire_manifeste(
    scenario: ScenarioUniforme,
    resultat: ResultatDirige,
) -> ManifesteScenario:
    """Assemble le manifeste du scénario champ uniforme (métadonnées fixes).

    Args:
        scenario: configuration validée de l'expérience.
        resultat: résultats calculés par ``resoudre_scenario``.

    Returns:
        Le manifeste immuable, prêt pour la figure, l'export ou l'archivage.
    """
    try:
        version_code = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version_code = "non-installe"
    return ManifesteScenario(
        identifiant="jdriftx-uniforme-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, p. 253, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description="Coût dirigé entre deux points dans un champ de vent uniforme 2D.",
        hypothese=(
            "Champ de vitesse constant, non nul et indépendant du temps.",
            "Seule la projection longitudinale positive est facturée.",
            "L'écart transversal n'est pas pénalisé.",
        ),
        limites=(
            "Cas jouet synthétique : aucune donnée ni paramètre historique.",
            "Pas une métrique au sens strict (coût nul possible entre points distincts).",
            "Ne valide pas la pseudo-distance dans un champ variable.",
            "Coût amont noté +inf : l'export JSON n'est pas strictement conforme RFC 8259.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.uniforme import "
            "SCENARIO_DEFAUT, resoudre_scenario; print(resoudre_scenario(SCENARIO_DEFAUT))'"
        ),
    )
