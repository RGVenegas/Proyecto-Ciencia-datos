import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.artifacts import load_model, load_scaler, load_metadata
from src.preprocessing import transform_single_record

df_raw = pd.read_csv(ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv")

# Cargar modelo entrenado
model = load_model()
scaler = load_scaler()
metadata = load_metadata()
feature_names = metadata["feature_names"]
referencia = metadata["valores_referencia"]

records = []
# Evaluamos todo el dataset
for index, row in df_raw.iterrows():
    record_dict = row.to_dict()
    record_dict["Ratio_Saldo_Ingreso"] = record_dict["Saldo_Total_CLP"] / record_dict["Ingreso_CLP"]
    
    vector = transform_single_record(record_dict, feature_names, scaler)
    prob = model.predict_proba(vector)[0][1]
    pred = model.predict(vector)[0]
    
    records.append({
        "Index": index,
        "Num_Entidades_Deuda": int(row["Num_Entidades_Deuda"]),
        "Peor_Calificacion_12M": float(row["Peor_Calificacion_12M"]),
        "Ingreso_CLP": float(row["Ingreso_CLP"]),
        "Saldo_Total_CLP": float(row["Saldo_Total_CLP"]),
        "Variacion_Endeudamiento": float(row["Variacion_Endeudamiento"]),
        "RiesgoAlto_Real": int(row["RiesgoAlto"]),
        "Prob_Modelo": prob,
        "Pred_Modelo": pred
    })

df_results = pd.DataFrame(records)

# 1. Buscar caso de Riesgo Bajo (prob < 0.05)
bajo = df_results[df_results["Prob_Modelo"] < 0.05].head(2)
print("=== CASOS DE RIESGO BAJO (Prob < 5%) ===")
for idx, r in bajo.iterrows():
    print(f"Num_Entidades_Deuda: {r['Num_Entidades_Deuda']}, Peor_Calificacion_12M: {r['Peor_Calificacion_12M']}, Ingreso_CLP: {r['Ingreso_CLP']:.0f}, Saldo_Total_CLP: {r['Saldo_Total_CLP']:.0f}, Variacion_Endeudamiento: {r['Variacion_Endeudamiento']:.2f} -> Prob: {r['Prob_Modelo']*100:.2f}%")

# 2. Buscar caso de Riesgo Moderado (30% <= prob <= 70%)
moderado = df_results[(df_results["Prob_Modelo"] >= 0.20) & (df_results["Prob_Modelo"] <= 0.80)].sort_values("Prob_Modelo")
print("\n=== CASOS DE RIESGO MODERADO (20% - 80%) ===")
if not moderado.empty:
    for idx, r in moderado.head(5).iterrows():
        print(f"Num_Entidades_Deuda: {r['Num_Entidades_Deuda']}, Peor_Calificacion_12M: {r['Peor_Calificacion_12M']}, Ingreso_CLP: {r['Ingreso_CLP']:.0f}, Saldo_Total_CLP: {r['Saldo_Total_CLP']:.0f}, Variacion_Endeudamiento: {r['Variacion_Endeudamiento']:.2f} -> Prob: {r['Prob_Modelo']*100:.2f}%")
else:
    print("No se encontraron casos en todo el dataset en el rango 20% - 80%.")

# 3. Buscar caso de Riesgo Alto (prob > 95%)
alto = df_results[df_results["Prob_Modelo"] > 0.95].head(2)
print("\n=== CASOS DE RIESGO ALTO (Prob > 95%) ===")
for idx, r in alto.iterrows():
    print(f"Num_Entidades_Deuda: {r['Num_Entidades_Deuda']}, Peor_Calificacion_12M: {r['Peor_Calificacion_12M']}, Ingreso_CLP: {r['Ingreso_CLP']:.0f}, Saldo_Total_CLP: {r['Saldo_Total_CLP']:.0f}, Variacion_Endeudamiento: {r['Variacion_Endeudamiento']:.2f} -> Prob: {r['Prob_Modelo']*100:.2f}%")

# Buscar cuáles son los valores de probabilidad únicos para entender la distribución del modelo
print("\nProbabilidades únicas del modelo (primeras 20):")
print(df_results["Prob_Modelo"].value_counts().head(20))
