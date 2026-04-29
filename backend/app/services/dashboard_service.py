# backend/app/services/dashboard_service.py

from datetime import datetime

from app.core.time import now_for_timezone
from app.dashboard.weather_section import WeatherDashboardSection
from app.dashboard.nasa_section import NasaDashboardSection
from app.dashboard.music_section import MusicDashboardSection
from app.schemas.dashboard import DashboardRead
from app.services.location_service import LocationService
from app.dashboard.tmdb_section import TmdbDashboardSection
from app.dashboard.ticketmaster_section import TicketmasterDashboardSection
from app.dashboard.space_section import SpaceDashboardSection

class DashboardService:
    def __init__(self, db):
        self.location_service = LocationService(db)
        self.weather_section = WeatherDashboardSection(db)
        self.nasa_section = NasaDashboardSection(db)
        self.music_section = MusicDashboardSection(db)
        self.tmdb_section = TmdbDashboardSection(db)
        self.ticketmaster_section = TicketmasterDashboardSection(db)
        self.space_section = SpaceDashboardSection(db)

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
            music=self.music_section.build(start=start),
            tmdb=self.tmdb_section.build(start=start),
            ticketmaster=self.ticketmaster_section.build(
                start=start,
                location_key=location.key,
            ),
            space=self.space_section.build(start=start),
        )