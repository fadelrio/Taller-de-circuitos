import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
archivo_base = "data_reglin_par.txt"              # [Vin, Vo]
archivo_errores = "mediciones_reglin_completo.txt"  # [Vin, Vo, errVin?, errVo?]

# === Función notación de ingeniería ===
def eng_format(x, sig_figs=3):
    if x == 0:
        return "0"
    exp = int(np.floor(np.log10(abs(x)) / 3) * 3)
    mant = x / (10 ** exp)
    prefixes = {-12:"p",-9:"n",-6:"µ",-3:"m",0:"",3:"k",6:"M",9:"G",12:"T"}
    return f"{mant:.{sig_figs}g} {prefixes.get(exp, f'e{exp}')}"

# === Cargar datos base ===
data = np.loadtxt(archivo_base, skiprows=1)
Vin, Vo = data[:, 0], data[:, 1]

# Calcular regulación base
idx_vin12, idx_vin24 = np.argmin(np.abs(Vin - 12)), np.argmin(np.abs(Vin - 24))
vo1, vo2 = Vo[idx_vin12], Vo[idx_vin24]
reglin_base = (vo2 - vo1) / 12

print("=== Datos base ===")
print(f"Vin≈{Vin[idx_vin12]} → Vo={vo1}")
print(f"Vin≈{Vin[idx_vin24]} → Vo={vo2}")
print(f"Regulación de línea (base) = {eng_format(reglin_base)} V/V")

# === Cargar mediciones ===
datos_validos = []
with open(archivo_errores, "r") as f:
    next(f)
    for linea in f:
        partes = linea.strip().split()
        if len(partes) >= 2:
            vin = float(partes[0])
            vo = float(partes[1])
            errvin = float(partes[2]) if len(partes) > 2 and partes[2] != "" else 0.0
            errvo = float(partes[3]) if len(partes) > 3 and partes[3] != "" else 0.0
            datos_validos.append([vin, vo, errvin, errvo])

tiene_errores = len(datos_validos) > 0
if tiene_errores:
    data_err = np.array(datos_validos)
    Vin_err, Vo_err, errVin, errVo = data_err[:,0], data_err[:,1], data_err[:,2], data_err[:,3]

    # Calcular regulación con mediciones
    idx_vin12_err = np.argmin(np.abs(Vin_err - 12))
    idx_vin24_err = np.argmin(np.abs(Vin_err - 24))
    vo1_err, vo2_err = Vo_err[idx_vin12_err], Vo_err[idx_vin24_err]
    reglin_err = (vo2_err - vo1_err) / 12

    print("\n=== Mediciones ===")
    print(f"Vin≈{Vin_err[idx_vin12_err]} → Vo={vo1_err}")
    print(f"Vin≈{Vin_err[idx_vin24_err]} → Vo={vo2_err}")
    print(f"Regulación de línea (medida) = {eng_format(reglin_err)} V/V")

# === GRAFICAR ===
plt.figure(figsize=(7,5))
plt.plot(Vin, Vo, '-', color='b', linewidth=2, label="Curva teórica")

if tiene_errores:
    plt.errorbar(Vin_err, Vo_err, xerr=errVin, yerr=errVo,
                 fmt='o', color='r', ecolor='k', elinewidth=1.2, capsize=3)
    plt.plot(Vin_err, Vo_err, '-', color='r', linewidth=1.5, label="Mediciones")

plt.xlabel("Vin [V]")
plt.ylabel("Vo [V]")
plt.title("Curva de regulación de línea")
plt.xlim(0, 24)  # <== Límite del eje horizontal de 0 a 24 V
plt.grid(True)
plt.legend()

# Mostrar ambas regulaciones
texto = f"Teórica = {eng_format(reglin_base)}V"
if tiene_errores:
    texto += f"\nMedida = {eng_format(reglin_err)}V"

plt.text(0.68, 0.1, texto, transform=plt.gca().transAxes,
         fontsize=10, bbox=dict(facecolor="white", alpha=0.7))

plt.show()

