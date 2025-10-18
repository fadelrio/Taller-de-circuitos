import numpy as np
import matplotlib.pyplot as plt

# === ARCHIVO DE ENTRADA ===
archivo_csv = "bajja.csv"  # <-- cambialo si el nombre es otro

# === CONFIGURACIÓN DEL OSCILOSCOPIO ===
puntos_totales_original = 32000
tiempo_total_original = 320e-5  # <-- COMPLETAR si corresponde (ej: 50e-6, 500e-6, etc.)

# === PARÁMETROS DE RECORTE ===
t_inicio_us = 0     # arranca en 300 µs del tiempo original
t_fin_us_nuevo = 3200  # termina a los 400 µs del nuevo eje (es decir, 700 µs del original)

# === LECTURA DE DATOS ===
datos = []
with open(archivo_csv, "r", encoding="latin1") as f:
    for linea in f:
        linea = linea.strip().replace("\ufeff", "")
        if not linea or not any(c.isdigit() for c in linea):
            continue
        partes = linea.replace(",", " ").split()
        try:
            numeros = [float(p) for p in partes]
            if len(numeros) >= 2:
                datos.append(numeros[:2])
        except ValueError:
            continue

if len(datos) == 0:
    raise ValueError("No se encontraron datos numéricos válidos en el archivo.")

datos = np.array(datos)

# === CORRECCIÓN DE OFFSET (RESTAR VALOR FINAL) ===
ch1 = datos[:, 0] - datos[-1, 0]
if datos.shape[1] > 1:
    ch2 = datos[:, 1] - datos[-1, 1]
else:
    ch2 = None

# === CONVERSIÓN A VOLTIOS ===
ch1 = ch1 / 1000.0
if ch2 is not None:
    ch2 = ch2 / 1000.0

# === EJE DE TIEMPO ===
n = len(datos)
dt = tiempo_total_original / puntos_totales_original
t = np.arange(n) * dt  # tiempo en segundos

# === RECORTE ENTRE t_inicio_us Y (t_inicio_us + t_fin_us_nuevo) ===
t_ini = t_inicio_us * 1e-6
t_fin = (t_inicio_us + t_fin_us_nuevo) * 1e-6
mask = (t >= t_ini) & (t <= t_fin)

t = t[mask] - t_ini  # redefinir tiempo para que arranque en 0
ch1 = ch1[mask]
if ch2 is not None:
    ch2 = ch2[mask]

# === GRAFICAR ===
plt.figure(figsize=(10, 5))
plt.plot(t * 1e3, ch1, label="Tensión de salida", color="b")
if ch2 is not None:
    plt.plot(t * 1e3, ch2, label="Tensión de entrada", color="r")

plt.xlabel("Tiempo [ms]")
plt.ylabel("Tensión [V]")
plt.title("Tiempo de encendido")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

