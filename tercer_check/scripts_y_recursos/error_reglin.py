import pandas as pd

# Nombre de archivo de entrada y salida
archivo_entrada = "mediciones_reglin.txt"
archivo_salida = "mediciones_reglin_completo.txt"

# Leer el archivo, separando por tabulaciones o espacios
df = pd.read_csv(archivo_entrada, sep=r'\s+', engine='python')

# Función para contar cantidad de decimales
def contar_decimales(valor):
    try:
        s = str(valor).strip()
        if '.' in s:
            return len(s.split('.')[1])
        else:
            return 0
    except:
        return 0

# Función para calcular la incertidumbre
def calcular_incertidumbre(valor):
    decimales = contar_decimales(valor)
    if decimales == 3:
        digito = 0.001
    elif decimales == 2:
        digito = 0.01
    else:
        # Si no hay decimales, asumimos error de 1 unidad en el último dígito (1.0)
        digito = 1.0
    return valor * 0.7 / 100 + 3 * digito

# Calcular DVin y DVout si no existen o están incompletas
df['DVin[V]'] = df['Vin[V]'].apply(calcular_incertidumbre)
df['DVout[V]'] = df['Vout[V]'].apply(calcular_incertidumbre)

# Guardar el nuevo archivo con formato tabulado
df.to_csv(archivo_salida, sep='\t', index=False, float_format='%.6f')

print(f"Archivo generado: {archivo_salida}")
print(df)

