import json
import re

from app.models.noaa_space_weather_report import NoaaSpaceWeatherReport
from app.repositories.noaa_space_weather_repository import (
    NoaaSpaceWeatherRepository,
)


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

    def summarize_scales(self, report: NoaaSpaceWeatherReport) -> str | None:
        if not report.scales_json:
            return None

        try:
            data = json.loads(report.scales_json)
        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None

        parts: list[str] = []

        for key in ["R", "S", "G"]:
            value = data.get(key)
            if value is None:
                continue

            if isinstance(value, dict):
                scale = value.get("Scale") or value.get("scale") or value.get("level")
                text = value.get("Text") or value.get("text")
                if scale or text:
                    parts.append(f"{key}: {scale or text}")
            else:
                parts.append(f"{key}: {value}")

        return " · ".join(parts) if parts else None

    def summarize_alert_titles(self, report: NoaaSpaceWeatherReport) -> list[str]:
        if not report.alerts_json:
            return []

        try:
            data = json.loads(report.alerts_json)
        except json.JSONDecodeError:
            return []

        if not isinstance(data, list):
            return []

        titles: list[str] = []

        for item in data[:10]:
            if not isinstance(item, dict):
                continue

            title = (
                item.get("message")
                or item.get("product_id")
                or item.get("issue_datetime")
                or item.get("serial_number")
            )

            if title:
                titles.append(str(title))

        return titles

    def summarize_forecast_text(self, report: NoaaSpaceWeatherReport) -> str | None:
        text = report.three_day_forecast_text

        if not text:
            return None

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        interesting = []

        patterns = [
            "R1-R2",
            "R3-R5",
            "S1",
            "G1",
            "G2",
            "G3",
            "G4",
            "G5",
            "Geomagnetic",
            "Solar Radiation",
            "Radio Blackout",
        ]

        for line in lines:
            if any(pattern in line for pattern in patterns):
                interesting.append(re.sub(r"\s+", " ", line))

            if len(interesting) >= 6:
                break

        if interesting:
            return " | ".join(interesting)

        return " ".join(lines[:6]) if lines else None