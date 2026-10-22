"""Local Streamlit app for exploring synthetic 2D vector fields.

Run with: uv sync --group app && uv run streamlit run apps/interactive_lab.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from jdriftx.fields import vector_field

st.set_page_config(page_title="J-DriftX — laboratoire interactif", layout="wide")
st.title("Laboratoire interactif J-DriftX")
st.caption(
    "Prototype pédagogique : les champs affichés sont synthétiques et ne constituent "
    "pas une simulation météorologique ni une validation du modèle J-DriftX."
)

with st.sidebar:
    st.header("Paramètres")
    field_label = st.selectbox(
        "Champ mathématique",
        ["Uniforme", "Cisaillement linéaire", "Radial (source / puits)"],
    )
    speed = st.slider("Vitesse de base", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    angle = st.slider("Direction du champ (degrés)", -180, 180, 0, 5)
    shear = st.slider("Cisaillement (par unité de longueur)", -2.0, 2.0, 0.5, 0.1)
    radial_strength = st.slider("Intensité radiale", -2.0, 2.0, 1.0, 0.1)
    grid_size = st.slider("Résolution de la grille", 9, 41, 21, 4)

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

left, right = st.columns([3, 2])
with left:
    figure, axis = plt.subplots(figsize=(8, 6))
    stream = axis.streamplot(
        x_grid,
        y_grid,
        u_grid,
        v_grid,
        color=magnitude,
        cmap="viridis",
        density=1.0,
    )
    axis.quiver(x_grid, y_grid, u_grid, v_grid, color="black", alpha=0.45, scale=60)
    axis.set_xlabel("x (unité arbitraire)")
    axis.set_ylabel("y (unité arbitraire)")
    axis.set_title("Champ vectoriel et lignes de courant")
    axis.set_aspect("equal")
    figure.colorbar(stream.lines, ax=axis, label="Norme du vecteur (unité arbitraire)")
    st.pyplot(figure)
    plt.close(figure)

with right:
    st.subheader("Lecture du résultat")
    st.write(f"**Champ choisi :** {field_label}")
    st.write(f"**Norme maximale sur la grille :** {float(magnitude.max()):.3f}")
    st.write(
        "Les lignes de courant sont tangentes au champ vectoriel représenté. "
        "Elles ne sont pas automatiquement des trajectoires temporelles si le champ "
        "dépend du temps."
    )
    st.write(
        "La résolution change l'échantillonnage et l'apparence de la figure, pas la "
        "définition mathématique du champ."
    )

    if kind == "uniform":
        st.latex(r"u(x,y)=U\cos(\theta),\quad v(x,y)=U\sin(\theta)")
        st.write("Champ constant : direction et norme identiques en tout point.")
    elif kind == "shear":
        st.latex(r"u(x,y)=U\cos(\theta)+\gamma y,\quad v(x,y)=U\sin(\theta)")
        st.write("Cisaillement synthétique : la composante horizontale varie avec y.")
    else:
        st.latex(r"u(x,y)=\alpha x,\quad v(x,y)=\alpha y")
        st.write(
            "Champ radial : alpha positif diverge du centre ; alpha négatif converge "
            "vers le centre. Il s'agit d'un exemple mathématique, pas d'un écoulement "
            "atmosphérique modélisé."
        )

st.info(
    "Limites : coordonnées sans unité physique, domaine fini, champs stationnaires "
    "et synthétiques. Aucune donnée météo, topographique ou de concentration n'est utilisée."
)
