from app.models.ocean_conditions import OceanConditions
from app.repositories.ocean_conditions_repository import OceanConditionsRepository


class OceanConditionsService:
    def __init__(self, db):
        self.repo = OceanConditionsRepository(db)

    def save_latest_from_raw(
        self,
        location_key: str,
        station_id: str,
        raw: dict,
    ) -> OceanConditions:
        return self.repo.upsert(
            OceanConditions(
                location_key=location_key,
                station_id=station_id,
                observed_at=raw["observed_at"],
                water_temperature_f=_c_to_f(raw.get("water_temperature_c")),
                wave_height_ft=_m_to_ft(raw.get("wave_height_m")),
            )
        )

    def get_latest_for_location(
        self,
        location_key: str,
    ) -> OceanConditions | None:
        return self.repo.get_latest_for_location(location_key=location_key)


def _c_to_f(value: float | None) -> float | None:
    if value is None:
        return None

    return value * 9 / 5 + 32


def _m_to_ft(value: float | None) -> float | None:
    if value is None:
        return None

    return value * 3.28084