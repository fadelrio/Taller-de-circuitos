import numpy as np
import matplotlib.pyplot as plt

# === ARCHIVO DE ENTRADA ===
archivo = "mediciones_eficiencia_fuente.txt"

# === LECTURA DE DATOS ===
# Se asume que la primera fila tiene encabezados
datos = np.loadtxt(archivo, skiprows=1)

Iin = datos[:, 0]
Iout = datos[:, 1]
Vout = datos[:, 3]
Vin = datos[:, 2]

# === CÁLCULO DE EFICIENCIA ===
eficiencia = (Vout * Iout) / (Vin * Iin) * 100

# === GRÁFICO ===
plt.figure(figsize=(8,5))
plt.plot(Vin, eficiencia, 'r-o', label='Eficiencia')

plt.xlabel('Tensión de entrada[V]')
plt.ylabel('Eficiencia [%]')
plt.title('Eficiencia vs Tensión de entrada')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Ajustar límites
plt.xlim(left=0)
#plt.ylim(0, 110)

plt.show()

