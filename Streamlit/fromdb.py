import os
from google.cloud import bigquery

def searchdb(lat, lon):
    #encontrar lugares segun posicion, tipo de negocio y radio de busqueda
    credentials_path = 'pybigQcred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    client = bigquery.Client()
    QUERY = (
            'SELECT name, latitude, longitude FROM `proyecto-final-data-06-377500.datasetPruebaRev.metada_nahuel`'
            'WHERE ST_DWithin(ST_GeogPoint(longitude, latitude), ST_GeogPoint({}, {}), 1000)').format(lon,lat)

    dfquery = client.query(QUERY).to_dataframe()  # API request
    return(dfquery)


