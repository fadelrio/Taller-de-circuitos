import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN GENERAL ===
archivo = "rta_temp_b.csv"

# Podés ajustar estos si querés controlar la ventana gráfica
t_inicio = 0e-6
t_fin = None            # Si ponés None, no recorta por el final

# Si querés convertir a corriente: I = V / R
usar_conversion_corriente = False
resistencia = 0.47      # ohms

# === LECTURA DEL ARCHIVO ===
with open(archivo, "r") as f:
    lineas = f.readlines()

# Extraer encabezado
time_base = None
sampling_rate = None
data_unit = None

datos_raw = []

for linea in lineas:
    l = linea.strip()

    if l.startswith("Time Base:"):
        # Ejemplo: Time Base:5.00μs
        valor = l.split(":")[1].strip()
        if valor.endswith("μs"):
            time_base = float(valor[:-2]) * 1e-6
        elif valor.endswith("ms"):
            time_base = float(valor[:-2]) * 1e-3
        elif valor.endswith("s"):
            time_base = float(valor[:-1])

    elif l.startswith("Sampling Rate:"):
        # Ejemplo: 500MSa/s
        valor = l.split(":")[1].strip()
        if valor.endswith("MSa/s"):
            sampling_rate = float(valor[:-5]) * 1e6
        elif valor.endswith("GSa/s"):
            sampling_rate = float(valor[:-5]) * 1e9
        elif valor.endswith("kSa/s"):
            sampling_rate = float(valor[:-6]) * 1e3
        else:
            sampling_rate = float(valor.rstrip("Sa/s"))

    elif l.startswith("Data Uint:") or l.startswith("Data Unit:"):
        data_unit = l.split(":")[1].strip().lower()

    else:
        # Intentar interpretar como dato numérico
        try:
            datos_raw.append(float(l))
        except:
            pass   # líneas no numéricas se ignoran

# Convertir lista a numpy
datos = np.array(datos_raw)

# === CONVERSIÓN DE UNIDADES ===
if data_unit == "mv":
    datos = datos / 1000.0    # pasamos mV → V
elif data_unit == "v":
    pass                      # ya está en volt
# si aparece otra unidad, la agrego

# === Vector de tiempo ===
N = len(datos)
# periodo de muestreo
Ts = 1.0 / sampling_rate
t = np.arange(N) * Ts

# === AJUSTAR t_inicio ===
t_shift = t - t_inicio
mask = t_shift >= 0

# === RECORTE POR t_fin ===
if t_fin is not None:
    mask = mask & (t <= t_fin)

t_shift = t_shift[mask]
datos = datos[mask]

# === CONVERSIÓN A CORRIENTE (opcional) ===
if usar_conversion_corriente:
    datos = datos / resistencia

# === GRAFICO ===
plt.figure(figsize=(10,5))
plt.plot(t_shift * 1e6, datos - datos[0], linewidth=1.5)

plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [V]" if not usar_conversion_corriente else "Corriente [A]")
plt.grid(True)
plt.tight_layout()
plt.show()


