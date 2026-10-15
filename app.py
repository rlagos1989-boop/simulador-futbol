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
LIGAS_ESTATICAS = {
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
        disparos_puerta_l = st.number_input("Disparos a Puerta (1T)", 0, 15, 3, key="dp_l_ht")
        pases_comp_l = st.number_input("Pases Completados (1T)", 0, 600, 220, key="pc_l_ht")
        toques_area_l = st.number_input("Toques en Área Rival (1T)", 0, 100, 12, key="ta_l_ht")
        grandes_op_l = st.number_input("Grandes Oportunidades (1T)", 0, 10, 1, key="go_l_ht")

    with col_s2:
        tiros_v_base = st.number_input("Tiros Previstos / Totales (Visitante)", 1, 30, 9, key="t_v_base")
        goles_esp_v = st.number_input("xG / Goles Esperados Base (Visitante)", 0.1, 5.0, 1.1, key="xg_v_base")
        disparos_puerta_v = st.number_input("Disparos a Puerta (1T)", 0, 15, 2, key="dp_v_ht")
        pases_comp_v = st.number_input("Pases Completados (1T)", 0, 600, 180, key="pc_v_ht")
        toques_area_v = st.number_input("Toques en Área Rival (1T)", 0, 100, 8, key="ta_v_ht")
        grandes_op_v = st.number_input("Grandes Oportunidades (1T)", 0, 10, 0, key="go_v_ht")

    if st.button("🔮 Calcular Proyección Científica para el 2do Tiempo", type="primary"):
        np.random.seed(42)
        
        # Fórmula ponderada avanzada que evalúa volumen de juego (pases), peligro (toques en área) y eficacia (tiros y grandes ocasiones)
        peso_local = (disparos_puerta_l * 0.3) + (toques_area_l * 0.2) + (grandes_op_l * 0.4) + (pases_comp_l * 0.01)
        peso_vis = (disparos_puerta_v * 0.3) + (toques_area_v * 0.2) + (grandes_op_v * 0.4) + (pases_comp_v * 0.01)
        
        # Tasa esperada de goles para los 45 min restantes del 2T
        lambda_l_2t = max(0.25, peso_local * 0.12)
        lambda_v_2t = max(0.20, peso_vis * 0.12)
        
        # Simulación de Poisson para el 2T
        goles_l_2t_sim = np.random.poisson(lambda_l_2t)
        goles_v_2t_sim = np.random.poisson(lambda_v_2t)
        
        # Marcador final proyectado
        final_proyectado_l = goles_local_ht + goles_l_2t_sim
        final_proyectado_v = goles_vis_ht + goles_v_2t_sim
        
        st.markdown("---")
        st.success(f"🎯 **Marcador Proyectado al Final del Partido:** Local **{final_proyectado_l} - {final_proyectado_v}** Visitante")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Goles Estimados 2T (Local)", f"+{goles_l_2t_sim} goles", f"Ritmo ofensivo: {round(peso_local, 1)}")
        col_res2.metric("Goles Estimados 2T (Visitante)", f"+{goles_v_2t_sim} goles", f"Ritmo ofensivo: {round(peso_vis, 1)}")
        
        if grandes_op_l > grandes_op_v and toques_area_l > toques_area_v:
            st.info("💡 **Análisis Táctico:** El equipo local dominó territorialmente y generó mayor peligro en el área rival durante el primer tiempo; el modelo proyecta que mantendrá esa inercia o concretará más ocasiones si la visita no ajusta.")
        elif grandes_op_v > grandes_op_l:
            st.info("💡 **Análisis Táctico:** A pesar de la paridad, la visita demostró mayor colmillo y conversión en sus toques de área; peligro latente de contragolpe para el complemento.")
        else:
            st.info("💡 **Análisis Táctico:** Partido sumamente disputado en mediocampo con pocas diferencias en la construcción de pases; el segundo tiempo se define por detalles o errores tácticos.")

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

# =========================================================
# MÓDULO DE PREDICCIÓN EN VIVO DESDE EL MEDIO TIEMPO (HT to FT AVANZADO)
# =========================================================

st.markdown("---")
st.subheader("⏱️ Pronóstico Avanzado en Vivo (Medio Tiempo a Final)")
st.write("Ingresa las estadísticas detalladas del 1er Tiempo para que el modelo proyecte el rendimiento y marcador final del partido.")

with st.expander("📊 Panel de Métricas Detalladas del 1er Tiempo", expanded=True):
    col_ht_l, col_ht_v = st.columns(2)
    
    with col_ht_l:
        st.markdown("#### 🏠 Equipo Local (1T)")
        goles_local_ht = st.number_input("Goles (HT - Local)", 0, 10, 0, key="g_l_ht")
        disparos_tot_l = st.number_input("Disparos Totales (1T)", 0, 30, 6, key="dt_l_ht")
        disparos_puerta_l = st.number_input("Disparos a Puerta (1T)", 0, 15, 3, key="dp_l_ht")
        pases_comp_l = st.number_input("Pases Completados (1T)", 0, 600, 220, key="pc_l_ht")
        toques_area_l = st.number_input("Toques en Área Rival (1T)", 0, 100, 12, key="ta_l_ht")
        grandes_op_l = st.number_input("Grandes Oportunidades (1T)", 0, 10, 1, key="go_l_ht")

    with col_ht_v:
        st.markdown("#### ✈️ Equipo Visitante (1T)")
        goles_vis_ht = st.number_input("Goles (HT - Visitante)", 0, 10, 0, key="g_v_ht")
        disparos_tot_v = st.number_input("Disparos Totales (1T)", 0, 30, 4, key="dt_v_ht")
        disparos_puerta_v = st.number_input("Disparos a Puerta (1T)", 0, 15, 2, key="dp_v_ht")
        pases_comp_v = st.number_input("Pases Completados (1T)", 0, 600, 180, key="pc_v_ht")
        toques_area_v = st.number_input("Toques en Área Rival (1T)", 0, 100, 8, key="ta_v_ht")
        grandes_op_v = st.number_input("Grandes Oportunidades (1T)", 0, 10, 0, key="go_v_ht")
        
    if st.button("🔮 Calcular Proyección Científica para el 2do Tiempo", type="primary"):
        np.random.seed(42)
        
        # Fórmula ponderada avanzada que evalúa volumen de juego (pases), peligro (toques en área) y eficacia (tiros y grandes ocasiones)
        peso_local = (disparos_puerta_l * 0.3) + (toques_area_l * 0.2) + (grandes_op_l * 0.4) + (pases_comp_l * 0.01)
        peso_vis = (disparos_puerta_v * 0.3) + (toques_area_v * 0.2) + (grandes_op_v * 0.4) + (pases_comp_v * 0.01)
        
        # Tasa esperada de goles para los 45 min restantes del 2T
        lambda_l_2t = max(0.25, peso_local * 0.12)
        lambda_v_2t = max(0.20, peso_vis * 0.12)
        
        # Simulación de Poisson para el 2T
        goles_l_2t_sim = np.random.poisson(lambda_l_2t)
        goles_v_2t_sim = np.random.poisson(lambda_v_2t)
        
        # Marcador final proyectado
        final_proyectado_l = goles_local_ht + goles_l_2t_sim
        final_proyectado_v = goles_vis_ht + goles_v_2t_sim
        
        st.markdown("---")
        st.success(f"🎯 **Marcador Proyectado al Final del Partido:** Local **{final_proyectado_l} - {final_proyectado_v}** Visitante")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Goles Estimados 2T (Local)", f"+{goles_l_2t_sim} goles", f"Ritmo ofensivo: {round(peso_local, 1)}")
        col_res2.metric("Goles Estimados 2T (Visitante)", f"+{goles_v_2t_sim} goles", f"Ritmo ofensivo: {round(peso_vis, 1)}")
        
        if grandes_op_l > grandes_op_v and toques_area_l > toques_area_v:
            st.info("💡 **Análisis Táctico:** El equipo local dominó territorialmente y generó mayor peligro en el área rival durante el primer tiempo; el modelo proyecta que mantendrá esa inercia o concretará más ocasiones si la visita no ajusta.")
        elif grandes_op_v > grandes_op_l:
            st.info("💡 **Análisis Táctico:** A pesar de la paridad, la visita demostró mayor colmillo y conversión en sus toques de área; peligro latente de contragolpe para el complemento.")
        else:
            st.info("💡 **Análisis Táctico:** Partido sumamente disputado en mediocampo con pocas diferencias en la construcción de pases; el segundo tiempo se define por detalles o errores tácticos.")



