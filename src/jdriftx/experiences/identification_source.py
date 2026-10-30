"""Identification de source : carte de sensibilité du coût, pas une probabilité.

Cette expérience porte la dernière étape du plan de figures du chapitre de
2008 (figure 6, p. 255) : une pollution est détectée dans le coin inférieur
gauche d'un domaine carré, sous un vent uniforme dirigé vers ce coin. Le
modèle direct est le panache de similitude de l'expérience de la figure 3
(transport advectif dominant, diffusivité transversale constante) : la
concentration est nulle en amont de la source candidate et gaussienne en
traverse. La fonctionnelle J(p) somme les écarts quadratiques entre les
concentrations prédites aux capteurs et les concentrations observées ; le
débit étant le seul paramètre linéaire, son optimal Q* s'écrit en forme
fermée par moindres carrés pour chaque position candidate. La carte de
J minimal sur une grille de positions candidates met en évidence la
non-identifiabilité position-débit : une vallée du coût s'étire le long de
l'axe du vent, une seule cellule de large.

Cette carte est une carte de sensibilité du coût d'ajustement : elle n'est
pas une probabilité de source (aucun prior, aucun postériori). Le livrable
est conceptuel (niveau R1) : cas synthétique sans donnée historique, pas
une reproduction quantitative du chapitre de 2008. Tous les objets sont
immuables et validés à la construction ; les ``dict`` restent confinés à
la frontière d'export JSON, conformément à la charte qualité du dépôt.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

import numpy as np

from jdriftx.experiences.reconstruction_vent import Rectangle

NiveauFidelite = Literal["R0", "R1", "R2"]

_SEUIL_VALLEE = 1e-2
_MARGE_MINIMUM = 1e-30


def _valide_point(nom: str, point: tuple[float, float]) -> None:
    """Lève ValueError si le point n'est pas un couple de coordonnées finies."""
    coordonnees = tuple(point)
    if len(coordonnees) != 2 or any(isinstance(valeur, (bool, np.bool_)) for valeur in coordonnees):
        msg = f"Le point {nom} doit être un couple (x, y) numérique (booléens exclus)."
        raise ValueError(msg)
    if not all(math.isfinite(c) for c in coordonnees):
        msg = f"Le point {nom} doit être un couple (x, y) de coordonnées finies."
        raise ValueError(msg)


def _vitesse(vent: tuple[float, float]) -> float:
    """Renvoie la norme du vent, strictement positive après validation."""
    return math.sqrt(vent[0] * vent[0] + vent[1] * vent[1])


def concentration(
    scenario: ScenarioIdentification,
    point: tuple[float, float],
    source: tuple[float, float],
    debit: float,
) -> float:
    """Évalue la concentration au sol du panache de similitude.

    Args:
        scenario: configuration typée (vent, diffusivité, debit vrai).
        point: point d'évaluation (x, y) en m.
        source: position candidate de la source (x, y) en m.
        debit: débit de masse de la source candidate, en kg/s.

    Returns:
        La concentration au sol en kg/m² : nulle en amont de la source
        (transport advectif dominant), gaussienne en travers avec un
        écart-type en racine carrée de la distance advective.
    """
    _valide_point("point", point)
    _valide_point("source", source)
    if isinstance(debit, (bool, np.bool_)):
        msg = "Le débit doit être numérique (booléens exclus)."
        raise ValueError(msg)
    return _concentration_panache(scenario.vent, scenario.diffusivite, point, source, debit)


def _concentration_panache(
    vent: tuple[float, float],
    diffusivite: float,
    point: tuple[float, float],
    source: tuple[float, float],
    debit: float,
) -> float:
    """Calcule le panache de similitude (amont nul, traverse gaussienne)."""
    vitesse = _vitesse(vent)
    ex = (vent[0] / vitesse, vent[1] / vitesse)
    nx = (-ex[1], ex[0])
    dx = point[0] - source[0]
    dy = point[1] - source[1]
    x_av = dx * ex[0] + dy * ex[1]
    if x_av <= 0.0:
        return 0.0
    sigma = math.sqrt(2.0 * diffusivite * x_av / vitesse)
    y_tr = dx * nx[0] + dy * nx[1]
    amplitude = debit / (vitesse * sigma * math.sqrt(2.0 * math.pi))
    return amplitude * math.exp(-(y_tr * y_tr) / (2.0 * sigma * sigma))


