from datetime import datetime, time, timedelta

from sqlalchemy.orm import Session

from app.schemas.weather_dashboard import (
    WeatherCurrent,
    WeatherDay,
    WeatherHour,
    WeatherMonth,
    WeatherSection,
    WeatherToday,
    WeatherWeek,
)
from app.services.weather_forecast_service import WeatherForecastService


class WeatherDashboardSection:
    def __init__(self, db: Session):
        self.weather_service = WeatherForecastService(db)

    def build(
        self,
        start: datetime,
        end: datetime,
        location_key: str,
    ) -> WeatherSection:
        current_row = self.weather_service.get_latest_current(
            location_key=location_key,
        )

        current = (
            WeatherCurrent.model_validate(current_row)
            if current_row
            else None
        )

        today_start = datetime.combine(start.date(), time.min)
        tomorrow_start = today_start + timedelta(days=1)
        week_end = today_start + timedelta(days=7)
        month_end = today_start + timedelta(days=31)

        hourly_rows = self.weather_service.list_forecasts_between(
            start=start,
            end=tomorrow_start,
            location_key=location_key,
        )

        daily_rows = self.weather_service.list_forecasts_between(
            start=today_start,
            end=month_end,
            location_key=location_key,
        )

        hourly = [
            WeatherHour.model_validate(row)
            for row in hourly_rows
            if row.granularity == "hourly"
        ]

        daily = [
            WeatherDay.model_validate(row)
            for row in daily_rows
            if row.granularity == "daily"
        ]

        today_summary = daily[0] if daily else None
        today_hours = hourly

        next_hours = hourly[:6]

        week_days = daily[:7]
        month_days = daily

        return WeatherSection(
            current=current,
            today=WeatherToday(
                summary=today_summary,
                hours=today_hours,
            ),
            next_hours=next_hours,
            week=WeatherWeek(
                days=week_days,
            ),
            month=WeatherMonth(
                days=month_days,
            ),
        )