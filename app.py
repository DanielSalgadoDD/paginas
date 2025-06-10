import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium
import requests
import numpy as np

# -------------------------
# Datos originales
# -------------------------
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
df["ICA"] = pd.to_numeric(df["ICA"], errors='coerce').astype("Int64")
df["RETEICA / autorretencion"] = pd.to_numeric(df["RETEICA / autorretencion"], errors='coerce').astype("Int64")
df["Factura"] = pd.to_numeric(df["Factura"], errors='coerce').astype("Int64")

# -------------------------
# Empresa por ciudad
# -------------------------
empresa_por_ciudad = {
    "Bogota": "MEXICHEM",
    "Cali": "MEXICHEM",
    "Barranquilla": "MEXICHEM",
    "Soledad": "MEXICHEM",
    "Itagui": "CELTA",
    "Cartagena": "MEXICHEM",
    "Guachene": "PDO",
    "Becerril": "PDO",
    "Yopal": "PDO",
    "Medellin": "CELTA",
    "ANORÍ": "CELTA",
    "BELLO": "CELTA",
    "BUCARAMANGA": "CELTA",
    "BARRANCABERMEJA": "CELTA",
    "CHIA": "MEXICHEM",
    "FLORIDABLANCA": "CELTA",
    "GIRÓN": "CELTA",
    "MANIZALEZ": "CELTA",
    "MONTERIA": "PDO",
    "MOSQUERA": "MEXICHEM",
    "PALMIRA": "PDO",
    "PIEDECUESTA": "CELTA",
    "PEREIRA": "PDO",
    "RIO NEGRO SANTANDER": "PDO",
    "RIO ORO CESAR": "PDO",
    "SOGAMOSO": "PDO",
    "SOACHA": "MEXICHEM",
    "TOCANCIPA": "MEXICHEM"
}
df["Empresa"] = df["Ciudad"].apply(lambda c: empresa_por_ciudad.get(c.strip().upper().title(), "OTRA"))

# -------------------------
# Coordenadas por ciudad
# -------------------------
coordenadas_fijas = {
    "Bogota": (4.7110, -74.0721),
    "Cali": (3.4516, -76.5320),
    "Barranquilla": (10.9685, -74.7813),
    "Soledad": (10.9184, -74.7649),
    "Itagui": (6.1719, -75.6111),
    "Cartagena": (10.3910, -75.4794),
    "Guachene": (3.0315, -76.3927),
    "Becerril": (9.7035, -73.2793),
    "Yopal": (5.3378, -72.3959),
    "Medellin": (6.2442, -75.5812),
    "ANORÍ": (7.1895, -75.1298),
    "BELLO": (6.3373, -75.5582),
    "BUCARAMANGA": (7.1193, -73.1227),
    "BARRANCABERMEJA": (7.0653, -73.8545),
    "CHIA": (4.8581, -74.0583),
    "FLORIDABLANCA": (7.0631, -73.0877),
    "GIRÓN": (7.0688, -73.1698),
    "MANIZALEZ": (5.0703, -75.5138),
    "MONTERIA": (8.7489, -75.8814),
    "MOSQUERA": (4.7084, -74.2317),
    "PALMIRA": (3.5399, -76.3033),
    "PIEDECUESTA": (7.0703, -73.0514),
    "PEREIRA": (4.8143, -75.6946),
    "RIO NEGRO SANTANDER": (7.3892, -73.1745),
    "RIO ORO CESAR": (8.2637, -73.3151),
    "SOGAMOSO": (5.7146, -72.9334),
    "SOACHA": (4.5786, -74.2144),
    "TOCANCIPA": (4.6965, -73.9155),
}
coordenadas_fijas = {k.upper(): v for k, v in coordenadas_fijas.items()}
df[["lat", "lon"]] = df["Ciudad"].apply(lambda ciudad: pd.Series(coordenadas_fijas.get(ciudad.strip().upper(), (None, None))))

