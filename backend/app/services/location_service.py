from sqlalchemy.orm import Session

from app.models.location import Location
from app.repositories.location_repository import LocationRepository


class LocationService:
    def __init__(self, db: Session):
        self.repo = LocationRepository(db)

    def get_required(self, location_key: str) -> Location:
        location = self.repo.get_by_key(location_key)

        if not location:
            raise ValueError(f"Unknown location_key: {location_key}")

        return location

    def list_active(self) -> list[Location]:
        return self.repo.list_active()

    def create_location(
        self,
        key: str,
        name: str,
        latitude: float,
        longitude: float,
        timezone: str,
    ) -> Location:
        existing = self.repo.get_by_key(key)
        if existing:
            return existing

        return self.repo.create(
            Location(
                key=key,
                name=name,
                latitude=latitude,
                longitude=longitude,
                timezone=timezone,
            )
        )