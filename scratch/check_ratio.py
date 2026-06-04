import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"

df = pd.read_csv(DATA_RAW)

print(df[['Saldo_Total_CLP', 'Ingreso_CLP', 'Ratio_Saldo_Ingreso']].head(10))

# Calculemos el ratio directamente para estas filas
print("\nRatio calculado manual (Saldo / Ingreso):")
print((df['Saldo_Total_CLP'] / df['Ingreso_CLP']).head(10))

# Veamos si hay alguna diferencia de escala o si el ratio en el dataset es otra cosa,
# como por ejemplo Saldo_Total_CLP / (Ingreso_CLP * 12) o algo similar.
# Veamos el cociente entre el ratio del dataset y el calculado manual:
manual = df['Saldo_Total_CLP'] / df['Ingreso_CLP']
ratio_dataset = df['Ratio_Saldo_Ingreso']
cociente = ratio_dataset / manual
print("\nCociente (Ratio Dataset / Ratio Manual):")
print(cociente.head(10))
print("\nEstadísticas del Cociente:")
print(cociente.describe())
