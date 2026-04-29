# backend/app/routers/health.py

import os

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
def basic_health():
    return {"status": "ok"}


@router.get("/full")
def full_health(db: Session = Depends(get_db)):
    checks = {}

    try:
        db.execute(text("SELECT 1"))
        checks["database"] = {"status": "ok"}
    except Exception as exc:
        checks["database"] = {"status": "error", "message": str(exc)}

    checks["tmdb_config"] = {
        "status": "ok"
        if os.getenv("TMDB_API_KEY") or os.getenv("TMDB_BEARER_TOKEN")
        else "error",
        "message": "configured"
        if os.getenv("TMDB_API_KEY") or os.getenv("TMDB_BEARER_TOKEN")
        else "missing TMDB_API_KEY or TMDB_BEARER_TOKEN",
    }

    checks["musicbrainz_config"] = {
        "status": "ok",
        "message": "no API key required",
    }

    overall = "ok" if all(item["status"] == "ok" for item in checks.values()) else "error"

    return {
        "status": overall,
        "checks": checks,
    }