def _coins(rectangle: Rectangle) -> tuple[tuple[float, float], ...]:
    """Renvoie les quatre coins d'un rectangle aligné sur les axes."""
    x0, y0 = rectangle.coin
    x1 = x0 + rectangle.largeur
    y1 = y0 + rectangle.hauteur
    return ((x0, y0), (x1, y0), (x0, y1), (x1, y1))


def _valide_vent_et_scalaires(scenario: ScenarioIdentification) -> None:
    """Vérifie le vent, puis la diffusivité et le débit strictement positifs."""
    _valide_point("vent", scenario.vent)
    if _vitesse(scenario.vent) <= 0.0:
        msg = "Le vent doit être un vecteur non nul."
        raise ValueError(msg)
    if any(
        isinstance(valeur, (bool, np.bool_))
        for valeur in (scenario.diffusivite, scenario.debit_vrai)
    ):
        msg = "La diffusivité et le débit doivent être numériques (booléens exclus)."
        raise ValueError(msg)
    if not math.isfinite(scenario.diffusivite) or scenario.diffusivite <= 0.0:
        msg = "La diffusivité doit être finie et strictement positive."
        raise ValueError(msg)
    if not math.isfinite(scenario.debit_vrai) or scenario.debit_vrai <= 0.0:
        msg = "Le débit vrai doit être fini et strictement positif."
        raise ValueError(msg)


def _valide_geometrie(scenario: ScenarioIdentification) -> None:
    """Vérifie l'emboîtement domaine, fenêtre, vignoble puis source vraie."""
    _valide_point("source_vrai", scenario.source_vrai)
    if not all(scenario.domaine.contient(coin) for coin in _coins(scenario.fenetre)):
        msg = "La fenêtre doit être entièrement contenue dans le domaine."
        raise ValueError(msg)
    if not all(scenario.fenetre.contient(coin) for coin in _coins(scenario.vignoble)):
        msg = "Le vignoble doit être entièrement contenu dans la fenêtre."
        raise ValueError(msg)
    if not scenario.vignoble.contient(scenario.source_vrai):
        msg = "La source vraie doit rester dans le vignoble."
        raise ValueError(msg)
    if not scenario.fenetre.contient(scenario.source_vrai):
        msg = "La source vraie doit être dans la fenêtre."
        raise ValueError(msg)


def _valide_mesures_vent(scenario: ScenarioIdentification) -> None:
    """Vérifie les trois mesures de vent, distinctes et dans la fenêtre."""
    if len(scenario.mesures_vent) != 3:
        msg = "Le scénario exige exactement trois mesures de vent."
        raise ValueError(msg)
    for mesure in scenario.mesures_vent:
        _valide_point("mesure", mesure)
        if not scenario.fenetre.contient(mesure):
            msg = "Les mesures de vent doivent être dans la fenêtre."
            raise ValueError(msg)
    for avant, apres in itertools.pairwise(scenario.mesures_vent):
        if avant == apres:
            msg = "Les trois mesures de vent doivent être distinctes."
            raise ValueError(msg)


def _valide_capteurs(scenario: ScenarioIdentification) -> None:
    """Vérifie les cinq capteurs, distincts et dans la fenêtre."""
    if len(scenario.capteurs) != 5:
        msg = "Le scénario exige exactement cinq capteurs."
        raise ValueError(msg)
    for capteur in scenario.capteurs:
        _valide_point("capteur", capteur)
        if not scenario.fenetre.contient(capteur):
            msg = "Les capteurs doivent être dans la fenêtre."
            raise ValueError(msg)
    for avant, apres in itertools.pairwise(scenario.capteurs):
        if avant == apres:
            msg = "Les cinq capteurs doivent être distincts."
            raise ValueError(msg)


def _valide_detection(scenario: ScenarioIdentification) -> None:
    """Vérifie l'indice, le seuil et l'unicité du capteur de détection."""
    if isinstance(scenario.indice_detection, (bool, np.bool_)) or not isinstance(
        scenario.indice_detection, int
    ) or not 0 <= scenario.indice_detection < 5:
        msg = "L'indice de détection doit désigner l'un des cinq capteurs."
        raise ValueError(msg)
    if isinstance(scenario.seuil_detection, (bool, np.bool_)):
        msg = "Le seuil de détection doit être numérique (booléens exclus)."
        raise ValueError(msg)
    if not math.isfinite(scenario.seuil_detection) or scenario.seuil_detection <= 0.0:
        msg = "Le seuil de détection doit être fini et strictement positif."
        raise ValueError(msg)
    observees = tuple(
        _concentration_panache(
            scenario.vent,
            scenario.diffusivite,
            capteur,
            scenario.source_vrai,
            scenario.debit_vrai,
        )
        for capteur in scenario.capteurs
    )
    au_dessus = [v >= scenario.seuil_detection for v in observees]
    if sum(au_dessus) != 1 or not au_dessus[scenario.indice_detection]:
        msg = "Seul le capteur de détection doit dépasser le seuil de détection."
        raise ValueError(msg)


