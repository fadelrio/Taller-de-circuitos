import numpy as np
import matplotlib.pyplot as plt

# Parámetros del archivo
archivo = "esc_carg.csv"
puntos_totales = 64000
tiempo_total = 10e-6 * 10  # 10 µs/div × 10 divisiones = 100 µs

# Leer archivo ignorando encabezado
with open(archivo, "r", encoding="latin1") as f:
    lineas = f.readlines()

# Filtrar líneas que contengan números
datos = []
for linea in lineas:
    linea = linea.strip().replace(",", ".")
    try:
        valor = float(linea)
        datos.append(valor)
    except ValueError:
        continue

# Generar eje de tiempo
n = len(datos)
t = np.linspace(0, tiempo_total, n)

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(t * 1e6, datos, color='b')  # tiempo en microsegundos
plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [mV]")
plt.title("Curva de tensión vs tiempo (esc_carg.csv)")
plt.grid(True)
plt.tight_layout()
plt.show()

