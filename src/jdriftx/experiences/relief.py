"""Relief et dispersion : la correction déplace le point de calcul.

Cette expérience porte l'étape D du plan de figures du chapitre de 2008
(figure 5, pp. 254-255) : un modèle numérique de terrain synthétique
sur un domaine de 2 km x 2 km, une source de scalaire passif dans un
vent uniforme du nord, et la comparaison de deux conventions
d'évaluation de la concentration au sol. Sans correction, le modèle
ignore le relief : le sol du modèle est le plan z = 0 et le point de
calcul est posé à hauteur d'évaluation au-dessus. Avec correction, le
point de calcul est posé à la même hauteur au-dessus du sol réel. Le
panache gaussien, le vent, la source et les écarts-types de Briggs
sont strictement identiques dans les deux calculs : la seule
différence est l'altitude du point de calcul.

Le point scientifique est une ablation : hors des collines, les deux
calculs coïncident ; la correction n'ajoute des cellules affectées
qu'autour des crêtes, et l'effet décroît à mesure que le panache
s'élargit (écart-type vertical croissant avec la distance sous le
vent). La correction est volontairement minimale : ni déviation du
panache par les collines, ni allongement du trajet, ni perturbation du
vent par le relief ; le terme de réflexion au sol reste référé au sol
du modèle (z = 0) dans les deux calculs.

Le livrable est conceptuel (niveau R1) : MNT synthétique sans donnée
historique, pas une reproduction quantitative du chapitre de 2008.
Tous les objets sont immuables et validés à la construction ; les
``dict`` restent confinés à la frontière d'export JSON, conformément
à la charte qualité du dépôt.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

import numpy as np

from jdriftx.experiences.reconstruction_vent import Rectangle
from jdriftx.similitude import concentration_panache
from jdriftx.stabilite import ClasseStabilite
from jdriftx.terrain import terrain_surface

NiveauFidelite = Literal["R0", "R1", "R2"]

_PAS_GRILLE = 50.0
_TOLERANCE_SOL_PLAT = 0.5


def _valide_point(nom: str, point: tuple[float, float]) -> None:
    """Lève ValueError si le point n'est pas un couple de coordonnées finies."""
    if len(tuple(point)) != 2 or not all(math.isfinite(c) for c in tuple(point)):
        msg = f"Le point {nom} doit être un couple (x, y) de coordonnées finies."
        raise ValueError(msg)


def _coins(rectangle: Rectangle) -> tuple[tuple[float, float], ...]:
    """Renvoie les quatre coins d'un rectangle aligné sur les axes."""
    x0, y0 = rectangle.coin
    x1 = x0 + rectangle.largeur
    y1 = y0 + rectangle.hauteur
    return ((x0, y0), (x1, y0), (x0, y1), (x1, y1))


@dataclass(frozen=True)
class CollineGaussienne:
    """Colline synthétique à profil gaussien, évaluée par `jdriftx.terrain`.

    Attributes:
        centre: centre (x, y) de la colline, en m.
        hauteur: amplitude de la colline (m), finie et strictement positive.
        echelle: échelle gaussienne (m), finie et strictement positive.
    """

    centre: tuple[float, float]
    hauteur: float
    echelle: float

    def __post_init__(self) -> None:
        """Valide le centre, la hauteur et l'échelle gaussienne."""
        _valide_point("centre", self.centre)
        if not math.isfinite(self.hauteur) or self.hauteur <= 0.0:
            msg = "La hauteur doit être finie et strictement positive."
            raise ValueError(msg)
        if not math.isfinite(self.echelle) or self.echelle <= 0.0:
            msg = "L'échelle doit être finie et strictement positive."
            raise ValueError(msg)

    def altitude(self, x: float, y: float) -> float:
        """Évalue l'altitude de la colline au point (x, y), en m."""
        grille_x = np.asarray([[x]], dtype=float)
        grille_y = np.asarray([[y]], dtype=float)
        surface = terrain_surface(
            grille_x,
            grille_y,
            "hill",
            height=self.hauteur,
            width=self.echelle,
            center_x=self.centre[0],
            center_y=self.centre[1],
        )
        return float(surface[0, 0])


def _valide_collines(collines: tuple[CollineGaussienne, ...], fenetre: Rectangle) -> None:
    """Valide exactement deux collines, à centres distincts, dans la fenêtre."""
    if len(collines) != 2:
        msg = "Le scénario exige exactement deux collines."
        raise ValueError(msg)
    for colline in collines:
        if not fenetre.contient(colline.centre):
            msg = "Les collines doivent être dans la fenêtre."
            raise ValueError(msg)
    if collines[0].centre == collines[1].centre:
        msg = "Les deux collines doivent être en des centres distincts."
        raise ValueError(msg)


