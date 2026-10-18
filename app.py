import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from mplsoccer import Pitch

st.set_page_config(page_title="Simulador Monte Carlo Predictivo Ultra Pro 2026/2027", layout="wide")

ARCH_HISTORIAL = "registro_pronosticos.csv"

# ==============================================================================
# 1. BASE DE DATOS Y FEEDS AUTOMÁTICOS
# ==============================================================================
LIGAS_AUTO = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/E0.csv",
    "🇪🇸 LaLiga Española (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/SP1.csv",
    "🇮🇹 Serie A (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/I1.csv",
    "🇩🇪 Bundesliga (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/D1.csv",
    "🇫🇷 Ligue 1 (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/F1.csv"
}

# Botón para limpiar caché
if st.button("🔄 Limpiar Caché y Actualizar Datos"):
    st.cache_data.clear()
    st.success("¡Caché limpiada correctamente! Recargando datos...")
    st.rerun()

LIGAS_ESTATICAS = {
    "🇲🇽 Liga MX (2026/27)": {
        "Club America": {"pj": 10, "gf": 1.67, "gc": 0.33, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.1, "remates_arco": 5.6},
        "Club Tijuana": {"pj": 10, "gf": 1.33, "gc": 0.33, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.5, "remates_arco": 3.8},
        "Toluca": {"pj": 10, "gf": 2.00, "gc": 1.00, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.1, "remates_arco": 5.7},
        "UNAM Pumas": {"pj": 10, "gf": 2.33, "gc": 1.67, "gf1t": 1.00, "corners": 5.3, "tarjetas": 2.4, "remates_arco": 4.6},
        "Monterrey": {"pj": 10, "gf": 2.00, "gc": 1.33, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.2, "remates_arco": 5.8},
        "Cruz Azul": {"pj": 10, "gf": 2.33, "gc": 2.00, "gf1t": 1.10, "corners": 5.9, "tarjetas": 2.0, "remates_arco": 5.3},
        "Queretaro": {"pj": 10, "gf": 1.67, "gc": 1.33, "gf1t": 0.70, "corners": 4.2, "tarjetas": 2.5, "remates_arco": 3.5},
        "Necaxa": {"pj": 10, "gf": 1.67, "gc": 1.67, "gf1t": 0.70, "corners": 4.4, "tarjetas": 2.5, "remates_arco": 3.9},
        "Atlas": {"pj": 10, "gf": 1.33, "gc": 1.33, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.7, "remates_arco": 4.0},
        "Guadalajara Chivas": {"pj": 10, "gf": 0.67, "gc": 1.00, "gf1t": 0.30, "corners": 5.2, "tarjetas": 2.4, "remates_arco": 4.9},
        "Pachuca": {"pj": 10, "gf": 1.33, "gc": 1.00, "gf1t": 0.60, "corners": 5.5, "tarjetas": 2.2, "remates_arco": 4.5},
        "Tigres UANL": {"pj": 10, "gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3, "remates_arco": 5.4}
    },
    "🇭🇳 Liga Nacional (Honduras 2026/27)": {
        "Real Espana": {"pj": 10, "gf": 2.50, "gc": 0.00, "gf1t": 1.00, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 5.0},
        "Olimpia": {"pj": 10, "gf": 2.50, "gc": 0.50, "gf1t": 1.10, "corners": 5.8, "tarjetas": 2.4, "remates_arco": 5.8},
        "Marathon": {"pj": 10, "gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.7, "remates_arco": 4.4},
        "Motagua": {"pj": 10, "gf": 1.50, "gc": 1.00, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.6, "remates_arco": 5.1},
        "CD Victoria": {"pj": 10, "gf": 1.25, "gc": 1.45, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.7, "remates_arco": 3.7},
        "Real Sociedad": {"pj": 10, "gf": 1.05, "gc": 1.60, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.6, "remates_arco": 3.3}
    }
}

@st.cache_data(ttl=21600)
def obtener_promedios_torneo(nombre_torneo):
    if nombre_torneo in LIGAS_ESTATICAS:
        return LIGAS_ESTATICAS[nombre_torneo]

    url = LIGAS_AUTO.get(nombre_torneo)
    if not url:
        return {}

    try:
        df = pd.read_csv(url)
        df = df.dropna(subset=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'])
        equipos = sorted(list(set(df['HomeTeam'].unique()).union(set(df['AwayTeam'].unique()))))
        stats = {}

        for eq in equipos:
            home = df[df['HomeTeam'] == eq]
            away = df[df['AwayTeam'] == eq]
            pj = len(home) + len(away)
            if pj == 0:
                continue

            gf = home['FTHG'].sum() + away['FTAG'].sum()
            gc = home['FTAG'].sum() + away['FTHG'].sum()
            gf1t = (home['HTHG'].sum() if 'HTHG' in home else 0) + (away['HTAG'].sum() if 'HTAG' in away else 0)
            corners = (home['HC'].sum() if 'HC' in home else 0) + (away['AC'].sum() if 'AC' in away else 0)
            tarjetas = (home['HY'].sum() + away['AY'].sum()) if ('HY' in home and 'AY' in home) else 20
            remates = (home['HST'].sum() if 'HST' in home else gf * 2.3) + (away['AST'].sum() if 'AST' in away else gf * 2.3)

            stats[eq] = {
                "pj": pj,
                "gf": round(gf / pj, 2),
                "gc": round(gc / pj, 2),
                "gf1t": round(gf1t / pj, 2),
                "corners": round(corners / pj, 2),
                "tarjetas": round(tarjetas / pj, 2),
                "remates_arco": round(remates / pj, 2)
            }
        return stats
    except Exception:
        return {}

# ==============================================================================
# 2. PERSISTENCIA Y HISTORIAL
# ==============================================================================
def cargar_historial():
    if os.path.exists(ARCH_HISTORIAL):
        return pd.read_csv(ARCH_HISTORIAL)
    return pd.DataFrame(columns=["ID", "Fecha", "Liga", "Partido", "Pronóstico", "Evaluación"])

def guardar_historial(df):
    df.to_csv(ARCH_HISTORIAL, index=False)

if "historial_df" not in st.session_state:
    st.session_state.historial_df = cargar_historial()

# ==============================================================================
# 3. INTERFAZ Y SIMULADOR
# ==============================================================================
st.title("⚽ Simulador Monte Carlo Predictivo Ultra Pro 2026/2027")

todas_las_ligas = list(LIGAS_AUTO.keys()) + list(LIGAS_ESTATICAS.keys())
liga_sel = st.selectbox("Seleccionar Torneo / Liga:", todas_las_ligas)

with st.spinner("Cargando métricas de la temporada..."):
    datos_equipos = obtener_promedios_torneo(liga_sel)

if datos_equipos:
    equipos = list(datos_equipos.keys())
    col1, col2 = st.columns(2)
    with col1:
        eq_loc = st.selectbox("Equipo Local:", equipos, index=0)
    with col2:
        idx_v = 1 if len(equipos) > 1 else 0
        eq_vis = st.selectbox("Equipo Visitante:", equipos, index=idx_v)

    d_loc = datos_equipos[eq_loc]
    d_vis = datos_equipos[eq_vis]

    st.subheader(f"📈 Métricas Base: {eq_loc} vs {eq_vis}")
    c_m1, c_m2, c_m3, c_m4, c_m5, c_m6 = st.columns(6)
    c_m1.metric("Partidos", f"{d_loc['pj']} / {d_vis['pj']}")
    c_m2.metric(f"Goles Local", f"{d_loc['gf']}")
    c_m3.metric(f"Goles Visitante", f"{d_vis['gf']}")
    c_m4.metric("Córners Est.", f"{round(d_loc['corners'] + d_vis['corners'], 1)}")
    c_m5.metric("Tarjetas Est.", f"{round(d_loc['tarjetas'] + d_vis['tarjetas'], 1)}")
    c_m6.metric("Remates Est.", f"{round(d_loc.get('remates_arco', 5.0) + d_vis.get('remates_arco', 4.5), 1)}")

    if st.button("🚀 CALCULAR PREDICCIÓN MONTE CARLO (10,000 SIMULACIONES)", type="primary", use_container_width=True):
        diff_loc = (d_loc["gf"] - d_vis["gc"]) + (d_loc["gf1t"] - 0.5)
        diff_vis = (d_vis["gf"] - d_loc["gc"]) + (d_vis["gf1t"] - 0.5)
        prio_loc = int(np.clip(5 + diff_loc * 2.0, 1, 10))
        prio_vis = int(np.clip(5 + diff_vis * 2.0, 1, 10))

        f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
        f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

        l_gf_loc = max(0.2, (d_loc["gf"] + d_vis["gc"]) / 2.0 * f_prio_loc)
        l_gf_vis = max(0.2, (d_vis["gf"] + d_loc["gc"]) / 2.0 * f_prio_vis)

        N = 10000
        goles_ft_loc = np.random.poisson(l_gf_loc, N)
        goles_ft_vis = np.random.poisson(l_gf_vis, N)

        p_win_loc = np.mean(goles_ft_loc > goles_ft_vis) * 100
        p_draw = np.mean(goles_ft_loc == goles_ft_vis) * 100
        p_win_vis = np.mean(goles_ft_loc < goles_ft_vis) * 100

        st.markdown("### 🏆 Probabilidades 1X2 (FT)")
        r1, r2, r3 = st.columns(3)
        r1.metric(f"Victoria {eq_loc}", f"{p_win_loc:.1f}%")
        r2.metric("Empate", f"{p_draw:.1f}%")
        r3.metric(f"Victoria {eq_vis}", f"{p_win_vis:.1f}%")
else:
    st.error("No se pudieron cargar los datos del torneo seleccionado.")
