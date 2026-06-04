import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"

df = pd.read_csv(DATA_RAW)

print("=== Reportes_Central_12M ===")
print(df.groupby("RiesgoAlto")["Reportes_Central_12M"].describe())

print("\n=== Reportes_Central_36M ===")
print(df.groupby("RiesgoAlto")["Reportes_Central_36M"].describe())

print("\n=== Variacion_Endeudamiento ===")
print(df.groupby("RiesgoAlto")["Variacion_Endeudamiento"].describe())

# Veamos qué pasa si evaluamos el Perfil C pero con un Ratio de 0.5 en lugar de 1.25 (reduciendo la deuda total a 600.000)
# También queremos ver el efecto de Reportes_Central_12M y Reportes_Central_36M.
# En la API, el cliente se autocompleta con valores de referencia.
# En los valores de referencia (la mediana global):
# Reportes_Central_12M = 12
# Reportes_Central_36M = 30
# ¿Cuáles son los valores medianos de estas variables para la clase 0?
print("\n=== Medianas de la clase 0 (Riesgo bajo) ===")
print(df[df["RiesgoAlto"] == 0].median(numeric_only=True))

print("\n=== Medianas de la clase 1 (Riesgo alto) ===")
print(df[df["RiesgoAlto"] == 1].median(numeric_only=True))
