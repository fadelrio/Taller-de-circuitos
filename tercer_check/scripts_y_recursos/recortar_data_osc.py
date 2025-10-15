import numpy as np

# === Parámetros ===
archivo_entrada = "esc_carg.csv"
archivo_salida = "esc_carg_recortado.csv"
t_inicial_us = 37.51   # [µs]
t_final_us = 58.51     # [µs]
tiempo_total_us = 100  # [µs]
puntos_totales = 64000

# === Leer archivo original (solo valores numéricos) ===
with open(archivo_entrada, "r", encoding="latin1") as f:
    lineas = f.readlines()

datos = []
for linea in lineas:
    linea = linea.strip().replace(",", ".")
    try:
        valor = float(linea)
        datos.append(valor)
    except ValueError:
        continue

# === Crear eje de tiempo ===
n = len(datos)
t_us = np.linspace(0, tiempo_total_us, n)

# === Determinar índices del recorte ===
mask = (t_us >= t_inicial_us) & (t_us <= t_final_us)
t_rec = t_us[mask]
v_rec = np.array(datos)[mask]

# === Escribir nuevo archivo con mismo formato ===
with open(archivo_salida, "w", encoding="latin1") as f:
    # copiar encabezado (las líneas no numéricas)
    for linea in lineas:
        if not any(c.isdigit() for c in linea.strip()):
            f.write(linea)
    # escribir los datos recortados
    for v in v_rec:
        f.write(f"\t\t{v:.4f}\n")

print(f"Archivo '{archivo_salida}' creado con {len(v_rec)} puntos entre {t_inicial_us} µs y {t_final_us} µs.")

