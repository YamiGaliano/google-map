import streamlit as st
from streamlit_js_eval import get_geolocation
from auth import *
from tobigq import *
from fromdb import searchdb
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy
import cv2
import numpy as np
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium

loc = get_geolocation()
#st.write(f"Your coordinates are {loc}")
#lat=float(loc['coords']['latitude'])
#lon=float(loc['coords']['longitude'])
#st.write(f"Latitude is {lat}")
#st.write(f"Longitude is {lon}")

if __name__ == '__main__':
    st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
    
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 36px; margin-top: -100px; margin-bottom: -100px;"><strong>[EF] APP</strong></p>'
    new_image = '<img src="https://media.tenor.com/cyNmFWbyEBkAAAAM/cat.gif" alt="EZ App image" class="center" style="width:150px;height:150px; margin-top: -50px;margin-left: 50px;"></p>'
    st.sidebar.markdown(new_title, unsafe_allow_html=True)
    st.sidebar.markdown(new_image, unsafe_allow_html=True)

    user = st.sidebar.selectbox(
            "Elija Usuario",
            ("Ale", "Michi", "Cris", "Lider", "La Yani"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    tipo = st.sidebar.radio(
        "Seleccione categoria 👉",
        ('Restaurant', 'Gimnasio', 'Hotel del amor')
    )
    
    country = "United States"
    city = ""

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(city+", "+country)
    zoomvalue =3
    lat = location.latitude
    lon = location.longitude
    m = folium.Map(location=[lat, lon], zoom_start=25)
    fg = folium.FeatureGroup(name="Markers")
    c1, c2, c3= st.columns([1, 4, 2])
    with c1:
        st.write("##")
        st.write("Ciudad")
    with c2:
        city = st.text_input("", "La quiaca")
    with c3:
        st.write("##")
        if st.button("display user"):  
            #display_user()
            userid = 107030417114826409179
            name = str()
            lat = -22.104403
            lon = -65.596771
            #Busqueda API PLACES y Carga Incremental
            #searchload(lat, lon)
            dfquery = searchdb(lat, lon)
            zoomvalue = 16
            fg.add_child(
                folium.Marker(
                    [lat, lon], 
                    popup="Your location popup", 
                    tooltip="Your location tooltip",
                    icon=folium.Icon(color="red"),
                    )
            )
            for ind in dfquery.index:
                fg.add_child(
                    folium.Marker(
                    [dfquery['latitude'][ind], dfquery['longitude'][ind]], 
                    popup=dfquery['name'][ind], 
                    tooltip=dfquery['name'][ind],
                    icon=folium.Icon(color="blue",prefix='fa',icon='fa-cutlery'),
                    )
                )

    fg.add_child(
        folium.Marker(
        [lat, lon], popup="Your location popup", tooltip="Your location tooltip", icon=folium.Icon(color="red"),
        )
    )
    output = st_folium(
        m,     
        center=[lat,lon],
        zoom=zoomvalue,
        key="map",feature_group_to_add=fg, width=700, height=400, returned_objects=["last_object_clicked"]
    )

    


    
