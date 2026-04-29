from datetime import datetime

from pydantic import BaseModel

from app.schemas.music_dashboard import MusicSection
from app.schemas.nasa_dashboard import NasaSection
from app.schemas.tmdb_dashboard import TmdbSection
from app.schemas.weather_dashboard import WeatherSection
from app.schemas.ticketmaster_dashboard import TicketmasterSection
from app.schemas.space_dashboard import SpaceSection
from app.schemas.usgs_dashboard import UsgsSection
from app.schemas.noaa_dashboard import NoaaSection
from app.schemas.ocean_dashboard import OceanSection
from app.schemas.nature_dashboard import NatureSection

class DashboardRead(BaseModel):
    generated_at: datetime
    start: datetime
    end: datetime
    weather: WeatherSection
    nasa: NasaSection
    music: MusicSection
    tmdb: TmdbSection
    ticketmaster: TicketmasterSection
    space: SpaceSection
    usgs: UsgsSection
    noaa: NoaaSection
    ocean: OceanSection
    nature: NatureSection