# -------------------------
# GeoJSON de Colombia
# -------------------------
url_geojson = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/COL.geo.json"
colombia_geojson = requests.get(url_geojson).json()

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(layout="wide")
st.title("Visualización de ICA por ciudad")
tabs = st.tabs(["🏢 Bases Centrales", "📍 Ciudades ICA"])

# -------------------------
# Tab 1: Bases centrales
# -------------------------
with tabs[0]:
    st.subheader("Bases centrales")
    mapa_bases = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles="CartoDB positron")
    folium.GeoJson(colombia_geojson, style_function=lambda x: {'fillColor': '#ffffff00', 'color': 'black', 'weight': 2}).add_to(mapa_bases)

    bases = {
        "Bogotá": ("MEXICHEM", 4.7110, -74.0721),
        "Guachené": ("PDO", 3.0315, -76.3927),
        "Medellín": ("CELTA", 6.2442, -75.5812),
    }

    colores_empresa = {
        "MEXICHEM": "darkblue",
        "PDO": "lightblue",
        "CELTA": "red"
    }

    for ciudad, (empresa, lat, lon) in bases.items():
        color = colores_empresa.get(empresa.upper(), "gray")
        popup = f"<b>{empresa}</b><br>{ciudad}"
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=empresa,
            icon=folium.Icon(color=color, icon="building")
        ).add_to(mapa_bases)

    st_folium(mapa_bases, width=1000, height=600)

# -------------------------
# Tab 2: Ciudades ICA
# -------------------------
with tabs[1]:
    st.subheader("Ciudades con ICA")
    col1, col2, col3 = st.columns(3)

    ica_val = col1.selectbox("Filtrar por ICA", options=["Todos"] + sorted(df["ICA"].dropna().astype(str).unique().tolist()))
    reteica_val = col2.selectbox("Filtrar por RETEICA", options=["Todos"] + sorted(df["RETEICA / autorretencion"].dropna().astype(str).unique().tolist()))
    factura_val = col3.selectbox("¿Tiene Factura?", options=["Todos", "Sí", "No"])

    df_filtrado = df.copy()

    if ica_val != "Todos":
        df_filtrado = df_filtrado[df_filtrado["ICA"] == int(ica_val)]
    if reteica_val != "Todos":
        df_filtrado = df_filtrado[df_filtrado["RETEICA / autorretencion"] == int(reteica_val)]
    if factura_val != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Factura"].notna()] if factura_val == "Sí" else df_filtrado[df_filtrado["Factura"].isna()]

    mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles="CartoDB positron")
    folium.GeoJson(colombia_geojson, style_function=lambda x: {'fillColor': '#ffffff00', 'color': 'black', 'weight': 2}).add_to(mapa)
    marker_cluster = MarkerCluster().add_to(mapa)

    colores_empresa = {
        "MEXICHEM": "darkblue",
        "PDO": "lightblue",
        "CELTA": "red"
    }

    ciudad_counts = df_filtrado["Ciudad"].value_counts()
    desplazamientos = np.linspace(-0.02, 0.02, ciudad_counts.max())
    desplazador = {}

    for _, row in df_filtrado.iterrows():
        ciudad = row["Ciudad"]
        lat, lon = row["lat"], row["lon"]
        empresa = row["Empresa"]
        if pd.notna(lat) and pd.notna(lon):
            count = desplazador.get(ciudad, 0)
            lat_offset = lat + desplazamientos[count]
            lon_offset = lon + desplazamientos[count]
            desplazador[ciudad] = count + 1

            popup = f"<b>{ciudad}</b><br>Empresa: {empresa}<br>ICA: {row['ICA']}<br>RETEICA: {row['RETEICA / autorretencion']}<br>Factura: {row['Factura']}"
            color = colores_empresa.get(empresa.upper(), "gray")

            folium.Marker(
                location=[lat_offset, lon_offset],
                popup=popup,
                tooltip=empresa,
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(marker_cluster)

    st_folium(mapa, width=1000, height=600)