def _valide_grille_candidats(scenario: ScenarioIdentification) -> None:
    """Vérifie que le pas des candidats pave exactement la fenêtre."""
    if isinstance(scenario.pas_candidats, (bool, np.bool_)):
        msg = "Le pas des candidats doit être numérique (booléens exclus)."
        raise ValueError(msg)
    if not math.isfinite(scenario.pas_candidats) or scenario.pas_candidats <= 0.0:
        msg = "Le pas des candidats doit être fini et strictement positif."
        raise ValueError(msg)
    if not math.isclose(scenario.fenetre.largeur % scenario.pas_candidats, 0.0, abs_tol=1e-9):
        msg = "Le pas des candidats doit diviser la largeur de la fenêtre."
        raise ValueError(msg)
    if not math.isclose(scenario.fenetre.hauteur % scenario.pas_candidats, 0.0, abs_tol=1e-9):
        msg = "Le pas des candidats doit diviser la hauteur de la fenêtre."
        raise ValueError(msg)


def _valide_candidat_decale(scenario: ScenarioIdentification) -> None:
    """Vérifie le candidat témoin : sur la grille, strictement amont, distinct."""
    _valide_point("candidat_decale", scenario.candidat_decale)
    if not scenario.fenetre.contient(scenario.candidat_decale):
        msg = "Le candidat décalé doit être dans la fenêtre."
        raise ValueError(msg)
    dx = scenario.candidat_decale[0] - scenario.source_vrai[0]
    dy = scenario.candidat_decale[1] - scenario.source_vrai[1]
    if abs(dx / scenario.pas_candidats - round(dx / scenario.pas_candidats)) > 1e-9:
        msg = "Le candidat décalé doit être un nœud de la grille."
        raise ValueError(msg)
    if abs(dy / scenario.pas_candidats - round(dy / scenario.pas_candidats)) > 1e-9:
        msg = "Le candidat décalé doit être un nœud de la grille."
        raise ValueError(msg)
    vitesse = _vitesse(scenario.vent)
    ex = (scenario.vent[0] / vitesse, scenario.vent[1] / vitesse)
    if dx * ex[0] + dy * ex[1] >= 0.0:
        msg = "Le candidat décalé doit être strictement amont de la source."
        raise ValueError(msg)
    if scenario.candidat_decale == scenario.source_vrai:
        msg = "Le candidat décalé doit être distinct de la source vraie."
        raise ValueError(msg)


@dataclass(frozen=True)
class ScenarioIdentification:
    """Configuration immuable de l'identification de source.

    Attributes:
        vent: vecteur vent uniforme (u, v) en m/s, non nul.
        diffusivite: diffusivité transversale K en m²/s, strictement positive.
        debit_vrai: débit de masse de la source synthétique, en kg/s.
        source_vrai: position (x, y) de la source synthétique, en m.
        vignoble: rectangle de la parcelle émettrice, contenant la source.
        mesures_vent: exactement trois points de mesure du vent, en m.
        capteurs: exactement cinq capteurs au sol (x, y), distincts, en m.
        indice_detection: indice du capteur qui détecte la pollution.
        seuil_detection: seuil de concentration de la détection, en kg/m².
        fenetre: rectangle de calcul et d'affichage, contenu dans le domaine.
        domaine: rectangle du domaine d'étude.
        pas_candidats: pas de la grille des positions candidates, en m.
        candidat_decale: position témoin décalée au vent, sur la grille.
    """

    vent: tuple[float, float]
    diffusivite: float
    debit_vrai: float
    source_vrai: tuple[float, float]
    vignoble: Rectangle
    mesures_vent: tuple[tuple[float, float], ...]
    capteurs: tuple[tuple[float, float], ...]
    indice_detection: int
    seuil_detection: float
    fenetre: Rectangle
    domaine: Rectangle
    pas_candidats: float
    candidat_decale: tuple[float, float]

    def __post_init__(self) -> None:
        """Valide le scénario complet via les validateurs spécialisés."""
        _valide_vent_et_scalaires(self)
        _valide_geometrie(self)
        _valide_mesures_vent(self)
        _valide_capteurs(self)
        _valide_detection(self)
        _valide_grille_candidats(self)
        _valide_candidat_decale(self)


