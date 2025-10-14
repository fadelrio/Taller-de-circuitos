import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo1 = "data_regcar_par.txt"  # [RL, Vo]
archivo2 = "data_reglin_par.txt"  # [Vin, Vo]
r1 = 5
r2 = 100

# === Función notación de ingeniería ===
def eng_format(x, sig_figs=3):
    if x == 0:
        return "0"
    exp = int(np.floor(np.log10(abs(x)) / 3) * 3)
    mant = x / (10 ** exp)
    prefixes = {
        -12: "p", -9: "n", -6: "µ", -3: "m",
         0: "", 3: "k", 6: "M", 9: "G", 12: "T"
    }
    prefix = prefixes.get(exp, f"e{exp}")
    return f"{mant:.{sig_figs}g} {prefix}"

# === Cargar archivo 1 (salteando cabecera) ===
data1 = np.loadtxt(archivo1, skiprows=2)
RL = data1[:, 0]
Vo1 = data1[:, 1]

# Buscar el valor más cercano a r1 y r2
idx_r1 = np.argmin(np.abs(RL - r1))
idx_r2 = np.argmin(np.abs(RL - r2))
v1 = Vo1[idx_r1]
v2 = Vo1[idx_r2]

print(f"Usando RL≈{RL[idx_r1]} → v1={v1}")
print(f"Usando RL≈{RL[idx_r2]} → v2={v2}")

# Calcular regcar
regcar = ((1 - v1/v2) * r2) / ((v1/v2) * (r2/r1) - 1)

# === Graficar archivo 1 ===
plt.figure(figsize=(7,5))
plt.plot(RL, Vo1, "-", label="Vo vs RL", linewidth = 2)
plt.xlabel("RL [Ω]")
plt.ylabel("Vo [V]")
plt.title("Curva de regulación de carga")
plt.grid(True)
plt.legend()

# Mostrar regcar en el gráfico
plt.text(.8, .1, f"Regulación de carga = {eng_format(regcar)}Ω",
         transform=plt.gca().transAxes,
         fontsize=10, bbox=dict(facecolor="white", alpha=0.7))

# === Cargar archivo 2 (salteando cabecera) ===
data2 = np.loadtxt(archivo2, skiprows=1)
Vin = data2[:, 0]
Vo2 = data2[:, 1]

# Buscar el valor más cercano a 12V y 24V
idx_vin12 = np.argmin(np.abs(Vin - 12))
idx_vin24 = np.argmin(np.abs(Vin - 24))
vo1 = Vo2[idx_vin12]
vo2 = Vo2[idx_vin24]

print(f"Usando Vin≈{Vin[idx_vin12]} → vo1={vo1}")
print(f"Usando Vin≈{Vin[idx_vin24]} → vo2={vo2}")

# Calcular reglin
reglin = (vo2 - vo1) / 12

# === Graficar archivo 2 ===
plt.figure(figsize=(7,5))
plt.plot(Vin, Vo2, "-", label="Vo vs Vin", linewidth = 2)
plt.xlabel("Vin [V]")
plt.ylabel("Vo [V]")
plt.title("Curva de regulación de linea")
plt.grid(True)
plt.legend()

# Mostrar reglin en el gráfico
plt.text(.8, .1, f"Regulación de linea = {eng_format(reglin)}V",
         transform=plt.gca().transAxes,
         fontsize=10, bbox=dict(facecolor="white", alpha=0.7))

plt.show()

