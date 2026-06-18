"""Punto de entrada serverless para Vercel (@vercel/python + FastAPI ASGI)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api.main import app  # noqa: E402
