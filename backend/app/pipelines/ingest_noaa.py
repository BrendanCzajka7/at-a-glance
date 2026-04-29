from datetime import datetime, time, timedelta

from app.external.noaa_client import NoaaClient
from app.services.location_service import LocationService
from app.services.noaa_space_weather_service import NoaaSpaceWeatherService
from app.services.noaa_tide_service import NoaaTideService
from app.services.noaa_weather_alert_service import NoaaWeatherAlertService


class NoaaIngestPipeline:
    def __init__(self, db):
        self.client = NoaaClient()
        self.location_service = LocationService(db)
        self.tide_service = NoaaTideService(db)
        self.alert_service = NoaaWeatherAlertService(db)
        self.space_weather_service = NoaaSpaceWeatherService(db)

    async def run_for_location(self, location_key: str) -> dict:
        location = self.location_service.get_required(location_key)

        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        tomorrow_start = today_start + timedelta(days=1)

        result = {
            "location_key": location.key,
            "tide_rows": 0,
            "weather_alert_rows": 0,
            "space_weather_saved": False,
        }

        if location.noaa_tide_station_id:
            raw_tides = await self.client.fetch_tide_predictions(
                station_id=location.noaa_tide_station_id,
                start=today_start,
                end=tomorrow_start,
            )

            tide_rows = self.tide_service.save_from_raw_predictions(
                location_key=location.key,
                station_id=location.noaa_tide_station_id,
                raw_predictions=raw_tides,
            )

            result["tide_rows"] = len(tide_rows)

        raw_alerts = await self.client.fetch_active_weather_alerts(
            latitude=location.latitude,
            longitude=location.longitude,
        )

        alert_rows = self.alert_service.save_from_raw_alerts(
            location_key=location.key,
            raw_alerts=raw_alerts,
        )

        result["weather_alert_rows"] = len(alert_rows)

        return result

    async def run_for_all_active_locations(self) -> dict:
        locations = self.location_service.list_active()
        results = {}

        for location in locations:
            results[location.key] = await self.run_for_location(location.key)

        return results

    async def run_space_weather(self) -> dict:
        scales = await self.client.fetch_space_weather_scales()
        alerts = await self.client.fetch_space_weather_alerts()
        forecast_text = await self.client.fetch_three_day_space_weather_forecast()

        self.space_weather_service.save_report(
            scales=scales,
            alerts=alerts,
            forecast_text=forecast_text,
        )

        return {
            "space_weather_saved": True,
            "alert_count": len(alerts),
        }

    async def run_all(self) -> dict:
        location_results = await self.run_for_all_active_locations()
        space_weather_result = await self.run_space_weather()

        return {
            "locations": location_results,
            "space_weather": space_weather_result,
        }