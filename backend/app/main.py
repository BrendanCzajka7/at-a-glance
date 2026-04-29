from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.db import Base, engine
from app.models.weather_forecast import WeatherForecast
from app.models.nasa_apod import NasaApod
from app.models.nasa_space_weather_notification import NasaSpaceWeatherNotification
from app.routers.nasa import router as nasa_router
from app.routers.nasa_space_weather import router as nasa_space_weather_router
from app.routers.dashboard import router as dashboard_router
from app.routers.jobs import router as jobs_router
from app.routers.weather_forecast import router as weather_forecast_router
from app.models.location import Location
from app.routers.locations import router as locations_router
from app.models.nasa_neo import NasaNeoCloseApproach
from app.models.nasa_epic import NasaEpicImage
from app.routers.nasa_epic import router as nasa_epic_router
from app.routers.nasa_neos import router as nasa_neos_router

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

app.include_router(weather_forecast_router)
app.include_router(jobs_router)
app.include_router(dashboard_router)
app.include_router(locations_router)
app.include_router(nasa_router)
app.include_router(nasa_space_weather_router)
app.include_router(nasa_epic_router)
app.include_router(nasa_neos_router)

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