from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.nasa_neo import NasaNeoCloseApproach
from app.repositories.nasa_neo_repository import NasaNeoRepository


class NasaNeoService:
    def __init__(self, db: Session):
        self.repo = NasaNeoRepository(db)

    def save_from_feed(self, raw: dict) -> list[NasaNeoCloseApproach]:
        rows: list[NasaNeoCloseApproach] = []

        by_date = raw.get("near_earth_objects", {})

        for date_key, objects in by_date.items():
            for obj in objects:
                close_approaches = obj.get("close_approach_data", [])

                if not close_approaches:
                    continue

                approach = close_approaches[0]
                diameter_m = obj.get("estimated_diameter", {}).get("meters", {})

                rows.append(
                    NasaNeoCloseApproach(
                        neo_reference_id=obj["neo_reference_id"],
                        name=obj["name"],
                        nasa_jpl_url=obj.get("nasa_jpl_url"),
                        close_approach_date=date.fromisoformat(date_key),
                        close_approach_time=approach.get("close_approach_date_full"),
                        estimated_diameter_min_m=diameter_m.get(
                            "estimated_diameter_min"
                        ),
                        estimated_diameter_max_m=diameter_m.get(
                            "estimated_diameter_max"
                        ),
                        miss_distance_km=float(
                            approach.get("miss_distance", {}).get("kilometers")
                            or 0
                        ),
                        miss_distance_lunar=float(
                            approach.get("miss_distance", {}).get("lunar")
                            or 0
                        ),
                        relative_velocity_kph=float(
                            approach.get("relative_velocity", {}).get(
                                "kilometers_per_hour"
                            )
                            or 0
                        ),
                        is_potentially_hazardous=obj.get(
                            "is_potentially_hazardous_asteroid",
                            False,
                        ),
                    )
                )

        return self.repo.upsert_many(rows)

    def list_between(
        self,
        start: date,
        end: date,
    ) -> list[NasaNeoCloseApproach]:
        return self.repo.list_between(start=start, end=end)

    def list_notable_between(
        self,
        start: date,
        end: date,
    ) -> list[NasaNeoCloseApproach]:
        rows = self.repo.list_between(start=start, end=end)

        notable = [
            row
            for row in rows
            if row.is_potentially_hazardous
            or (row.miss_distance_lunar is not None and row.miss_distance_lunar <= 20)
            or (
                row.estimated_diameter_max_m is not None
                and row.estimated_diameter_max_m >= 100
            )
        ]

        return notable