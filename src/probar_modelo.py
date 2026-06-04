"""Verifica la carga del modelo exportado y resume metadata."""
import json
import sys
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import METADATA_PATH, MODEL_PATH

print("=== Verificación de artefactos ===")
print(f"Modelo: {MODEL_PATH} -> {'OK' if MODEL_PATH.exists() else 'NO ENCONTRADO'}")

if MODEL_PATH.exists():
    modelo = joblib.load(MODEL_PATH)
    print(f"Tipo de algoritmo: {type(modelo).__name__}")
    if hasattr(modelo, "feature_importances_"):
        print("Primeras 5 importancias:", modelo.feature_importances_[:5])
    elif hasattr(modelo, "coef_") and modelo.coef_ is not None:
        print("Primeros 5 coeficientes:", modelo.coef_.ravel()[:5])

if METADATA_PATH.exists():
    with open(METADATA_PATH, encoding="utf-8") as handle:
        metadata = json.load(handle)
    print(f"Modelo seleccionado: {metadata.get('modelo_seleccionado')}")
    print(f"F1 test: {metadata.get('metricas_test', {}).get('f1')}")

print("\nPara probar la API: uvicorn src.api.main:app --host 127.0.0.1 --port 8000")
