"""Rutas centralizadas del proyecto."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"
DATA_PROCESSED = ROOT / "data" / "processed" / "dataset_crediticio_procesado.csv"
MODELS_DIR = ROOT / "models"
MODEL_PATH = MODELS_DIR / "modelo_final.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
METADATA_PATH = MODELS_DIR / "metadata.json"
FRONTEND_DIR = ROOT / "frontend"

# Variables con importancia >= umbral se solicitan al usuario; el resto usa valores de referencia.
FEATURE_IMPORTANCE_THRESHOLD = 0.001

CATEGORICAL_COLUMNS = ["Sexo", "Tipo_Empleo", "Ciudad_Chile"]
TARGET_COLUMN = "RiesgoAlto"
LEAKAGE_COLUMNS = ["No.", "ScoreRiesgo"]
RANDOM_STATE = 42
