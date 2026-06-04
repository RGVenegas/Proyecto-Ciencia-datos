"""Entrenamiento modular y exportación de artefactos para despliegue."""
from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.config import (
    DATA_PROCESSED,
    FEATURE_IMPORTANCE_THRESHOLD,
    METADATA_PATH,
    MODEL_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    SCALER_PATH,
)
from src.preprocessing import (
    clean_dataset,
    encode_features,
    load_raw_dataset,
    quality_report,
    save_metadata,
    split_and_scale,
)


def build_models() -> dict:
    return {
        "Regresión Logística": LogisticRegression(random_state=RANDOM_STATE, max_iter=1000),
        "Árbol de Decisión": DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=5),
        "Random Forest": RandomForestClassifier(
            random_state=RANDOM_STATE, n_estimators=100, max_depth=5
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            random_state=RANDOM_STATE, n_estimators=100, max_depth=3
        ),
        "Support Vector Machine": SVC(random_state=RANDOM_STATE),
    }


def compare_models(x_train, x_test, y_train, y_test) -> tuple[dict, dict, dict]:
    models = build_models()
    holdout: dict = {}
    cv_scores: dict = {}
    timings: dict = {}
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    for name, model in models.items():
        start = time.perf_counter()
        model.fit(x_train, y_train)
        fit_seconds = time.perf_counter() - start

        start = time.perf_counter()
        y_pred = model.predict(x_test)
        predict_seconds = time.perf_counter() - start

        scores = cross_val_score(model, x_train, y_train, cv=skf, scoring="f1")
        holdout[name] = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
        }
        cv_scores[name] = {
            "f1_mean": float(np.mean(scores)),
            "f1_std": float(np.std(scores)),
            "fold_scores": [float(s) for s in scores],
        }
        timings[name] = {
            "fit_seconds": round(fit_seconds, 4),
            "predict_854_rows_seconds": round(predict_seconds, 4),
        }

    return holdout, cv_scores, timings


def reference_profile(cleaned) -> dict:
    """Valores de referencia para variables sin aporte predictivo en la UI."""
    return {
        "Sexo": str(cleaned["Sexo"].mode().iloc[0]),
        "Tipo_Empleo": str(cleaned["Tipo_Empleo"].mode().iloc[0]),
        "Ciudad_Chile": str(cleaned["Ciudad_Chile"].mode().iloc[0]),
        "Edad": int(cleaned["Edad"].median()),
        "Tiene_Vehiculo": int(cleaned["Tiene_Vehiculo"].median()),
        "Tiene_Tarjeta": int(cleaned["Tiene_Tarjeta"].median()),
        "Saldo_Tarjeta_CLP": float(cleaned["Saldo_Tarjeta_CLP"].median()),
        "Peor_Calificacion_36M": float(cleaned["Peor_Calificacion_36M"].median()),
        "Reportes_Central_36M": int(cleaned["Reportes_Central_36M"].median()),
        "Reportes_Central_12M": int(cleaned["Reportes_Central_12M"].median()),
        "Promedio_Saldo_CLP": float(cleaned["Promedio_Saldo_CLP"].median()),
        "Maximo_Saldo_CLP": float(cleaned["Maximo_Saldo_CLP"].median()),
    }


def predictive_variables(model, feature_names: list[str]) -> dict:
    ranking = sorted(
        zip(feature_names, model.feature_importances_),
        key=lambda item: item[1],
        reverse=True,
    )
    relevant = [
        {"feature": name, "importance": float(value)}
        for name, value in ranking
        if value >= FEATURE_IMPORTANCE_THRESHOLD
    ]
    excluded = [
        {"feature": name, "importance": float(value)}
        for name, value in ranking
        if value < FEATURE_IMPORTANCE_THRESHOLD
    ]
    return {
        "umbral_importancia": FEATURE_IMPORTANCE_THRESHOLD,
        "variables_relevantes": relevant,
        "variables_excluidas": excluded,
        "campos_formulario": [
            "Num_Entidades_Deuda",
            "Peor_Calificacion_12M",
            "Ingreso_CLP",
            "Saldo_Total_CLP",
            "Variacion_Endeudamiento",
        ],
        "nota_ratio": "Ratio_Saldo_Ingreso se calcula como Saldo_Total_CLP / Ingreso_CLP.",
    }


def feature_importance(model, feature_names: list[str]) -> list[dict]:
    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_") and model.coef_ is not None:
        values = np.abs(model.coef_.ravel())
    else:
        return []

    ranking = sorted(
        [{"feature": name, "importance": float(value)} for name, value in zip(feature_names, values)],
        key=lambda item: item["importance"],
        reverse=True,
    )
    return ranking[:10]


def train_and_export() -> dict:
    raw = load_raw_dataset()
    cleaned = clean_dataset(raw)
    features, target = encode_features(cleaned)
    split = split_and_scale(features, target)

    holdout, cv_scores, timings = compare_models(
        split["x_train"], split["x_test"], split["y_train"], split["y_test"]
    )

    winner = max(holdout, key=lambda name: holdout[name]["f1"])
    model = build_models()[winner]
    model.fit(split["x_train"], split["y_train"])
    y_pred = model.predict(split["x_test"])

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(split["scaler"], SCALER_PATH)

    processed = pd.concat([split["x_scaled"], target.reset_index(drop=True)], axis=1)
    processed.to_csv(DATA_PROCESSED, index=False)

    metadata = {
        "modelo_seleccionado": winner,
        "tipo_modelo": type(model).__name__,
        "feature_names": split["feature_names"],
        "metricas_test": holdout[winner],
        "classification_report": classification_report(
            split["y_test"], y_pred, output_dict=True
        ),
        "comparacion_holdout": holdout,
        "validacion_cruzada": cv_scores,
        "tiempos_entrenamiento": timings,
        "calidad_datos": quality_report(cleaned),
        "top_features": feature_importance(model, split["feature_names"]),
        "variables_predictivas": predictive_variables(model, split["feature_names"]),
        "valores_referencia": reference_profile(cleaned),
        "notas": {
            "data_leakage": "ScoreRiesgo excluido por derivarse del target.",
            "criterio_seleccion": "Mayor F1-Score en hold-out estratificado 80/20.",
        },
    }
    save_metadata(METADATA_PATH, metadata)
    return metadata


if __name__ == "__main__":
    result = train_and_export()
    print(f"Modelo exportado: {result['modelo_seleccionado']}")
    print(f"F1 test: {result['metricas_test']['f1']:.4f}")
