import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo = "rta_apagado_10.CSV"

t_inicio = -0.00187999948      # tiempo desde donde quiero empezar a graficar
t_fin = 0.00247800086        # tiempo máximo a graficar

# === CARGA ===
# Carga columnas 3 y 4 (índices 3 y 4 → tiempo y tensión)
datos = np.loadtxt(archivo, delimiter=",", skiprows=2, usecols=(3, 4))

# Separar columnas
tiempo = datos[:, 0]
tension = datos[:, 1]

# === FILTRADO POR RANGO DE TIEMPO ===
# Seleccionar solo los puntos entre t_inicio y t_fin
mask = (tiempo >= t_inicio) & (tiempo <= t_fin)
tiempo_filtrado = tiempo[mask]
tension_filtrada = tension[mask]

# Hacer que t_inicio sea el nuevo cero
tiempo_filtrado = tiempo_filtrado - t_inicio

# === GRAFICAR ===
plt.figure(figsize=(8, 5))

plt.plot(tiempo_filtrado*1e3, tension_filtrada, linewidth=2)

plt.xlabel("Tiempo [ms]")
plt.ylabel("Tensión [V]")
plt.grid(True)

plt.tight_layout()
plt.show()

