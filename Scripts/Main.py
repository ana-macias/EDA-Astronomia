import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# data =pd.read_csv(r'C:\\Users\\amaci\\Documents\\EDA_Astronomia\\EDA-Astronomia\\Datasets\\nasa.csv', skiprows=96)
data =pd.read_csv('../Datasets/nasa.csv', skiprows=96)
# Columnas a consevar del CSV Original

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

# HIPOTESIS 1 #
# __________________________________________________________________________________________
# Utilizamos las filas de las columnas necesarias para esta hipótesis
cols_necesarias = ["pl_name","pl_insol", "pl_bmasse", "pl_eqt",'st_spectype', 'discoverymethod']

df = df_hipotesis.dropna(subset=cols_necesarias)

# Fijamos la zona habitable como insolación entre 0.35 y 2 veces la de la Tierra
zona_habitable = df[(df["pl_insol"] >= 0.35) & (df["pl_insol"] <= 2)]

# Planetas fuera de la zona habitable
fuera_zona_habitable = df[(df["pl_insol"] < 0.35) | (df["pl_insol"] > 2)]

# Estadísticas comparativas
comparacion = {
    "Dentro Zona Habitable": zona_habitable["pl_eqt"].describe(),
    "Fuera Zona Habitable": fuera_zona_habitable["pl_eqt"].describe()
}

# Filtro de candidatos con condiciones similares a la Tierra
candidatos_vida = zona_habitable[
    (zona_habitable["pl_eqt"] >= 200) &
    (zona_habitable["pl_eqt"] <= 320)
]

# Seleccionamos columnas relevantes y ordenamos
candidatos_vida_seleccion = candidatos_vida[["pl_name", "pl_bmasse", "pl_eqt", "pl_insol"]].sort_values(by="pl_eqt")
print(candidatos_vida_seleccion)
#_____________________________________________________________________________________________
# Grafico Scatterplot con los 19 planetas
plt.figure(figsize=(10, 6))
sns.scatterplot(data=candidatos_vida_seleccion, x='pl_eqt', y='pl_insol')
for _, row in candidatos_vida_seleccion.iterrows():
    plt.text(row['pl_eqt']+2, row['pl_insol'], row['pl_name'], fontsize=8)

# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'ScatterplotNombres19.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/ScatterplotNombres19.jpg')
#_____________________________________________________________________________________________
# Filtrar planetas con temperatura de equilibrio conocida
df_temp = df[df['pl_eqt'].notna()]

#_____________________________________________________________________________________________
# Grafico KDE  respecto a la T de equilibrio

#plt.figure(figsize=(10, 6))
#sns.kdeplot(data=df_temp[df_temp['en_zona_habitable'] == True], x='pl_eqt', label='En zona habitable', fill=True)
#sns.kdeplot(data=df_temp[df_temp['en_zona_habitable'] == False], x='pl_eqt', label='Fuera de zona habitable', fill=True)

#plt.title('Distribución KDE de temperatura de equilibrio (pl_eqt)')
#plt.xlabel('Temperatura de equilibrio (K)')
#plt.ylabel('Densidad estimada')
#plt.xlim(0, 1000)  # Ajusta si hay valores extremos
#plt.legend()
#plt.grid(True)
# Creamos la ruta de cada gráfico
#ruta = '../img/intro'
#os.makedirs(ruta, exist_ok=True)
#nombre_archivo = 'KdeTemperaturas.jpg'
#plt.savefig(os.path.join(ruta,nombre_archivo))
#plt.savefig('../Imagenes/KdeTemperaturas.jpg')

# HIPOTESIS 2 #
#_______________________________________________________________________________________________
# Definir la zona habitable como insolación entre 0.35 y 2 veces la de la Tierra
zona_habitable = df[(df["pl_insol"] >= 0.35) & (df["pl_insol"] <= 2)]
zona_habitable

# Planetas fuera de la zona habitable
fuera_zona_habitable = df[(df["pl_insol"] < 0.35) | (df["pl_insol"] > 2)]

# Estadísticas comparativas
comparacion = {
    "Dentro Zona Habitable": zona_habitable[["pl_bmasse", "pl_eqt"]].describe(),
    "Fuera Zona Habitable": fuera_zona_habitable[["pl_bmasse", "pl_eqt"]].describe()
}

# Filtro de candidatos con condiciones similares a la Tierra
candidatos_vida = zona_habitable[
    (zona_habitable["pl_bmasse"] >= 0.8) & 
    (zona_habitable["pl_bmasse"] <= 10) &
    (zona_habitable["pl_eqt"] >= 200) &
    (zona_habitable["pl_eqt"] <= 320)
]

# Seleccionar columnas relevantes y ordenar
candidatos_vida_seleccion = candidatos_vida[["pl_name", "pl_bmasse", "pl_eqt", "pl_insol"]].sort_values(by="pl_eqt")

# _____________________________________________________________________________________________
# Grafico de Barras
# Crear columna si está en zona habitable
df['en_zona_habitable'] = df['pl_insol'].between(0.35, 2)

