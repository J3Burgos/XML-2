import pandas as pd

# Define las reglas
REGLAS = {
    "2ªB": {
        "rango_temporadas": (1977, 2020),
        "ascenso directo": lambda pos: pos == 1,  # simplificado
        "playoff ascenso": lambda pos: 1 <= pos <= 4,
        "descenso directo": lambda pos: pos >= 17,
        "playout permanencia": lambda pos: pos == 16
    },
    "1ª RFEF": {
        "rango_temporadas": (2021, 2099),
        "ascenso directo": lambda pos: pos == 1,
        "playoff ascenso": lambda pos: 2 <= pos <= 5,
        "descenso directo": lambda pos: 16 <= pos <= 20,
        "playout": lambda pos: False
    },
    "2ª RFEF": {
        "rango_temporadas": (2021, 2099),
        "ascenso directo": lambda pos: pos == 1,
        "playoff ascenso": lambda pos: 2 <= pos <= 5,
        "descenso directo": lambda pos: 14 <= pos <= 18,
        "playout permanencia": lambda pos: pos == 13
    }
}

def clasificar_equipo(row):
    cat = row["categoria"]
    pos = int(row["puesto"])
    temp = int(row["temporada"].split("-")[0])

    if cat not in REGLAS:
        return None

    reglas = REGLAS[cat]
    min_temp, max_temp = reglas["rango_temporadas"]
    if not (min_temp <= temp <= max_temp):
        return None

    for tipo, regla in reglas.items():
        if tipo == "rango_temporadas":
            continue
        if regla(pos):
            return tipo
    return None

# Cargar el CSV de clasificaciones (el input base)
df = pd.read_csv("clasificacion_total.csv")  # debe tener: temporada, categoria, grupo, puesto, equipo

# Aplicar la clasificación
df["tipo"] = df.apply(clasificar_equipo, axis=1)

# Filtrar filas relevantes
df_filtrado = df[df["tipo"].notnull()].sort_values(by=["temporada", "categoria", "grupo", "puesto"])

# Guardar CSV
df_filtrado.to_csv("equipos_promocionados.csv", index=False)
print("✅ CSV generado: equipos_promocionados.csv")
