# -*- coding: utf-8 -*-
"""
Lee un txt con columnas: r_l  V(vin)  V(vo)  I(RL1)  I(VIN1)
y grafica:  -100 * ((V(vo) * I(RL)) / (V(VIN) * I(VIN)))  vs  I(RL)

Uso rápido:
- Editá RUTA_ARCHIVO con tu archivo.
- Ejecutá: python script.py
"""

import re
import matplotlib.pyplot as plt
from pathlib import Path

# === CONFIGURACIÓN ===
RUTA_ARCHIVO = "data_pot_vs_r_log.txt"   # <-- Cambiá esto
GUARDAR_COMO = "grafico_eficiencia_vs_corriente.png"

def es_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def leer_datos(ruta: str):
    """
    Devuelve listas: i_rl, vvin, vvo, ivin
    Ignora líneas que no tengan al menos 5 números válidos.
    """
    i_rl, vvin, vvo, ivin = [], [], [], []

    p = Path(ruta)
    if not p.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # separa por cualquier cantidad de espacios o tabs
            toks = re.split(r"\s+", line)
            # necesitamos al menos 5 columnas numéricas
            if len(toks) < 5:
                continue

            # intentamos parsear las 5 primeras como float
            # (si falla, la línea no es de datos)
            try:
                # col 0 = r_l (no usada), 1=V(VIN), 2=V(vo), 3=I(RL), 4=I(VIN)
                _r_l  = float(toks[0])
                v_in  = float(toks[1])
                v_o   = float(toks[2])
                i_rl_ = float(toks[3])
                i_in  = float(toks[4])
            except ValueError:
                # no es línea de datos (encabezados, "Step Information:", etc.)
                continue

            vvin.append(v_in)
            vvo.append(v_o)
            i_rl.append(i_rl_)
            ivin.append(i_in)

    if not i_rl:
        raise RuntimeError("No se encontraron filas de datos válidas. "
                           "¿El archivo tiene el formato esperado?")
    return i_rl, vvin, vvo, ivin

def main():
    i_rl, vvin, vvo, ivin = leer_datos(RUTA_ARCHIVO)

    # y = -100 * (V(vo) * I(RL)) / (V(VIN) * I(VIN))
    y = []
    for Vo, IRL, Vin, Iin in zip(vvo, i_rl, vvin, ivin):
        denom = Vin * Iin
        if denom == 0:
            y.append(float("nan"))  # evita división por cero
        else:
            y.append(-100.0 * (Vo * IRL) / denom)

    # --- GRAFICAR ---
    plt.figure(figsize=(7, 4.5))
    plt.plot(i_rl, y, linewidth=2)
    plt.xlabel(r"$I_o$ [A]")
    plt.ylabel("Eficiencia [%]")
    plt.title(r"Eficiencia vs $I_o$ ($V_{IN} = 9.5V)$")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(GUARDAR_COMO,format='png')
    print(f"Gráfico guardado como: {GUARDAR_COMO}")
    plt.show()

if __name__ == "__main__":
    main()
