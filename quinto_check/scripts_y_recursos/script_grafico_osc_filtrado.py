import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt  # <-- agregado

# === CONFIGURACIÓN ===
archivo = "ripple_12_10.CSV"
tiempo_total = 70e-6      # tiempo total en segundos
t_inicio = 0e-6           # tiempo desde el que quiero empezar a graficar
t_fin = 70e-6             # tiempo máximo hasta el que quiero graficar

# === FILTRO MEDIANA ===
ventana_ms = 0.00050e-3   # 0.00015 ms = 1.5e-7 s

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

# === Calcular dt y tamaño de ventana en muestras ===
dt = t_shift[1] - t_shift[0]
Nventana = int(round(ventana_ms / dt))

# Hacerlo impar (requisito del medfilt)
if Nventana % 2 == 0:
    Nventana += 1
if Nventana < 3:
    Nventana = 3

print(f"Ventana de mediana: {Nventana} muestras")

# === Aplicar filtro mediana ===
datos = medfilt(datos, kernel_size=Nventana)

# === Conversión de tensión a corriente (ajuste relativo) ===
datos = datos - datos[0]

# === GRAFICAR ===
plt.figure(figsize=(8, 5))
plt.plot((t_shift * 1e6), datos, linewidth=2)

plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [V]")
plt.grid(True)

plt.tight_layout()
plt.show()

