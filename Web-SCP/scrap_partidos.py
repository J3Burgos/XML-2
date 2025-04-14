import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def crear_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def scrap_partidos(driver, temporada_inicio, temporada_fin, grupo, liga_code, competicion):
    url = f"https://www.bdfutbol.com/es/t{temporada_inicio}-{temporada_fin}{liga_code}{grupo}.html?tab=partidos"
    print(f"🔎 Visitando: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"❌ Error cargando la página: {e}")
        return pd.DataFrame()

    tabla = soup.find('table', class_='tabla_partidos')
    if not tabla:
        print(f"❌ No se encontró tabla de partidos en: {url}")
        return pd.DataFrame()

    filas = tabla.find_all('tr')[1:]

    data = []
    for fila in filas:
        celdas = fila.find_all('td')
        if len(celdas) < 6:
            continue

        jornada = celdas[0].text.strip()
        fecha = celdas[1].text.strip()
        local = celdas[2].text.strip()
        resultado = celdas[3].text.strip()
        visitante = celdas[4].text.strip()
        estado = celdas[5].text.strip()

        if "-" in resultado:
            goles_local, goles_visitante = resultado.split("-")
            goles_local = goles_local.strip()
            goles_visitante = goles_visitante.strip()
        else:
            goles_local = goles_visitante = ""

        data.append({
            'competicion': competicion,
            'liga': liga_code,
            'temporada': f"{temporada_inicio}-{temporada_fin}",
            'grupo': grupo,
            'jornada': jornada,
            'fecha': fecha,
            'local': local,
            'visitante': visitante,
            'goles_local': goles_local,
            'goles_visitante': goles_visitante,
            'estado': estado
        })

    return pd.DataFrame(data)


def cargar_existente(path_csv):
    if os.path.exists(path_csv) and os.path.getsize(path_csv) > 0:
        try:
            return pd.read_csv(path_csv)
        except pd.errors.EmptyDataError:
            print("⚠️ CSV existente pero vacío. Se ignorará.")
            return pd.DataFrame()
    return pd.DataFrame()

def scrap_partidos_liga(driver, df_total, competicion, liga_code, temporadas):
    for temporada in temporadas:
        ti, tf = temporada.split("-")
        grupo = 1
        while True:
            print(f"🎯 Extrayendo partidos de {competicion} {temporada}, Grupo {grupo}...")
            df = scrap_partidos(driver, ti, tf, grupo, liga_code, competicion)
            if df.empty:
                if grupo == 1:
                    print(f"⚠️ Sin datos para {competicion} {temporada}")
                else:
                    print(f"⛔ Fin de grupos en {competicion} {temporada}")
                break
            df_total = pd.concat([df_total, df], ignore_index=True)
            print(f"✅ Añadidos partidos: {competicion} {temporada} G{grupo}")
            grupo += 1
    return df_total


if __name__ == "__main__":
    CSV_SALIDA = "partidos_total.csv"
    df_total = cargar_existente(CSV_SALIDA)

    # TODAS LAS TEMPORADAS
    temporadas_2ab = [f"{y}-{str(y+1)[-2:]}" for y in range(1977, 2021)]
    temporadas_2rfef = [f"{y}-{str(y+1)[-2:]}" for y in range(2021, 2025)]
    temporadas_1rfef = [f"{y}-{str(y+1)[-2:]}" for y in range(2021, 2025)]

    driver = crear_driver()

    df_total = scrap_partidos_liga(driver, df_total, "2ªB", "2aB", temporadas_2ab)
    df_total = scrap_partidos_liga(driver, df_total, "2ª RFEF", "2aB", temporadas_2rfef)
    df_total = scrap_partidos_liga(driver, df_total, "1ª RFEF", "1rf", temporadas_1rfef)

    driver.quit()

    if not df_total.empty:
        df_total.to_csv(CSV_SALIDA, index=False)
        print(f"📁 Guardado final en '{CSV_SALIDA}' con {len(df_total)} partidos.")
    else:
        print("⚠️ No se guardó ningún archivo porque no se extrajeron partidos.")
