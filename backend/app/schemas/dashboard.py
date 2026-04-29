from datetime import datetime

from pydantic import BaseModel

from app.schemas.nasa_dashboard import NasaSection
from app.schemas.weather_dashboard import WeatherSection


class DashboardRead(BaseModel):
    generated_at: datetime
    start: datetime
    end: datetime
    weather: WeatherSection
    nasa: NasaSection