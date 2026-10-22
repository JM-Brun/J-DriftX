"""Interactive convergence study for periodic 1D advection-diffusion.

Run with: uv sync --group app && uv run streamlit run apps/convergence_lab.py
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jdriftx.periodic_transport import (
    periodic_sine_solution,
    solve_periodic_sine_transport,
    solve_periodic_upwind_euler,
)

st.set_page_config(page_title="J-DriftX — convergence numérique", layout="wide")
st.title("Convergence numérique : advection-diffusion périodique")
st.warning(
    "Expérience de vérification numérique. Le cas périodique est synthétique et "
    "ne constitue pas une simulation de dispersion atmosphérique."
)

left, right = st.columns(2)
with left:
    n_cells = st.select_slider(
        "Nombre de cellules spatiales",
        options=[24, 32, 48, 64, 96, 128],
        value=64,
    )
    end_time = st.slider("Temps final", 0.1, 1.0, 0.4, 0.1)
    velocity = st.slider("Vitesse u", -1.0, 1.0, 0.4, 0.05)
with right:
    diffusivity = st.slider("Diffusivité K", 0.0, 0.05, 0.01, 0.005)
    mean_concentration = st.slider("Concentration moyenne", 0.5, 2.0, 1.0, 0.1)
    amplitude = st.slider("Amplitude initiale", 0.05, 0.5, 0.3, 0.05)

length = 1.0
dx = length / n_cells
limits = []
if abs(velocity) > 0:
    limits.append(0.5 * dx / abs(velocity))
if diffusivity > 0:
    limits.append(0.5 * dx**2 / diffusivity)
stability_dt = min(limits) if limits else 0.1
fraction = st.slider("Fraction du pas conservateur", 0.05, 0.8, 0.35, 0.05)
dt = stability_dt * fraction

try:
    x, numerical, actual_dt = solve_periodic_sine_transport(
        n_cells=n_cells,
        length=length,
        end_time=end_time,
        dt=dt,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
except ValueError as exc:
    st.error(f"Calcul non réalisé : {exc}")
    st.stop()

exact = periodic_sine_solution(
    x,
    end_time,
    length=length,
    mean_concentration=mean_concentration,
    amplitude=amplitude,
    velocity=velocity,
    diffusivity=diffusivity,
)
error = numerical - exact
l2_error = float(np.sqrt(np.mean(error**2)))
linf_error = float(np.max(np.abs(error)))
mass_numerical = float(np.sum(numerical) * dx)
mass_expected = mean_concentration * length

figure = go.Figure()
figure.add_trace(go.Scatter(x=x, y=exact, mode="lines", name="Solution analytique"))
figure.add_trace(go.Scatter(x=x, y=numerical, mode="markers", name="Différences centrées + RK4"))
x_upwind, upwind, _upwind_dt = solve_periodic_upwind_euler(
    n_cells=n_cells,
    length=length,
    end_time=end_time,
    dt=dt,
    mean_concentration=mean_concentration,
    amplitude=amplitude,
    velocity=velocity,
    diffusivity=diffusivity,
)
upwind_error = float(np.sqrt(np.mean((upwind - exact) ** 2)))
cross_method_error = float(np.sqrt(np.mean((numerical - upwind) ** 2)))
figure.add_trace(
    go.Scatter(x=x_upwind, y=upwind, mode="lines", name="Référence indépendante : Euler amont")
)
figure.update_layout(
    title="Solution numérique et référence analytique",
    xaxis_title="Position x / longueur du domaine",
    yaxis_title="Concentration (unité arbitraire)",
    height=460,
)
st.plotly_chart(figure, use_container_width=True)

metrics = st.columns(6)
metrics[0].metric("Erreur L2 RK4", f"{l2_error:.3e}")
metrics[1].metric("Erreur max RK4", f"{linf_error:.3e}")
metrics[2].metric("Erreur L2 Euler amont", f"{upwind_error:.3e}")
metrics[3].metric("Écart entre schémas", f"{cross_method_error:.3e}")
metrics[4].metric("Masse RK4", f"{mass_numerical:.8f}")
metrics[5].metric("Pas temporel effectif", f"{actual_dt:.3e}")
st.caption(
    f"Référence de masse : {mass_expected:.8f}. Les deux schémas conservent la moyenne "
    "périodique à l'arrondi près ; leur écart fournit un contrôle croisé indépendant. "
    "Le schéma Euler amont est d'ordre un et généralement plus diffusif."
)

st.divider()
st.header("1. Convergence spatiale")
st.markdown(
    "Le pas temporel est réduit comme le carré du pas spatial pour limiter son influence. "
    "L'erreur est comparée à la solution analytique au même instant. Le schéma centré "
    "et RK4 est d'ordre spatial deux pour ce cas régulier ; les résultats doivent confirmer "
    "cette tendance avant toute interprétation."
)

space_counts = [24, 32, 48, 64, 96, 128]
space_errors = []
space_steps = []
for count in space_counts:
    local_dx = length / count
    local_limits = []
    if abs(velocity) > 0:
        local_limits.append(local_dx / abs(velocity))
    if diffusivity > 0:
        local_limits.append(local_dx**2 / diffusivity)
    local_scale = min(local_limits) if local_limits else 0.1
    local_dt = 0.15 * local_scale
    local_x, local_c, _local_actual_dt = solve_periodic_sine_transport(
        n_cells=count,
        length=length,
        end_time=end_time,
        dt=local_dt,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    local_exact = periodic_sine_solution(
        local_x,
        end_time,
        length=length,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    space_errors.append(float(np.sqrt(np.mean((local_c - local_exact) ** 2))))
    space_steps.append(local_dx)

def _observed_order(steps: list[float], errors: list[float]) -> float | None:
    valid = [
        (step, error)
        for step, error in zip(steps, errors, strict=True)
        if np.isfinite(error) and error > np.finfo(float).eps
    ]
    if len(valid) < 2:
        return None
    valid_steps, valid_errors = zip(*valid, strict=True)
    return float(np.polyfit(np.log(valid_steps), np.log(valid_errors), 1)[0])


spatial_order = _observed_order(space_steps, space_errors)
spatial_order_label = f"{spatial_order:.2f}" if spatial_order is not None else "indisponible"
space_figure = go.Figure()
space_figure.add_trace(
    go.Scatter(x=space_steps, y=space_errors, mode="lines+markers", name="Erreur L2")
)
space_figure.update_layout(
    title=f"Erreur spatiale (pente observée : {spatial_order_label})",
    xaxis_title="Pas spatial Δx",
    yaxis_title="Erreur L2 discrète",
    xaxis_type="log",
    yaxis_type="log",
    height=420,
)
st.plotly_chart(space_figure, use_container_width=True)
st.caption(
    f"Pente ajustée sur ces résolutions : {spatial_order:.2f}. C'est un indicateur empirique "
    "sur cette plage de maillages, pas une preuve générale de l'ordre de convergence."
)

st.divider()
st.header("2. Convergence temporelle")
st.markdown(
    "Le maillage spatial est fixé. Les calculs sont comparés à une solution numérique "
    "de référence obtenue avec le même opérateur spatial et un pas temporel beaucoup plus "
    "petit. Cette comparaison isole mieux l'erreur temporelle que la comparaison à la "
    "solution exacte, qui contient aussi l'erreur spatiale."
)

time_counts = [1, 2, 4, 8]
time_steps = [stability_dt * 0.8 / count for count in time_counts]
reference_dt = max(time_steps[0] / 128.0, end_time / 50000.0)
_, temporal_reference, _ = solve_periodic_sine_transport(
    n_cells=n_cells,
    length=length,
    end_time=end_time,
    dt=reference_dt,
    mean_concentration=mean_concentration,
    amplitude=amplitude,
    velocity=velocity,
    diffusivity=diffusivity,
)
time_errors = []
time_actual_steps = []
for time_step in time_steps:
    _, temporal_solution, actual_time_step = solve_periodic_sine_transport(
        n_cells=n_cells,
        length=length,
        end_time=end_time,
        dt=time_step,
        mean_concentration=mean_concentration,
        amplitude=amplitude,
        velocity=velocity,
        diffusivity=diffusivity,
    )
    time_actual_steps.append(actual_time_step)
    time_errors.append(float(np.sqrt(np.mean((temporal_solution - temporal_reference) ** 2))))

time_order = _observed_order(time_actual_steps, time_errors)
time_order_label = f"{time_order:.2f}" if time_order is not None else "indisponible"
time_figure = go.Figure()
time_figure.add_trace(
    go.Scatter(
        x=time_actual_steps,
        y=time_errors,
        mode="lines+markers",
        name="Écart à la référence temporelle",
    )
)
time_figure.update_layout(
    title=f"Erreur temporelle (pente observée : {time_order_label})",
    xaxis_title="Pas temporel effectif Δt",
    yaxis_title="Erreur L2 par rapport à la référence",
    xaxis_type="log",
    yaxis_type="log",
    height=420,
)
st.plotly_chart(time_figure, use_container_width=True)
st.caption(
    f"Référence calculée avec dt demandé = {reference_dt:.3e}. Pente ajustée : {time_order_label}. "
    "Pente indicative, dépendant du régime d'erreur, de l'arrondi et de la précision "
    "de la référence."
)

with st.expander("Équation, solution exacte et limites"):
    st.latex(
        r"\frac{\partial c}{\partial t}"
        r"+u\frac{\partial c}{\partial x}"
        r"=K\frac{\partial^2 c}{\partial x^2}"
    )
    st.latex(
        r"c(x,t)=\bar c+A\,e^{-K(2\pi/L)^2t}"
        r"\sin\left(\frac{2\pi}{L}(x-ut)\right)"
    )
    st.markdown(
        """
        **Hypothèses :** domaine périodique de longueur L, vitesse constante, diffusivité
        constante, condition initiale sinusoïdale et coefficients sans dimension imposée.

        **Schéma numérique :** différences finies centrées en espace et Runge-Kutta classique
        d'ordre 4 en temps. Le code vérifie la stabilité linéaire du pas choisi pour
        l'opérateur discret.

        **Interprétation :** la convergence sur ce cas lisse teste une implémentation numérique
        et ses ordres observés. Elle ne teste ni des conditions aux limites réalistes, ni des
        sources ponctuelles, ni des coefficients variables, ni la physique de la dérive des
        gouttelettes. La solution analytique est une référence indépendante du solveur.
        """
    )