@dataclass(frozen=True)
class ResultatIdentification:
    """Résultats numériques immuables de l'identification de source.

    Attributes:
        vent_mesure_1: vent évalué à la première mesure (m s^-1).
        vent_mesure_2: vent évalué à la seconde mesure (m s^-1).
        vent_mesure_3: vent évalué à la troisième mesure (m s^-1).
        concentrations_observees: concentrations synthétiques aux cinq capteurs (kg/m²).
        concentration_detection: concentration au capteur de détection (kg/m²).
        cellules_detectees: cellules de la grille au-dessus du seuil de détection.
        concentration_maximale: maximum du champ aux centres des cellules (kg/m²).
        cout_nul: coût de l'absence de source, somme des carrés observés.
        cout_minimum: coût minimal sur la grille des candidats, exactement nul.
        position_estimee: position candidate du minimum du coût (m).
        debit_etoile: débit optimal à la position estimée (kg/s).
        couts_grille: coûts minimaux aux nœuds, ligne par ligne (j, puis i).
        nombre_cellules_vallee: cellules sous le seuil relatif de vallée.
        etendue_vallee: étendue de la vallée le long de l'axe du vent (m).
        largeur_vallee: largeur quantifiée de la vallée en traverse (m).
        cout_relatif_decale: coût du candidat décalé, rapporté au coût nul.
        debit_etoile_decale: débit optimal au candidat décalé (kg/s).
        decalage_vent: distance au vent entre source vraie et candidat décalé (m).
    """

    vent_mesure_1: tuple[float, float]
    vent_mesure_2: tuple[float, float]
    vent_mesure_3: tuple[float, float]
    concentrations_observees: tuple[float, ...]
    concentration_detection: float
    cellules_detectees: int
    concentration_maximale: float
    cout_nul: float
    cout_minimum: float
    position_estimee: tuple[float, float]
    debit_etoile: float
    couts_grille: tuple[float, ...]
    nombre_cellules_vallee: int
    etendue_vallee: float
    largeur_vallee: float
    cout_relatif_decale: float
    debit_etoile_decale: float
    decalage_vent: float


SCENARIO_DEFAUT = ScenarioIdentification(
    vent=(-1.8, -1.8),
    diffusivite=4.0,
    debit_vrai=2.0,
    source_vrai=(1500.0, 1500.0),
    vignoble=Rectangle(coin=(1400.0, 1400.0), largeur=200.0, hauteur=200.0),
    mesures_vent=((400.0, 1500.0), (1000.0, 1000.0), (1500.0, 400.0)),
    capteurs=(
        (300.0, 300.0),
        (400.0, 200.0),
        (200.0, 400.0),
        (700.0, 300.0),
        (300.0, 700.0),
    ),
    indice_detection=0,
    seuil_detection=1e-3,
    fenetre=Rectangle(coin=(0.0, 0.0), largeur=2000.0, hauteur=2000.0),
    domaine=Rectangle(coin=(0.0, 0.0), largeur=20000.0, hauteur=20000.0),
    pas_candidats=100.0,
    candidat_decale=(1800.0, 1800.0),
)


def _cout_minimal(
    scenario: ScenarioIdentification,
    source: tuple[float, float],
    observees: tuple[float, ...],
    cout_nul: float,
) -> tuple[float, float]:
    """Renvoie le coût minimal et le débit optimal pour une position candidate."""
    reponses = tuple(
        _concentration_panache(scenario.vent, scenario.diffusivite, capteur, source, 1.0)
        for capteur in scenario.capteurs
    )
    norme = sum(r * r for r in reponses)
    if norme <= 0.0:
        return cout_nul, 0.0
    produit = sum(r * c for r, c in zip(reponses, observees, strict=True))
    cout = cout_nul - (produit * produit) / norme
    cout = max(cout, 0.0)
    return cout, produit / norme


