from sqlalchemy.orm import Session

from app.models.location import Location


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_key(self, key: str) -> Location | None:
        return self.db.query(Location).filter(Location.key == key).first()

    def list_active(self) -> list[Location]:
        return (
            self.db.query(Location)
            .filter(Location.is_active == True)
            .order_by(Location.name.asc())
            .all()
        )

    def create(self, location: Location) -> Location:
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location