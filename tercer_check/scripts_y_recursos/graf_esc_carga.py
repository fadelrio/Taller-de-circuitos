import numpy as np
import matplotlib.pyplot as plt

# === Parámetros del archivo ===
archivo = "esc_carg_recortado.csv"
puntos_totales_original = 64000
tiempo_total_original = 10e-6 * 10  # 100 µs en total

# === Leer archivo e ignorar encabezado ===
with open(archivo, "r", encoding="latin1") as f:
    lineas = f.readlines()

# Filtrar solo los datos numéricos
datos = []
for linea in lineas:
    linea = linea.strip().replace(",", ".")
    try:
        valor = float(linea)
        datos.append(valor)
    except ValueError:
        continue

# === Calcular eje de tiempo ===
# Intervalo temporal entre muestras (del archivo original)
dt = tiempo_total_original / puntos_totales_original
n = len(datos)
t = np.arange(n) * dt  # tiempo en segundos

# === Graficar ===
plt.figure(figsize=(10, 5))
plt.plot(t * 1e6, datos, color='b')
plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [mV]")
plt.title("Curva de tensión vs tiempo (esc_carg_recortado.csv)")
plt.grid(True)
plt.tight_layout()
plt.show()

