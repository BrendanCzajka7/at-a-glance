from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.nasa_neo import NasaNeoCloseApproach


class NasaNeoRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_many(
        self,
        rows: list[NasaNeoCloseApproach],
    ) -> list[NasaNeoCloseApproach]:
        saved: list[NasaNeoCloseApproach] = []

        for row in rows:
            existing = (
                self.db.query(NasaNeoCloseApproach)
                .filter(
                    NasaNeoCloseApproach.neo_reference_id == row.neo_reference_id,
                    NasaNeoCloseApproach.close_approach_date == row.close_approach_date,
                )
                .first()
            )

            if existing:
                existing.name = row.name
                existing.nasa_jpl_url = row.nasa_jpl_url
                existing.close_approach_time = row.close_approach_time
                existing.estimated_diameter_min_m = row.estimated_diameter_min_m
                existing.estimated_diameter_max_m = row.estimated_diameter_max_m
                existing.miss_distance_km = row.miss_distance_km
                existing.miss_distance_lunar = row.miss_distance_lunar
                existing.relative_velocity_kph = row.relative_velocity_kph
                existing.is_potentially_hazardous = row.is_potentially_hazardous
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
        start: date,
        end: date,
    ) -> list[NasaNeoCloseApproach]:
        return (
            self.db.query(NasaNeoCloseApproach)
            .filter(
                NasaNeoCloseApproach.close_approach_date >= start,
                NasaNeoCloseApproach.close_approach_date <= end,
            )
            .order_by(
                NasaNeoCloseApproach.close_approach_date.asc(),
                NasaNeoCloseApproach.miss_distance_lunar.asc(),
            )
            .all()
        )