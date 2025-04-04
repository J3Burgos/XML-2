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


def scrap_clasificacion(driver, temporada_inicio, temporada_fin, grupo, liga_code, competicion):
    url = f"https://www.bdfutbol.com/es/t/t{temporada_inicio}-{temporada_fin}{liga_code}{grupo}.html"
    driver.get(url)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception:
        return pd.DataFrame()

    tablas = soup.find_all('table')
    if len(tablas) < 18:
        return pd.DataFrame()

    tabla = tablas[17]
    filas = tabla.find_all('tr')[1:]

    data = []
    for fila in filas:
        celdas = fila.find_all('td')
        if len(celdas) < 13:
            continue

        posicion_td = celdas[1]
        equipo_td = celdas[3]
        puntos_raw = celdas[4].text.strip()

        # --- Detectar Copa del Rey (si contiene símbolo '⬤') ---
        copa_del_rey = "⬤" in equipo_td.text
        equipo = equipo_td.text.replace("⬤", "").strip()

        # --- Detectar estado según clases CSS en la celda de posición ---
        clases = posicion_td.get("class", [])
        if "BAIXA_ADM" in clases or puntos_raw.endswith("*"):
            estado = "Descenso Administrativo"
        elif "PUJA" in clases:
            estado = "Ascenso"
        elif "prom_puja" in clases:
            estado = "Promoción Ascenso"
        elif "prom_baixa" in clases:
            estado = "Promoción Permanencia"
        elif "BAIXA" in clases:
            estado = "Descenso"
        else:
            estado = "Permanencia"

        puntos = puntos_raw.replace("*", "")

        data.append({
            'competicion': competicion,
            'liga': liga_code,
            'temporada': f"{temporada_inicio}-{temporada_fin}",
            'grupo': grupo,
            'posición': posicion_td.text.strip(),
            'equipo': equipo,
            'puntos': puntos,
            'pj': celdas[5].text.strip(),
            'pg': celdas[6].text.strip(),
            'pe': celdas[7].text.strip(),
            'pp': celdas[8].text.strip(),
            'gf': celdas[9].text.strip(),
            'gc': celdas[10].text.strip(),
            'ta': celdas[11].text.strip(),
            'tr': celdas[12].text.strip(),
            'copa_del_rey': copa_del_rey,
            'estado': estado
        })

    return pd.DataFrame(data)


def cargar_existente(path_csv):
    return pd.read_csv(path_csv) if os.path.exists(path_csv) else pd.DataFrame()


def scrap_liga(driver, df_total, competicion, liga_code, temporadas):
    for temporada in temporadas:
        ti, tf = temporada.split("-")
        grupo = 1
        while True:
            ya_esta = (
                not df_total.empty and
                ((df_total["temporada"] == f"{ti}-{tf}") &
                 (df_total["grupo"] == grupo) &
                 (df_total["liga"] == liga_code)).any()
            )
            if ya_esta:
                print(f"⏭️ Ya existe: {competicion} {temporada} G{grupo}")
                grupo += 1
                continue

            print(f"📊 Extrayendo {competicion} {temporada}, Grupo {grupo}...")
            df = scrap_clasificacion(driver, ti, tf, grupo, liga_code, competicion)
            if df.empty:
                if grupo == 1:
                    print(f"⚠️ Sin datos para {competicion} {temporada}")
                else:
                    print(f"⛔ Fin de grupos en {competicion} {temporada}")
                break

            df_total = pd.concat([df_total, df], ignore_index=True)
            print(f"✅ Añadido: {competicion} {temporada} G{grupo}")
            grupo += 1
    return df_total


if __name__ == "__main__":
    CSV_SALIDA = "clasificacion_totalminuscula.csv"
    df_total = cargar_existente(CSV_SALIDA)

    temporadas_2ab = [f"{y}-{str(y+1)[-2:]}" for y in range(1977, 2021)]
    temporadas_2rfef = [f"{y}-{str(y+1)[-2:]}" for y in range(2021, 2025)]
    temporadas_1rfef = [f"{y}-{str(y+1)[-2:]}" for y in range(2021, 2025)]

    driver = crear_driver()

    df_total = scrap_liga(driver, df_total, "2ªB", "2aB", temporadas_2ab)
    df_total = scrap_liga(driver, df_total, "2ª RFEF", "2aB", temporadas_2rfef)
    df_total = scrap_liga(driver, df_total, "1ª RFEF", "1rf", temporadas_1rfef)

    driver.quit()

    df_total.to_csv(CSV_SALIDA, index=False)
    print(f"📁 Guardado final en '{CSV_SALIDA}' con {len(df_total)} filas.")
