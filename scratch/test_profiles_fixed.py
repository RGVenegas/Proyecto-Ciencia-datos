import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.artifacts import load_model, load_scaler, load_metadata
from src.preprocessing import transform_single_record
from src.api.schemas import EvaluacionCrediticiaInput

# Cargar artefactos
metadata = load_metadata()
model = load_model()
scaler = load_scaler()
feature_names = metadata["feature_names"]
referencia = metadata.get("valores_referencia", {})

# Definir los 3 perfiles del usuario
perfil_a = EvaluacionCrediticiaInput(
    Num_Entidades_Deuda=1,
    Peor_Calificacion_12M=0.0, # Normal
    Ingreso_CLP=2500000.0,
    Saldo_Total_CLP=250000.0,
    Variacion_Endeudamiento=0.0
)

perfil_b = EvaluacionCrediticiaInput(
    Num_Entidades_Deuda=6,
    Peor_Calificacion_12M=2.0, # Morosidad relevante
    Ingreso_CLP=800000.0,
    Saldo_Total_CLP=4000000.0,
    Variacion_Endeudamiento=0.45
)

perfil_c = EvaluacionCrediticiaInput(
    Num_Entidades_Deuda=3,
    Peor_Calificacion_12M=1.0, # Con atrasos leves
    Ingreso_CLP=1200000.0,
    Saldo_Total_CLP=1500000.0,
    Variacion_Endeudamiento=0.15
)

perfiles = {"Perfil A (Riesgo Bajo)": perfil_a, "Perfil B (Riesgo Alto)": perfil_b, "Perfil C (Riesgo Moderado)": perfil_c}

for name, input_data in perfiles.items():
    print(f"\n=== {name} ===")
    cliente_completo = input_data.to_cliente_completo(referencia)
    
    # IMPORTANTE: Corregimos el Ratio_Saldo_Ingreso para que coincida con la escala anual (dividido por 12)
    # recalculamos el ratio como saldo_total / (ingreso * 12)
    ratio_anual = round(cliente_completo.Saldo_Total_CLP / (cliente_completo.Ingreso_CLP * 12), 4)
    cliente_completo.Ratio_Saldo_Ingreso = ratio_anual
    
    print("Cliente completo corregido:")
    print(f"  Ingreso: {cliente_completo.Ingreso_CLP}")
    print(f"  Deuda: {cliente_completo.Saldo_Total_CLP}")
    print(f"  Ratio Saldo Ingreso (corregido): {cliente_completo.Ratio_Saldo_Ingreso}")
    
    # Transformar registro
    vector_escalado = transform_single_record(cliente_completo.model_dump(), feature_names, scaler)
    
    # Predicción
    prob = model.predict_proba(vector_escalado)[0]
    pred = model.predict(vector_escalado)[0]
    print(f"Predicción clase: {pred}, Probabilidad de Riesgo Alto: {prob[1]:.4f} ({prob[1]*100:.2f}%)")
