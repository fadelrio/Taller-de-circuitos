# Nombre del archivo de entrada y salida
archivo_entrada = "data_potencia_raw.txt"
archivo_salida = "data_potencia_formatted.txt"

# Abrir los archivos con la codificación adecuada
with open(archivo_entrada, "r", encoding="latin1") as entrada, open(archivo_salida, "w", encoding="utf-8") as salida:
    for linea in entrada:
        try:
            # Separar la línea en dos partes usando el tabulador como delimitador
            partes = linea.strip().split("\t")
            
            if len(partes) == 2:
                # Primera parte (sin cambios)
                x = partes[0]
                
                # Segunda parte (eliminar paréntesis, 'dB' y '°', luego dividir en dos valores)
                y_z = partes[1].replace("(", "").replace(")", "").replace("dB", "").replace("°", "")
                y, z = map(float, y_z.split(","))
                
                # Escribir en el archivo de salida con el formato solicitado
                salida.write(f"{x} {y} {z}\n")
            else:
                # Si la línea no tiene el formato esperado, la ignoramos
                print(f"Línea ignorada (formato inválido): {linea.strip()}")
        except ValueError as e:
            # Imprimir errores específicos para depuración
            print(f"Error al procesar la línea: {linea.strip()} - {e}")

print(f"Datos formateados guardados en '{archivo_salida}'.")


