import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv('nasa.csv', skiprows=96) # CSV Original que limpio

columnas_a_conservar = [
    'pl_name',        # nombre del planeta
    'pl_bmasse',      # masa terrestre
    'pl_rade',        # radio del planeta
    'pl_insol',       # irradiancia
    'pl_eqt',         # temperatura de equilibrio
    'pl_orbeccen',    # excentricidad orbital
    'pl_orbsmax',
    'sy_pnum',        # número de planetas en el sistema
    'sy_snum',
    'st_spectype',    # tipo espectral de la estrella
    'st_teff',        # temperatura de la estrella
    'discoverymethod'
]                       
df_hipotesis = data[columnas_a_conservar]
df_hipotesis.to_csv('../Datasets/hipotesis_2.csv') # Guardar DF en un nuevo CSV desde el que trabajaré

# QUE GRAFICAS PUEDO HACER CON ESTE CSV
# HEATMAP
# Seleccionar solo columnas numéricas
numeric_df = df_hipotesis.select_dtypes(include='number')

# Calcular la matriz de correlación
correlation_matrix = numeric_df.corr()

# Generar el heatmap con escala entre -1 y 1
plt.figure(figsize=(6, 4))
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    cmap='coolwarm', 
    fmt=".2f", 
    linewidths=0.5, 
    vmin=-1, 
    vmax=1
)
plt.title("Mapa de Calor de Correlaciones (Escala -1 a 1)")
plt.savefig()
plt.show()