def _valide_vent(vent: tuple[float, float]) -> None:
    """Valide un vent uniforme de composantes finies et de norme positive."""
    if len(tuple(vent)) != 2 or not all(math.isfinite(c) for c in tuple(vent)):
        msg = "Le vent doit être un couple (u, v) de composantes finies."
        raise ValueError(msg)
    if math.hypot(vent[0], vent[1]) <= 0.0:
        msg = "Le vent doit être de norme strictement positive."
        raise ValueError(msg)


def _valide_parametres(scenario: ScenarioRelief) -> None:
    """Valide le débit, la classe de stabilité, les hauteurs et le seuil."""
    if not math.isfinite(scenario.debit) or scenario.debit <= 0.0:
        msg = "Le débit doit être strictement positif."
        raise ValueError(msg)
    try:
        ClasseStabilite(scenario.classe)
    except ValueError as err:
        msg = f"Classe de stabilité inconnue : {scenario.classe!r} (attendu : A à F)."
        raise ValueError(msg) from err
    if not math.isfinite(scenario.hauteur_source) or scenario.hauteur_source <= 0.0:
        msg = "La hauteur de source doit être strictement positive."
        raise ValueError(msg)
    if not math.isfinite(scenario.seuil) or scenario.seuil <= 0.0:
        msg = "Le seuil doit être strictement positif."
        raise ValueError(msg)
    if not math.isfinite(scenario.hauteur_evaluation) or scenario.hauteur_evaluation <= 0.0:
        msg = "La hauteur d'évaluation doit être strictement positive."
        raise ValueError(msg)


def _valide_source(scenario: ScenarioRelief) -> None:
    """Valide une source dans la fenêtre, sur un sol quasi plat, au vent des collines."""
    if not scenario.fenetre.contient(scenario.source):
        msg = "La source doit être dans la fenêtre."
        raise ValueError(msg)
    relief_source = scenario.altitude_sol(*scenario.source)
    if relief_source > _TOLERANCE_SOL_PLAT:
        msg = "La source doit être posée sur un sol quasi plat (relief < 0,5 m)."
        raise ValueError(msg)
    u, v = scenario.vent
    for colline in scenario.collines:
        dx = colline.centre[0] - scenario.source[0]
        dy = colline.centre[1] - scenario.source[1]
        if dx * u + dy * v <= 0.0:
            msg = "Les collines doivent être sous le vent de la source."
            raise ValueError(msg)


@dataclass(frozen=True)
class ScenarioRelief:
    """Configuration immuable de l'expérience de relief.

    Attributes:
        collines: exactement deux collines gaussiennes, à centres distincts.
        vent: vent uniforme (u, v) en m s^-1, de norme strictement positive.
        source: position (x, y) de la source, sur un sol quasi plat.
        debit: émission massique (kg s^-1), strictement positive.
        classe: classe de stabilité de Pasquill (A à F).
        hauteur_source: hauteur effective de la source au-dessus du sol local (m).
        seuil: seuil de concentration définissant les régions affectées (kg m^-3).
        hauteur_evaluation: hauteur du point de calcul au-dessus du sol (m).
        fenetre: rectangle de calcul et d'affichage, contenu dans le domaine.
        domaine: rectangle du domaine d'étude.
    """

    collines: tuple[CollineGaussienne, ...]
    vent: tuple[float, float]
    source: tuple[float, float]
    debit: float
    classe: str
    hauteur_source: float
    seuil: float
    hauteur_evaluation: float
    fenetre: Rectangle
    domaine: Rectangle

    def __post_init__(self) -> None:
        """Valide la fenêtre, les collines, le vent, les paramètres et la source."""
        if not all(self.domaine.contient(coin) for coin in _coins(self.fenetre)):
            msg = "La fenêtre doit être entièrement contenue dans le domaine."
            raise ValueError(msg)
        _valide_collines(self.collines, self.fenetre)
        _valide_vent(self.vent)
        _valide_parametres(self)
        _valide_source(self)

    def altitude_sol(self, x: float, y: float) -> float:
        """Évalue l'altitude du MNT synthétique au point (x, y), en m."""
        return sum(colline.altitude(x, y) for colline in self.collines)

    @property
    def altitude_axe(self) -> float:
        """Altitude de l'axe du panache (m), au-dessus du sol local à la source."""
        return self.hauteur_source + self.altitude_sol(*self.source)