# Filtrar masas entre 0.8 y 10
df_rango = df[(df['pl_bmasse'].notna()) & (df['pl_bmasse'] >= 0.8) & (df['pl_bmasse'] <= 10)].copy()

# Definir rangos de masa dentro de ese intervalo
bins = [0.8, 2, 4, 6, 8, 10]
labels = ['0.8–2', '2–4', '4–6', '6–8', '8–10']
df_rango['masa_rango'] = pd.cut(df_rango['pl_bmasse'], bins=bins, labels=labels, include_lowest=True)

# Agrupar y contar
conteo = df_rango.groupby(['masa_rango', 'en_zona_habitable']).size().unstack(fill_value=0)

# Graficar
conteo.plot(kind='bar', figsize=(10, 6), color=['salmon', 'mediumseagreen'])
plt.title('Planetas por rango de masa (0.8–10) y zona habitable')
plt.xlabel('Rango de masa (masas terrestres)')
plt.ylabel('Cantidad de planetas')
plt.legend(title='En zona habitable', labels=['No', 'Sí'])
plt.xticks(rotation=0)
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'Barras.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/Barras.jpg')

#_____________________________________________________________________________________________
# Grafico Scatterplot temperaturas de equilibrio
# Filtrar planetas con temperatura y masa disponibles
df_scatter = df[df['pl_eqt'].notna() & df['pl_bmasse'].notna()]

# Crear scatterplot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_scatter, x='pl_eqt', y='pl_bmasse', hue='en_zona_habitable', alpha=0.7)

# Marcar zona tipo Tierra (opcional)
plt.axvspan(200, 320, color='green', alpha=0.1, label='Zona temp. tipo Tierra')
plt.axhspan(0.8, 10, color='blue', alpha=0.05, label='Masa tipo Tierra')

plt.title('Temperatura de equilibrio vs Masa planetaria')
plt.xlabel('Temperatura de equilibrio (K)')
plt.ylabel('Masa (masas terrestres)')
plt.xlim(0, 1000)
plt.ylim(0, 20)
plt.legend(title='En zona habitable')
plt.grid(True)
plt.tight_layout()
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'Scatterplot.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/Scatterplot.jpg')

#___________________________________________________________________________________________________
# Gráfico Scatterplot con los 13 planetas
plt.figure(figsize=(10, 6))
sns.scatterplot(data=candidatos_vida_seleccion, x='pl_eqt', y='pl_bmasse')
for _, row in candidatos_vida_seleccion.iterrows():
    plt.text(row['pl_eqt']+2, row['pl_bmasse'], row['pl_name'], fontsize=8)
   
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'ScatterplotNombres13.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/ScatterplotNombres13.jpg')

#_____________________________________________________________________________________________
# HIPOTESIS 3
# Filtrar filas donde el tipo espectral comienza con G, K o M
df_filtered = df[df['st_spectype'].str.startswith(('G', 'K', 'M'), na=False)]

def espectral_valida(row):
    tipo = row['st_spectype'][0]  # primera letra
    temp = row['st_teff']
    if tipo == 'G':
        return 5300 <= temp <= 6000
    elif tipo == 'K':
        return 3900 <= temp <= 5300
    elif tipo == 'M':
        return 2000 <= temp <= 3500
    return False

# Aplicar la función para crear una nueva columna de verificación
df_filtered['teff_valida'] = df_filtered.apply(espectral_valida, axis=1)

df_filtered[['pl_name', 'st_spectype', 'st_teff', 'teff_valida']]

#__________________________________________________________________________________
# Grafico de barras tipo de planeta
# Agrupar y contar los tipos espectrales (primer carácter)
df_filtered["tipo_spectral"] = df_filtered["st_spectype"].str[0]
conteo = df_filtered["tipo_spectral"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
sns.barplot(x=conteo.index, y=conteo.values, palette="viridis")
plt.title("Cantidad de planetas habitables por tipo espectral de estrella")
plt.xlabel("Tipo espectral")
plt.ylabel("Número de planetas habitables")
plt.grid(True, axis='y')
plt.tight_layout()
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'BarrasPlanetas.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/BarrasPlanetas.jpg')


# De estos 271, alguno está en la zona habitable?
# Filtrar planetas habitables
habitables = df_filtered[
    (df_filtered["pl_bmasse"] >= 0.5) & (df_filtered["pl_bmasse"] <= 10) & 
    (df_filtered["pl_eqt"] >= 200) & (df_filtered["pl_eqt"] <= 320) & 
    (df_filtered["pl_insol"] >= 0.35) & (df_filtered["pl_insol"] <= 2)
]

# Grafico Scatterplot con estos nuevos 13 planetas
plt.figure(figsize=(10, 6))
sns.scatterplot(data=habitables, x='pl_eqt', y='pl_bmasse')
for _, row in habitables.iterrows():
    plt.text(row['pl_eqt']+2, row['pl_bmasse'], row['pl_name'], fontsize=8)

# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'ScatterplotNombres.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/ScatterplotNombres.jpg')

#_________________________________________________________________________________________________
# HIPOTESIS 4
# Clasificar órbitas
df_clean = df.copy()
df_clean = df_clean[df_clean['pl_orbeccen'].notnull()]
df_clean['orbital_type'] = np.where(df_clean['pl_orbeccen'] < 0.1, 'Casi circular', 'Excéntrica')

# Filtrar exoplanetas con datos suficientes para análisis de habitabilidad
df_filtrado = df_clean[
    df_clean[['pl_bmasse', 'pl_insol', 'pl_eqt', 'st_teff']].notnull().any(axis=1)
]

# Definimos criterio de habitabilidad:
# - pl_insol entre 0.35 y 2 (zona habitable aproximada)
# - o temperatura de equilibrio entre 200K y 320K
# - y estrella con temperatura entre 5000K y 6000K (tipo solar)
df_filtrado['en_zona_habitable'] = (
    ((df_filtrado['pl_insol'].between(0.35, 2)) | 
     (df_filtrado['pl_eqt'].between(200, 320))) &
    (df_filtrado['st_teff'].between(5000, 6000))
)
# Estadísticas comparativas
hab_stats = df_filtrado.groupby('orbital_type')['en_zona_habitable'].agg(['count', 'sum', 'mean'])
hab_stats.rename(columns={'count': 'Total', 'sum': 'Habitables', 'mean': 'Proporción'}, inplace=True)

#___________________________________________________________________________________________
# Grafico de barras órbita
# Comparar cuántos planetas tienen órbitas casi circulares vs. excéntricas.
sns.countplot(data=df_filtrado, x='orbital_type')
plt.title("Distribución de Tipos de Órbitas")
plt.xlabel("Tipo de Órbita")
plt.ylabel("Número de Exoplanetas")
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'BarrasOrbita.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/BarrasOrbita.jpg')

#_____________________________________________________________________________________________
# Gráfico de barras órbita y habitabilidad
# Comparar cuántos planetas potencialmente habitables tienen órbitas circulares o excéntricas.

sns.countplot(data=df_filtrado, x='orbital_type', hue='en_zona_habitable')
plt.title("Exoplanetas en Zona Habitable por Tipo de Órbita")
plt.xlabel("Tipo de Órbita")
plt.ylabel("Número de Exoplanetas")
plt.legend(title="¿En zona habitable?")
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'BarrasOrbitaHabitable.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/BarrasOrbitaHabitable.jpg')

#______________________________________________________________________________________________
# HIPOTESIS 5
# Extraer nombre del sistema (todo antes del primer espacio en pl_name)
df['system_name'] = df['pl_name'].str.extract(r'^([^\s]+)')

# Definir si el planeta está en la zona habitable:
# - Irradiancia entre 0.35 y 2 o temperatura de equilibrio entre 180K y 310K
# - Estrella tipo solar (temperatura entre 5000K y 6000K)
df['en_zona_habitable'] = (
    ((df['pl_insol'].between(0.35, 2)) | (df['pl_eqt'].between(200, 320))) &
    (df['st_teff'].between(5000, 6000))
)

# Agrupar por sistema: tomar número de planetas y si hay alguno habitable
systems = df.groupby('system_name').agg({
    'sy_pnum': 'first',
    'en_zona_habitable': 'max'  # True si al menos uno es habitable
}).rename(columns={'en_zona_habitable': 'tiene_planetas_habitables'})

# Agrupar por cantidad de planetas y calcular estadísticas
result = systems.groupby('sy_pnum')['tiene_planetas_habitables'].agg(['count', 'sum', 'mean'])
result.rename(columns={'count': 'Total Sistemas', 'sum': 'Con Habitables', 'mean': 'Proporción'}, inplace=True)

#___________________________________________________________________________________________________
# Grafico de barras número de planetas
# Resetear el índice para facilitar graficar
result_reset = result.reset_index()

fig, ax1 = plt.subplots(figsize=(8, 6))

# Barras: proporción de sistemas con habitables
ax1.bar(result_reset['sy_pnum'], result_reset['Proporción'], color='skyblue')
ax1.set_xlabel('Número de Planetas en el Sistema')
ax1.set_ylabel('Proporción con Planetas Habitables', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(0, 1)
ax1.set_title('Proporción de Sistemas con Planetas Habitables vs. Número de Planetas')

plt.tight_layout()
# Creamos la ruta de cada gráfico
ruta = '../img/intro'
os.makedirs(ruta, exist_ok=True)
nombre_archivo = 'BarrasNumeroPlanetas.jpg'
plt.savefig(os.path.join(ruta,nombre_archivo))
plt.savefig('../Imagenes/BarrasNumeroPlanetas.jpg')

# FINAL 
candidatos_vida.to_csv('../Datasets/candidatos_tipo_tierra.csv', index=False)
print (candidatos_vida)

