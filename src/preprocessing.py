"""Pipeline reproducible de limpieza, codificación y escalado."""
from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import (
    CATEGORICAL_COLUMNS,
    DATA_RAW,
    LEAKAGE_COLUMNS,
    RANDOM_STATE,
    TARGET_COLUMN,
)


def load_raw_dataset(path=DATA_RAW) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Imputación contextual alineada con el notebook y el informe."""
    data = df.copy()
    data = data.drop(columns=[c for c in LEAKAGE_COLUMNS if c in data.columns], errors="ignore")

    # Recalcular escala del Ratio Saldo/Ingreso a nivel mensual
    if "Saldo_Total_CLP" in data.columns and "Ingreso_CLP" in data.columns:
        data["Ratio_Saldo_Ingreso"] = data["Saldo_Total_CLP"] / data["Ingreso_CLP"]

    for col in ("Peor_Calificacion_36M", "Peor_Calificacion_12M"):
        if col in data.columns:
            data[col] = data[col].fillna(-1)

    if "Tipo_Empleo" in data.columns:
        data["Tipo_Empleo"] = data["Tipo_Empleo"].fillna("DESCONOCIDO")

    for col in data.select_dtypes(include=[np.number]).columns:
        data[col] = data[col].fillna(data[col].median())

    for col in data.select_dtypes(exclude=[np.number]).columns:
        if col != TARGET_COLUMN:
            data[col] = data[col].fillna(data[col].mode()[0])

    return data


def encode_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    encoded = pd.get_dummies(df, columns=CATEGORICAL_COLUMNS, drop_first=True)
    features = encoded.drop(columns=[TARGET_COLUMN], errors="ignore")
    target = encoded[TARGET_COLUMN]
    return features, target


def split_and_scale(
    features: pd.DataFrame,
    target: pd.Series,
    test_size: float = 0.2,
) -> dict[str, Any]:
    x_train_raw, x_test_raw, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    scaler = StandardScaler()
    scaler.fit(x_train_raw)

    x_train = pd.DataFrame(scaler.transform(x_train_raw), columns=features.columns)
    x_test = pd.DataFrame(scaler.transform(x_test_raw), columns=features.columns)
    x_scaled = pd.DataFrame(scaler.transform(features), columns=features.columns)

    return {
        "x_train": x_train,
        "x_test": x_test,
        "y_train": y_train,
        "y_test": y_test,
        "x_scaled": x_scaled,
        "feature_names": list(features.columns),
        "scaler": scaler,
    }


def transform_single_record(record: dict[str, Any], feature_names: list[str], scaler: StandardScaler) -> pd.DataFrame:
    """Convierte un registro crudo en vector escalado alineado al entrenamiento."""
    frame = pd.DataFrame([record])
    frame = clean_dataset(frame)
    encoded, _ = encode_features(
        pd.concat([frame, pd.DataFrame({TARGET_COLUMN: [0]})], axis=1)
    )

    aligned = pd.DataFrame(columns=feature_names, index=[0]).fillna(0.0)
    for column in encoded.columns:
        if column in aligned.columns:
            aligned[column] = encoded[column].values

    return pd.DataFrame(scaler.transform(aligned), columns=feature_names)


def quality_report(df: pd.DataFrame) -> dict[str, Any]:
    """Métricas de calidad solicitadas en la retroalimentación de la Sumativa 1."""
    numeric = df.select_dtypes(include=[np.number])
    report: dict[str, Any] = {
        "registros": int(len(df)),
        "columnas": int(df.shape[1]),
        "nulos_por_columna": df.isna().sum().to_dict(),
        "balance_clases": df[TARGET_COLUMN].value_counts(normalize=True).round(4).to_dict()
        if TARGET_COLUMN in df.columns
        else {},
    }

    if not numeric.empty:
        q1 = numeric.quantile(0.25)
        q3 = numeric.quantile(0.75)
        iqr = q3 - q1
        outlier_mask = ((numeric < (q1 - 1.5 * iqr)) | (numeric > (q3 + 1.5 * iqr))).sum()
        report["outliers_iqr_por_columna"] = outlier_mask.to_dict()
        report["outliers_iqr_total"] = int(outlier_mask.sum())

    return report


def save_metadata(path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
