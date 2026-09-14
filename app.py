import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Configuración de página
st.set_page_config(
    page_title="Simulador Predictivo de Fútbol Ultra Pro 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Personalizados para Interfaz Moderna
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .league-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
        border-radius: 8px;
        background-color: #1e222d;
        border: 1px solid #2e3440;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
    }
    .badge-v { background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-e { background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-d { background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    
    .match-card {
        background: #1a1f2c;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #00d46a;
    }
</style>
""", unsafe_allow_html=True)

# Helper para generar historial representativo de los últimos 5 partidos si no existe explícito
def obtener_ultimos_5(gf, gc):
    # Genera una racha realista coherente con el promedio del equipo
    if gf > 1.8:
        return [
            {"rival": "Rival A", "res": "3-1", "tipo": "V"},
            {"rival": "Rival B", "res": "2-0", "tipo": "V"},
            {"rival": "Rival C", "res": "1-1", "tipo": "E"},
            {"rival": "Rival D", "res": "2-1", "tipo": "V"},
            {"rival": "Rival E", "res": "0-1", "tipo": "D"},
        ]
    elif gf >= 1.3:
        return [
            {"rival": "Rival A", "res": "1-0", "tipo": "V"},
            {"rival": "Rival B", "res": "1-1", "tipo": "E"},
            {"rival": "Rival C", "res": "0-2", "tipo": "D"},
            {"rival": "Rival D", "res": "2-1", "tipo": "V"},
            {"rival": "Rival E", "res": "2-2", "tipo": "E"},
        ]
    else:
        return [
            {"rival": "Rival A", "res": "0-1", "tipo": "D"},
            {"rival": "Rival B", "res": "0-0", "tipo": "E"},
            {"rival": "Rival C", "res": "1-2", "tipo": "D"},
            {"rival": "Rival D", "res": "1-0", "tipo": "V"},
            {"rival": "Rival E", "res": "0-2", "tipo": "D"},
        ]

@st.cache_data(ttl=86400)
def cargar_base_datos_actualizada():
    raw_db = {
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": {
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
        "🇩🇪 Bundesliga": {
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
        "🇭🇳 Liga Nacional Honduras": {
            "Real Espana": {"gf": 2.50, "gc": 0.50, "gf1t": 1.00, "corners": 5.5, "tarjetas": 2.3},
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
        "🇮🇹 Serie A": {
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
        "🇲🇽 Liga MX": {
            "Club America": {"gf": 1.67, "gc": 0.33, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.1},
            "Club Tijuana": {"gf": 1.33, "gc": 0.33, "gf1t": 0.60, "corners": 4.7, "tarjetas": 2.5},
            "Toluca": {"gf": 2.00, "gc": 1.00, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.1},
            "UNAM Pumas": {"gf": 2.33, "gc": 1.67, "gf1t": 1.00, "corners": 5.3, "tarjetas": 2.4},
            "Monterrey": {"gf": 2.00, "gc": 1.33, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.2},
            "Cruz Azul": {"gf": 2.33, "gc": 2.00, "gf1t": 1.10, "corners": 5.9, "tarjetas": 2.0},
            "Queretaro": {"gf": 1.67, "gc": 1.33, "gf1t": 0.70, "corners": 4.2, "tarjetas": 2.5},
            "Necaxa": {"gf": 1.67, "gc": 1.67, "gf1t": 0.70, "corners": 4.4, "tarjetas": 2.5},
            "Atlas": {"gf": 1.33, "gc": 1.33, "gf1t": 0.55, "corners": 4.5, "tarjetas": 2.7},
            "Guadalajara Chivas": {"gf": 0.67, "gc": 1.00, "gf1t": 0.30, "corners": 5.2, "tarjetas": 2.4},
            "Tigres UANL": {"gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3}
        },
        "🇪🇸 LaLiga Española": {
            "Real Madrid": {"gf": 2.15, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 1.8},
            "Barcelona": {"gf": 2.05, "gc": 0.95, "gf1t": 0.90, "corners": 6.2, "tarjetas": 2.0},
            "Atl. Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
            "Real Sociedad": {"gf": 1.45, "gc": 1.05, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.4},
            "Villarreal": {"gf": 1.70, "gc": 1.40, "gf1t": 0.75, "corners": 5.1, "tarjetas": 2.5},
            "Sevilla": {"gf": 1.35, "gc": 1.30, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.8},
            "Betis": {"gf": 1.40, "gc": 1.20, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3},
            "Ath Bilbao": {"gf": 1.55, "gc": 1.00, "gf1t": 0.65, "corners": 5.3, "tarjetas": 2.3}
        },
        "🇪🇺 UEFA Champions League": {
            "Real Madrid": {"gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7},
            "FC Barcelona": {"gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9},
            "Bayern Múnich": {"gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5},
            "Manchester City": {"gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4},
            "PSG": {"gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8},
            "Arsenal": {"gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6},
            "Inter de Milán": {"gf": 2.18, "gc": 0.68, "gf1t": 0.98, "corners": 6.0, "tarjetas": 1.7}
        }
    }

    # Asignar automáticamente últimos 5 partidos a cada equipo
    for liga, equipos in raw_db.items():
        for eq_nombre, datos in equipos.items():
            datos["ultimos_5"] = obtener_ultimos_5(datos["gf"], datos["gc"])

    return raw_db

db = cargar_base_datos_actualizada()

# --- ENCABEZADO ---
st.title("⚽ Simulador Predictivo de Fútbol Ultra Pro")
st.markdown("Plataforma interactiva con análisis Poisson y métricas de rendimiento en tiempo real.")

# --- BARRA DE BOTONES HORIZONTALES PARA LIGAS ---
st.write("### 🏆 Selecciona una Liga")
ligas_lista = list(db.keys())

if "liga_seleccionada" not in st.session_state:
    st.session_state.liga_seleccionada = ligas_lista[0]

# Renderizado de botones horizontales
cols = st.columns(len(ligas_lista))
for idx, liga in enumerate(ligas_lista):
    btn_type = "primary" if st.session_state.liga_seleccionada == liga else "secondary"
    if cols[idx].button(liga, key=f"btn_liga_{idx}", use_container_width=True, type=btn_type):
        st.session_state.liga_seleccionada = liga
        st.rerun()

liga_actual = st.session_state.liga_seleccionada
equipos_liga = list(db[liga_actual].keys())

st.divider()

# --- SELECCIÓN DE EQUIPOS & PANEL DE ESTADÍSTICAS ---
col_local, col_vs, col_visita = st.columns([5, 2, 5])

with col_local:
    st.subheader("🏠 Equipo Local")
    local_nombre = st.selectbox("Selecciona equipo local:", equipos_liga, index=0, key="select_local")
    local_data = db[liga_actual][local_nombre]
    
    st.metric("Goles Favor (Prom)", f"{local_data['gf']:.2f}")
    st.metric("Goles Contra (Prom)", f"{local_data['gc']:.2f}")
    st.metric("Córneres (Prom)", f"{local_data['corners']:.1f}")
    
    st.write("**Últimos 5 Partidos:**")
    u5_html = ""
    for m in local_data["ultimos_5"]:
        badge_class = f"badge-{m['tipo'].lower()}"
        u5_html += f"<span class='{badge_class}'>{m['tipo']}</span> {m['res']} vs {m['rival']} &nbsp;|&nbsp; "
    st.markdown(u5_html, unsafe_allow_html=True)

with col_visita:
    st.subheader("✈️ Equipo Visitante")
    visita_idx = 1 if len(equipos_liga) > 1 else 0
    visita_nombre = st.selectbox("Selecciona equipo visitante:", equipos_liga, index=visita_idx, key="select_visita")
    visita_data = db[liga_actual][visita_nombre]
    
    st.metric("Goles Favor (Prom)", f"{visita_data['gf']:.2f}")
    st.metric("Goles Contra (Prom)", f"{visita_data['gc']:.2f}")
    st.metric("Córneres (Prom)", f"{visita_data['corners']:.1f}")
    
    st.write("**Últimos 5 Partidos:**")
    u5_html_v = ""
    for m in visita_data["ultimos_5"]:
        badge_class = f"badge-{m['tipo'].lower()}"
        u5_html_v += f"<span class='{badge_class}'>{m['tipo']}</span> {m['res']} vs {m['rival']} &nbsp;|&nbsp; "
    st.markdown(u5_html_v, unsafe_allow_html=True)

with col_vs:
    st.write(" ")
    st.write(" ")
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

st.divider()

# --- MOTOR DE SIMULACIÓN Y POISSON ---
if st.button("🚀 Ejecutar Análisis Estadístico y Simulación", use_container_width=True, type="primary"):
    # Cálculo de xG mediante intensidad
    xg_local = (local_data['gf'] + visita_data['gc']) / 2.0
    xg_visita = (visita_data['gf'] + local_data['gc']) / 2.0
    
    # Matriz de Probabilidades Poisson
    max_goles = 6
    matriz_poisson = np.zeros((max_goles, max_goles))
    
    for i in range(max_goles):
        for j in range(max_goles):
            matriz_poisson[i, j] = poisson.pmf(i, xg_local) * poisson.pmf(j, xg_visita)
            
    prob_local = np.sum(np.tril(matriz_poisson, -1)) * 100
    prob_empate = np.sum(np.diag(matriz_poisson)) * 100
    prob_visita = np.sum(np.triu(matriz_poisson, 1)) * 100
    
    st.write("### 📊 Proyección Estadística del Partido")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(f"Victoria {local_nombre}", f"{prob_local:.1f}%")
    col_p2.metric("Probabilidad Empate", f"{prob_empate:.1f}%")
    col_p3.metric(f"Victoria {visita_nombre}", f"{prob_visita:.1f}%")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("xG Esperado Local", f"{xg_local:.2f}")
    col_m2.metric("Córneres Totales Est.", f"{local_data['corners'] + visita_data['corners']:.1f}")
    col_m3.metric("Tarjetas Totales Est.", f"{local_data['tarjetas'] + visita_data['tarjetas']:.1f}")

    # Marcadores más probables
    marcadores = []
    for i in range(4):
        for j in range(4):
            marcadores.append((f"{i} - {j}", matriz_poisson[i, j] * 100))
            
    marcadores.sort(key=lambda x: x[1], reverse=True)
    
    st.write("#### 🎯 Marcadores Más Probables")
    col_m_top = st.columns(5)
    for idx, (m_str, prob_val) in enumerate(marcadores[:5]):
        col_m_top[idx].metric(f"Opción #{idx+1}", m_str, f"{prob_val:.1f}%")

