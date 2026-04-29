import json
import re

from app.models.noaa_space_weather_report import NoaaSpaceWeatherReport
from app.repositories.noaa_space_weather_repository import (
    NoaaSpaceWeatherRepository,
)
from app.schemas.noaa_dashboard import NoaaSpaceWeatherDayCard


class NoaaSpaceWeatherService:
    def __init__(self, db):
        self.repo = NoaaSpaceWeatherRepository(db)

    def save_report(
        self,
        scales: dict,
        alerts: list[dict],
        forecast_text: str,
    ) -> NoaaSpaceWeatherReport:
        return self.repo.create(
            NoaaSpaceWeatherReport(
                scales_json=json.dumps(scales),
                alerts_json=json.dumps(alerts),
                three_day_forecast_text=forecast_text,
            )
        )

    def get_latest(self) -> NoaaSpaceWeatherReport | None:
        return self.repo.get_latest()

    def get_scales_data(self, report: NoaaSpaceWeatherReport) -> dict:
        if not report.scales_json:
            return {}

        try:
            data = json.loads(report.scales_json)
        except json.JSONDecodeError:
            return {}

        return data if isinstance(data, dict) else {}

    def forecast_days(
        self,
        report: NoaaSpaceWeatherReport,
    ) -> list[NoaaSpaceWeatherDayCard]:
        data = self.get_scales_data(report)

        return [
            self._forecast_day(data.get("1"), "Today"),
            self._forecast_day(data.get("2"), "Tomorrow"),
            self._forecast_day(data.get("3"), "Day 3"),
        ]

    def current_scale_value(
        self,
        report: NoaaSpaceWeatherReport,
        category: str,
        field: str,
    ) -> str | None:
        data = self.get_scales_data(report)
        current = data.get("0") or {}
        category_data = current.get(category) or {}

        value = category_data.get(field)

        if value is None:
            return None

        return str(value)

    def alert_count(self, report: NoaaSpaceWeatherReport) -> int:
        return len(_load_alerts(report))

    def recent_alert_titles(
        self,
        report: NoaaSpaceWeatherReport,
        limit: int = 3,
    ) -> list[str]:
        alerts = _load_alerts(report)
        titles: list[str] = []

        for item in alerts[:limit]:
            title = _compact_alert_title(item)
            if title:
                titles.append(title)

        return titles

    def _forecast_day(
        self,
        raw: dict | None,
        label: str,
    ) -> NoaaSpaceWeatherDayCard:
        raw = raw or {}

        r = raw.get("R") or {}
        s = raw.get("S") or {}
        g = raw.get("G") or {}

        return NoaaSpaceWeatherDayCard(
            label=label,
            date=raw.get("DateStamp"),
            radio_blackout_minor_prob=_safe_int(r.get("MinorProb")),
            radio_blackout_major_prob=_safe_int(r.get("MajorProb")),
            solar_radiation_storm_prob=_safe_int(s.get("Prob")),
            geomagnetic_scale=_safe_str(g.get("Scale")),
            geomagnetic_text=_safe_str(g.get("Text")),
        )


def _load_alerts(report: NoaaSpaceWeatherReport) -> list[dict]:
    if not report.alerts_json:
        return []

    try:
        data = json.loads(report.alerts_json)
    except json.JSONDecodeError:
        return []

    return data if isinstance(data, list) else []


def _compact_alert_title(item: dict) -> str | None:
    message = item.get("message") or item.get("message_body")

    if isinstance(message, str):
        for line in message.splitlines():
            cleaned = _clean_line(line)

            if cleaned.startswith(("ALERT:", "WATCH:", "WARNING:", "SUMMARY:", "EXTENDED WARNING:")):
                return cleaned

    product_id = item.get("product_id")
    issue_datetime = item.get("issue_datetime")

    if product_id and issue_datetime:
        return f"{product_id} · {issue_datetime}"

    if product_id:
        return str(product_id)

    return None


def _safe_int(value) -> int | None:
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_str(value) -> str | None:
    if value is None:
        return None

    return str(value)


def _clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()