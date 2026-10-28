"""Génère la figure 5 : la correction de relief déplace le point de calcul.

Le schéma est une reconstruction conceptuelle (niveau R1), étape D du
plan de figures du chapitre de 2008 : un MNT synthétique de 2 km × 2 km
(deux collines gaussiennes), une source de scalaire passif dans un vent
uniforme du nord, et les régions affectées par un panache gaussien
évalué sans correction (le relief est ignoré : le sol du modèle est le
plan z = 0) puis avec correction (le point de calcul suit le sol réel).
Le vent, la source et les écarts-types de Briggs sont identiques dans
les deux calculs : seule l'altitude du point de calcul change, et hors
des collines les deux cartes coïncident. Ce n'est pas une reproduction
de la figure du chapitre Springer ni une validation quantitative des
données historiques.

Toutes les valeurs affichées proviennent de la tranche typée
``jdriftx.experiences.relief`` (configuration -> collines -> vent ->
source -> résultats -> manifeste) : la figure rend des résultats
calculés et ne peut pas diverger silencieusement de l'implémentation
testée. La sortie est déterministe ; la copie versionnée du SVG doit
rester strictement synchronisée (test d'égalité octet par octet).
"""

from __future__ import annotations

import math
from html import escape

from jdriftx.experiences.relief import (
    SCENARIO_DEFAUT,
    ScenarioRelief,
    concentrations_au_point,
    resoudre_scenario,
)

SVG_WIDTH = 1100
SVG_HEIGHT = 780

_COTE_FENETRE = 2000.0
ECHELLE_FENETRE = 0.15
PAS_CELLULE = 50.0
LIGNE1_Y = 100.0
LIGNE2_Y = 440.0
PANEL_A_X = 35.0
PANEL_B_X = 390.0
PANEL_C_X = 35.0
PANEL_D_X = 390.0
DECALAGE = 62.5
PAS_GRILLE = 250.0
ECHELLE_FLECHE = 5.0
SEUILS_BANDES = (5.0, 15.0, 25.0, 35.0)
COULEURS_BANDES = ("#ece0c8", "#dbc49e", "#c9ac7c", "#b5905b")


def formate_composante(valeur: float) -> str:
    """Formate une composante de vent ; la poussière numérique rend « 0.00 »."""
    if abs(valeur) < 1e-9:
        return "0.00"
    return f"{valeur:+.2f}"


def _entier_espace(valeur: int) -> str:
    """Formate un entier avec un espace comme séparateur de milliers."""
    return f"{valeur:,}".replace(",", " ")


def _text(x: float, y: float, value: str, *, size: int = 17, weight: str = "normal") -> str:
    """Renvoie un élément text SVG échappé."""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" fill="#202833">{escape(value)}</text>'
    )


def _px(x0: float, x: float) -> float:
    """Convertit une abscisse monde (m) en pixels dans un panneau."""
    return x0 + x * ECHELLE_FENETRE


def _py(y0: float, y: float) -> float:
    """Convertit une ordonnée monde (m) en pixels (axe y vers le haut)."""
    return y0 + (_COTE_FENETRE - y) * ECHELLE_FENETRE


def _fleches_uniformes(x0: float, y0: float, u: float, v: float) -> list[str]:
    """Dessine la grille de flèches du vent uniforme d'un panneau."""
    elements: list[str] = []
    for i in range(8):
        x = DECALAGE + i * PAS_GRILLE
        for j in range(8):
            y = DECALAGE + j * PAS_GRILLE
            px = _px(x0, x)
            py = _py(y0, y)
            elements.append(
                f'<line x1="{px:.1f}" y1="{py:.1f}" '
                f'x2="{px + u * ECHELLE_FLECHE:.1f}" y2="{py - v * ECHELLE_FLECHE:.1f}" '
                'stroke="#2c7a55" stroke-width="2" marker-end="url(#flecheV)"/>'
            )
    return elements


def _marquages(x0: float, y0: float, scenario: ScenarioRelief) -> list[str]:
    """Dessine la source et les deux sommets de collines avec leurs étiquettes."""
    elements: list[str] = []
    px_s = _px(x0, scenario.source[0])
    py_s = _py(y0, scenario.source[1])
    elements.append(f'<circle cx="{px_s:.1f}" cy="{py_s:.1f}" r="6" fill="#2864a5"/>')
    elements.append(_text(px_s + 9.0, py_s - 9.0, "S", size=14, weight="bold"))
    for etiquette, colline in zip(("A", "B"), scenario.collines, strict=True):
        px = _px(x0, colline.centre[0])
        py = _py(y0, colline.centre[1])
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#7a5c2e"/>')
        elements.append(_text(px + 9.0, py - 9.0, etiquette, size=14, weight="bold"))
    return elements


