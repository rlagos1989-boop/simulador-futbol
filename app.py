import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime

st.set_page_config(page_title="Simulador Monte Carlo Predictivo Ultra Pro 2026/2027", layout="wide")

ARCH_HISTORIAL = "registro_pronosticos.csv"

# ==============================================================================
# 1. BASE DE DATOS Y FEEDS AUTOMÁTICOS (100% COBERTURA DE EQUIPOS Y NOMBRES REALES)
# ==============================================================================

# Ligas que extraen automáticamente a todos sus equipos en tiempo real desde servidor CSV
LIGAS_AUTO = {
    "🏴󠁧󠁢󠁥󠁮󠁧U+E007F Premier League (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/E0.csv",
    "🇪🇸 LaLiga Española (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/SP1.csv",
    "🇮🇹 Serie A (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/I1.csv",
    "🇩🇪 Bundesliga (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/D1.csv",
    "🇫🇷 Ligue 1 (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/F1.csv"
}
# ==============================================================================
# --- BOTÓN PARA LIMPIAR CACHÉ Y ACTUALIZAR DATOS ---
# ==============================================================================
if st.button("🔄 Limpiar Caché y Actualizar Datos"):
    st.cache_data.clear() # Borra la memoria temporal de Streamlit
    st.success("¡Caché limpiada correctamente! Recargando datos...")
    st.rerun() # Refresca la aplicación al instante


