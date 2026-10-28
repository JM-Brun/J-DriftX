"""Génère la figure 4 : les champs s'ajoutent, pas les régions affectées.

Le schéma est une reconstruction conceptuelle (niveau R1), étape C du plan
de figures du chapitre de 2008 : deux sources gaussiennes synthétiques dans
un champ de vent analytique incompressible, leurs contributions
individuelles et leur somme. La concentration totale est exactement la
somme des contributions (linéarité), mais les régions au-dessus du seuil
ne s'ajoutent pas : la région totale contient un « pont » entre les deux
disques, où chaque contribution seule reste sous le seuil. Ce n'est pas
une reproduction de la figure du chapitre Springer ni une validation
quantitative des données historiques.

Toutes les valeurs affichées proviennent de la tranche typée
``jdriftx.experiences.superposition_sources`` (configuration -> sources ->
champ -> mesures -> résultats -> manifeste) : la figure rend des résultats
calculés et ne peut pas diverger silencieusement de l'implémentation
testée. La sortie est déterministe ; la copie versionnée du SVG doit
rester strictement synchronisée (test d'égalité octet par octet).
"""

from __future__ import annotations

import math
from html import escape

from jdriftx.champ_analytique import ChampPlan
from jdriftx.experiences.superposition_sources import (
    SCENARIO_DEFAUT,
    SourceGaussienne,
    resoudre_scenario,
)

SVG_WIDTH = 1100
SVG_HEIGHT = 780

_COTE_FENETRE = 2000.0
ECHELLE_FENETRE = 0.16
PANEL_Y = 105.0
PANEL_A_X = 35.0
PANEL_B_X = 390.0
PANEL_C_X = 745.0
DECALAGE = 62.5
PAS_GRILLE = 250.0
ECHELLE_FLECHE = 5.0
PAS_CELLULE = 100.0


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


def _py(y: float) -> float:
    """Convertit une ordonnée monde (m) en pixels dans un panneau (axe y vers le haut)."""
    return PANEL_Y + (_COTE_FENETRE - y) * ECHELLE_FENETRE


def _fleches(
    champ: ChampPlan,
    x0: float,
    marqueur: str,
    couleur: str,
) -> tuple[list[str], float]:
    """Dessine la grille de flèches d'un champ ; renvoie éléments et norme maximale.

    Args:
        champ: champ plan stationnaire à représenter.
        x0: abscisse pixel d'origine du panneau.
        marqueur: identifiant du marqueur de pointe de flèche.
        couleur: couleur des flèches.

    Returns:
        Les éléments SVG des flèches et la norme maximale rencontrée (m s^-1).
    """
    elements: list[str] = []
    norme_max = 0.0
    for i in range(8):
        x = DECALAGE + i * PAS_GRILLE
        for j in range(8):
            y = DECALAGE + j * PAS_GRILLE
            u, v = champ.vitesse(x, y)
            norme = math.sqrt(u * u + v * v)
            norme_max = max(norme_max, norme)
            px = _px(x0, x)
            py = _py(y)
            elements.append(
                f'<line x1="{px:.1f}" y1="{py:.1f}" '
                f'x2="{px + u * ECHELLE_FLECHE:.1f}" y2="{py - v * ECHELLE_FLECHE:.1f}" '
                f'stroke="{couleur}" stroke-width="2" marker-end="url(#{marqueur})"/>'
            )
    return elements, norme_max


def _marquages(
    x0: float,
    mesures: tuple[tuple[float, float], ...],
    vents: tuple[tuple[float, float], ...],
) -> list[str]:
    """Dessine les points de mesure, leur vent évalué et leurs étiquettes."""
    elements: list[str] = []
    for etiquette, point, vent in zip(("M1", "M2", "M3"), mesures, vents, strict=True):
        px = _px(x0, point[0])
        py = _py(point[1])
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#202833"/>')
        elements.append(
            f'<line x1="{px:.1f}" y1="{py:.1f}" '
            f'x2="{px + vent[0] * ECHELLE_FLECHE:.1f}" '
            f'y2="{py - vent[1] * ECHELLE_FLECHE:.1f}" '
            'stroke="#202833" stroke-width="3" marker-end="url(#flecheM)"/>'
        )
        elements.append(_text(px + 9.0, py - 9.0, etiquette, size=14, weight="bold"))
    return elements


