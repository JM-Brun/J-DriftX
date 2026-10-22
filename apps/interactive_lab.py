"""Local Streamlit app for exploring synthetic fields and terrain.

Run with: uv sync --group app && uv run streamlit run apps/interactive_lab.py
"""

from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jdriftx.fields import vector_field
from jdriftx.terrain import terrain_surface

st.set_page_config(
    page_title="J-DriftX — laboratoire interactif",
    page_icon="🌬️",
    layout="wide",
)
st.title("Laboratoire interactif J-DriftX")
st.caption(
    "Prototype pédagogique. Les champs et reliefs sont synthétiques : "
    "ils ne constituent ni une simulation météorologique ni une validation de J-DriftX."
)

field_tab, terrain_tab, about_tab = st.tabs(
    ["🌬️ Champs de vecteurs", "⛰️ Reliefs synthétiques", "🧭 Lire les résultats"]
)

with field_tab:
    with st.sidebar:
        st.header("Champ vectoriel")
        field_label = st.selectbox(
            "Famille de champ",
            ["Uniforme", "Cisaillement linéaire", "Radial (source / puits)"],
        )
        speed = st.slider("Vitesse de base", 0.1, 10.0, 2.0, 0.1)
        angle = st.slider("Direction (degrés)", -180, 180, 0, 5)
        shear = st.slider("Cisaillement (par unité de longueur)", -2.0, 2.0, 0.5, 0.1)
        radial_strength = st.slider("Intensité radiale", -2.0, 2.0, 1.0, 0.1)
        grid_size = st.slider("Résolution numérique", 9, 41, 21, 4)
        show_vectors = st.checkbox("Afficher les vecteurs", value=True)
        show_contours = st.checkbox("Afficher les contours de norme", value=False)

    kind_by_label = {
        "Uniforme": "uniform",
        "Cisaillement linéaire": "shear",
        "Radial (source / puits)": "radial",
    }
    kind = kind_by_label[field_label]
    coordinates = np.linspace(-5.0, 5.0, grid_size)
    x_grid, y_grid = np.meshgrid(coordinates, coordinates)
    u_grid, v_grid = vector_field(
        x_grid,
        y_grid,
        kind,  # type: ignore[arg-type]
        speed=speed,
        angle_deg=float(angle),
        shear=shear,
        radial_strength=radial_strength,
    )
    magnitude = np.hypot(u_grid, v_grid)
    dy = coordinates[1] - coordinates[0]
    dv_dy, dv_dx = np.gradient(v_grid, dy, dy)
    du_dy, du_dx = np.gradient(u_grid, dy, dy)
    divergence = du_dx + dv_dy
    vorticity = dv_dx - du_dy

    figure = go.Figure()
    figure.add_trace(
        go.Heatmap(
            x=coordinates,
            y=coordinates,
            z=magnitude,
            colorscale="Viridis",
            colorbar={"title": "||v||"},
            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>||v||=%{z:.3f}<extra></extra>",
            name="Norme",
        )
    )
    if show_contours:
        figure.add_trace(
            go.Contour(
                x=coordinates,
                y=coordinates,
                z=magnitude,
                showscale=False,
                contours={"coloring": "none", "showlabels": True},
                line={"color": "white", "width": 1},
                name="Contours de norme",
            )
        )
    if show_vectors:
        stride = max(1, math.ceil(grid_size / 13))
        max_component = max(float(np.max(np.abs(u_grid))), float(np.max(np.abs(v_grid))), 1e-9)
        arrow_scale = 0.35 * (10.0 / (grid_size - 1)) / max_component
        annotations = []
        for row in range(0, grid_size, stride):
            for col in range(0, grid_size, stride):
                u_arrow = float(u_grid[row, col]) * arrow_scale
                v_arrow = float(v_grid[row, col]) * arrow_scale
                if abs(u_arrow) + abs(v_arrow) < 1e-12:
                    continue
                annotations.append(
                    {
                        "x": float(x_grid[row, col]) + u_arrow,
                        "y": float(y_grid[row, col]) + v_arrow,
                        "ax": float(x_grid[row, col]),
                        "ay": float(y_grid[row, col]),
                        "xref": "x",
                        "yref": "y",
                        "axref": "x",
                        "ayref": "y",
                        "showarrow": True,
                        "arrowhead": 3,
                        "arrowsize": 1,
                        "arrowwidth": 1.3,
                        "arrowcolor": "white",
                    }
                )
        figure.update_layout(annotations=annotations)
    figure.update_layout(
        title="Champ vectoriel — couleur = norme",
        xaxis_title="x (unité arbitraire)",
        yaxis_title="y (unité arbitraire)",
        yaxis={"scaleanchor": "x", "scaleratio": 1},
        margin={"l": 10, "r": 10, "t": 55, "b": 10},
        height=620,
    )

    left, right = st.columns([3, 1])
    with left:
        st.plotly_chart(figure, use_container_width=True)
    with right:
        st.metric("Norme maximale", f"{float(magnitude.max()):.3f}")
        st.metric("Divergence max. |·|", f"{float(np.abs(divergence).max()):.3f}")
        st.metric("Rotationnel max. |·|", f"{float(np.abs(vorticity).max()):.3f}")
        st.caption(
            "Divergence et rotationnel sont estimés par différences finies sur la grille. "
            "Leur précision dépend de la résolution."
        )
    with st.expander("Équation et interprétation"):
        if kind == "uniform":
            st.latex(r"u(x,y)=U\cos(\theta),\qquad v(x,y)=U\sin(\theta)")
            st.write("Champ constant : divergence et rotationnel théoriques nuls.")
        elif kind == "shear":
            st.latex(r"u(x,y)=U\cos(\theta)+\gamma y,\qquad v(x,y)=U\sin(\theta)")
            st.write(
                "Cisaillement : la composante horizontale varie avec y. "
                "La divergence théorique est nulle ; le rotationnel dépend de gamma."
            )
        else:
            st.latex(r"u(x,y)=\alpha x,\qquad v(x,y)=\alpha y")
            st.write(
                "Champ radial : divergence théorique égale à 2alpha et rotationnel nul. "
                "alpha positif correspond à une source ; alpha négatif à un puits."
            )

