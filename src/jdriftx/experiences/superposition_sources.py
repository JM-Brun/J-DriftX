"""Superposition de deux sources : les champs s'ajoutent, pas les régions.

Cette expérience porte l'étape C du plan de figures du chapitre de 2008
(figure 4, p. 254) : deux sources de scalaire passif dans un champ de vent
analytique incompressible évalué en trois points de mesure, avec la
comparaison des contributions individuelles et de leur somme. Le point
scientifique est l'additivité : la concentration totale est exactement la
somme des contributions tant que l'équation gouvernante est linéaire, mais
les régions « affectées » (concentration au-dessus d'un seuil) ne s'ajoutent
pas : dans ce cas jouet, la région totale contient un « pont » où chaque
contribution seule est sous le seuil, et sa surface dépasse la somme des
surfaces individuelles.

Le livrable est conceptuel (niveau R1) : cas synthétique sans donnée
historique, pas une reproduction quantitative du chapitre de 2008. Le champ
de vent n'est pas assimilé à partir des trois mesures : il est analytique et
évalué aux points de mesure (l'expérience de reconstruction du vent établit
la non-unicité à deux mesures, et trois mesures ne la lèvent pas). Tous
les objets sont immuables et validés à la construction ; les ``dict``
restent confinés à la frontière d'export JSON, conformément à la charte
qualité du dépôt.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np
from importlib import metadata
from typing import Literal

from jdriftx.champ_analytique import ChampFonctionCourant, ChampPlan
from jdriftx.experiences.reconstruction_vent import Rectangle

NiveauFidelite = Literal["R0", "R1", "R2"]

_COTE_FENETRE = 2000.0
_PAS_GRILLE = 100.0
_PAS_DERIVEE = 1.0


def _valide_point(nom: str, point: tuple[float, float]) -> None:
    """Lève ValueError si le point n'est pas un couple de coordonnées finies."""
    coordonnees = tuple(point)
    if len(coordonnees) != 2 or any(isinstance(valeur, (bool, np.bool_)) for valeur in coordonnees):
        msg = f"Le point {nom} doit être un couple (x, y) numérique (booléens exclus)."
        raise ValueError(msg)
    if not all(math.isfinite(c) for c in coordonnees):
        msg = f"Le point {nom} doit être un couple (x, y) de coordonnées finies."
        raise ValueError(msg)


def _coins(rectangle: Rectangle) -> tuple[tuple[float, float], ...]:
    """Renvoie les quatre coins d'un rectangle aligné sur les axes."""
    x0, y0 = rectangle.coin
    x1 = x0 + rectangle.largeur
    y1 = y0 + rectangle.hauteur
    return ((x0, y0), (x1, y0), (x0, y1), (x1, y1))


@dataclass(frozen=True)
class SourceGaussienne:
    """Source synthétique à profil gaussien isotrope, concentration relative.

    Attributes:
        position: centre (x, y) de la source, en m.
        amplitude: concentration relative au centre, finie et strictement positive.
        longueur: échelle gaussienne (m), finie et strictement positive.
    """

    position: tuple[float, float]
    amplitude: float
    longueur: float

    def __post_init__(self) -> None:
        """Valide la position, l'amplitude et l'échelle gaussienne."""
        _valide_point("position", self.position)
        if any(isinstance(valeur, (bool, np.bool_)) for valeur in (self.amplitude, self.longueur)):
            msg = "L'amplitude et la longueur doivent être numériques (booléens exclus)."
            raise ValueError(msg)
        if not math.isfinite(self.amplitude) or self.amplitude <= 0.0:
            msg = "L'amplitude doit être finie et strictement positive."
            raise ValueError(msg)
        if not math.isfinite(self.longueur) or self.longueur <= 0.0:
            msg = "La longueur doit être finie et strictement positive."
            raise ValueError(msg)

    def concentration(self, x: float, y: float) -> float:
        """Évalue la contribution relative de la source au point (x, y)."""
        _valide_point("evaluation", (x, y))
        dx = x - self.position[0]
        dy = y - self.position[1]
        return self.amplitude * math.exp(-(dx * dx + dy * dy) / (self.longueur * self.longueur))

    def rayon_affecte(self, seuil: float) -> float:
        """Rayon analytique du disque affecté ; exige 0 < seuil <= amplitude."""
        if isinstance(seuil, (bool, np.bool_)):
            msg = "Le seuil doit être numérique (booléens exclus)."
            raise ValueError(msg)
        if seuil <= 0.0 or seuil > self.amplitude:
            msg = "Le seuil doit être strictement positif et au plus égal à l'amplitude."
            raise ValueError(msg)
        return self.longueur * math.sqrt(math.log(self.amplitude / seuil))


