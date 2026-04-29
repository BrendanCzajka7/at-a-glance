from datetime import datetime

from app.models.noaa_tide_prediction import NoaaTidePrediction
from app.repositories.noaa_tide_prediction_repository import (
    NoaaTidePredictionRepository,
)


class NoaaTideService:
    def __init__(self, db):
        self.repo = NoaaTidePredictionRepository(db)

    def save_from_raw_predictions(
        self,
        location_key: str,
        station_id: str,
        raw_predictions: list[dict],
    ) -> list[NoaaTidePrediction]:
        rows: list[NoaaTidePrediction] = []
        seen_keys: set[tuple[str, str | None]] = set()

        for raw in raw_predictions:
            time_raw = raw.get("t")
            height_raw = raw.get("v")
            tide_type = raw.get("type")

            if not time_raw:
                continue

            key = (time_raw, tide_type)
            if key in seen_keys:
                continue

            seen_keys.add(key)

            try:
                prediction_time = datetime.strptime(time_raw, "%Y-%m-%d %H:%M")
            except ValueError:
                continue

            rows.append(
                NoaaTidePrediction(
                    location_key=location_key,
                    station_id=station_id,
                    prediction_time=prediction_time,
                    tide_type=tide_type,
                    height_ft=_safe_float(height_raw),
                )
            )

        return self.repo.upsert_many(rows)

    def list_between(
        self,
        location_key: str,
        start: datetime,
        end: datetime,
    ) -> list[NoaaTidePrediction]:
        return self.repo.list_between(
            location_key=location_key,
            start=start,
            end=end,
        )


def _safe_float(value):
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None