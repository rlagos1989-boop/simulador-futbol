import streamlit as st
import numpy as np
import pandas as pd

# Configuración inicial de la página web
st.set_page_config(
    page_title="Simulador Estadístico de Fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base de datos integrada de equipos por liga
BASE_DATOS = {
    "MLS (EE. UU.)": {
        "Inter Miami CF": {"gf": 2.20, "gc": 1.25, "gf1t": 1.10, "corners": 4.8},
        "LA Galaxy": {"gf": 1.90, "gc": 1.40, "gf1t": 0.80, "corners": 5.1},
        "Columbus Crew": {"gf": 1.95, "gc": 1.15, "gf1t": 0.95, "corners": 5.4}
    },
    "LaLiga (España)": {
        "Real Madrid": {"gf": 2.15, "gc": 0.80, "gf1t": 1.00, "corners": 5.8},
        "FC Barcelona": {"gf": 2.05, "gc": 0.95, "gf1t": 0.90, "corners": 6.2},
        "Atlético Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9}
    },
    "Serie A (Italia)": {
        "Inter Milan": {"gf": 1.90, "gc": 0.85, "gf1t": 0.95, "corners": 5.1},
        "AC Milan": {"gf": 1.70, "gc": 1.15, "gf1t": 0.75, "corners": 5.3},
        "SSC Napoli": {"gf": 1.75, "gc": 0.90, "gf1t": 0.80, "corners": 5.6}
    },
    "Bundesliga (Alemania)": {
        "Bayer Leverkusen": {"gf": 2.35, "gc": 0.90, "gf1t": 1.15, "corners": 6.4},
        "Bayern München": {"gf": 2.50, "gc": 1.05, "gf1t": 1.30, "corners": 6.7}
    },
    "Premier League (Inglaterra)": {
        "Manchester City": {"gf": 2.40, "gc": 0.85, "gf1t": 1.20, "corners": 7.1},
        "Arsenal FC": {"gf": 2.25, "gc": 0.75, "gf1t": 1.10, "corners": 6.6},
        "Chelsea FC": {"gf": 1.75, "gc": 1.30, "gf1t": 0.80, "corners": 5.4}
    },
    "Liga Nacional (Honduras)": {
        "CD Olimpia": {"gf": 2.05, "gc": 0.70, "gf1t": 0.95, "corners": 5.2},
        "FC Motagua": {"gf": 1.70, "gc": 0.95, "gf1t": 0.75, "corners": 4.8},
        "CD Marathon": {"gf": 1.50, "gc": 1.05, "gf1t": 0.60, "corners": 4.6}
    }
}

st.title("⚽ SIMULADOR PREDICTIVO MONTE CARLO")
st.markdown("Algoritmo con distribución de Poisson para proyecciones de 1T, Final y Córners.")

# Panel Lateral: Selección de Liga y Equipos
st.sidebar.header("⚙️ Configuración del Partido")

liga_sel = st.sidebar.selectbox("Seleccionar Liga:", list(BASE_DATOS.keys()))
equipos_liga = list(BASE_DATOS[liga_sel].keys())

col_inputs1, col_inputs2 = st.columns(2)

with col_inputs1:
    st.subheader("🏠 Equipo Local")
    eq_local = st.selectbox("Local:", equipos_liga, index=0)
    prio_loc = st.slider("Necesidad de Ganar (Local):", 1, 10, 8, key="p_loc")

with col_inputs2:
    st.subheader("✈️ Equipo Visitante")
    idx_vis = 1 if len(equipos_liga) > 1 else 0
    eq_visita = st.selectbox("Visitante:", equipos_liga, index=idx_vis)
    prio_vis = st.slider("Necesidad de Ganar (Visitante):", 1, 10, 7, key="p_vis")

ritmo_opt = st.select_slider(
    "🔥 Ritmo / Intensidad Esperada del Partido:",
    options=["Bajo (0.85x)", "Normal (1.00x)", "Alto (1.12x)", "Vertiginoso (1.25x)"],
    value="Alto (1.12x)"
)

# Factores de cálculo
f_ritmo = float(ritmo_opt.split("(")[1].replace("x)", ""))
f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

if st.button("🚀 CALCULAR PREDICCIÓN (10,000 SIMULACIONES)", use_container_width=True):
    data_loc = BASE_DATOS[liga_sel][eq_local]
    data_vis = BASE_DATOS[liga_sel][eq_visita]

    # Tasas Poisson ajustadas
    l_gf_loc = data_loc["gf"] * 1.10 * f_prio_loc * f_ritmo
    l_gf_vis = data_vis["gf"] * f_prio_vis * f_ritmo

    l_1t_loc = data_loc["gf1t"] * f_prio_loc * f_ritmo
    l_1t_vis = data_vis["gf1t"] * f_prio_vis * f_ritmo

    l_corners_tot = (data_loc["corners"] + data_vis["corners"]) * f_ritmo

    # Motor Monte Carlo (10,000 partidos)
    N = 10000
    goles_loc = np.random.poisson(l_gf_loc, N)
    goles_vis = np.random.poisson(l_gf_vis, N)

    goles_1t_loc = np.random.poisson(l_1t_loc, N)
    goles_1t_vis = np.random.poisson(l_1t_vis, N)

    corners_ft = np.random.poisson(l_corners_tot, N)
    corners_1t = np.random.poisson(l_corners_tot * 0.45, N)

    # Resultados
    p_win_loc = np.mean(goles_loc > goles_vis) * 100
    p_draw = np.mean(goles_loc == goles_vis) * 100
    p_win_vis = np.mean(goles_loc < goles_vis) * 100

    p_1t_05 = np.mean((goles_1t_loc + goles_1t_vis) > 0.5) * 100
    p_ft_25 = np.mean((goles_loc + goles_vis) > 2.5) * 100
    p_corn_95 = np.mean(corners_ft > 9.5) * 100
    p_corn_45_1t = np.mean(corners_1t > 4.5) * 100

    st.markdown("---")
    st.subheader("📊 Probabilidades 1X2 (Tiempo Completo)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Victoria Local", f"{p_win_loc:.1f}%")
    c2.metric("Empate", f"{p_draw:.1f}%")
    c3.metric("Victoria Visitante", f"{p_win_vis:.1f}%")

    st.subheader("🎯 Pronósticos Sugeridos y Líneas de Valor")
    st.write(f"⏱️ **Goles 1er Tiempo (> 0.5 1T):** **{p_1t_05:.1f}%** (Promedio esperable: {np.mean(goles_1t_loc + goles_1t_vis):.2f} goles)")
    st.write(f"⚽ **Goles Partido Completo (> 2.5 FT):** **{p_ft_25:.1f}%** (Promedio esperable: {np.mean(goles_loc + goles_vis):.2f} goles)")
    st.write(f"🚩 **Córners 1er Tiempo (> 4.5 1T):** **{p_corn_45_1t:.1f}%** (Promedio esperable: {np.mean(corners_1t):.1f} córners)")
    st.write(f"🚩 **Córners Totales (> 9.5 FT):** **{p_corn_95:.1f}%** (Promedio esperable: {np.mean(corners_ft):.1f} córners)")

