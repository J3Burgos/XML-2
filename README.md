# XML-2

## ⚙️ Instrucciones para Ejecutar el Scraper

Este proyecto permite scrapear automáticamente todas las clasificaciones históricas desde **1977–78** hasta **2023–24** de las competiciones:

- **2ª División B**
- **1ª RFEF**
- **2ª RFEF**

### 📁 Estructura del Dataset
El archivo generado se llama:

```
clasificacion_total.csv
```

Y contiene, entre otros, los siguientes campos:

| Campo        | Descripción                                          |
|--------------|------------------------------------------------------|
| `competicion`| Competición (`2ªB`, `1ª RFEF`, `2ª RFEF`)            |
| `temporada`  | Temporada en formato `AAAA-AA`                       |
| `grupo`      | Grupo dentro de la competición                       |
| `posición`   | Posición final del equipo                            |
| `equipo`     | Nombre del club                                       |
| `puntos`     | Puntos totales al final de la temporada              |
| `pj`–`tr`    | Partidos jugados, ganados, goles, tarjetas, etc.     |

### ▶️ Cómo ejecutar el scraping

1. **Instala dependencias** (si no lo has hecho):

```bash
pip install selenium beautifulsoup4 pandas
```

2. **Asegúrate de tener `chromedriver`** en tu PATH o en el directorio del script.

3. **Ejecuta el script principal:**

```bash
python scraper_clasificacion.py
```

Este script:
- Recorrerá todas las temporadas y ligas.
- Detectará automáticamente cuántos grupos hay por temporada.
- No volverá a scrapear temporadas que ya estén guardadas en `clasificacion_total.csv`.

4. **Ejecuta el script limpiar ligas:**

```bash
python limpiarcsv.py
```
Este script:
- Borrara automaticamente la columna ligas ya que es muy redundante tener competicion y liga en el mismo dataset.


## 🧭 Lógica de Ascensos y Descensos

El dataset recoge información de las categorías **2ªB (hasta 2020–21)**, **1ª RFEF** y **2ª RFEF** (desde 2021–22). Para interpretar correctamente los **ascensos y descensos**, se ha implementado la siguiente lógica basada en normativa oficial y análisis de las fases de promoción.

---

### 🟦 2ªB (1977–78 a 2020–21)

| Concepto              | Condición                                               |
|-----------------------|----------------------------------------------------------|
| **Ascenso directo**   | Variable: algunos años el 1º accedía a fase final directa |
| **Playoff ascenso**   | 1º al 4º clasificaban a fase de promoción                |
| **Descenso directo**  | Últimos 3–4 puestos por grupo                            |
| **Promoción permanencia (Playout)** | 16º en algunos años jugaba permanencia |

---

### 🟥 1ª RFEF (desde 2021–22)

| Concepto              | Condición                                               |
|-----------------------|----------------------------------------------------------|
| **Ascenso directo**   | 1º de cada grupo asciende directamente a 2ª División     |
| **Playoff ascenso**   | 2º al 5º disputan promoción (eliminatoria nacional)     |
| **Descenso directo**  | Puestos 16º al 20º por grupo                             |
| **Playout**           | No existe                                                |

---

### 🟩 2ª RFEF (desde 2021–22)

| Concepto              | Condición                                               |
|-----------------------|----------------------------------------------------------|
| **Ascenso directo**   | 1º de cada grupo asciende directamente a 1ª RFEF         |
| **Playoff ascenso**   | 2º al 5º disputan fase de ascenso                        |
| **Descenso directo**  | Puestos 14º al 18º por grupo                             |
| **Playout permanencia** | 13º juega promoción de permanencia contra otros 13º  |

---

## 🛠 Cómo se determinan los ascensos/descensos en el dataset

- Se añade automáticamente la columna `ascenso` con valores:
  - `"Sí"` → si asciende directamente o gana playoff
  - `"Playoff"` → si disputa fase de ascenso pero no gana
  - `"No"` → si no juega por ascender

- Se añade la columna `descenso` con valores:
  - `"Sí"` → si desciende directamente o pierde promoción
  - `"Playout"` → si disputa permanencia
  - `"No"` → si mantiene la categoría sin disputar fases

- Además, se complementa con scraping de páginas de promoción como:
  ```
  https://www.bdfutbol.com/es/t/t2023-24aPRF.html
  https://www.bdfutbol.com/es/t/t2023-24aPR3.html
  ```
