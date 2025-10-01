import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# Lista de archivos a graficar
archivos = [
    "escalon_ent_15u_sc.txt",
    "escalon_carg_15u_sc.txt",
    "escalon_ref_15u_sc.txt",
    "escalon_ent_1u_sc.txt",
    "escalon_carg_1u_sc.txt",
    "escalon_ref_1u_sc.txt"
]

# Diccionario para los títulos (puedes modificar los valores)
titulos = {
    "escalon_ent_15u_sc.txt": "Escalón Entrada 15u sin compensar",
    "escalon_carg_15u_sc.txt": "Escalón Carga 15u sin compensar",
    "escalon_ref_15u_sc.txt": "Escalón Referencia 15u sin compensar",
    "escalon_ent_1u_sc.txt": "Escalón Entrada 1u sin compensar",
    "escalon_carg_1u_sc.txt": "Escalón Carga 1u sin compensar",
    "escalon_ref_1u_sc.txt": "Escalón Referencia 1u sin compensar"
}

# Formateador para el eje X (notación de ingeniería en segundos)
formatter = EngFormatter(unit='s')

# Recorremos todos los archivos
for archivo in archivos:
    # Leer el archivo, separador por espacios, saltando encabezado
    df = pd.read_csv(archivo, sep=r"\s+", skiprows=1, names=["Tiempo [s]", "Tensión [V]"])
    
    # Crear figura
    fig, ax = plt.subplots()
    ax.plot(df["Tiempo [s]"], df["Tensión [V]"], color="b")
    
    # Títulos y etiquetas
    ax.set_title(titulos.get(archivo, archivo))
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Tensión [V]")
    
    # Aplicar notación de ingeniería al eje X
    ax.xaxis.set_major_formatter(formatter)
    
    ax.grid(True)

# Mostrar todas las figuras al final
plt.show()

