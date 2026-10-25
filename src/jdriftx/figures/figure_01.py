"""Génère la figure 1 : deux mesures ne déterminent pas un champ unique.

Le schéma est une reconstruction conceptuelle (niveau R1), étape B du plan
de figures du chapitre de 2008 : deux champs de vent incompressibles très
différents coïncident exactement aux deux points de mesure, donc un champ
interpolé à partir de deux mesures n'est pas unique. Ce n'est pas une
reproduction de la figure du chapitre Springer ni une validation
quantitative des données historiques.

Toutes les valeurs affichées proviennent de la tranche typée
``jdriftx.experiences.reconstruction_vent`` (configuration -> champs ->
mesures -> résultats -> manifeste) : la figure rend des résultats calculés
et ne peut pas diverger silencieusement de l'implémentation testée.
"""

from __future__ import annotations

import math
from html import escape

from jdriftx.champ_analytique import ChampPlan
from jdriftx.experiences.reconstruction_vent import SCENARIO_DEFAUT, resoudre_scenario

SVG_WIDTH = 1100
SVG_HEIGHT = 700

_COTE_FENETRE = 2000.0
ECHELLE_FENETRE = 0.16
PANEL_X_GAUCHE = 50.0
PANEL_X_DROIT = 730.0
PANEL_Y = 120.0
DECALAGE = 62.5
PAS_GRILLE = 250.0
ECHELLE_FLECHE = 5.0
ECHELLE_ZOOM = 0.7
ZOOM_X = 30.0
ZOOM_ORIGINE_X = 100.0
ZOOM_Y = 516.0
ZOOM_ORIGINE_Y = 700.0
ENCART_X = 590.0
ENCART_Y = 516.0
COTE_ENCART = 100.0
ECHELLE_ENCART = 0.005


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


def _zx(x: float) -> float:
    """Convertit une abscisse monde (m) en pixels dans le zoom parcelle."""
    return ZOOM_X + (x - ZOOM_ORIGINE_X) * ECHELLE_ZOOM


def _zy(y: float) -> float:
    """Convertit une ordonnée monde (m) en pixels dans le zoom (axe y vers le haut)."""
    return ZOOM_Y + (ZOOM_ORIGINE_Y - y) * ECHELLE_ZOOM


def _dx(x: float) -> float:
    """Convertit une abscisse monde du domaine (m) en pixels dans l'encart."""
    return ENCART_X + x * ECHELLE_ENCART


def _dy(y: float) -> float:
    """Convertit une ordonnée monde du domaine (m) en pixels dans l'encart."""
    return ENCART_Y + COTE_ENCART - y * ECHELLE_ENCART


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
    """Dessine les points de mesure, leur vent mesuré et leurs étiquettes."""
    elements: list[str] = []
    for etiquette, point, vent in zip(("M1", "M2"), mesures, vents, strict=True):
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


