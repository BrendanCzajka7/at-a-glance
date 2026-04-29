from datetime import datetime

from app.models.ocean_conditions import OceanConditions


class OceanConditionsRepository:
    def __init__(self, db):
        self.db = db

    def upsert(self, row: OceanConditions) -> OceanConditions:
        existing = (
            self.db.query(OceanConditions)
            .filter(
                OceanConditions.location_key == row.location_key,
                OceanConditions.station_id == row.station_id,
                OceanConditions.observed_at == row.observed_at,
            )
            .first()
        )

        if existing:
            existing.water_temperature_f = row.water_temperature_f
            existing.wave_height_ft = row.wave_height_ft
            existing.fetched_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_latest_for_location(
        self,
        location_key: str,
    ) -> OceanConditions | None:
        return (
            self.db.query(OceanConditions)
            .filter(OceanConditions.location_key == location_key)
            .order_by(OceanConditions.observed_at.desc())
            .first()
        )