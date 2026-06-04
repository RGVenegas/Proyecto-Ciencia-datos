import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"

df = pd.read_csv(DATA_RAW)
print("=== Dimensiones y Columnas ===")
print(df.shape)
print(df.columns)

print("\n=== Primeras 5 filas ===")
print(df.head())

print("\n=== Distribución de RiesgoAlto ===")
print(df["RiesgoAlto"].value_counts())

print("\n=== Estadísticas por clase (RiesgoAlto) ===")
stats = df.groupby("RiesgoAlto").agg({
    "Num_Entidades_Deuda": ["mean", "median", "max"],
    "Peor_Calificacion_12M": ["mean", "median", "max"],
    "Reportes_Central_12M": ["mean", "median", "max"],
    "Reportes_Central_36M": ["mean", "median", "max"],
    "Ingreso_CLP": ["mean", "median"],
    "Saldo_Total_CLP": ["mean", "median"],
    "Ratio_Saldo_Ingreso": ["mean", "median", "max"]
})
print(stats)

print("\n=== Valores de Peor_Calificacion_12M por RiesgoAlto ===")
print(pd.crosstab(df["Peor_Calificacion_12M"], df["RiesgoAlto"]))

print("\n=== Valores de Num_Entidades_Deuda por RiesgoAlto ===")
print(pd.crosstab(df["Num_Entidades_Deuda"], df["RiesgoAlto"]))
