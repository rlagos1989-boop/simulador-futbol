import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime

st.set_page_config(page_title="Predictor & Tracker de Fútbol Pro (2026/2027)", layout="wide")

ARCH_HISTORIAL = "registro_pronosticos.csv"

# ==============================================================================
# 1. FUENTES DE DATOS - AUTO-ACTUALIZABLES Y DICCIORARIOS COMPLETOS 2026/2027
# ==============================================================================

# Ligas con servidores CSV de actualización diaria en vivo (Código de temporada 2627)
LIGAS_AUTO = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League 26/27": "https://www.football-data.co.uk/mmz4281/2627/E0.csv",
    "🇪🇸 LaLiga Española 26/27": "https://www.football-data.co.uk/mmz4281/2627/SP1.csv",
    "🇮🇹 Serie A 26/27": "https://www.football-data.co.uk/mmz4281/2627/I1.csv",
    "🇩🇪 Bundesliga 26/27": "https://www.football-data.co.uk/mmz4281/2627/D1.csv",
    "🇫🇷 Ligue 1 26/27": "https://www.football-data.co.uk/mmz4281/2627/F1.csv"
}

# Ligas y Torneos con planteles y métricas completas para 2026/2027
LIGAS_ESTATICAS = {
    "🇪🇺 UEFA Champions League (2026/27)": {
        "Arsenal": {"pj": 8, "gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6},
        "Aston Villa": {"pj": 8, "gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.1},
        "Liverpool": {"pj": 8, "gf": 2.40, "gc": 0.88, "gf1t": 1.15, "corners": 7.0, "tarjetas": 1.6},
        "Manchester City": {"pj": 8, "gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4},
        "Manchester United": {"pj": 8, "gf": 1.80, "gc": 1.18, "gf1t": 0.78, "corners": 5.8, "tarjetas": 2.0},
        "Lille": {"pj": 8, "gf": 1.75, "gc": 1.00, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.0},
        "PSG": {"pj": 8, "gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8},
        "Napoli": {"pj": 8, "gf": 1.90, "gc": 0.95, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.0},
        "LASK": {"pj": 8, "gf": 1.50, "gc": 1.25, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2},
        "Slavia Praga": {"pj": 8, "gf": 1.95, "gc": 0.88, "gf1t": 0.88, "corners": 5.8, "tarjetas": 2.1},
        "Club Brujas": {"pj": 8, "gf": 1.88, "gc": 1.05, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.1},
        "Lens": {"pj": 8, "gf": 1.68, "gc": 1.02, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.1},
        "Slovan Bratislava": {"pj": 8, "gf": 1.45, "gc": 1.58, "gf1t": 0.58, "corners": 4.4, "tarjetas": 2.5},
        "Bayern Múnich": {"pj": 8, "gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5},
        "Borussia Dortmund": {"pj": 8, "gf": 2.10, "gc": 1.18, "gf1t": 0.95, "corners": 5.9, "tarjetas": 2.0},
        "AS Roma": {"pj": 8, "gf": 1.70, "gc": 1.10, "gf1t": 0.68, "corners": 5.5, "tarjetas": 2.3},
        "Inter de Milán": {"pj": 8, "gf": 2.18, "gc": 0.68, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.7},
        "PSV Eindhoven": {"pj": 8, "gf": 2.45, "gc": 0.85, "gf1t": 1.18, "corners": 6.6, "tarjetas": 1.5},
        "Feyenoord": {"pj": 8, "gf": 2.05, "gc": 1.02, "gf1t": 0.92, "corners": 6.1, "tarjetas": 1.8},
        "Real Madrid": {"pj": 8, "gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7},
        "Villarreal": {"pj": 8, "gf": 1.82, "gc": 1.15, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2},
        "FC Barcelona": {"pj": 8, "gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9},
        "Atlético de Madrid": {"pj": 8, "gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
        "Real Betis": {"pj": 8, "gf": 1.72, "gc": 1.02, "gf1t": 0.72, "corners": 5.5, "tarjetas": 2.2},
        "FC Porto": {"pj": 8, "gf": 2.10, "gc": 0.85, "gf1t": 0.98, "corners": 6.1, "tarjetas": 2.1},
        "VfB Stuttgart": {"pj": 8, "gf": 1.90, "gc": 1.28, "gf1t": 0.82, "corners": 5.6, "tarjetas": 1.9},
        "AEK Atenas": {"pj": 8, "gf": 1.65, "gc": 1.15, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.4},
        "Viking FK": {"pj": 8, "gf": 1.58, "gc": 1.32, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.0},
        "Bodø/Glimt": {"pj": 8, "gf": 2.02, "gc": 1.22, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.7},
        "Sporting CP": {"pj": 8, "gf": 2.25, "gc": 0.82, "gf1t": 1.08, "corners": 6.3, "tarjetas": 1.8},
        "Galatasaray": {"pj": 8, "gf": 2.22, "gc": 1.12, "gf1t": 1.02, "corners": 6.2, "tarjetas": 2.5},
        "Fenerbahçe": {"pj": 8, "gf": 2.12, "gc": 0.98, "gf1t": 0.98, "corners": 6.0, "tarjetas": 2.4},
        "Shakhtar Donetsk": {"pj": 8, "gf": 1.80, "gc": 1.15, "gf1t": 0.78, "corners": 5.2, "tarjetas": 2.0},
        "Como 1907": {"pj": 8, "gf": 1.48, "gc": 1.35, "gf1t": 0.62, "corners": 4.8, "tarjetas": 2.2},
        "RB Leipzig": {"pj": 8, "gf": 2.00, "gc": 1.08, "gf1t": 0.90, "corners": 5.8, "tarjetas": 1.9},
        "Sabah Bakú": {"pj": 8, "gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.6}
    },
    "🇪🇺 UEFA Europa League (2026/27)": {
        "Hapoel Beer Sheva": {"pj": 8, "gf": 1.42, "gc": 1.30, "gf1t": 0.58, "corners": 4.5, "tarjetas": 2.5},
        "Sunderland": {"pj": 8, "gf": 1.55, "gc": 1.25, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.1},
        "Crystal Palace": {"pj": 8, "gf": 1.62, "gc": 1.20, "gf1t": 0.68, "corners": 5.2, "tarjetas": 2.0},
        "Bournemouth": {"pj": 8, "gf": 1.68, "gc": 1.28, "gf1t": 0.72, "corners": 5.4, "tarjetas": 2.2},
        "Real Sociedad": {"pj": 8, "gf": 1.48, "gc": 1.05, "gf1t": 0.65, "corners": 5.5, "tarjetas": 2.1},
        "Celta Vigo": {"pj": 8, "gf": 1.60, "gc": 1.30, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.3},
        "Salzburgo": {"pj": 8, "gf": 1.95, "gc": 1.20, "gf1t": 0.88, "corners": 5.8, "tarjetas": 1.9},
        "Sturm Graz": {"pj": 8, "gf": 1.60, "gc": 1.30, "gf1t": 0.68, "corners": 4.9, "tarjetas": 2.3},
        "Viktoria Plzen": {"pj": 8, "gf": 1.62, "gc": 1.08, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.2},
        "Sparta Praga": {"pj": 8, "gf": 1.75, "gc": 1.20, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.3},
        "Anderlecht": {"pj": 8, "gf": 1.68, "gc": 1.12, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.1},
        "Union Saint-Gilloise": {"pj": 8, "gf": 1.58, "gc": 1.18, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.3},
        "Marseille": {"pj": 8, "gf": 1.95, "gc": 1.15, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.4},
        "Rennes": {"pj": 8, "gf": 1.70, "gc": 1.20, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.1},
        "Lyon": {"pj": 8, "gf": 1.82, "gc": 1.22, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2},
        "Bayer Leverkusen": {"pj": 8, "gf": 2.20, "gc": 0.92, "gf1t": 1.02, "corners": 6.2, "tarjetas": 1.9},
        "Hoffenheim": {"pj": 8, "gf": 1.85, "gc": 1.35, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.2},
        "Juventus": {"pj": 8, "gf": 1.80, "gc": 0.68, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.0},
        "AC Milan": {"pj": 8, "gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.2},
        "Nijmegen": {"pj": 8, "gf": 1.45, "gc": 1.35, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.0},
        "AZ Alkmaar": {"pj": 8, "gf": 1.88, "gc": 1.10, "gf1t": 0.82, "corners": 5.7, "tarjetas": 1.9},
        "Torreense": {"pj": 8, "gf": 1.25, "gc": 1.48, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.5},
        "Levski Sofía": {"pj": 8, "gf": 1.40, "gc": 1.32, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.4},
        "Dinamo Zagreb": {"pj": 8, "gf": 1.85, "gc": 1.25, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.2},
        "Omonia": {"pj": 8, "gf": 1.42, "gc": 1.28, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.6},
        "OFI Creta": {"pj": 8, "gf": 1.35, "gc": 1.42, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.6},
        "Olympiacos Piraeus": {"pj": 8, "gf": 1.78, "gc": 0.98, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.3},
        "Lillestrom": {"pj": 8, "gf": 1.48, "gc": 1.38, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.1},
        "Jagiellonia": {"pj": 8, "gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.3},
        "Lech Poznan": {"pj": 8, "gf": 1.62, "gc": 1.20, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.2},
        "Benfica": {"pj": 8, "gf": 2.10, "gc": 0.88, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.9},
        "Celtic": {"pj": 8, "gf": 2.25, "gc": 1.10, "gf1t": 1.02, "corners": 6.4, "tarjetas": 1.6},
        "Celje": {"pj": 8, "gf": 1.42, "gc": 1.38, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.3},
        "Besiktas": {"pj": 8, "gf": 1.78, "gc": 1.18, "gf1t": 0.78, "corners": 5.5, "tarjetas": 2.3},
        "Ferencvaros": {"pj": 8, "gf": 1.58, "gc": 1.22, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.4},
        "Ararat-Armenia": {"pj": 8, "gf": 1.25, "gc": 1.50, "gf1t": 0.48, "corners": 4.1, "tarjetas": 2.6}
    },
    "🇪🇺 UEFA Conference League (2026/27)": {
        "Mjallby": {"pj": 6, "gf": 1.38, "gc": 1.28, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.0},
        "Brighton": {"pj": 6, "gf": 1.88, "gc": 1.25, "gf1t": 0.82, "corners": 5.8, "tarjetas": 2.0},
        "Mónaco": {"pj": 6, "gf": 1.95, "gc": 1.10, "gf1t": 0.88, "corners": 5.6, "tarjetas": 2.1},
        "Jablonec": {"pj": 6, "gf": 1.32, "gc": 1.40, "gf1t": 0.52, "corners": 4.3, "tarjetas": 2.4},
        "Caballero": {"pj": 6, "gf": 1.45, "gc": 1.35, "gf1t": 0.58, "corners": 4.7, "tarjetas": 2.3},
        "San Truiden": {"pj": 6, "gf": 1.40, "gc": 1.38, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.2},
        "Friburgo": {"pj": 6, "gf": 1.72, "gc": 1.18, "gf1t": 0.72, "corners": 5.4, "tarjetas": 1.9},
        "Atalanta": {"pj": 6, "gf": 2.15, "gc": 1.00, "gf1t": 1.00, "corners": 6.1, "tarjetas": 2.0},
        "Ajax": {"pj": 6, "gf": 2.02, "gc": 1.05, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.8},
        "Twente": {"pj": 6, "gf": 1.72, "gc": 1.18, "gf1t": 0.72, "corners": 5.4, "tarjetas": 2.0},
        "Getafe": {"pj": 6, "gf": 1.30, "gc": 1.10, "gf1t": 0.52, "corners": 4.6, "tarjetas": 2.8},
        "KuPS": {"pj": 6, "gf": 1.32, "gc": 1.38, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.1},
        "CSKA Sofía": {"pj": 6, "gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.5},
        "Hajduk Split": {"pj": 6, "gf": 1.52, "gc": 1.25, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.3},
        "Pafos": {"pj": 6, "gf": 1.48, "gc": 1.18, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.5},
        "Aarhus": {"pj": 6, "gf": 1.42, "gc": 1.30, "gf1t": 0.58, "corners": 4.7, "tarjetas": 2.1},
        "FC Copenhague": {"pj": 6, "gf": 1.82, "gc": 1.08, "gf1t": 0.78, "corners": 5.6, "tarjetas": 1.9},
        "Midtjylland": {"pj": 6, "gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.2},
        "Nordsjaelland": {"pj": 6, "gf": 1.78, "gc": 1.28, "gf1t": 0.78, "corners": 5.5, "tarjetas": 1.8},
        "Panathinaikos": {"pj": 6, "gf": 1.58, "gc": 1.08, "gf1t": 0.68, "corners": 5.2, "tarjetas": 2.5},
        "Brann": {"pj": 6, "gf": 1.62, "gc": 1.28, "gf1t": 0.68, "corners": 5.2, "tarjetas": 1.9},
        "Braga": {"pj": 6, "gf": 1.82, "gc": 1.18, "gf1t": 0.78, "corners": 5.6, "tarjetas": 2.2},
        "Copas": {"pj": 6, "gf": 1.38, "gc": 1.32, "gf1t": 0.58, "corners": 4.9, "tarjetas": 2.4},
        "Lugano": {"pj": 6, "gf": 1.52, "gc": 1.28, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2},
        "Crvena Zvezda": {"pj": 6, "gf": 1.90, "gc": 1.35, "gf1t": 0.82, "corners": 5.5, "tarjetas": 2.4},
        "Thun": {"pj": 6, "gf": 1.45, "gc": 1.35, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.1},
        "Trabzonspor": {"pj": 6, "gf": 1.68, "gc": 1.22, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.5},
        "Borac Banja Luka": {"pj": 6, "gf": 1.22, "gc": 1.38, "gf1t": 0.48, "corners": 4.2, "tarjetas": 2.6},
        "Kairat Almaty": {"pj": 6, "gf": 1.35, "gc": 1.40, "gf1t": 0.52, "corners": 4.3, "tarjetas": 2.3},
        "Egnatia": {"pj": 6, "gf": 1.18, "gc": 1.45, "gf1t": 0.45, "corners": 4.0, "tarjetas": 2.6},
        "Inter Escaldes": {"pj": 6, "gf": 1.12, "gc": 1.55, "gf1t": 0.42, "corners": 3.8, "tarjetas": 2.7},
        "Kauno Zalgiris": {"pj": 6, "gf": 1.20, "gc": 1.48, "gf1t": 0.45, "corners": 4.1, "tarjetas": 2.4},
        "Universidad de Craiova": {"pj": 6, "gf": 1.48, "gc": 1.28, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.4},
        "Iberia 1999": {"pj": 6, "gf": 1.25, "gc": 1.42, "gf1t": 0.48, "corners": 4.1, "tarjetas": 2.5},
        "Lincoln Red Imps": {"pj": 6, "gf": 1.08, "gc": 1.60, "gf1t": 0.40, "corners": 3.7, "tarjetas": 2.8},
        "Riga FC": {"pj": 6, "gf": 1.32, "gc": 1.48, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.5}
    },
    "🇲🇽 Liga MX (Apertura 2026 / Clausura 2027)": {
        "Club América": {"pj": 8, "gf": 2.10, "gc": 0.90, "gf1t": 1.10, "corners": 6.3, "tarjetas": 2.2},
        "Guadalajara Chivas": {"pj": 8, "gf": 1.85, "gc": 1.00, "gf1t": 0.90, "corners": 6.0, "tarjetas": 2.3},
        "Cruz Azul": {"pj": 8, "gf": 1.95, "gc": 0.85, "gf1t": 1.00, "corners": 6.2, "tarjetas": 2.1},
        "Tigres UANL": {"pj": 8, "gf": 2.00, "gc": 1.05, "gf1t": 1.05, "corners": 6.2, "tarjetas": 2.2},
        "Monterrey Rayados": {"pj": 8, "gf": 2.15, "gc": 0.95, "gf1t": 1.10, "corners": 6.5, "tarjetas": 2.0},
        "Pumas UNAM": {"pj": 8, "gf": 1.70, "gc": 1.25, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.4},
        "Deportivo Toluca": {"pj": 8, "gf": 2.20, "gc": 1.10, "gf1t": 1.15, "corners": 6.4, "tarjetas": 2.1},
        "Pachuca FC": {"pj": 8, "gf": 1.65, "gc": 1.30, "gf1t": 0.75, "corners": 6.0, "tarjetas": 2.5},
        "Club León": {"pj": 8, "gf": 1.60, "gc": 1.35, "gf1t": 0.80, "corners": 5.9, "tarjetas": 2.3},
        "Santos Laguna": {"pj": 8, "gf": 1.45, "gc": 1.50, "gf1t": 0.70, "corners": 5.5, "tarjetas": 2.6},
        "Atlas FC": {"pj": 8, "gf": 1.40, "gc": 1.45, "gf1t": 0.65, "corners": 5.6, "tarjetas": 2.4},
        "Club Necaxa": {"pj": 8, "gf": 1.35, "gc": 1.40, "gf1t": 0.60, "corners": 5.3, "tarjetas": 2.2},
        "Club Puebla": {"pj": 8, "gf": 1.25, "gc": 1.60, "gf1t": 0.55, "corners": 5.1, "tarjetas": 2.5},
        "Club Tijuana (Xolos)": {"pj": 8, "gf": 1.30, "gc": 1.55, "gf1t": 0.60, "corners": 5.2, "tarjetas": 2.6},
        "Querétaro FC": {"pj": 8, "gf": 1.15, "gc": 1.65, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.5},
        "Atlético San Luis": {"pj": 8, "gf": 1.40, "gc": 1.50, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.3},
        "FC Juárez (Bravos)": {"pj": 8, "gf": 1.20, "gc": 1.70, "gf1t": 0.50, "corners": 4.9, "tarjetas": 2.7},
        "Atlante FC": {"pj": 8, "gf": 1.10, "gc": 1.60, "gf1t": 0.45, "corners": 4.7, "tarjetas": 2.4}
    },
    "🇸🇦 Saudi Pro League 2026/2027 (18 Equipos)": {
        "Al-Hilal FC": {"pj": 7, "gf": 3.28, "gc": 0.71, "gf1t": 1.40, "corners": 6.9, "tarjetas": 1.6},
        "Ittihad FC": {"pj": 7, "gf": 1.71, "gc": 0.86, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.2},
        "Al-Nassr FC": {"pj": 7, "gf": 2.28, "gc": 1.00, "gf1t": 1.10, "corners": 6.3, "tarjetas": 2.0},
        "Al-Qadisiya": {"pj": 7, "gf": 2.28, "gc": 1.14, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.3},
        "NEOM SC": {"pj": 7, "gf": 1.85, "gc": 0.86, "gf1t": 0.90, "corners": 5.5, "tarjetas": 2.1},
        "Al-Ahli Saudi FC": {"pj": 7, "gf": 2.28, "gc": 1.42, "gf1t": 1.00, "corners": 5.7, "tarjetas": 2.4},
        "Al-Kholood Club": {"pj": 7, "gf": 1.71, "gc": 1.42, "gf1t": 0.75, "corners": 4.8, "tarjetas": 2.5},
        "Al Draih": {"pj": 7, "gf": 1.00, "gc": 0.71, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.3},
        "Al-Ettifaq": {"pj": 7, "gf": 1.57, "gc": 1.57, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.2},
        "Al-Hazm": {"pj": 7, "gf": 1.00, "gc": 1.28, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6},
        "Al-Riyadh": {"pj": 7, "gf": 1.14, "gc": 2.28, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.5},
        "Al-Fayha": {"pj": 7, "gf": 1.00, "gc": 1.57, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.4},
        "Al Khaleej Club": {"pj": 7, "gf": 0.43, "gc": 1.42, "gf1t": 0.20, "corners": 3.8, "tarjetas": 2.6},
        "Al-Shabab": {"pj": 7, "gf": 0.86, "gc": 1.57, "gf1t": 0.35, "corners": 4.6, "tarjetas": 2.7},
        "Al-Fateh": {"pj": 7, "gf": 0.57, "gc": 1.57, "gf1t": 0.25, "corners": 4.2, "tarjetas": 2.4},
        "Al-Faisaly": {"pj": 7, "gf": 0.71, "gc": 1.85, "gf1t": 0.30, "corners": 3.9, "tarjetas": 2.5},
        "Al-Taawoun FC": {"pj": 7, "gf": 0.43, "gc": 1.71, "gf1t": 0.20, "corners": 4.1, "tarjetas": 2.3},
        "Abha Club": {"pj": 7, "gf": 0.71, "gc": 1.85, "gf1t": 0.30, "corners": 3.7, "tarjetas": 2.8}
    },
    "🇭🇳 Liga Nacional Honduras (Apertura 2026 - 12 Equipos)": {
        "CD Olimpia": {"pj": 7, "gf": 2.20, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 2.3},
        "FC Motagua": {"pj": 7, "gf": 1.90, "gc": 1.00, "gf1t": 0.85, "corners": 5.4, "tarjetas": 2.5},
        "Real España": {"pj": 7, "gf": 1.85, "gc": 0.90, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.2},
        "CD Marathón": {"pj": 7, "gf": 1.70, "gc": 0.95, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.6},
        "Olancho FC": {"pj": 7, "gf": 1.30, "gc": 1.15, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
        "Génesis FC": {"pj": 7, "gf": 1.20, "gc": 1.30, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.4},
        "Juticalpa FC": {"pj": 7, "gf": 1.10, "gc": 1.40, "gf1t": 0.45, "corners": 4.1, "tarjetas": 2.5},
        "Lobos UPNFM": {"pj": 7, "gf": 1.15, "gc": 1.65, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.4},
        "Platense FC": {"pj": 7, "gf": 1.25, "gc": 1.45, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.7},
        "CD Choloma": {"pj": 7, "gf": 1.05, "gc": 1.60, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.6},
        "CD Estrella Roja": {"pj": 7, "gf": 1.35, "gc": 1.70, "gf1t": 0.55, "corners": 4.2, "tarjetas": 2.8},
        "CA Independiente Siguatepeque": {"pj": 7, "gf": 1.15, "gc": 1.50, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5}
    }
}

@st.cache_data(ttl=21600) # Se recalcula automáticamente cada 6 horas
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

            stats[eq] = {
                "pj": pj,
                "gf": round(gf / pj, 2),
                "gc": round(gc / pj, 2),
                "gf1t": round(gf1t / pj, 2),
                "corners": round(corners / pj, 2),
                "tarjetas": round(tarjetas / pj, 2)
            }
        return stats
    except Exception:
        st.warning(f"Descargando datos base para {nombre_torneo}...")
        return {}

# ==============================================================================
# 2. MANEJO DEL ARCHIVO HISTORIAL (CSV PERSISTENTE)
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
# 3. INTERFAZ DE USUARIO Y CONTROL
# ==============================================================================

st.title("⚽ Predictor & Tracker de Apuestas Pro (2026/2027)")

pestana1, pestana2 = st.tabs(["📊 Análisis y Pronósticos", "📜 Historial (Acertó / Falló)"])

todas_las_ligas = list(LIGAS_AUTO.keys()) + list(LIGAS_ESTATICAS.keys())

with pestana1:
    liga_sel = st.selectbox("Seleccionar Torneo / Liga:", todas_las_ligas)

    with st.spinner("Cargando métricas de la temporada 2026/2027..."):
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

        st.subheader(f"📈 Métricas de Referencia 2026/2027: {eq_loc} vs {eq_vis}")

        c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns(5)
        c_m1.metric(f"Partidos ({eq_loc})", f"{d_loc['pj']}")
        c_m2.metric(f"Goles Prom. {eq_loc}", f"{d_loc['gf']}")
        c_m3.metric(f"Goles Prom. {eq_vis}", f"{d_vis['gf']}")
        c_m4.metric("Córners Esperados", f"{round(d_loc['corners'] + d_vis['corners'], 1)}")
        c_m5.metric("Tarjetas Esperadas", f"{round(d_loc['tarjetas'] + d_vis['tarjetas'], 1)}")

        st.divider()
        st.subheader("📝 Guardar Pronóstico para Seguimiento")

        with st.form("form_guardar_pronostico"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                pronostico = st.selectbox("Predicción / Mercado:", [
                    f"Gana {eq_loc}",
                    f"Gana {eq_vis}",
                    "Empate",
                    "Over 2.5 Goles",
                    "Under 2.5 Goles",
                    "Ambos Anotan (Sí)",
                    "Over 8.5 Córners",
                    "Over 9.5 Córners",
                    "Over 4.5 Tarjetas"
                ])
            with c_p2:
                estado_inicial = st.selectbox("Estado del Encuentro:", ["⏳ Pendiente", "✅ Acertado", "❌ Fallado"])

            btn_guardar = st.form_submit_button("💾 Guardar Registro en Archivo CSV")

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

