# backend/app/routers/__init__.py

from fastapi import APIRouter

from app.routers.dashboard import router as dashboard_router
from app.routers.jobs import router as jobs_router
from app.routers.locations import router as locations_router
from app.routers.nasa import router as nasa_router
from app.routers.nasa_epic import router as nasa_epic_router
from app.routers.nasa_neos import router as nasa_neos_router
from app.routers.nasa_space_weather import router as nasa_space_weather_router
from app.routers.weather_forecast import router as weather_forecast_router
from app.routers.music import router as music_router
from app.routers.tmdb import router as tmdb_router
from app.routers.app_events import router as app_events_router
from app.routers.health import router as health_router

api_router = APIRouter()

api_router.include_router(weather_forecast_router)
api_router.include_router(jobs_router)
api_router.include_router(dashboard_router)
api_router.include_router(locations_router)
api_router.include_router(nasa_router)
api_router.include_router(nasa_space_weather_router)
api_router.include_router(nasa_epic_router)
api_router.include_router(nasa_neos_router)
api_router.include_router(music_router)
api_router.include_router(tmdb_router)
api_router.include_router(app_events_router)
api_router.include_router(health_router)