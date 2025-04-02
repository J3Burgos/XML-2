import pandas as pd

# Cargar dataset
df = pd.read_csv("clasificacion_total.csv")

# Ordenar por temporada (importante para coger la primera)
df = df.sort_values(by=["equipo", "temporada"])

# Agrupar por equipo y coger la primera temporada en la que aparece
primeras_apariciones = df.groupby("equipo")["temporada"].first().reset_index()

# Ordenar alfabéticamente
primeras_apariciones = primeras_apariciones.sort_values(by="equipo")

# Guardar CSV
primeras_apariciones.to_csv("equipos_unicos_con_temporada.csv", index=False)
print(f"✅ Archivo 'equipos_unicos_con_temporada.csv' generado con {len(primeras_apariciones)} equipos.")
