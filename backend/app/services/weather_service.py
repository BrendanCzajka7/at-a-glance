from datetime import datetime

from sqlalchemy.orm import Session

from app.models.weather_snapshot import WeatherSnapshot
from app.repositories.weather_repository import WeatherRepository


class WeatherService:
    def __init__(self, db: Session):
        self.repo = WeatherRepository(db)

    def save_current_weather(
        self,
        raw: dict,
        location_name: str,
        latitude: float,
        longitude: float,
    ) -> WeatherSnapshot:
        current = raw["current_weather"]

        snapshot = WeatherSnapshot(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            temperature_f=current["temperature"],
            wind_speed_mph=current.get("windspeed"),
            weather_code=current.get("weathercode"),
            observed_at=datetime.fromisoformat(current["time"]),
        )

        return self.repo.create_snapshot(snapshot)

    def get_latest_weather(self, limit: int = 20) -> list[WeatherSnapshot]:
        return self.repo.list_latest(limit=limit)