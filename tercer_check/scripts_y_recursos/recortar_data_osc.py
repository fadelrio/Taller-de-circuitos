import numpy as np
import re

# === CONFIGURACIÓN ===
archivo_entrada = "esc_carg2.csv"
archivo_salida = "esc_carg2_recortado.csv"
t_inicial_us = 15.5   # [µs]
t_final_us = 44     # [µs]

# === LEER ARCHIVO ===
with open(archivo_entrada, "r", encoding="latin1") as f:
    lineas = f.readlines()

# === EXTRAER METADATOS ===
# Buscar base de tiempo y cantidad de puntos en el encabezado
base_tiempo_us = None
puntos_totales = None

for linea in lineas:
    if "Base" in linea and "μs" in linea:
        try:
            base_tiempo_us = float(re.findall(r"([\d.]+)", linea)[0])
        except Exception:
            pass
    if "points" in linea:
        try:
            puntos_totales = int(re.findall(r"(\d+)", linea)[0])
        except Exception:
            pass

# Valores por defecto si no se encuentran
if base_tiempo_us is None:
    base_tiempo_us = float(input("No se detectó Base de tiempo. Ingrese valor en µs/div: "))
if puntos_totales is None:
    puntos_totales = 64000  # valor típico

# === DETERMINAR TIEMPO TOTAL ===
tiempo_total_us = base_tiempo_us * 10  # normalmente 10 divisiones horizontales

# === LEER DATOS NUMÉRICOS ===
datos = []
for linea in lineas:
    linea = linea.strip().replace(",", ".")
    try:
        valor = float(linea)
        datos.append(valor)
    except ValueError:
        continue

if len(datos) == 0:
    raise ValueError("No se detectaron datos numéricos en el archivo.")

# === CREAR EJE DE TIEMPO ===
n = len(datos)
t_us = np.linspace(0, tiempo_total_us, n)

# === FILTRAR RANGO ===
mask = (t_us >= t_inicial_us) & (t_us <= t_final_us)
t_rec = t_us[mask]
v_rec = np.array(datos)[mask]

# === ESCRIBIR NUEVO ARCHIVO ===
with open(archivo_salida, "w", encoding="latin1") as f:
    # Copiar encabezado (las líneas no numéricas)
    for linea in lineas:
        if not any(c.isdigit() for c in linea.strip()):
            f.write(linea)
    # Escribir datos recortados
    for v in v_rec:
        f.write(f"\t\t{v:.4f}\n")

print(f"✅ Archivo '{archivo_salida}' creado con {len(v_rec)} puntos entre {t_inicial_us} µs y {t_final_us} µs.")