def _panneau_mnt(x0: float, y0: float, scenario: ScenarioRelief) -> list[str]:
    """Dessine le MNT synthétique en bandes d'altitude (cellules 50 m)."""
    elements: list[str] = []
    nombre = int(_COTE_FENETRE / PAS_CELLULE) + 1
    demi = PAS_CELLULE / 2.0
    x_origine = scenario.fenetre.coin[0]
    y_origine = scenario.fenetre.coin[1]
    for i in range(nombre):
        x = x_origine + i * PAS_CELLULE
        for j in range(nombre):
            y = y_origine + j * PAS_CELLULE
            altitude = scenario.altitude_sol(x, y)
            if altitude < SEUILS_BANDES[0]:
                continue
            bande = sum(1 for seuil in SEUILS_BANDES if altitude >= seuil) - 1
            elements.append(
                f'<rect x="{_px(x0, x - demi):.1f}" y="{_py(y0, y + demi):.1f}" '
                f'width="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                f'height="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                f'fill="{COULEURS_BANDES[bande]}" stroke="#a89478" stroke-width="1"/>'
            )
    return elements


def _panneau_region(
    x0: float,
    y0: float,
    scenario: ScenarioRelief,
    *,
    avec_correction: bool,
) -> tuple[list[str], int]:
    """Dessine la région {c >= seuil} en cellules de la grille 50 m."""
    elements: list[str] = []
    cellules = 0
    nombre = int(_COTE_FENETRE / PAS_CELLULE) + 1
    demi = PAS_CELLULE / 2.0
    x_origine = scenario.fenetre.coin[0]
    y_origine = scenario.fenetre.coin[1]
    for i in range(nombre):
        x = x_origine + i * PAS_CELLULE
        for j in range(nombre):
            y = y_origine + j * PAS_CELLULE
            c_sans, c_avec = concentrations_au_point(scenario, x, y)
            concentration = c_avec if avec_correction else c_sans
            if concentration >= scenario.seuil:
                cellules += 1
                elements.append(
                    f'<rect x="{_px(x0, x - demi):.1f}" y="{_py(y0, y + demi):.1f}" '
                    f'width="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                    f'height="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                    'fill="#dbe9f7" stroke="#8fb3d9" stroke-width="1"/>'
                )
    return elements, cellules


