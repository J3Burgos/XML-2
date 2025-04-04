import pandas as pd

df = pd.read_csv("clasificacion_totalminuscula.csv")

# Eliminar columna 'liga' si existe
if 'liga' in df.columns:
    df = df.drop(columns=['liga'])

# Convertir temporada en año inicial para orden cronológico
df["temp_orden"] = df["temporada"].apply(lambda x: int(x.split("-")[0]))

# Asegurar que grupo es entero
df["grupo"] = df["grupo"].astype(int)

# Ordenar por competicion, temporada (cronológica) y grupo
df = df.sort_values(by=["temp_orden", "competicion", "grupo"]).drop(columns=["temp_orden"])

# Reordenar columnas
columnas_ordenadas = ['competicion', 'temporada', 'grupo', 'posición', 'equipo', 'puntos',
                      'pj', 'pg', 'pe', 'pp', 'gf', 'gc', 'ta', 'tr']

# Añadir columnas si existen
if 'copa_del_rey' in df.columns:
    columnas_ordenadas.append('copa_del_rey')
if 'estado' in df.columns:
    columnas_ordenadas.append('estado')

df = df[columnas_ordenadas]

# Guardar CSV limpio y ordenado
df.to_csv("clasificacion_totalminuscula.csv", index=False)
print("✅ CSV ordenado por competicion, temporada y grupo.")
