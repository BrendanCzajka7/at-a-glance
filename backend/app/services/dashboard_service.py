from datetime import datetime

from sqlalchemy.orm import Session

from app.core.time import now_for_timezone
from app.dashboard.weather_section import WeatherDashboardSection
from app.schemas.dashboard import DashboardRead
from app.services.location_service import LocationService
from app.dashboard.nasa_section import NasaDashboardSection


class DashboardService:
    def __init__(self, db: Session):
        self.location_service = LocationService(db)
        self.weather_section = WeatherDashboardSection(db)
        self.nasa_section = NasaDashboardSection(db)

    def get_dashboard(
        self,
        start: datetime,
        end: datetime,
        location_key: str,
    ) -> DashboardRead:
        location = self.location_service.get_required(location_key)

        return DashboardRead(
            generated_at=now_for_timezone(location.timezone),
            start=start,
            end=end,
            weather=self.weather_section.build(
                start=start,
                end=end,
                location_key=location.key,
            ),
            nasa=self.nasa_section.build(start=start),
        )