import numpy as np
import matplotlib.pyplot as plt
import os

# === CONFIGURACIÓN ===
archivo_base = "data_regcar_par.txt"     # [RL, Vo]
archivo_med = "mediciones_regcar2.txt"   # [Vo, RL, (opcional) DVo, DRL%]
r1 = 5
r2 = 100

# === Función notación de ingeniería ===
def eng_format(x, sig_figs=3):
    if x == 0:
        return "0"
    exp = int(np.floor(np.log10(abs(x)) / 3) * 3)
    mant = x / (10 ** exp)
    prefixes = {-12:"p",-9:"n",-6:"µ",-3:"m",0:"",3:"k",6:"M",9:"G",12:"T"}
    return f"{mant:.{sig_figs}g} {prefixes.get(exp, f'e{exp}')}"

# === Cargar curva base ===
data_base = np.loadtxt(archivo_base, skiprows=2)
RL_base, Vo_base = data_base[:, 0], data_base[:, 1]

# Puntos teóricos
idx_r1 = np.argmin(np.abs(RL_base - r1))
idx_r2 = np.argmin(np.abs(RL_base - r2))
v1, v2 = Vo_base[idx_r1], Vo_base[idx_r2]
regcar_base = ((1 - v1/v2) * r2) / ((v1/v2) * (r2/r1) - 1)

print(f"[BASE] RL≈{RL_base[idx_r1]}Ω → V1={v1:.3f} V")
print(f"[BASE] RL≈{RL_base[idx_r2]}Ω → V2={v2:.3f} V")
print(f"[BASE] Regulación de carga = {regcar_base:.3e} Ω")

# === Cargar mediciones ===
data_med = np.loadtxt(archivo_med, skiprows=1)
Vo_med, RL_med = data_med[:, 0], data_med[:, 1]
DVo = data_med[:, 2] if data_med.shape[1] >= 3 else np.zeros_like(Vo_med)
DRL = (data_med[:, 3] / 100 * RL_med) if data_med.shape[1] >= 4 else np.zeros_like(RL_med)

# Ordenar por RL
orden = np.argsort(RL_med)
RL_med, Vo_med, DVo, DRL = RL_med[orden], Vo_med[orden], DVo[orden], DRL[orden]

# Puntos experimentales
idx_r1m = np.argmin(np.abs(RL_med - r1))
idx_r2m = np.argmin(np.abs(RL_med - r2))
v1m, v2m = Vo_med[idx_r1m], Vo_med[idx_r2m]
regcar_med = ((1 - v1m/v2m) * r2) / ((v1m/v2m) * (r2/r1) - 1)

print(f"[MEDICIÓN] RL≈{RL_med[idx_r1m]}Ω → V1={v1m:.3f} V")
print(f"[MEDICIÓN] RL≈{RL_med[idx_r2m]}Ω → V2={v2m:.3f} V")
print(f"[MEDICIÓN] Regulación de carga = {regcar_med:.3e} Ω")

# === GRAFICAR ===
plt.figure(figsize=(7,5))
plt.plot(RL_base, Vo_base, '-', color='b', linewidth=2, label="Curva teórica")

if np.any(DVo) or np.any(DRL):
    plt.errorbar(RL_med, Vo_med, xerr=DRL, yerr=DVo,
                 fmt='o', color='r', ecolor='k', elinewidth=1.2, capsize=3)
    plt.plot(RL_med, Vo_med, '-', color='r', linewidth=1.5, label="Mediciones")
else:
    plt.plot(RL_med, Vo_med, 'r-', linewidth=1.5, label="Mediciones")

plt.xlabel("RL [Ω]")
plt.ylabel("Vo [V]")
plt.title("Curva de regulación de carga")
plt.grid(True)
plt.legend()

texto = f"Teórica: {eng_format(regcar_base)}Ω\nMedida: {eng_format(regcar_med)}Ω"
plt.text(0.68, 0.1, texto, transform=plt.gca().transAxes,
         fontsize=10, bbox=dict(facecolor="white", alpha=0.7))

plt.show()