with terrain_tab:
    st.subheader("Construire un relief synthétique")
    terrain_left, terrain_right = st.columns([1, 2])
    with terrain_left:
        terrain_label = st.selectbox(
            "Forme",
            ["Colline gaussienne", "Vallée gaussienne", "Crête", "Terrain plat"],
        )
        terrain_kind_by_label = {
            "Colline gaussienne": "hill",
            "Vallée gaussienne": "valley",
            "Crête": "ridge",
            "Terrain plat": "flat",
        }
        terrain_kind = terrain_kind_by_label[terrain_label]
        terrain_height = st.slider("Hauteur signée", 0.1, 5.0, 2.0, 0.1)
        terrain_width = st.slider("Largeur caractéristique", 0.3, 4.0, 1.5, 0.1)
        center_x = st.slider("Centre x", -3.0, 3.0, 0.0, 0.25)
        center_y = st.slider("Centre y", -3.0, 3.0, 0.0, 0.25)
        terrain_grid_size = st.slider("Résolution du relief", 15, 61, 31, 4, key="terrain_grid")
    terrain_coordinates = np.linspace(-5.0, 5.0, terrain_grid_size)
    terrain_x, terrain_y = np.meshgrid(terrain_coordinates, terrain_coordinates)
    elevation = terrain_surface(
        terrain_x,
        terrain_y,
        terrain_kind,  # type: ignore[arg-type]
        height=terrain_height,
        width=terrain_width,
        center_x=center_x,
        center_y=center_y,
    )
    dz_dy, dz_dx = np.gradient(
        elevation,
        terrain_coordinates[1] - terrain_coordinates[0],
        terrain_coordinates[1] - terrain_coordinates[0],
    )
    slope_magnitude = np.hypot(dz_dx, dz_dy)
    with terrain_right:
        terrain_figure = go.Figure(
            data=[
                go.Surface(
                    x=terrain_x,
                    y=terrain_y,
                    z=elevation,
                    colorscale="Earth",
                    colorbar={"title": "z*"},
                    contours={
                        "z": {
                            "show": True,
                            "usecolormap": True,
                            "project_z": True,
                        }
                    },
                    hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z*=%{z:.3f}<extra></extra>",
                )
            ]
        )
        terrain_figure.update_layout(
            title="Surface 3D et projection des contours",
            scene={
                "xaxis_title": "x*",
                "yaxis_title": "y*",
                "zaxis_title": "z* (hauteur relative)",
                "aspectratio": {"x": 1, "y": 1, "z": 0.55},
            },
            margin={"l": 0, "r": 0, "t": 50, "b": 0},
            height=600,
        )
        st.plotly_chart(terrain_figure, use_container_width=True)
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Altitude max. relative", f"{float(elevation.max()):.3f}")
    metric2.metric("Altitude min. relative", f"{float(elevation.min()):.3f}")
    metric3.metric("Pente max. estimée", f"{float(slope_magnitude.max()):.3f}")
    st.warning(
        "Ce relief est synthétique et sans unité physique. La pente est calculée "
        "numériquement. Aucun effet sur le vent ou la dispersion n'est simulé."
    )

with about_tab:
    st.subheader("Comment interpréter ces expériences")
    st.markdown(
        r"""
        - **Couleur** : norme du champ dans le premier onglet ; altitude relative dans le second.
        - **Flèches** : direction et sens locaux du champ. Leur longueur est mise à l'échelle
          pour rester lisible ; elle ne constitue donc pas une échelle quantitative directe.
        - **Divergence** : mesure locale du bilan de flux sortant dans un champ continu.
        - **Rotationnel 2D** : composante verticale du rotationnel, soit
          \\(\partial v/\partial x - \partial u/\partial y\\).
        - **Pente** : norme du gradient du relief synthétique, estimée par différences finies.
        """
    )
    st.info(
        "Les coordonnées sont sans dimension. Ces expériences illustrent des objets "
        "mathématiques ; elles ne sont pas des données météo, un solveur CFD ou une "
        "validation scientifique de J-DriftX."
    )
