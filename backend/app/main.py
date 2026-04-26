from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.db import Base, engine
from app.models.weather_snapshot import WeatherSnapshot
from app.routers.jobs import router as jobs_router
from app.routers.weather import router as weather_router

app = FastAPI(title="Weather Baseplate API")

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

app.include_router(weather_router)
app.include_router(jobs_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="assets",
    )

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(FRONTEND_DIST / "index.html")