# Base estática completa restaurada al 100%
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
        "Atlante": {"pj": 10, "gf": 1.67, "gc": 1.67, "gf1t": 0.65, "corners": 4.3, "tarjetas": 2.6, "remates_arco": 3.4},
        "Puebla": {"pj": 10, "gf": 1.00, "gc": 1.00, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.6, "remates_arco": 3.7},
        "Guadalajara Chivas": {"pj": 10, "gf": 0.67, "gc": 1.00, "gf1t": 0.30, "corners": 5.2, "tarjetas": 2.4, "remates_arco": 4.9},
        "Pachuca": {"pj": 10, "gf": 1.33, "gc": 1.00, "gf1t": 0.60, "corners": 5.5, "tarjetas": 2.2, "remates_arco": 4.5},
        "Club Leon": {"pj": 10, "gf": 1.00, "gc": 1.33, "gf1t": 0.45, "corners": 4.9, "tarjetas": 2.6, "remates_arco": 4.4},
        "Atl San Luis": {"pj": 10, "gf": 1.33, "gc": 1.67, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3, "remates_arco": 4.0},
        "Tigres UANL": {"pj": 10, "gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3, "remates_arco": 5.4},
        "Santos Laguna": {"pj": 10, "gf": 0.67, "gc": 2.33, "gf1t": 0.25, "corners": 4.6, "tarjetas": 2.4, "remates_arco": 4.1},
        "Juarez": {"pj": 10, "gf": 0.33, "gc": 2.33, "gf1t": 0.15, "corners": 4.3, "tarjetas": 2.8, "remates_arco": 3.6},
        "Mazatlán FC": {"pj": 10, "gf": 1.10, "gc": 1.60, "gf1t": 0.45, "corners": 4.7, "tarjetas": 2.4, "remates_arco": 3.4}
    },
    "🇺🇸 MLS (Estados Unidos - 30 Equipos)": {
        "Inter Miami": {"pj": 10, "gf": 2.20, "gc": 1.25, "gf1t": 1.05, "corners": 5.0, "tarjetas": 2.0, "remates_arco": 5.8},
        "Los Angeles FC": {"pj": 10, "gf": 1.90, "gc": 1.20, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.2, "remates_arco": 5.2},
        "LA Galaxy": {"pj": 10, "gf": 1.85, "gc": 1.30, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.1, "remates_arco": 5.0},
        "Columbus Crew": {"pj": 10, "gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.6, "tarjetas": 1.9, "remates_arco": 5.4},
        "Seattle Sounders": {"pj": 10, "gf": 1.60, "gc": 1.10, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.0, "remates_arco": 4.6},
        "FC Cincinnati": {"pj": 10, "gf": 1.75, "gc": 1.15, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.0, "remates_arco": 4.8},
        "Atlanta United": {"pj": 10, "gf": 1.65, "gc": 1.35, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.2, "remates_arco": 4.5},
        "New York City FC": {"pj": 10, "gf": 1.55, "gc": 1.25, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.1, "remates_arco": 4.4},
        "New York Red Bulls": {"pj": 10, "gf": 1.60, "gc": 1.20, "gf1t": 0.70, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.3},
        "Philadelphia Union": {"pj": 10, "gf": 1.70, "gc": 1.25, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.1, "remates_arco": 4.6},
        "Orlando City": {"pj": 10, "gf": 1.65, "gc": 1.30, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.0, "remates_arco": 4.5},
        "Nashville SC": {"pj": 10, "gf": 1.40, "gc": 1.15, "gf1t": 0.55, "corners": 4.8, "tarjetas": 1.9, "remates_arco": 4.0},
        "New England Revolution": {"pj": 10, "gf": 1.50, "gc": 1.40, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.2, "remates_arco": 4.2},
        "Toronto FC": {"pj": 10, "gf": 1.35, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.1, "remates_arco": 3.9},
        "CF Montréal": {"pj": 10, "gf": 1.40, "gc": 1.45, "gf1t": 0.58, "corners": 4.7, "tarjetas": 2.2, "remates_arco": 4.0},
        "DC United": {"pj": 10, "gf": 1.45, "gc": 1.55, "gf1t": 0.60, "corners": 4.9, "tarjetas": 2.4, "remates_arco": 4.1},
        "Charlotte FC": {"pj": 10, "gf": 1.38, "gc": 1.30, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.0, "remates_arco": 3.9},
        "Chicago Fire": {"pj": 10, "gf": 1.30, "gc": 1.60, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.3, "remates_arco": 3.8},
        "St. Louis City SC": {"pj": 10, "gf": 1.55, "gc": 1.45, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.2, "remates_arco": 4.3},
        "Minnesota United": {"pj": 10, "gf": 1.50, "gc": 1.35, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.0, "remates_arco": 4.2},
        "Houston Dynamo": {"pj": 10, "gf": 1.42, "gc": 1.30, "gf1t": 0.58, "corners": 4.8, "tarjetas": 2.1, "remates_arco": 4.0},
        "Sporting Kansas City": {"pj": 10, "gf": 1.45, "gc": 1.50, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.0, "remates_arco": 4.1},
        "Real Salt Lake": {"pj": 10, "gf": 1.60, "gc": 1.35, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.1, "remates_arco": 4.4},
        "Colorado Rapids": {"pj": 10, "gf": 1.50, "gc": 1.40, "gf1t": 0.62, "corners": 5.0, "tarjetas": 2.0, "remates_arco": 4.2},
        "Portland Timbers": {"pj": 10, "gf": 1.65, "gc": 1.50, "gf1t": 0.70, "corners": 5.3, "tarjetas": 2.2, "remates_arco": 4.5},
        "Vancouver Whitecaps": {"pj": 10, "gf": 1.48, "gc": 1.30, "gf1t": 0.60, "corners": 4.8, "tarjetas": 1.9, "remates_arco": 4.1},
        "San Jose Earthquakes": {"pj": 10, "gf": 1.35, "gc": 1.65, "gf1t": 0.52, "corners": 4.6, "tarjetas": 2.3, "remates_arco": 3.8},
        "Austin FC": {"pj": 10, "gf": 1.30, "gc": 1.40, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.0, "remates_arco": 3.7},
        "FC Dallas": {"pj": 10, "gf": 1.40, "gc": 1.38, "gf1t": 0.58, "corners": 4.8, "tarjetas": 2.1, "remates_arco": 3.9},
        "San Diego FC": {"pj": 10, "gf": 1.35, "gc": 1.35, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.0, "remates_arco": 3.8}
    },
    "🇭🇳 Liga Nacional (Honduras 2026/27)": {
        "Real Espana": {"pj": 10, "gf": 2.50, "gc": 0.00, "gf1t": 1.00, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 5.0},
        "Olimpia": {"pj": 10, "gf": 2.50, "gc": 0.50, "gf1t": 1.10, "corners": 5.8, "tarjetas": 2.4, "remates_arco": 5.8},
        "Marathon": {"pj": 10, "gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.7, "remates_arco": 4.4},
        "Olancho": {"pj": 10, "gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.8, "remates_arco": 3.9},
        "Motagua": {"pj": 10, "gf": 1.50, "gc": 1.00, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.6, "remates_arco": 5.1},
        "Estrella Roja": {"pj": 10, "gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.0, "tarjetas": 2.9, "remates_arco": 3.8},
        "Atletico Independiente": {"pj": 10, "gf": 1.00, "gc": 1.00, "gf1t": 0.40, "corners": 3.9, "tarjetas": 3.0, "remates_arco": 3.5},
        "Genesis": {"pj": 10, "gf": 1.00, "gc": 1.00, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.8, "remates_arco": 3.6},
        "UPNFM": {"pj": 10, "gf": 0.50, "gc": 1.50, "gf1t": 0.25, "corners": 3.8, "tarjetas": 2.9, "remates_arco": 3.6},
        "Platense": {"pj": 10, "gf": 0.50, "gc": 2.00, "gf1t": 0.20, "corners": 3.7, "tarjetas": 3.1, "remates_arco": 3.7},
        "Choloma": {"pj": 10, "gf": 0.50, "gc": 2.00, "gf1t": 0.20, "corners": 3.6, "tarjetas": 3.2, "remates_arco": 3.3},
        "Juticalpa": {"pj": 10, "gf": 0.50, "gc": 3.00, "gf1t": 0.15, "corners": 3.5, "tarjetas": 3.0, "remates_arco": 3.5},
        "CD Victoria": {"pj": 10, "gf": 1.25, "gc": 1.45, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.7, "remates_arco": 3.7},
        "Real Sociedad": {"pj": 10, "gf": 1.05, "gc": 1.60, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.6, "remates_arco": 3.3}
    },
    "🇸🇦 Saudi Professional League (2026/27)": {
        "Al Hilal": {"pj": 10, "gf": 2.30, "gc": 0.80, "gf1t": 1.10, "corners": 6.2, "tarjetas": 1.9, "remates_arco": 7.1},
        "Al Ettifaq": {"pj": 10, "gf": 1.45, "gc": 1.25, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.3, "remates_arco": 4.3},
        "Al Ittihad": {"pj": 10, "gf": 1.95, "gc": 1.10, "gf1t": 0.90, "corners": 5.6, "tarjetas": 2.4, "remates_arco": 4.8},
        "Al Shabab": {"pj": 10, "gf": 1.50, "gc": 1.30, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.4, "remates_arco": 3.7},
        "Al Ahli SC": {"pj": 10, "gf": 1.85, "gc": 1.15, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.2, "remates_arco": 5.2},
        "Al Nassr": {"pj": 10, "gf": 2.20, "gc": 1.00, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.1, "remates_arco": 6.0},
        "Neom SC": {"pj": 10, "gf": 1.30, "gc": 1.40, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.3, "remates_arco": 4.9},
        "Al-Qadisiya": {"pj": 10, "gf": 2.28, "gc": 1.14, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.3, "remates_arco": 5.5},
        "Al-Kholood Club": {"pj": 10, "gf": 1.71, "gc": 1.42, "gf1t": 0.75, "corners": 4.8, "tarjetas": 2.5, "remates_arco": 4.2},
        "Al Draih": {"pj": 10, "gf": 1.00, "gc": 0.71, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.3, "remates_arco": 3.5},
        "Al-Hazm": {"pj": 10, "gf": 1.00, "gc": 1.28, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6, "remates_arco": 3.4},
        "Al-Riyadh": {"pj": 10, "gf": 1.14, "gc": 2.28, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.5, "remates_arco": 3.6},
        "Al-Fayha": {"pj": 10, "gf": 1.00, "gc": 1.57, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.4, "remates_arco": 3.3},
        "Al Khaleej Club": {"pj": 10, "gf": 0.43, "gc": 1.42, "gf1t": 0.20, "corners": 3.8, "tarjetas": 2.6, "remates_arco": 2.9},
        "Al-Fateh": {"pj": 10, "gf": 0.57, "gc": 1.57, "gf1t": 0.25, "corners": 4.2, "tarjetas": 2.4, "remates_arco": 3.1},
        "Al-Taawoun FC": {"pj": 10, "gf": 0.43, "gc": 1.71, "gf1t": 0.20, "corners": 4.1, "tarjetas": 2.3, "remates_arco": 3.0},
        "Al-Okhdood": {"pj": 10, "gf": 0.80, "gc": 1.65, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.5, "remates_arco": 3.2},
        "Damac FC": {"pj": 10, "gf": 1.10, "gc": 1.60, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.4, "remates_arco": 3.5},
        "Al-Raed": {"pj": 10, "gf": 0.90, "gc": 1.75, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6, "remates_arco": 3.3}
    },
     "🇪🇺 UEFA Champions League (2026/27 - 36 Equipos)": {
        "Real Madrid": {"pj": 8, "gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7, "remates_arco": 6.6},
        "Manchester City": {"pj": 8, "gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4, "remates_arco": 6.9},
        "FC Barcelona": {"pj": 8, "gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9, "remates_arco": 6.5},
        "Bayern Múnich": {"pj": 8, "gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5, "remates_arco": 6.8},
        "Arsenal": {"pj": 8, "gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6, "remates_arco": 6.2},
        "PSG": {"pj": 8, "gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8, "remates_arco": 6.1},
        "Inter de Milán": {"pj": 8, "gf": 2.18, "gc": 0.68, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.7, "remates_arco": 5.4},
        "Liverpool": {"pj": 8, "gf": 2.40, "gc": 0.88, "gf1t": 1.15, "corners": 7.0, "tarjetas": 1.6, "remates_arco": 6.3},
        "Atlético de Madrid": {"pj": 8, "gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6, "remates_arco": 4.5},
        "Aston Villa": {"pj": 8, "gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.1, "remates_arco": 4.8},
        "Borussia Dortmund": {"pj": 8, "gf": 2.10, "gc": 1.18, "gf1t": 0.95, "corners": 5.9, "tarjetas": 2.0, "remates_arco": 5.5},
        "Roma": {"pj": 8, "gf": 1.75, "gc": 1.00, "gf1t": 0.75, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.7},
        "Manchester United": {"pj": 8, "gf": 1.80, "gc": 1.18, "gf1t": 0.78, "corners": 5.8, "tarjetas": 2.0, "remates_arco": 4.9},
        "Sporting CP": {"pj": 8, "gf": 2.25, "gc": 0.82, "gf1t": 1.08, "corners": 6.3, "tarjetas": 1.8, "remates_arco": 5.8},
        "Real Betis": {"pj": 8, "gf": 1.80, "gc": 0.95, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.2, "remates_arco": 4.8},
        "Porto": {"pj": 8, "gf": 1.98, "gc": 0.95, "gf1t": 0.88, "corners": 5.9, "tarjetas": 2.1, "remates_arco": 5.2},
        "Club Brujas": {"pj": 8, "gf": 1.88, "gc": 1.05, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.1, "remates_arco": 4.8},
        "PSV": {"pj": 8, "gf": 2.45, "gc": 0.85, "gf1t": 1.18, "corners": 6.6, "tarjetas": 1.5, "remates_arco": 6.2},
        "Lille": {"pj": 8, "gf": 1.75, "gc": 1.00, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.0, "remates_arco": 4.5},
        "RB Leipzig": {"pj": 8, "gf": 2.00, "gc": 1.08, "gf1t": 0.90, "corners": 5.8, "tarjetas": 1.9, "remates_arco": 5.2},
        "Napoli": {"pj": 8, "gf": 1.90, "gc": 1.02, "gf1t": 0.82, "corners": 5.6, "tarjetas": 2.1, "remates_arco": 5.0},
        "Feyenoord": {"pj": 8, "gf": 2.05, "gc": 1.02, "gf1t": 0.92, "corners": 6.1, "tarjetas": 1.8, "remates_arco": 5.3},
        "Villarreal": {"pj": 8, "gf": 1.78, "gc": 1.12, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2, "remates_arco": 4.6},
        "Galatasaray": {"pj": 8, "gf": 2.22, "gc": 1.12, "gf1t": 1.02, "corners": 6.2, "tarjetas": 2.5, "remates_arco": 5.7},
        "Shakhtar Donetsk": {"pj": 8, "gf": 1.80, "gc": 1.15, "gf1t": 0.78, "corners": 5.2, "tarjetas": 2.0, "remates_arco": 4.6},
        "Bodø/Glimt": {"pj": 8, "gf": 2.02, "gc": 1.22, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.7, "remates_arco": 5.2},
        "Fenerbahçe": {"pj": 8, "gf": 2.12, "gc": 0.98, "gf1t": 0.98, "corners": 6.0, "tarjetas": 2.4, "remates_arco": 5.5},
        "Stuttgart": {"pj": 8, "gf": 1.90, "gc": 1.28, "gf1t": 0.82, "corners": 5.6, "tarjetas": 1.9, "remates_arco": 5.0},
        "Slavia Praga": {"pj": 8, "gf": 1.75, "gc": 1.20, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.3, "remates_arco": 4.5},
        "Lens": {"pj": 8, "gf": 1.68, "gc": 1.15, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.2, "remates_arco": 4.3},
        "Como": {"pj": 8, "gf": 1.65, "gc": 1.25, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.2, "remates_arco": 4.2},
        "Sabah": {"pj": 8, "gf": 1.50, "gc": 1.35, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.4, "remates_arco": 3.8},
        "LASK": {"pj": 8, "gf": 1.62, "gc": 1.25, "gf1t": 0.68, "corners": 4.9, "tarjetas": 2.2, "remates_arco": 4.1},
        "Viking Stavanger": {"pj": 8, "gf": 1.58, "gc": 1.30, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.3, "remates_arco": 4.0},
        "Slovan Bratislava": {"pj": 8, "gf": 1.45, "gc": 1.58, "gf1t": 0.58, "corners": 4.4, "tarjetas": 2.5, "remates_arco": 3.7},
        "AEK Atenas": {"pj": 8, "gf": 1.70, "gc": 1.15, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.4, "remates_arco": 4.4}
    },
    "🇪🇺 UEFA Europa League (2026/27 - 36 Equipos)": {
        "Anderlecht": {"pj": 8, "gf": 1.68, "gc": 1.12, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.1, "remates_arco": 4.3},
        "Athletic Club Bilbao": {"pj": 8, "gf": 1.80, "gc": 0.95, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.2, "remates_arco": 4.8},
        "AZ Alkmaar": {"pj": 8, "gf": 1.88, "gc": 1.10, "gf1t": 0.82, "corners": 5.7, "tarjetas": 1.9, "remates_arco": 4.9},
        "Besiktas": {"pj": 8, "gf": 1.78, "gc": 1.18, "gf1t": 0.78, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.6},
        "Bodø/Glimt": {"pj": 8, "gf": 2.02, "gc": 1.22, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.7, "remates_arco": 5.2},
        "Braga": {"pj": 8, "gf": 1.82, "gc": 1.18, "gf1t": 0.78, "corners": 5.6, "tarjetas": 2.2, "remates_arco": 4.8},
        "Dinamo Kiev": {"pj": 8, "gf": 1.55, "gc": 1.30, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1, "remates_arco": 3.9},
        "Eintracht Frankfurt": {"pj": 8, "gf": 1.95, "gc": 1.15, "gf1t": 0.88, "corners": 5.6, "tarjetas": 2.0, "remates_arco": 5.0},
        "Elfsborg": {"pj": 8, "gf": 1.50, "gc": 1.35, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.0, "remates_arco": 3.8},
        "FCSB (Steaua)": {"pj": 8, "gf": 1.48, "gc": 1.25, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.4, "remates_arco": 3.7},
        "Fenerbahçe": {"pj": 8, "gf": 2.12, "gc": 0.98, "gf1t": 0.98, "corners": 6.0, "tarjetas": 2.4, "remates_arco": 5.5},
        "Ferencvaros": {"pj": 8, "gf": 1.58, "gc": 1.22, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.4, "remates_arco": 4.0},
        "Galatasaray": {"pj": 8, "gf": 2.22, "gc": 1.12, "gf1t": 1.02, "corners": 6.2, "tarjetas": 2.5, "remates_arco": 5.7},
        "Hoffenheim": {"pj": 8, "gf": 1.85, "gc": 1.35, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.2, "remates_arco": 4.8},
        "Lazio": {"pj": 8, "gf": 1.90, "gc": 1.05, "gf1t": 0.85, "corners": 5.7, "tarjetas": 2.1, "remates_arco": 5.0},
        "Ludogorets Razgrad": {"pj": 8, "gf": 1.52, "gc": 1.28, "gf1t": 0.62, "corners": 4.8, "tarjetas": 2.3, "remates_arco": 3.9},
        "Lyon": {"pj": 8, "gf": 1.82, "gc": 1.22, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2, "remates_arco": 5.0},
        "Maccabi Tel Aviv": {"pj": 8, "gf": 1.50, "gc": 1.30, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.3, "remates_arco": 3.8},
        "Malmö FF": {"pj": 8, "gf": 1.65, "gc": 1.20, "gf1t": 0.70, "corners": 5.2, "tarjetas": 1.9, "remates_arco": 4.2},
        "Manchester United": {"pj": 8, "gf": 1.80, "gc": 1.18, "gf1t": 0.78, "corners": 5.8, "tarjetas": 2.0, "remates_arco": 4.9},
        "Midtjylland": {"pj": 8, "gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.2, "remates_arco": 4.4},
        "Niza": {"pj": 8, "gf": 1.62, "gc": 1.15, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.0, "remates_arco": 4.1},
        "Olympiacos": {"pj": 8, "gf": 1.78, "gc": 0.98, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.3, "remates_arco": 4.6},
        "PAOK Salónica": {"pj": 8, "gf": 1.75, "gc": 1.10, "gf1t": 0.75, "corners": 5.4, "tarjetas": 2.4, "remates_arco": 4.5},
        "FC Oporto": {"pj": 8, "gf": 2.10, "gc": 0.85, "gf1t": 0.98, "corners": 6.1, "tarjetas": 2.1, "remates_arco": 5.4},
        "Rangers FC": {"pj": 8, "gf": 1.82, "gc": 1.12, "gf1t": 0.78, "corners": 5.7, "tarjetas": 2.0, "remates_arco": 4.7},
        "RFS Riga": {"pj": 8, "gf": 1.30, "gc": 1.52, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.5, "remates_arco": 3.3},
        "AS Roma": {"pj": 8, "gf": 1.70, "gc": 1.10, "gf1t": 0.68, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.6},
        "Real Sociedad": {"pj": 8, "gf": 1.48, "gc": 1.05, "gf1t": 0.65, "corners": 5.5, "tarjetas": 2.1, "remates_arco": 4.5},
        "Slavia Praga": {"pj": 8, "gf": 1.95, "gc": 0.88, "gf1t": 0.88, "corners": 5.8, "tarjetas": 2.1, "remates_arco": 5.0},
        "Tottenham Hotspur": {"pj": 8, "gf": 2.15, "gc": 1.10, "gf1t": 0.95, "corners": 6.5, "tarjetas": 1.8, "remates_arco": 5.6},
        "Twente": {"pj": 8, "gf": 1.72, "gc": 1.18, "gf1t": 0.72, "corners": 5.4, "tarjetas": 2.0, "remates_arco": 4.4},
        "Union Saint-Gilloise": {"pj": 8, "gf": 1.58, "gc": 1.18, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.3, "remates_arco": 4.0},
        "Viktoria Plzen": {"pj": 8, "gf": 1.62, "gc": 1.08, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.2, "remates_arco": 4.2},
        "Qarabag FK": {"pj": 8, "gf": 1.68, "gc": 1.25, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.2, "remates_arco": 4.3}
    },
    "🇪🇺 UEFA Conference League (2026/27 - 36 Equipos)": {
        "AOP Paphos": {"pj": 6, "gf": 1.48, "gc": 1.18, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.5, "remates_arco": 3.8},
        "APOEL Nicosia": {"pj": 6, "gf": 1.50, "gc": 1.12, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.4, "remates_arco": 3.9},
        "Astana": {"pj": 6, "gf": 1.38, "gc": 1.32, "gf1t": 0.55, "corners": 4.4, "tarjetas": 2.2, "remates_arco": 3.5},
        "Banja Luka (Borac)": {"pj": 6, "gf": 1.22, "gc": 1.38, "gf1t": 0.48, "corners": 4.2, "tarjetas": 2.6, "remates_arco": 3.1},
        "Celje": {"pj": 6, "gf": 1.42, "gc": 1.38, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.3, "remates_arco": 3.6},
        "Cercle Brugge": {"pj": 6, "gf": 1.60, "gc": 1.25, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.1, "remates_arco": 4.1},
        "Chelsea FC": {"pj": 6, "gf": 2.40, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8, "remates_arco": 6.2},
        "Dinamo Minsk": {"pj": 6, "gf": 1.25, "gc": 1.40, "gf1t": 0.50, "corners": 4.1, "tarjetas": 2.4, "remates_arco": 3.2},
        "Djurgarden": {"pj": 6, "gf": 1.58, "gc": 1.20, "gf1t": 0.68, "corners": 5.0, "tarjetas": 1.9, "remates_arco": 4.0},
        "Fiorentina": {"pj": 6, "gf": 1.95, "gc": 1.05, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.1, "remates_arco": 5.2},
        "FC Copenhague": {"pj": 6, "gf": 1.82, "gc": 1.08, "gf1t": 0.78, "corners": 5.6, "tarjetas": 1.9, "remates_arco": 4.7},
        "FC St. Gallen": {"pj": 6, "gf": 1.65, "gc": 1.35, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.2, "remates_arco": 4.3},
        "Heidenheim": {"pj": 6, "gf": 1.62, "gc": 1.28, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.0, "remates_arco": 4.1},
        "HJK Helsinki": {"pj": 6, "gf": 1.35, "gc": 1.35, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.0, "remates_arco": 3.4},
        "Jagiellonia": {"pj": 6, "gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.3, "remates_arco": 4.4},
        "LASK Linz": {"pj": 6, "gf": 1.50, "gc": 1.25, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2, "remates_arco": 3.9},
        "Legia Varsovia": {"pj": 6, "gf": 1.75, "gc": 1.15, "gf1t": 0.75, "corners": 5.4, "tarjetas": 2.3, "remates_arco": 4.5},
        "Lugano": {"pj": 6, "gf": 1.52, "gc": 1.28, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2, "remates_arco": 3.9},
        "Mladá Boleslav": {"pj": 6, "gf": 1.40, "gc": 1.35, "gf1t": 0.58, "corners": 4.5, "tarjetas": 2.3, "remates_arco": 3.5},
        "Noa": {"pj": 6, "gf": 1.20, "gc": 1.48, "gf1t": 0.45, "corners": 4.0, "tarjetas": 2.5, "remates_arco": 3.1},
        "Omonia Nicosia": {"pj": 6, "gf": 1.42, "gc": 1.28, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.6, "remates_arco": 3.6},
        "Olimpija Ljubljana": {"pj": 6, "gf": 1.48, "gc": 1.22, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.2, "remates_arco": 3.8},
        "Panathinaikos": {"pj": 6, "gf": 1.58, "gc": 1.08, "gf1t": 0.68, "corners": 5.2, "tarjetas": 2.5, "remates_arco": 4.0},
        "Petrocub": {"pj": 6, "gf": 1.15, "gc": 1.50, "gf1t": 0.42, "corners": 3.9, "tarjetas": 2.6, "remates_arco": 2.9},
        "Rapid Viena": {"pj": 6, "gf": 1.70, "gc": 1.15, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.1, "remates_arco": 4.4},
        "Real Betis": {"pj": 6, "gf": 1.72, "gc": 1.02, "gf1t": 0.72, "corners": 5.5, "tarjetas": 2.2, "remates_arco": 4.5},
        "Shamrock Rovers": {"pj": 6, "gf": 1.30, "gc": 1.40, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.3, "remates_arco": 3.3},
        "The New Saints": {"pj": 6, "gf": 1.18, "gc": 1.55, "gf1t": 0.45, "corners": 3.8, "tarjetas": 2.5, "remates_arco": 3.0},
        "TSC Backa Topola": {"pj": 6, "gf": 1.35, "gc": 1.40, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.4, "remates_arco": 3.4},
        "Vitoria Guimaraes": {"pj": 6, "gf": 1.78, "gc": 1.05, "gf1t": 0.75, "corners": 5.5, "tarjetas": 2.3, "remates_arco": 4.6},
        "Vikingur Reykjavik": {"pj": 6, "gf": 1.32, "gc": 1.42, "gf1t": 0.52, "corners": 4.3, "tarjetas": 2.4, "remates_arco": 3.3},
        "Larne FC": {"pj": 6, "gf": 1.08, "gc": 1.60, "gf1t": 0.40, "corners": 3.7, "tarjetas": 2.7, "remates_arco": 2.8},
        "Gent": {"pj": 6, "gf": 1.68, "gc": 1.20, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.1, "remates_arco": 4.3},
        "Hearts": {"pj": 6, "gf": 1.45, "gc": 1.30, "gf1t": 0.58, "corners": 4.8, "tarjetas": 2.3, "remates_arco": 3.7},
        "Paksi FC": {"pj": 6, "gf": 1.35, "gc": 1.42, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.4, "remates_arco": 3.4},
        "Silkeborg": {"pj": 6, "gf": 1.50, "gc": 1.30, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.0, "remates_arco": 3.8}
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
# 2. PERSISTENCIA EN ARCHIVO Y CONTROL DE HISTORIAL
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
# 3. INTERFAZ Y SIMULADOR MONTE CARLO
# ==============================================================================

st.title("⚽ Simulador Monte Carlo Predictivo Ultra Pro 2026/2027")

pestana1, pestana2 = st.tabs(["🚀 Simulación Monte Carlo y Pronósticos", "📜 Historial de Pronósticos"])

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

            l_gf_loc = max(0.2, (d_loc["gf"] + d_vis["gc"]) / 2.0 * f_prio_loc * f_ritmo)
            l_gf_vis = max(0.2, (d_vis["gf"] + d_loc["gc"]) / 2.0 * f_prio_vis * f_ritmo)

            l_1t_loc = max(0.1, d_loc["gf1t"] * f_prio_loc)
            l_1t_vis = max(0.1, d_vis["gf1t"] * f_prio_vis)

            l_2t_loc = max(0.1, l_gf_loc - l_1t_loc)
            l_2t_vis = max(0.1, l_gf_vis - l_1t_vis)

            l_corners_tot = (d_loc["corners"] + d_vis["corners"]) * f_ritmo
            l_tarjetas_tot = (d_loc["tarjetas"] + d_vis["tarjetas"]) * f_ritmo
            l_remates_tot = (d_loc.get("remates_arco", 5.0) + d_vis.get("remates_arco", 4.5)) * f_ritmo

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

            # --- PROBABILIDADES DE GANADOR 1X2 ---
            p_win_loc_ft = np.mean(goles_ft_loc > goles_ft_vis) * 100
            p_draw_ft = np.mean(goles_ft_loc == goles_ft_vis) * 100
            p_win_vis_ft = np.mean(goles_ft_loc < goles_ft_vis) * 100

            p_win_loc_1t = np.mean(goles_1t_loc > goles_1t_vis) * 100
            p_draw_1t = np.mean(goles_1t_loc == goles_1t_vis) * 100
            p_win_vis_1t = np.mean(goles_1t_loc < goles_1t_vis) * 100

            p_win_loc_2t = np.mean(goles_2t_loc > goles_2t_vis) * 100
            p_draw_2t = np.mean(goles_2t_loc == goles_2t_vis) * 100
            p_win_vis_2t = np.mean(goles_2t_loc < goles_2t_vis) * 100

            # --- PORCENTAJES DE GOLES POR TIEMPO Y MERCADOS ---
            p_1t_05 = np.mean((goles_1t_loc + goles_1t_vis) > 0.5) * 100
            p_1t_15 = np.mean((goles_1t_loc + goles_1t_vis) > 1.5) * 100

            p_ft_05 = np.mean((goles_ft_loc + goles_ft_vis) > 0.5) * 100
            p_ft_15 = np.mean((goles_ft_loc + goles_ft_vis) > 1.5) * 100
            p_ft_25 = np.mean((goles_ft_loc + goles_ft_vis) > 2.5) * 100
            p_ft_35 = np.mean((goles_ft_loc + goles_ft_vis) > 3.5) * 100

            p_btts = np.mean((goles_ft_loc > 0) & (goles_ft_vis > 0)) * 100

            prom_1t_tot = np.mean(goles_1t_loc + goles_1t_vis)
            prom_ft_tot = np.mean(goles_ft_loc + goles_ft_vis)

            # --- DESPLIEGUE RESULTADOS 1X2 ---
            st.markdown("### 🏆 Probabilidades 1X2 (Tiempo Completo / Descanso / 2do Tiempo)")

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

            # --- FORMATO DE PORCENTAJES DE GOLES ---
            st.markdown("### ⚽ Mercados y Porcentajes de Goles")

            col_g1, col_g2, col_g3 = st.columns(3)

            with col_g1:
                st.markdown("#### ⏱️ Primer Tiempo (1T)")
                st.write(f"• **Over 0.5 Goles 1T:** **{p_1t_05:.1f}%**")
                st.write(f"• **Over 1.5 Goles 1T:** **{p_1t_15:.1f}%**")
                st.write(f"📊 *Promedio Esperado 1T:* **{prom_1t_tot:.2f} goles**")

            with col_g2:
                st.markdown("#### ⚽ Partido Completo (FT)")
                st.write(f"• **Over 0.5 Goles FT:** **{p_ft_05:.1f}%**")
                st.write(f"• **Over 1.5 Goles FT:** **{p_ft_15:.1f}%**")
                st.write(f"• **Over 2.5 Goles FT:** **{p_ft_25:.1f}%**")
                st.write(f"• **Over 3.5 Goles FT:** **{p_ft_35:.1f}%**")
                st.write(f"📊 *Promedio Esperado FT:* **{prom_ft_tot:.2f} goles**")

            with col_g3:
                st.markdown("#### 🤝 Ambos Equipos Anotan")
                st.write(f"• **Ambos Anotan (Sí / BTTS):** **{p_btts:.1f}%**")
                st.write(f"• **Ambos Anotan (No):** **{(100 - p_btts):.1f}%**")
                st.write(f"🎯 *Goles {eq_loc}:* **{np.mean(goles_ft_loc):.2f}**")
                st.write(f"🎯 *Goles {eq_vis}:* **{np.mean(goles_ft_vis):.2f}**")

            st.markdown("---")

            # --- CÓRNERS, TARJETAS Y DISPAROS ---
            st.markdown("### 🚩 Córners, Tarjetas y Disparos a Puerta")
            col_c1, col_c2 = st.columns(2)

            with col_c1:
                st.markdown("#### 🚩 Córners")
                st.write(f"• **Over 4.5 Córners 1T:** **{np.mean(corners_1t > 4.5)*100:.1f}%** (Prom: {np.mean(corners_1t):.1f})")
                st.write(f"• **Over 8.5 Córners FT:** **{np.mean(corners_ft > 8.5)*100:.1f}%** (Prom: {np.mean(corners_ft):.1f})")
                st.write(f"• **Over 9.5 Córners FT:** **{np.mean(corners_ft > 9.5)*100:.1f}%**")
                st.write(f"• **Over 10.5 Córners FT:** **{np.mean(corners_ft > 10.5)*100:.1f}%**")

            with col_c2:
                st.markdown("#### 🟨🟫 Disciplina y Remates")
                st.write(f"• **Over 3.5 Tarjetas FT:** **{np.mean(tarjetas_ft > 3.5)*100:.1f}%** (Prom: {np.mean(tarjetas_ft):.1f})")
                st.write(f"• **Over 4.5 Tarjetas FT:** **{np.mean(tarjetas_ft > 4.5)*100:.1f}%**")
                st.write(f"• **Probabilidad de Tarjeta Roja:** **{np.mean(rojas)*100:.1f}%**")
                st.write(f"• **Over 8.5 Disparos a Puerta:** **{np.mean(remates_ft > 8.5)*100:.1f}%** (Prom: {np.mean(remates_ft):.1f})")

        st.divider()
        st.subheader("📝 Registrar Pronóstico en Archivo CSV")

        with st.form("form_guardar_pronostico"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                pronostico = st.selectbox("Predicción / Mercado:", [
                    f"Gana {eq_loc} FT", f"Gana {eq_vis} FT", "Empate FT",
                    f"Gana {eq_loc} 1T", f"Gana {eq_vis} 1T", "Empate 1T",
                    "Over 0.5 Goles 1T", "Over 1.5 Goles 1T",
                    "Over 1.5 Goles FT", "Over 2.5 Goles FT", "Over 3.5 Goles FT",
                    "Ambos Anotan (Sí)", "Ambos Anotan (No)",
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

import matplotlib.pyplot as plt
from mplsoccer import Pitch

# ==============================================================================
# --- MÓDULO VISUAL: ESTILO ESTADIO, MARCADOR LED Y CANCHA TÁCTICA (MPLSOCCER) ---
# ==============================================================================

# Generador automático de URL de escudos/logos basados en el nombre del equipo
def obtener_logo_equipo(nombre_equipo):
    # Diccionario de respaldo para logos principales o formato automático vía API pública
    logos_especiales = {
        "Real Madrid": "https://a.espncdn.com/i/teamlogos/soccer/500/86.png",
        "Barcelona": "https://a.espncdn.com/i/teamlogos/soccer/500/83.png",
        "Manchester City": "https://a.espncdn.com/i/teamlogos/soccer/500/382.png",
        "Arsenal": "https://a.espncdn.com/i/teamlogos/soccer/500/359.png",
        "Inter Miami": "https://a.espncdn.com/i/teamlogos/soccer/500/18275.png",
        "Olimpia": "https://a.espncdn.com/i/teamlogos/soccer/500/2361.png",
        "Motagua": "https://a.espncdn.com/i/teamlogos/soccer/500/2362.png",
        "PSG": "https://a.espncdn.com/i/teamlogos/soccer/500/160.png",
        "Bayern Múnich": "https://a.espncdn.com/i/teamlogos/soccer/500/132.png"
    }
    # Si no está en el diccionario especial, busca un placeholder dinámico limpio con las iniciales
    if nombre_equipo in logos_especiales:
        return logos_especiales[nombre_equipo]
    return f"https://images.fotmob.com/image_resources/logo/teamlogo/{nombre_equipo.lower().replace(' ', '')}.png"

if 'goles_ft_loc' in locals() and 'goles_ft_vis' in locals():
    st.divider()
    
    # --- 1. MARCADOR LED ESTILO ESTADIO ---
    logo_loc_url = obtener_logo_equipo(eq_loc)
    logo_vis_url = obtener_logo_equipo(eq_vis)
    
    media_l_estadio = round(np.mean(goles_ft_loc), 1)
    media_v_estadio = round(np.mean(goles_ft_vis), 1)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 2px solid #334155; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); text-align: center; margin-bottom: 25px;">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 3px; color: #38bdf8; font-weight: 700; margin-bottom: 15px;">🏟️ Gran Pantalla del Estadio - Simulación Oficial</div>
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div style="width: 30%; text-align: center;">
                    <img src="{logo_loc_url}" width="75" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); border-radius: 50%; background: #ffffff10; padding: 5px;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/53/53283.png';">
                    <h3 style="color: white; margin-top: 10px; font-size: 20px;">{eq_loc}</h3>
                </div>
                <div style="width: 40%; text-align: center;">
                    <div style="background: #020617; display: inline-block; padding: 10px 30px; border-radius: 12px; border: 2px solid #0ea5e9; box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);">
                        <span style="font-size: 38px; font-weight: 900; color: #f8fafc; font-family: monospace;">{media_l_estadio} - {media_v_estadio}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 8px;">Expectativa de Goles (xG)</div>
                </div>
                <div style="width: 30%; text-align: center;">
                    <img src="{logo_vis_url}" width="75" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); border-radius: 50%; background: #ffffff10; padding: 5px;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/53/53283.png';">
                    <h3 style="color: white; margin-top: 10px; font-size: 20px;">{eq_vis}</h3>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

      # --- 2. CANCHA DE FÚTBOL TÁCTICA (MPLSOCCER - CORREGIDO) ---
    st.markdown("### 🗺️ Búnker Táctico: Posicionamiento en Cancha")
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1b4d3e', line_color='#ffffff', stripe=True)
    fig, ax = pitch.draw(figsize=(10, 6))
    
    # Coordenadas exactas con listas de igual tamaño para Local y Visitante
    # Local (Izquierda a Derecha)
    pitch.scatter([15], [40], s=300, color='#38bdf8', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Portero
    pitch.scatter([35, 35, 35, 35], [20, 35, 50, 65], s=250, color='#38bdf8', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Defensas
    pitch.scatter([60, 60], [30, 50], s=250, color='#38bdf8', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Mediocampistas
    pitch.scatter([85, 85, 85], [25, 50, 75], s=250, color='#38bdf8', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Delanteros

    # Visitante (Derecha a Izquierda)
    pitch.scatter([105], [40], s=300, color='#f43f5e', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Portero
    pitch.scatter([85, 85, 85, 85], [20, 35, 50, 65], s=250, color='#f43f5e', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Defensas
    pitch.scatter([60, 60], [25, 75], s=250, color='#f43f5e', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Mediocampistas
    pitch.scatter([35, 35, 35], [25, 50, 75], s=250, color='#f43f5e', edgecolors='white', linewidth=2, zorder=3, ax=ax) # Delanteros

    ax.set_title(f"Esquema Táctico en Vivo: {eq_loc} vs {eq_vis}", fontsize=14, color='white', fontweight='bold', pad=15)
    st.pyplot(fig)
# ==============================================================================
# --- ESTILOS CSS PARA MEJORAR CONTRASTE Y LEGIBILIDAD DE MÉTRICAS ---
# ==============================================================================
st.markdown("""
    <style>
    /* Forzar texto claro e iluminado en todas las métricas de Streamlit */
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        font-size: 28px !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }
    /* Contenedor de métricas estilo cristal translúcido iluminado */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# --- DESPLIEGUE DE RESULTADOS (SIN ERRORES DE SANGRÍA / INDENTACIÓN) ---
# ==============================================================================
if 'goles_ft_loc' in locals() and 'goles_ft_vis' in locals():
    
    # 1. MARCADOR LED ESTILO ESTADIO
    logo_loc_url = obtener_logo_equipo(eq_loc)
    logo_vis_url = obtener_logo_equipo(eq_vis)
    
    media_l_estadio = round(np.mean(goles_ft_loc), 1)
    media_v_estadio = round(np.mean(goles_ft_vis), 1)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 2px solid #334155; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); text-align: center; margin-bottom: 25px;">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 3px; color: #38bdf8; font-weight: 700; margin-bottom: 15px;">🏟️ Gran Pantalla del Estadio - Simulación Oficial</div>
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div style="width: 30%; text-align: center;">
                    <img src="{logo_loc_url}" width="75" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); border-radius: 50%; background: #ffffff10; padding: 5px;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/53/53283.png';">
                    <h3 style="color: white; margin-top: 10px; font-size: 20px;">{eq_loc}</h3>
                </div>
                <div style="width: 40%; text-align: center;">
                    <div style="background: #020617; display: inline-block; padding: 10px 30px; border-radius: 12px; border: 2px solid #0ea5e9; box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);">
                        <span style="font-size: 38px; font-weight: 900; color: #f8fafc; font-family: monospace;">{media_l_estadio} - {media_v_estadio}</span>
                    </div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 8px;">Expectativa de Goles (xG)</div>
                </div>
                <div style="width: 30%; text-align: center;">
                    <img src="{logo_vis_url}" width="75" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); border-radius: 50%; background: #ffffff10; padding: 5px;" onerror="this.src='https://cdn-icons-png.flaticon.com/512/53/53283.png';">
                    <h3 style="color: white; margin-top: 10px; font-size: 20px;">{eq_vis}</h3>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
# ==============================================================================
# --- 2. ANÁLISIS DEL RESULTADO Y MARCADOR MÁS PROBABLE (ESTÉTICA MEJORADA) ---
# ==============================================================================
if 'goles_ft_loc' in locals() and 'goles_ft_vis' in locals():
    st.markdown("### 🏆 Análisis Definitivo del Resultado y Marcador Más Probable")
    
    marcadores_sim = [f"{l}-{v}" for l, v in zip(goles_ft_loc, goles_ft_vis)]
    df_marcadores = pd.Series(marcadores_sim).value_counts(normalize=True) * 100
    top_marcador = df_marcadores.index[0]
    prob_marcador = df_marcadores.iloc[0]
    
    media_l = np.mean(goles_ft_loc)
    media_v = np.mean(goles_ft_vis)
    
    if media_l > media_v:
        veredicto_ganador = f"🔥 **Ganador Predicho:** {eq_loc} (Local)"
    elif media_v > media_l:
        veredicto_ganador = f"🔥 **Ganador Predicho:** {eq_vis} (Visitante)"
    else:
        veredicto_ganador = "🤝 **Pronóstico:** Alta probabilidad de Empate técnico"

    col_an1, col_an2 = st.columns([1.5, 1])
    
    with col_an1:
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.85); padding: 20px; border-radius: 14px; border: 1px solid rgba(56, 189, 248, 0.4); backdrop-filter: blur(10px); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); text-align: center;">
                <h4 style="color: #38bdf8; margin-top: 0; font-size: 18px;">🎯 Veredicto de la IA (Monte Carlo)</h4>
                <p style="font-size: 16px; margin-bottom: 8px; color: #f8fafc;">Marcador más probable:</p>
                <div style="font-size: 28px; font-weight: 900; color: #38bdf8; background: rgba(2, 6, 23, 0.6); padding: 10px; border-radius: 10px; border: 1px solid #0ea5e9; margin: 10px 0;">
                    {eq_loc} {top_marcador} {eq_vis}
                </div>
                <p style="font-size: 14px; color: #cbd5e1;">Probabilidad estadística: <b style="color: #34d399; font-size: 16px;">{prob_marcador:.1f}%</b></p>
                <hr style="border-color: #334155; margin: 12px 0;">
                <p style="font-size: 16px; font-weight: bold; color: #38bdf8; margin-bottom: 0;">{veredicto_ganador}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_an2:
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.85); padding: 20px; border-radius: 14px; border: 1px solid rgba(51, 65, 85, 0.8); backdrop-filter: blur(10px); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); text-align: center;">
                <h4 style="color: #f8fafc; margin-top: 0; font-size: 16px;">📋 Top 3 Marcadores</h4>
        """, unsafe_allow_html=True)
        for m, p in df_marcadores.head(3).items():
            st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.5); padding: 6px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #334155;">
                    <b style='color:#f8fafc; font-size: 15px;'>{m}</b> ➔ <span style='color:#38bdf8; font-weight: bold;'>{p:.1f}%</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# --- 3. PANEL EN VIVO / MEDIO TIEMPO (CON FORMACIONES Y ESTADÍSTICAS MANUALES) ---
# ==============================================================================
st.divider()
st.markdown("### 🔴 Panel En Vivo / Análisis de Medio Tiempo")

with st.container():
    st.markdown("Introduce las formaciones tácticas actuales, los goles y las estadísticas registradas al finalizar el **primer tiempo** para recalcular el resultado final:")
    
    # Selectores manuales de formación dentro del panel en vivo
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        formacion_viva_l = st.selectbox(f"Formación Táctica Actual ({eq_loc}):", ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2", "4-1-4-1"], index=0, key="form_l_vivo")
    with col_form2:
        formacion_viva_v = st.selectbox(f"Formación Táctica Actual ({eq_vis}):", ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2", "4-1-4-1"], index=0, key="form_v_vivo")

    st.markdown("---")
    col_live_a, col_live_b = st.columns(2)
    
    with col_live_a:
        st.markdown(f"#### 🏠 {eq_loc} ({form_l_vivo if 'form_l_vivo' in locals() else '4-3-3'})")
        g_ht_l = st.number_input(f"Goles actuales ({eq_loc}):", 0, 10, 0, key="gh_l_v")
        xg_ht_l = st.number_input(f"xG / Goles Esperados ({eq_loc}):", 0.0, 10.0, 0.75, key="xg_l_v")
        pos_ht_l = st.slider(f"Posesión de Balón % ({eq_loc}):", 0, 100, 50, key="pos_l_v")
        pases_ht_l = st.number_input(f"Pases Completados ({eq_loc}):", 0, 1000, 180, key="pas_l_v")
        grandes_ht_l = st.number_input(f"Grandes Jugadas de Gol ({eq_loc}):", 0, 20, 1, key="gra_l_v")
        corners_ht_l = st.number_input(f"Tiros de Esquina ({eq_loc}):", 0, 20, 3, key="cor_l_v")
        tiros_tot_l = st.number_input(f"Tiros Totales ({eq_loc}):", 0, 30, 6, key="tot_l_v")
        tiros_puerta_l = st.number_input(f"Tiros a Puerta ({eq_loc}):", 0, 20, 2, key="puerta_l_v")

    with col_live_b:
        st.markdown(f"#### ✈️ {eq_vis} ({form_v_vivo if 'form_v_vivo' in locals() else '4-4-2'})")
        g_ht_v = st.number_input(f"Goles actuales ({eq_vis}):", 0, 10, 0, key="gh_v_v")
        xg_ht_v = st.number_input(f"xG / Goles Esperados ({eq_vis}):", 0.0, 10.0, 0.65, key="xg_v_v")
        pos_ht_v = st.slider(f"Posesión de Balón % ({eq_vis}):", 0, 100, 50, key="pos_v_v")
        pases_ht_v = st.number_input(f"Pases Completados ({eq_vis}):", 0, 1000, 160, key="pas_v_v")
        grandes_ht_v = st.number_input(f"Grandes Jugadas de Gol ({eq_vis}):", 0, 20, 1, key="gra_v_v")
        corners_ht_v = st.number_input(f"Tiros de Esquina ({eq_vis}):", 0, 20, 2, key="cor_v_v")
        tiros_tot_v = st.number_input(f"Tiros Totales ({eq_vis}):", 0, 30, 5, key="tot_v_v")
        tiros_puerta_v = st.number_input(f"Tiros a Puerta ({eq_vis}):", 0, 20, 2, key="puerta_v_v")

    if st.button("⚡ Ejecutar Proyección Científica en Vivo (2do Tiempo)", use_container_width=True):
        factor_dinamico_l = 1.0 + ((tiros_puerta_l - tiros_puerta_v) * 0.04) + ((xg_ht_l - xg_ht_v) * 0.05)
        factor_dinamico_v = 1.0 + ((tiros_puerta_v - tiros_puerta_l) * 0.04) + ((xg_ht_v - xg_ht_l) * 0.05)
        
        sims_vivos = 10000
        goles_2t_l = np.random.poisson(max(0.1, 1.1 * max(0.5, factor_dinamico_l)), sims_vivos)
        goles_2t_v = np.random.poisson(max(0.1, 0.9 * max(0.5, factor_dinamico_v)), sims_vivos)
        
        goles_totales_final_l = g_ht_l + goles_2t_l
        goles_totales_final_v = g_ht_v + goles_2t_v
        
        p_l_live = np.mean(goles_totales_final_l > goles_totales_final_v) * 100
        p_v_live = np.mean(goles_totales_final_l < goles_totales_final_v) * 100
        p_e_live = np.mean(goles_totales_final_l == goles_totales_final_v) * 100
        
        media_fin_l = np.mean(goles_totales_final_l)
        media_fin_v = np.mean(goles_totales_final_v)
        
        st.markdown("---")
        st.markdown("### 📊 Resultado Proyectado en Tiempo Real (Final del Partido)")
        
        col_res_l1, col_res_l2, col_res_l3 = st.columns(3)
        col_res_l1.metric(f"Victoria {eq_loc}", f"{p_l_live:.1f}%", f"Prom: {media_fin_l:.1f} goles")
        col_res_l2.metric("Empate Final", f"{p_e_live:.1f}%")
        col_res_l3.metric(f"Victoria {eq_vis}", f"{p_v_live:.1f}%", f"Prom: {media_fin_v:.1f} goles")

import matplotlib.pyplot as plt

# ==============================================================================
# --- MÓDULOS AVANZADOS (SISTEMA DE MATRIZ, NARRACIÓN Y ANÁLISIS) ---
# ==============================================================================

# --- MATRIZ TÉRMICA DE MARCADORES (CON MATPLOTLIB) ---
def generar_matriz_calor_marcadores(goles_loc, goles_vis, max_goles=5):
    matriz = np.zeros((max_goles + 1, max_goles + 1))
    N = len(goles_loc)
    for l, v in zip(goles_loc, goles_vis):
        if l <= max_goles and v <= max_goles:
            matriz[l, v] += 1
    matriz = (matriz / N) * 100
    
    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(matriz, cmap='viridis')
    fig.colorbar(cax)
    
    ax.set_xticks(range(max_goles + 1))
    ax.set_yticks(range(max_goles + 1))
    ax.set_xlabel('Goles Visitante', color='white', fontsize=11)
    ax.set_ylabel('Goles Local', color='white', fontsize=11)
    ax.set_title('🔥 Matriz Térmica de Marcadores Exactos (%)', color='white', pad=15, fontsize=12, fontweight='bold')
    
    for i in range(max_goles + 1):
        for j in range(max_goles + 1):
            ax.text(j, i, f"{matriz[i, j]:.1f}%", ha='center', va='center', color='white', fontsize=9, fontweight='bold')
            
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.tick_params(colors='white')
    plt.tight_layout()
    return fig

# --- GENERADOR DE RELATO Y NARRACIÓN DEL PARTIDO ---
def generar_relato_partido(eq_loc, eq_vis, g_loc, g_vis, estilo_loc, estilo_vis, al_loc, al_vis):
    minutos_gol_loc = sorted(np.random.randint(5, 88, size=g_loc)) if g_loc > 0 else []
    minutos_gol_vis = sorted(np.random.randint(5, 88, size=g_vis)) if g_vis > 0 else []
    
    jugadores_loc = [j.strip() for j in al_loc.split(",") if j.strip()]
    jugadores_vis = [j.strip() for j in al_vis.split(",") if j.strip()]
    
    del_loc = jugadores_loc[-1] if len(jugadores_loc) > 0 else "el delantero local"
    del_vis = jugadores_vis[-1] if len(jugadores_vis) > 0 else "el delantero visitante"
    med_loc = jugadores_loc[len(jugadores_loc)//2] if len(jugadores_loc) > 1 else "el mediocampista"
    med_vis = jugadores_vis[len(jugadores_vis)//2] if len(jugadores_vis) > 1 else "el mediocampista"
    
    relato = []
    relato.append(f"⏱️ **0'**: ¡Arranca el partido! **{eq_loc}** ({estilo_loc}) vs **{eq_vis}** ({estilo_vis}). Se siente la tensión táctica desde el primer minuto.")
    
    eventos = []
    for m in minutos_gol_loc:
        eventos.append((m, f"⚽ **{m}' ¡GOOOOL DE {eq_loc}!** Asistencia magistral de {med_loc} para que **{del_loc}** defina al fondo de la red."))
    for m in minutos_gol_vis:
        eventos.append((m, f"⚽ **{m}' ¡GOOOOL DE {eq_vis}!** Contraataque letal conducido por {med_vis} que culmina en gol de **{del_vis}**."))
    
    eventos.append((45, f"⏸️ **45'**: Final del Primer Tiempo. Los técnicos ajustan la estrategia en vestuarios."))
    eventos.sort(key=lambda x: x[0])
    
    for _, txt in eventos:
        relato.append(txt)
        
    relato.append(f"🏁 **90'**: ¡Pitazo final! Resultado definitivo: **{eq_loc} {g_loc} - {g_vis} {eq_vis}**.")
    return relato


# ==============================================================================
# --- ESTRUCTURA PRINCIPAL DE PESTAÑAS ---
# ==============================================================================

p1, p2, p3, p4 = st.tabs([
    "🚀 Simulación & Live", 
    "🏟️ Alineaciones & Narración", 
    "📊 Inteligencia Avanzada & Apuestas", 
    "📜 Historial & Backtesting"
])

# ------------------------------------------------------------------------------
# PESTAÑA 2: ALINEACIONES Y NARRACIÓN DEL PARTIDO
# ------------------------------------------------------------------------------
with p2:
    st.subheader("🏟️ Búnker Táctico: Alineaciones, Esquemas y Narración IA")
    col_t1, col_t2 = st.columns(2)
    
    eq_l_nombre = eq_loc if 'eq_loc' in locals() else 'Equipo Local'
    eq_v_nombre = eq_vis if 'eq_vis' in locals() else 'Equipo Visitante'
    
    with col_t1:
        st.markdown(f"### 🏠 {eq_l_nombre}")
        estilo_loc = st.selectbox("Esquema Táctico del DT (Local):", [
            "4-3-3 Posesión y Presión Alta", 
            "4-4-2 Bloque Medio y Transición", 
            "3-5-2 Posesión y Juego de Bandas", 
            "5-3-2 Bloque Bajo y Contraataque"
        ], key="est_loc_tab")
        alineacion_loc = st.text_area("Alineación Titular (Separa los 11 jugadores por comas):", 
                                      "Portero, Def1, Def2, Def3, Def4, Med1, Med2, Med3, Del1, Del2, Del3", key="alin_loc_tab")
        
    with col_t2:
        st.markdown(f"### ✈️ {eq_v_nombre}")
        estilo_vis = st.selectbox("Esquema Táctico del DT (Visitante):", [
            "4-3-3 Posesión y Presión Alta", 
            "4-4-2 Bloque Medio y Transición", 
            "3-5-2 Posesión y Juego de Bandas", 
            "5-3-2 Bloque Bajo y Contraataque"
        ], key="est_vis_tab")
        alineacion_vis = st.text_area("Alineación Titular (Separa los 11 jugadores por comas):", 
                                      "Portero, Def1, Def2, Def3, Def4, Med1, Med2, Med3, Del1, Del2, Del3", key="alin_vis_tab")

    if st.button("🎙️ Generar Resumen Narrativo del Partido", use_container_width=True):
        if 'goles_ft_loc' in locals():
            g_sim_l = int(np.round(np.mean(goles_ft_loc)))
            g_sim_v = int(np.round(np.mean(goles_ft_vis)))
            
            comentarios = generar_relato_partido(eq_l_nombre, eq_v_nombre, g_sim_l, g_sim_v, estilo_loc, estilo_vis, alineacion_loc, alineacion_vis)
            
            st.markdown("---")
            st.markdown("#### 📜 Transmisión y Minuto a Minuto del Partido:")
            for c in comentarios:
                st.write(c)
        else:
            st.warning("⚠️ Primero ejecuta la simulación en la Pestaña 1 para obtener los marcadores del partido.")

# ------------------------------------------------------------------------------
# PESTAÑA 3: INTELIGENCIA AVANZADA, CONTEXTO DE TORNEO Y APUESTAS DE VALOR
# ------------------------------------------------------------------------------
with p3:
    st.subheader("📊 Centro de Inteligencia Deportivo, Tabla & Apuestas de Valor")
    
    st.markdown("### 🏆 Contexto de Torneo & Necesidad de Puntos")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pts_loc = st.number_input(f"Puntos actuales ({eq_l_nombre}):", 0, 120, 45, key="pts_l")
        pos_loc = st.number_input(f"Posición en la Tabla ({eq_l_nombre}):", 1, 20, 2, key="pos_l_tab")
    with col_p2:
        pts_vis = st.number_input(f"Puntos actuales ({eq_v_nombre}):", 0, 120, 42, key="pts_v")
        pos_vis = st.number_input(f"Posición en la Tabla ({eq_v_nombre}):", 1, 20, 4, key="pos_v_tab")

    obj_loc = "Lucha por el Título" if pos_loc <= 2 else ("Puestos de Champions / Copas" if pos_loc <= 5 else ("Peligro de Descenso" if pos_loc >= 17 else "Zona Media"))
    obj_vis = "Lucha por el Título" if pos_vis <= 2 else ("Puestos de Champions / Copas" if pos_vis <= 5 else ("Peligro de Descenso" if pos_vis >= 17 else "Zona Media"))
    
    st.info(f"📌 **Contexto del Partido:**\n\n"
            f"• **{eq_l_nombre}**: {pts_loc} pts (Posición #{pos_loc}) ➔ **Objetivo:** {obj_loc}\n\n"
            f"• **{eq_v_nombre}**: {pts_vis} pts (Posición #{pos_vis}) ➔ **Objetivo:** {obj_vis}")

    st.divider()

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("#### 🧮 Comparador de Cuotas (Value Bet Finder)")
        cuota_loc = st.number_input(f"Cuota Victoria Local ({eq_l_nombre}):", 1.01, 20.0, 2.10)
        
    with col_v2:
        st.markdown("#### ⚡ Calculadora de Volatilidad")
        volatilidad = "Alta 🔥" if abs(pts_loc - pts_vis) <= 3 else "Moderada ⚖️"
        st.metric("Nivel de Volatilidad del Partido", volatilidad)

    if 'goles_ft_loc' in locals():
        fig_heat = generar_matriz_calor_marcadores(goles_ft_loc, goles_ft_vis)
        st.pyplot(fig_heat)
        
        prob_implicita_cuota = (1 / cuota_loc) * 100
        prob_modelo = np.mean(goles_ft_loc > goles_ft_vis) * 100
        edge = prob_modelo - prob_implicita_cuota
        
        if edge > 5.0:
            st.success(f"🔥 **¡APUESTA CON ALTO VALOR (EDGE POSITIVO)!**\n\n"
                       f"Probabilidad de tu Modelo: **{prob_modelo:.1f}%** vs Probabilidad de la Cuota: **{prob_implicita_cuota:.1f}%** (Ventaja: **+{edge:.1f}%**)")
        else:
            st.info(f"⚖️ **Cuota Sin Ventaja Clara:** Probabilidad del Modelo: **{prob_modelo:.1f}%** vs Probabilidad de la Cuota: **{prob_implicita_cuota:.1f}%** (Diferencia: {edge:.1f}%)")

# ------------------------------------------------------------------------------
# PESTAÑA 4: HISTORIAL Y PERFORMANCE DE MODELO
# ------------------------------------------------------------------------------
with p4:
    st.subheader("📜 Rendimiento Histórico y Registros de Pronósticos")
    st.dataframe(st.session_state.historial_df, use_container_width=True)


