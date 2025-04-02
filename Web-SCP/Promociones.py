import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import unidecode

# --- URLs de promoción ---
PROMOCIONES = [
    # 🔼 Ascensos a 1ª RFEF o 2ª División
    {"tipo": "ascenso", "url": "https://www.bdfutbol.com/es/t/t2023-24aPRF.html", "temporada": "2023-24"},
    {"tipo": "ascenso", "url": "https://www.bdfutbol.com/es/t/t2022-23aPR2.html", "temporada": "2022-23"},
    {"tipo": "ascenso", "url": "https://www.bdfutbol.com/es/t/t2010-11aPR2.html", "temporada": "2010-11"},
    
    # 🔽 Permanencia en 2ªB o 2ª RFEF o 1ª RFEF
    {"tipo": "descenso", "url": "https://www.bdfutbol.com/es/t/t2023-24aPR3.html", "temporada": "2023-24"},
    {"tipo": "descenso", "url": "https://www.bdfutbol.com/es/t/t2010-11aPR3.html", "temporada": "2010-11"},
]

# --- Extraer equipos desde página de promoción ---
def scrap_promo_equipos(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"❌ Error al acceder a {url}")
        return [], []

    soup = BeautifulSoup(resp.text, 'html.parser')

    ganadores = [div.text.strip() for div in soup.select("div.blue")]
    raw_celdas = soup.select("table td")
    participantes = set()

    for celda in raw_celdas:
        text = celda.text.strip()
        if (
            not text or
            re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", text) or
            re.match(r"\d{4}-\d{2}", text) or
            re.match(r"\d+-\d+", text) or
            any(p in text.lower() for p in ["ida", "vuelta", "semifinal", "final"])
        ):
            continue
        if 3 <= len(text) <= 40:
            participantes.add(text)

    return sorted(participantes), sorted(ganadores)

# --- Normalización inteligente de nombres ---
def nombres_compatibles(nombre_csv, lista_web):
    nombre_csv = unidecode.unidecode(nombre_csv.lower())
    for nombre_web in lista_web:
        nombre_web = unidecode.unidecode(nombre_web.lower())
        if nombre_web in nombre_csv or nombre_csv in nombre_web:
            return True
    return False

# --- Aplicar actualizaciones al CSV ---
def actualizar_csv(csv_path):
    df = pd.read_csv(csv_path)

    if "ascenso" not in df.columns:
        df["ascenso"] = "No"
    if "descenso" not in df.columns:
        df["descenso"] = "No"

    actualizados = {"ascenso": 0, "descenso": 0}

    for promo in PROMOCIONES:
        tipo = promo["tipo"]
        url = promo["url"]
        temporada = promo["temporada"]

        print(f"\n🔁 Procesando {tipo.upper()} - {temporada}")
        participantes, ganadores = scrap_promo_equipos(url)

        for idx, row in df.iterrows():
            if row["temporada"] != temporada:
                continue

            equipo = row["equipo"].strip()

            if nombres_compatibles(equipo, participantes):
                if tipo == "ascenso":
                    df.at[idx, "ascenso"] = "Playoff"
                elif tipo == "descenso":
                    df.at[idx, "descenso"] = "Playout"

            if nombres_compatibles(equipo, ganadores):
                if tipo == "ascenso":
                    df.at[idx, "ascenso"] = "Sí"
                    actualizados["ascenso"] += 1
                elif tipo == "descenso":
                    df.at[idx, "descenso"] = "Sí"
                    actualizados["descenso"] += 1

    df.to_csv(csv_path, index=False)
    print("\n✅ CSV actualizado:")
    print(f" - {actualizados['ascenso']} equipos marcados como ascendidos.")
    print(f" - {actualizados['descenso']} equipos marcados como descendidos.")


# 🟢 EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    actualizar_csv("clasificacion_total.csv")
