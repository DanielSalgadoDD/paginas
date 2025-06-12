import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim

# Título de la app
st.title("Tributación en Colombia")

# Crear pestañas
tabs = st.tabs(["🏢 Bases Centrales", "📍 Tributación por empresa"])

# ------------------ PESTAÑA 1 ------------------
with tabs[0]:
    st.subheader("Bases centrales")
    empresas = {
        "MEXICHEM": {"location": [4.60971, -74.08175], "color": "darkblue"},
        "PDO": {"location": [3.0326, -76.4081], "color": "lightblue"},
        "CELTA": {"location": [10.9184, -74.7679], "color": "red"},
    }

    mapa_bases = folium.Map(location=[5.0, -74.0], zoom_start=6)

    for nombre, info in empresas.items():
        folium.Marker(
            location=info["location"],
            popup=nombre,
            icon=folium.Icon(color=info["color"])
        ).add_to(mapa_bases)

    folium_static(mapa_bases)

# ------------------ PESTAÑA 2 ------------------
with tabs[1]:
    st.subheader("Tributación por empresa")

    # ------------------ Datos ------------------
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
    df['Ciudad'] = df['Ciudad'].str.title()
    df['EMPRESA'] = df['EMPRESA'].str.upper()
    df['ALUMBRADO'] = df['ALUMBRADO'].astype(str)

    # ------------------ Filtros ------------------
    def multiselect_con_todos(label, opciones):
        seleccion = st.sidebar.multiselect(label, options=["Todos"] + opciones, default=["Todos"])
        if "Todos" in seleccion:
            return opciones
        return seleccion

    ica_filter = multiselect_con_todos("Filtrar por ICA", sorted(df['ICA'].astype(str).unique()))
    reteica_filter = multiselect_con_todos("Filtrar por RETEICA", sorted(df['RETEICA / autorretencion'].astype(str).unique()))
    factura_filter = multiselect_con_todos("Filtrar por Factura", sorted(df['Factura'].astype(str).unique()))
    alumbrado_filter = multiselect_con_todos("Filtrar por Alumbrado", sorted(df['ALUMBRADO'].unique()))
    empresa_filter = multiselect_con_todos("Filtrar por Empresa", sorted(df['EMPRESA'].unique()))

    df_filtrado = df[
        df['ICA'].astype(str).isin(ica_filter) &
        df['RETEICA / autorretencion'].astype(str).isin(reteica_filter) &
        df['Factura'].astype(str).isin(factura_filter) &
        df['ALUMBRADO'].isin(alumbrado_filter) &
        df['EMPRESA'].isin(empresa_filter)
    ]

    # Mostrar tabla filtrada
    st.dataframe(df_filtrado)

    # ------------------ Geolocalización con caché ------------------
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

    # ------------------ Mapa ------------------
    mapa = folium.Map(location=[5.0, -74.0], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(mapa)

    color_por_empresa = {
        "MEXICHEM": "darkblue",
        "PDO": "lightblue",
        "CELTA": "red"
    }

    ciudades_marcadas = set()
    for _, row in df_filtrado.iterrows():
        ciudad = row['Ciudad']
        empresa = row['EMPRESA']
        color = color_por_empresa.get(empresa, "gray")

        key = (ciudad, empresa)
        if key not in ciudades_marcadas:
            coords = geolocalizar_ciudad(ciudad)
            if coords:
                popup_info = f"""
                <b>Ciudad:</b> {ciudad}<br>
                <b>Empresa:</b> {empresa}<br>
                <b>ICA:</b> {row['ICA']}<br>
                <b>RETEICA:</b> {row['RETEICA / autorretencion']}<br>
                <b>Factura:</b> {row['Factura']}<br>
                <b>Alumbrado:</b> {row['ALUMBRADO']}
                """
                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_info, max_width=300),
                    icon=folium.Icon(color=color)
                ).add_to(marker_cluster)
                ciudades_marcadas.add(key)

    folium_static(mapa)

