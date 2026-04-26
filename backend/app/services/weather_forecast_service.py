from datetime import datetime

from sqlalchemy.orm import Session

from app.models.weather_forecast import WeatherForecast
from app.repositories.weather_forecast_repository import WeatherForecastRepository


class WeatherForecastService:
    def __init__(self, db: Session):
        self.repo = WeatherForecastRepository(db)

    def save_forecast_response(
        self,
        raw: dict,
        location_key: str,
        location_name: str,
    ) -> list[WeatherForecast]:
        rows: list[WeatherForecast] = []

        current = raw.get("current")
        if current:
            rows.append(
                WeatherForecast(
                    source="open_meteo",
                    location_key=location_key,
                    location_name=location_name,
                    granularity="current",
                    forecast_for=datetime.fromisoformat(current["time"]),
                    temperature_f=current.get("temperature_2m"),
                    apparent_temperature_f=current.get("apparent_temperature"),
                    precipitation_inches=current.get("precipitation"),
                    weather_code=current.get("weather_code"),
                    wind_speed_mph=current.get("wind_speed_10m"),
                    wind_gust_mph=current.get("wind_gusts_10m"),
                )
            )

        hourly = raw.get("hourly")
        if hourly:
            for i, time_value in enumerate(hourly["time"]):
                rows.append(
                    WeatherForecast(
                        source="open_meteo",
                        location_key=location_key,
                        location_name=location_name,
                        granularity="hourly",
                        forecast_for=datetime.fromisoformat(time_value),
                        temperature_f=hourly["temperature_2m"][i],
                        apparent_temperature_f=hourly["apparent_temperature"][i],
                        precipitation_probability=hourly["precipitation_probability"][i],
                        precipitation_inches=hourly["precipitation"][i],
                        weather_code=hourly["weather_code"][i],
                        wind_speed_mph=hourly["wind_speed_10m"][i],
                        wind_gust_mph=hourly["wind_gusts_10m"][i],
                        uv_index=hourly["uv_index"][i],
                    )
                )

        daily = raw.get("daily")
        if daily:
            for i, date_value in enumerate(daily["time"]):
                rows.append(
                    WeatherForecast(
                        source="open_meteo",
                        location_key=location_key,
                        location_name=location_name,
                        granularity="daily",
                        forecast_for=datetime.fromisoformat(date_value),
                        temperature_max_f=daily["temperature_2m_max"][i],
                        temperature_min_f=daily["temperature_2m_min"][i],
                        precipitation_probability=daily["precipitation_probability_max"][i],
                        precipitation_inches=daily["precipitation_sum"][i],
                        weather_code=daily["weather_code"][i],
                        uv_index=daily["uv_index_max"][i],
                        sunrise=datetime.fromisoformat(daily["sunrise"][i]),
                        sunset=datetime.fromisoformat(daily["sunset"][i]),
                    )
                )

        return self.repo.upsert_many(rows)

    def list_forecasts_between(
        self,
        start: datetime,
        end: datetime,
        location_key: str = "okaloosa_island",
    ) -> list[WeatherForecast]:
        return self.repo.list_between(
            start=start,
            end=end,
            location_key=location_key,
        )