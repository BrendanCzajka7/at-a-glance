# backend/app/main.py

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.models
from app.core.db import Base, engine
from app.routers import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="At A Glance API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(api_router)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    mount_frontend(app)

    return app


def mount_frontend(app: FastAPI) -> None:
    base_dir = Path(__file__).resolve().parents[2]
    frontend_dist = base_dir / "frontend" / "dist"

    if not frontend_dist.exists():
        return

    app.mount(
        "/assets",
        StaticFiles(directory=frontend_dist / "assets"),
        name="assets",
    )

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(frontend_dist / "index.html")


app = create_app()