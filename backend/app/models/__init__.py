# backend/app/models/__init__.py

from app.models.location import Location
from app.models.weather_forecast import WeatherForecast
from app.models.nasa_apod import NasaApod
from app.models.nasa_space_weather_notification import NasaSpaceWeatherNotification
from app.models.nasa_neo import NasaNeoCloseApproach
from app.models.nasa_epic import NasaEpicImage
from app.models.music_artist import MusicArtist
from app.models.music_release import MusicRelease
from app.models.tmdb_watch_item import TmdbWatchItem
from app.models.tmdb_movie_release import TmdbMovieRelease
from app.models.app_event import AppEvent
from app.models.ticketmaster_concert import TicketmasterConcert
from app.models.space_launch import SpaceLaunch
from app.models.usgs_earthquake import UsgsEarthquake
from app.models.noaa_tide_prediction import NoaaTidePrediction
from app.models.noaa_weather_alert import NoaaWeatherAlert
from app.models.noaa_space_weather_report import NoaaSpaceWeatherReport
from app.models.ocean_conditions import OceanConditions
from app.models.nature_photo import NaturePhoto

__all__ = [
    "Location",
    "WeatherForecast",
    "NasaApod",
    "NasaSpaceWeatherNotification",
    "NasaNeoCloseApproach",
    "NasaEpicImage",
    "MusicArtist",
    "MusicRelease",
    "TmdbWatchItem",
    "TmdbMovieRelease",
    "AppEvent",
    "TicketmasterConcert",
    "SpaceLaunch",
    "UsgsEarthquake",
]