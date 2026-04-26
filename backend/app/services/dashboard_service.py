from datetime import datetime

from sqlalchemy.orm import Session

from app.dashboard.weather_section import WeatherDashboardSection
from app.schemas.dashboard import DashboardRead


class DashboardService:
    def __init__(self, db: Session):
        self.weather_section = WeatherDashboardSection(db)

    def get_dashboard(
        self,
        start: datetime,
        end: datetime,
        location_key: str = "okaloosa_island",
    ) -> DashboardRead:
        return DashboardRead(
            generated_at=datetime.utcnow(),
            start=start,
            end=end,
            weather=self.weather_section.build(
                start=start,
                end=end,
                location_key=location_key,
            ),
        )