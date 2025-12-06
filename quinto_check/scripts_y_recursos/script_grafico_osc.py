import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo = "TP3_carga_dinamica.CSV"
tiempo_total = 14e-6      # tiempo total en segundos
t_inicio =0e-6           # tiempo desde el que quiero empezar a graficar
t_fin = 14e-6             # tiempo máximo hasta el que quiero graficar

# === CARGA ===
datos = np.loadtxt(archivo, delimiter=",", skiprows=3, usecols=1)

# Número de muestras
N = len(datos)

# Vector de tiempo original
t = np.linspace(0, tiempo_total, N)

# === AJUSTAR TIEMPO (correr el cero) ===
t_shift = t - t_inicio

# === FILTRAR POR t_inicio y t_fin ===
mask = (t_shift >= 0) & (t <= t_fin)
t_shift = t_shift[mask]
datos = datos[mask]

# === Conversión de tensión a corriente ===
datos = datos

# === GRAFICAR ===
plt.figure(figsize=(8, 5))
plt.plot((t_shift * 1e6), datos, linewidth=2)

plt.xlabel("Tiempo [us]")
plt.ylabel("Tension [V]")
plt.grid(True)

plt.tight_layout()
plt.show()

