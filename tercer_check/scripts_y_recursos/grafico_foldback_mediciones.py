import numpy as np
import matplotlib.pyplot as plt
import os

# === CONFIGURACIÓN ===
archivo_teorico = "data_foldback.txt"         # [RL, Vo]
archivo_mediciones = "mediciones_foldback.txt"  # [Vo, Io, (opcional: errV, errI)]

# === CARGAR CURVA TEÓRICA ===
data_teo = np.loadtxt(archivo_teorico, skiprows=1)
vo_teo, io_teo = data_teo[:, 1], data_teo[:, 2]

# === CARGAR MEDICIONES ===
if not os.path.exists(archivo_mediciones):
    raise FileNotFoundError(f"No se encontró {archivo_mediciones}")
data_med = np.loadtxt(archivo_mediciones, skiprows=1)
vo_med, io_med = data_med[:, 0], data_med[:, 1]
err_v = data_med[:, 2] if data_med.shape[1] >= 3 else np.zeros_like(vo_med)
err_i = data_med[:, 3] if data_med.shape[1] >= 4 else np.zeros_like(io_med)

# === IMPRIMIR DATOS ===
print("\n--- Mediciones ---")
for i, (v, iout) in enumerate(zip(vo_med, io_med)):
    texto = f"Punto {i+1}: Vo={v:.5f}V"
    if np.any(err_v): texto += f" ±{err_v[i]:.5f}V"
    texto += f" | Io={iout:.5f}A"
    if np.any(err_i): texto += f" ±{err_i[i]:.6f}A"
    print(texto)

# === GRAFICAR ===
plt.figure(figsize=(7,5))
plt.plot(io_teo, vo_teo, '-', color='b', linewidth=2, label="Curva teórica")

if np.any(err_v) or np.any(err_i):
    plt.errorbar(io_med, vo_med, xerr=err_i, yerr=err_v,
                 fmt='o', color='r', ecolor='k', elinewidth=1.2, capsize=3)
    plt.plot(io_med, vo_med, '-', color='r', linewidth=1.5, label="Mediciones")
else:
    plt.plot(io_med, vo_med, 'r-', linewidth=1.5, label="Mediciones")

plt.xlabel(r"$I_{o}$ [A]")
plt.ylabel(r"$V_{o}$ [V]")
plt.title("Curva Foldback")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

