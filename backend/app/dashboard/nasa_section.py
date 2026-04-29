from sqlalchemy.orm import Session

from app.schemas.nasa_dashboard import NasaApodCard, NasaSection
from app.services.nasa_apod_service import NasaApodService


class NasaDashboardSection:
    def __init__(self, db: Session):
        self.apod_service = NasaApodService(db)

    def build(self) -> NasaSection:
        apod = self.apod_service.get_latest()

        return NasaSection(
            apod=NasaApodCard.model_validate(apod) if apod else None,
        )