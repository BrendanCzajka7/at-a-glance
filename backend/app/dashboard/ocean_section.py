from app.schemas.ocean_dashboard import OceanConditionsCard, OceanSection
from app.services.ocean_conditions_service import OceanConditionsService


class OceanDashboardSection:
    def __init__(self, db):
        self.ocean_service = OceanConditionsService(db)

    def build(self, location_key: str) -> OceanSection:
        latest = self.ocean_service.get_latest_for_location(
            location_key=location_key,
        )

        return OceanSection(
            current=OceanConditionsCard.model_validate(latest) if latest else None,
        )