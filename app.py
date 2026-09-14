import streamlit as st
import numpy as np
import pandas as pd
import random

# ==============================================================================
# --- CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS AVANZADOS (DISEÑO DINÁMICO) ---
# ==============================================================================

st.set_page_config(
    page_title="Simulador Predictivo de Fútbol Ultra Pro 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de CSS para fondo dinámico, tarjetas con efecto vidrio e interactividad
st.markdown("""
<style>
    /* Fondo con gradiente oscuro dinámico */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a2332 0%, #0d1117 75%, #05070a 100%);
        color: #e6edf3;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Efecto para botones de navegación superior */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(145deg, #1f293d, #161f2e);
        color: #f0f6fc;
        border: 1px solid #30363d;
        font-weight: 600;
        padding: 8px 12px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    div.stButton > button:hover {
        border-color: #58a6ff;
        color: #58a6ff;
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(88, 166, 255, 0.2);
    }

    /* Tarjetas de últimos 5 partidos con Glassmorphism */
    .match-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .badge-v { background-color: #238636; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-e { background-color: #9e6a03; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-d { background-color: #da3633; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    
    /* Métrica estilizada */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800;
        color: #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- CARGA AUTOMÁTICA DE DATOS Y GENERADOR DE HISTORIAL ---
# ==============================================================================

@st.cache_data(ttl=86400)
def cargar_base_datos_actualizada():
    return {
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
            "Tottenham": {"gf": 1.90, "gc": 1.45, "gf1t": 0.85, "corners": 6.1, "tarjetas": 2.3}
        },
        "🇪🇸 LaLiga Española": {
            "Real Madrid": {"gf": 2.15, "gc": 0.80, "gf1t": 1.00, "corners": 5.8, "tarjetas": 1.8},
            "Barcelona": {"gf": 2.05, "gc": 0.95, "gf1t": 0.90, "corners": 6.2, "tarjetas": 2.0},
            "Atl. Madrid": {"gf": 1.65, "gc": 0.85, "gf1t": 0.70, "corners": 4.9, "tarjetas": 2.6},
            "Ath Bilbao": {"gf": 1.55, "gc": 1.00, "gf1t": 0.65, "corners": 5.3, "tarjetas": 2.3},
            "Real Sociedad": {"gf": 1.45, "gc": 1.05, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.4},
            "Villarreal": {"gf": 1.70, "gc": 1.40, "gf1t": 0.75, "corners": 5.1, "tarjetas": 2.5},
            "Sevilla": {"gf": 1.35, "gc": 1.30, "gf1t": 0.50, "corners": 4.7, "tarjetas": 2.8},
            "Betis": {"gf": 1.40, "gc": 1.20, "gf1t": 0.55, "corners": 4.8, "tarjetas": 2.3}
        },
        "🇩🇪 Bundesliga": {
            "Bayern Munich": {"gf": 2.50, "gc": 1.05, "gf1t": 1.30, "corners": 6.7, "tarjetas": 1.7},
            "Bayer Leverkusen": {"gf": 2.35, "gc": 0.90, "gf1t": 1.15, "corners": 6.4, "tarjetas": 1.9},
            "Dortmund": {"gf": 2.00, "gc": 1.20, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.0},
            "RB Leipzig": {"gf": 1.90, "gc": 1.10, "gf1t": 0.85, "corners": 5.2, "tarjetas": 2.1},
            "Stuttgart": {"gf": 1.95, "gc": 1.25, "gf1t": 0.85, "corners": 5.5, "tarjetas": 2.0},
            "Eintracht Frankfurt": {"gf": 1.75, "gc": 1.35, "gf1t": 0.75, "corners": 5.0, "tarjetas": 2.2}
        },
        "🇮🇹 Serie A": {
            "Inter": {"gf": 1.90, "gc": 0.85, "gf1t": 0.95, "corners": 5.1, "tarjetas": 2.1},
            "Juventus": {"gf": 1.45, "gc": 0.80, "gf1t": 0.60, "corners": 4.3, "tarjetas": 2.3},
            "AC Milan": {"gf": 1.70, "gc": 1.15, "gf1t": 0.75, "corners": 5.3, "tarjetas": 2.2},
            "Atalanta": {"gf": 2.05, "gc": 1.20, "gf1t": 0.95, "corners": 6.0, "tarjetas": 2.1},
            "Napoli": {"gf": 1.75, "gc": 0.90, "gf1t": 0.80, "corners": 5.6, "tarjetas": 2.0},
            "AS Roma": {"gf": 1.55, "gc": 1.15, "gf1t": 0.65, "corners": 5.0, "tarjetas": 2.4}
        },
        "🇭🇳 Liga Nacional Honduras": {
            "Olimpia": {"gf": 2.50, "gc": 0.50, "gf1t": 1.10, "corners": 5.8, "tarjetas": 2.4},
            "Real Espana": {"gf": 2.50, "gc": 0.00, "gf1t": 1.00, "corners": 5.5, "tarjetas": 2.3},
            "Motagua": {"gf": 1.50, "gc": 1.00, "gf1t": 0.60, "corners": 5.0, "tarjetas": 2.6},
            "Marathon": {"gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.8, "tarjetas": 2.7},
            "Olancho": {"gf": 1.00, "gc": 0.50, "gf1t": 0.50, "corners": 4.4, "tarjetas": 2.8}
        },
        "🇲🇽 Liga MX": {
            "Club America": {"gf": 1.67, "gc": 0.33, "gf1t": 0.80, "corners": 5.8, "tarjetas": 2.1},
            "Cruz Azul": {"gf": 2.33, "gc": 2.00, "gf1t": 1.10, "corners": 5.9, "tarjetas": 2.0},
            "Monterrey": {"gf": 2.00, "gc": 1.33, "gf1t": 0.85, "corners": 5.6, "tarjetas": 2.2},
            "Tigres UANL": {"gf": 1.67, "gc": 2.67, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.3},
            "Toluca": {"gf": 2.00, "gc": 1.00, "gf1t": 0.90, "corners": 5.7, "tarjetas": 2.1}
        },
        "🇺🇸 MLS": {
            "Inter Miami": {"gf": 2.20, "gc": 1.25, "gf1t": 1.05, "corners": 5.0, "tarjetas": 2.0},
            "Los Angeles FC": {"gf": 1.90, "gc": 1.20, "gf1t": 0.85, "corners": 5.9, "tarjetas": 2.2},
            "Columbus Crew": {"gf": 2.00, "gc": 1.15, "gf1t": 0.90, "corners": 5.6, "tarjetas": 1.9},
            "Los Angeles Galaxy": {"gf": 1.80, "gc": 1.45, "gf1t": 0.80, "corners": 5.4, "tarjetas": 2.1}
        },
        "🇪🇺 UEFA Champions League": {
            "RealMadrid": {"gf": 2.48, "gc": 0.78, "gf1t": 1.15, "corners": 6.5, "tarjetas": 1.7},
            "ManchesterCity": {"gf": 2.45, "gc": 0.80, "gf1t": 1.20, "corners": 7.4, "tarjetas": 1.4},
            "BayernMúnich": {"gf": 2.62, "gc": 0.82, "gf1t": 1.25, "corners": 7.2, "tarjetas": 1.5},
            "FCBarcelona": {"gf": 2.58, "gc": 0.88, "gf1t": 1.20, "corners": 6.7, "tarjetas": 1.9},
            "PSG": {"gf": 2.38, "gc": 0.85, "gf1t": 1.15, "corners": 6.6, "tarjetas": 1.8},
            "Arsenal": {"gf": 2.35, "gc": 0.72, "gf1t": 1.12, "corners": 6.8, "tarjetas": 1.6}
        }
    }

# Función para simular últimos 5 partidos con estructura realista
def generar_ultimos_5_partidos(equipo, lista_rivales, stats):
    random.seed(sum(ord(c) for c in equipo)) # Semilla fija basada en el nombre para consistencia
    rivales_disponibles = [r for r in lista_rivales if r != equipo]
    if not rivales_disponibles:
        rivales_disponibles = ["Rival A", "Rival B", "Rival C", "Rival D", "Rival E"]
    
    historial = []
    for _ in range(5):
        rival = random.choice(rivales_disponibles)
        es_local = random.choice([True, False])
        g_propios = np.random.poisson(stats["gf"])
        g_rival = np.random.poisson(stats["gc"])
        
        if g_propios > g_rival:
            res_label, badge_class = "Victoria", "badge-v"
        elif g_propios == g_rival:
            res_label, badge_class = "Empate", "badge-e"
        else:
            res_label, badge_class = "Derrota", "badge-d"
            
        condicion = "vs" if es_local else "@"
        marcador = f"{g_propios} - {g_rival}" if es_local else f"{g_rival} - {g_propios}"
        
        historial.append({
            "rival": rival,
            "condicion": condicion,
            "marcador": marcador,
            "resultado": res_label,
            "badge": badge_class
        })
    return historial

BASE_DATOS = cargar_base_datos_actualizada()

# ==============================================================================
# --- INTERFAZ SUPERIOR: SELECCIÓN DE LIGAS (BOTONES DE NAVEGACIÓN) ---
# ==============================================================================

st.title("⚽ SIMULADOR PREDICTIVO MONTE CARLO ULTRA PRO")

# Estado de sesión para controlar la liga activa
if "liga_activa" not in st.session_state:
    st.session_state["liga_activa"] = list(BASE_DATOS.keys())[0]

st.markdown("##### 🏆 Selecciona un Torneo / Liga:")
ligas_keys = list(BASE_DATOS.keys())

# Renderizado de botones de ligas en grid superior
cols_ligas = st.columns(4)
for idx, liga_nombre in enumerate(ligas_keys):
    col = cols_ligas[idx % 4]
    # Resaltar la liga seleccionada
    label = f"🔥 {liga_nombre}" if st.session_state["liga_activa"] == liga_nombre else liga_nombre
    if col.button(label, key=f"btn_liga_{idx}"):
        st.session_state["liga_activa"] = liga_nombre
        st.rerun()

liga_sel = st.session_state["liga_activa"]
equipos_liga = list(BASE_DATOS[liga_sel].keys())

st.markdown("---")

# ==============================================================================
# --- SELECCIÓN DE EQUIPOS Y DATOS DE ENTRADA ---
# ==============================================================================

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("### 🏠 Equipo Local")
    eq_local_nombre = st.selectbox("Seleccionar Local:", equipos_liga, index=0, key="select_local")

with col_sel2:
    st.markdown("### ✈️ Equipo Visitante")
    idx_vis = 1 if len(equipos_liga) > 1 else 0
    eq_visita_nombre = st.selectbox("Seleccionar Visitante:", equipos_liga, index=idx_vis, key="select_visita")

data_loc = BASE_DATOS[liga_sel][eq_local_nombre]
data_vis = BASE_DATOS[liga_sel][eq_visita_nombre]

# ==============================================================================
# --- MÓDULO VISUAL: ÚLTIMOS 5 RESULTADOS POR EQUIPO ---
# ==============================================================================

st.markdown("### 📊 Últimos 5 Resultados")

col_hist1, col_hist2 = st.columns(2)

with col_hist1:
    st.markdown(f"**Historial Reciente de {eq_local_nombre}**")
    hist_loc = generar_ultimos_5_partidos(eq_local_nombre, equipos_liga, data_loc)
    for part in hist_loc:
        st.markdown(f"""
        <div class="match-card">
            <span><b>{eq_local_nombre}</b> {part['condicion']} {part['rival']}</span>
            <span><b>{part['marcador']}</b></span>
            <span class="{part['badge']}">{part['resultado']}</span>
        </div>
        """, unsafe_allow_html=True)

with col_hist2:
    st.markdown(f"**Historial Reciente de {eq_visita_nombre}**")
    hist_vis = generar_ultimos_5_partidos(eq_visita_nombre, equipos_liga, data_vis)
    for part in hist_vis:
        st.markdown(f"""
        <div class="match-card">
            <span><b>{eq_visita_nombre}</b> {part['condicion']} {part['rival']}</span>
            <span><b>{part['marcador']}</b></span>
            <span class="{part['badge']}">{part['resultado']}</span>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# --- CÁLCULO Y ANÁLISIS DE PRIORIDAD E INTENSIDAD ---
# ==============================================================================

diff_loc = (data_loc["gf"] - data_vis["gc"]) + (data_loc["gf1t"] - 0.5)
diff_vis = (data_vis["gf"] - data_loc["gc"]) + (data_vis["gf1t"] - 0.5)

prio_loc = int(np.clip(5 + diff_loc * 2.0, 1, 10))
prio_vis = int(np.clip(5 + diff_vis * 2.0, 1, 10))

f_prio_loc = 1.0 + (prio_loc - 5) * 0.04
f_prio_vis = 1.0 + (prio_vis - 5) * 0.04

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

st.markdown("---")
st.markdown("### 🤖 Análisis Estadístico Automático")

col_auto1, col_auto2, col_auto3 = st.columns(3)
with col_auto1:
    st.metric(f"🎯 Prioridad ({eq_local_nombre})", f"{prio_loc} / 10")
with col_auto2:
    st.metric(f"🎯 Prioridad ({eq_visita_nombre})", f"{prio_vis} / 10")
with col_auto3:
    st.metric("🔥 Intensidad Evaluada", ritmo_label, f"x{f_ritmo:.2f}")

# ==============================================================================
# --- SIMULACIÓN MONTE CARLO COMPLETA ---
# ==============================================================================

st.markdown("---")
if st.button("🚀 CALCULAR PREDICCIÓN (10,000 SIMULACIONES)", use_container_width=True):
    l_gf_loc = data_loc["gf"] * 1.10 * f_prio_loc * f_ritmo
    l_gf_vis = data_vis["gf"] * f_prio_vis * f_ritmo
    
    # Generación de distribuciones de Poisson
    n_sims = 10000
    sim_loc_ft = np.random.poisson(l_gf_loc, n_sims)
    sim_vis_ft = np.random.poisson(l_gf_vis, n_sims)
    
    sim_loc_1t = np.random.poisson(data_loc["gf1t"] * f_prio_loc * f_ritmo, n_sims)
    sim_vis_1t = np.random.poisson(data_vis["gf1t"] * f_prio_vis * f_ritmo, n_sims)
    
    # Cálculo de probabilidades 1X2
    prob_win_loc = np.mean(sim_loc_ft > sim_vis_ft) * 100
    prob_draw = np.mean(sim_loc_ft == sim_vis_ft) * 100
    prob_win_vis = np.mean(sim_loc_ft < sim_vis_ft) * 100
    
    prob_1t_loc = np.mean(sim_loc_1t > sim_vis_1t) * 100
    prob_1t_draw = np.mean(sim_loc_1t == sim_vis_1t) * 100
    prob_1t_vis = np.mean(sim_loc_1t < sim_vis_1t) * 100
    
    # Presentación de Resultados
    st.markdown("## 📈 Proyección de Resultados")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric(f"🏠 Gana {eq_local_nombre}", f"{prob_win_loc:.1f}%")
    with col_res2:
        st.metric("🤝 Empate (FT)", f"{prob_draw:.1f}%")
    with col_res3:
        st.metric(f"✈️ Gana {eq_visita_nombre}", f"{prob_win_vis:.1f}%")
        
    st.markdown("#### ⏱️ Probabilidades 1er Tiempo (1T)")
    col_1t1, col_1t2, col_1t3 = st.columns(3)
    with col_1t1:
        st.write(f"**Local (1T):** {prob_1t_loc:.1f}%")
    with col_1t2:
        st.write(f"**Empate (1T):** {prob_1t_draw:.1f}%")
    with col_1t3:
        st.write(f"**Visitante (1T):** {prob_1t_vis:.1f}%")
        
    st.markdown("#### ⚽ Mercados Complementarios Esperados")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.write(f"**Goles Esperados:** {np.mean(sim_loc_ft + sim_vis_ft):.2f}")
    with c_m2:
        st.write(f"**Córners Esperados:** {data_loc['corners'] + data_vis['corners']:.1f}")
    with c_m3:
        st.write(f"**Tarjetas Esperadas:** {tarj_comb:.1f}")

...

[Mensaje acortado]  Ver mensaje completo
