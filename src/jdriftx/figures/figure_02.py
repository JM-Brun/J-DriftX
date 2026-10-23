"""Generate an original schematic of symmetric and directed distances.

The diagram is an explanatory reconstruction (R0/R1), not a reproduction of
Springer's artwork or a quantitative validation of the historical algorithm.
It uses a uniform, non-zero wind and the convention implemented by
``pseudo_distance_uniforme``: only the positive longitudinal displacement is
charged; a target upstream receives an infinite cost.
"""

from __future__ import annotations

from html import escape

SVG_WIDTH = 1100
SVG_HEIGHT = 520


def _text(x: int, y: int, value: str, *, size: int = 17, weight: str = "normal") -> str:
    """Return one escaped SVG text element."""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" '
        f'font-weight="{weight}" fill="#202833">{escape(value)}</text>'
    )


def render_figure_02_svg() -> str:
    """Return a deterministic, dependency-free SVG explanatory figure."""
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Distance euclidienne et temps de transport dirigé</title>',
        '<desc id="desc">Deux schémas comparant la distance géométrique symétrique '
        'au coût longitudinal orienté par un vent uniforme.</desc>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(32, 38, "Figure 2 — Deux notions de distance", size=25, weight="bold"),
        '<line x1="550" y1="65" x2="550" y2="485" stroke="#d5dbe3" stroke-width="2"/>',
        _text(34, 82, "A. Distance euclidienne", size=21, weight="bold"),
        _text(34, 110, "Symétrique : dE(A, B) = dE(B, A)", size=16),
        '<line x1="130" y1="300" x2="420" y2="190" stroke="#2864a5" stroke-width="4"/>',
        '<circle cx="130" cy="300" r="8" fill="#2864a5"/>',
        '<circle cx="420" cy="190" r="8" fill="#c45132"/>',
        _text(108, 326, "A", size=20, weight="bold"),
        _text(430, 190, "B", size=20, weight="bold"),
        _text(200, 224, "segment direct", size=16),
        _text(34, 430, "La longueur ne dépend pas du sens de parcours.", size=16),
        _text(580, 82, "B. Coût de migration dirigé", size=21, weight="bold"),
        _text(580, 110, "Vent uniforme vers +x : u = (U, 0), U > 0", size=16),
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2c7a55"/></marker></defs>',
        '<line x1="610" y1="155" x2="1010" y2="155" stroke="#2c7a55" '
        'stroke-width="3" marker-end="url(#arrow)"/>',
        _text(770, 145, "vent", size=15),
        '<line x1="650" y1="310" x2="950" y2="310" stroke="#2864a5" '
        'stroke-width="4" marker-end="url(#arrow)"/>',
        '<circle cx="650" cy="310" r="8" fill="#2864a5"/>',
        '<circle cx="950" cy="245" r="8" fill="#c45132"/>',
        '<line x1="950" y1="245" x2="950" y2="310" stroke="#c45132" '
        'stroke-width="2" stroke-dasharray="6 5"/>',
        _text(628, 338, "A", size=20, weight="bold"),
        _text(960, 245, "B", size=20, weight="bold"),
        _text(795, 294, "projection B⊥", size=15),
        _text(665, 375, "τ(A, B) = Δx / U (aval) ; +∞ (amont)", size=16),
        _text(580, 411, "Le décalage transversal n'est pas pénalisé dans ce cas jouet.", size=15),
        _text(580, 438, "Une cible en amont reçoit +∞ selon la convention retenue.", size=15),
        _text(
            32,
            487,
            "Schéma original, champ uniforme 2D ; pas une métrique au sens strict "
            "ni une reproduction quantitative.",
            size=13,
        ),
        '</svg>',
    ]
    return "\n".join(elements) + "\n"
