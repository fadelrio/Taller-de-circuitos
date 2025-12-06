import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo = "gates_mosfets.CSV"
tiempo_total = 28e-6      # tiempo total en segundos
t_inicio = 0e-6           # tiempo desde el que empieza a graficar
t_fin = 28e-6             # tiempo máximo a graficar

# === CARGA ===
# Carga columnas 1 y 2 (índices 1 y 2)
datos = np.loadtxt(archivo, delimiter=",", skiprows=3, usecols=(1, 2))

# Separar columnas
dato1 = datos[:, 0]
dato2 = datos[:, 1]

# Número de muestras
N = len(datos)

# Vector de tiempo original
t = np.linspace(0, tiempo_total, N)

# === AJUSTAR TIEMPO (correr el cero) ===
t_shift = t - t_inicio

# === FILTRAR POR t_inicio y t_fin ===
mask = (t_shift >= 0) & (t <= t_fin)

t_shift = t_shift[mask]
dato1 = dato1[mask]
dato2 = dato2[mask]

# === GRAFICAR ===
plt.figure(figsize=(8, 5))

plt.plot(t_shift * 1e6, dato1, linewidth=2)
plt.plot(t_shift * 1e6, dato2, linewidth=2)

plt.xlabel("Tiempo [us]")
plt.ylabel("Tensión [V]")
plt.grid(True)

plt.tight_layout()
plt.show()

