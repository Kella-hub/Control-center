import streamlit as st
import pandas as pd
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components
from drivers.simulation import SimulationDriver

st.set_page_config(
    page_title="NetDevOps Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 NetDevOps Dashboard")
st.subheader("Automation • Observability • Security")
st.write("---")

# Chargement des données
driver = SimulationDriver()
driver.connect()
devices = driver.get_devices()

# --- Observabilité ---
st.header("📊 Observabilité - État des équipements")

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
st.dataframe(df, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Équipements totaux", len(devices))
col2.metric("Équipements UP", sum(1 for d in devices if d.status == "up"))
col3.metric("Équipements DOWN", sum(1 for d in devices if d.status == "down"))

st.write("---")

# Graphiques
st.subheader("📈 Utilisation CPU et Mémoire")
col_a, col_b = st.columns(2)

with col_a:
    fig_cpu = px.bar(df, x="Nom", y="CPU (%)", title="Utilisation CPU (%)", color="CPU (%)", color_continuous_scale="OrRd")
    st.plotly_chart(fig_cpu, use_container_width=True)

with col_b:
    fig_mem = px.bar(df, x="Nom", y="Mémoire (%)", title="Utilisation Mémoire (%)", color="Mémoire (%)", color_continuous_scale="Blues")
    st.plotly_chart(fig_mem, use_container_width=True)

st.write("---")

# --- Topologie ---
st.subheader("🗺️ Topologie du réseau (simulation)")

net = Network(height="500px", width="100%", bgcolor="#0e1117", font_color="white")

# Couleurs selon le type
colors = {
    "router": "#e74c3c",
    "switch": "#3498db",
    "end_device": "#2ecc71"
}

for device in devices:
    color = colors.get(device.device_type, "#95a5a6")
    title = f"{device.name}<br>IP: {device.ip}<br>CPU: {device.cpu}% | RAM: {device.memory}%"
    net.add_node(device.name, label=device.name, title=title, color=color, size=25)

# Liens simples de simulation
net.add_edge("R1-Core", "R2-Edge")
net.add_edge("R1-Core", "SW1-Access")
net.add_edge("R1-Core", "SW2-Access")
net.add_edge("SW1-Access", "PC-Admin")
net.add_edge("SW2-Access", "Server-Web")

net.save_graph("topology.html")
with open("topology.html", "r", encoding="utf-8") as f:
    html = f.read()

components.html(html, height=520)

st.success("Phase 2 en cours • Topologie interactive ajoutée")