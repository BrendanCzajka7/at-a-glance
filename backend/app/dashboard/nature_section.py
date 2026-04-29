from datetime import datetime

from app.schemas.nature_dashboard import NaturePhotoCard, NatureSection
from app.services.nature_photo_service import NaturePhotoService


class NatureDashboardSection:
    def __init__(self, db):
        self.nature_service = NaturePhotoService(db)

    def build(self, now: datetime) -> NatureSection:
        photos = self.nature_service.list_for_date(now.date())

        return NatureSection(
            today=[
                NaturePhotoCard.model_validate(photo)
                for photo in photos
            ],
        )