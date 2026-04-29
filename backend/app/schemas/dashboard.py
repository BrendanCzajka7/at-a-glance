# backend/app/schemas/dashboard.py

from datetime import datetime

from pydantic import BaseModel

from app.schemas.nasa_dashboard import NasaSection
from app.schemas.weather_dashboard import WeatherSection
from app.schemas.music_dashboard import MusicSection


class DashboardRead(BaseModel):
    generated_at: datetime
    start: datetime
    end: datetime
    weather: WeatherSection
    nasa: NasaSection
    music: MusicSection