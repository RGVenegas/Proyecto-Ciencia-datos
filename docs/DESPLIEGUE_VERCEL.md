# Despliegue en Vercel

Guía para publicar **CreditVision** (FastAPI + front-end + modelo ML) en Vercel.

## Archivos añadidos al repositorio

| Archivo | Función |
|---------|---------|
| `api/index.py` | Entrada serverless (FastAPI ASGI) |
| `vercel.json` | Build `@vercel/python` y rutas |
| `.vercelignore` | Excluye notebooks, datos crudos y tests del bundle |
| `runtime.txt` | Python 3.11 |
| `requirements.txt` | Incluye `mangum` |

## Qué debes hacer tú

### 1. Subir los cambios a GitHub

Desde la raíz del proyecto:

```bash
git add api/ vercel.json .vercelignore runtime.txt requirements.txt docs/DESPLIEGUE_VERCEL.md README.md
git commit -m "Configurar despliegue en Vercel con Mangum y FastAPI"
git push origin main
```

(Ajusta el mensaje de commit si quieres.)

### 2. Crear cuenta y conectar el repo

1. Entra a [https://vercel.com](https://vercel.com) e inicia sesión (con GitHub).
2. **Add New… → Project**.
3. Importa el repositorio `Proyecto-Ciencia-datos`.
4. **Framework Preset:** Other (no Next.js).
5. **Root Directory:** `.` (raíz).
6. **Build Command:** déjalo vacío (no hace falta build).
7. **Output Directory:** déjalo vacío.
8. Clic en **Deploy**.

Vercel instalará `requirements.txt` y expondrá la función `api/index.py`.

### 3. Verificar el despliegue

Sustituye `TU-URL` por la que te asigne Vercel (ej. `proyecto-ciencia-datos.vercel.app`):

| Recurso | URL |
|---------|-----|
| Interfaz | `https://TU-URL/` |
| Resultado | `https://TU-URL/resultado` |
| Health | `https://TU-URL/health` |
| Swagger | `https://TU-URL/docs` |
| Predicción | `POST https://TU-URL/predict` |

Prueba rápida en terminal:

```bash
curl https://TU-URL/health
```

Respuesta esperada: `{"status":"ok","modelo_cargado":true,...}`

### 4. Probar una predicción (JSON)

```bash
curl -X POST https://TU-URL/predict \
  -H "Content-Type: application/json" \
  -d "{\"Num_Entidades_Deuda\":1,\"Peor_Calificacion_12M\":0,\"Ingreso_CLP\":2500000,\"Saldo_Total_CLP\":250000,\"Variacion_Endeudamiento\":0}"
```

### 5. Capturas para el informe

- Pantalla principal con formulario.
- Página `/resultado` con dictamen.
- `/docs` (Swagger).
- Respuesta de `/health`.

## Notas importantes

- **Primera petición lenta:** el cold start de Python + scikit-learn puede tardar 5–15 s.
- **Límite Hobby:** `maxDuration` 10 s por petición (suficiente para una predicción).
- **Modelo en repo:** deben estar en GitHub `models/modelo_final.pkl`, `scaler.pkl`, `metadata.json`.
- **Localhost sigue válido** para la Tarea 2; Vercel es despliegue público adicional.

## Probar en local (opcional, simula Vercel)

```bash
pip install mangum
python -c "from api.index import app; print('OK', app.title)"
```

Seguir usando uvicorn para desarrollo diario:

```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

## Si el deploy falla

| Error | Solución |
|-------|----------|
| `functions doesn't match any Serverless Functions` | Usar `vercel.json` con `builds` + `@vercel/python` (ya incluido) |
| Build timeout | Revisa que `.vercelignore` excluya `data/` y `notebooks/` |
| 500 en `/health` | Confirma que `models/` está en GitHub |
| Module not found `src` | Verifica que `api/index.py` esté en la raíz del repo |
| Function too large | No subas CSV procesados; solo `models/` + código |

## Redesplegar

Cada `git push` a `main` redeploya automáticamente si el proyecto está conectado en Vercel.