@dataclass(frozen=True)
class ResultatRelief:
    """Résultats numériques immuables de l'expérience de relief.

    Attributes:
        altitude_max_mnt: altitude maximale du MNT sur la grille 50 m (m).
        altitude_axe: altitude de l'axe du panache (m).
        cellules_sans: cellules de la région {c >= seuil} sans correction.
        cellules_avec: cellules de la région {c >= seuil} avec correction.
        surface_region_sans: surface de la région sans correction (m²).
        surface_region_avec: surface de la région avec correction (m²).
        concentration_max_sans: concentration maximale sans correction (kg m^-3).
        concentration_max_avec: concentration maximale avec correction (kg m^-3).
        ratio_sommet_1: rapport de concentration au centre de la colline 1.
        ratio_sommet_2: rapport de concentration au centre de la colline 2.
    """

    altitude_max_mnt: float
    altitude_axe: float
    cellules_sans: int
    cellules_avec: int
    surface_region_sans: float
    surface_region_avec: float
    concentration_max_sans: float
    concentration_max_avec: float
    ratio_sommet_1: float
    ratio_sommet_2: float


COLLINE_1_DEFAUT = CollineGaussienne(centre=(1000.0, 1600.0), hauteur=40.0, echelle=90.0)
COLLINE_2_DEFAUT = CollineGaussienne(centre=(1000.0, 1400.0), hauteur=35.0, echelle=60.0)

SCENARIO_DEFAUT = ScenarioRelief(
    collines=(COLLINE_1_DEFAUT, COLLINE_2_DEFAUT),
    vent=(0.0, -3.0),
    source=(1000.0, 1900.0),
    debit=2.0,
    classe="C",
    hauteur_source=50.0,
    seuil=2e-5,
    hauteur_evaluation=3.0,
    fenetre=Rectangle(coin=(0.0, 0.0), largeur=2000.0, hauteur=2000.0),
    domaine=Rectangle(coin=(0.0, 0.0), largeur=20000.0, hauteur=20000.0),
)


def concentrations_au_point(scenario: ScenarioRelief, x: float, y: float) -> tuple[float, float]:
    """Évalue les concentrations (kg m^-3) sans et avec correction au point (x, y).

    Sans correction, le sol du modèle est le plan z = 0 : le point de calcul
    est posé à la hauteur d'évaluation au-dessus de ce plan. Avec correction,
    le point est posé à la même hauteur au-dessus du sol réel. Le panache,
    le vent et les écarts-types de Briggs sont identiques : seule l'altitude
    du point de calcul change. En amont de la source, la concentration est
    nulle dans les deux conventions.

    Args:
        scenario: configuration immuable de l'expérience.
        x: abscisse du point de calcul (m).
        y: ordonnée du point de calcul (m).

    Returns:
        Le couple (concentration sans correction, concentration avec correction).
    """
    u, v = scenario.vent
    norme = math.hypot(u, v)
    dx = x - scenario.source[0]
    dy = y - scenario.source[1]
    sous_vent = (dx * u + dy * v) / norme
    if sous_vent <= 0.0:
        return (0.0, 0.0)
    lateral = (dx * -v + dy * u) / norme
    hauteur_axe = scenario.altitude_axe
    hauteur_modele = scenario.hauteur_evaluation
    c_sans = concentration_panache(
        sous_vent,
        lateral,
        hauteur_modele,
        scenario.debit,
        norme,
        scenario.classe,
        hauteur=hauteur_axe,
    )
    z_reel = scenario.altitude_sol(x, y) + scenario.hauteur_evaluation
    c_avec = concentration_panache(
        sous_vent,
        lateral,
        z_reel,
        scenario.debit,
        norme,
        scenario.classe,
        hauteur=hauteur_axe,
    )
    return (float(c_sans), float(c_avec))