def render_figure_05_svg() -> str:
    """Renvoie le SVG déterministe de la figure 5 (étape D : relief)."""
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    u, v = scenario.vent
    if math.hypot(u, v) < 1.0:
        msg = "Le scénario exige un vent assez fort pour être lisible."
        raise ValueError(msg)
    if resultat.altitude_max_mnt + scenario.hauteur_evaluation >= resultat.altitude_axe:
        msg = "Les collines doivent rester sous l'axe du panache."
        raise ValueError(msg)
    if resultat.cellules_sans == 0 or resultat.cellules_avec == 0:
        msg = "Les régions affectées ne doivent pas être vides."
        raise ValueError(msg)
    if resultat.cellules_avec <= resultat.cellules_sans:
        msg = "La correction doit élargir la région affectée."
        raise ValueError(msg)
    if resultat.ratio_sommet_1 < 1.5:
        msg = "L'effet de la correction doit rester lisible sur la première colline."
        raise ValueError(msg)
    if math.hypot(u, v) * ECHELLE_FLECHE >= 40.0:
        msg = "Les flèches se chevaucheraient : réduire l'échelle des flèches."
        raise ValueError(msg)
    panneau_c, cellules_c = _panneau_region(PANEL_C_X, LIGNE2_Y, scenario, avec_correction=False)
    if cellules_c != resultat.cellules_sans:
        msg = "La figure et la tranche doivent compter les mêmes cellules sans correction."
        raise ValueError(msg)
    panneau_d, cellules_d = _panneau_region(PANEL_D_X, LIGNE2_Y, scenario, avec_correction=True)
    if cellules_d != resultat.cellules_avec:
        msg = "La figure et la tranche doivent compter les mêmes cellules avec correction."
        raise ValueError(msg)
    u_txt = formate_composante(u)
    v_txt = formate_composante(v)
    ligne_vent = f"u = ({u_txt}, {v_txt}) m/s, identique dans les deux calculs."
    debit_txt = f"{scenario.debit:.1f}"
    ligne_panache = f"Panache gaussien (Briggs, classe {scenario.classe}) : Q = {debit_txt} kg/s,"
    hauteur_txt = f"{scenario.hauteur_source:.0f}"
    axe_txt = f"{resultat.altitude_axe:.1f}"
    evaluation_txt = f"{scenario.hauteur_evaluation:.0f}"
    ligne_geometrie = (
        f"h = {hauteur_txt} m ; axe à {axe_txt} m ; "
        f"point à {evaluation_txt} m du sol."
    )
    ligne_seuil = f"Seuil : {scenario.seuil:.1e} kg m⁻³"
    surface_sans_txt = _entier_espace(int(resultat.surface_region_sans))
    ligne_sans = f"Région sans : {surface_sans_txt} m² ({resultat.cellules_sans} cellules)"
    surface_avec_txt = _entier_espace(int(resultat.surface_region_avec))
    ligne_avec = f"Région avec : {surface_avec_txt} m² ({resultat.cellules_avec} cellules)"
    ligne_cmax_sans = f"c max sans : {resultat.concentration_max_sans:.1e} kg m⁻³"
    ligne_cmax_avec = f"c max avec : {resultat.concentration_max_avec:.1e} kg m⁻³"
    ligne_ratio_1 = f"Ratio au sommet A : \u00d7{resultat.ratio_sommet_1:.2f}"
    ligne_ratio_2 = f"Ratio au sommet B : \u00d7{resultat.ratio_sommet_2:.2f}"
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Figure 5 : la correction de relief déplace le point de calcul</title>',
        '<desc id="desc">MNT synthétique, vent uniforme du nord : régions affectées '
        "sans et avec correction de relief.</desc>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(
            32.0,
            38.0,
            "Figure 5 — Relief : la correction déplace le point de calcul",
            size=22,
            weight="bold",
        ),
        _text(
            32.0,
            66.0,
            "MNT synthétique, vent uniforme du nord : régions affectées sans et "
            "avec correction de relief.",
            size=16,
        ),
        "<defs>",
        '<marker id="flecheV" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker>',
        "</defs>",
        _text(35.0, 92.0, "A. MNT synthétique (cellules 50 m)", size=16, weight="bold"),
        '<rect x="30" y="95" width="310" height="310" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *_panneau_mnt(PANEL_A_X, LIGNE1_Y, scenario),
        *_marquages(PANEL_A_X, LIGNE1_Y, scenario),
        _text(390.0, 92.0, "B. Vent uniforme du nord", size=16, weight="bold"),
        '<rect x="385" y="95" width="310" height="310" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *_fleches_uniformes(PANEL_B_X, LIGNE1_Y, u, v),
        _text(
            35.0,
            432.0,
            "C. Sans correction : relief ignoré (grille 50 m)",
            size=16,
            weight="bold",
        ),
        '<rect x="30" y="435" width="310" height="310" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_c,
        *_marquages(PANEL_C_X, LIGNE2_Y, scenario),
        _text(
            390.0,
            432.0,
            f"D. Avec correction : {scenario.hauteur_evaluation:.0f} m au-dessus du sol réel",
            size=16,
            weight="bold",
        ),
        '<rect x="385" y="435" width="310" height="310" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_d,
        *_marquages(PANEL_D_X, LIGNE2_Y, scenario),
        _text(745.0, 100.0, "MNT synthétique (niveau R1)", size=17, weight="bold"),
        _text(745.0, 128.0, "Deux collines gaussiennes sur l'axe du panache :", size=15),
        _text(745.0, 152.0, "A : 40 m (échelle 90 m), à 300 m sous le vent ;", size=15),
        _text(745.0, 176.0, "B : 35 m (échelle 60 m), à 500 m sous le vent.", size=15),
        _text(745.0, 200.0, "Source posée sur un sol quasi plat (relief < 0,5 m).", size=15),
        _text(745.0, 232.0, "Vent et panache", size=17, weight="bold"),
        _text(745.0, 260.0, ligne_vent, size=15),
        _text(745.0, 284.0, ligne_panache, size=15),
        _text(745.0, 308.0, ligne_geometrie, size=15),
        _text(745.0, 332.0, "Réflexion au sol du modèle référée à z = 0.", size=15),
        _text(745.0, 364.0, "Sans / avec correction", size=17, weight="bold"),
        _text(745.0, 392.0, "Sans : le sol du modèle est le plan z = 0.", size=15),
        _text(745.0, 416.0, "Avec : le point suit le sol réel, le panache ne change pas.", size=15),
        _text(745.0, 440.0, "Vent, source et σ(x) identiques : ablation.", size=15),
        _text(745.0, 472.0, "Résultats (tranche typée)", size=17, weight="bold"),
        _text(745.0, 500.0, ligne_seuil, size=15),
        _text(745.0, 524.0, ligne_sans, size=15),
        _text(745.0, 548.0, ligne_avec, size=15),
        _text(745.0, 572.0, ligne_cmax_sans, size=15),
        _text(745.0, 596.0, ligne_cmax_avec, size=15),
        _text(745.0, 620.0, ligne_ratio_1, size=15),
        _text(745.0, 644.0, ligne_ratio_2, size=15),
        _text(745.0, 676.0, "Lecture", size=17, weight="bold"),
        _text(
            745.0,
            704.0,
            "Hors des collines, les cartes coïncident ; la correction n'ajoute",
            size=15,
        ),
        _text(
            745.0,
            728.0,
            "des cellules qu'aux crêtes, et l'effet décroît quand σz croît.",
            size=15,
        ),
        _text(
            30.0,
            765.0,
            "Reconstruction conceptuelle (R1) ; MNT synthétique ; pas une "
            "reproduction quantitative du chapitre de 2008 (pp. 254-255).",
            size=13,
        ),
        "</svg>",
    ]
    return "\n".join(elements) + "\n"
