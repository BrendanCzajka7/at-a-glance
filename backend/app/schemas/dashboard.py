from datetime import datetime

from pydantic import BaseModel

from app.schemas.music_dashboard import MusicSection
from app.schemas.nasa_dashboard import NasaSection
from app.schemas.tmdb_dashboard import TmdbSection
from app.schemas.weather_dashboard import WeatherSection


class DashboardRead(BaseModel):
    generated_at: datetime
    start: datetime
    end: datetime
    weather: WeatherSection
    nasa: NasaSection
    music: MusicSection
    tmdb: TmdbSection