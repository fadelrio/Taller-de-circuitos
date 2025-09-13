import re
import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo1 = "data_foldback.txt"  # [RL, Vo]

data1 = np.loadtxt(archivo1, skiprows=1)
vo = data1[:, 1]
irl = data1[:, 2]

# === Graficar archivo 1 ===
plt.figure(figsize=(7,5))
plt.plot(irl, vo, "-", linewidth = 2)
plt.xlabel(r"$I_{o}$ [A]")
plt.ylabel(r"$V_{o}$ [V]")
plt.grid(True)

plt.show()
