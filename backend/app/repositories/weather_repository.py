from sqlalchemy.orm import Session

from app.models.weather_snapshot import WeatherSnapshot


class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_snapshot(self, snapshot: WeatherSnapshot) -> WeatherSnapshot:
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot

    def list_latest(self, limit: int = 20) -> list[WeatherSnapshot]:
        return (
            self.db.query(WeatherSnapshot)
            .order_by(WeatherSnapshot.observed_at.desc())
            .limit(limit)
            .all()
        )