"""Carga centralizada de artefactos del modelo."""
from __future__ import annotations

import json
from functools import lru_cache

import joblib

from src.config import METADATA_PATH, MODEL_PATH, SCALER_PATH


class ArtifactError(RuntimeError):
    """Error al cargar artefactos de ML."""


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise ArtifactError(
            f"No se encontró {MODEL_PATH}. Ejecute: python -m src.entrenar_modelo"
        )
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_scaler():
    if not SCALER_PATH.exists():
        raise ArtifactError(
            f"No se encontró {SCALER_PATH}. Ejecute: python -m src.entrenar_modelo"
        )
    return joblib.load(SCALER_PATH)


@lru_cache(maxsize=1)
def load_metadata() -> dict:
    if not METADATA_PATH.exists():
        raise ArtifactError(
            f"No se encontró {METADATA_PATH}. Ejecute: python -m src.entrenar_modelo"
        )
    with open(METADATA_PATH, encoding="utf-8") as handle:
        return json.load(handle)