def _grille_couts(
    scenario: ScenarioIdentification, observees: tuple[float, ...], cout_nul: float
) -> tuple[list[float], float, tuple[float, float], float]:
    """Balaie la grille des candidats et retient le minimum du coût."""
    nombre_cote = int(scenario.fenetre.largeur / scenario.pas_candidats) + 1
    pas = scenario.pas_candidats
    couts: list[float] = []
    cout_minimum = cout_nul
    position_estimee: tuple[float, float] = (0.0, 0.0)
    debit_etoile = 0.0
    for j in range(nombre_cote):
        for i in range(nombre_cote):
            candidat = (i * pas, j * pas)
            cout, debit = _cout_minimal(scenario, candidat, observees, cout_nul)
            couts.append(cout)
            if cout < cout_minimum - _MARGE_MINIMUM:
                cout_minimum = cout
                position_estimee = candidat
                debit_etoile = debit
    return couts, cout_minimum, position_estimee, debit_etoile


def _vallee_cout(
    scenario: ScenarioIdentification, couts: list[float], cout_nul: float
) -> tuple[int, float, float]:
    """Mesure la vallée du coût : cellules, étendue au vent, largeur en travers."""
    nombre_cote = int(scenario.fenetre.largeur / scenario.pas_candidats) + 1
    pas = scenario.pas_candidats
    vitesse = _vitesse(scenario.vent)
    ex = (scenario.vent[0] / vitesse, scenario.vent[1] / vitesse)
    nx = (-ex[1], ex[0])
    nombre_cellules = 0
    proj_min = math.inf
    proj_max = -math.inf
    perp_min = math.inf
    perp_max = -math.inf
    for j in range(nombre_cote):
        for i in range(nombre_cote):
            cout = couts[j * nombre_cote + i]
            if cout / cout_nul > _SEUIL_VALLEE:
                continue
            dx = i * pas - scenario.source_vrai[0]
            dy = j * pas - scenario.source_vrai[1]
            proj = dx * ex[0] + dy * ex[1]
            perp = dx * nx[0] + dy * nx[1]
            nombre_cellules += 1
            proj_min = min(proj_min, proj)
            proj_max = max(proj_max, proj)
            perp_min = min(perp_min, perp)
            perp_max = max(perp_max, perp)
    return nombre_cellules, proj_max - proj_min, (perp_max - perp_min) + pas


def _detection_champ(scenario: ScenarioIdentification) -> tuple[int, float]:
    """Compte les cellules détectées et le maximum du champ aux centres."""
    pas = scenario.pas_candidats
    nombre_cellules_champ = int(scenario.fenetre.largeur / pas)
    cellules_detectees = 0
    concentration_maximale = 0.0
    for j in range(nombre_cellules_champ):
        for i in range(nombre_cellules_champ):
            centre = (i * pas + 0.5 * pas, j * pas + 0.5 * pas)
            valeur = _concentration_panache(
                scenario.vent,
                scenario.diffusivite,
                centre,
                scenario.source_vrai,
                scenario.debit_vrai,
            )
            concentration_maximale = max(concentration_maximale, valeur)
            if valeur >= scenario.seuil_detection:
                cellules_detectees += 1
    return cellules_detectees, concentration_maximale


def resoudre_scenario(scenario: ScenarioIdentification) -> ResultatIdentification:
    """Résout le scénario d'identification : observations, carte, vallée.

    Args:
        scenario: configuration immuable (vent, source, capteurs, grille).

    Returns:
        Les vents évalués aux mesures, les concentrations observées, les
        cellules détectées, le champ maximal, le coût nul, la carte des
        coûts minimaux avec sa position et son débit optimaux, la vallée
        du coût le long de l'axe du vent, et les valeurs du candidat
        décalé au vent.
    """
    observees = tuple(
        _concentration_panache(
            scenario.vent,
            scenario.diffusivite,
            capteur,
            scenario.source_vrai,
            scenario.debit_vrai,
        )
        for capteur in scenario.capteurs
    )
    cout_nul = sum(c * c for c in observees)
    couts, cout_minimum, position_estimee, debit_etoile = _grille_couts(
        scenario, observees, cout_nul
    )
    nombre_cellules_vallee, etendue_vallee, largeur_vallee = _vallee_cout(scenario, couts, cout_nul)
    cout_decale, debit_decale = _cout_minimal(
        scenario, scenario.candidat_decale, observees, cout_nul
    )
    dx_decale = scenario.candidat_decale[0] - scenario.source_vrai[0]
    dy_decale = scenario.candidat_decale[1] - scenario.source_vrai[1]
    decalage = math.sqrt(dx_decale * dx_decale + dy_decale * dy_decale)
    cellules_detectees, concentration_maximale = _detection_champ(scenario)
    return ResultatIdentification(
        vent_mesure_1=scenario.vent,
        vent_mesure_2=scenario.vent,
        vent_mesure_3=scenario.vent,
        concentrations_observees=observees,
        concentration_detection=observees[scenario.indice_detection],
        cellules_detectees=cellules_detectees,
        concentration_maximale=concentration_maximale,
        cout_nul=cout_nul,
        cout_minimum=cout_minimum,
        position_estimee=position_estimee,
        debit_etoile=debit_etoile,
        couts_grille=tuple(couts),
        nombre_cellules_vallee=nombre_cellules_vallee,
        etendue_vallee=etendue_vallee,
        largeur_vallee=largeur_vallee,
        cout_relatif_decale=cout_decale / cout_nul,
        debit_etoile_decale=debit_decale,
        decalage_vent=decalage,
    )


