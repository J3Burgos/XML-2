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


def debug_tablas(driver, temporada_inicio, temporada_fin, grupo, liga_code):
    url = f"https://www.bdfutbol.com/es/t/t{temporada_inicio}-{temporada_fin}{liga_code}{grupo}.html"
    print(f"🔍 Visitando: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"❌ Error al cargar la página: {e}")
        return

    tablas = soup.find_all("table")
    print(f"📋 Total de tablas encontradas: {len(tablas)}\n")

    for i, tabla in enumerate(tablas):
        print(f"\n=== 🧾 TABLA {i} ===\n")
        filas = tabla.find_all("tr")
        for fila in filas:
            celdas = fila.find_all(["td", "th"])
            texto_fila = " | ".join(c.text.strip().replace("\n", " ") for c in celdas)
            print(texto_fila)
        print("-" * 60)

    # Mostrar leyenda si existe
    leyenda_divs = soup.find_all("div", class_="text")
    if leyenda_divs:
        print("\n📌 Posible leyenda encontrada:")
        for div in leyenda_divs:
            print(div.get_text().strip())


if __name__ == "__main__":
    driver = crear_driver()

    # Cambia estos valores para inspeccionar diferentes páginas
    debug_tablas(driver, "2023", "24", 1, "2aB")

    driver.quit()
