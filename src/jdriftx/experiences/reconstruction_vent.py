"""Reconstruction du vent à deux mesures : l'interpolation n'est pas unique.

Cette expérience porte l'étape B du plan de figures du chapitre de 2008 :
montrer qu'un champ interpolé à partir de deux mesures ponctuelles n'est pas
unique. Deux champs incompressibles très différents, un champ cellulaire
périodique (choix 1) et sa superposition avec une perturbation de plus
petite longueur d'onde (choix 2), coïncident exactement aux deux points de
mesure du scénario ; hors de ces points, ils diffèrent nettement.

Le livrable est conceptuel (niveau R1) : cas synthétique sans donnée
historique, pas une reproduction quantitative du chapitre de 2008. Tous
les objets sont immuables et validés à la construction ; les ``dict``
restent confinés à la frontière d'export JSON, conformément à la charte
qualité du dépôt.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

import numpy as np

from jdriftx.champ_analytique import ChampFonctionCourant, ChampPlan, SuperpositionChamps

NiveauFidelite = Literal["R0", "R1", "R2"]

_COTE_FENETRE = 2000.0
_PAS_GRILLE = 100.0
_PAS_DERIVEE = 1.0


def _valide_point(nom: str, point: tuple[float, float]) -> None:
    """Lève ValueError si le point n'est pas un couple de coordonnées finies."""
    coordonnees = tuple(point)
    if len(coordonnees) != 2 or any(isinstance(valeur, (bool, np.bool_)) for valeur in coordonnees):
        msg = f"Le point {nom} doit être un couple de coordonnées numériques (booléens exclus)."
        raise ValueError(msg)
    if not all(math.isfinite(c) for c in coordonnees):
        msg = f"Le point {nom} doit être un couple de coordonnées finies."
        raise ValueError(msg)


@dataclass(frozen=True)
class Rectangle:
    """Rectangle immuable aligné sur les axes, en mètres.

    Attributes:
        coin: coin (x, y) de coordonnées finies.
        largeur: largeur en m, finie et strictement positive.
        hauteur: hauteur en m, finie et strictement positive.
    """

    coin: tuple[float, float]
    largeur: float
    hauteur: float

    def __post_init__(self) -> None:
        """Valide le coin et des dimensions finies strictement positives."""
        _valide_point("coin", self.coin)
        dimensions = (self.largeur, self.hauteur)
        if any(isinstance(valeur, (bool, np.bool_)) for valeur in dimensions):
            msg = "La largeur et la hauteur doivent être numériques (booléens exclus)."
            raise ValueError(msg)
        if not all(math.isfinite(d) and d > 0.0 for d in dimensions):
            msg = "La largeur et la hauteur doivent être finies et strictement positives."
            raise ValueError(msg)

    @property
    def surface(self) -> float:
        """Surface du rectangle en m²."""
        return self.largeur * self.hauteur

    def contient(self, point: tuple[float, float]) -> bool:
        """Indique si le point appartient au rectangle, frontière incluse."""
        _valide_point("point", point)
        x, y = point
        return (
            self.coin[0] <= x <= self.coin[0] + self.largeur
            and self.coin[1] <= y <= self.coin[1] + self.hauteur
        )


@dataclass(frozen=True)
class ScenarioReconstruction:
    """Configuration immuable d'une reconstruction du vent à deux mesures.

    Attributes:
        champ_choix_1: premier champ candidat (champ cellulaire).
        champ_choix_2: second champ candidat (superposition).
        mesures: exactement deux points de mesure (x, y) en m, distincts.
        parcelle: rectangle de la parcelle de référence, dans le domaine.
        domaine: rectangle du domaine d'étude.
        trajectoire: polyligne relevée au sol, dans la parcelle.
    """

    champ_choix_1: ChampFonctionCourant
    champ_choix_2: SuperpositionChamps
    mesures: tuple[tuple[float, float], ...]
    parcelle: Rectangle
    domaine: Rectangle
    trajectoire: tuple[tuple[float, float], ...]

    def __post_init__(self) -> None:
        """Valide les mesures, la parcelle et la trajectoire."""
        if len(self.mesures) != 2:
            msg = "Le scénario exige exactement deux mesures."
            raise ValueError(msg)
        for mesure in self.mesures:
            _valide_point("mesure", mesure)
        if self.mesures[0] == self.mesures[1]:
            msg = "Les deux points de mesure doivent être distincts."
            raise ValueError(msg)
        if not all(self.domaine.contient(mesure) for mesure in self.mesures):
            msg = "Les points de mesure doivent être dans le domaine."
            raise ValueError(msg)
        coins = (
            self.parcelle.coin,
            (self.parcelle.coin[0] + self.parcelle.largeur, self.parcelle.coin[1]),
            (self.parcelle.coin[0], self.parcelle.coin[1] + self.parcelle.hauteur),
            (
                self.parcelle.coin[0] + self.parcelle.largeur,
                self.parcelle.coin[1] + self.parcelle.hauteur,
            ),
        )
        if not all(self.domaine.contient(coin) for coin in coins):
            msg = "La parcelle doit être entièrement contenue dans le domaine."
            raise ValueError(msg)
        if len(self.trajectoire) < 2:
            msg = "La trajectoire doit contenir au moins deux points."
            raise ValueError(msg)
        for point in self.trajectoire:
            _valide_point("trajectoire", point)
            if not self.parcelle.contient(point):
                msg = "Les points de la trajectoire doivent être dans la parcelle."
                raise ValueError(msg)
        for avant, apres in zip(self.trajectoire, self.trajectoire[1:], strict=False):
            if avant == apres:
                msg = "Deux points consécutifs de la trajectoire doivent être distincts."
                raise ValueError(msg)


