import re
import numpy as np
import matplotlib.pyplot as plt

# ===============================
#   LEER Y PARSEAR EL ARCHIVO
# ===============================

freq = []
mag = []
phase = []

with open("bode_buck.txt", "r") as f:
    for line in f:
        match = re.search(r'([\d\.eE\+\-]+)\s*\(\s*([\d\.\+\-eE]+)dB\s*,\s*([\d\.\+\-eE]+)°\s*\)', line)
        if match:
            freq.append(float(match.group(1)))
            mag.append(float(match.group(2)))
            phase.append(float(match.group(3)))

freq = np.array(freq)
mag = np.array(mag)
phase = np.array(phase)

# ===============================
#           GRAFICAR
# ===============================

plt.figure(figsize=(10, 6))

# Eje principal (magnitud)
ax1 = plt.gca()
ax1.semilogx(freq, mag, label="Magnitud (dB)")
ax1.set_xlabel("Frecuencia (Hz)")
ax1.set_ylabel("Magnitud (dB)")
ax1.grid(True, which="both", ls="--")

# Segundo eje para la fase
ax2 = ax1.twinx()
ax2.semilogx(freq, phase, color="orange", label="Fase (°)")
ax2.set_ylabel("Fase (°)")

# Título
plt.title("Bode - Magnitud y Fase (ejes separados)")

# Leyenda combinada
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc="best")

plt.tight_layout()

# ===============================
#     GUARDAR EN EPS
# ===============================
plt.savefig("bode_combined.eps", format="eps", dpi=300)

plt.show()


