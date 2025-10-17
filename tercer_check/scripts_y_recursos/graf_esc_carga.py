import numpy as np
import matplotlib.pyplot as plt

# === ARCHIVOS ===
archivo_csv = "esc_carg2_recortado.csv"   # salida del osciloscopio
archivo_sim = "escalon_carg_1u.txt"       # simulación SPICE

# === CONFIGURACIÓN DEL OSCILOSCOPIO ===
puntos_totales_original = 64000
tiempo_total_original = 128e-6  # duración total de la adquisición (128 µs en este caso)

# === LEER DATOS DEL OSCILOSCOPIO ===
with open(archivo_csv, "r", encoding="latin1") as f:
    lineas = f.readlines()

datos_osc = []
for linea in lineas:
    linea = linea.strip().replace(",", ".")
    try:
        valor = float(linea)
        datos_osc.append(valor)
    except ValueError:
        continue

datos_osc = np.array(datos_osc)

# Eje de tiempo del osciloscopio
n = len(datos_osc)
dt = tiempo_total_original / puntos_totales_original
t_osc = np.arange(n) * dt  # tiempo en segundos

# === LEER DATOS DE LA SIMULACIÓN ===
datos_sim = np.loadtxt(archivo_sim, skiprows=1)
t_sim = datos_sim[:, 0]        # tiempo [s]
v_sim = datos_sim[:, 1] * 1000 # convertir a mV

# === AJUSTE DE OFFSET ===
datos_osc = datos_osc - datos_osc[0]  # corrección de offset en medición
v_sim = v_sim - v_sim[0]              # corrección de offset en simulación

# === GRAFICAR ===
plt.figure(figsize=(10, 5))
plt.plot(t_osc * 1e6, datos_osc, label="Medición", color='b')
plt.plot(t_sim * 1e6, v_sim, label="Simulación", color='r', linestyle='--')

plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [mV]")
plt.title("Escalon de carga simulado y medido")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

