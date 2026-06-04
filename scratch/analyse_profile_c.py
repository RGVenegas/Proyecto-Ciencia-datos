import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"

df = pd.read_csv(DATA_RAW)

# Filtrar registros en el dataset que tengan:
# Num_Entidades_Deuda == 3
# Peor_Calificacion_12M == 1
# Y veamos la distribución de RiesgoAlto en ese subconjunto.
subset = df[(df["Num_Entidades_Deuda"] == 3) & (df["Peor_Calificacion_12M"] == 1)]
print(f"Cantidad de registros con Num_Entidades_Deuda = 3 y Peor_Calificacion_12M = 1: {len(subset)}")
print("Distribución de RiesgoAlto en este subset:")
print(subset["RiesgoAlto"].value_counts())

# Ahora veamos el Ratio_Saldo_Ingreso de este subset
print("\nEstadísticas de Ratio_Saldo_Ingreso en este subset:")
print(subset.groupby("RiesgoAlto")["Ratio_Saldo_Ingreso"].describe())

# Perfil C corregido tiene Ratio_Saldo_Ingreso = 0.1042
# Veamos cuántos de este subset tienen un ratio cercano a 0.1042 (por ejemplo entre 0.08 y 0.13)
subset_ratio = subset[(subset["Ratio_Saldo_Ingreso"] >= 0.08) & (subset["Ratio_Saldo_Ingreso"] <= 0.13)]
print(f"\nCantidad con ratio entre 0.08 y 0.13: {len(subset_ratio)}")
print("Distribución de RiesgoAlto:")
print(subset_ratio["RiesgoAlto"].value_counts())
