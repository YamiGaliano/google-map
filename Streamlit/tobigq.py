import requests
import json
import os
import streamlit as st
import pandas as pd
import parse
from glom import glom
from ast import literal_eval
from tabulate import tabulate
from google.cloud import bigquery


def searchload(lat, lon,radio):
    #encontrar lugares segun posicion, tipo de negocio y radio de busqueda
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius={radio}&type=restaurant&key=AIzaSyAHXRKJ13tnjffJ6o6AHJIhs-_EKOoTTt4"
    payload={}
    headers = {}
    credentials_path = 'pybigQcred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    client = bigquery.Client()
    response = requests.request("GET", url, headers=headers, data=payload)
    jsonsearch = json.loads(response.text)
    dfsearch = pd.json_normalize(jsonsearch['results'])
    
    for ind in dfsearch.index:
        #Encontrar cada lugar
        id = dfsearch['place_id'][ind]
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&key=AIzaSyAHXRKJ13tnjffJ6o6AHJIhs-_EKOoTTt4"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        jsonplace = json.loads(response.text)
        dfplace = pd.json_normalize(jsonplace['result'])
        queryname = dfplace['name'].item()
        queryname = queryname.replace(r'"', r'\"')
        st.write(f"lugar especifico encontrado: {queryname}")
        st.write("Ejecutando SELECT")
        print(queryname)
        print("Iniciando SELECT")
        listaempty = ['']
        emptyitem = pd.Series(listaempty)
        QUERY = (
            'SELECT name FROM `proyecto-final-data-06-377500.datasetPruebaRev.metada_nahuel`'
            'WHERE name = """{0}""" limit 10').format(queryname)

        query_job = client.query(QUERY)  # API request
        rows = query_job.result()
        if rows.total_rows == 0: #Row not found, insert new row
            st.write("No se encontraron filas, Insertando...")
            dfplace['name'].item()
            #insert to BigQ 
            table_id = "proyecto-final-data-06-377500.datasetPruebaRev.metada_nahuel"
            rows_to_insert = [
                {'name': str(dfplace.get('name', emptyitem).item()), 
                 'address': str(dfplace.get('formatted_address',emptyitem).item()),
                 'gmap_id': str(dfplace.get('place_id', emptyitem).item()),
                 'description': dfplace.get('editorial_summary.overview', emptyitem).item(),
                 'latitude': str(dfplace.get('geometry.location.lat', emptyitem).item()),
                 'longitude': str(dfplace.get('geometry.location.lng', emptyitem).item()),
                 'category': dfplace.get('types', emptyitem).str[0].item(),
                 'avg_rating': str(dfplace.get('rating', emptyitem).item()),
                 'num_of_reviews': str(dfplace.get('user_ratings_total', emptyitem).item()),
                 'price': str(dfplace.get('price_level', emptyitem).item()),
                 'hours': str(dfplace.get('current_opening_hours.weekday_text', emptyitem).item()),
                 'url': str(dfplace.get('url', emptyitem).item())
                 },
            ]
            print(type(rows_to_insert))
            errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
            if errors == []:
                print("New rows have been added to Metadata.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors)) 
            
            table_rev = "proyecto-final-data-06-377500.datasetPruebaRev.reviews_nahuel"
            urlreview = str(dfplace.get('reviews.author_url', emptyitem).item())
            userid = parse.search('https://www.google.com/maps/contrib/{}/reviews', urlreview)
            rows_to_rev = [
                {'user_id': userid[0],
                 'name': str(dfplace.get('reviews.author_name', emptyitem).item()), 
                 'time': str(dfplace.get('reviews.time',emptyitem).item()),
                 'rating': str(dfplace.get('reviews.rating',emptyitem).item()),
                 'text': str(dfplace.get('reviews.text',emptyitem).item()),
                 'gmap_id': str(dfplace.get('place_id', emptyitem).item())
                 },
            ]
            print(type(rows_to_rev))
            errors = client.insert_rows_json(table_rev, rows_to_rev)  # Make an API request.
            if errors == []:
                print("New rows have been added to Revirews.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors)) 

        else: #Rows found, proceed to update
            query_text = ('UPDATE `proyecto-final-data-06-377500.datasetPruebaRev.metada_nahuel` '
                'SET address = "{}", '
                'gmap_id = "{}", '
                'description = "{}", '
                'latitude = {}, '
                'longitude = {}, '
                'category = "{}", '
                'avg_rating = {}, '
                'num_of_reviews = {}, '
                'price = "{}", '
                'hours = "{}", '
                'url = "{}" '
                'WHERE name = "{}"').format(str(dfplace.get('formatted_address',emptyitem).item()), str(dfplace.get('place_id', emptyitem).item()),str(dfplace.get('editorial_summary.overview', emptyitem).item()),str(dfplace.get('geometry.location.lat', emptyitem).item()),str(dfplace.get('geometry.location.lng', emptyitem).item()),dfplace.get('types', emptyitem).str[0].item(),str(dfplace.get('rating', emptyitem).item()), str(dfplace.get('user_ratings_total', emptyitem).item()), str(dfplace.get('price_level', emptyitem).item()), str(dfplace.get('current_opening_hours.weekday_text', emptyitem).item()), str(dfplace.get('url', emptyitem).item()),queryname)
            st.write(query_text)
            query_job = client.query(query_text)

            # Wait for query job to finish.
            query_job.result()

            assert query_job.num_dml_affected_rows is not None
            st.write(f"DML query modified {query_job.num_dml_affected_rows} rows.")
            print(f"DML query modified {query_job.num_dml_affected_rows} rows.")