def _panneau_source_seule(
    x0: float,
    active: SourceGaussienne,
    inactive: SourceGaussienne,
    rayon: float,
    etiquette_active: str,
    etiquette_inactive: str,
) -> list[str]:
    """Dessine un panneau : disque affecté d'une source, l'autre en creux."""
    px_a = _px(x0, active.position[0])
    py_a = _py(active.position[1])
    px_i = _px(x0, inactive.position[0])
    py_i = _py(inactive.position[1])
    return [
        f'<circle cx="{px_a:.1f}" cy="{py_a:.1f}" r="{rayon * ECHELLE_FENETRE:.1f}" '
        'fill="#dbe9f7" stroke="#2864a5" stroke-width="2"/>',
        f'<circle cx="{px_i:.1f}" cy="{py_i:.1f}" r="6" fill="#ffffff" '
        'stroke="#8a94a3" stroke-width="2" stroke-dasharray="4 3"/>',
        f'<circle cx="{px_a:.1f}" cy="{py_a:.1f}" r="6" fill="#2864a5"/>',
        _text(px_a - 16.0, py_a - 12.0, etiquette_active, size=14, weight="bold"),
        _text(px_i + 10.0, py_i - 10.0, etiquette_inactive, size=13),
    ]


def _panneau_somme(
    x0: float,
    source_1: SourceGaussienne,
    source_2: SourceGaussienne,
    seuil: float,
    rayon_1: float,
    rayon_2: float,
) -> tuple[list[str], int]:
    """Dessine la région totale {c1 + c2 >= seuil} en cellules de la grille."""
    elements: list[str] = []
    cellules = 0
    nombre = int(_COTE_FENETRE / PAS_CELLULE) + 1
    demi = PAS_CELLULE / 2.0
    for i in range(nombre):
        x = i * PAS_CELLULE
        for j in range(nombre):
            y = j * PAS_CELLULE
            totale = source_1.concentration(x, y) + source_2.concentration(x, y)
            if totale >= seuil:
                cellules += 1
                elements.append(
                    f'<rect x="{_px(x0, x - demi):.1f}" y="{_py(y + demi):.1f}" '
                    f'width="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                    f'height="{PAS_CELLULE * ECHELLE_FENETRE:.1f}" '
                    'fill="#cfe0f2" stroke="#8fb3d9" stroke-width="1"/>'
                )
    for source, rayon in ((source_1, rayon_1), (source_2, rayon_2)):
        px = _px(x0, source.position[0])
        py = _py(source.position[1])
        elements.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rayon * ECHELLE_FENETRE:.1f}" '
            'fill="none" stroke="#2864a5" stroke-width="2" stroke-dasharray="6 5"/>'
        )
    for source, etiquette in ((source_1, "S1"), (source_2, "S2")):
        px = _px(x0, source.position[0])
        py = _py(source.position[1])
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#2864a5"/>')
        elements.append(_text(px - 16.0, py - 12.0, etiquette, size=14, weight="bold"))
    return elements, cellules