def _valide_sources(
    source_1: SourceGaussienne,
    source_2: SourceGaussienne,
    fenetre: Rectangle,
) -> None:
    """Valide deux sources distinctes situées dans la fenêtre."""
    if source_1.position == source_2.position:
        msg = "Les deux sources doivent être en des positions distinctes."
        raise ValueError(msg)
    for source in (source_1, source_2):
        if not fenetre.contient(source.position):
            msg = "Les sources doivent être dans la fenêtre."
            raise ValueError(msg)


def _valide_mesures(
    mesures: tuple[tuple[float, float], ...],
    fenetre: Rectangle,
) -> None:
    """Valide exactement trois mesures distinctes dans la fenêtre."""
    if len(mesures) != 3:
        msg = "Le scénario exige exactement trois mesures."
        raise ValueError(msg)
    for mesure in mesures:
        _valide_point("mesure", mesure)
        if not fenetre.contient(mesure):
            msg = "Les points de mesure doivent être dans la fenêtre."
            raise ValueError(msg)
    for avant, apres in itertools.pairwise(mesures):
        if avant == apres:
            msg = "Les trois points de mesure doivent être distincts."
            raise ValueError(msg)


def _valide_disques(
    source_1: SourceGaussienne,
    source_2: SourceGaussienne,
    seuil: float,
    fenetre: Rectangle,
) -> None:
    """Valide que les disques affectés restent dans la fenêtre."""
    for source in (source_1, source_2):
        rayon = source.rayon_affecte(seuil)
        x0, y0 = source.position
        boite = Rectangle(coin=(x0 - rayon, y0 - rayon), largeur=2.0 * rayon, hauteur=2.0 * rayon)
        if not all(fenetre.contient(coin) for coin in _coins(boite)):
            msg = "Les disques affectés doivent rester dans la fenêtre."
            raise ValueError(msg)


@dataclass(frozen=True)
class ScenarioSuperposition:
    """Configuration immuable de la superposition de deux sources.

    Attributes:
        source_1: première source gaussienne.
        source_2: seconde source gaussienne, en position distincte.
        champ_vent: champ de vent analytique incompressible.
        mesures: exactement trois points de mesure du vent (x, y) en m, distincts.
        seuil: seuil de concentration relative définissant les régions affectées.
        fenetre: rectangle de calcul et d'affichage, contenu dans le domaine.
        domaine: rectangle du domaine d'étude.
    """

    source_1: SourceGaussienne
    source_2: SourceGaussienne
    champ_vent: ChampFonctionCourant
    mesures: tuple[tuple[float, float], ...]
    seuil: float
    fenetre: Rectangle
    domaine: Rectangle

    def __post_init__(self) -> None:
        """Valide les sources, les mesures, le seuil et la fenêtre."""
        if not all(self.domaine.contient(coin) for coin in _coins(self.fenetre)):
            msg = "La fenêtre doit être entièrement contenue dans le domaine."
            raise ValueError(msg)
        _valide_sources(self.source_1, self.source_2, self.fenetre)
        _valide_mesures(self.mesures, self.fenetre)
        if isinstance(self.seuil, (bool, np.bool_)):
            msg = "Le seuil doit être numérique (booléens exclus)."
            raise ValueError(msg)
        if not math.isfinite(self.seuil) or self.seuil <= 0.0:
            msg = "Le seuil doit être fini et strictement positif."
            raise ValueError(msg)
        if self.seuil >= min(self.source_1.amplitude, self.source_2.amplitude):
            msg = (
                "Le seuil doit rester sous la plus petite amplitude "
                "pour que chaque région affectée soit non vide."
            )
            raise ValueError(msg)
        _valide_disques(self.source_1, self.source_2, self.seuil, self.fenetre)


