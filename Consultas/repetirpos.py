from pymongo import MongoClient
from collections import defaultdict

def extraer_posiciones_consecutivas(db):
    coleccion = db["clasificacion"]

    # Agrupar por equipo
    equipos_data = defaultdict(list)
    for doc in coleccion.find({}, {"equipo": 1, "temporada": 1, "posicion": 1, "_id": 0}):
        equipo = doc["equipo"]
        temporada = doc["temporada"]
        posicion = doc["posicion"]
        equipos_data[equipo].append((temporada, posicion))

    resultados = []

    # Procesar por equipo
    for equipo, temporadas in equipos_data.items():
        # Ordenar por temporada (asume formato tipo '2000-01')
        temporadas.sort(key=lambda x: int(x[0].split("-")[0]))

        # Buscar secuencias de 3 posiciones iguales
        for i in range(len(temporadas) - 2):
            pos1 = temporadas[i][1]
            pos2 = temporadas[i+1][1]
            pos3 = temporadas[i+2][1]

            if pos1 == pos2 == pos3:
                resultados.append({
                    "equipo": equipo,
                    "posicion_repetida": pos1,
                    "temporadas": [temporadas[i][0], temporadas[i+1][0], temporadas[i+2][0]]
                })
                break  # Solo mostrar una coincidencia por equipo

    return resultados

# === MAIN ===
if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["futbol"]

    repeticiones = extraer_posiciones_consecutivas(db)

    if repeticiones:
        print("Equipos que repitieron la misma posición 3 temporadas :\n")
        for r in repeticiones:
            print(f"{r['equipo']} — Posición: {r['posicion_repetida']} — Temporadas: {', '.join(r['temporadas'])}")
    else:
        print("Ningún equipo repitió posición 3 años seguidos.")
