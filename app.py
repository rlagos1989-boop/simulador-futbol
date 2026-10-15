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
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/E0.csv",
    "🇪🇸 LaLiga Española (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/SP1.csv",
    "🇮🇹 Serie A (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/I1.csv",
    "🇩🇪 Bundesliga (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/D1.csv",
    "🇫🇷 Ligue 1 (2026/27)": "https://www.football-data.co.uk/mmz4281/2627/F1.csv"
}

# Base estática completa restaurada al 100%
LIGAS_ESTATICAS ={
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
            "Arsenal": {"gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6},
            "AstonVilla": {"gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.1},
            "Liverpool": {"gf": 2.40, "gc": 0.88, "gf1t": 1.15, "corners": 7.0, "tarjetas": 1.6},
            "ManchesterCity": {"gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4},
            "ManchesterUnited": {"gf": 1.80, "gc": 1.18, "gf1t": 0.78, "corners": 5.8, "tarjetas": 2.0},
            "Lille": {"gf": 1.75, "gc": 1.00, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.0},
            "PSG": {"gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8},
            "Napoli": {"gf": 1.90, "gc": 0.95, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.0},
            "LASK": {"gf": 1.50, "gc": 1.25, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2},
            "SlaviaPraga": {"gf": 1.95, "gc": 0.88, "gf1t": 0.88, "corners": 5.8, "tarjetas": 2.1},
            "ClubBrujas": {"gf": 1.88, "gc": 1.05, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.1},
            "Lens": {"gf": 1.68, "gc": 1.02, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.1},
            "SlovanBratislava": {"gf": 1.45, "gc": 1.58, "gf1t": 0.58, "corners": 4.4, "tarjetas": 2.5},
            "BayernMúnich": {"gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5},
            "BorussiaDortmund": {"gf": 2.10, "gc": 1.18, "gf1t": 0.95, "corners": 5.9, "tarjetas": 2.0},
            "ASRoma": {"gf": 1.70, "gc": 1.10, "gf1t": 0.68, "corners": 5.5, "tarjetas": 2.3},
            "InterdeMilán": {"gf": 2.18, "gc": 0.68, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.7},
            "PSVEindhoven": {"gf": 2.45, "gc": 0.85, "gf1t": 1.18, "corners": 6.6, "tarjetas": 1.5},
            "Feyenoord": {"gf": 2.05, "gc": 1.02, "gf1t": 0.92, "corners": 6.1, "tarjetas": 1.8},
            "RealMadrid": {"gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7},
            "Villarreal": {"gf": 1.82, "gc": 1.15, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2},
            "FCBarcelona": {"gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9},
            "Atl. Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
            "RealBetis": {"gf": 1.72, "gc": 1.02, "gf1t": 0.72, "corners": 5.5, "tarjetas": 2.2},
            "FCPorto": {"gf": 2.10, "gc": 0.85, "gf1t": 0.98, "corners": 6.1, "tarjetas": 2.1},
            "VfBStuttgart": {"gf": 1.90, "gc": 1.28, "gf1t": 0.82, "corners": 5.6, "tarjetas": 1.9},
            "AEKAtenas": {"gf": 1.65, "gc": 1.15, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.4},
            "VikingFK": {"gf": 1.58, "gc": 1.32, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.0},
            "Bodø/Glimt": {"gf": 2.02, "gc": 1.22, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.7},
            "SportingCP": {"gf": 2.25, "gc": 0.82, "gf1t": 1.08, "corners": 6.3, "tarjetas": 1.8},
            "Galatasaray": {"gf": 2.22, "gc": 1.12, "gf1t": 1.02, "corners": 6.2, "tarjetas": 2.5},
            "Fenerbahçe": {"gf": 2.12, "gc": 0.98, "gf1t": 0.98, "corners": 6.0, "tarjetas": 2.4},
            "ShakhtarDonetsk": {"gf": 1.80, "gc": 1.15, "gf1t": 0.78, "corners": 5.2, "tarjetas": 2.0},
            "Como1907": {"gf": 1.48, "gc": 1.35, "gf1t": 0.62, "corners": 4.8, "tarjetas": 2.2},
            "RBLeipzig": {"gf": 2.00, "gc": 1.08, "gf1t": 0.90, "corners": 5.8, "tarjetas": 1.9},
            "SabahBakú": {"gf": 1.30, "gc": 1.55, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.6}
        },
        "🇪🇺 UEFA Europa League (2026/27)": {
            "HapoelBeerSheva": {"gf": 1.42, "gc": 1.30, "gf1t": 0.58, "corners": 4.5, "tarjetas": 2.5},
            "Sunderland": {"gf": 1.55, "gc": 1.25, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.1},
            "CrystalPalace": {"gf": 1.62, "gc": 1.20, "gf1t": 0.68, "corners": 5.2, "tarjetas": 2.0},
            "Bournemouth": {"gf": 1.68, "gc": 1.28, "gf1t": 0.72, "corners": 5.4, "tarjetas": 2.2},
            "RealSociedad": {"gf": 1.48, "gc": 1.05, "gf1t": 0.65, "corners": 5.5, "tarjetas": 2.1},
            "CeltaVigo": {"gf": 1.60, "gc": 1.30, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.3},
            "Salzburgo": {"gf": 1.95, "gc": 1.20, "gf1t": 0.88, "corners": 5.8, "tarjetas": 1.9},
            "SturmGraz": {"gf": 1.60, "gc": 1.30, "gf1t": 0.68, "corners": 4.9, "tarjetas": 2.3},
            "ViktoriaPlzen": {"gf": 1.62, "gc": 1.08, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.2},
            "SpartaPraga": {"gf": 1.75, "gc": 1.20, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.3},
            "Anderlecht": {"gf": 1.68, "gc": 1.12, "gf1t": 0.72, "corners": 5.2, "tarjetas": 2.1},
            "UnionSaint-Gilloise": {"gf": 1.58, "gc": 1.18, "gf1t": 0.68, "corners": 5.1, "tarjetas": 2.3},
            "Marsella": {"gf": 1.95, "gc": 1.15, "gf1t": 0.85, "corners": 5.8, "tarjetas": 2.4},
            "Rennes": {"gf": 1.70, "gc": 1.20, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.1},
            "Lyon": {"gf": 1.82, "gc": 1.22, "gf1t": 0.78, "corners": 5.4, "tarjetas": 2.2},
            "BayerLeverkusen": {"gf": 2.20, "gc": 0.92, "gf1t": 1.02, "corners": 6.2, "tarjetas": 1.9},
            "Hoffenheim": {"gf": 1.85, "gc": 1.35, "gf1t": 0.80, "corners": 5.3, "tarjetas": 2.2},
            "Juventus": {"gf": 1.80, "gc": 0.68, "gf1t": 0.80, "corners": 5.5, "tarjetas": 2.0},
            "ACMilán": {"gf": 1.85, "gc": 1.15, "gf1t": 0.82, "corners": 5.7, "tarjetas": 2.2},
            "Nijmegen": {"gf": 1.45, "gc": 1.35, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.0},
            "AZAlkmaar": {"gf": 1.88, "gc": 1.10, "gf1t": 0.82, "corners": 5.7, "tarjetas": 1.9},
            "Torreense": {"gf": 1.25, "gc": 1.48, "gf1t": 0.50, "corners": 4.2, "tarjetas": 2.5},
            "LevskiSofía": {"gf": 1.40, "gc": 1.32, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.4},
            "DinamoZagreb": {"gf": 1.85, "gc": 1.25, "gf1t": 0.82, "corners": 5.4, "tarjetas": 2.2},
            "Omonia": {"gf": 1.42, "gc": 1.28, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.6},
            "OFICreta": {"gf": 1.35, "gc": 1.42, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.6},
            "OlympiacosPiraeus": {"gf": 1.78, "gc": 0.98, "gf1t": 0.78, "corners": 5.3, "tarjetas": 2.3},
            "Lillestrom": {"gf": 1.48, "gc": 1.38, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.1},
            "Jagiellonia": {"gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.1, "tarjetas": 2.3},
            "LechPoznan": {"gf": 1.62, "gc": 1.20, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.2},
            "Benfica": {"gf": 2.10, "gc": 0.88, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.9},
            "Céltico": {"gf": 2.25, "gc": 1.10, "gf1t": 1.02, "corners": 6.4, "tarjetas": 1.6},
            "Celje": {"gf": 1.42, "gc": 1.38, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.3},
            "Besiktas": {"gf": 1.78, "gc": 1.18, "gf1t": 0.78, "corners": 5.5, "tarjetas": 2.3},
            "Ferencvaros": {"gf": 1.58, "gc": 1.22, "gf1t": 0.68, "corners": 5.0, "tarjetas": 2.4},
            "Ararat- Armenia": {"gf": 1.25, "gc": 1.50, "gf1t": 0.48, "corners": 4.1, "tarjetas": 2.6}
        },
        "🇪🇺 UEFA Conference League (2026/27)": {
            "Mjallby": {"gf": 1.38, "gc": 1.28, "gf1t": 0.55, "corners": 4.6, "tarjetas": 2.0},
            "Brighton": {"gf": 1.88, "gc": 1.25, "gf1t": 0.82, "corners": 5.8, "tarjetas": 2.0},
            "Mónaco": {"gf": 1.95, "gc": 1.10, "gf1t": 0.88, "corners": 5.6, "tarjetas": 2.1},
            "Jablonec": {"gf": 1.32, "gc": 1.40, "gf1t": 0.52, "corners": 4.3, "tarjetas": 2.4},
            "Caballero": {"gf": 1.45, "gc": 1.35, "gf1t": 0.58, "corners": 4.7, "tarjetas": 2.3},
            "SanTruiden": {"gf": 1.40, "gc": 1.38, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.2},
            "Friburgo": {"gf": 1.72, "gc": 1.18, "gf1t": 0.72, "corners": 5.4, "tarjetas": 1.9},
            "Atalanta": {"gf": 2.15, "gc": 1.00, "gf1t": 1.00, "corners": 6.1, "tarjetas": 2.0},
            "Ajax": {"gf": 2.02, "gc": 1.05, "gf1t": 0.92, "corners": 5.9, "tarjetas": 1.8},
            "Twente": {"gf": 1.72, "gc": 1.18, "gf1t": 0.72, "corners": 5.4, "tarjetas": 2.0},
            "Getafe": {"gf": 1.30, "gc": 1.10, "gf1t": 0.52, "corners": 4.6, "tarjetas": 2.8},
            "KuPS": {"gf": 1.32, "gc": 1.38, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.1},
            "CSKASofía": {"gf": 1.45, "gc": 1.30, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.5},
            "HajdukSplit": {"gf": 1.52, "gc": 1.25, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.3},
            "Pafos": {"gf": 1.48, "gc": 1.18, "gf1t": 0.62, "corners": 4.7, "tarjetas": 2.5},
            "Aarhus": {"gf": 1.42, "gc": 1.30, "gf1t": 0.58, "corners": 4.7, "tarjetas": 2.1},
            "FCCopenhague": {"gf": 1.82, "gc": 1.08, "gf1t": 0.78, "corners": 5.6, "tarjetas": 1.9},
            "Midtjylland": {"gf": 1.72, "gc": 1.22, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.2},
            "Nordsjaelland": {"gf": 1.78, "gc": 1.28, "gf1t": 0.78, "corners": 5.5, "tarjetas": 1.8},
            "Panathinaikos": {"gf": 1.58, "gc": 1.08, "gf1t": 0.68, "corners": 5.2, "tarjetas": 2.5},
            "Brann": {"gf": 1.62, "gc": 1.28, "gf1t": 0.68, "corners": 5.2, "tarjetas": 1.9},
            "Braga": {"gf": 1.82, "gc": 1.18, "gf1t": 0.78, "corners": 5.6, "tarjetas": 2.2},
            "Copas": {"gf": 1.38, "gc": 1.32, "gf1t": 0.58, "corners": 4.9, "tarjetas": 2.4},
            "Lugano": {"gf": 1.52, "gc": 1.28, "gf1t": 0.62, "corners": 4.9, "tarjetas": 2.2},
            "Crvenazvezda": {"gf": 1.90, "gc": 1.35, "gf1t": 0.82, "corners": 5.5, "tarjetas": 2.4},
            "Thun": {"gf": 1.45, "gc": 1.35, "gf1t": 0.58, "corners": 4.6, "tarjetas": 2.1},
            "Trabzonspor": {"gf": 1.68, "gc": 1.22, "gf1t": 0.72, "corners": 5.3, "tarjetas": 2.5},
            "BoracBanjaLuka": {"gf": 1.22, "gc": 1.38, "gf1t": 0.48, "corners": 4.2, "tarjetas": 2.6},
            "KairatAlmaty": {"gf": 1.35, "gc": 1.40, "gf1t": 0.52, "corners": 4.3, "tarjetas": 2.3},
            "Egnatia": {"gf": 1.18, "gc": 1.45, "gf1t": 0.45, "corners": 4.0, "tarjetas": 2.6},
            "InterEscaldes": {"gf": 1.12, "gc": 1.55, "gf1t": 0.42, "corners": 3.8, "tarjetas": 2.7},
            "KaunoZalgiris": {"gf": 1.20, "gc": 1.48, "gf1t": 0.45, "corners": 4.1, "tarjetas": 2.4},
            "UniversidaddeCraiova": {"gf": 1.48, "gc": 1.28, "gf1t": 0.60, "corners": 4.8, "tarjetas": 2.4},
            "Iberia1999": {"gf": 1.25, "gc": 1.42, "gf1t": 0.48, "corners": 4.1, "tarjetas": 2.5},
            "LincolnRedImps": {"gf": 1.08, "gc": 1.60, "gf1t": 0.40, "corners": 3.7, "tarjetas": 2.8},
            "RigaFC": {"gf": 1.32, "gc": 1.48, "gf1t": 0.52, "corners": 4.4, "tarjetas": 2.5}
        }
    }

BASE_DATOS = cargar_base_datos_actualizada()

# ==============================================================================
# --- INTERFAZ PRINCIPAL DE STREAMLIT ---
# ==============================================================================

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

    with col_inputs2:
        st.subheader("✈️ Equipo Visitante")
        idx_vis = 1 if len(equipos_liga) > 1 else 0
        eq_visita_nombre = st.selectbox("Visitante:", equipos_liga, index=idx_vis)

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
        data_loc = {"gf": gf_loc, "gc": gc_loc, "gf1t": gf1t_loc, "corners": corn_loc, "tarjetas": tarj_loc}

    with col_m2:
        eq_visita_nombre = st.text_input("Nombre del Equipo Visitante:", "Equipo B")
        gf_vis = st.number_input("Goles Promedio Favor (Visitante):", 0.1, 5.0, 1.3, step=0.1)
        gc_vis = st.number_input("Goles Promedio Contra (Visitante):", 0.1, 5.0, 1.4, step=0.1)
        gf1t_vis = st.number_input("Goles Promedio 1er Tiempo (Visitante):", 0.0, 3.0, 0.5, step=0.1)
        corn_vis = st.number_input("Córners Promedio por Partido (Visitante):", 0.0, 12.0, 4.4, step=0.1)
        tarj_vis = st.number_input("Tarjetas Promedio por Partido (Visitante):", 0.0, 8.0, 2.5, step=0.1)
        data_vis = {"gf": gf_vis, "gc": gc_vis, "gf1t": gf1t_vis, "corners": corn_vis, "tarjetas": tarj_vis}

# ==============================================================================
# --- CÁLCULO Y ANÁLISIS AUTOMÁTICO DE PRIORIDAD E INTENSIDAD DE JUEGO ---
# ==============================================================================

# 1. Prioridad Automática (Análisis de poder ofensivo vs fragilidad defensiva rival)
diff_loc = (data_loc["gf"] - data_vis["gc"]) + (data_loc["gf1t"] - 0.5)
diff_vis = (data_vis["gf"] - data_loc["gc"]) + (data_vis["gf1t"] - 0.5)

prio_loc = int(np.clip(5 + diff_loc * 2.0, 1, 10))
prio_vis = int(np.clip(5 + diff_vis * 2.0, 1, 10))

f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

# 2. Intensidad y Ritmo Automáticos (Combinación de Tarjetas, Goles y Córners Esperados)
tarj_comb = data_loc.get("tarjetas", 2.2) + data_vis.get("tarjetas", 2.2)
goles_comb = data_loc["gf"] + data_vis["gf"]
corners_comb = data_loc["corners"] + data_vis["corners"]

score_ritmo = (tarj_comb / 4.5) * 0.5 + (goles_comb / 3.0) * 0.3 + (corners_comb / 10.0) * 0.2

if score_ritmo >= 1.22:
    ritmo_label = "⚔️ Clásico / Alta Rivalidad"
    f_ritmo = 1.28
elif score_ritmo >= 1.05:
    ritmo_label = "🔥 Intenso / Directo"
    f_ritmo = 1.15
elif score_ritmo >= 0.88:
    ritmo_label = "⚡ Normal / Estándar"
    f_ritmo = 1.00
else:
    ritmo_label = "🍵 Calmado / Amistoso"
    f_ritmo = 0.80

# --- PANEL DE VISUALIZACIÓN AUTOMÁTICA ---
st.markdown("---")
st.markdown("### 🤖 Análisis Estadístico Automático")

col_auto1, col_auto2, col_auto3 = st.columns(3)
with col_auto1:
    st.metric(f"🎯 Prioridad Auto ({eq_local_nombre})", f"{prio_loc} / 10", help="Nivel de necesidad evaluado automáticamente según xG vs Defensa Rival")
with col_auto2:
    st.metric(f"🎯 Prioridad Auto ({eq_visita_nombre})", f"{prio_vis} / 10", help="Nivel de necesidad evaluado automáticamente según xG vs Defensa Rival")
with col_auto3:
    st.metric("🔥 Intensidad Auto", ritmo_label, f"Multiplicador x{f_ritmo:.2f}", help="Análisis automático de ritmo basado en fricción, tarjetas y córners esperados")

# ==============================================================================
# --- EJECUCIÓN DE SIMULACIÓN MONTE CARLO ---
# ==============================================================================

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
# =========================================================
# MÓDULO UNIFICADO: TÁCTICA, BAJAS Y SIMULACIÓN CON GRÁFICA
# =========================================================

st.markdown("---")
st.subheader("⚽ Centro de Simulación Táctica y Predicción Avanzada")

with st.expander("⚙️ 1. Configurar Alineaciones y Bajas (Factor Humano)", expanded=True):
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("#### 🏠 Equipo Local")
        formacion_local = st.selectbox("Formación (Local)", ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2", "4-1-4-1"], key="f_loc_unif")
        notas_local = st.text_area("Bajas / Notas (Local)", placeholder="Ej: No juega Vinicius Jr, baja por lesión", key="n_loc_unif")
        
    with col_t2:
        st.markdown("#### ✈️ Equipo Visitante")
        formacion_vis = st.selectbox("Formación (Visitante)", ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2", "4-1-4-1"], key="f_vis_unif")
        notas_vis = st.text_area("Bajas / Notas (Visitante)", placeholder="Ej: Sin portero titular", key="n_vis_unif")
        
    # Cálculo inteligente de factores de rendimiento basados en ausencias y esquemas
    f_rend_l = 1.0
    f_rend_v = 1.0
    
    palabras_alerta = ["no juega", "lesion", "lesionado", "baja", "suspendido", "ausente", "fuera", "operado"]
    for palabra in palabras_alerta:
        if palabra in notas_local.lower():
            f_rend_l -= 0.15  # Penalización del 15% por baja sensible local
        if palabra in notas_vis.lower():
            f_rend_v -= 0.15  # Penalización del 15% por baja sensible visitante

    # Bonificación táctica de mediocampo
    if formacion_local == "4-3-3" and formacion_vis == "4-4-2":
        f_rend_l += 0.05
    elif formacion_local == "4-4-2" and formacion_vis == "4-3-3":
        f_rend_v += 0.05

    if f_rend_l < 1.0 or f_rend_v < 1.0:
        st.warning("⚠️ El modelo ha detectado ausencias y ha ajustado dinámicamente la fuerza ofensiva de los equipos.")

with st.expander("📊 2. Estadísticas Base y Disparos para la Cancha", expanded=True):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        tiros_l_base = st.number_input("Tiros Previstos / Totales (Local)", 1, 30, 12, key="t_l_base")
        goles_esp_l = st.number_input("xG / Goles Esperados Base (Local)", 0.1, 5.0, 1.6, key="xg_l_base")
    with col_s2:
        tiros_v_base = st.number_input("Tiros Previstos / Totales (Visitante)", 1, 30, 9, key="t_v_base")
        goles_esp_v = st.number_input("xG / Goles Esperados Base (Visitante)", 0.1, 5.0, 1.1, key="xg_v_base")

if st.button("🚀 Simular Partido Completo (Aplicando Táctica y Bajas)", type="primary"):
    # Aplicar los factores de rendimiento de las alineaciones y bajas a los goles esperados
    xg_l_final = goles_esp_l * f_rend_l
    xg_v_final = goles_esp_v * f_rend_v
    
    np.random.seed(42)
    goles_sim_l = np.random.poisson(xg_l_final)
    goles_sim_v = np.random.poisson(xg_v_final)
    
    st.markdown("---")
    st.success(f"🎯 **Resultado Final Simulado:** Local **{goles_sim_l} - {goles_sim_v}** Visitante")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Poder Local Ajustado", f"{int(f_rend_l*100)}%", f"Esquema: {formacion_local}")
    col_m2.metric("Poder Visitante Ajustado", f"{int(f_rend_v*100)}%", f"Esquema: {formacion_vis}")
    col_m3.metric("Expectativa de Goles (xG)", f"{round(xg_l_final, 2)} - {round(xg_v_final, 2)}")
