from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.schemas.nasa_dashboard import (
    NasaApodCard,
    NasaEpicCard,
    NasaNeoCard,
    NasaNeoSection,
    NasaSection,
)
from app.services.nasa_apod_service import NasaApodService
from app.services.nasa_epic_service import NasaEpicService
from app.services.nasa_neo_service import NasaNeoService


class NasaDashboardSection:
    def __init__(self, db: Session):
        self.apod_service = NasaApodService(db)
        self.epic_service = NasaEpicService(db)
        self.neo_service = NasaNeoService(db)

    def build(self, start: datetime) -> NasaSection:
        apod = self.apod_service.get_latest()
        epic = self.epic_service.get_latest()

        today = start.date()
        week_end = today + timedelta(days=7)
        month_end = today + timedelta(days=31)

        today_neos = self.neo_service.list_notable_between(
            start=today,
            end=today,
        )

        week_neos = self.neo_service.list_notable_between(
            start=today,
            end=week_end,
        )

        month_neos = self.neo_service.list_notable_between(
            start=today,
            end=month_end,
        )

        return NasaSection(
            apod=NasaApodCard.model_validate(apod) if apod else None,
            epic=NasaEpicCard.model_validate(epic) if epic else None,
            neos=NasaNeoSection(
                today=[NasaNeoCard.model_validate(item) for item in today_neos],
                week=[NasaNeoCard.model_validate(item) for item in week_neos],
                month=[NasaNeoCard.model_validate(item) for item in month_neos],
            ),
        )