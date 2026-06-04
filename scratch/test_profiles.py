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

print("Modelo seleccionado:", metadata.get("modelo_seleccionado"))
print("Feature names:", feature_names)
print("Valores de referencia:", referencia)

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
    print("Cliente completo antes de transformar:")
    print(cliente_completo.model_dump())
    
    # Transformar registro
    vector_escalado = transform_single_record(cliente_completo.model_dump(), feature_names, scaler)
    print("Vector escalado:")
    print(vector_escalado)
    
    # Predicción
    prob = model.predict_proba(vector_escalado)[0]
    pred = model.predict(vector_escalado)[0]
    print(f"Predicción clase: {pred}, Probabilidad de Riesgo Alto: {prob[1]:.4f} ({prob[1]*100:.2f}%)")
