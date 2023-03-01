import streamlit as st
from tobigq import searchload
from fromdb import searchdb
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import math
country = "United States"
city = ""
etiqueta = ""
def delstate():
    if "etiquet" in st.session_state:
        del st.session_state.etiquet
if __name__ == '__main__':
    
    st.write('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)
    
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    new_title = '<p style="font-family:sans-serif; text-align:center; color:White; font-size: 36px; margin-top: -100px; margin-bottom: -100px;"><strong>[EF] APP</strong></p>'
    new_image = '<img src="https://iili.io/HVFlYoG.jpg" alt="EZ App image" class="center" style="width:175px;height:175px; margin-top: -50px;margin-left: 70px;"></p>'
    st.sidebar.markdown(new_title, unsafe_allow_html=True)
    st.sidebar.markdown(new_image, unsafe_allow_html=True)


    userdict = {"Philip Wunderlich": "113381142542018467294",
                "Mike Johnson" : "115330754707742864419", 
                "William Gilane Jr" : "112782794276785059993", 
                "Phil Yelton" : "102657099077047497420",
                "Justin Caldwell" : "107705240711231122119"}

    user = st.sidebar.selectbox(
            "Elija Usuario: ",
            ("Philip Wunderlich", "Mike Johnson", "William Gilane Jr", "Phil Yelton", "Justin Caldwell"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
    user_id = userdict[user]
    radio = st.sidebar.slider("Seleccione radio de búsqueda en metros:", min_value = 0, max_value = 2000, step = 1, value = 500)
    #st.sidebar.write('Values:', values)
    iframeperson = folium.IFrame('<b>' + str(user) + '</b> <br> Estás aquí')
    popupperson = folium.Popup(iframeperson, min_width=300, max_width=300)


    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    #location = geolocator.geocode(city)
    location = geolocator.geocode(city+", "+country)
    zoomvalue =4
    lat = location.latitude
    lon = location.longitude
    print("Primer geoloc " + str(lat) + " " + str(lon) + city+", "+country)
    m = folium.Map(location=[lat, lon], zoom_start=25)
    fg = folium.FeatureGroup(name="Markers")
    x = st.empty()
    c1, c2= st.columns([7, 1])
    with c1:
        if "etiquet" in st.session_state:
            etiqueta = st.session_state.etiquet.address
        city = x.text_input("Ingrese ciudad: ", etiqueta)
        if "etiquet" in st.session_state:
            city = st.session_state.etiquet.address
    with c2:
        #st.write("##")
        if st.button("Buscar", key="busca"):  
            #display_user()
            userid = user_id
            name = str()
            #location = geolocator.geocode(city+", "+country)
            location = geolocator.geocode(city)
            lat = location.latitude
            lon = location.longitude
            print("Boton geoloc " + str(lat) + " " + str(lon) + city+", "+country)
            print("Boton etiqueta: " + etiqueta)
            #Busqueda API PLACES y Carga Incremental
            #searchload(lat, lon, radio)
            dfquery = searchdb(float(lat), float(lon), userid, radio)
            #conexion ML
            zoomvalue = 16

            fg.add_child(
                folium.Marker(
                    [lat, lon], 
                    popup=popupperson,
                    tooltip="Tu ubicacion",
                    icon=folium.Icon(color="red", prefix='fa', icon='fa-user-circle-o'),
                )
            )
            
            for ind in dfquery.index:
                if (math.isnan(dfquery['predicted_rating'][ind])):
                    fg.add_child(
                        folium.Marker(
                        [dfquery['latitude'][ind], dfquery['longitude'][ind]], 
                        popup="<b>Nombre: </b>" + dfquery['name'][ind] + "<br> <b>Direccion: </b>" + dfquery['address'][ind] + "<br> <b>Calificación: </b>" + dfquery['avg_rating'][ind], 
                        tooltip="<b>Nombre: </b>" + dfquery['name'][ind] + "<br> <b>Direccion: </b>" + dfquery['address'][ind] + "<br> <b>Calificación: </b>" + dfquery['avg_rating'][ind],
                        icon=folium.Icon(color="blue",prefix='fa',icon='fa-cutlery'),
                        )
                    )
                else:
                    #print(dfquery['predicted_rating'][ind])
                    fg.add_child(
                        folium.Marker(
                        [dfquery['latitude'][ind], dfquery['longitude'][ind]], 
                        popup="<b>¡RECOMENDADO! <br> Nombre: </b>" + dfquery['name'][ind] + "<br> <b>Direccion: </b>" + dfquery['address'][ind] + "<br> <b>Calificación: </b>" + dfquery['avg_rating'][ind], 
                        tooltip="<b>¡RECOMENDADO! <br> Nombre: </b>" + dfquery['name'][ind] + "<br> <b>Direccion: </b>" + dfquery['address'][ind] + "<br> <b>Calificación: </b>" + dfquery['avg_rating'][ind],
                        icon=folium.Icon(color="black",prefix='fa',icon='fa-sellsy'),
                        )
                    )

    fg.add_child(
        folium.Marker(
        [lat, lon], 
        #popup=popupperson, 
        tooltip="<b>Tu ubicación", 
        icon=folium.Icon(color="red", prefix='fa', icon='fa-user-circle-o'),
        )
    )
    print("folium 116, zoom = " + str(zoomvalue) )
    print("Ultimo geoloc " + str(lat) + " " + str(lon) + city+", "+country)
    output = st_folium(
        m,     
        center=[lat,lon],
        zoom=zoomvalue,
        key="map",feature_group_to_add=fg, width=700, height=400, returned_objects=["last_clicked"]
    )

    if output:
        try:
            if output["last_clicked"] != "":
                coordenadas = str(output["last_clicked"]["lat"]) + ", " + str(output["last_clicked"]["lng"])
                print("etiquetaul: " + etiqueta)
                print("coordenadas: " + coordenadas)
                st.session_state.etiquet = geolocator.reverse(coordenadas)
                x.text_input("Ingrese ciudad: ", st.session_state.etiquet)
                #etiqueta = geolocator.reverse(coordenadas)
                print("etiquetaul: " + etiqueta)
                city = st.session_state.etiquet
                #x.text_input("Ingrese ciudad: ", city)
        except:
            print("clave no encontrada")