def render_figure_04_svg() -> str:
    """Renvoie le SVG déterministe de la figure 4 (étape C : superposition)."""
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    vents = (resultat.vent_mesure_1, resultat.vent_mesure_2, resultat.vent_mesure_3)
    for vent in vents:
        if math.hypot(vent[0], vent[1]) < 1.0:
            msg = "Le scénario exige des mesures de vent assez fortes pour être lisibles."
            raise ValueError(msg)
    if resultat.divergence_max >= 1e-12:
        msg = "La divergence numérique du champ doit rester sous 1e-12 s^-1."
        raise ValueError(msg)
    if min(resultat.rayon_affecte_1, resultat.rayon_affecte_2) * ECHELLE_FENETRE < 15.0:
        msg = "Les disques affectés doivent rester visibles à l'échelle du panneau."
        raise ValueError(msg)
    if resultat.concentration_max_totale <= max(
        scenario.source_1.amplitude, scenario.source_2.amplitude
    ):
        msg = "La somme doit dépasser chaque contribution maximale individuelle."
        raise ValueError(msg)
    fleches_a, norme_a = _fleches(scenario.champ_vent, PANEL_A_X, "flecheA", "#2c7a55")
    fleches_b, norme_b = _fleches(scenario.champ_vent, PANEL_B_X, "flecheB", "#2c7a55")
    fleches_c, norme_c = _fleches(scenario.champ_vent, PANEL_C_X, "flecheC", "#2c7a55")
    if max(norme_a, norme_b, norme_c) * ECHELLE_FLECHE >= 40.0:
        msg = "Les flèches se chevaucheraient : réduire l'échelle des flèches."
        raise ValueError(msg)
    panneau_c, cellules = _panneau_somme(
        PANEL_C_X,
        scenario.source_1,
        scenario.source_2,
        scenario.seuil,
        resultat.rayon_affecte_1,
        resultat.rayon_affecte_2,
    )
    if cellules == 0:
        msg = "La région totale {c1 + c2 >= seuil} ne doit pas être vide."
        raise ValueError(msg)
    if cellules * PAS_CELLULE * PAS_CELLULE != resultat.surface_affectee_totale:
        msg = "La figure et la tranche doivent compter les mêmes cellules affectées."
        raise ValueError(msg)
    lignes_mesures: list[str] = []
    for indice, (etiquette, vent) in enumerate(zip(("M1", "M2", "M3"), vents, strict=True)):
        u = formate_composante(vent[0])
        v = formate_composante(vent[1])
        ligne = f"u({etiquette}) = ({u}, {v}) m/s"
        lignes_mesures.append(_text(32.0, 498.0 + 28.0 * indice, ligne, size=15))
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Figure 4 : les champs s\'ajoutent, pas les régions</title>',
        '<desc id="desc">Deux sources gaussiennes dans un champ de vent '
        "incompressible : contributions individuelles et somme.</desc>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(
            32.0,
            38.0,
            "Figure 4 — Deux sources : les champs s'ajoutent, pas les régions",
            size=22,
            weight="bold",
        ),
        _text(
            32.0,
            66.0,
            "Deux sources gaussiennes dans un champ de vent incompressible : "
            "contributions individuelles et somme.",
            size=16,
        ),
        "<defs>",
        '<marker id="flecheA" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker>',
        '<marker id="flecheB" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker>',
        '<marker id="flecheC" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker>',
        '<marker id="flecheM" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#202833"/></marker>',
        "</defs>",
        _text(35.0, 92.0, "A. Source S1 seule", size=16, weight="bold"),
        '<rect x="30" y="100" width="330" height="330" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *fleches_a,
        *_panneau_source_seule(
            PANEL_A_X,
            scenario.source_1,
            scenario.source_2,
            resultat.rayon_affecte_1,
            "S1",
            "S2",
        ),
        *_marquages(PANEL_A_X, scenario.mesures, vents),
        _text(390.0, 92.0, "B. Source S2 seule", size=16, weight="bold"),
        '<rect x="385" y="100" width="330" height="330" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *fleches_b,
        *_panneau_source_seule(
            PANEL_B_X,
            scenario.source_2,
            scenario.source_1,
            resultat.rayon_affecte_2,
            "S2",
            "S1",
        ),
        *_marquages(PANEL_B_X, scenario.mesures, vents),
        _text(745.0, 92.0, "C. Somme c1 + c2 (grille 100 m)", size=16, weight="bold"),
        '<rect x="740" y="100" width="330" height="330" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *fleches_c,
        *panneau_c,
        *_marquages(PANEL_C_X, scenario.mesures, vents),
        _text(32.0, 470.0, "Trois mesures de vent évaluées", size=17, weight="bold"),
        *lignes_mesures,
        _text(32.0, 590.0, "Champ analytique incompressible :", size=15),
        _text(32.0, 614.0, "∇·u < 1e-12 s⁻¹ (grille 100 m)", size=15),
        _text(32.0, 638.0, "Trois mesures ne rendent pas le champ unique.", size=15),
        _text(400.0, 470.0, "Seuil et régions affectées", size=17, weight="bold"),
        _text(400.0, 498.0, f"Seuil : {scenario.seuil:.1f} (concentration relative)", size=15),
        _text(400.0, 526.0, f"r1 = r2 = {resultat.rayon_affecte_1:.1f} m", size=15),
        _text(
            400.0,
            554.0,
            f"S1 = S2 = {_entier_espace(int(resultat.surface_affectee_1))} m²",
            size=15,
        ),
        _text(
            400.0,
            590.0,
            f"Région totale (grille 100 m) : "
            f"{_entier_espace(int(resultat.surface_affectee_totale))} m²",
            size=15,
        ),
        _text(400.0, 614.0, "Région totale > S1 + S2 : dans le pont,", size=15),
        _text(400.0, 638.0, "chaque contribution seule est sous le seuil.", size=15),
        _text(742.0, 470.0, "Additivité supposée", size=17, weight="bold"),
        _text(742.0, 498.0, "c = c1 + c2 exact (équation de transport linéaire) ;", size=15),
        _text(742.0, 526.0, "les régions affectées, elles, ne s'ajoutent pas.", size=15),
        _text(
            742.0,
            554.0,
            f"Contribution de S2 en S1 : {resultat.contribution_croisee_1:.4f}",
            size=15,
        ),
        _text(
            742.0,
            582.0,
            f"Concentration max (somme, grille) : {resultat.concentration_max_totale:.3f}",
            size=15,
        ),
        _text(742.0, 616.0, "Aucune donnée historique : niveau R1.", size=15),
        _text(
            30.0,
            760.0,
            "Reconstruction conceptuelle (R1) ; cas synthétique ; pas une "
            "reproduction quantitative du chapitre de 2008 (p. 254).",
            size=13,
        ),
        "</svg>",
    ]
    return "\n".join(elements) + "\n"
