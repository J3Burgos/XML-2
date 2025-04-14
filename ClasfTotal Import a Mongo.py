import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import os

# === CONFIGURACIÓN ===
CSV_PATH = "clasificacion_total.csv"  # asegúrate de que esté en el mismo directorio
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "futbol"
COLLECTION_NAME = "clasificacion"

def limpiar_y_normalizar_datos(csv_path):
    try:
        df = pd.read_csv(csv_path)
        df['puntos'] = pd.to_numeric(df['puntos'], errors='coerce')
        df = df.dropna(subset=['puntos'])
        df['puntos'] = df['puntos'].astype(int)

        df.columns = [
            "competicion", "temporada", "grupo", "posicion", "equipo", "puntos",
            "partidos_jugados", "partidos_ganados", "partidos_empatados", "partidos_perdidos",
            "goles_favor", "goles_contra", "tarjetas_amarillas", "tarjetas_rojas",
            "ascenso", "descenso"
        ]

        return df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error al procesar el CSV: {e}")
        return []

def insertar_en_mongodb(datos, uri, db_name, collection_name):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        coleccion = db[collection_name]

        if datos:
            resultado = coleccion.insert_many(datos)
            print(f"✅ {len(resultado.inserted_ids)} documentos insertados correctamente en '{collection_name}'.")
        else:
            print("⚠️ No hay datos para insertar.")
    except BulkWriteError as bwe:
        print("❌ Error al insertar en MongoDB:", bwe.details)
    except Exception as e:
        print(f"❌ Conexión o inserción fallida: {e}")

if __name__ == "__main__":
    if os.path.exists(CSV_PATH):
        datos = limpiar_y_normalizar_datos(CSV_PATH)
        insertar_en_mongodb(datos, MONGO_URI, DB_NAME, COLLECTION_NAME)
    else:
        print(f"❌ No se encontró el archivo '{CSV_PATH}'.")
