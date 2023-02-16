import os
from pprint import pprint
from google.cloud import storage
import time

# Credenciales de Google Cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'proyecto-final-data-06-377500-1be437e68663.json'
storage_client = storage.Client()
# Definicion del nombre del bucket de GCS
bucket_name = 'henry_dataset'

# Funcion para subir el aarchivo al Bucket

def upload_to_bucket(blob_names, file_paths, bucket_name):
    bucket = storage_client.get_bucket(bucket_name)
    blobs = []
    for i in range(len(blob_names)):
        blob = bucket.blob(blob_names[i])
        blob.upload_from_filename(file_paths[i])
        blobs.append(blob)
    return blobs

carpeta= "./datasets/"
carpeta_cloud = 'HenryDatasets/'
# Lista de archivos en la carpeta
archivos = [carpeta+archivo for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo)) and '.csv' in archivo]
print(archivos)
#Lista de archivos para cloud
archivos_cloud =  [carpeta_cloud+archivo for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo)) and '.csv' in archivo]
print(archivos_cloud)

blob_names = archivos_cloud
file_paths = archivos

# Llamado a funcion para subir archivo, el formato es (path de destino en cloud, path del archivo local, nombre del bucket)
#response = upload_to_bucket(blob_names, file_paths, bucket_name)

# Respuesta para saber que termino, no es necesario
# print(response)