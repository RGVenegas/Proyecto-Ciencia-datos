"""Pruebas básicas de la API local."""
from fastapi.testclient import TestClient

from src.api.main import app

cliente_completo = {
    "Sexo": "F",
    "Tipo_Empleo": "IND",
    "Tiene_Vehiculo": 0,
    "Edad": 44,
    "Ciudad_Chile": "SANTIAGO",
    "Num_Entidades_Deuda": 4,
    "Tiene_Tarjeta": 1,
    "Saldo_Tarjeta_CLP": 2036506.5,
    "Saldo_Total_CLP": 11000844.5,
    "Variacion_Endeudamiento": 0.21,
    "Peor_Calificacion_36M": 0,
    "Peor_Calificacion_12M": 0,
    "Reportes_Central_36M": 36,
    "Reportes_Central_12M": 12,
    "Promedio_Saldo_CLP": 6807461.3,
    "Maximo_Saldo_CLP": 9098774,
    "Ingreso_CLP": 4250000,
    "Ratio_Saldo_Ingreso": 2.5884,
}

cliente_predictivo = {
    "Num_Entidades_Deuda": 4,
    "Peor_Calificacion_12M": 0,
    "Ingreso_CLP": 4250000,
    "Saldo_Total_CLP": 11000844.5,
    "Variacion_Endeudamiento": 0.21,
}


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_predict_endpoint():
    client = TestClient(app)
    response = client.post("/predict", json=cliente_predictivo)
    assert response.status_code == 200
    body = response.json()
    assert body["riesgo_alto"] in (0, 1)
    assert body["variables_evaluadas"]["Ratio_Saldo_Ingreso"] > 0


def test_model_variables_endpoint():
    client = TestClient(app)
    response = client.get("/model/variables")
    assert response.status_code == 200
    body = response.json()
    assert "introduccion" in body
    assert len(body["campos_formulario"]) == 5


def test_predict_completo_endpoint():
    client = TestClient(app)
    response = client.post("/predict/completo", json=cliente_completo)
    assert response.status_code == 200
