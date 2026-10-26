"""Rendu HTML reproductible de l'explorateur de champs de vent 2D.

Le calcul des vitesses est délégué à :func:`jdriftx.fields.vector_field`.
Ce module ne connaît que la présentation SVG des résultats calculés : la page
Quarto fournit les paramètres et importe cette unique API dans Pyodide.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from html import escape

import numpy as np
from numpy.typing import NDArray

from jdriftx.fields import FieldKind, vector_field

_FAMILY_TO_KIND: dict[str, FieldKind] = {
    "Uniforme": "uniform",
    "Cisaillement linéaire": "shear",
    "Radial (source / puits)": "radial",
}
_GRID_COORDINATES = np.linspace(-5.0, 5.0, 11)
_SVG_WIDTH = 760
_SVG_HEIGHT = 520
_MARGIN_LEFT = 58
_MARGIN_RIGHT = 28
_MARGIN_TOP = 36
_MARGIN_BOTTOM = 72


@dataclass(frozen=True)
class WindFieldExplorerConfig:
    """Paramètres contrôlés de l'explorateur pédagogique de champ 2D.

    Les coordonnées sont réduites et les vitesses sont dans une unité arbitraire.
    Cette configuration ne représente ni une observation météorologique ni un
    couplage au relief.
    """

    family: str
    speed: float
    angle_deg: float
    shear: float
    radial_strength: float
    probe_x: float
    probe_y: float

    def __post_init__(self) -> None:
        """Refuse une famille inconnue ou des paramètres non finis."""
        if self.family not in _FAMILY_TO_KIND:
            msg = f"Famille de champ inconnue : {self.family!r}."
            raise ValueError(msg)
        values = (
            self.speed,
            self.angle_deg,
            self.shear,
            self.radial_strength,
            self.probe_x,
            self.probe_y,
        )
        if not all(math.isfinite(value) for value in values):
            msg = "Les paramètres de l'explorateur doivent être finis."
            raise ValueError(msg)

    @property
    def kind(self) -> FieldKind:
        """Retourne le type fermé attendu par ``vector_field``."""
        return _FAMILY_TO_KIND[self.family]


def _attrs(**values: float | int | str) -> str:
    """Sérialise des attributs SVG/HTML en échappant leurs valeurs."""
    return " ".join(
        f"{('class' if name == 'class_' else name.replace('_', '-'))}="
        f'"{escape(str(value), quote=True)}"'
        for name, value in values.items()
    )


def _colour(norm: float, maximum: float) -> str:
    """Retourne une couleur dépendant de la norme relative du vecteur."""
    ratio = min(1.0, norm / maximum)
    return f"hsl({220.0 - 190.0 * ratio:.1f} 75% {32.0 + 24.0 * ratio:.1f}%)"


def _void_element(tag: str, **values: float | int | str) -> str:
    """Retourne un élément SVG sans contenu."""
    return f"<{tag} {_attrs(**values)}/>"


def _text_element(value: str, **attributes: float | int | str) -> str:
    """Retourne un élément texte SVG dont le contenu est échappé."""
    return f"<text {_attrs(**attributes)}>{escape(value)}</text>"


def _to_x(value: float) -> float:
    """Projette une abscisse réduite sur le canevas SVG."""
    plot_width = _SVG_WIDTH - _MARGIN_LEFT - _MARGIN_RIGHT
    return _MARGIN_LEFT + (value + 5.0) * plot_width / 10.0


def _to_y(value: float) -> float:
    """Projette une ordonnée réduite sur le canevas SVG, axe vers le haut."""
    plot_height = _SVG_HEIGHT - _MARGIN_TOP - _MARGIN_BOTTOM
    return _SVG_HEIGHT - _MARGIN_BOTTOM - (value + 5.0) * plot_height / 10.0


def _render_svg(
    config: WindFieldExplorerConfig,
    u_grid: NDArray[np.float64],
    v_grid: NDArray[np.float64],
    magnitude: NDArray[np.float64],
) -> str:
    """Rend les vecteurs évalués par le noyau Python dans un SVG accessible."""
    maximum = max(float(np.max(magnitude)), 1e-9)
    plot_width = _SVG_WIDTH - _MARGIN_LEFT - _MARGIN_RIGHT
    plot_height = _SVG_HEIGHT - _MARGIN_TOP - _MARGIN_BOTTOM
    parts = [
        "<svg "
        + _attrs(
            viewBox=f"0 0 {_SVG_WIDTH} {_SVG_HEIGHT}",
            class_="vector-field-svg",
            role="img",
            aria_label=f"Champ vectoriel 2D {config.family}, calculé par Python",
        )
        + ">",
        f"<title>Champ vectoriel 2D : {escape(config.family)}</title>",
    ]
    for tick in range(-4, 5, 2):
        parts.append(
            _void_element(
                "line",
                x1=_to_x(tick),
                y1=_to_y(-5),
                x2=_to_x(tick),
                y2=_to_y(5),
                stroke="#d9e2ec",
                stroke_width=1,
            )
        )
        parts.append(
            _void_element(
                "line",
                x1=_to_x(-5),
                y1=_to_y(tick),
                x2=_to_x(5),
                y2=_to_y(tick),
                stroke="#d9e2ec",
                stroke_width=1,
            )
        )
    parts.extend(
        [
            _void_element(
                "rect",
                x=_to_x(-5),
                y=_to_y(5),
                width=plot_width,
                height=plot_height,
                fill="none",
                stroke="#8fa3b5",
                stroke_width=1.25,
            ),
            _void_element(
                "line",
                x1=_to_x(-5),
                y1=_to_y(0),
                x2=_to_x(5),
                y2=_to_y(0),
                stroke="#60788a",
                stroke_width=1.4,
            ),
            _void_element(
                "line",
                x1=_to_x(0),
                y1=_to_y(-5),
                x2=_to_x(0),
                y2=_to_y(5),
                stroke="#60788a",
                stroke_width=1.4,
            ),
        ]
    )
    for row, y_value in enumerate(_GRID_COORDINATES):
        for column, x_value in enumerate(_GRID_COORDINATES):
            u_value = float(u_grid[row, column])
            v_value = float(v_grid[row, column])
            norm = float(magnitude[row, column])
            ratio = norm / maximum
            start_x, start_y = _to_x(float(x_value)), _to_y(float(y_value))
            colour = _colour(norm, maximum)
            parts.append(
                _void_element(
                    "circle",
                    cx=start_x,
                    cy=start_y,
                    r=3.5 + 1.8 * ratio,
                    fill=colour,
                    opacity=0.26,
                )
            )
            if norm < 1e-10:
                continue
            length = 10.0 + 19.0 * ratio
            end_x = start_x + u_value / norm * length
            end_y = start_y - v_value / norm * length
            unit_x = (end_x - start_x) / length
            unit_y = (end_y - start_y) / length
            perpendicular_x, perpendicular_y = -unit_y, unit_x
            head_left_x = end_x - 6 * unit_x + 4 * perpendicular_x
            head_left_y = end_y - 6 * unit_y + 4 * perpendicular_y
            head_right_x = end_x - 6 * unit_x - 4 * perpendicular_x
            head_right_y = end_y - 6 * unit_y - 4 * perpendicular_y
            points = " ".join(
                (
                    f"{end_x},{end_y}",
                    f"{head_left_x},{head_left_y}",
                    f"{head_right_x},{head_right_y}",
                )
            )
            parts.append(
                _void_element(
                    "line",
                    x1=start_x,
                    y1=start_y,
                    x2=end_x,
                    y2=end_y,
                    stroke=colour,
                    stroke_width=1.8,
                    stroke_linecap="round",
                )
            )
            parts.append(_void_element("polygon", points=points, fill=colour))
    probe_x, probe_y = _to_x(config.probe_x), _to_y(config.probe_y)
    parts.extend(
        [
            _void_element(
                "circle",
                cx=probe_x,
                cy=probe_y,
                r=7,
                fill="#ffffff",
                fill_opacity=0.92,
                stroke="#111827",
                stroke_width=2,
            ),
            _void_element(
                "line",
                x1=probe_x - 10,
                y1=probe_y,
                x2=probe_x + 10,
                y2=probe_y,
                stroke="#111827",
                stroke_width=1.5,
            ),
            _void_element(
                "line",
                x1=probe_x,
                y1=probe_y - 10,
                x2=probe_x,
                y2=probe_y + 10,
                stroke="#111827",
                stroke_width=1.5,
            ),
        ]
    )
    for tick in (-5, 0, 5):
        parts.append(
            _text_element(
                str(tick),
                x=_to_x(tick),
                y=_SVG_HEIGHT - 48,
                text_anchor="middle",
                fill="#334e68",
                font_size=13,
            )
        )
        parts.append(
            _text_element(
                str(tick),
                x=42,
                y=_to_y(tick) + 4,
                text_anchor="end",
                fill="#334e68",
                font_size=13,
            )
        )
    parts.extend(
        [
            _text_element(
                "x — position réduite",
                x=_MARGIN_LEFT + plot_width / 2,
                y=_SVG_HEIGHT - 18,
                text_anchor="middle",
                fill="#334e68",
                font_size=13,
                font_weight=600,
            ),
            _text_element(
                "y — position réduite",
                x=16,
                y=_MARGIN_TOP + plot_height / 2,
                transform=f"rotate(-90 16 {_MARGIN_TOP + plot_height / 2})",
                text_anchor="middle",
                fill="#334e68",
                font_size=13,
                font_weight=600,
            ),
        ]
    )
    legend_x, legend_y = _SVG_WIDTH - 222, 16
    for index in range(7):
        parts.append(
            _void_element(
                "rect",
                x=legend_x + index * 18,
                y=legend_y,
                width=18,
                height=9,
                fill=_colour(index / 6 * maximum, maximum),
            )
        )
    parts.extend(
        [
            _text_element(
                "couleur = norme relative",
                x=legend_x,
                y=legend_y - 4,
                fill="#334e68",
                font_size=11,
            ),
            _text_element("0", x=legend_x, y=legend_y + 22, fill="#334e68", font_size=10),
            _text_element(
                f"{maximum:.2f}",
                x=legend_x + 126,
                y=legend_y + 22,
                text_anchor="end",
                fill="#334e68",
                font_size=10,
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def render_wind_field_explorer_html(config: WindFieldExplorerConfig) -> str:
    """Calcule puis rend l'explorateur de champ vectoriel 2D en HTML/SVG.

    La fonction est l'unique entrée de présentation pour Quarto Live. Elle
    appelle ``vector_field`` sur une grille et au point de lecture, puis estime
    divergence et rotationnel par différences finies pour l'affichage.
    """
    x_grid, y_grid = np.meshgrid(_GRID_COORDINATES, _GRID_COORDINATES)
    u_grid, v_grid = vector_field(
        x_grid,
        y_grid,
        config.kind,
        speed=config.speed,
        angle_deg=config.angle_deg,
        shear=config.shear,
        radial_strength=config.radial_strength,
    )
    magnitude = np.hypot(u_grid, v_grid)
    spacing = float(_GRID_COORDINATES[1] - _GRID_COORDINATES[0])
    dv_dy, dv_dx = np.gradient(v_grid, spacing, spacing)
    du_dy, du_dx = np.gradient(u_grid, spacing, spacing)
    divergence = du_dx + dv_dy
    vorticity = dv_dx - du_dy
    probe_u, probe_v = vector_field(
        np.asarray([[config.probe_x]]),
        np.asarray([[config.probe_y]]),
        config.kind,
        speed=config.speed,
        angle_deg=config.angle_deg,
        shear=config.shear,
        radial_strength=config.radial_strength,
    )
    local_u = float(probe_u[0, 0])
    local_v = float(probe_v[0, 0])
    descriptions = {
        "uniform": "Les mêmes vecteurs sont reproduits partout.",
        "shear": "La composante horizontale varie linéairement avec y.",
        "radial": (
            "Les vecteurs divergent de l'origine pour une intensité positive "
            "et y convergent pour une intensité négative."
        ),
    }
    cards = (
        "<div><span>Point lu</span><strong>"
        f"({config.probe_x:.2f}, {config.probe_y:.2f})</strong></div>"
        "<div><span>Vecteur local</span><strong>"
        f"({local_u:.2f}, {local_v:.2f})</strong></div>"
        "<div><span>Norme locale</span><strong>"
        f"{math.hypot(local_u, local_v):.2f}</strong></div>"
        "<div><span>Divergence moyenne estimée</span><strong>"
        f"{float(np.mean(divergence)):.2f}</strong></div>"
        "<div><span>Rotationnel moyen estimé</span><strong>"
        f"{float(np.mean(vorticity)):.2f}</strong></div>"
    )
    style = """
