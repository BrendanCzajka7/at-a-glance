from datetime import datetime

from app.models.space_launch import SpaceLaunch


class SpaceLaunchRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(self, launches: list[SpaceLaunch]) -> list[SpaceLaunch]:
        saved: list[SpaceLaunch] = []

        for launch in launches:
            existing = (
                self.db.query(SpaceLaunch)
                .filter(SpaceLaunch.launch_library_id == launch.launch_library_id)
                .first()
            )

            if existing:
                existing.name = launch.name
                existing.net = launch.net
                existing.status_name = launch.status_name
                existing.mission_name = launch.mission_name
                existing.mission_description = launch.mission_description
                existing.provider_name = launch.provider_name
                existing.rocket_name = launch.rocket_name
                existing.pad_name = launch.pad_name
                existing.location_name = launch.location_name
                existing.image_url = launch.image_url
                existing.webcast_url = launch.webcast_url
                existing.source_url = launch.source_url
                existing.is_crewed = launch.is_crewed
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(launch)
                saved.append(launch)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        start: datetime,
        end: datetime,
    ) -> list[SpaceLaunch]:
        return (
            self.db.query(SpaceLaunch)
            .filter(
                SpaceLaunch.net >= start,
                SpaceLaunch.net <= end,
            )
            .order_by(SpaceLaunch.net.asc())
            .all()
        )