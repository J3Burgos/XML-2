import pandas as pd
import unidecode

# Archivos
CSV_CLASIFICACION = "clasificacion_total.csv"
CSV_EQUIVALENCIAS = "equipos_equivalentes.csv"

#  Cargar datos
df = pd.read_csv(CSV_CLASIFICACION)
equiv = pd.read_csv(CSV_EQUIVALENCIAS)

#  Función de limpieza (mayúsculas + sin tildes)
def limpiar(nombre):
    return unidecode.unidecode(str(nombre)).upper()

# Diccionario de equivalencias
equiv_dict = {
    limpiar(row["equipo_original"]): limpiar(row["equipo_normalizado"])
    for _, row in equiv.iterrows()
}

#  Aplicar limpieza y equivalencias
df["equipo"] = df["equipo"].apply(lambda x: equiv_dict.get(limpiar(x), limpiar(x)))

# 💾 Guardar
df.to_csv(CSV_CLASIFICACION, index=False)
print(" Todos los equipos convertidos a MAYÚSCULAS y sin tildes, aplicando equivalencias si existen.")
