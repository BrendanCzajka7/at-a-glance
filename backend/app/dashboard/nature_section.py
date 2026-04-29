from datetime import datetime

from app.schemas.nature_dashboard import NaturePhotoCard, NatureSection
from app.services.nature_photo_service import NaturePhotoService


class NatureDashboardSection:
    def __init__(self, db):
        self.nature_service = NaturePhotoService(db)

    def build(self, now: datetime) -> NatureSection:
        photo = self.nature_service.get_for_date(now.date())

        if not photo:
            photo = self.nature_service.get_latest()

        return NatureSection(
            today=NaturePhotoCard.model_validate(photo) if photo else None,
        )