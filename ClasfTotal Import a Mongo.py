import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import os

# === CONFIGURACIÓN ===
CSV_PATH = "clasificacion_total.csv"  
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "futbol"
COLLECTION_NAME = "clasificacion"

def limpiar_y_normalizar_datos(csv_path):
    try:
        df = pd.read_csv(csv_path)

        # Conversión de columnas numéricas
        columnas_numericas = [
            "puntos", "pj", "pg", "pe", "pp", "gf", "gc", "ta", "tr"
        ]
        for col in columnas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convertir columna booleana (copa_del_rey puede venir como string)
        df["copa_del_rey"] = df["copa_del_rey"].astype(str).str.lower().map({"true": True, "false": False})

        # Convertir posición a numérica
        df["posición"] = pd.to_numeric(df["posición"], errors="coerce")

        # Limpiar filas inválidas
        df = df.dropna(subset=["equipo", "temporada", "puntos"])

        # Cambiar nombre de columnas para mongo (sin tildes ni mayúsculas raras)
        df.rename(columns={
            "posición": "posicion",
            "pj": "partidos_jugados",
            "pg": "partidos_ganados",
            "pe": "partidos_empatados",
            "pp": "partidos_perdidos",
            "gf": "goles_favor",
            "gc": "goles_contra",
            "ta": "tarjetas_amarillas",
            "tr": "tarjetas_rojas",
            "copa_del_rey": "copa_del_rey",
            "estado": "estado_final"
        }, inplace=True)

        return df.to_dict(orient="records")
    except Exception as e:
        print(f"❌ Error al procesar el CSV: {e}")
        return []

def insertar_en_mongodb(datos, uri, db_name, collection_name):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        coleccion = db[collection_name]
        coleccion.drop()  # Limpieza previa, opcional

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
