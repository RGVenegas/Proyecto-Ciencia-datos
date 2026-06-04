# Predicción de Riesgo Crediticio mediante Machine Learning

Sistema de alerta temprana para evaluar riesgo crediticio en clientes del sector financiero chileno. Incluye pipeline modular de datos, entrenamiento comparativo de modelos y **despliegue local** mediante API FastAPI + interfaz web.

## Características

- Metodología CRISP-DM con fase de despliegue en localhost.
- Preprocesamiento reproducible fuera del notebook (`src/preprocessing.py`).
- Comparación de 5 algoritmos con métricas, validación cruzada y tiempos de entrenamiento.
- API REST funcional con validación de entrada, manejo de errores e interpretabilidad básica.
- Front-end integrado para evaluar clientes desde el navegador.

## Estructura del repositorio

```text
data/raw/                 Dataset original
data/processed/           Dataset procesado exportado
models/                   modelo_final.pkl, scaler.pkl, metadata.json
notebooks/Notebook.ipynb  Análisis exploratorio y experimentación
src/
  preprocessing.py        Limpieza, codificación y escalado
  entrenar_modelo.py      Entrenamiento y exportación de artefactos
  artifacts.py            Carga centralizada del modelo
  api/main.py             API FastAPI
frontend/                 Interfaz web
tests/test_api.py         Pruebas de endpoints
docs/ARQUITECTURA_DESPLIEGUE.md
```

## Requisitos

- Python 3.10+
- Dependencias mínimas:

```bash
pip install -r requirements.txt
```

## Ejecución reproducible (Tarea 2)

### 1. Entrenar y exportar artefactos

Desde la raíz del proyecto:

```bash
python -m src.entrenar_modelo
```

Genera:

- `models/modelo_final.pkl`
- `models/scaler.pkl`
- `models/metadata.json`
- `data/processed/dataset_crediticio_procesado.csv`

### 2. Levantar la API en localhost

```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Usar el sistema

| Recurso | URL |
|---------|-----|
| Interfaz web | http://127.0.0.1:8000/ |
| Swagger / OpenAPI | http://127.0.0.1:8000/docs |
| Health check | http://127.0.0.1:8000/health |
| Info del modelo | http://127.0.0.1:8000/model/info |
| Predicción | `POST http://127.0.0.1:8000/predict` |

### 4. Probar endpoints por terminal

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/model/info
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @docs/ejemplo_cliente.json
python src/probar_modelo.py
python -m pytest tests/test_api.py -q
```

## Endpoints principales

### `GET /health`

Verifica que la API y los artefactos estén disponibles.

### `GET /model/info`

Devuelve métricas de test, validación cruzada por fold, tiempos computacionales, reporte de calidad de datos y top variables.

### `POST /predict`

Recibe un perfil de cliente en JSON y responde con:

- clasificación binaria (`riesgo_alto`)
- probabilidad estimada
- latencia en milisegundos
- variables más influyentes del modelo exportado

## Mejoras incorporadas desde la Sumativa 1

Según retroalimentación del profesor:

1. **Calidad de datos ampliada**: outliers por IQR, balance de clases y nulos en `metadata.json`.
2. **Comparación técnica más profunda**: tiempos de entrenamiento/predicción y scores por fold en CV.
3. **Interpretabilidad concreta**: top features expuestas en API y front-end.
4. **Arquitectura menos dependiente del notebook**: módulos Python reutilizables para entrenamiento y despliegue.
5. **Documentación de ejecución** detallada para reproducibilidad completa.

## Integrantes

- Rodrigo Venegas
- Diego Carmona
- Vicente Bustamante