@dataclass(frozen=True)
class ResultatSuperposition:
    """Résultats numériques immuables de la superposition de deux sources.

    Attributes:
        vent_mesure_1: vent évalué à la première mesure (m s^-1).
        vent_mesure_2: vent évalué à la seconde mesure (m s^-1).
        vent_mesure_3: vent évalué à la troisième mesure (m s^-1).
        divergence_max: divergence numérique maximale du champ de vent (s^-1).
        rayon_affecte_1: rayon analytique du disque affecté de la source 1 (m).
        rayon_affecte_2: rayon analytique du disque affecté de la source 2 (m).
        surface_affectee_1: surface analytique du disque affecté de la source 1 (m²).
        surface_affectee_2: surface analytique du disque affecté de la source 2 (m²).
        surface_affectee_totale: surface de la région {c1 + c2 >= seuil} sur la grille (m²).
        concentration_max_totale: maximum de la concentration totale sur la grille.
        contribution_croisee_1: contribution de la source 2 au centre de la source 1.
        contribution_croisee_2: contribution de la source 1 au centre de la source 2.
    """

    vent_mesure_1: tuple[float, float]
    vent_mesure_2: tuple[float, float]
    vent_mesure_3: tuple[float, float]
    divergence_max: float
    rayon_affecte_1: float
    rayon_affecte_2: float
    surface_affectee_1: float
    surface_affectee_2: float
    surface_affectee_totale: float
    concentration_max_totale: float
    contribution_croisee_1: float
    contribution_croisee_2: float


CHAMP_VENT_DEFAUT = ChampFonctionCourant(amplitude=800.0, longueur=1000.0)
SOURCE_1_DEFAUT = SourceGaussienne(position=(700.0, 1200.0), amplitude=1.0, longueur=300.0)
SOURCE_2_DEFAUT = SourceGaussienne(position=(1300.0, 1200.0), amplitude=1.0, longueur=300.0)

