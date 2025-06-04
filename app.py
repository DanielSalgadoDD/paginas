import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Simulación de tu DataFrame
data = {
    "Ciudad": ["BOGOTA", "CALI", "MEDELLIN", "CARTAGENA", "BARRANQUILLA", "BOGOTA", "MEDELLIN"],
    "ICA": ["Sí", "No", "Sí", "No", "Sí", "No", "Sí"],
    "ReteICA": ["Sí", "Sí", "No", "No", "Sí", "No", "Sí"],
    "Factura": ["Sí", "Sí", "No", "Sí", "No", "Sí", "No"]
}
df = pd.DataFrame(data)

# Coordenadas de ciudades
coordenadas = {
    "BOGOTA": (4.711, -74.0721),
    "CALI": (3.4516, -76.531985),
    "BARRANQUILLA": (10.9639, -74.7964),
    "MEDELLIN": (6.2518, -75.5636),
    "CARTAGENA": (10.391, -75.4794),
}

# --- Interfaz ---
st.title("🌆 Mapa de Ciudades de Colombia con Filtros")

# Filtros
ica_filter = st.selectbox("Filtrar por ICA", ["Todos"] + sorted(df["ICA"].unique().tolist()))
reteica_filter = st.selectbox("Filtrar por ReteICA", ["Todos"] + sorted(df["ReteICA"].unique().tolist()))
factura_filter = st.selectbox("Filtrar por Factura", ["Todos"] + sorted(df["Factura"].unique().tolist()))

# Aplicar filtros
df_filtrado = df.copy()
if ica_filter != "Todos":
    df_filtrado = df_filtrado[df_filtrado["ICA"] == ica_filter]
if reteica_filter != "Todos":
    df_filtrado = df_filtrado[df_filtrado["ReteICA"] == reteica_filter]
if factura_filter != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Factura"] == factura_filter]

# Crear mapa
m = folium.Map(location=[4.5709, -74.2973], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

# Agregar marcadores
for ciudad in df_filtrado["Ciudad"].unique():
    if ciudad in coordenadas:
        lat, lon = coordenadas[ciudad]
        folium.Marker(location=[lat, lon], popup=ciudad).add_to(marker_cluster)

# Mostrar mapa
st_folium(m, width=700, height=500)
