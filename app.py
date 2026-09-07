import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Simulador Predictivo de Fútbol Ultra Pro 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base de datos completa con los equipos exactos de tus tablas, UEFA y Leagues Cup
BASE_DATOS = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (2026/27)": {
        "Arsenal": {"gf": 2.20, "gc": 0.80, "gf1t": 1.10, "corners": 6.5, "tarjetas": 1.8},
        "Aston Villa": {"gf": 1.80, "gc": 1.30, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.4},
        "Chelsea": {"gf": 1.75, "gc": 1.30, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.5},
        "Everton": {"gf": 1.20, "gc": 1.40, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.3},
        "Fulham": {"gf": 1.40, "gc": 1.40, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
        "Liverpool": {"gf": 2.30, "gc": 1.00, "gf1t": 1.05, "corners": 6.9, "tarjetas": 1.7},
        "Manchester City": {"gf": 2.40, "gc": 0.85, "gf1t": 1.20, "corners": 7.1, "tarjetas": 1.5},
        "Manchester Utd": {"gf": 1.55, "gc": 1.35, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.2},
        "Newcastle": {"gf": 1.75, "gc": 1.25, "gf1t": 0.75, "corners": 5.6, "tarjetas": 2.1},
        "Sunderland": {"gf": 1.25, "gc": 1.50, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.4},
        "Tottenham": {"gf": 1.90, "gc": 1.45, "gf1t": 0.85, "corners": 6.1, "tarjetas": 2.3},
        "Coventry": {"gf": 1.15, "gc": 1.55, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Crystal Palace": {"gf": 1.30, "gc": 1.40, "gf1t": 0.45, "corners": 4.5, "tarjetas": 2.1},
        "Hull": {"gf": 1.10, "gc": 1.60, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.6},
        "Ipswich": {"gf": 1.15, "gc": 1.65, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Bournemouth": {"gf": 1.45, "gc": 1.55, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.3},
        "Brighton": {"gf": 1.60, "gc": 1.40, "gf1t": 0.70, "corners": 5.5, "tarjetas": 2.0},
        "Leeds": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.6, "tarjetas": 2.5},
        "Nottingham": {"gf": 1.25, "gc": 1.45, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5},
        "Brentford": {"gf": 1.50, "gc": 1.50, "gf1t": 0.65, "corners": 4.6, "tarjetas": 2.0}
    },
    "🇩🇪 Bundesliga (2026/27)": {
        "Union Berlin": {"gf": 1.25, "gc": 1.30, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.4},
        "Eintracht Frankfurt": {"gf": 1.75, "gc": 1.35, "gf1t": 0.75, "corners": 5.0, "tarjetas": 2.2},
        "Bayern Munich": {"gf": 2.50, "gc": 1.05, "gf1t": 1.30, "corners": 6.7, "tarjetas": 1.7},
        "Bayer Leverkusen": {"gf": 2.35, "gc": 0.90, "gf1t": 1.15, "corners": 6.4, "tarjetas": 1.9},
        "Werder Bremen": {"gf": 1.40, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.2},
        "Schalke": {"gf": 1.25, "gc": 1.55, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.6},
        "Hamburger SV": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.5},
        "Dortmund": {"gf": 2.00, "gc": 1.20, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.0},
        "B. Monchengladbach": {"gf": 1.50, "gc": 1.50, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1},
        "Hoffenheim": {"gf": 1.60, "gc": 1.70, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.4},
        "FC Koln": {"gf": 1.25, "gc": 1.50, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5},
        "Mainz": {"gf": 1.35, "gc": 1.40, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.5},
        "Freiburg": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.7, "tarjetas": 1.9},
        "Augsburg": {"gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.6},
        "Paderborn": {"gf": 1.15, "gc": 1.60, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.4},
        "Stuttgart": {"gf": 1.95, "gc": 1.25, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.0},
        "Elversberg": {"gf": 1.10, "gc": 1.65, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.5},
        "RB Leipzig": {"gf": 1.90, "gc": 1.10, "gf1t": 0.85, "corners": 5.2, "tarjetas": 2.1}
    },
    "🇭🇳 Liga Nacional (Honduras 2026/27)": {
        "Real Espana": {"gf": 2.50, "gc": 0.00, "gf1t": 1.00, "corners": 5.5, "tarjetas": 2.3},
        "Olimpia": {"gf": 2.50, "gc": 0.50, "gf1t": 1.10, "corners": 5.8, "tarjetas": 2.4},
        "Marathon": {"gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.7},
        "Olancho": {"gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.8},
        "Motagua": {"gf": 1.50, "gc": 1.00, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.6},
        "Estrella Roja": {"gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.0, "tarjetas": 2.9},
        "Atletico Independiente": {"gf": 1.00, "gc": 1.00, "gf1t": 0.40, "corners": 3.9, "tarjetas": 3.0},
        "Genesis": {"gf": 1.00, "gc": 1.00, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.8},
        "UPNFM": {"gf": 0.50, "gc": 1.50, "gf1t": 0.25, "corners": 3.8, "tarjetas": 2.9},
        "Platense": {"gf": 0.50, "gc": 2.00, "gf1t": 0.20, "corners": 3.7, "tarjetas": 3.1},
        "Choloma": {"gf": 0.50, "gc": 2.00, "gf1t": 0.20, "corners": 3.6, "tarjetas": 3.2},
        "Juticalpa": {"gf": 0.50, "gc": 3.00, "gf1t": 0.15, "corners": 3.5, "tarjetas": 3.0}
    },
    "🇮🇹 Serie A (2026/27)": {
        "Lecce": {"gf": 1.05, "gc": 1.45, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.6},
        "Bologna": {"gf": 1.40, "gc": 1.00, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3},
        "Frosinone": {"gf": 1.10, "gc": 1.55, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.7},
        "Genoa": {"gf": 1.15, "gc": 1.30, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6},
        "Napoli": {"gf": 1.75, "gc": 0.90, "gf1t": 0.80, "corners": 5.6, "tarjetas": 2.0},
        "Udinese": {"gf": 1.25, "gc": 1.35, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5},
        "Monza": {"gf": 1.05, "gc": 1.40, "gf1t": 0.35, "corners": 4.1, "tarjetas": 2.3},
        "Sassuolo": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.4},
        "Venezia": {"gf": 1.00, "gc": 1.60, "gf1t": 0.35, "corners": 3.8, "tarjetas": 2.5},
        "AS Roma": {"gf": 1.55, "gc": 1.15, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.4},
        "Inter": {"gf": 1.90, "gc": 0.85, "gf1t": 0.95, "corners": 5.1, "tarjetas": 2.1},
        "Juventus": {"gf": 1.45, "gc": 0.80, "gf1t": 0.60, "corners": 4.3, "tarjetas": 2.3},
        "Fiorentina": {"gf": 1.60, "gc": 1.25, "gf1t": 0.70, "corners": 5.4, "tarjetas": 2.5},
        "AC Milan": {"gf": 1.70, "gc": 1.15, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.2},
        "Atalanta": {"gf": 2.05, "gc": 1.20, "gf1t": 0.95, "corners": 6.0, "tarjetas": 2.1},
        "Lazio": {"gf": 1.50, "gc": 1.10, "gf1t": 0.60, "corners": 4.9, "tarjetas": 2.6},
        "Cagliari": {"gf": 1.10, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6},
        "Torino": {"gf": 1.15, "gc": 1.05, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.4},
        "Parma": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.4},
        "Como": {"gf": 1.20, "gc": 1.50, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.4}
    },
    "🇲🇽 Liga MX (2026/27)": {
        "Club America": {"gf": 1.67, "gc": 0.33, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.1},
        "Club Tijuana": {"gf": 1.33, "gc": 0.33, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.5},
        "Toluca": {"gf": 2.00, "gc": 1.00, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.1},
        "UNAM Pumas": {"gf": 2.33, "gc": 1.67, "gf1t": 1.00, "corners": 5.3, "tarjetas": 2.4},
        "Monterrey": {"gf": 2.00, "gc": 1.33, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.2},
        "Cruz Azul": {"gf": 2.33, "gc": 2.00, "gf1t": 1.10, "corners": 5.9, "tarjetas": 2.0},
        "Queretaro": {"gf": 1.67, "gc": 1.33, "gf1t": 0.70, "corners": 4.2, "tarjetas": 2.5},
        "Necaxa": {"gf": 1.67, "gc": 1.67, "gf1t": 0.70, "corners": 4.4, "tarjetas": 2.5},
        "Atlas": {"gf": 1.33, "gc": 1.33, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.7},
        "Atlante": {"gf": 1.67, "gc": 1.67, "gf1t": 0.65, "corners": 4.3, "tarjetas": 2.6},
        "Puebla": {"gf": 1.00, "gc": 1.00, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.6},
        "Guadalajara Chivas": {"gf": 0.67, "gc": 1.00, "gf1t": 0.30, "corners": 5.2, "tarjetas": 2.4},
        "Pachuca": {"gf": 1.33, "gc": 1.00, "gf1t": 0.60, "corners": 5.5, "tarjetas": 2.2},
        "Club Leon": {"gf": 1.00, "gc": 1.33, "gf1t": 0.45, "corners": 4.9, "tarjetas": 2.6},
        "Atl San Luis": {"gf": 1.33, "gc": 1.67, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3},
        "Tigres UANL": {"gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3},
        "Santos Laguna": {"gf": 0.67, "gc": 2.33, "gf1t": 0.25, "corners": 4.6, "tarjetas": 2.4},
        "Juarez": {"gf": 0.33, "gc": 2.33, "gf1t": 0.15, "corners": 4.3, "tarjetas": 2.8}
    },
    "🇵🇹 Liga Portugal (2026/27)": {
        "FC Porto": {"gf": 2.00, "gc": 0.00, "gf1t": 1.00, "corners": 6.1, "tarjetas": 2.0},
        "Gil Vicente": {"gf": 1.00, "gc": 0.00, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.5},
        "Maritimo": {"gf": 1.00, "gc": 0.00, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.6},
        "Arouca": {"gf": 1.00, "gc": 0.00, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Sporting CP": {"gf": 2.00, "gc": 2.00, "gf1t": 0.90, "corners": 6.3, "tarjetas": 2.1},
        "Braga": {"gf": 2.00, "gc": 2.00, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.3},
        "Nacional": {"gf": 2.00, "gc": 2.00, "gf1t": 0.80, "corners": 4.4, "tarjetas": 2.7},
        "Academico Viseu": {"gf": 2.00, "gc": 2.00, "gf1t": 0.75, "corners": 4.1, "tarjetas": 2.6},
        "Famalicao": {"gf": 1.00, "gc": 1.00, "gf1t": 0.45, "corners": 4.5, "tarjetas": 2.4},
        "Estrela": {"gf": 2.00, "gc": 2.00, "gf1t": 0.80, "corners": 4.3, "tarjetas": 2.6},
        "Estoril": {"gf": 1.00, "gc": 1.00, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.5},
        "Santa Clara": {"gf": 2.00, "gc": 2.00, "gf1t": 0.80, "corners": 4.2, "tarjetas": 2.6},
        "Moreirense": {"gf": 2.00, "gc": 2.00, "gf1t": 0.75, "corners": 4.1, "tarjetas": 2.5},
        "Benfica": {"gf": 2.00, "gc": 2.00, "gf1t": 0.95, "corners": 6.5, "tarjetas": 2.0},
        "Vitoria Guimaraes": {"gf": 0.00, "gc": 1.00, "gf1t": 0.00, "corners": 4.8, "tarjetas": 2.5},
        "Rio Ave": {"gf": 0.00, "gc": 1.00, "gf1t": 0.00, "corners": 4.2, "tarjetas": 2.6},
        "Casa Pia": {"gf": 0.00, "gc": 1.00, "gf1t": 0.00, "corners": 4.0, "tarjetas": 2.7},
        "Alverca": {"gf": 0.00, "gc": 2.00, "gf1t": 0.00, "corners": 3.8, "tarjetas": 2.8}
    },
    "🇸🇦 Saudi Professional League (2026/27)": {
        "Al Hilal": {"gf": 2.30, "gc": 0.80, "gf1t": 1.10, "corners": 6.2, "tarjetas": 1.9},
        "Al Ettifaq": {"gf": 1.45, "gc": 1.25, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.3},
        "Al Ittihad": {"gf": 1.95, "gc": 1.10, "gf1t": 0.90, "corners": 5.6, "tarjetas": 2.4},
        "Al Shabab": {"gf": 1.50, "gc": 1.30, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.4},
        "Abha": {"gf": 1.15, "gc": 1.60, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.6},
        "Al Ahli SC": {"gf": 1.85, "gc": 1.15, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.2},
        "Al Hazem": {"gf": 1.05, "gc": 1.70, "gf1t": 0.35, "corners": 3.8, "tarjetas": 2.7},
        "Al Nassr": {"gf": 2.20, "gc": 1.00, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.1},
        "Al Fateh": {"gf": 1.35, "gc": 1.45, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.3},
        "Al Qadsiah": {"gf": 1.40, "gc": 1.35, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.4},
        "Al Taawon": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.3},
        "Al Faisaly": {"gf": 1.10, "gc": 1.50, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Al Khaleej": {"gf": 1.15, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.5},
        "Al Riyadh": {"gf": 1.10, "gc": 1.55, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.6},
        "Neom SC": {"gf": 1.30, "gc": 1.40, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.3},
        "Al Diriyah": {"gf": 1.00, "gc": 1.65, "gf1t": 0.30, "corners": 3.7, "tarjetas": 2.6},
        "Al Fayha": {"gf": 1.15, "gc": 1.45, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Al Kholood": {"gf": 1.05, "gc": 1.60, "gf1t": 0.35, "corners": 3.8, "tarjetas": 2.7}
    },
    "🇪🇸 LaLiga Española (2026/27)": {
        "Real Sociedad": {"gf": 1.45, "gc": 1.05, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.4},
        "Elche": {"gf": 1.10, "gc": 1.45, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6},
        "Alaves": {"gf": 1.15, "gc": 1.40, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.7},
        "Celta Vigo": {"gf": 1.35, "gc": 1.45, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.4},
        "Malaga": {"gf": 1.10, "gc": 1.50, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.7},
        "Rayo Vallecano": {"gf": 1.15, "gc": 1.30, "gf1t": 0.40, "corners": 4.3, "tarjetas": 2.7},
        "Real Madrid": {"gf": 2.15, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 1.8},
        "Villarreal": {"gf": 1.70, "gc": 1.40, "gf1t": 0.75, "corners": 5.1, "tarjetas": 2.5},
        "Barcelona": {"gf": 2.05, "gc": 0.95, "gf1t": 0.90, "corners": 6.2, "tarjetas": 2.0},
        "Atl. Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
        "Sevilla": {"gf": 1.35, "gc": 1.30, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.8},
        "Racing Santander": {"gf": 1.10, "gc": 1.55, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.6},
        "Dep. A Coruna": {"gf": 1.15, "gc": 1.50, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.5},
        "Valencia": {"gf": 1.25, "gc": 1.25, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.6},
        "Ath Bilbao": {"gf": 1.55, "gc": 1.00, "gf1t": 0.65, "corners": 5.3, "tarjetas": 2.3},
        "Espanyol": {"gf": 1.15, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6},
        "Betis": {"gf": 1.40, "gc": 1.20, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
        "Getafe": {"gf": 0.95, "gc": 1.10, "gf1t": 0.30, "corners": 3.8, "tarjetas": 3.2},
        "Osasuna": {"gf": 1.30, "gc": 1.35, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.5},
        "Levante": {"gf": 1.15, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6}
    },
    "🇺🇸 MLS (Estados Unidos 2026)": {
        "Vancouver Whitecaps": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1},
        "Los Angeles FC": {"gf": 1.90, "gc": 1.20, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.2},
        "San Jose Earthquakes": {"gf": 1.30, "gc": 1.60, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.3},
        "Houston Dynamo": {"gf": 1.40, "gc": 1.35, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.2},
        "Real Salt Lake": {"gf": 1.55, "gc": 1.40, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "FC Dallas": {"gf": 1.35, "gc": 1.40, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.0},
        "St. Louis City": {"gf": 1.40, "gc": 1.50, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.4},
        "Portland Timbers": {"gf": 1.60, "gc": 1.55, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.2},
        "Seattle Sounders": {"gf": 1.60, "gc": 1.10, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.0},
        "Minnesota United": {"gf": 1.45, "gc": 1.40, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.1},
        "Colorado Rapids": {"gf": 1.40, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.2},
        "Los Angeles Galaxy": {"gf": 1.80, "gc": 1.45, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.1},
        "San Diego FC": {"gf": 1.30, "gc": 1.45, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.2},
        "Austin FC": {"gf": 1.30, "gc": 1.45, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.1},
        "Sporting Kansas City": {"gf": 1.35, "gc": 1.55, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.3},
        "Nashville SC": {"gf": 1.30, "gc": 1.25, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.0},
        "Inter Miami": {"gf": 2.20, "gc": 1.25, "gf1t": 1.05, "corners": 5.0, "tarjetas": 2.0},
        "New England Revolution": {"gf": 1.35, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.1},
        "Chicago Fire": {"gf": 1.35, "gc": 1.55, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.3},
        "New York City": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.2},
        "FC Cincinnati": {"gf": 1.75, "gc": 1.25, "gf1t": 0.80, "corners": 4.8, "tarjetas": 2.1},
        "Charlotte": {"gf": 1.30, "gc": 1.35, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.2},
        "New York Red Bulls": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 5.1, "tarjetas": 2.5},
        "DC United": {"gf": 1.35, "gc": 1.55, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.4},
        "Orlando City": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "Columbus Crew": {"gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.6, "tarjetas": 1.9},
        "Toronto FC": {"gf": 1.25, "gc": 1.50, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.2},
        "Philadelphia Union": {"gf": 1.55, "gc": 1.35, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "CF Montreal": {"gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.2},
        "Atlanta Utd": {"gf": 1.50, "gc": 1.45, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.0}
    },
    "🇫🇷 Ligue 1 (Francia 2026/27)": {
        "Auxerre": {"gf": 1.15, "gc": 1.45, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.4},
        "Le Havre": {"gf": 1.05, "gc": 1.40, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.5},
        "Le Mans": {"gf": 1.00, "gc": 1.55, "gf1t": 0.35, "corners": 3.8, "tarjetas": 2.6},
        "Lille": {"gf": 1.65, "gc": 1.10, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.1},
        "Lorient": {"gf": 1.20, "gc": 1.50, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.3},
        "Monaco": {"gf": 1.95, "gc": 1.20, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.2},
        "Nice": {"gf": 1.45, "gc": 1.00, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.3},
        "PSG": {"gf": 2.45, "gc": 0.85, "gf1t": 1.20, "corners": 6.8, "tarjetas": 1.8},
        "Strasbourg": {"gf": 1.25, "gc": 1.40, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.4},
        "Angers": {"gf": 1.05, "gc": 1.50, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.5},
        "Brest": {"gf": 1.45, "gc": 1.20, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.2},
        "Troyes": {"gf": 1.00, "gc": 1.60, "gf1t": 0.30, "corners": 3.8, "tarjetas": 2.6},
        "Paris FC": {"gf": 1.10, "gc": 1.45, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.4},
        "Marseille": {"gf": 1.80, "gc": 1.25, "gf1t": 0.80, "corners": 5.6, "tarjetas": 2.5},
        "Toulouse": {"gf": 1.25, "gc": 1.35, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.3},
        "Lens": {"gf": 1.50, "gc": 1.15, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.4},
        "Rennes": {"gf": 1.55, "gc": 1.30, "gf1t": 0.65, "corners": 5.1, "tarjetas": 2.1}
        "Lyon":{"gf":1.65,"gc":1.25,"gf1t":0.70,"corners":5.4,"tarjetas":2.2,}
    },
    "🏆 Leagues Cup (2026)": {
        "Austin FC": {"gf": 1.30, "gc": 1.45, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.1},
        "Charlotte": {"gf": 1.30, "gc": 1.35, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.2},
        "Chicago Fire": {"gf": 1.35, "gc": 1.55, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.3},
        "FC Cincinnati": {"gf": 1.75, "gc": 1.25, "gf1t": 0.80, "corners": 4.8, "tarjetas": 2.1},
        "Columbus Crew": {"gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.6, "tarjetas": 1.9},
        "FC Dallas": {"gf": 1.35, "gc": 1.40, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.0},
        "Los Angeles FC": {"gf": 1.90, "gc": 1.20, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.2},
        "Real Salt Lake": {"gf": 1.55, "gc": 1.40, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "Nashville SC": {"gf": 1.30, "gc": 1.25, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.0},
        "Portland Timbers": {"gf": 1.60, "gc": 1.55, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.2},
        "Inter Miami": {"gf": 2.20, "gc": 1.25, "gf1t": 1.05, "corners": 5.0, "tarjetas": 2.0},
        "Philadelphia Union": {"gf": 1.55, "gc": 1.35, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "New York City": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.2},
        "Seattle Sounders": {"gf": 1.60, "gc": 1.10, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.0},
        "Orlando City": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.1},
        "San Diego FC": {"gf": 1.30, "gc": 1.45, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.2},
        "Minnesota United": {"gf": 1.45, "gc": 1.40, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.1},
        "Vancouver Whitecaps": {"gf": 1.50, "gc": 1.35, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1},
        "Club America": {"gf": 1.67, "gc": 0.33, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.1},
        "Juarez": {"gf": 0.33, "gc": 2.33, "gf1t": 0.15, "corners": 4.3, "tarjetas": 2.8},
        "Cruz Azul": {"gf": 2.33, "gc": 2.00, "gf1t": 1.10, "corners": 5.9, "tarjetas": 2.0},
        "Club Leon": {"gf": 1.00, "gc": 1.33, "gf1t": 0.45, "corners": 4.9, "tarjetas": 2.6},
        "Tigres UANL": {"gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3},
        "Toluca": {"gf": 2.00, "gc": 1.00, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.1},
        "Monterrey": {"gf": 2.00, "gc": 1.33, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.2},
        "Atlante": {"gf": 1.67, "gc": 1.67, "gf1t": 0.65, "corners": 4.3, "tarjetas": 2.6},
        "Guadalajara Chivas": {"gf": 0.67, "gc": 1.00, "gf1t": 0.30, "corners": 5.2, "tarjetas": 2.4},
        "Pachuca": {"gf": 1.33, "gc": 1.00, "gf1t": 0.60, "corners": 5.5, "tarjetas": 2.2},
        "Club Tijuana": {"gf": 1.33, "gc": 0.33, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.5},
        "Santos Laguna": {"gf": 0.67, "gc": 2.33, "gf1t": 0.25, "corners": 4.6, "tarjetas": 2.4},
        "Atlas": {"gf": 1.33, "gc": 1.33, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.7},
        "Necaxa": {"gf": 1.67, "gc": 1.67, "gf1t": 0.70, "corners": 4.4, "tarjetas": 2.5},
        "Atl San Luis": {"gf": 1.33, "gc": 1.67, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3},
        "UNAM Pumas": {"gf": 2.33, "gc": 1.67, "gf1t": 1.00, "corners": 5.3, "tarjetas": 2.4},
        "Queretaro": {"gf": 1.67, "gc": 1.33, "gf1t": 0.70, "corners": 4.2, "tarjetas": 2.5},
        "Puebla": {"gf": 1.00, "gc": 1.00, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.6}
    },
    "🇪🇺 UEFA Champions League (2026/27)": {
"Arsenal":{"gf":2.35,"gc":0.72,"gf1t":1.12,"gc1t":0.22,"corners":6.8,"tarjetas":1.6,"rojas":0.05,"posicion":1,"pts_ult_5":13,"sin_ganar":0,"bajas_clave":0,},
"AstonVilla":{"gf":1.85,"gc":1.15,"gf1t":0.82,"gc1t":0.48,"corners":5.4,"tarjetas":2.1,"rojas":0.06,"posicion":2,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":1,},
"Liverpool":{"gf":2.40,"gc":0.88,"gf1t":1.15,"gc1t":0.35,"corners":7.0,"tarjetas":1.6,"rojas":0.04,"posicion":3,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":1,},
"ManchesterCity":{"gf":2.45,"gc":0.80,"gf1t":1.20,"gc1t":0.30,"corners":7.4,"tarjetas":1.4,"rojas":0.03,"posicion":4,"pts_ult_5":11,"sin_ganar":1,"bajas_clave":2,},
"ManchesterUnited":{"gf":1.80,"gc":1.18,"gf1t":0.78,"gc1t":0.48,"corners":5.8,"tarjetas":2.0,"rojas":0.07,"posicion":5,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"Lille":{"gf":1.75,"gc":1.00,"gf1t":0.78,"gc1t":0.42,"corners":5.3,"tarjetas":2.0,"rojas":0.07,"posicion":6,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"PSG":{"gf":2.38,"gc":0.85,"gf1t":1.15,"gc1t":0.32,"corners":6.6,"tarjetas":1.8,"rojas":0.05,"posicion":7,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":1,},
"Napoli":{"gf":1.90,"gc":0.95,"gf1t":0.85,"gc1t":0.38,"corners":5.9,"tarjetas":2.0,"rojas":0.05,"posicion":8,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":1,},
"LASK":{"gf":1.50,"gc":1.25,"gf1t":0.62,"gc1t":0.50,"corners":4.9,"tarjetas":2.2,"rojas":0.08,"posicion":9,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":1,},
"SlaviaPraga":{"gf":1.95,"gc":0.88,"gf1t":0.88,"gc1t":0.32,"corners":5.8,"tarjetas":2.1,"rojas":0.08,"posicion":10,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":0,},
"ClubBrujas":{"gf":1.88,"gc":1.05,"gf1t":0.82,"gc1t":0.42,"corners":5.7,"tarjetas":2.1,"rojas":0.08,"posicion":11,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"Lens":{"gf":1.68,"gc":1.02,"gf1t":0.72,"gc1t":0.40,"corners":5.2,"tarjetas":2.1,"rojas":0.06,"posicion":12,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"SlovanBratislava":{"gf":1.45,"gc":1.58,"gf1t":0.58,"gc1t":0.65,"corners":4.4,"tarjetas":2.5,"rojas":0.12,"posicion":13,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":1,},
"BayernMúnich":{"gf":2.62,"gc":0.82,"gf1t":1.25,"gc1t":0.30,"corners":7.2,"tarjetas":1.5,"rojas":0.04,"posicion":14,"pts_ult_5":13,"sin_ganar":0,"bajas_clave":1,},
"BorussiaDortmund":{"gf":2.10,"gc":1.18,"gf1t":0.95,"gc1t":0.48,"corners":5.9,"tarjetas":2.0,"rojas":0.07,"posicion":15,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"ASRoma":{"gf":1.70,"gc":1.10,"gf1t":0.68,"gc1t":0.42,"corners":5.5,"tarjetas":2.3,"rojas":0.10,"posicion":16,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"InterdeMilán":{"gf":2.18,"gc":0.68,"gf1t":0.98,"gc1t":0.22,"corners":6.0,"tarjetas":1.7,"rojas":0.03,"posicion":17,"pts_ult_5":13,"sin_ganar":0,"bajas_clave":0,},
"PSVEindhoven":{"gf":2.45,"gc":0.85,"gf1t":1.18,"gc1t":0.32,"corners":6.6,"tarjetas":1.5,"rojas":0.04,"posicion":18,"pts_ult_5":13,"sin_ganar":0,"bajas_clave":0,},
"Feyenoord":{"gf":2.05,"gc":1.02,"gf1t":0.92,"gc1t":0.38,"corners":6.1,"tarjetas":1.8,"rojas":0.05,"posicion":19,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":0,},
"RealMadrid":{"gf":2.48,"gc":0.78,"gf1t":1.15,"gc1t":0.28,"corners":6.5,"tarjetas":1.7,"rojas":0.04,"posicion":20,"pts_ult_5":13,"sin_ganar":0,"bajas_clave":1,},
"Villarreal":{"gf":1.82,"gc":1.15,"gf1t":0.78,"gc1t":0.48,"corners":5.4,"tarjetas":2.2,"rojas":0.08,"posicion":21,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"FCBarcelona":{"gf":2.58,"gc":0.88,"gf1t":1.20,"gc1t":0.35,"corners":6.7,"tarjetas":1.9,"rojas":0.06,
"posicion":22,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":0,},
"AtléticodeMadrid":{"gf":1.88,"gc":0.82,"gf1t":0.88,"gc1t":0.32,"corners":5.4,"tarjetas":2.3,"rojas"0.09,"posicion":23,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":0,},
"RealBetis":{"gf":1.72,"gc":1.02,"gf1t":0.72,"gc1t":0.40,"corners":5.5,"tarjetas":2.2,"rojas":0.07,"posicion":24,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"FCPorto":{"gf":2.10,"gc":0.85,"gf1t":0.98,"gc1t":0.32,"corners":6.1,"tarjetas":2.1,"rojas":0.07,"posicion":25,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":0,},
"VfBStuttgart":{"gf":1.90,"gc":1.28,"gf1t":0.82,"gc1t":0.52,"corners":5.6,"tarjetas":1.9,"rojas":0.06,
"posicion":26,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"AEKAtenas":{"gf":1.65,"gc":1.15,"gf1t":0.72,"gc1t":0.45,"corners":5.1,"tarjetas":2.4,"rojas":0.10,"posicion":27,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"VikingFK":{"gf":1.58,"gc":1.32,"gf1t":0.65,"gc1t":0.52,"corners":5.0,"tarjetas":2.0,"rojas":0.06,"posicion":28,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":1,},
"Bodø/Glimt":{"gf":2.02,"gc":1.22,"gf1t":0.92,"gc1t":0.50,"corners":5.9,"tarjetas":1.7,"rojas":0.05,
"posicion":29,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":0,},
"SportingCP":{"gf":2.25,"gc":0.82,"gf1t":1.08,"gc1t":0.28,"corners":6.3,"tarjetas":1.8,"rojas":0.05,
"posicion":30,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":0,},
"Galatasaray":{"gf":2.22,"gc":1.12,"gf1t":1.02,"gc1t":0.45,"corners":6.2,"tarjetas":2.5,"rojas":0.12,
"posicion":31,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":1,},
"Fenerbahçe":{"gf":2.12,"gc":0.98,"gf1t":0.98,"gc1t":0.38,"corners":6.0,"tarjetas":2.4,"rojas":0.11,"posicion":32,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":1,},
"ShakhtarDonetsk":{"gf":1.80,"gc":1.15,"gf1t":0.78,"gc1t":0.48,"corners":5.2,"tarjetas":2.0,"rojas":0.07,"posicion":33,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"Como1907":{"gf":1.48,"gc":1.35,"gf1t":0.62,"gc1t":0.55,"corners":4.8,"tarjetas":2.2,"rojas":0.08,
"posicion":34,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"RBLeipzig":{"gf":2.00,"gc":1.08,"gf1t":0.90,"gc1t":0.42,"corners":5.8,"tarjetas":1.9,"rojas":0.06,
"posicion":35,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":1,},
"SabahBakú":{"gf":1.30,"gc":1.55,"gf1t":0.50,"gc1t":0.62,"corners":4.2,"tarjetas":2.6,"rojas":0.13,
"posicion":36,"pts_ult_5":4,"sin_ganar":3,"bajas_clave":1,},
    },
    "🇪🇺 UEFA Europa League (2026/27)": {
"Sunderland":{"gf":1.55,"gc":1.25,"gf1t":0.65,"gc1t":0.50,"corners":5.0,"tarjetas":2.1,"rojas":0.07,
"posicion":1,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"CrystalPalace":{"gf":1.62,"gc":1.20,"gf1t":0.68,"gc1t":0.48,"corners":5.2,"tarjetas":2.0,"rojas":0.06,"posicion":2,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"Bournemouth":{"gf":1.68,"gc":1.28,"gf1t":0.72,"gc1t":0.52,"corners":5.4,"tarjetas":2.2,"rojas":0.08,"posicion":3,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"RealSociedad":{"gf":1.48,"gc":1.05,"gf1t":0.65,"gc1t":0.42,"corners":5.5,"tarjetas":2.1,"rojas":0.07,"posicion":4,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"CeltaVigo":{"gf":1.60,"gc":1.30,"gf1t":0.68,"gc1t":0.52,"corners":5.1,"tarjetas":2.3,"rojas":0.09,
"posicion":5,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":0,},
"Salzburgo":{"gf":1.95,"gc":1.20,"gf1t":0.88,"gc1t":0.48,"corners":5.8,"tarjetas":1.9,"rojas":0.06,
"posicion":6,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"SturmGraz":{"gf":1.60,"gc":1.30,"gf1t":0.68,"gc1t":0.52,"corners":4.9,"tarjetas":2.3,"rojas":0.09,
"posicion":7,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":0,},
"ViktoriaPlzen":{"gf":1.62,"gc":1.08,"gf1t":0.68,"gc1t":0.42,"corners":5.0,"tarjetas":2.2,"rojas":0.08,"posicion":8,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"SpartaPraga":{"gf":1.75,"gc":1.20,"gf1t":0.72,"gc1t":0.48,"corners":5.3,"tarjetas":2.3,"rojas":0.10,
"posicion":9,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"Anderlecht":{"gf":1.68,"gc":1.12,"gf1t":0.72,"gc1t":0.45,"corners":5.2,"tarjetas":2.1,"rojas":0.07,"posicion":10,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"UnionSaint-Gilloise":{"gf":1.58,"gc":1.18,"gf1t":0.68,"gc1t":0.48,"corners":5.1,"tarjetas":2.3,
"rojas":0.09,"posicion":11,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":1,},
"Marsella":{"gf":1.95,"gc":1.15,"gf1t":0.85,"gc1t":0.45,"corners":5.8,"tarjetas":2.4,"rojas":0.10,
"posicion":12,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"Rennes":{"gf":1.70,"gc":1.20,"gf1t":0.72,"gc1t":0.48,"corners":5.3,"tarjetas":2.1,"rojas":0.07,
"posicion":13,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"Lyon":{"gf":1.82,"gc":1.22,"gf1t":0.78,"gc1t":0.50,"corners":5.4,"tarjetas":2.2,"rojas":0.08,
"posicion":14,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"BayerLeverkusen":{"gf":2.20,"gc":0.92,"gf1t":1.02,"gc1t":0.32,"corners":6.2,"tarjetas":1.9,"rojas":0.06,"posicion":15,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":1,},
"Hoffenheim":{"gf":1.85,"gc":1.35,"gf1t":0.80,"gc1t":0.55,"corners":5.3,"tarjetas":2.2,"rojas":0.08,
"posicion":16,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"Juventus":{"gf":1.80,"gc":0.68,"gf1t":0.80,"gc1t":0.22,"corners":5.5,"tarjetas":2.0,"rojas":0.04,"posicion":17,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":1,},
"ACMilán":{"gf":1.85,"gc":1.15,"gf1t":0.82,"gc1t":0.48,"corners":5.7,"tarjetas":2.2,"rojas":0.09,"posicion":18,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"Nijmegen":{"gf":1.45,"gc":1.35,"gf1t":0.60,"gc1t":0.55,"corners":4.8,"tarjetas":2.0,"rojas":0.06,"posicion":19,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"AZAlkmaar":{"gf":1.88,"gc":1.10,"gf1t":0.82,"gc1t":0.48,"corners":5.7,"tarjetas":1.9,"rojas":0.06,"posicion":20,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"Torreense":{"gf":1.25,"gc":1.48,"gf1t":0.50,"gc1t":0.60,"corners":4.2,"tarjetas":2.5,"rojas":0.11,"posicion":21,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":1,},
"LevskiSofía":{"gf":1.40,"gc":1.32,"gf1t":0.58,"gc1t":0.52,"corners":4.6,"tarjetas":2.4,"rojas":0.10,
"posicion":22,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"DinamoZagreb":{"gf":1.85,"gc":1.25,"gf1t":0.82,"gc1t":0.52,"corners":5.4,"tarjetas":2.2,"rojas":0.9,"posicion":23,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"Omonia":{"gf":1.42,"gc":1.28,"gf1t":0.58,"gc1t":0.50,"corners":4.6,"tarjetas":2.6,"rojas":0.12,"posicion":24,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"OFICreta":{"gf":1.35,"gc":1.42,"gf1t":0.52,"gc1t":0.58,"corners":4.4,"tarjetas":2.6,"rojas":0.12,"posicion":25,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":1,},
"OlympiacosPiraeus":{"gf":1.78,"gc":0.98,"gf1t":0.78,"gc1t":0.38,"corners":5.3,"tarjetas":2.3,"rojas":0.09,"posicion":26,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"HapoelBeerSheva":{"gf":1.42,"gc":1.30,"gf1t":0.58,"gc1t":0.52,"corners":4.5,"tarjetas":2.5,"rojas"0.11,"posicion":27,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"Lillestrom":{"gf":1.48,"gc":1.38,"gf1t":0.60,"gc1t":0.55,"corners":4.8,"tarjetas":2.1,"rojas":0.07,"posicion":28,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"Jagiellonia":{"gf":1.72,"gc":1.22,"gf1t":0.72,"gc1t":0.50,"corners":5.1,"tarjetas":2.3,"rojas":0.09,"posicion":29,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"LechPoznan":{"gf":1.62,"gc":1.20,"gf1t":0.68,"gc1t":0.48,"corners":5.0,"tarjetas":2.2,"rojas":0.08,"posicion":30,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"Benfica":{"gf":2.10,"gc":0.88,"gf1t":0.98,"gc1t":0.32,"corners":6.0,"tarjetas":1.9,"rojas":0.06,"posicion":31,"pts_ult_5":10,"sin_ganar":1,"bajas_clave":1,},
"Céltico":{"gf":2.25,"gc":1.10,"gf1t":1.02,"gc1t":0.42,"corners":6.4,"tarjetas":1.6,"rojas":0.05,"posicion":32,"pts_ult_5":12,"sin_ganar":0,"bajas_clave":0,},
"Celje":{"gf":1.42,"gc":1.38,"gf1t":0.58,"gc1t":0.55,"corners":4.6,"tarjetas":2.3,"rojas":0.09,"posicion":33,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"Besiktas":{"gf":1.78,"gc":1.18,"gf1t":0.78,"gc1t":0.50,"corners":5.5,"tarjetas":2.3,"rojas":0.09,"posicion":34,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"Ferencvaros":{"gf":1.58,"gc":1.22,"gf1t":0.68,"gc1t":0.50,"corners":5.0,"tarjetas":2.4,"rojas":0.10,
"posicion":35,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":0,},
"Ararat-Armenia":{"gf":1.25,"gc":1.50,"gf1t":0.48,"gc1t":0.62,"corners":4.1,"tarjetas":2.6,"rojas":0.13,"posicion":36,"pts_ult_5":4,"sin_ganar":3,"bajas_clave":1,},
},
    "🇪🇺 UEFA Conference League (2026/27)": {
"Mjallby":{"gf":1.38,"gc":1.28,"gf1t":0.55,"gc1t":0.52,"corners":4.6,"tarjetas":2.0,"rojas":0.06,"posicion":1,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":0,},
"Brighton":{"gf":1.88,"gc":1.25,"gf1t":0.82,"gc1t":0.50,"corners":5.8,"tarjetas":2.0,"rojas":0.06,"posicion":2,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"Mónaco":{"gf":1.95,"gc":1.10,"gf1t":0.88,"gc1t":0.48,"corners":5.6,"tarjetas":2.1,"rojas":0.10,"posicion":3,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"Jablonec":{"gf":1.32,"gc":1.40,"gf1t":0.52,"gc1t":0.58,"corners":4.3,"tarjetas":2.4,"rojas":0.09,"posicion":4,"pts_ult_5":5,"sin_ganar":2,"bajas_clave":0,},
"Caballero":{"gf":1.45,"gc":1.35,"gf1t":0.58,"gc1t":0.55,"corners":4.7,"tarjetas":2.3,"rojas":0.08,"posicion":5,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"SanTruiden":{"gf":1.40,"gc":1.38,"gf1t":0.55,"gc1t":0.55,"corners":4.5,"tarjetas":2.2,"rojas":0.07,"posicion":6,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"Friburgo":{"gf":1.72,"gc":1.18,"gf1t":0.72,"gc1t":0.48,"corners":5.4,"tarjetas":1.9,"rojas":0.05,"posicion":7,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"Atalanta":{"gf":2.15,"gc":1.00,"gf1t":1.00,"gc1t":0.38,"corners":6.1,"tarjetas":2.0,"rojas":0.05,"posicion":8,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":1,},
"Ajax":{"gf":2.02,"gc":1.05,"gf1t":0.92,"gc1t":0.42,"corners":5.9,"tarjetas":1.8,"rojas":0.05,"posicion":9,"pts_ult_5":11,"sin_ganar":0,"bajas_clave":1,},
"Twente":{"gf":1.72,"gc":1.18,"gf1t":0.72,"gc1t":0.50,"corners":5.4,"tarjetas":2.0,"rojas":0.06,"posicion":10,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"Getafe":{"gf":1.30,"gc":1.10,"gf1t":0.52,"gc1t":0.42,"corners":4.6,"tarjetas":2.8,"rojas":0.14,"posicion":11,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":0,},
"KuPS":{"gf":1.32,"gc":1.38,"gf1t":0.52,"gc1t":0.55,"corners":4.4,"tarjetas":2.1,"rojas":0.07,"posicion":12,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":1,},
"CSKASofía":{"gf":1.45,"gc":1.30,"gf1t":0.60,"gc1t":0.52,"corners":4.8,"tarjetas":2.5,"rojas":0.11,"posicion":13,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"HajdukSplit":{"gf":1.52,"gc":1.25,"gf1t":0.62,"gc1t":0.50,"corners":4.9,"tarjetas":2.3,"rojas":0.09,"posicion":14,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":1,},
"Pafos":{"gf":1.48,"gc":1.18,"gf1t":0.62,"gc1t":0.45,"corners":4.7,"tarjetas":2.5,"rojas":0.10,"posicion":15,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":0,},
"Aarhus":{"gf":1.42,"gc":1.30,"gf1t":0.58,"gc1t":0.52,"corners":4.7,"tarjetas":2.1,"rojas":0.07,"posicion":16,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":0,},
"FCCopenhague":{"gf":1.82,"gc":1.08,"gf1t":0.78,"gc1t":0.42,"corners":5.6,"tarjetas":1.9,"rojas":0.6,"posicion":17,"pts_ult_5":10,"sin_ganar":0,"bajas_clave":1,},
"Midtjylland":{"gf":1.72,"gc":1.22,"gf1t":0.72,"gc1t":0.50,"corners":5.3,"tarjetas":2.2,"rojas":0.08,
"posicion":18,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"Nordsjaelland":{"gf":1.78,"gc":1.28,"gf1t":0.78,"gc1t":0.52,"corners":5.5,"tarjetas":1.8,"rojas":0.05,"posicion":19,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":0,},
"Panathinaikos":{"gf":1.58,"gc":1.08,"gf1t":0.68,"gc1t":0.42,"corners":5.2,"tarjetas":2.5,"rojas":0.11,"posicion":20,"pts_ult_5":8,"sin_ganar":1,"bajas_clave":1,},
"Brann":{"gf":1.62,"gc":1.28,"gf1t":0.68,"gc1t":0.52,"corners":5.2,"tarjetas":1.9,"rojas":0.06,"posicion":21,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":0,},
"Braga":{"gf":1.82,"gc":1.18,"gf1t":0.78,"gc1t":0.48,"corners":5.6,"tarjetas":2.2,"rojas":0.08,"posicion":22,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":1,},
"Copas":{"gf":1.38,"gc":1.32,"gf1t":0.58,"gc1t":0.55,"corners":4.9,"tarjetas":2.4,"rojas":0.10,"posicion":23,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"Lugano":{"gf":1.52,"gc":1.28,"gf1t":0.62,"gc1t":0.50,"corners":4.9,"tarjetas":2.2,"rojas":0.08,"posicion":24,"pts_ult_5":7,"sin_ganar":2,"bajas_clave":0,},
"Crvenazvezda":{"gf":1.90,"gc":1.35,"gf1t":0.82,"gc1t":0.58,"corners":5.5,"tarjetas":2.4,"rojas":0.11,"posicion":25,"pts_ult_5":9,"sin_ganar":1,"bajas_clave":0,},
"Thun":{"gf":1.45,"gc":1.35,"gf1t":0.58,"gc1t":0.55,"corners":4.6,"tarjetas":2.1,"rojas":0.07,"posicion":26,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"Trabzonspor":{"gf":1.68,"gc":1.22,"gf1t":0.72,"gc1t":0.50,"corners":5.3,"tarjetas":2.5,"rojas":0.11,
"posicion":27,"pts_ult_5":7,"sin_ganar":1,"bajas_clave":0,},
"BoracBanjaLuka":{"gf":1.22,"gc":1.38,"gf1t":0.48,"gc1t":0.55,"corners":4.2,"tarjetas":2.6,"rojas":0.13,"posicion":28,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":0,},
"KairatAlmaty":{"gf":1.35,"gc":1.40,"gf1t":0.52,"gc1t":0.58,"corners":4.3,"tarjetas":2.3,"rojas":0.09
"posicion":29,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":1,},
"Egnatia":{"gf":1.18,"gc":1.45,"gf1t":0.45,"gc1t":0.60,"corners":4.0,"tarjetas":2.6,"rojas":0.12,"posicion":30,"pts_ult_5":4,"sin_ganar":3,"bajas_clave":0,},
"InterEscaldes":{"gf":1.12,"gc":1.55,"gf1t":0.42,"gc1t":0.65,"corners":3.8,"tarjetas":2.7,"rojas":0.14,"posicion":31,"pts_ult_5":3,"sin_ganar":4,"bajas_clave":1,},
"KaunoZalgiris":{"gf":1.20,"gc":1.48,"gf1t":0.45,"gc1t":0.62,"corners":4.1,"tarjetas":2.4,"rojas":0.1,
"posicion":32,"pts_ult_5":4,"sin_ganar":3,"bajas_clave":0,},
"UniversidaddeCraiova":{"gf":1.48,"gc":1.28,"gf1t":0.60,"gc1t":0.52,"corners":4.8,"tarjetas":2.4,"rojas":0.10,"posicion":33,"pts_ult_5":6,"sin_ganar":2,"bajas_clave":1,},
"Iberia1999":{"gf":1.25,"gc":1.42,"gf1t":0.48,"gc1t":0.60,"corners":4.1,"tarjetas":2.5,"rojas":0.11,
"posicion":34,"pts_ult_5":4,"sin_ganar":3,"bajas_clave":0,},
"LincolnRedImps":{"gf":1.08,"gc":1.60,"gf1t":0.40,"gc1t":0.68,"corners":3.7,"tarjetas":2.8,"rojas":0.15,"posicion":35,"pts_ult_5":3,"sin_ganar":4,"bajas_clave":1,},
"RigaFC":{"gf":1.32,"gc":1.48,"gf1t":0.52,"gc1t":0.60,"corners":4.4,"tarjetas":2.5,"rojas":0.12,"posicion":36,"pts_ult_5":5,"sin_ganar":3,"bajas_clave":0,},
    }
}

st.title("⚽ SIMULADOR PREDICTIVO MONTE CARLO ULTRA PRO")
st.markdown("Resultados 1X2 Tiempo Completo y 1er Tiempo, Goles, Córners y Tarjetas.")

modo = st.sidebar.radio("Modo de Selección de Equipos:", ["📋 Elegir de la Lista de Ligas", "✍️ Ingresar Equipos Manualmente"])

data_loc, data_vis = None, None
eq_local_nombre, eq_visita_nombre = "Local", "Visitante"

if modo == "📋 Elegir de la Lista de Ligas":
    liga_sel = st.sidebar.selectbox("Seleccionar Torneo / Liga:", list(BASE_DATOS.keys()))
    equipos_liga = list(BASE_DATOS[liga_sel].keys())

    col_inputs1, col_inputs2 = st.columns(2)
    with col_inputs1:
        st.subheader("🏠 Equipo Local")
        eq_local_nombre = st.selectbox("Local:", equipos_liga, index=0)
        prio_loc = st.slider("Necesidad de Ganar (Local):", 1, 10, 8, key="p_loc_1")

    with col_inputs2:
        st.subheader("✈️ Equipo Visitante")
        idx_vis = 1 if len(equipos_liga) > 1 else 0
        eq_visita_nombre = st.selectbox("Visitante:", equipos_liga, index=idx_vis)
        prio_vis = st.slider("Necesidad de Ganar (Visitante):", 1, 10, 7, key="p_vis_1")

    data_loc = BASE_DATOS[liga_sel][eq_local_nombre]
    data_vis = BASE_DATOS[liga_sel][eq_visita_nombre]

else:
    st.subheader("✍️ Ingreso Manual y Ajuste Estadístico de Equipos")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        eq_local_nombre = st.text_input("Nombre del Equipo Local:", "Equipo A")
        gf_loc = st.number_input("Goles Promedio Favor (Local):", 0.1, 5.0, 1.8, step=0.1)
        gc_loc = st.number_input("Goles Promedio Contra (Local):", 0.1, 5.0, 1.0, step=0.1)
        gf1t_loc = st.number_input("Goles Promedio 1er Tiempo (Local):", 0.0, 3.0, 0.8, step=0.1)
        corn_loc = st.number_input("Córners Promedio por Partido (Local):", 0.0, 12.0, 5.2, step=0.1)
        tarj_loc = st.number_input("Tarjetas Promedio por Partido (Local):", 0.0, 8.0, 2.3, step=0.1)
        prio_loc = st.slider("Necesidad de Ganar (Local):", 1, 10, 8, key="p_loc_2")
        data_loc = {"gf": gf_loc, "gc": gc_loc, "gf1t": gf1t_loc, "corners": corn_loc, "tarjetas": tarj_loc}

    with col_m2:
        eq_visita_nombre = st.text_input("Nombre del Equipo Visitante:", "Equipo B")
        gf_vis = st.number_input("Goles Promedio Favor (Visitante):", 0.1, 5.0, 1.3, step=0.1)
        gc_vis = st.number_input("Goles Promedio Contra (Visitante):", 0.1, 5.0, 1.4, step=0.1)
        gf1t_vis = st.number_input("Goles Promedio 1er Tiempo (Visitante):", 0.0, 3.0, 0.5, step=0.1)
        corn_vis = st.number_input("Córners Promedio por Partido (Visitante):", 0.0, 12.0, 4.4, step=0.1)
        tarj_vis = st.number_input("Tarjetas Promedio por Partido (Visitante):", 0.0, 8.0, 2.5, step=0.1)
        prio_vis = st.slider("Necesidad de Ganar (Visitante):", 1, 10, 7, key="p_vis_2")
        data_vis = {"gf": gf_vis, "gc": gc_vis, "gf1t": gf1t_vis, "corners": corn_vis, "tarjetas": tarj_vis}

# --- NUEVA INTERFAZ MODERNA Y LIMPIA PARA RITMO / INTENSIDAD ---
st.markdown("### 🔥 Ritmo e Intensidad del Partido")

# Opciones con tarjetas estilizadas horizontales
opciones_ritmo = {
    "🍵 Calmado / Amistoso": 0.80,
    "⚡ Normal / Estándar": 1.00,
    "🔥 Intenso / Directo": 1.15,
    "⚔️ Clásico / Alta Rivalidad": 1.28
}

ritmo_sel = st.radio(
    label="Selecciona la intensidad de juego:",
    options=list(opciones_ritmo.keys()),
    index=2,
    horizontal=True,
    label_visibility="collapsed"
)

f_ritmo = opciones_ritmo[ritmo_sel]

f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

if st.button("🚀 CALCULAR PREDICCIÓN (10,000 SIMULACIONES)", use_container_width=True):
    l_gf_loc = data_loc["gf"] * 1.10 * f_prio_loc * f_ritmo
    l_gf_vis = data_vis["gf"] * f_prio_vis * f_ritmo

    l_1t_loc = data_loc["gf1t"] * f_prio_loc * f_ritmo
    l_1t_vis = data_vis["gf1t"] * f_prio_vis * f_ritmo

    l_corners_tot = (data_loc["corners"] + data_vis["corners"]) * f_ritmo
    l_tarjetas_tot = (data_loc["tarjetas"] + data_vis["tarjetas"]) * f_ritmo

    N = 10000
    goles_loc = np.random.poisson(l_gf_loc, N)
    goles_vis = np.random.poisson(l_gf_vis, N)

    goles_1t_loc = np.random.poisson(l_1t_loc, N)
    goles_1t_vis = np.random.poisson(l_1t_vis, N)

    corners_ft = np.random.poisson(l_corners_tot, N)
    corners_1t = np.random.poisson(l_corners_tot * 0.45, N)

    tarjetas_ft = np.random.poisson(l_tarjetas_tot, N)
    
    p_roja_base = min(0.42, 0.16 * (l_tarjetas_tot / 4.2))
    rojas = np.random.binomial(1, p_roja_base, N)

    # Probabilidades 1X2 Tiempo Completo
    p_win_loc = np.mean(goles_loc > goles_vis) * 100
    p_draw = np.mean(goles_loc == goles_vis) * 100
    p_win_vis = np.mean(goles_loc < goles_vis) * 100

    # Probabilidades 1X2 1er Tiempo
    p_1t_win_loc = np.mean(goles_1t_loc > goles_1t_vis) * 100
    p_1t_draw = np.mean(goles_1t_loc == goles_1t_vis) * 100
    p_1t_win_vis = np.mean(goles_1t_loc < goles_1t_vis) * 100

    p_1t_05 = np.mean((goles_1t_loc + goles_1t_vis) > 0.5) * 100
    p_ft_25 = np.mean((goles_loc + goles_vis) > 2.5) * 100
    p_corn_95 = np.mean(corners_ft > 9.5) * 100
    p_corn_45_1t = np.mean(corners_1t > 4.5) * 100
    p_tarj_45 = np.mean(tarjetas_ft > 4.5) * 100
    p_roja = np.mean(rojas) * 100

    st.markdown("---")
    st.subheader(f"📊 Probabilidades 1X2 (Tiempo Completo): {eq_local_nombre} vs {eq_visita_nombre}")

    c1, c2, c3 = st.columns(3)
    c1.metric(f"Victoria {eq_local_nombre}", f"{p_win_loc:.1f}%")
    c2.metric("Empate Final", f"{p_draw:.1f}%")
    c3.metric(f"Victoria {eq_visita_nombre}", f"{p_win_vis:.1f}%")

    st.subheader(f"⏱️ Probabilidades 1X2 (Resultado al Descanso / 1er Tiempo)")

    d1, d2, d3 = st.columns(3)
    d1.metric(f"Gana 1T {eq_local_nombre}", f"{p_1t_win_loc:.1f}%")
    d2.metric("Empate al 1T", f"{p_1t_draw:.1f}%")
    d3.metric(f"Gana 1T {eq_visita_nombre}", f"{p_1t_win_vis:.1f}%")

    st.subheader("🎯 Pronósticos Sugeridos y Líneas de Valor")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### ⚽ Goles y Córners")
        st.write(f"⏱️ **Goles 1er Tiempo (> 0.5 1T):** **{p_1t_05:.1f}%** (Promedio esperable: {np.mean(goles_1t_loc + goles_1t_vis):.2f} goles)")
        st.write(f"⚽ **Goles Partido Completo (> 2.5 FT):** **{p_ft_25:.1f}%** (Promedio esperable: {np.mean(goles_loc + goles_vis):.2f} goles)")
        st.write(f"🚩 **Córners 1er Tiempo (> 4.5 1T):** **{p_corn_45_1t:.1f}%** (Promedio esperable: {np.mean(corners_1t):.1f} córners)")
        st.write(f"🚩 **Córners Totales (> 9.5 FT):** **{p_corn_95:.1f}%** (Promedio esperable: {np.mean(corners_ft):.1f} córners)")

    with col_b:
        st.markdown("### 🟨🟫 Tarjetas y Disciplina")
        st.write(f"🟨 **Total Tarjetas Amarillas (> 4.5):** **{p_tarj_45:.1f}%** (Promedio esperable: {np.mean(tarjetas_ft):.1f} tarjetas)")
        st.write(f"🟥 **Probabilidad de Tarjeta Roja en el Partido:** **{p_roja:.1f}%**")


