from sqlalchemy.orm import Session

from app.external.open_meteo_client import OpenMeteoClient
from app.models.weather_forecast import WeatherForecast
from app.services.location_service import LocationService
from app.services.weather_forecast_service import WeatherForecastService

from app.core.time import now_for_timezone

class WeatherForecastIngestPipeline:
    def __init__(self, db: Session):
        self.client = OpenMeteoClient()
        self.location_service = LocationService(db)
        self.weather_service = WeatherForecastService(db)

    async def run_for_location(self, location_key: str) -> list[WeatherForecast]:
        location = self.location_service.get_required(location_key)

        raw = await self.client.fetch_forecast(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone,
        )

        return self.weather_service.save_forecast_response(
            raw=raw,
            location_key=location.key,
            location_name=location.name,
        )
    
    async def run_for_all_active_locations(self) -> dict:
        locations = self.location_service.list_active()

        results = {}

        for location in locations:
            rows = await self.run_for_location(location.key)

            cleanup_before = now_for_timezone(location.timezone) - timedelta(days=2)
            deleted_old = self.weather_service.delete_old_forecasts(
                before=cleanup_before,
            )

            results[location.key] = {
                "saved_rows": len(rows),
                "deleted_old_rows": deleted_old,
            }

        return results