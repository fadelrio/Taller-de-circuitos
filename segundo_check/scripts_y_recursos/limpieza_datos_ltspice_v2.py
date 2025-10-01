import re
import csv

# === PARÁMETROS ===
archivo_entrada = "segundo_check_comp_1u.txt"
archivo_salida = "segundo_check_comp_bonito_1u.csv"

# Encabezados que pediste
encabezados = [
    "frecuencia",
    "mod_comp_corriente", "fase_comp_corriente",
    "mod_comp_tension", "fase_comp_tension",
    "mod_sin_comp_corriente", "fase_sin_comp_corriente",
    "mod_sin_comp_tension", "fase_sin_comp_tension"
]

# Regex para extraer valores del tipo (XdB,Y°)
patron = re.compile(r"\(([-+0-9.eE]+)dB,([-+0-9.eE]+)°\)")

with open(archivo_entrada, "r", encoding="latin1") as f_in, \
     open(archivo_salida, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(encabezados)  # escribir cabecera

    for linea in f_in:
        linea = linea.strip()
        if not linea:
            continue

        partes = linea.split("\t")  # dividir por tabulaciones
        frecuencia = float(partes[0])  # primera columna

        # Extraer los pares dB y ° de las demás columnas
        valores = []
        for col in partes[1:]:
            m = patron.search(col)
            if m:
                mod = float(m.group(1))   # magnitud en dB
                fase = float(m.group(2))  # fase en grados
                valores.extend([mod, fase])
            else:
                raise ValueError(f"No se pudo parsear la columna: {col}")

        # Escribir la fila
        writer.writerow([frecuencia] + valores)

print(f"Conversión terminada. Archivo guardado en: {archivo_salida}")

