import numpy as np
import matplotlib.pyplot as plt
import os

# === CONFIGURACIÓN ===
archivo_teorico = "data_foldback.txt"        # [RL, Vo]
archivo_mediciones = "mediciones_foldback.txt"  # [Vo, Io, (opcional: errV, errI)]

# === CARGAR CURVA TEÓRICA ===
data_teo = np.loadtxt(archivo_teorico, skiprows=1)
vo_teo = data_teo[:, 1]
io_teo = data_teo[:, 2]

# === INTENTAR CARGAR MEDICIONES ===
if not os.path.exists(archivo_mediciones):
    raise FileNotFoundError(f"No se encontró el archivo {archivo_mediciones}")

data_med = np.loadtxt(archivo_mediciones, skiprows=1)

# Estructura mínima esperada: 2 columnas (Vo, Io)
vo_med = data_med[:, 0]
io_med = data_med[:, 1]

# Verificar si existen columnas de error
if data_med.shape[1] >= 3:
    err_v = data_med[:, 2]
else:
    err_v = np.zeros_like(vo_med)

if data_med.shape[1] >= 4:
    err_i = data_med[:, 3]
else:
    err_i = np.zeros_like(io_med)

# === IMPRIMIR DATOS ===
print("\n--- Mediciones ---")
for idx in range(len(vo_med)):
    txt = f"Punto {idx+1}:  Vo = {vo_med[idx]:.5f} V"
    if np.any(err_v):  # si hay errores no nulos
        txt += f" ±{err_v[idx]:.5f} V"
    txt += f"   |   Io = {io_med[idx]:.5f} A"
    if np.any(err_i):
        txt += f" ±{err_i[idx]:.6f} A"
    print(txt)

# === GRAFICAR ===
plt.figure(figsize=(7,5))
plt.plot(io_teo, vo_teo, "-", linewidth=2, label="Curva teórica")

if np.any(err_v) or np.any(err_i):
    plt.errorbar(io_med, vo_med, xerr=err_i, yerr=err_v,
                 fmt='ro', ecolor='gray', capsize=3, label="Mediciones (±inc.)")
    plt.plot(io_med, vo_med, 'r--', linewidth=1.5)
else:
    plt.plot(io_med, vo_med, 'ro--', label="Mediciones")

plt.xlabel(r"$I_{o}$ [A]")
plt.ylabel(r"$V_{o}$ [V]")
plt.title("Curva Foldback: Teórica vs. Medida")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

