import streamlit as st
from drivers.simulation import SimulationDriver

st.set_page_config(
    page_title="NetDevOps Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("NetDevOps Dashboard")
st.subheader("Automation • Observability • Security")
st.write("---")

driver = SimulationDriver()
driver.connect()
devices = driver.get_devices()

st.success(f"{len(devices)} équipements chargés (simulation)")

for device in devices:
    info = device.get_info()
    st.write(f"**{info['name']}** ({info['ip']}) — {info['type']} — CPU: {info['cpu']}% — RAM: {info['memory']}% — {info['status']}")