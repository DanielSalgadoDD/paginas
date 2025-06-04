# app.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# ------------------------
# Datos originales
# ------------------------
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

# ------------------------
# Geolocalización de ciudades
# ------------------------
geolocator = Nominatim(user_agent="my-app")

@st.cache_data
def obtener_coord(ciudad):
    try:
        location = geolocator.geocode(ciudad + ", Colombia")
        if location:
            return location.latitude, location.longitude
    except:
        return None, None
    return None, None

# Obtener coordenadas
df[['lat', 'lon']] = df['Ciudad'].apply(lambda x: pd.Series(obtener_coord(x)))

# ------------------------
# Interfaz Streamlit
# ------------------------
st.title("Mapa de Ciudades de Colombia con ICA")

# Selector de ciudades
ciudades_seleccionadas = st.multiselect(
    "Selecciona ciudades para mostrar en el mapa:",
    options=df['Ciudad'].tolist(),
    default=df['Ciudad'].tolist()
)

# Filtrar datos
df_filtrado = df[df['Ciudad'].isin(ciudades_seleccionadas)].dropna(subset=["lat", "lon"])

# ------------------------
# Crear mapa
# ------------------------
m = folium.Map(location=[4.5709, -74.2973], zoom_start=5.3)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['Ciudad']}<br>ICA: {row['ICA']}",
        tooltip=row["Ciudad"]
    ).add_to(marker_cluster)

# Mostrar mapa en Streamlit
st_folium(m, width=700, height=500)

