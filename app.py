import streamlit as st
import pandas as pd
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components
from drivers.simulation import SimulationDriver
from datetime import datetime
import random

st.set_page_config(
    page_title="NetDevOps Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Style global (vert) ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0fdf4;
    }
    [data-testid="stSidebar"] {
        background-color: #064e3b;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .big-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #064e3b;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #047857;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Historique des automatisations (session) ---
if "automation_logs" not in st.session_state:
    st.session_state.automation_logs = []

# --- Sidebar ---
with st.sidebar:
    st.title("🌐 NetDevOps")
    st.caption("Automation • Observability • Security")
    st.write("---")

    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "📊 Observabilité", "🗺️ Topologie", "⚙️ Automatisation", "🔒 Sécurité"],
        index=0
    )

    st.write("---")
    st.success("Mode : Simulation")
    st.caption("Phase 3 en cours")

# Chargement des données
driver = SimulationDriver()
driver.connect()
devices = driver.get_devices()

data = []
for device in devices:
    info = device.get_info()
    data.append({
        "Nom": info["name"],
        "IP": info["ip"],
        "Type": info["type"].capitalize(),
        "Statut": info["status"].upper(),
        "CPU (%)": info["cpu"],
        "Mémoire (%)": info["memory"],
        "Dernière vue": info["last_seen"]
    })
df = pd.DataFrame(data)

# ====================== PAGES ======================

if page == "🏠 Accueil":
    st.markdown('<p class="big-title">NetDevOps Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Automatisation • Observabilité • Sécurité réseau</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3 style="color:#064e3b; margin-bottom:1rem;">Bienvenue</h3>
        <p style="color:#374151; font-size:1.05rem; line-height:1.6;">
            Cet outil te permet de superviser, automatiser et sécuriser un réseau informatique<br>
            en mode simulation. Conçu pour apprendre les bonnes pratiques NetDevOps.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Équipements totaux", len(devices))
    with col2:
        st.metric("Équipements UP", sum(1 for d in devices if d.status == "up"), delta="Tous opérationnels")
    with col3:
        st.metric("Équipements DOWN", sum(1 for d in devices if d.status == "down"))

    st.write("---")
    st.subheader("Aperçu rapide du réseau")
    st.dataframe(df, use_container_width=True)

elif page == "📊 Observabilité":
    st.title("📊 Observabilité")

    st.subheader("État des équipements")
    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.subheader("Utilisation CPU et Mémoire (temps réel)")
    col_a, col_b = st.columns(2)

    with col_a:
        fig_cpu = px.bar(df, x="Nom", y="CPU (%)", title="CPU (%)", color="CPU (%)", color_continuous_scale="OrRd")
        st.plotly_chart(fig_cpu, use_container_width=True)

    with col_b:
        fig_mem = px.bar(df, x="Nom", y="Mémoire (%)", title="Mémoire (%)", color="Mémoire (%)", color_continuous_scale="Blues")
        st.plotly_chart(fig_mem, use_container_width=True)

    st.write("---")
    st.subheader("🕒 Historique des métriques")
    selected_device = st.selectbox("Choisir un équipement", [d.name for d in devices])

    base_cpu = next(d.cpu for d in devices if d.name == selected_device)
    base_mem = next(d.memory for d in devices if d.name == selected_device)

    history = []
    for i in range(12):
        history.append({
            "Heure": f"{i*5} min",
            "CPU (%)": max(5, min(90, base_cpu + random.randint(-8, 8))),
            "Mémoire (%)": max(10, min(85, base_mem + random.randint(-5, 5)))
        })

    hist_df = pd.DataFrame(history)
    fig_hist = px.line(hist_df, x="Heure", y=["CPU (%)", "Mémoire (%)"], title=f"Évolution - {selected_device}", markers=True)
    st.plotly_chart(fig_hist, use_container_width=True)

elif page == "🗺️ Topologie":
    st.title("🗺️ Topologie du réseau")

    net = Network(height="600px", width="100%", bgcolor="#3b3b3d", font_color="white")
    colors = {
        "router": "#e74c3c",
        "switch": "#3498db",
        "end_device": "#2ecc71"
    }

    for device in devices:
        color = colors.get(device.device_type, "#a7f3d0")
        title = f"{device.name}<br>IP: {device.ip}<br>CPU: {device.cpu}% | RAM: {device.memory}%"
        net.add_node(device.name, label=device.name, title=title, color=color, size=25)

    net.add_edge("R1-Core", "R2-Edge")
    net.add_edge("R1-Core", "SW1-Access")
    net.add_edge("R1-Core", "SW2-Access")
    net.add_edge("SW1-Access", "PC-Admin")
    net.add_edge("SW2-Access", "Server-Web")

    net.save_graph("topology.html")
    with open("topology.html", "r", encoding="utf-8") as f:
        html = f.read()

    components.html(html, height=620)
    st.caption("Astuce : tu peux déplacer les nœuds avec la souris.")

elif page == "⚙️ Automatisation":
    st.title("⚙️ Automatisation")

    st.subheader("Actions disponibles")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💾 Backup de configuration")
        target_backup = st.selectbox("Équipement à sauvegarder", [d.name for d in devices], key="backup_select")
        if st.button("Lancer le backup", key="btn_backup"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log = {
                "Date": now,
                "Action": "Backup configuration",
                "Équipement": target_backup,
                "Statut": "Succès",
                "Détail": f"Backup simulé de {target_backup}"
            }
            st.session_state.automation_logs.insert(0, log)
            st.success(f"Backup de **{target_backup}** effectué avec succès (simulation)")

    with col2:
        st.markdown("### 📡 Déploiement de VLAN")
        target_vlan = st.selectbox("Équipement cible", [d.name for d in devices if d.device_type in ["switch", "router"]], key="vlan_select")
        vlan_id = st.number_input("ID du VLAN", min_value=1, max_value=4094, value=10)
        if st.button("Déployer le VLAN", key="btn_vlan"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log = {
                "Date": now,
                "Action": "Déploiement VLAN",
                "Équipement": target_vlan,
                "Statut": "Succès",
                "Détail": f"VLAN {vlan_id} déployé sur {target_vlan}"
            }
            st.session_state.automation_logs.insert(0, log)
            st.success(f"VLAN **{vlan_id}** déployé sur **{target_vlan}** (simulation)")

    st.write("---")
    st.subheader("📜 Journal des automatisations")

    if st.session_state.automation_logs:
        logs_df = pd.DataFrame(st.session_state.automation_logs)
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("Aucune action effectuée pour le moment.")

elif page == "🔒 Sécurité":
    st.title("🔒 Sécurité & Conformité")
    st.info("Section en construction (Phase 4)")
    st.write("Ici on ajoutera :")
    st.markdown("""
    - Authentification et rôles
    - Détection d'appareils non autorisés
    - Contrôles de conformité
    - Score de sécurité
    """)