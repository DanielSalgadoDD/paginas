import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import time
import random

# Título de la aplicación
st.title("Mapa Tributario por Empresa")

# Crear pestañas
tabs = st.tabs(["🏢 Bases Centrales", "📍 Ciudades ICA"])

# ------------------ PESTAÑA 1 ------------------
with tabs[0]:
    st.subheader("Bases centrales")

    # Diccionario con datos fijos
    empresas = {
        "MEXICHEM": {"location": [4.60971, -74.08175], "color": "darkblue"},
        "PDO": {"location": [3.0326, -76.4081], "color": "lightblue"},
        "CELTA": {"location": [6.2442, -75.5812], "color": "red"},
    }

    # Crear el mapa centrado en Colombia
    mapa_bases = folium.Map(location=[5.0, -74.0], zoom_start=6)

    # Agregar los marcadores
    for nombre, info in empresas.items():
        folium.Marker(
            location=info["location"],
            popup=nombre,
            icon=folium.Icon(color=info["color"])
        ).add_to(mapa_bases)

    # Mostrar el mapa en Streamlit
    folium_static(mapa_bases)

# ------------------ PESTAÑA 2 ------------------
with tabs[1]:
    st.subheader("Ciudades con ICA")

    # Datos de ejemplo (pegados desde la entrada del usuario)
    data = """
Ciudad	ICA	RETEICA / autorretencion	Factura	ALUMBRADO	EMPRESA
Bogota	6	6	NO	NO	Mexichem
Cali	6	6	NO	NO	Mexichem
Barranquilla	1	12	NO	NO	Mexichem
Soledad	1	12	NO	NO	Mexichem
Itagui	1	6	12	NO	Mexichem
Cartagena	1	6	NO	NO	Mexichem
Guachene	1	6	NO	NO	Mexichem
Becerril	1	6	NO	NO	Mexichem
Yopal	1	6	NO	NO	Mexichem
Medellin	1	NO	NO	NO	Mexichem
ANORÍ	1	NO	NO	NO	Mexichem
BELLO	1	NO	NO	NO	Mexichem
BUCARAMANGA	1	NO	NO	NO	Mexichem
BARRANCABERMEJA	1	NO	NO	NO	Mexichem
CHIA	1	NO	NO	NO	Mexichem
FLORIDABLANCA	1	NO	NO	NO	Mexichem
GIRÓN	1	NO	NO	NO	Mexichem
MANIZALEZ	1	NO	NO	NO	Mexichem
MONTERIA	1	NO	NO	NO	Mexichem
MOSQUERA	1	NO	NO	NO	Mexichem
PALMIRA	1	NO	NO	NO	Mexichem
PIEDECUESTA	1	NO	NO	NO	Mexichem
PEREIRA	1	NO	NO	NO	Mexichem
RIO NEGRO SANTANDER	1	NO	NO	NO	Mexichem
RIO ORO CESAR	1	NO	NO	NO	Mexichem
SOGAMOSO	1	NO	NO	NO	Mexichem
SOACHA	1	NO	NO	NO	Mexichem
TOCANCIPA	1	NO	NO	NO	Mexichem
Bogota	0	6	NO	NO	PDO
Cali	0	6	NO	NO	PDO
Barranquilla	0	12	NO	NO	PDO
Guachene	1	6	NO	24	PDO
Bogota	6	6	NO	NO	CELTA
Cali	6	6	NO	NO	CELTA
Barranquilla	1	12	NO	NO	CELTA
Soledad	1	12	NO	NO	CELTA
Guachene	1	6	NO	NO	CELTA
"""
    from io import StringIO
    df = pd.read_csv(StringIO(data), sep="\t")

    # Opciones de filtros
    ica_options = df['ICA'].unique()
    reteica_options = df['RETEICA / autorretencion'].unique()
    factura_options = df['Factura'].unique()

    # Filtros en la barra lateral
    ica_filter = st.sidebar.selectbox("Filtrar por ICA", options=ica_options)
    reteica_filter = st.sidebar.selectbox("Filtrar por RETEICA", options=reteica_options)
    factura_filter = st.sidebar.selectbox("Filtrar por Factura", options=factura_options)

    # Aplicar filtros al DataFrame
    df_filtrado = df[
        (df['ICA'] == ica_filter) &
        (df['RETEICA / autorretencion'] == reteica_filter) &
        (df['Factura'] == factura_filter)
    ]

    # Mostrar tabla con los resultados filtrados
    st.dataframe(df_filtrado)

    # Geolocalizador con cache para no exceder límite de uso
    @st.cache_data(show_spinner=False)
    def geolocalizar_ciudad(ciudad):
        geolocator = Nominatim(user_agent="mi_app_geocoder")
        try:
            location = geolocator.geocode(f"{ciudad}, Colombia", timeout=10)
            if location:
                return [location.latitude, location.longitude]
        except:
            return None
        return None

    # Crear el mapa
    mapa = folium.Map(location=[5.0, -74.0], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(mapa)

    # Colores por empresa
    color_por_empresa = {
        "Mexichem": "darkblue",
        "PDO": "lightblue",
        "CELTA": "red"
    }

    # Contador para ajustar coordenadas si hay duplicados
    ciudad_empresa_count = {}

    # Agregar marcadores
    for idx, row in df_filtrado.iterrows():
        ciudad = row['Ciudad'].title()
        empresa = row['EMPRESA']
        color = color_por_empresa.get(empresa.upper(), "gray")

        key = (ciudad, empresa)
        count = ciudad_empresa_count.get(ciudad, 0)
        coords = geolocalizar_ciudad(ciudad)

        if coords:
            # Ajustar ligeramente lat/lon si hay múltiples puntos en la misma ciudad
            lat_offset = (random.random() - 0.5) * 0.02
            lon_offset = (random.random() - 0.5) * 0.02
            coords[0] += lat_offset * count
            coords[1] += lon_offset * count

            popup_text = f"{ciudad} - {empresa}"
            folium.Marker(
                location=coords,
                popup=popup_text,
                icon=folium.Icon(color=color)
            ).add_to(marker_cluster)

        ciudad_empresa_count[ciudad] = count + 1

    # Mostrar mapa
    folium_static(mapa)
