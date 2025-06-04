import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- Coordenadas proporcionadas ---
coordenadas = {
    "BOGOTA": (4.711, -74.0721),
    "CALI": (3.4516, -76.531985),
    "BARRANQUILLA": (10.9639, -74.7964),
    "SOLEDAD": (10.9184, -74.7679),
    "ITAGUI": (6.1719, -75.611),
    "CARTAGENA": (10.391, -75.4794),
    "GUACHENE": (3.1576, -76.3953),
    "BECERRIL": (9.7031, -73.2736),
    "YOPAL": (5.3494, -72.4094),
    "MEDELLIN": (6.2518, -75.5636),
    "ANORÍ": (7.1833, -75.0833),
    "BELLO": (6.3333, -75.5667),
    "BUCARAMANGA": (7.1193, -73.1227),
    "BARRANCABERMEJA": (7.0653, -73.8547),
    "CHIA": (4.858, -74.058),
    "FLORIDABLANCA": (7.0638, -73.0877),
    "GIRÓN": (7.0716, -73.1687),
    "MANIZALEZ": (5.07, -75.5206),
    "MONTERIA": (8.75, -75.88),
    "MOSQUERA": (4.7089, -74.2306),
    "PALMIRA": (3.5399, -76.3039),
    "PIEDECUESTA": (7.0722, -73.05),
    "PEREIRA": (4.8143, -75.6946),
    "RIO NEGRO SANTANDER": (7.3706, -73.1814),
    "RIO ORO CESAR": (8.2749, -73.166),
    "SOGAMOSO": (5.7146, -72.9331),
    "SOACHA": (4.5793, -74.2168),
    "TOCANCIPA": (4.9639, -73.9167),
}

# --- Tus datos ---
data = {
    "Ciudad": list(coordenadas.keys()),
    "ICA": [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "RETEICA": [6, 6, 12, 12, 6, 6, 6, 6, 6, 0] + [None] * 18,
    "Factura": [None, None, None, None, 12, None, None, None, None, None] + [None] * 18,
}
df = pd.DataFrame(data)

# --- Título ---
st.title("🗺️ Mapa de Ciudades de Colombia según ICA, RETEICA y Factura")

# --- Preparar valores de filtros con opción "Todos" ---
ica_values = ["Todos"] + sorted(df["ICA"].dropna().unique().tolist())
reteica_values = ["Todos"] + sorted(df["RETEICA"].dropna().unique().tolist())
factura_values = ["Todos"] + sorted(df["Factura"].dropna().unique().tolist())

ica_filter = st.selectbox("Selecciona un valor de ICA:", ica_values)
reteica_filter = st.selectbox("Selecciona un valor de RETEICA:", reteica_values)
factura_filter = st.selectbox("Selecciona un valor de Factura:", factura_values)

# --- Filtrar datos ---
filtro = pd.Series([True] * len(df))

if ica_filter != "Todos":
    filtro &= (df["ICA"] == ica_filter)
    
if reteica_filter != "Todos":
    filtro &= (df["RETEICA"] == reteica_filter)

if factura_filter != "Todos":
    filtro &= (df["Factura"] == factura_filter)

ciudades_filtradas = df[filtro]

# --- Crear mapa ---
m = folium.Map(location=[4.5, -74.1], zoom_start=6)

# --- Agregar marcadores con información detallada ---
for _, row in ciudades_filtradas.iterrows():
    ciudad = row["Ciudad"]
    if ciudad in coordenadas:
        lat, lon = coordenadas[ciudad]
        popup_text = f"""<b>{ciudad}</b><br>
        ICA: {row['ICA']}<br>
        RETEICA: {row['RETEICA']}<br>
        Factura: {row['Factura']}"""
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# --- Mostrar solo un mapa ---
st_data = st_folium(m, width=700, height=500)
