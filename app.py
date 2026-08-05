import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Simulador Predictivo de Fútbol Ultra Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base de datos completa
BASE_DATOS = {
    "Liga MX (México)": {
        "Club América": {"gf": 2.10, "gc": 0.90, "gf1t": 1.00, "corners": 5.8, "tarjetas": 2.1},
        "Tigres UANL": {"gf": 1.85, "gc": 0.95, "gf1t": 0.85, "corners": 5.4, "tarjetas": 2.3},
        "CF Monterrey (Rayados)": {"gf": 1.90, "gc": 1.00, "gf1t": 0.90, "corners": 5.6, "tarjetas": 2.2},
        "CD Cruz Azul": {"gf": 1.80, "gc": 0.85, "gf1t": 0.80, "corners": 5.9, "tarjetas": 2.0},
        "CD Guadalajara (Chivas)": {"gf": 1.50, "gc": 1.10, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.4},
        "Toluca FC": {"gf": 2.05, "gc": 1.25, "gf1t": 0.95, "corners": 5.7, "tarjetas": 2.1},
        "Pachuca FC": {"gf": 1.75, "gc": 1.30, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.2},
        "Pumas UNAM": {"gf": 1.60, "gc": 1.20, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.5},
        "Club León": {"gf": 1.45, "gc": 1.35, "gf1t": 0.60, "corners": 4.9, "tarjetas": 2.6},
        "Club Santos Laguna": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.6, "tarjetas": 2.4},
        "Atlas FC": {"gf": 1.25, "gc": 1.40, "gf1t": 0.45, "corners": 4.5, "tarjetas": 2.7},
        "Club Necaxa": {"gf": 1.35, "gc": 1.45, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.5},
        "Club Puebla": {"gf": 1.20, "gc": 1.60, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6},
        "Atletic de San Luis": {"gf": 1.40, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3},
        "FC Juárez": {"gf": 1.25, "gc": 1.55, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.8},
        "Mazatlán FC": {"gf": 1.15, "gc": 1.65, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.7},
        "Club Tijuana (Xolos)": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.6},
        "Querétaro FC": {"gf": 1.10, "gc": 1.60, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.5}
    },
    "UEFA Champions League": {
        "Real Madrid": {"gf": 2.30, "gc": 0.90, "gf1t": 1.10, "corners": 6.2, "tarjetas": 1.8},
        "Manchester City": {"gf": 2.45, "gc": 0.85, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5},
        "FC Bayern München": {"gf": 2.50, "gc": 1.00, "gf1t": 1.30, "corners": 6.8, "tarjetas": 1.7},
        "Paris Saint-Germain (PSG)": {"gf": 2.20, "gc": 1.05, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.1},
        "FC Barcelona": {"gf": 2.10, "gc": 1.00, "gf1t": 0.95, "corners": 6.4, "tarjetas": 2.0},
        "Inter Milan": {"gf": 1.95, "gc": 0.80, "gf1t": 0.95, "corners": 5.3, "tarjetas": 2.2},
        "Arsenal FC": {"gf": 2.20, "gc": 0.75, "gf1t": 1.10, "corners": 6.7, "tarjetas": 1.8},
        "Bayer 04 Leverkusen": {"gf": 2.30, "gc": 0.95, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.9},
        "Borussia Dortmund": {"gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.8, "tarjetas": 2.0},
        "Atlético de Madrid": {"gf": 1.75, "gc": 0.90, "gf1t": 0.75, "corners": 5.0, "tarjetas": 2.6},
        "Liverpool FC": {"gf": 2.30, "gc": 1.00, "gf1t": 1.05, "corners": 6.9, "tarjetas": 1.7},
        "Juventus": {"gf": 1.50, "gc": 0.85, "gf1t": 0.65, "corners": 4.5, "tarjetas": 2.3},
        "AC Milan": {"gf": 1.70, "gc": 1.15, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.2},
        "Aston Villa": {"gf": 1.80, "gc": 1.30, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.4},
        "Atalanta": {"gf": 2.05, "gc": 1.20, "gf1t": 0.95, "corners": 6.0, "tarjetas": 2.1},
        "Sporting CP": {"gf": 2.10, "gc": 0.90, "gf1t": 1.00, "corners": 6.1, "tarjetas": 2.2},
        "SL Benfica": {"gf": 2.00, "gc": 0.95, "gf1t": 0.95, "corners": 6.1, "tarjetas": 2.0},
        "RB Leipzig": {"gf": 1.90, "gc": 1.10, "gf1t": 0.85, "corners": 5.2, "tarjetas": 2.1}
    },
    "UEFA Europa League": {
        "AS Roma": {"gf": 1.70, "gc": 1.05, "gf1t": 0.75, "corners": 5.2, "tarjetas": 2.4},
        "Manchester United": {"gf": 1.75, "gc": 1.25, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.2},
        "Tottenham Hotspur": {"gf": 1.95, "gc": 1.35, "gf1t": 0.90, "corners": 6.2, "tarjetas": 2.3},
        "SS Lazio": {"gf": 1.65, "gc": 1.10, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.5},
        "Athletic Club Bilbao": {"gf": 1.60, "gc": 0.95, "gf1t": 0.70, "corners": 5.4, "tarjetas": 2.3},
        "Real Sociedad": {"gf": 1.50, "gc": 1.00, "gf1t": 0.65, "corners": 5.1, "tarjetas": 2.4},
        "Eintracht Frankfurt": {"gf": 1.80, "gc": 1.30, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.2},
        "Olympique de Marseille": {"gf": 1.85, "gc": 1.20, "gf1t": 0.85, "corners": 5.7, "tarjetas": 2.5},
        "FC Porto": {"gf": 1.90, "gc": 0.90, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.6},
        "Olympiacos FC": {"gf": 1.65, "gc": 1.00, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.7},
        "Galatasaray SK": {"gf": 2.00, "gc": 1.20, "gf1t": 0.90, "corners": 5.9, "tarjetas": 2.8},
        "Fenerbahçe SK": {"gf": 1.95, "gc": 1.15, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.7},
        "AFC Ajax": {"gf": 1.80, "gc": 1.25, "gf1t": 0.80, "corners": 5.6, "tarjetas": 2.1},
        "RSC Anderlecht": {"gf": 1.60, "gc": 1.20, "gf1t": 0.70, "corners": 5.2, "tarjetas": 2.3}
    },
    "UEFA Conference League": {
        "Chelsea FC": {"gf": 2.10, "gc": 1.10, "gf1t": 0.95, "corners": 5.9, "tarjetas": 2.4},
        "ACF Fiorentina": {"gf": 1.75, "gc": 1.15, "gf1t": 0.75, "corners": 5.6, "tarjetas": 2.5},
        "Real Betis": {"gf": 1.60, "gc": 1.10, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.3},
        "RC Lens": {"gf": 1.50, "gc": 1.05, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.4},
        "1. FC Heidenheim": {"gf": 1.45, "gc": 1.35, "gf1t": 0.60, "corners": 4.5, "tarjetas": 2.2},
        "Panathinaikos FC": {"gf": 1.40, "gc": 1.10, "gf1t": 0.55, "corners": 4.7, "tarjetas": 2.7},
        "KAA Gent": {"gf": 1.55, "gc": 1.25, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.2},
        "Legia Warszawa": {"gf": 1.50, "gc": 1.20, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.8},
        "Vitoria Guimaraes": {"gf": 1.55, "gc": 1.10, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.6},
        "FC Rapid Wien": {"gf": 1.45, "gc": 1.25, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.5}
    },
    "Concacaf Champions Cup": {
        "Club América": {"gf": 2.25, "gc": 0.85, "gf1t": 1.05, "corners": 6.0, "tarjetas": 2.1},
        "Tigres UANL": {"gf": 1.95, "gc": 0.90, "gf1t": 0.90, "corners": 5.6, "tarjetas": 2.3},
        "CF Monterrey": {"gf": 2.00, "gc": 0.95, "gf1t": 0.95, "corners": 5.8, "tarjetas": 2.2},
        "Inter Miami CF": {"gf": 2.15, "gc": 1.20, "gf1t": 1.00, "corners": 5.0, "tarjetas": 2.0},
        "Columbus Crew": {"gf": 1.90, "gc": 1.10, "gf1t": 0.85, "corners": 5.5, "tarjetas": 1.9},
        "CD Olimpia": {"gf": 1.70, "gc": 1.10, "gf1t": 0.75, "corners": 4.9, "tarjetas": 2.6},
        "LD Alajuelense": {"gf": 1.65, "gc": 1.15, "gf1t": 0.70, "corners": 4.7, "tarjetas": 2.5},
        "Deportivo Saprissa": {"gf": 1.60, "gc": 1.20, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.6},
        "FC Motagua": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.5, "tarjetas": 2.7},
        "CS Herediano": {"gf": 1.50, "gc": 1.25, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.5},
        "Seattle Sounders": {"gf": 1.60, "gc": 1.10, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.1},
        "Pachuca FC": {"gf": 1.80, "gc": 1.25, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.3}
    },
    "Leagues Cup (MLS vs Liga MX)": {
        "Inter Miami CF": {"gf": 2.20, "gc": 1.30, "gf1t": 1.05, "corners": 5.0, "tarjetas": 2.0},
        "Club América": {"gf": 2.10, "gc": 1.00, "gf1t": 0.95, "corners": 5.8, "tarjetas": 2.1},
        "Columbus Crew": {"gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.6, "tarjetas": 1.9},
        "Tigres UANL": {"gf": 1.90, "gc": 0.95, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.3},
        "CF Monterrey": {"gf": 1.95, "gc": 1.05, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.2},
        "Los Angeles FC (LAFC)": {"gf": 1.90, "gc": 1.20, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.2},
        "CD Cruz Azul": {"gf": 1.75, "gc": 0.95, "gf1t": 0.75, "corners": 5.8, "tarjetas": 2.0},
        "FC Cincinnati": {"gf": 1.75, "gc": 1.25, "gf1t": 0.80, "corners": 4.8, "tarjetas": 2.1},
        "Pachuca FC": {"gf": 1.70, "gc": 1.35, "gf1t": 0.75, "corners": 5.4, "tarjetas": 2.3},
        "Toluca FC": {"gf": 2.00, "gc": 1.30, "gf1t": 0.90, "corners": 5.6, "tarjetas": 2.2}
    },
    "Premier League (Inglaterra)": {
        "Manchester City": {"gf": 2.40, "gc": 0.85, "gf1t": 1.20, "corners": 7.1, "tarjetas": 1.5},
        "Arsenal FC": {"gf": 2.25, "gc": 0.75, "gf1t": 1.10, "corners": 6.6, "tarjetas": 1.8},
        "Liverpool FC": {"gf": 2.30, "gc": 1.00, "gf1t": 1.05, "corners": 6.9, "tarjetas": 1.7},
        "Chelsea FC": {"gf": 1.75, "gc": 1.30, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.5},
        "Manchester United": {"gf": 1.55, "gc": 1.35, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.2},
        "Tottenham Hotspur": {"gf": 1.90, "gc": 1.45, "gf1t": 0.85, "corners": 6.1, "tarjetas": 2.3},
        "Aston Villa": {"gf": 1.80, "gc": 1.30, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.4},
        "Newcastle United": {"gf": 1.75, "gc": 1.25, "gf1t": 0.75, "corners": 5.6, "tarjetas": 2.1},
        "Brighton & Hove Albion": {"gf": 1.60, "gc": 1.40, "gf1t": 0.70, "corners": 5.5, "tarjetas": 2.0},
        "West Ham United": {"gf": 1.45, "gc": 1.50, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.2},
        "Wolverhampton Wanderers": {"gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.6},
        "Fulham FC": {"gf": 1.40, "gc": 1.40, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
        "Brentford FC": {"gf": 1.50, "gc": 1.50, "gf1t": 0.65, "corners": 4.6, "tarjetas": 2.0},
        "Everton FC": {"gf": 1.15, "gc": 1.45, "gf1t": 0.40, "corners": 4.3, "tarjetas": 2.4},
        "Bournemouth": {"gf": 1.45, "gc": 1.55, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.3},
        "Crystal Palace": {"gf": 1.25, "gc": 1.40, "gf1t": 0.45, "corners": 4.5, "tarjetas": 2.1},
        "Leicester City": {"gf": 1.20, "gc": 1.65, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.2},
        "Ipswich Town": {"gf": 1.10, "gc": 1.70, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.5},
        "Southampton FC": {"gf": 1.05, "gc": 1.75, "gf1t": 0.35, "corners": 4.2, "tarjetas": 2.4},
        "Nottingham Forest": {"gf": 1.25, "gc": 1.45, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5}
    },
    "LaLiga (España)": {
        "Real Madrid": {"gf": 2.15, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 1.8},
        "FC Barcelona": {"gf": 2.05, "gc": 0.95, "gf1t": 0.90, "corners": 6.2, "tarjetas": 2.0},
        "Atlético de Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
        "Athletic Club": {"gf": 1.55, "gc": 1.00, "gf1t": 0.65, "corners": 5.3, "tarjetas": 2.3},
        "Villarreal CF": {"gf": 1.70, "gc": 1.40, "gf1t": 0.75, "corners": 5.1, "tarjetas": 2.5},
        "Girona FC": {"gf": 1.80, "gc": 1.30, "gf1t": 0.80, "corners": 5.2, "tarjetas": 2.1},
        "Real Sociedad": {"gf": 1.45, "gc": 1.05, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.4},
        "Real Betis": {"gf": 1.40, "gc": 1.20, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
        "Sevilla FC": {"gf": 1.35, "gc": 1.30, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.8},
        "Valencia CF": {"gf": 1.25, "gc": 1.25, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.6},
        "CA Osasuna": {"gf": 1.30, "gc": 1.35, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.5},
        "RC Celta de Vigo": {"gf": 1.35, "gc": 1.45, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.4},
        "Rayo Vallecano": {"gf": 1.15, "gc": 1.30, "gf1t": 0.40, "corners": 4.3, "tarjetas": 2.7},
        "RCD Mallorca": {"gf": 1.10, "gc": 1.20, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.8},
        "RCD Espanyol": {"gf": 1.15, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6},
        "Getafe CF": {"gf": 0.95, "gc": 1.10, "gf1t": 0.30, "corners": 3.8, "tarjetas": 3.2},
        "UD Las Palmas": {"gf": 1.10, "gc": 1.45, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.4},
        "Deportivo Alavés": {"gf": 1.15, "gc": 1.40, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.7},
        "CD Leganés": {"gf": 1.00, "gc": 1.35, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.5},
        "Real Valladolid": {"gf": 0.95, "gc": 1.60, "gf1t": 0.30, "corners": 3.8, "tarjetas": 2.6}
    },
    "Serie A (Italia)": {
        "Inter Milan": {"gf": 1.90, "gc": 0.85, "gf1t": 0.95, "corners": 5.1, "tarjetas": 2.1},
        "AC Milan": {"gf": 1.70, "gc": 1.15, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.2},
        "Juventus": {"gf": 1.45, "gc": 0.80, "gf1t": 0.60, "corners": 4.3, "tarjetas": 2.3},
        "SSC Napoli": {"gf": 1.75, "gc": 0.90, "gf1t": 0.80, "corners": 5.6, "tarjetas": 2.0},
        "Atalanta": {"gf": 2.05, "gc": 1.20, "gf1t": 0.95, "corners": 6.0, "tarjetas": 2.1},
        "AS Roma": {"gf": 1.55, "gc": 1.15, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.4},
        "SS Lazio": {"gf": 1.50, "gc": 1.10, "gf1t": 0.60, "corners": 4.9, "tarjetas": 2.6},
        "ACF Fiorentina": {"gf": 1.60, "gc": 1.25, "gf1t": 0.70, "corners": 5.4, "tarjetas": 2.5},
        "Bologna FC": {"gf": 1.40, "gc": 1.00, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.3},
        "Torino FC": {"gf": 1.15, "gc": 1.05, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.4},
        "Udinese Calcio": {"gf": 1.25, "gc": 1.35, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.5},
        "Genoa CFC": {"gf": 1.15, "gc": 1.30, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.6},
        "Parma Calcio": {"gf": 1.30, "gc": 1.50, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.4},
        "Hellas Verona": {"gf": 1.20, "gc": 1.55, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.7},
        "US Lecce": {"gf": 1.00, "gc": 1.45, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.6},
        "Empoli FC": {"gf": 1.05, "gc": 1.35, "gf1t": 0.35, "corners": 4.0, "tarjetas": 2.5},
        "Cagliari Calcio": {"gf": 1.10, "gc": 1.50, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.6},
        "AC Monza": {"gf": 1.05, "gc": 1.40, "gf1t": 0.35, "corners": 4.1, "tarjetas": 2.3},
        "Como 1907": {"gf": 1.20, "gc": 1.50, "gf1t": 0.45, "corners": 4.4, "tarjetas": 2.4},
        "Venezia FC": {"gf": 1.00, "gc": 1.60, "gf1t": 0.35, "corners": 3.8, "tarjetas": 2.5}
    },
    "Bundesliga (Alemania)": {
        "FC Bayern München": {"gf": 2.50, "gc": 1.05, "gf1t": 1.30, "corners": 6.7, "tarjetas": 1.7},
        "Bayer 04 Leverkusen": {"gf": 2.35, "gc": 0.90, "gf1t": 1.15, "corners": 6.4, "tarjetas": 1.9},
        "Borussia Dortmund": {"gf": 2.00, "gc": 1.20, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.0},
        "RB Leipzig": {"gf": 1.90, "gc": 1.10, "gf1t": 0.85, "corners": 5.2, "tarjetas": 2.1},
        "Eintracht Frankfurt": {"gf": 1.75, "gc": 1.35, "gf1t": 0.75, "corners": 5.0, "tarjetas": 2.2},
        "VfB Stuttgart": {"gf": 1.95, "gc": 1.25, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.0},
        "VfL Wolfsburg": {"gf": 1.40, "gc": 1.40, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.3},
        "Borussia M'gladbach": {"gf": 1.50, "gc": 1.50, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1},
        "SC Freiburg": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.7, "tarjetas": 1.9},
        "1. FSV Mainz 05": {"gf": 1.35, "gc": 1.40, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.5},
        "FC Augsburg": {"gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.6},
        "TSG 1899 Hoffenheim": {"gf": 1.60, "gc": 1.70, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.4},
        "1. FC Union Berlin": {"gf": 1.15, "gc": 1.30, "gf1t": 0.40, "corners": 4.2, "tarjetas": 2.4},
        "SV Werder Bremen": {"gf": 1.40, "gc": 1.50, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.2},
        "1. FC Heidenheim": {"gf": 1.35, "gc": 1.45, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.1},
        "FC St. Pauli": {"gf": 1.10, "gc": 1.40, "gf1t": 0.40, "corners": 4.1, "tarjetas": 2.3},
        "Holstein Kiel": {"gf": 1.15, "gc": 1.75, "gf1t": 0.40, "corners": 4.0, "tarjetas": 2.5},
        "VfL Bochum": {"gf": 1.05, "gc": 1.80, "gf1t": 0.35, "corners": 3.9, "tarjetas": 2.7}
    },
    "MLS (EE. UU.)": {
        "Inter Miami CF": {"gf": 2.20, "gc": 1.25, "gf1t": 1.10, "corners": 4.8, "tarjetas": 2.0},
        "LA Galaxy": {"gf": 1.90, "gc": 1.40, "gf1t": 0.80, "corners": 5.1, "tarjetas": 2.1},
        "Columbus Crew": {"gf": 1.95, "gc": 1.15, "gf1t": 0.95, "corners": 5.4, "tarjetas": 1.9},
        "FC Cincinnati": {"gf": 1.70, "gc": 1.20, "gf1t": 0.75, "corners": 4.7, "tarjetas": 2.2},
        "Los Angeles FC (LAFC)": {"gf": 1.85, "gc": 1.10, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.3},
        "Seattle Sounders FC": {"gf": 1.55, "gc": 1.05, "gf1t": 0.65, "corners": 5.2, "tarjetas": 2.0},
        "New York Red Bulls": {"gf": 1.60, "gc": 1.15, "gf1t": 0.70, "corners": 5.0, "tarjetas": 2.4},
        "Atlanta United FC": {"gf": 1.65, "gc": 1.35, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.1},
        "Philadelphia Union": {"gf": 1.50, "gc": 1.30, "gf1t": 0.65, "corners": 4.9, "tarjetas": 2.2},
        "New York City FC": {"gf": 1.55, "gc": 1.25, "gf1t": 0.70, "corners": 5.1, "tarjetas": 2.3},
        "Orlando City SC": {"gf": 1.60, "gc": 1.30, "gf1t": 0.70, "corners": 4.8, "tarjetas": 2.2},
        "Real Salt Lake": {"gf": 1.65, "gc": 1.25, "gf1t": 0.75, "corners": 5.0, "tarjetas": 2.1},
        "Portland Timbers": {"gf": 1.70, "gc": 1.50, "gf1t": 0.75, "corners": 5.2, "tarjetas": 2.2},
        "Minnesota United FC": {"gf": 1.45, "gc": 1.35, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.0},
        "Colorado Rapids": {"gf": 1.55, "gc": 1.45, "gf1t": 0.65, "corners": 4.8, "tarjetas": 2.1},
        "Houston Dynamo FC": {"gf": 1.35, "gc": 1.25, "gf1t": 0.55, "corners": 4.7, "tarjetas": 2.4},
        "Austin FC": {"gf": 1.25, "gc": 1.35, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.2},
        "Nashville SC": {"gf": 1.20, "gc": 1.30, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.0},
        "St. Louis City SC": {"gf": 1.40, "gc": 1.60, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.5},
        "Chicago Fire FC": {"gf": 1.25, "gc": 1.60, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.3},
        "CF Montréal": {"gf": 1.30, "gc": 1.65, "gf1t": 0.50, "corners": 4.3, "tarjetas": 2.2},
        "D.C. United": {"gf": 1.40, "gc": 1.70, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.6},
        "New England Revolution": {"gf": 1.15, "gc": 1.65, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.1},
        "Toronto FC": {"gf": 1.20, "gc": 1.60, "gf1t": 0.45, "corners": 4.3, "tarjetas": 2.3},
        "San Jose Earthquakes": {"gf": 1.30, "gc": 1.80, "gf1t": 0.50, "corners": 4.6, "tarjetas": 2.4},
        "FC Dallas": {"gf": 1.35, "gc": 1.45, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.1},
        "Sporting Kansas City": {"gf": 1.30, "gc": 1.70, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.3},
        "Vancouver Whitecaps": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.0},
        "San Diego FC": {"gf": 1.30, "gc": 1.40, "gf1t": 0.50, "corners": 4.5, "tarjetas": 2.2}
    },
    "Liga Nacional (Honduras)": {
        "CD Olimpia": {"gf": 2.05, "gc": 0.70, "gf1t": 0.95, "corners": 5.2, "tarjetas": 2.6},
        "FC Motagua": {"gf": 1.70, "gc": 0.95, "gf1t": 0.75, "corners": 4.8, "tarjetas": 2.7},
        "CD Marathon": {"gf": 1.50, "gc": 1.05, "gf1t": 0.60, "corners": 4.6, "tarjetas": 2.8},
        "Real España": {"gf": 1.60, "gc": 1.10, "gf1t": 0.70, "corners": 4.7, "tarjetas": 2.7},
        "Olancho FC": {"gf": 1.35, "gc": 1.10, "gf1t": 0.55, "corners": 4.3, "tarjetas": 2.9},
        "CD Victoria": {"gf": 1.20, "gc": 1.40, "gf1t": 0.45, "corners": 4.1, "tarjetas": 2.8},
        "UPNFM (Lobos)": {"gf": 1.10, "gc": 1.50, "gf1t": 0.40, "corners": 4.0, "tarjetas": 3.0},
        "Genesis FC": {"gf": 1.15, "gc": 1.30, "gf1t": 0.45, "corners": 4.2, "tarjetas": 2.9},
        "Real Sociedad (Tocoa)": {"gf": 1.10, "gc": 1.45, "gf1t": 0.40, "corners": 3.9, "tarjetas": 3.1},
        "Juticalpa FC": {"gf": 1.05, "gc": 1.35, "gf1t": 0.35, "corners": 3.8, "tarjetas": 3.0}
    }
}

st.title("⚽ SIMULADOR PREDICTIVO MONTE CARLO ULTRA PRO")
st.markdown("Incluye probabilidades de **Goles (1T y FT)**, **Córners**, **Tarjetas Amarillas** y **Tarjeta Roja**.")

# Opciones de Modo de Uso
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

ritmo_opt = st.select_slider(
    "🔥 Ritmo / Intensidad Esperada del Partido:",
    options=["Calmado / Amistoso (0.80x)", "Normal (1.00x)", "Picado / Intenso (1.15x)", "Rivalidad / Clásico (1.28x)"],
    value="Picado / Intenso (1.15x)"
)

f_ritmo = float(ritmo_opt.split("(")[1].replace("x)", ""))
f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

if st.button("🚀 CALCULAR PREDICCIÓN (10,000 SIMULACIONES)", use_container_width=True):
    # Lambdas ajustados
    l_gf_loc = data_loc["gf"] * 1.10 * f_prio_loc * f_ritmo
    l_gf_vis = data_vis["gf"] * f_prio_vis * f_ritmo

    l_1t_loc = data_loc["gf1t"] * f_prio_loc * f_ritmo
    l_1t_vis = data_vis["gf1t"] * f_prio_vis * f_ritmo

    l_corners_tot = (data_loc["corners"] + data_vis["corners"]) * f_ritmo
    l_tarjetas_tot = (data_loc["tarjetas"] + data_vis["tarjetas"]) * f_ritmo

    # Motor Monte Carlo (10,000 sim)
    N = 10000
    goles_loc = np.random.poisson(l_gf_loc, N)
    goles_vis = np.random.poisson(l_gf_vis, N)

    goles_1t_loc = np.random.poisson(l_1t_loc, N)
    goles_1t_vis = np.random.poisson(l_1t_vis, N)

    corners_ft = np.random.poisson(l_corners_tot, N)
    corners_1t = np.random.poisson(l_corners_tot * 0.45, N)

    tarjetas_ft = np.random.poisson(l_tarjetas_tot, N)
    
    # Probabilidad de tarjeta roja basada en agresividad combinada
    p_roja_base = min(0.42, 0.16 * (l_tarjetas_tot / 4.2))
    rojas = np.random.binomial(1, p_roja_base, N)

    # Porcentajes calculados
    p_win_loc = np.mean(goles_loc > goles_vis) * 100
    p_draw = np.mean(goles_loc == goles_vis) * 100
    p_win_vis = np.mean(goles_loc < goles_vis) * 100

    p_1t_05 = np.mean((goles_1t_loc + goles_1t_vis) > 0.5) * 100
    p_ft_25 = np.mean((goles_loc + goles_vis) > 2.5) * 100
    p_corn_95 = np.mean(corners_ft > 9.5) * 100
    p_corn_45_1t = np.mean(corners_1t > 4.5) * 100
    p_tarj_45 = np.mean(tarjetas_ft > 4.5) * 100
    p_roja = np.mean(rojas) * 100

    st.markdown("---")
    st.subheader(f"📊 Probabilidades 1X2: {eq_local_nombre} vs {eq_visita_nombre}")

    c1, c2, c3 = st.columns(3)
    c1.metric(f"Victoria {eq_local_nombre}", f"{p_win_loc:.1f}%")
    c2.metric("Empate", f"{p_draw:.1f}%")
    c3.metric(f"Victoria {eq_visita_nombre}", f"{p_win_vis:.1f}%")

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

