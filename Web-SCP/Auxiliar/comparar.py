import pandas as pd

# Cargar los dos CSV
df1 = pd.read_csv("clasificacion_total.csv")
df2 = pd.read_csv("clasificacion_totalminuscula.csv")

# Normaliza nombres (quita espacios, pone minúsculas)
df1['equipo_normalizado'] = df1['equipo'].str.strip().str.lower()
df2['equipo_normalizado'] = df2['equipo'].str.strip().str.lower()

# Obtener equipos únicos
equipos1 = df1['equipo_normalizado'].unique()
equipos2 = df2['equipo_normalizado'].unique()

# Equipos que no están en ambos CSV
solo_en_df1 = [e for e in equipos1 if e not in equipos2]
solo_en_df2 = [e for e in equipos2 if e not in equipos1]

# Buscar los nombres originales (para mostrar en el CSV de salida)
originales_df1 = df1[df1['equipo_normalizado'].isin(solo_en_df1)][['equipo']].drop_duplicates()
originales_df2 = df2[df2['equipo_normalizado'].isin(solo_en_df2)][['equipo']].drop_duplicates()

# Unir resultados en un nuevo DataFrame
comparacion = pd.DataFrame({
    'equipo_csv1': originales_df1['equipo'].reset_index(drop=True),
    'equipo_csv2': originales_df2['equipo'].reset_index(drop=True)
})

# Guardar diferencias
comparacion.to_csv("equipos_diferentes.csv", index=False)
print("🔍 Comparación completa. Resultados guardados en 'equipos_diferentes.csv'.")
