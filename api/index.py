"""Punto de entrada serverless para Vercel (FastAPI + Mangum)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mangum import Mangum  # noqa: E402

from src.api.main import app as fastapi_app  # noqa: E402

# Vercel invoca esta app ASGI; Mangum adapta el handler serverless.
app = fastapi_app
handler = Mangum(fastapi_app, lifespan="off")
