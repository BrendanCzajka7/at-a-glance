from datetime import datetime

from sqlalchemy.orm import Session

from app.models.weather_forecast import WeatherForecast


class WeatherForecastRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_many(self, forecasts: list[WeatherForecast]) -> list[WeatherForecast]:
        saved: list[WeatherForecast] = []

        for forecast in forecasts:
            existing = (
                self.db.query(WeatherForecast)
                .filter(
                    WeatherForecast.source == forecast.source,
                    WeatherForecast.location_key == forecast.location_key,
                    WeatherForecast.forecast_for == forecast.forecast_for,
                    WeatherForecast.granularity == forecast.granularity,
                )
                .first()
            )

            if existing:
                existing.location_name = forecast.location_name
                existing.temperature_f = forecast.temperature_f
                existing.temperature_max_f = forecast.temperature_max_f
                existing.temperature_min_f = forecast.temperature_min_f
                existing.apparent_temperature_f = forecast.apparent_temperature_f
                existing.precipitation_probability = forecast.precipitation_probability
                existing.precipitation_inches = forecast.precipitation_inches
                existing.wind_speed_mph = forecast.wind_speed_mph
                existing.wind_gust_mph = forecast.wind_gust_mph
                existing.uv_index = forecast.uv_index
                existing.weather_code = forecast.weather_code
                existing.sunrise = forecast.sunrise
                existing.sunset = forecast.sunset
                existing.fetched_at = datetime.utcnow()

                saved.append(existing)
            else:
                self.db.add(forecast)
                saved.append(forecast)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        start: datetime,
        end: datetime,
        location_key: str = "okaloosa_island",
    ) -> list[WeatherForecast]:
        return (
            self.db.query(WeatherForecast)
            .filter(
                WeatherForecast.location_key == location_key,
                WeatherForecast.forecast_for >= start,
                WeatherForecast.forecast_for < end,
            )
            .order_by(
                WeatherForecast.forecast_for.asc(),
                WeatherForecast.granularity.asc(),
            )
            .all()
        )
    
    def get_latest_current(
        self,
        location_key: str,
    ) -> WeatherForecast | None:
        return (
            self.db.query(WeatherForecast)
            .filter(
                WeatherForecast.location_key == location_key,
                WeatherForecast.granularity == "current",
            )
            .order_by(WeatherForecast.forecast_for.desc())
            .first()
        )

    def delete_old_forecasts(
        self,
        before: datetime,
    ) -> int:
        deleted_count = (
            self.db.query(WeatherForecast)
            .filter(WeatherForecast.forecast_for < before)
            .delete()
        )

        self.db.commit()
        return deleted_count