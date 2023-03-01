import os
from google.cloud import bigquery

def searchdb(lat, lon, user, radio):
    #encontrar lugares segun posicion, tipo de negocio y radio de busqueda
    credentials_path = 'pybigQcred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    client = bigquery.Client()

    QUERY = (
            'SELECT name, gmap_id,description,address,avg_rating, latitude, longitude FROM `proyecto-final-data-06-377500.datasetPruebaRev.metadata_final_yami`'
            'WHERE cat_id = "6" and ST_DWithin(ST_GeogPoint(safe_cast(longitude as FLOAT64),safe_cast(latitude as FLOAT64)), ST_GeogPoint({}, {}), {}) limit 30').format(lon,lat,radio)
            #'WHERE ST_DWithin(ST_GeogPoint(longitude, latitude), ST_GeogPoint({}, {}), 500) limit 10').format(float(lon),float(lat))
    print(QUERY)
    dfquery = client.query(QUERY).to_dataframe()  # API request
    dfquery['predicted_rating'] = ''
    dfquery['gmap_id2'] = ''
    #gmaparray = dfquery['gmap_id'].to_numpy()
    gmaparray = dfquery['gmap_id'].values.tolist()
    print(gmaparray)
    QUERY2 = (
        'SELECT gmap_id, predicted_rating FROM `proyecto-final-data-06-377500.datasetPruebaRev.recmlfull`'
        'WHERE gmap_id in UNNEST({}) and user_id = "{}" limit 30').format(gmaparray,user)
    dfMLquery = client.query(QUERY2).to_dataframe()  # API request
    dfMLquery.sort_values(by=['predicted_rating'])
    print(QUERY2)
    print(client.query(QUERY2).to_dataframe())
    dfquery['predicted_rating'] = dfMLquery['predicted_rating']
    dfquery['gmap_id2'] = dfMLquery['gmap_id']

    return(dfquery)