@dataclass(frozen=True)
class ResultatReconstruction:
    """Résultats numériques immuables d'une reconstruction à deux mesures.

    Attributes:
        vent_mesure_1: vent du choix 1 à la première mesure, en m s^-1.
        vent_mesure_2: vent du choix 1 à la seconde mesure, en m s^-1.
        ecart_entre_choix: écart maximal entre les deux choix aux mesures (m s^-1).
        divergence_max_choix_1: divergence numérique maximale du choix 1,
            mesurée sur la fenêtre d'évaluation (côté 2000 m, pas 100 m), en s^-1.
        divergence_max_choix_2: divergence numérique maximale du choix 2,
            mesurée sur la fenêtre d'évaluation (côté 2000 m, pas 100 m), en s^-1.
        longueur_trajectoire: longueur de la polyligne relevée au sol (m).
    """

    vent_mesure_1: tuple[float, float]
    vent_mesure_2: tuple[float, float]
    ecart_entre_choix: float
    divergence_max_choix_1: float
    divergence_max_choix_2: float
    longueur_trajectoire: float


CHAMP_CHOIX_1 = ChampFonctionCourant(amplitude=800.0, longueur=1000.0)
PERTURBATION = ChampFonctionCourant(amplitude=400.0, longueur=500.0)
CHAMP_CHOIX_2 = SuperpositionChamps((CHAMP_CHOIX_1, PERTURBATION))

SCENARIO_DEFAUT = ScenarioReconstruction(
    champ_choix_1=CHAMP_CHOIX_1,
    champ_choix_2=CHAMP_CHOIX_2,
    mesures=((250.0, 500.0), (750.0, 500.0)),
    parcelle=Rectangle(coin=(150.0, 550.0), largeur=100.0, hauteur=100.0),
    domaine=Rectangle(coin=(0.0, 0.0), largeur=20000.0, hauteur=20000.0),
    trajectoire=((150.0, 575.0), (250.0, 575.0), (250.0, 625.0), (150.0, 625.0)),
)


def _divergence_numerique_max(champ: ChampPlan) -> float:
    """Estime la divergence maximale d'un champ par différences centrées.

    La divergence est évaluée sur la grille régulière couvrant la fenêtre
    d'affichage (côté 2000 m, pas 100 m) avec un pas de différenciation de
    1 m ; pour un champ à fonction de courant, elle est nulle aux erreurs
    d'arrondi près.

    Args:
        champ: champ plan stationnaire.

    Returns:
        La valeur absolue maximale de la divergence estimée sur la grille.
    """
    h = _PAS_DERIVEE
    nombre = int(_COTE_FENETRE / _PAS_GRILLE) + 1
    divergence_max = 0.0
    for i in range(nombre):
        x = i * _PAS_GRILLE
        for j in range(nombre):
            y = j * _PAS_GRILLE
            du_dx = (champ.vitesse(x + h, y)[0] - champ.vitesse(x - h, y)[0]) / (2.0 * h)
            dv_dy = (champ.vitesse(x, y + h)[1] - champ.vitesse(x, y - h)[1]) / (2.0 * h)
            divergence_max = max(divergence_max, abs(du_dx + dv_dy))
    return divergence_max