def render_figure_01_svg() -> str:
    """Renvoie le SVG déterministe de la figure 1 (Étape B : non-unicité)."""
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    vent_1 = resultat.vent_mesure_1
    vent_2 = resultat.vent_mesure_2
    if abs(vent_1[0]) < 0.5 or abs(vent_2[0]) < 0.5:
        msg = "Le scénario exige des mesures assez fortes pour être lisibles à l'échelle."
        raise ValueError(msg)
    if resultat.ecart_entre_choix >= 1e-10:
        msg = "Les deux choix doivent coïncider aux mesures à 1e-10 m/s près."
        raise ValueError(msg)
    if max(resultat.divergence_max_choix_1, resultat.divergence_max_choix_2) >= 1e-12:
        msg = "La divergence numérique des deux champs doit rester sous 1e-12 s^-1."
        raise ValueError(msg)
    fleches_a, norme_a = _fleches(scenario.champ_choix_1, PANEL_X_GAUCHE, "flecheA", "#2c7a55")
    fleches_b, norme_b = _fleches(scenario.champ_choix_2, PANEL_X_DROIT, "flecheB", "#7a5230")
    if max(norme_a, norme_b) * ECHELLE_FLECHE >= 40.0:
        msg = "Les flèches se chevaucheraient : réduire l'échelle des flèches."
        raise ValueError(msg)
    surface_parcelle = scenario.parcelle.surface
    surface_domaine = scenario.domaine.surface
    rapport = int(surface_domaine / surface_parcelle)
    coin = scenario.parcelle.coin
    largeur = scenario.parcelle.largeur
    hauteur = scenario.parcelle.hauteur
    points = " ".join(f"{_zx(x):.1f},{_zy(y):.1f}" for x, y in scenario.trajectoire)
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Figure 1 : deux mesures ne déterminent pas un champ unique</title>',
        '<desc id="desc">Deux champs de vent incompressibles très différents '
        "coïncident aux deux points de mesure M1 et M2.</desc>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(
            32.0,
            38.0,
            "Figure 1 — Deux mesures ne déterminent pas un champ unique",
            size=25,
            weight="bold",
        ),
        _text(
            32.0,
            66.0,
            "Deux champs incompressibles très différents coïncident aux deux mesures : "
            "le champ interpolé n'est pas unique.",
            size=16,
        ),
        "<defs>",
        '<marker id="flecheA" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker>',
        '<marker id="flecheB" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#7a5230"/></marker>',
        '<marker id="flecheM" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#202833"/></marker>',
        '<marker id="flecheT" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2864a5"/></marker>',
        "</defs>",
        _text(34.0, 82.0, "A. Choix 1 : champ cellulaire", size=21, weight="bold"),
        '<rect x="30" y="100" width="360" height="360" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *fleches_a,
        *_marquages(PANEL_X_GAUCHE, scenario.mesures, (vent_1, vent_2)),
        _text(714.0, 82.0, "B. Choix 2 : champ superposé", size=21, weight="bold"),
        '<rect x="710" y="100" width="360" height="360" fill="#f8f5f1" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *fleches_b,
        *_marquages(PANEL_X_DROIT, scenario.mesures, (vent_1, vent_2)),
        _text(402.0, 82.0, "Deux mesures communes", size=17, weight="bold"),
        _text(
            402.0,
            116.0,
            f"u(M1) = ({formate_composante(vent_1[0])}, {formate_composante(vent_1[1])}) m/s",
            size=16,
        ),
        _text(
            402.0,
            144.0,
            f"u(M2) = ({formate_composante(vent_2[0])}, {formate_composante(vent_2[1])}) m/s",
            size=16,
        ),
        _text(402.0, 182.0, "Écart entre les deux choix", size=16),
        _text(402.0, 208.0, "aux mesures : < 1e-10 m/s", size=16),
        _text(402.0, 246.0, "∇·u < 1e-12 s⁻¹ (grille 100 m)", size=15),
        _text(
            402.0,
            284.0,
            f"Parcelle : {_entier_espace(int(surface_parcelle))} m² (1 ha)",
            size=15,
        ),
        _text(
            402.0,
            312.0,
            f"Domaine : {int(scenario.domaine.largeur / 1000.0)} km sur "
            f"{int(scenario.domaine.hauteur / 1000.0)} km "
            f"({_entier_espace(int(surface_domaine / 1_000_000.0))} km²)",
            size=15,
        ),
        _text(402.0, 356.0, f"Rapport des surfaces : {_entier_espace(rapport)}", size=15),
        _text(30.0, 482.0, "C. Zoom sur la parcelle", size=16, weight="bold"),
        '<rect x="30" y="516" width="140" height="140" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        f'<rect x="{_zx(coin[0]):.1f}" y="{_zy(coin[1] + hauteur):.1f}" '
        f'width="{largeur * ECHELLE_ZOOM:.1f}" height="{hauteur * ECHELLE_ZOOM:.1f}" '
        'fill="none" stroke="#2864a5" stroke-width="2"/>',
        f'<polyline points="{points}" fill="none" stroke="#2864a5" '
        'stroke-width="2" marker-end="url(#flecheT)"/>',
        f'<circle cx="{_zx(scenario.trajectoire[0][0]):.1f}" '
        f'cy="{_zy(scenario.trajectoire[0][1]):.1f}" r="4" fill="#2864a5"/>',
        f'<line x1="{_zx(coin[0]):.1f}" y1="641.0" x2="{_zx(coin[0] + largeur):.1f}" '
        'y2="641.0" stroke="#202833" stroke-width="2"/>',
        _text(_zx(coin[0]) + 17.0, 636.0, f"{int(largeur)} m", size=13),
        _text(
            30.0,
            674.0,
            f"Trajectoire relevée au sol : {resultat.longueur_trajectoire:.0f} m",
            size=14,
        ),
        _text(590.0, 482.0, "D. Domaine, fenêtre et parcelle", size=16, weight="bold"),
        '<rect x="590" y="516" width="100" height="100" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        f'<rect x="{_dx(0.0):.1f}" y="{_dy(_COTE_FENETRE):.1f}" '
        f'width="{_COTE_FENETRE * ECHELLE_ENCART:.1f}" '
        f'height="{_COTE_FENETRE * ECHELLE_ENCART:.1f}" '
        'fill="none" stroke="#7a5230" stroke-width="1.5"/>',
        f'<circle cx="{_dx(coin[0] + largeur / 2.0):.1f}" '
        f'cy="{_dy(coin[1] + hauteur / 2.0):.1f}" r="2.5" fill="#2864a5"/>',
        _text(590.0, 640.0, "Cadre : domaine d'étude", size=12),
        _text(
            590.0,
            658.0,
            f"Rectangle : fenêtre {int(_COTE_FENETRE / 1000.0)} km "
            f"sur {int(_COTE_FENETRE / 1000.0)} km",
            size=12,
        ),
        _text(590.0, 676.0, "Point : parcelle 1 ha", size=12),
        _text(714.0, 482.0, "Niveau R1 — reconstruction conceptuelle", size=16, weight="bold"),
        _text(714.0, 516.0, "Schéma original créé pour J-DriftX :", size=14),
        _text(714.0, 540.0, "pas une reproduction de la figure du chapitre", size=14),
        _text(714.0, 564.0, "Springer, ni une validation quantitative des", size=14),
        _text(714.0, 588.0, "données historiques.", size=14),
        _text(
            32.0,
            690.0,
            "Cas synthétique ; pas une reproduction quantitative du chapitre de 2008.",
            size=13,
        ),
        "</svg>",
    ]
    return "\n".join(elements) + "\n"
