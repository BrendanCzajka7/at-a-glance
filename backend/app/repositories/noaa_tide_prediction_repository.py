from datetime import datetime

from app.models.noaa_tide_prediction import NoaaTidePrediction


class NoaaTidePredictionRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(
        self,
        rows: list[NoaaTidePrediction],
    ) -> list[NoaaTidePrediction]:
        saved: list[NoaaTidePrediction] = []

        for row in rows:
            existing = (
                self.db.query(NoaaTidePrediction)
                .filter(
                    NoaaTidePrediction.location_key == row.location_key,
                    NoaaTidePrediction.station_id == row.station_id,
                    NoaaTidePrediction.prediction_time == row.prediction_time,
                    NoaaTidePrediction.tide_type == row.tide_type,
                )
                .first()
            )

            if existing:
                existing.height_ft = row.height_ft
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(row)
                saved.append(row)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        location_key: str,
        start: datetime,
        end: datetime,
    ) -> list[NoaaTidePrediction]:
        return (
            self.db.query(NoaaTidePrediction)
            .filter(
                NoaaTidePrediction.location_key == location_key,
                NoaaTidePrediction.prediction_time >= start,
                NoaaTidePrediction.prediction_time < end,
            )
            .order_by(NoaaTidePrediction.prediction_time.asc())
            .all()
        )