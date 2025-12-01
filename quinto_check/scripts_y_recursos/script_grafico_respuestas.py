import numpy as np
import matplotlib.pyplot as plt

# ==== ARCHIVOS ====
archivo1 = "respuesta_compensada.txt"   # <-- cambiá por tu archivo
archivo2 = "respuesta_sin_compensar.txt"   # <-- cambiá por tu archivo

# ==== FUNCIÓN PARA CARGAR ====
def cargar_archivo(nombre):
    # carga dos columnas: tiempo y tensión
    data = np.loadtxt(nombre, skiprows = 1)
    t = data[:, 0]
    v = data[:, 1]
    return t, v

# ==== CARGA DE DATOS ====
t1, v1 = cargar_archivo(archivo1)
t2, v2 = cargar_archivo(archivo2)

# ==== GRÁFICO ====
plt.figure(figsize=(8, 5))

plt.plot(t1*1000, v1, label=f"Respuesta compensada", linewidth=2)

plt.xlabel("Tiempo [ms]")
plt.ylabel("Tensión [V]")
plt.grid(True)
plt.legend()


plt.figure(figsize=(8, 5))

plt.plot(t2*1000, v2, label="Respuesta sin compensar", linewidth=2)

plt.xlabel("Tiempo [ms]")
plt.ylabel("Tensión [V]")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

