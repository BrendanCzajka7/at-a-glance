from datetime import datetime, time, timedelta

from sqlalchemy.orm import Session

from app.schemas.nasa_dashboard import (
    NasaApodCard,
    NasaSection,
    NasaSpaceWeatherCard,
    NasaSpaceWeatherSection,
)
from app.services.nasa_apod_service import NasaApodService
from app.services.nasa_space_weather_service import NasaSpaceWeatherService


class NasaDashboardSection:
    def __init__(self, db: Session):
        self.apod_service = NasaApodService(db)
        self.space_weather_service = NasaSpaceWeatherService(db)

    def build(self, start: datetime) -> NasaSection:
        apod = self.apod_service.get_latest()

        today_start = datetime.combine(start.date(), time.min)
        tomorrow_start = today_start + timedelta(days=1)

        week_start = today_start
        week_end = today_start + timedelta(days=7)

        today_notifications = self.space_weather_service.list_between(
            start=today_start,
            end=tomorrow_start,
            limit=5,
        )

        week_notifications = self.space_weather_service.list_between(
            start=week_start,
            end=week_end,
            limit=10,
        )

        return NasaSection(
            apod=NasaApodCard.model_validate(apod) if apod else None,
            space_weather=NasaSpaceWeatherSection(
                today=[
                    NasaSpaceWeatherCard.model_validate(item)
                    for item in today_notifications
                ],
                week=[
                    NasaSpaceWeatherCard.model_validate(item)
                    for item in week_notifications
                ],
            ),
        )