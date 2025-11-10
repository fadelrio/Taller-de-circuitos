import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo = "triangula2.csv"

# Parámetros del osciloscopio (según encabezado del archivo)
sampling_rate = 500e6     # 500 MSa/s = 500 millones de muestras por segundo
data_points = 64000       # número total de puntos

# === LECTURA DE DATOS ===
# Ignorar encabezado hasta llegar a los datos numéricos
with open(archivo, 'r') as f:
    lineas = f.readlines()

# Encontrar primera línea numérica
for i, linea in enumerate(lineas):
    try:
        float(linea.strip().split()[0])
        inicio_datos = i
        break
    except ValueError:
        continue

# Cargar los datos en milivoltios
datos_mV = np.loadtxt(archivo, skiprows=inicio_datos)
# Convertir a voltios
datos_V = datos_mV / 1000.0

# === ESCALA DE TIEMPO ===
dt = 1 / sampling_rate            # intervalo entre muestras [s]
tiempo_total = len(datos_V) * dt  # duración total de la adquisición
t = np.linspace(0, tiempo_total, len(datos_V), endpoint=False)

# === SELECCIÓN DE FRAGMENTO ===
# Elegí el fragmento que querés ver (en segundos)
t_inicio = 3.85e-6   # por ejemplo: 0 µs
t_fin = 43.85e-6     # por ejemplo: 20 µs

# Convertir a índices
idx_ini = int(t_inicio / dt)
idx_fin = int(t_fin / dt)

# Limitar a los rangos válidos
idx_ini = max(0, idx_ini)
idx_fin = min(len(datos_V), idx_fin)

# Recortar los datos
t_frag = t[idx_ini:idx_fin] - t[idx_ini]  # eje de tiempo reiniciado
y_frag = datos_V[idx_ini:idx_fin]

# === GRAFICAR ===
plt.figure(figsize=(10, 5))
plt.plot(t_frag * 1e6, y_frag, color='b')
plt.title("Señal cuadrada")
plt.xlabel("Tiempo [µs]")
plt.ylabel("Tensión [V]")
plt.grid(True)
plt.tight_layout()
plt.show()

# === INFO ADICIONAL ===
print(f"Duración total de la señal: {tiempo_total*1e6:.2f} µs")
print(f"Fragmento mostrado: {t_inicio*1e6:.2f} µs a {t_fin*1e6:.2f} µs")
print(f"Cantidad total de puntos: {len(datos_V)}")
print(f"Cantidad de puntos mostrados: {len(y_frag)}")

