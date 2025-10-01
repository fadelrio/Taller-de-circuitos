import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === PARÁMETROS ===
archivo_csv = "segundo_check_comp_bonito.csv"

# Leer CSV
df = pd.read_csv(archivo_csv)

# Definición de señales: (mod, fase, nombre, tipo)
seniales = [
    ("mod_comp_corriente", "fase_comp_corriente", "Lazo de corriente", "corriente"),
    ("mod_comp_tension", "fase_comp_tension", "Lazo de tension compensado", "tension"),
    ("mod_sin_comp_corriente", "fase_sin_comp_corriente", "Lazo de corriente", "corriente"),
    ("mod_sin_comp_tension", "fase_sin_comp_tension", "Lazo de tension sin compensar", "tension"),
]

# Función para calcular margen de fase
def calcular_margen_fase(freq, mag_db, fase, tipo):
    # Buscar cruce de 0 dB
    idx = np.where(np.diff(np.sign(mag_db)))[0]
    if len(idx) == 0:
        return None, None
    i = idx[0]
    # Interpolar frecuencia de cruce
    f_cruce = np.interp(0, [mag_db[i], mag_db[i+1]], [freq[i], freq[i+1]])
    # Interpolar fase en ese cruce
    fase_cruce = np.interp(f_cruce, freq, fase)

    if tipo == "corriente":
        margen_fase = 180 + fase_cruce
    else:  # tensión
        margen_fase = 360 + fase_cruce

    return f_cruce, margen_fase

# Graficar cada señal
for mod_col, fase_col, nombre, tipo in seniales:
    freq = df["frecuencia"].values
    mag_db = df[mod_col].values
    fase = df[fase_col].values

    # Ajuste de fase para señales de tensión
    if tipo == "tension":
        fase = fase - 360

    # Calcular margen de fase
    f_cruce, margen_fase = calcular_margen_fase(freq, mag_db, fase, tipo)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    fig.suptitle(f"Bode - {nombre}")

    # Magnitud
    ax1.semilogx(freq, mag_db, label="Magnitud")
    ax1.set_ylabel("Magnitud (dB)")
    ax1.grid(True, which="both", ls="--")

    if f_cruce:
        ax1.axvline(f_cruce, color="r", linestyle="--", alpha=0.7)

    # Fase
    ax2.semilogx(freq, fase, label="Fase", color="g")
    ax2.set_ylabel("Fase (°)")
    ax2.set_xlabel("Frecuencia (Hz)")
    ax2.grid(True, which="both", ls="--")

    if f_cruce:
        ax2.axvline(f_cruce, color="r", linestyle="--", alpha=0.7)
        # Mostrar datos en un recuadro
        texto_info = (f"Frecuencia de cruce: {f_cruce:.2f} Hz\n"
                      f"Margen de fase: {margen_fase:.2f}°")
        ax2.text(
            0.98, 0.95, texto_info,
            transform=ax2.transAxes,
            fontsize=10,
            va="top", ha="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
        )

    plt.tight_layout()
    plt.show()

