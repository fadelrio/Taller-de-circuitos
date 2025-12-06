import numpy as np
import matplotlib.pyplot as plt

# === ARCHIVO DE ENTRADA ===
archivo = "mediciiones_reglin.txt"

# === LECTURA DE DATOS ===
# Se asume que la primera fila tiene encabezados
datos = np.loadtxt(archivo, delimiter=',', skiprows=1)

x = datos[:, 0]   # Tensión de entrada
y = datos[:, 1]   # Tensión de salida

# === REGRESIÓN LINEAL ===
coef = np.polyfit(x, y, 1)  # coef[0] = pendiente, coef[1] = intercepto
pendiente, intercepto = coef
recta = pendiente * x + intercepto

print("Pendiente:", pendiente)
print("Intercepto:", intercepto)

# === GRÁFICO ===
plt.figure(figsize=(8,5))

# Puntos discretos
plt.scatter(x, y, label='Datos medidos', s=30)

# Recta de regresión
plt.plot(x, recta, label='Recta de regresión', linestyle='--')

plt.xlabel('Tensión de entrada')
plt.ylabel('Tensión de salida')
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()

