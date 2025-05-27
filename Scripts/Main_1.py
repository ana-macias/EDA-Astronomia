import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# --- RUTAS ABSOLUTAS---
# Ruta del archivo original NASA)
ruta_nasa = r"C:\\Users\\amaci\\Documents\\EDA_Astronomia\\EDA-Astronomia\\Datasets\\nasa.csv"
# Ruta para guardar el CSV limpio
ruta_hipotesis = r"C:\\Users\\amaci\\Documents\\EDA_Astronomia\\EDA-Astronomia\\Datasets\\hipotesis_7.csv"
# Cargar datos originales (saltando 96 filas de metadatos)
data = pd.read_csv(ruta_nasa, skiprows=96)
# Columnas a conservar para el análisis
columnas_a_conservar = [
    'pl_name',        # nombre del planeta
    'pl_bmasse',      # masa terrestre
    'pl_rade',        # radio del planeta
    'pl_insol',       # irradiancia
    'pl_eqt',         # temperatura de equilibrio
    'pl_orbeccen',    # excentricidad orbital
    'pl_orbsmax',     # semieje mayor orbital
    'sy_pnum',        # número de planetas en el sistema
    'sy_snum',        # número de estrellas en el sistema
    'st_spectype',    # tipo espectral de la estrella
    'st_teff',        # temperatura de la estrella
    'discoverymethod' # método de descubrimiento
]
# Filtrar solo las columnas seleccionadas
df_hipotesis = data[columnas_a_conservar]
# Guardar DataFrame limpio en nuevo CSV
df_hipotesis.to_csv(ruta_hipotesis, index=False)
print(f"Datos limpios guardados en: {ruta_hipotesis}") # Guardar DF en un nuevo CSV desde el que trabajaré
# QUE GRAFICAS PUEDO HACER CON ESTE CSV
# HEATMAP
# Seleccionar solo columnas numéricas
numeric_df = df_hipotesis.select_dtypes(include='number')
# Calcular matriz de correlación
correlation_matrix = numeric_df.corr()
# Configurar el heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    linewidths=0.5,
    vmin=-1,            # Valor mínimo de la escala
    vmax=1              # Valor máximo de la escala
)
plt.title("Mapa de Calor de Correlaciones (Escala -1 a 1)")
# Guardar y mostrar gráfico (RUTA ABSOLTA PARA GUARDAR)
ruta_imagen = r"C:\\Users\\amaci\\Documents\\EDA_Astronomia\\EDA-Astronomia\\Imagenes\\heatmap.png"
plt.savefig(ruta_imagen)
plt.show()  











