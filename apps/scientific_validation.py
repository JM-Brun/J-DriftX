"""Scientific validation experiments: trajectories and analytic transport cases.

Run with: uv sync --group app && uv run streamlit run apps/scientific_validation.py
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jdriftx.advection_diffusion import gaussian_advection_diffusion
from jdriftx.trajectories import integrate_trajectory

st.set_page_config(page_title="J-DriftX — expériences de validation", layout="wide")
st.title("Expériences numériques et références analytiques")
st.warning(
    "Cas mathématiques de vérification du code. Ils ne constituent pas une validation "
    "physique, une simulation météorologique ou une prédiction de dispersion réelle."
)

trajectory_tab, transport_tab, validation_tab = st.tabs(
    ["Trajectoires", "Advection-diffusion 1D", "Erreur et limites"]
)

with trajectory_tab:
    st.subheader("Comparer Euler explicite et Runge-Kutta d'ordre 4")
    col1, col2 = st.columns(2)
    with col1:
        dt = st.select_slider("Pas de temps", options=[0.4, 0.2, 0.1, 0.05, 0.025], value=0.1)
        end_time = st.slider("Durée d'intégration", 1.0, 12.0, 6.0, 0.5)
    with col2:
        st.latex(r"\frac{dx}{dt}=-y,\qquad \frac{dy}{dt}=x")
        st.markdown(
            "Le champ de rotation est stationnaire. Pour la condition initiale "
            r"$(x(0),y(0))=(1,0)$, la solution exacte est $(\cos t,\sin t)$."
        )

    def _rotational_velocity(_t: float, x: float, y: float) -> tuple[float, float]:
        return (-y, x)

    times = np.linspace(0.0, end_time, 600)
    figure = go.Figure()
    exact_x, exact_y = np.cos(times), np.sin(times)
    figure.add_trace(go.Scatter(x=exact_x, y=exact_y, mode="lines", name="Solution exacte"))
    errors = {}
    for method in ("euler", "rk4"):
        _times, x_num, y_num = integrate_trajectory(
            _rotational_velocity, 1.0, 0.0, 0.0, end_time, dt, method
        )
        figure.add_trace(go.Scatter(x=x_num, y=y_num, mode="lines+markers", name=method.upper()))
        errors[method] = float(np.hypot(x_num[-1] - np.cos(end_time), y_num[-1] - np.sin(end_time)))
    figure.update_layout(
        title="Trajectoire dans le plan de phase",
        xaxis_title="x (unité arbitraire)",
        yaxis_title="y (unité arbitraire)",
        yaxis={"scaleanchor": "x", "scaleratio": 1},
        height=500,
    )
    st.plotly_chart(figure, use_container_width=True)
    m1, m2 = st.columns(2)
    m1.metric("Erreur finale Euler", f"{errors['euler']:.3e}")
    m2.metric("Erreur finale RK4", f"{errors['rk4']:.3e}")
    convergence = go.Figure()
    step_sizes = [end_time / count for count in (15, 30, 60, 120, 240)]
    for convergence_method in ("euler", "rk4"):
        errors_by_step = []
        for step_size in step_sizes:
            _t, x_path, y_path = integrate_trajectory(
                _rotational_velocity,
                1.0,
                0.0,
                0.0,
                end_time,
                step_size,
                convergence_method,
            )
            errors_by_step.append(
                np.hypot(
                    x_path[-1] - np.cos(end_time),
                    y_path[-1] - np.sin(end_time),
                )
            )
        convergence.add_trace(
            go.Scatter(
                x=step_sizes,
                y=errors_by_step,
                mode="lines+markers",
                name=convergence_method.upper(),
            )
        )
    convergence.update_layout(
        title="Erreur finale en fonction du pas de temps",
        xaxis_title="Pas de temps Δt",
        yaxis_title="Erreur euclidienne finale",
        xaxis_type="log",
        yaxis_type="log",
        height=420,
    )
    st.plotly_chart(convergence, use_container_width=True)
    st.caption(
        "La pente de cette courbe en échelle log-log permet d'observer l'ordre de convergence "
        "dans ce cas régulier ; elle ne garantit pas le même comportement pour tout problème."
    )
    st.caption(
        "L'erreur dépend du pas et de la durée. Une méthode d'ordre supérieur n'est pas "
        "automatiquement meilleure pour tout problème : stabilité, régularité et coût "
        "comptent aussi."
    )

with transport_tab:
    st.subheader("Solution gaussienne de l'équation advection-diffusion")
    st.latex(
        r"\frac{\partial c}{\partial t}+u\frac{\partial c}{\partial x}"
        r"=K\frac{\partial^2 c}{\partial x^2}"
    )
    left, right = st.columns(2)
    with left:
        mass = st.slider("Masse intégrée M", 0.1, 5.0, 1.0, 0.1)
        speed = st.slider("Vitesse constante u", -3.0, 3.0, 1.0, 0.1)
        diffusivity = st.slider("Diffusivité K", 0.0, 1.0, 0.2, 0.02)
    with right:
        sigma0 = st.slider("Écart-type initial σ₀", 0.1, 2.0, 0.5, 0.1)
        time = st.slider("Temps t", 0.0, 5.0, 2.0, 0.1)
        center0 = st.slider("Centre initial x₀", -3.0, 3.0, 0.0, 0.25)
    x = np.linspace(-10.0, 10.0, 4001)
    concentration = gaussian_advection_diffusion(
        x,
        time,
        mass=mass,
        initial_center=center0,
        velocity=speed,
        diffusivity=diffusivity,
        initial_sigma=sigma0,
    )
    initial = gaussian_advection_diffusion(
        x,
        0.0,
        mass=mass,
        initial_center=center0,
        velocity=speed,
        diffusivity=diffusivity,
        initial_sigma=sigma0,
    )
    profile = go.Figure()
    profile.add_trace(go.Scatter(x=x, y=initial, mode="lines", name="Initial"))
    profile.add_trace(go.Scatter(x=x, y=concentration, mode="lines", name="À l'instant t"))
    profile.update_layout(
        title="Translation et élargissement du profil",
        xaxis_title="Position x (unité cohérente)",
        yaxis_title="Concentration c (masse / unité de longueur)",
        height=480,
    )
    st.plotly_chart(profile, use_container_width=True)
    numerical_mass = float(np.trapezoid(concentration, x))
    theoretical_variance = sigma0**2 + 2.0 * diffusivity * time
    st.metric("Masse intégrée sur [-10, 10]", f"{numerical_mass:.6f} / {mass:.6f}")
    st.caption(
        f"Variance théorique : σ²(t) = σ₀² + 2Kt = {theoretical_variance:.4f}. "
        "La masse intégrée sur un domaine fini peut être légèrement inférieure à M si "
        "les queues de la gaussienne sortent du domaine."
    )

with validation_tab:
    st.subheader("Ce qui est vérifié — et ce qui ne l'est pas")
    st.markdown(
        """
        **Tests automatisés du noyau**
        - Champ de vitesse constant : la trajectoire est intégrée exactement, à l'arrondi près.
        - Champ rotationnel : comparaison de l'erreur d'Euler et de RK4 à la solution
          analytique.
        - Advection-diffusion : cas sans diffusion, conservation de la masse sur un domaine
          assez large, et croissance de variance conforme à la formule théorique.
        - Paramètres invalides : valeurs non finies, pas nul/négatif et diffusivité négative
          rejetés.

        **Limites importantes**
        - Les coordonnées et paramètres sont illustratifs ; aucune unité physique n'est imposée.
        - Le champ rotationnel est un problème ODE de vérification, pas un champ de vent.
        - La solution advection-diffusion suppose un domaine infini, une vitesse et une
          diffusivité constantes, sans réaction, dépôt, source continue ni conditions aux limites.
        - L'intégration numérique d'une trajectoire ne valide pas la fidélité du modèle physique.
        - Aucun couplage avec le relief, la turbulence ou la dynamique des
          particules n'est implémenté.
        """
    )
