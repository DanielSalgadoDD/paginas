# app.py
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
from geopy.geocoders import Nominatim

# Datos
data = {
    "Ciudad": ["Bogota", "Cali", "Barranquilla", "Soledad", "Itagui", "Cartagena", "Guachene", "Becerril", "Yopal",
               "Medellin", "ANORÍ", "BELLO", "BUCARAMANGA", "BARRANCABERMEJA", "CHIA", "FLORIDABLANCA", "GIRÓN",
               "MANIZALEZ", "MONTERIA", "MOSQUERA", "PALMIRA", "PIEDECUESTA", "PEREIRA", "RIO NEGRO SANTANDER",
               "RIO ORO CESAR", "SOGAMOSO", "SOACHA", "TOCANCIPA"],
    "ICA": [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "RETEICA / autorretencion": [6, 6, 12, 12, 6, 6, 6, 6, 6, 0] + [None]*18,
    "Factura": [None, None, None, None, 12, None, None, None, None, None] + [None]*18
}
df = pd.DataFrame(data)

# Obtener coordenadas
geolocator = Nominatim(user_agent="mapa_app")
def obtener_coord(ciudad):
    try:
        location = geolocator.geocode(f"{ciudad}, Colombia")
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        return pd.Series([None, None])
    return pd.Series([None, None])

df[["lat", "lon"]] = df["Ciudad"].apply(lambda x: obtener_coord(x.strip().upper()))

# Interfaz
st.title("Mapa Interactivo de Ciudades de Colombia")
ica_min, ica_max = st.slider("Filtrar por ICA", 1, 6, (1, 6))
df_filtrado = df[df["ICA"].between(ica_min, ica_max)]

# Mapa centrado en Colombia
mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6)
for _, row in df_filtrado.dropna(subset=["lat", "lon"]).iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['Ciudad']}<br>ICA: {row['ICA']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mapa)

folium_static(mapa)

