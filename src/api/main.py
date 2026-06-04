"""API local de predicción de riesgo crediticio (FastAPI)."""
from __future__ import annotations

import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.schemas import (
    ClienteInput,
    ErrorResponse,
    EvaluacionCrediticiaInput,
    HealthResponse,
    PredictionResponse,
)
from src.artifacts import ArtifactError, load_metadata, load_model, load_scaler
from src.config import FRONTEND_DIR
from src.preprocessing import transform_single_record
from src.variables_negocio import INTRO_SISTEMA, VARIABLES_EXCLUIDAS_UI, VARIABLES_NEGOCIO

app = FastAPI(
    title="API Riesgo Crediticio",
    description="Servicio local para evaluar riesgo crediticio con el modelo exportado.",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


def _clasificar_riesgo(probability: float, prediction: int) -> tuple[str, str]:
    pct = probability * 100
    if prediction == 0 and pct < 35:
        return "Bajo", "Aprobación recomendada. Perfil dentro de parámetros aceptables."
    if prediction == 0 or pct < 55:
        return "Moderado", "Revisión manual sugerida. Validar antecedentes comerciales adicionales."
    return "Alto", "Riesgo elevado. Considerar rechazo, reducir monto o exigir garantías."


def _run_prediction(
    cliente: ClienteInput,
    variables_evaluadas: dict | None = None,
) -> PredictionResponse:
    started = time.perf_counter()
    metadata = load_metadata()
    model = load_model()
    scaler = load_scaler()
    feature_names = metadata["feature_names"]

    vector = transform_single_record(cliente.model_dump(), feature_names, scaler)
    probability = float(model.predict_proba(vector)[0][1])
    prediction = int(model.predict(vector)[0])
    nivel, recomendacion = _clasificar_riesgo(probability, prediction)

    relevantes = metadata.get("variables_predictivas", {}).get("variables_relevantes", [])
    top = relevantes[:5] if relevantes else metadata.get("top_features", [])[:5]

    return PredictionResponse(
        riesgo_alto=prediction,
        probabilidad_riesgo_alto=round(probability, 4),
        etiqueta="Riesgo Alto" if prediction == 1 else "Riesgo Bajo",
        recomendacion=recomendacion,
        nivel_riesgo=nivel,
        modelo=metadata.get("modelo_seleccionado", "desconocido"),
        latencia_ms=round((time.perf_counter() - started) * 1000, 2),
        variables_clave=top,
        variables_evaluadas=variables_evaluadas,
    )


@app.get("/", include_in_schema=False)
def serve_frontend():
    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Front-end no encontrado.")
    return FileResponse(index)


@app.get("/resultado", include_in_schema=False)
def serve_resultado():
    page = FRONTEND_DIR / "resultado.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Página de resultado no encontrada.")
    return FileResponse(page)


@app.get("/health", response_model=HealthResponse, tags=["Sistema"])
def health_check():
    try:
        metadata = load_metadata()
        load_model()
        return HealthResponse(
            status="ok",
            modelo_cargado=True,
            modelo=metadata.get("modelo_seleccionado"),
        )
    except ArtifactError as exc:
        return HealthResponse(status="missing_artifacts", modelo_cargado=False, modelo=str(exc))


@app.get("/model/variables", tags=["Modelo"])
def model_variables():
    try:
        metadata = load_metadata()
        predictivas = metadata.get("variables_predictivas", {})
        return {
            "introduccion": INTRO_SISTEMA,
            "variables_negocio": VARIABLES_NEGOCIO,
            "variables_relevantes": predictivas.get("variables_relevantes", []),
            "variables_excluidas_ui": VARIABLES_EXCLUIDAS_UI,
            "campos_formulario": predictivas.get("campos_formulario", []),
            "nota_ratio": predictivas.get("nota_ratio"),
            "valores_referencia": metadata.get("valores_referencia", {}),
        }
    except ArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/model/info", tags=["Modelo"])
def model_info():
    try:
        metadata = load_metadata()
        model = load_model()
        return {
            "modelo": metadata.get("modelo_seleccionado"),
            "tipo": type(model).__name__,
            "metricas_test": metadata.get("metricas_test"),
            "variables_predictivas": metadata.get("variables_predictivas"),
            "comparacion_holdout": metadata.get("comparacion_holdout"),
            "validacion_cruzada": metadata.get("validacion_cruzada"),
            "top_features": metadata.get("top_features"),
        }
    except ArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post(
    "/predict",
    response_model=PredictionResponse,
    responses={422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    tags=["Predicción"],
)
def predict(cliente: EvaluacionCrediticiaInput):
    """Evalúa riesgo usando solo las variables con aporte predictivo real."""
    try:
        metadata = load_metadata()
        referencia = metadata.get("valores_referencia", {})
        completo = cliente.to_cliente_completo(referencia)
        return _run_prediction(completo, variables_evaluadas=cliente.variables_utilizadas())
    except ArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error interno de predicción: {exc}") from exc


@app.post(
    "/predict/completo",
    response_model=PredictionResponse,
    responses={422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    tags=["Predicción"],
)
def predict_completo(cliente: ClienteInput):
    """Perfil completo para integraciones técnicas."""
    try:
        return _run_prediction(cliente, variables_evaluadas=cliente.model_dump())
    except ArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error interno de predicción: {exc}") from exc


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(elapsed_ms)
    return response