def resoudre_scenario(scenario: ScenarioRelief) -> ResultatRelief:
    """Résout le scénario de relief : régions affectées avec et sans correction.

    Args:
        scenario: configuration immuable (collines, vent, source, seuil).

    Returns:
        L'altitude maximale du MNT sur la grille 50 m, l'altitude de l'axe
        du panache, les surfaces et nombres de cellules des régions
        {c >= seuil} sans et avec correction, les concentrations maximales
        correspondantes et les rapports de concentration aux centres des
        deux collines.
    """
    pas = _PAS_GRILLE
    x_origine = scenario.fenetre.coin[0]
    y_origine = scenario.fenetre.coin[1]
    nombre = int(scenario.fenetre.largeur / pas) + 1
    seuil = scenario.seuil
    altitude_max = 0.0
    cellules_sans = 0
    cellules_avec = 0
    c_max_sans = 0.0
    c_max_avec = 0.0
    for i in range(nombre):
        x = x_origine + i * pas
        for j in range(nombre):
            y = y_origine + j * pas
            altitude = scenario.altitude_sol(x, y)
            altitude_max = max(altitude_max, altitude)
            c_sans, c_avec = concentrations_au_point(scenario, x, y)
            c_max_sans = max(c_max_sans, c_sans)
            c_max_avec = max(c_max_avec, c_avec)
            if c_sans >= seuil:
                cellules_sans += 1
            if c_avec >= seuil:
                cellules_avec += 1
    colline_1 = scenario.collines[0]
    colline_2 = scenario.collines[1]
    c1_sans, c1_avec = concentrations_au_point(scenario, *colline_1.centre)
    c2_sans, c2_avec = concentrations_au_point(scenario, *colline_2.centre)
    surface_cellule = pas * pas
    return ResultatRelief(
        altitude_max_mnt=altitude_max,
        altitude_axe=scenario.altitude_axe,
        cellules_sans=cellules_sans,
        cellules_avec=cellules_avec,
        surface_region_sans=cellules_sans * surface_cellule,
        surface_region_avec=cellules_avec * surface_cellule,
        concentration_max_sans=c_max_sans,
        concentration_max_avec=c_max_avec,
        ratio_sommet_1=c1_avec / c1_sans,
        ratio_sommet_2=c2_avec / c2_sans,
    )


@dataclass(frozen=True)
class ManifesteRelief:
    """Manifeste immuable reliant l'expérience à sa spécification et ses limites.

    Attributes:
        identifiant: identifiant stable de l'expérience.
        niveau_fidelite: niveau de fidélité (R0 schéma, R1 reconstruction, R2 reproduction).
        source: référence documentée de la définition (DOI, pages).
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
    scenario: ScenarioRelief
    resultat: ResultatRelief
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire (frontière JSON uniquement)."""
        scenario = self.scenario
        collines = [
            {"centre": list(c.centre), "hauteur": c.hauteur, "echelle": c.echelle}
            for c in scenario.collines
        ]
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
                "collines": collines,
                "vent": list(scenario.vent),
                "source": list(scenario.source),
                "debit": scenario.debit,
                "classe": scenario.classe,
                "hauteur_source": scenario.hauteur_source,
                "seuil": scenario.seuil,
                "hauteur_evaluation": scenario.hauteur_evaluation,
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
                "altitude_max_mnt": self.resultat.altitude_max_mnt,
                "altitude_axe": self.resultat.altitude_axe,
                "cellules_sans": self.resultat.cellules_sans,
                "cellules_avec": self.resultat.cellules_avec,
                "surface_region_sans": self.resultat.surface_region_sans,
                "surface_region_avec": self.resultat.surface_region_avec,
                "concentration_max_sans": self.resultat.concentration_max_sans,
                "concentration_max_avec": self.resultat.concentration_max_avec,
                "ratio_sommet_1": self.resultat.ratio_sommet_1,
                "ratio_sommet_2": self.resultat.ratio_sommet_2,
            },
        }


def construire_manifeste(
    scenario: ScenarioRelief,
    resultat: ResultatRelief,
) -> ManifesteRelief:
    """Assemble le manifeste de l'expérience de relief (métadonnées fixes).

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
    description_manifeste = (
        "Relief synthétique : la correction déplace le point de calcul, pas le panache."
    )
    return ManifesteRelief(
        identifiant="jdriftx-relief-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, pp. 254-255, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description=description_manifeste,
        hypothese=(
            "Vent uniforme, identique dans les deux calculs.",
            "Panache gaussien de similitude (Briggs, classe C) ; réflexion au "
            "sol du modèle référée à z = 0.",
            "MNT synthétique : deux collines gaussiennes, aucune topographie mesurée.",
        ),
        limites=(
            "Correction minimale : ni déviation du panache, ni allongement du "
            "trajet, ni vent perturbé par le relief.",
            "Hors des collines, les deux calculs coïncident ; l'effet décroît "
            "quand l'écart-type vertical croît.",
            "Cas synthétique : aucune donnée ni paramètre historique.",
            "Ne constitue pas une reproduction quantitative du chapitre de 2008.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.relief import "
            "SCENARIO_DEFAUT, resoudre_scenario; print(resoudre_scenario(SCENARIO_DEFAUT))'"
        ),
    )