SCENARIO_DEFAUT = ScenarioSuperposition(
    source_1=SOURCE_1_DEFAUT,
    source_2=SOURCE_2_DEFAUT,
    champ_vent=CHAMP_VENT_DEFAUT,
    mesures=((400.0, 400.0), (1000.0, 400.0), (1600.0, 400.0)),
    seuil=0.5,
    fenetre=Rectangle(coin=(0.0, 0.0), largeur=2000.0, hauteur=2000.0),
    domaine=Rectangle(coin=(0.0, 0.0), largeur=20000.0, hauteur=20000.0),
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


def resoudre_scenario(scenario: ScenarioSuperposition) -> ResultatSuperposition:
    """Résout un scénario de superposition : mesures, rayons, surfaces, somme.

    Args:
        scenario: configuration immuable (sources, champ, mesures, seuil).

    Returns:
        Les vents évalués aux trois mesures, la divergence numérique maximale,
        les rayons et surfaces analytiques des disques affectés, la surface de
        la région totale estimée sur la grille, le maximum de la concentration
        totale et les contributions croisées aux centres des sources.
    """
    champ = scenario.champ_vent
    mesures_vent = tuple(champ.vitesse(*mesure) for mesure in scenario.mesures)
    seuil = scenario.seuil
    rayon_1 = scenario.source_1.rayon_affecte(seuil)
    rayon_2 = scenario.source_2.rayon_affecte(seuil)
    cote = scenario.fenetre.largeur
    nombre = int(cote / _PAS_GRILLE) + 1
    cellules = 0
    concentration_max = 0.0
    for i in range(nombre):
        x = i * _PAS_GRILLE
        for j in range(nombre):
            y = j * _PAS_GRILLE
            totale = scenario.source_1.concentration(x, y) + scenario.source_2.concentration(x, y)
            concentration_max = max(concentration_max, totale)
            if totale >= seuil:
                cellules += 1
    x1, y1 = scenario.source_1.position
    x2, y2 = scenario.source_2.position
    return ResultatSuperposition(
        vent_mesure_1=mesures_vent[0],
        vent_mesure_2=mesures_vent[1],
        vent_mesure_3=mesures_vent[2],
        divergence_max=_divergence_numerique_max(champ),
        rayon_affecte_1=rayon_1,
        rayon_affecte_2=rayon_2,
        surface_affectee_1=math.pi * rayon_1 * rayon_1,
        surface_affectee_2=math.pi * rayon_2 * rayon_2,
        surface_affectee_totale=cellules * _PAS_GRILLE * _PAS_GRILLE,
        concentration_max_totale=concentration_max,
        contribution_croisee_1=scenario.source_2.concentration(x1, y1),
        contribution_croisee_2=scenario.source_1.concentration(x2, y2),
    )


@dataclass(frozen=True)
class ManifesteSuperposition:
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
    scenario: ScenarioSuperposition
    resultat: ResultatSuperposition
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
                "source_1": {
                    "position": list(scenario.source_1.position),
                    "amplitude": scenario.source_1.amplitude,
                    "longueur": scenario.source_1.longueur,
                },
                "source_2": {
                    "position": list(scenario.source_2.position),
                    "amplitude": scenario.source_2.amplitude,
                    "longueur": scenario.source_2.longueur,
                },
                "champ_vent": {
                    "amplitude": scenario.champ_vent.amplitude,
                    "longueur": scenario.champ_vent.longueur,
                },
                "mesures": [list(mesure) for mesure in scenario.mesures],
                "seuil": scenario.seuil,
                "fenetre": [
                    list(scenario.fenetre.coin),
                    scenario.fenetre.largeur,
                    scenario.fenetre.hauteur,
                ],
                "domaine": [
                    list(scenario.domaine.coin),
                    scenario.domaine.largeur,
                    scenario.domaine.hauteur,
                ],
            },
            "resultats": {
                "vent_mesure_1": list(self.resultat.vent_mesure_1),
                "vent_mesure_2": list(self.resultat.vent_mesure_2),
                "vent_mesure_3": list(self.resultat.vent_mesure_3),
                "divergence_max": self.resultat.divergence_max,
                "rayon_affecte_1": self.resultat.rayon_affecte_1,
                "rayon_affecte_2": self.resultat.rayon_affecte_2,
                "surface_affectee_1": self.resultat.surface_affectee_1,
                "surface_affectee_2": self.resultat.surface_affectee_2,
                "surface_affectee_totale": self.resultat.surface_affectee_totale,
                "concentration_max_totale": self.resultat.concentration_max_totale,
                "contribution_croisee_1": self.resultat.contribution_croisee_1,
                "contribution_croisee_2": self.resultat.contribution_croisee_2,
            },
        }


def construire_manifeste(
    scenario: ScenarioSuperposition,
    resultat: ResultatSuperposition,
) -> ManifesteSuperposition:
    """Assemble le manifeste de l'expérience de superposition (métadonnées fixes).

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
    return ManifesteSuperposition(
        identifiant="jdriftx-superposition-sources-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, p. 254, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description=(
            "Superposition de deux sources : la concentration totale est la somme exacte "
            "des contributions, les régions affectées ne le sont pas."
        ),
        hypothese=(
            "Équation de transport linéaire : la concentration totale est la somme "
            "exacte des contributions.",
            "Sources gaussiennes isotropes synthétiques, à normalisation relative sans unité.",
            "Champ de vent analytique incompressible, évalué (non assimilé) aux mesures.",
        ),
        limites=(
            "Cas synthétique : aucune donnée ni paramètre historique.",
            "Les régions affectées ne sont pas additives : seule la concentration s'ajoute.",
            "Trois mesures ne suffisent pas à reconstruire le champ de vent (non-unicité).",
            "Ne constitue pas une reproduction quantitative du chapitre de 2008.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.superposition_sources import "
            "SCENARIO_DEFAUT, resoudre_scenario; print(resoudre_scenario(SCENARIO_DEFAUT))'"
        ),
    )