<style>
.field-readout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: .7rem;
  margin: 1rem 0;
}
.field-readout > div {
  padding: .75rem;
  border: 1px solid #d8e2ea;
  border-radius: .45rem;
  background: #fff;
}
.field-readout strong { display: block; color: #174a6b; font-size: 1.1rem; }
.vector-field-svg {
  width: 100%;
  height: auto;
  border: 1px solid #d8e2ea;
  border-radius: .5rem;
  background: #fff;
}
</style>
"""
    return (
        style
        + _render_svg(config, u_grid, v_grid, magnitude)
        + f'<div class="field-readout">{cards}</div>'
        + "<p><strong>Lecture du cas courant.</strong> "
        + descriptions[config.kind]
        + " Les diagnostics sont estimés sur la grille par NumPy.</p>"
    )


@dataclass(frozen=True)
class WindFieldScenario:
    """Cas pédagogique pré-calculé à partir du noyau Python partagé."""

    title: str
    summary: str
    config: WindFieldExplorerConfig


def default_wind_field_scenarios() -> tuple[WindFieldScenario, ...]:
    """Retourne des expériences contrôlées pour l'exploration statique du site.

    Chaque figure est calculée durant le rendu Quarto par ``vector_field``. Le
    navigateur n'exécute ensuite aucune approximation ou équation du modèle.
    """
    return (
        WindFieldScenario(
            title="Référence uniforme",
            summary="Même vecteur en tout point : base de comparaison.",
            config=WindFieldExplorerConfig(
                family="Uniforme",
                speed=2.0,
                angle_deg=0.0,
                shear=0.0,
                radial_strength=0.0,
                probe_x=2.0,
                probe_y=1.0,
            ),
        ),
        WindFieldScenario(
            title="Cisaillement linéaire",
            summary="La vitesse horizontale varie avec la position verticale.",
            config=WindFieldExplorerConfig(
                family="Cisaillement linéaire",
                speed=2.0,
                angle_deg=0.0,
                shear=0.35,
                radial_strength=0.0,
                probe_x=2.0,
                probe_y=1.0,
            ),
        ),
        WindFieldScenario(
            title="Source radiale",
            summary="Cas contrôlé où les vecteurs divergent depuis l'origine.",
            config=WindFieldExplorerConfig(
                family="Radial (source / puits)",
                speed=0.0,
                angle_deg=0.0,
                shear=0.0,
                radial_strength=0.35,
                probe_x=2.0,
                probe_y=1.0,
            ),
        ),
        WindFieldScenario(
            title="Puits radial",
            summary="Même loi avec signe opposé : les vecteurs convergent.",
            config=WindFieldExplorerConfig(
                family="Radial (source / puits)",
                speed=0.0,
                angle_deg=0.0,
                shear=0.0,
                radial_strength=-0.35,
                probe_x=2.0,
                probe_y=1.0,
            ),
        ),
    )


def render_wind_field_scenario_gallery_html(
    scenarios: tuple[WindFieldScenario, ...],
) -> str:
    """Rend une galerie HTML native de scénarios calculés lors du build.

    ``details`` fournit une interaction sans moteur Python côté navigateur :
    l'utilisateur ouvre le cas qui l'intéresse, alors que les cartes SVG ont
    déjà été produites par l'API Python du projet.
    """
    if not scenarios:
        msg = "Au moins un scénario de champ de vent est requis."
        raise ValueError(msg)
    panels = []
    for index, scenario in enumerate(scenarios):
        open_attribute = " open" if index == 0 else ""
        panels.append(
            '<details class="wind-field-scenario"'
            + open_attribute
            + "><summary><strong>"
            + escape(scenario.title)
            + "</strong><span>"
            + escape(scenario.summary)
            + "</span></summary>"
            + render_wind_field_explorer_html(scenario.config)
            + "</details>"
        )
    style = """
<style>
.wind-field-gallery { margin: 1.25rem 0; }
.wind-field-scenario {
  border: 1px solid #cbd8e1;
  border-radius: .55rem;
  margin: .75rem 0;
  overflow: hidden;
}
.wind-field-scenario > summary {
  cursor: pointer;
  padding: .8rem 1rem;
  background: #f5f8fa;
}
.wind-field-scenario > summary span {
  display: block;
  color: #486581;
  margin-top: .2rem;
}
.wind-field-scenario > :not(summary) { margin-left: 1rem; margin-right: 1rem; }
</style>
"""
    gallery = '<section class="wind-field-gallery" aria-label="Scénarios de champ de vent">'
    return style + gallery + "".join(panels) + "</section>" + "</section>"
