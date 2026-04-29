from datetime import datetime

import httpx


class NdbcClient:
    BASE_URL = "https://www.ndbc.noaa.gov/data/realtime2"

    async def fetch_latest_conditions(self, station_id: str) -> dict | None:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.BASE_URL}/{station_id}.txt")
            response.raise_for_status()
            text = response.text

        return parse_latest_standard_meteorological_row(text)


def parse_latest_standard_meteorological_row(text: str) -> dict | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if len(lines) < 3:
        return None

    header_line = lines[0].lstrip("#").strip()
    columns = header_line.split()

    for line in lines[2:]:
        if line.startswith("#"):
            continue

        values = line.split()

        if len(values) < len(columns):
            continue

        row = dict(zip(columns, values))

        observed_at = _parse_observed_at(row)

        if not observed_at:
            continue

        return {
            "observed_at": observed_at,
            "water_temperature_c": _safe_float(row.get("WTMP")),
            "wave_height_m": _safe_float(row.get("WVHT")),
        }

    return None


def _parse_observed_at(row: dict) -> datetime | None:
    try:
        year = int(row["YY"])
        month = int(row["MM"])
        day = int(row["DD"])
        hour = int(row["hh"])
        minute = int(row["mm"])
    except (KeyError, TypeError, ValueError):
        return None

    return datetime(year, month, day, hour, minute)


def _safe_float(value: str | None) -> float | None:
    if value is None:
        return None

    if value in {"MM", "999", "999.0", "99.0", "99.00"}:
        return None

    try:
        return float(value)
    except ValueError:
        return None