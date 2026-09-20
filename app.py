import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import datetime

st.set_page_config(page_title="Simulador Monte Carlo Predictivo Ultra Pro 2026/2027", layout="wide")

ARCH_HISTORIAL = "registro_pronosticos.csv"

# ==============================================================================
# 1. BASE DE DATOS Y FEEDS AUTOMÁTICOS (TEMPORADA 2026/2027)
# ==============================================================================

# Feeds CSV con actualización automática diaria para las 5 ligas europeas principales
LIGAS_AUTO = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League 26/27": "https://www.football-data.co.uk/mmz4281/2627/E0.csv",
    "🇪🇸 LaLiga Española 26/27": "https://www.football-data.co.uk/mmz4281/2627/SP1.csv",
    "🇮🇹 Serie A 26/27": "https://www.football-data.co.uk/mmz4281/2627/I1.csv",
    "🇩🇪 Bundesliga 26/27": "https://www.football-data.co.uk/mmz4281/2627/D1.csv",
    "🇫🇷 Ligue 1 26/27": "https://www.football-data.co.uk/mmz4281/2627/F1.csv"
}

# Bases completas para competiciones UEFA, Liga MX, Arabia y Honduras
LIGAS_ESTATICAS = {
    "🇲🇽 Liga MX (Apertura 2026 / Clausura 2027)": {
        "Club América": {"pj": 8, "gf": 2.10, "gc": 0.90, "gf1t": 1.10, "corners": 6.3, "tarjetas": 2.2, "remates_arco": 5.6},
        "Guadalajara Chivas": {"pj": 8, "gf": 1.85, "gc": 1.00, "gf1t": 0.90, "corners": 6.0, "tarjetas": 2.3, "remates_arco": 4.9},
        "Cruz Azul": {"pj": 8, "gf": 1.95, "gc": 0.85, "gf1t": 1.00, "corners": 6.2, "tarjetas": 2.1, "remates_arco": 5.3},
        "Tigres UANL": {"pj": 8, "gf": 2.00, "gc": 1.05, "gf1t": 1.05, "corners": 6.2, "tarjetas": 2.2, "remates_arco": 5.4},
        "Monterrey Rayados": {"pj": 8, "gf": 2.15, "gc": 0.95, "gf1t": 1.10, "corners": 6.5, "tarjetas": 2.0, "remates_arco": 5.8},
        "Pumas UNAM": {"pj": 8, "gf": 1.70, "gc": 1.25, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.4, "remates_arco": 4.6},
        "Deportivo Toluca": {"pj": 8, "gf": 2.20, "gc": 1.10, "gf1t": 1.15, "corners": 6.4, "tarjetas": 2.1, "remates_arco": 5.7},
        "Pachuca FC": {"pj": 8, "gf": 1.65, "gc": 1.30, "gf1t": 0.75, "corners": 6.0, "tarjetas": 2.5, "remates_arco": 4.5},
        "Club León": {"pj": 8, "gf": 1.60, "gc": 1.35, "gf1t": 0.80, "corners": 5.9, "tarjetas": 2.3, "remates_arco": 4.4},
        "Santos Laguna": {"pj": 8, "gf": 1.45, "gc": 1.50, "gf1t": 0.70, "corners": 5.5, "tarjetas": 2.6, "remates_arco": 4.1},
        "Atlas FC": {"pj": 8, "gf": 1.40, "gc": 1.45, "gf1t": 0.65, "corners": 5.6, "tarjetas": 2.4, "remates_arco": 4.0},
        "Club Necaxa": {"pj": 8, "gf": 1.35, "gc": 1.40, "gf1t": 0.60, "corners": 5.3, "tarjetas": 2.2, "remates_arco": 3.9},
        "Club Puebla": {"pj": 8, "gf": 1.25, "gc": 1.60, "gf1t": 0.55, "corners": 5.1, "tarjetas": 2.5, "remates_arco": 3.7},
        "Club Tijuana (Xolos)": {"pj": 8, "gf": 1.30, "gc": 1.55, "gf1t": 0.60, "corners": 5.2, "tarjetas": 2.6, "remates_arco": 3.8},
        "Querétaro FC": {"pj": 8, "gf": 1.15, "gc": 1.65, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.5, "remates_arco": 3.5},
        "Atlético San Luis": {"pj": 8, "gf": 1.40, "gc": 1.50, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.3, "remates_arco": 4.0},
        "FC Juárez (Bravos)": {"pj": 8, "gf": 1.20, "gc": 1.70, "gf1t": 0.50, "corners": 4.9, "tarjetas": 2.7, "remates_arco": 3.6},
        "Atlante FC": {"pj": 8, "gf": 1.10, "gc": 1.60, "gf1t": 0.45, "corners": 4.7, "tarjetas": 2.4, "remates_arco": 3.4}
    },
    "🇸🇦 Saudi Pro League 2026/2027 (18 Equipos)": {
        "Al-Hilal FC": {"pj": 7, "gf": 3.28, "gc": 0.71, "gf1t": 1.40, "corners": 6.9, "tarjetas": 1.6, "remates_arco": 7.1},
        "Ittihad FC": {"pj": 7, "gf": 1.71, "gc": 0.86, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.2, "remates_arco": 4.8},
        "Al-Nassr FC": {"pj": 7, "gf": 2.28, "gc": 1.00, "gf1t": 1.10, "corners": 6.3, "tarjetas": 2.0, "remates_arco": 6.0},
        "Al-Qadisiya": {"pj": 7, "gf": 2.28, "gc": 1.14, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.3, "remates_arco": 5.5},
        "NEOM SC": {"pj": 7, "gf": 1.85, "gc": 0.86, "gf1t": 0.90, "corners": 5.5, "tarjetas": 2.1, "remates_arco": 4.9},
        "Al-Ahli Saudi FC": {"pj": 7, "gf": 2.28, "gc": 1.42, "gf1t": 1.00, "corners": 5.7, "tarjetas": 2.4, "remates_arco": 5.2},
        "Al-Kholood Club": {"pj": 7, "gf": 1.71, "gc": 1.42, "gf1t": 0.75, "corners": 4.8, "tarjetas": 2.5, "remates_arco": 4.2},
        "Al Draih": {"pj": 7, "gf": 1.00, "gc": 0.71, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.3, "remates_arco": 3.5},
        "Al-Ettifaq": {"pj": 7, "gf": 1.57, "gc": 1.57, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.2, "remates_arco": 4.3},
        "Al-Hazm": {"pj": 7, "gf": 1.00, "gc": 1.28, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6, "remates_arco": 3.4},
        "Al-Riyadh": {"pj": 7, "gf": 1.14, "gc": 2.28, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.5, "remates_arco": 3.6},
        "Al-Fayha": {"pj": 7, "gf": 1.00, "gc": 1.57, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.4, "remates_arco": 3.3},
        "Al Khaleej Club": {"pj": 7, "gf": 0.43, "gc": 1.42, "gf1t": 0.20, "corners": 3.8, "tarjetas": 2.6, "remates_arco": 2.9},
        "Al-Shabab": {"pj": 7, "gf": 0.86, "gc": 1.57, "gf1t": 0.35, "corners": 4.6, "tarjetas": 2.7, "remates_arco": 3.7},
        "Al-Fateh": {"pj": 7, "gf": 0.57, "gc": 1.57, "gf1t": 0.25, "corners": 4.2, "tarjetas": 2.4, "remates_arco": 3.1},
        "Al-Faisaly": {"pj": 7, "gf": 0.71, "gc": 1.85, "gf1t": 0.30, "corners": 3.9, "tarjetas": 2.5, "remates_arco": 3.2},
        "Al-Taawoun FC": {"pj": 7, "gf": 0.43, "gc": 1.71, "gf1t": 0.20, "corners": 4.1, "tarjetas": 2.3, "remates_arco": 3.0},
        "Abha Club": {"pj": 7, "gf": 0.71, "gc": 1.85, "gf1t": 0.30, "corners": 3.7, "tarjetas": 2.8, "remates_arco": 3.1}
    },
    "🇭🇳 Liga Nacional Honduras (Apertura 2026 - 12 Equipos)": {
        "CD Olimpia": {"pj": 7, "gf": 2.20, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 2.3, "remates_arco": 5.8},
        "FC Motagua": {"pj": 7, "gf": 1.90, "gc": 1.00, "gf1t": 0.85, "corners": 5.4, "tarjetas": 2.5, "remates_arco": 5.1},
        "Real España": {"pj": 7, "gf": 1.85, "gc": 0.90, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.2, "remates_arco": 5.0},
        "CD Marathón": {"pj": 7, "gf": 1.70, "gc": 0.95, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.6, "remates_arco": 4.4},
        "Olancho FC": {"pj": 7, "gf": 1.30, "gc": 1.15, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3, "remates_arco": 3.9},
        "Génesis FC": {"pj": 7, "gf": 1.20, "gc": 1.30, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.4, "remates_arco": 3.6},
        "Juticalpa FC": {"pj": 7, "gf": 1.10, "gc": 1.40, "gf1t": 0.45, "corners": 4.1, "tarjetas": 2.5, "remates_arco": 3.5},
        "Lobos UPNFM": {"pj": 7, "gf": 1.15, "gc": 1.65, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.4, "remates_arco": 3.6},
        "Platense FC": {"pj": 7, "gf": 1.25, "gc": 1.45, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.7, "remates_arco": 3.7},
        "CD Choloma": {"pj": 7, "gf": 1.05, "gc": 1.60, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.6, "remates_arco": 3.3},
        "CD Estrella Roja": {"pj": 7, "gf": 1.35, "gc": 1.70, "gf1t": 0.55, "corners": 4.2, "tarjetas": 2.8, "remates_arco": 3.8},
        "CA Independiente Siguatepeque": {"pj": 7, "gf": 1.15, "gc": 1.50, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5, "remates_arco": 3.5}
    },
    "🇪🇺 UEFA Champions League (2026/27 - 36 Equipos)": {
        "Arsenal": {"pj": 8, "gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6, "remates_arco": 6.2},
        "Aston Villa": {"pj": 8, "gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.1, "remates_arco": 4.8},
        "Liverpool": {"pj": 8, "gf": 2.40, "gc": 0.88, "gf1t": 1.15, "corners": 7.0, "tarjetas": 1.6, "remates_arco": 6.3},
        "Manchester City": {"pj": 8, "gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4, "remates_arco": 6.9},
        "Manchester United": {"pj": 8, "gf": 1.80, "gc": 1.18, "gf1t": 0.78, "corners": 5.8, "tarjetas": 2.0, "remates_arco": 4.9},
        "Lille": {"pj": 8, "gf": 1.75, "gc": 1.00, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.0, "remates_arco": 4.5},
        "PSG": {"pj": 8, "gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8, "remates_arco": 6.1},
        "Napoli": {"pj": 8, "gf": 1.90, "gc": 0.95, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.0, "remates_arco": 5.2},
        "Bayern Múnich": {"pj": 8, "gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5, "remates_arco": 6.8},
        "Borussia Dortmund": {"pj": 8, "gf": 2.10, "gc": 1.18, "gf1t": 0.95, "corners": 5.9, "tarjetas": 2.0, "remates_arco": 5.5},
        "AS Roma": {"pj": 8, "gf": 1.70, "gc": 1.10, "gf1t": 0.68, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.6},
        "Inter de Milán": {"pj": 8, "gf": 2.18, "gc": 0.68, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.7, "remates_arco": 5.4},
        "Real Madrid": {"pj": 8, "gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7, "remates_arco": 6.6},
        "FC Barcelona": {"pj": 8, "gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9, "remates_arco": 6.5},
        "Atlético de Madrid": {"pj": 8, "gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6, "remates_arco": 4.5},
        "FC Porto": {"pj": 8, "gf": 2.10, "gc": 0.85, "gf1t": 0.98, "corners": 6.1, "tarjetas": 2.1, "remates_arco": 5.4},
        "Sporting CP": {"pj": 8, "gf": 2.25, "gc": 0.82, "gf1t": 1.08, "corners": 6.3, "tarjetas": 1.8, "remates_arco": 5.8},
        "RB Leipzig": {"pj": 8, "gf": 2.00, "gc": 1.08, "gf1t": 0.90, "corners": 5.8, "tarjetas": 1.9, "remates_arco": 5.2}
    },
    "🇪🇺 UEFA Europa League (2026/27 - 36 Equipos)": {
        "Bayer Leverkusen": {"pj": 8, "gf": 2.20, "gc": 0.92, "gf1t": 1.02, "corners": 6.2, "tarjetas": 1.9, "remates_arco": 5.8},
        "Juventus": {"pj": 8, "gf": 1.80, "gc": 0.68, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.0, "remates_arco": 4.9},
        "AC Milan": {"pj": 8, "gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.2, "remates_arco": 5.1},
        "Marseille": {"pj": 8, "gf": 1.95, "gc": 1.15, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.4, "remates_arco": 5.3},
        "Lyon": {"pj": 8, "gf": 1.82, "gc": 1.22, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2, "remates_arco": 5.0},
        "Real Sociedad": {"pj": 8, "gf": 1.48, "gc": 1.05, "gf1t": 0.65, "corners": 5.5, "tarjetas": 2.1, "remates_arco": 4.5},
        "AZ Alkmaar": {"pj": 8, "gf": 1.88, "gc": 1.10, "gf1t": 0.82, "corners": 5.7, "tarjetas": 1.9, "remates_arco": 4.9},
        "Benfica": {"pj": 8, "gf": 2.10, "gc": 0.88, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.9, "remates_arco": 5.4},
        "Celtic": {"pj": 8, "gf": 2.25, "gc": 1.10, "gf1t": 1.02, "corners": 6.4, "tarjetas": 1.6, "remates_arco": 5.8}
    },
    "🇪🇺 UEFA Conference League (2026/27 - 36 Equipos)": {
        "Atalanta": {"pj": 6, "gf": 2.15, "gc": 1.00, "gf1t": 1.00, "corners": 6.1, "tarjetas": 2.0, "remates_arco": 5.7},
        "Ajax": {"pj": 6, "gf": 2.02, "gc": 1.05, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.8, "remates_arco": 5.5},
        "Mónaco": {"pj": 6, "gf": 1.95, "gc": 1.10, "gf1t": 0.88, "corners": 5.6, "tarjetas": 2.1, "remates_arco": 5.1},
        "Brighton": {"pj": 6, "gf": 1.88, "gc": 1.25, "gf1t": 0.82, "corners": 5.8, "tarjetas": 2.0, "remates_arco": 4.9},
        "Braga": {"pj": 6, "gf": 1.82, "gc": 1.18, "gf1t": 0.78, "corners": 5.6, "tarjetas": 2.2, "remates_arco": 4.8},
        "FC Copenhague": {"pj": 6, "gf": 1.82, "gc": 1.08, "gf1t": 0.78, "corners": 5.6, "tarjetas": 1.9, "remates_arco": 4.7}
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

            tarj_h = (home['HY'].sum() + home['HR'].sum()) if ('HY' in home and 'HR' in home) else 0
            tarj_a = (away['AY'].sum() + away['AR'].sum()) if ('AY' in away and 'AR' in away) else 0
            tarjetas = tarj_h + tarj_a

            rem_h = home['HST'].sum() if 'HST' in home else (gf * 2.3)
            rem_a = away['AST'].sum() if 'AST' in away else (gf * 2.3)
            remates = rem_h + rem_a

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
# 2. PERSISTENCIA EN ARCHIVO Y CONTROL DE PRONÓSTICOS
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
# 3. INTERFAZ Y SIMULADOR MONTE CARLO (10,000 PARTIDOS)
# ==============================================================================

st.title("⚽ Simulador Monte Carlo Predictivo Ultra Pro 2026/2027")

pestana1, pestana2 = st.tabs(["🚀 Simulación Monte Carlo y Pronósticos", "📜 Historial de Pronósticos (Aciertos/Fallos)"])

todas_las_ligas = list(LIGAS_AUTO.keys()) + list(LIGAS_ESTATICAS.keys())

with pestana1:
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

        st.subheader(f"📈 Métricas Base de Referencia: {eq_loc} vs {eq_vis}")
        c_m1, c_m2, c_m3, c_m4, c_m5, c_m6 = st.columns(6)
        c_m1.metric("Partidos Jugados", f"{d_loc['pj']} / {d_vis['pj']}")
        c_m2.metric(f"Goles Prom. {eq_loc}", f"{d_loc['gf']}")
        c_m3.metric(f"Goles Prom. {eq_vis}", f"{d_vis['gf']}")
        c_m4.metric("Córners Totales Est.", f"{round(d_loc['corners'] + d_vis['corners'], 1)}")
        c_m5.metric("Tarjetas Totales Est.", f"{round(d_loc['tarjetas'] + d_vis['tarjetas'], 1)}")
        c_m6.metric("Disparos a Puerta Est.", f"{round(d_loc.get('remates_arco', 5.0) + d_vis.get('remates_arco', 4.5), 1)}")

        st.divider()

        if st.button("🚀 CALCULAR PREDICCIÓN MONTE CARLO (10,000 SIMULACIONES)", type="primary", use_container_width=True):
            # Análisis de Ponderación e Intensidad
            diff_loc = (d_loc["gf"] - d_vis["gc"]) + (d_loc["gf1t"] - 0.5)
            diff_vis = (d_vis["gf"] - d_loc["gc"]) + (d_vis["gf1t"] - 0.5)
            prio_loc = int(np.clip(5 + diff_loc * 2.0, 1, 10))
            prio_vis = int(np.clip(5 + diff_vis * 2.0, 1, 10))

            f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
            f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

            tarj_comb = d_loc.get("tarjetas", 2.2) + d_vis.get("tarjetas", 2.2)
            goles_comb = d_loc["gf"] + d_vis["gf"]
            corners_comb = d_loc["corners"] + d_vis["corners"]
            score_ritmo = (tarj_comb / 4.5) * 0.5 + (goles_comb / 3.0) * 0.3 + (corners_comb / 10.0) * 0.2
            f_ritmo = 1.28 if score_ritmo >= 1.22 else (1.15 if score_ritmo >= 1.05 else (1.00 if score_ritmo >= 0.88 else 0.80))

            # Parámetros lambda para las distribuciones Poisson
            l_gf_loc = max(0.2, (d_loc["gf"] + d_vis["gc"]) / 2.0 * f_prio_loc * f_ritmo)
            l_gf_vis = max(0.2, (d_vis["gf"] + d_loc["gc"]) / 2.0 * f_prio_vis * f_ritmo)

            l_1t_loc = max(0.1, d_loc["gf1t"] * f_prio_loc)
            l_1t_vis = max(0.1, d_vis["gf1t"] * f_prio_vis)

            l_2t_loc = max(0.1, l_gf_loc - l_1t_loc)
            l_2t_vis = max(0.1, l_gf_vis - l_1t_vis)

            l_corners_tot = (d_loc["corners"] + d_vis["corners"]) * f_ritmo
            l_tarjetas_tot = (d_loc["tarjetas"] + d_vis["tarjetas"]) * f_ritmo
            l_remates_tot = (d_loc.get("remates_arco", 5.0) + d_vis.get("remates_arco", 4.5)) * f_ritmo

            # 10,000 Iteraciones Monte Carlo
            N = 10000
            goles_1t_loc = np.random.poisson(l_1t_loc, N)
            goles_1t_vis = np.random.poisson(l_1t_vis, N)

            goles_2t_loc = np.random.poisson(l_2t_loc, N)
            goles_2t_vis = np.random.poisson(l_2t_vis, N)

            goles_ft_loc = goles_1t_loc + goles_2t_loc
            goles_ft_vis = goles_1t_vis + goles_2t_vis

            corners_ft = np.random.poisson(l_corners_tot, N)
            corners_1t = np.random.poisson(l_corners_tot * 0.45, N)

            tarjetas_ft = np.random.poisson(l_tarjetas_tot, N)
            p_roja_base = min(0.45, 0.16 * (l_tarjetas_tot / 4.2))
            rojas = np.random.binomial(1, p_roja_base, N)

            remates_ft = np.random.poisson(l_remates_tot, N)

            # Cálculo de Probabilidades 1X2
            p_win_loc_ft = np.mean(goles_ft_loc > goles_ft_vis) * 100
            p_draw_ft = np.mean(goles_ft_loc == goles_ft_vis) * 100
            p_win_vis_ft = np.mean(goles_ft_loc < goles_ft_vis) * 100

            p_win_loc_1t = np.mean(goles_1t_loc > goles_1t_vis) * 100
            p_draw_1t = np.mean(goles_1t_loc == goles_1t_vis) * 100
            p_win_vis_1t = np.mean(goles_1t_loc < goles_1t_vis) * 100

            p_win_loc_2t = np.mean(goles_2t_loc > goles_2t_vis) * 100
            p_draw_2t = np.mean(goles_2t_loc == goles_2t_vis) * 100
            p_win_vis_2t = np.mean(goles_2t_loc < goles_2t_vis) * 100

            # Despliegue de Ganadores y Resultados de Simulación
            st.markdown("### 🏆 ¿Quién gana? - Probabilidades 1X2 (FT / 1T / 2T)")

            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.markdown("**⏱️ Tiempo Completo (FT)**")
                st.metric(f"Victoria {eq_loc}", f"{p_win_loc_ft:.1f}%")
                st.metric("Empate Final", f"{p_draw_ft:.1f}%")
                st.metric(f"Victoria {eq_vis}", f"{p_win_vis_ft:.1f}%")

            with col_r2:
                st.markdown("**1️⃣ Primer Tiempo (1T)**")
                st.metric(f"Gana 1T {eq_loc}", f"{p_win_loc_1t:.1f}%")
                st.metric("Empate 1T", f"{p_draw_1t:.1f}%")
                st.metric(f"Gana 1T {eq_vis}", f"{p_win_vis_1t:.1f}%")

            with col_r3:
                st.markdown("**2️⃣ Segundo Tiempo (2T)**")
                st.metric(f"Gana 2T {eq_loc}", f"{p_win_loc_2t:.1f}%")
                st.metric("Empate 2T", f"{p_draw_2t:.1f}%")
                st.metric(f"Gana 2T {eq_vis}", f"{p_win_vis_2t:.1f}%")

            st.markdown("---")
            st.markdown("### 📊 Proyección de Goles, Córners, Tarjetas y Disparos")

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("#### ⚽ Goles y Córners")
                st.write(f"⏱️ **Goles 1er Tiempo (> 0.5 1T):** **{np.mean((goles_1t_loc + goles_1t_vis) > 0.5)*100:.1f}%** (Prom. 1T: {np.mean(goles_1t_loc + goles_1t_vis):.2f})")
                st.write(f"⚽ **Goles Partido Completo (> 2.5 FT):** **{np.mean((goles_ft_loc + goles_ft_vis) > 2.5)*100:.1f}%** (Prom. FT: {np.mean(goles_ft_loc + goles_ft_vis):.2f})")
                st.write(f"🚩 **Córners 1er Tiempo (> 4.5 1T):** **{np.mean(corners_1t > 4.5)*100:.1f}%** (Prom. 1T: {np.mean(corners_1t):.1f})")
                st.write(f"🚩 **Córners Partido Completo (> 9.5 FT):** **{np.mean(corners_ft > 9.5)*100:.1f}%** (Prom. FT: {np.mean(corners_ft):.1f})")

            with col_m2:
                st.markdown("#### 🟨🟫 Disciplina y Remates a Puerta")
                st.write(f"🟨 **Total Tarjetas Amarillas (> 4.5 FT):** **{np.mean(tarjetas_ft > 4.5)*100:.1f}%** (Prom. FT: {np.mean(tarjetas_ft):.1f})")
                st.write(f"🟥 **Probabilidad de Tarjeta Roja Directa/Doble Amarilla:** **{np.mean(rojas)*100:.1f}%**")
                st.write(f"🎯 **Disparos a Puerta Totales (> 8.5 FT):** **{np.mean(remates_ft > 8.5)*100:.1f}%** (Prom. FT: {np.mean(remates_ft):.1f})")

        st.divider()
        st.subheader("📝 Registrar Pronóstico en Archivo CSV")

        with st.form("form_guardar_pronostico"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                pronostico = st.selectbox("Predicción / Mercado:", [
                    f"Gana {eq_loc} FT", f"Gana {eq_vis} FT", "Empate FT",
                    f"Gana {eq_loc} 1T", f"Gana {eq_vis} 1T", "Empate 1T",
                    f"Gana {eq_loc} 2T", f"Gana {eq_vis} 2T", "Empate 2T",
                    "Over 0.5 Goles 1T", "Over 2.5 Goles FT", "Ambos Anotan (Sí)",
                    "Over 4.5 Córners 1T", "Over 9.5 Córners FT",
                    "Over 4.5 Tarjetas FT", "Habrá Tarjeta Roja (Sí)",
                    "Over 8.5 Disparos a Puerta FT"
                ])
            with c_p2:
                estado_inicial = st.selectbox("Estado del Encuentro:", ["⏳ Pendiente", "✅ Acertado", "❌ Fallado"])

            btn_guardar = st.form_submit_button("💾 Guardar Registro en CSV")

            if btn_guardar:
                nuevo_id = len(st.session_state.historial_df) + 1
                fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                partido_str = f"{eq_loc} vs {eq_vis}"

                nueva_fila = {
                    "ID": nuevo_id,
                    "Fecha": fecha_actual,
                    "Liga": liga_sel,
                    "Partido": partido_str,
                    "Pronóstico": pronostico,
                    "Evaluación": estado_inicial
                }

                st.session_state.historial_df = pd.concat([st.session_state.historial_df, pd.DataFrame([nueva_fila])], ignore_index=True)
                guardar_historial(st.session_state.historial_df)
                st.success("¡Pronóstico guardado exitosamente!")
    else:
        st.error("No se pudieron cargar los datos del torneo seleccionado.")

with pestana2:
    st.subheader("📋 Control y Edición de Aciertos / Fallos")
    df_actual = st.session_state.historial_df

    if not df_actual.empty:
        df_editado = st.data_editor(
            df_actual,
            column_config={
                "Evaluación": st.column_config.SelectboxColumn(
                    "¿Acertó el Pronóstico?",
                    options=["⏳ Pendiente", "✅ Acertado", "❌ Fallado"],
                    required=True
                )
            },
            disabled=["ID", "Fecha", "Liga", "Partido", "Pronóstico"],
            use_container_width=True
        )

        if st.button("💾 Actualizar Archivo CSV"):
            st.session_state.historial_df = df_editado
            guardar_historial(df_editado)
            st.success("¡Archivo `registro_pronosticos.csv` actualizado correctamente!")

        csv_bytes = df_editado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Registro (.CSV)",
            data=csv_bytes,
            file_name=f"registro_pronosticos_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Aún no tienes pronósticos registrados en la base de datos.")