def resoudre_scenario(scenario: ScenarioReconstruction) -> ResultatReconstruction:
    """Résout un scénario de reconstruction : mesures, écart, divergences.

    Args:
        scenario: configuration immuable (champs, mesures, parcelle, domaine).

    Returns:
        Les vents du choix 1 aux deux mesures, l'écart maximal entre les
        deux choix aux mesures, les divergences numériques maximales de
        chaque champ et la longueur de la trajectoire relevée au sol.
    """
    vent_mesure_1 = scenario.champ_choix_1.vitesse(*scenario.mesures[0])
    vent_mesure_2 = scenario.champ_choix_1.vitesse(*scenario.mesures[1])
    ecart = 0.0
    for point in scenario.mesures:
        u_1, v_1 = scenario.champ_choix_1.vitesse(*point)
        u_2, v_2 = scenario.champ_choix_2.vitesse(*point)
        ecart = max(ecart, math.hypot(u_1 - u_2, v_1 - v_2))
    longueur = 0.0
    for avant, apres in zip(scenario.trajectoire, scenario.trajectoire[1:], strict=False):
        longueur += math.hypot(apres[0] - avant[0], apres[1] - avant[1])
    return ResultatReconstruction(
        vent_mesure_1=vent_mesure_1,
        vent_mesure_2=vent_mesure_2,
        ecart_entre_choix=ecart,
        divergence_max_choix_1=_divergence_numerique_max(scenario.champ_choix_1),
        divergence_max_choix_2=_divergence_numerique_max(scenario.champ_choix_2),
        longueur_trajectoire=longueur,
    )


def _parametres_champ(champ: ChampPlan) -> dict[str, object]:
    """Exporte les paramètres d'un champ du scénario pour le manifeste.

    Seule la classe cellulaire expose amplitude et longueur ; toute autre
    implémentation du protocole est exportée par son type, sans inventer
    de paramètres.

    Args:
        champ: champ plan du scénario (protocole ``ChampPlan``).

    Returns:
        Un dictionnaire sérialisable pour la frontière JSON du manifeste.
    """
    if isinstance(champ, ChampFonctionCourant):
        return {"amplitude": champ.amplitude, "longueur": champ.longueur}
    return {"type": type(champ).__name__}


@dataclass(frozen=True)
class ManifesteReconstruction:
    """Manifeste immuable reliant l'expérience à sa spécification et ses limites.

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
    scenario: ScenarioReconstruction
    resultat: ResultatReconstruction
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire (frontière JSON uniquement)."""
        scenario = self.scenario
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
                "amplitude_choix_1": scenario.champ_choix_1.amplitude,
                "longueur_choix_1": scenario.champ_choix_1.longueur,
                "champs_choix_2": [
                    _parametres_champ(champ) for champ in scenario.champ_choix_2.champs
                ],
                "mesures": [list(mesure) for mesure in scenario.mesures],
                "parcelle": [
                    list(scenario.parcelle.coin),
                    scenario.parcelle.largeur,
                    scenario.parcelle.hauteur,
                ],
                "domaine": [
                    list(scenario.domaine.coin),
                    scenario.domaine.largeur,
                    scenario.domaine.hauteur,
                ],
                "trajectoire": [list(point) for point in scenario.trajectoire],
            },
            "resultats": {
                "vent_mesure_1": list(self.resultat.vent_mesure_1),
                "vent_mesure_2": list(self.resultat.vent_mesure_2),
                "ecart_entre_choix": self.resultat.ecart_entre_choix,
                "divergence_max_choix_1": self.resultat.divergence_max_choix_1,
                "divergence_max_choix_2": self.resultat.divergence_max_choix_2,
                "longueur_trajectoire": self.resultat.longueur_trajectoire,
            },
        }


def construire_manifeste(
    scenario: ScenarioReconstruction,
    resultat: ResultatReconstruction,
) -> ManifesteReconstruction:
    """Assemble le manifeste de l'expérience de reconstruction (métadonnées fixes).

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
    return ManifesteReconstruction(
        identifiant="jdriftx-reconstruction-vent-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, p. 253, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description=(
            "Reconstruction du vent à partir de deux mesures : deux champs distincts "
            "coïncident aux points de mesure."
        ),
        hypothese=(
            "Champs plans stationnaires incompressibles à fonction de courant.",
            "Exactement deux mesures ponctuelles de vent.",
            "Trajectoire relevée au sol fournie avec le scénario.",
        ),
        limites=(
            "Cas synthétique : aucune donnée ni paramètre historique.",
            "Deux champs très différents coïncident aux mesures : l'interpolation "
            "n'est pas unique.",
            "Ne constitue pas une reproduction quantitative du chapitre de 2008.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.reconstruction_vent import "
            "SCENARIO_DEFAUT, resoudre_scenario; print(resoudre_scenario(SCENARIO_DEFAUT))'"
        ),
    )
