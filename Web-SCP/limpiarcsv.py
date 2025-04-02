import pandas as pd

df = pd.read_csv("clasificacion_total.csv")

# Eliminar columna 'liga' si existe
if 'liga' in df.columns:
    df = df.drop(columns=['liga'])

# Reordenar columnas si quieres
columnas_ordenadas = ['competicion', 'temporada', 'grupo', 'posición', 'equipo', 'puntos',
                      'pj', 'pg', 'pe', 'pp', 'gf', 'gc', 'ta', 'tr']
df = df[columnas_ordenadas]

# Guardar CSV limpio
df.to_csv("clasificacion_total.csv", index=False)
print("✅ CSV actualizado sin columna 'liga'")