@dataclass(frozen=True)
class ManifesteIdentification:
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
    scenario: ScenarioIdentification
    resultat: ResultatIdentification
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
                "vent": list(scenario.vent),
                "diffusivite": scenario.diffusivite,
                "debit_vrai": scenario.debit_vrai,
                "source_vrai": list(scenario.source_vrai),
                "vignoble": [
                    list(scenario.vignoble.coin),
                    scenario.vignoble.largeur,
                    scenario.vignoble.hauteur,
                ],
                "mesures_vent": [list(mesure) for mesure in scenario.mesures_vent],
                "capteurs": [list(capteur) for capteur in scenario.capteurs],
                "indice_detection": scenario.indice_detection,
                "seuil_detection": scenario.seuil_detection,
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
                "pas_candidats": scenario.pas_candidats,
                "candidat_decale": list(scenario.candidat_decale),
            },
            "resultats": {
                "vent_mesure_1": list(self.resultat.vent_mesure_1),
                "vent_mesure_2": list(self.resultat.vent_mesure_2),
                "vent_mesure_3": list(self.resultat.vent_mesure_3),
                "concentrations_observees": list(self.resultat.concentrations_observees),
                "concentration_detection": self.resultat.concentration_detection,
                "cellules_detectees": self.resultat.cellules_detectees,
                "concentration_maximale": self.resultat.concentration_maximale,
                "cout_nul": self.resultat.cout_nul,
                "cout_minimum": self.resultat.cout_minimum,
                "position_estimee": list(self.resultat.position_estimee),
                "debit_etoile": self.resultat.debit_etoile,
                "nombre_cellules_vallee": self.resultat.nombre_cellules_vallee,
                "etendue_vallee": self.resultat.etendue_vallee,
                "largeur_vallee": self.resultat.largeur_vallee,
                "cout_relatif_decale": self.resultat.cout_relatif_decale,
                "debit_etoile_decale": self.resultat.debit_etoile_decale,
                "decalage_vent": self.resultat.decalage_vent,
            },
        }


def construire_manifeste(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
) -> ManifesteIdentification:
    """Assemble le manifeste de l'identification (métadonnées fixes).

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
    return ManifesteIdentification(
        identifiant="jdriftx-identification-source-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of Dispersion », "
            "chapitre 14, p. 255, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description=(
            "Identification de source : carte de sensibilité du coût d'ajustement, "
            "distincte d'une probabilité de source."
        ),
        hypothese=(
            "Transport advectif dominant : concentration nulle en amont de la source.",
            "Panache de similitude de la figure 3 : diffusivité transversale constante.",
            "Vent uniforme reconstruit à partir de trois mesures concordantes.",
            "Observations déterministes sans bruit aux cinq capteurs.",
            "Débit optimal en forme fermée par moindres carrés pour chaque candidat.",
        ),
        limites=(
            "Cas synthétique : aucune donnée ni paramètre historique.",
            "La carte de coût n'est pas une probabilité de source (aucun prior).",
            "Non-identifiabilité position-débit le long de l'axe du vent.",
            "Sans bruit : l'effet du bruit sur la vallée n'est pas traité.",
            "Ne constitue pas une reproduction quantitative du chapitre de 2008.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.identification_source import "
            "SCENARIO_DEFAUT, resoudre_scenario; print(resoudre_scenario(SCENARIO_DEFAUT))'"
        ),
    )
