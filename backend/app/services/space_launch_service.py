from datetime import datetime

from app.models.space_launch import SpaceLaunch
from app.repositories.space_launch_repository import SpaceLaunchRepository


class SpaceLaunchService:
    def __init__(self, db):
        self.repo = SpaceLaunchRepository(db)

    def save_from_raw_launches(
        self,
        raw_launches: list[dict],
    ) -> list[SpaceLaunch]:
        rows: list[SpaceLaunch] = []
        seen_ids: set[str] = set()

        for raw in raw_launches:
            launch_id = raw.get("id")
            name = raw.get("name")
            net_raw = raw.get("net")

            if not launch_id or not name or not net_raw:
                continue

            if launch_id in seen_ids:
                continue

            seen_ids.add(launch_id)

            try:
                net = datetime.fromisoformat(net_raw.replace("Z", "+00:00")).replace(
                    tzinfo=None
                )
            except ValueError:
                continue

            mission = raw.get("mission") or {}
            status = raw.get("status") or {}
            provider = raw.get("launch_service_provider") or {}
            rocket = raw.get("rocket") or {}
            rocket_config = rocket.get("configuration") or {}
            pad = raw.get("pad") or {}
            location = pad.get("location") or {}

            rows.append(
                SpaceLaunch(
                    launch_library_id=launch_id,
                    name=name,
                    net=net,
                    status_name=status.get("name"),
                    mission_name=mission.get("name"),
                    mission_description=mission.get("description"),
                    provider_name=provider.get("name"),
                    rocket_name=rocket_config.get("full_name")
                    or rocket_config.get("name"),
                    pad_name=pad.get("name"),
                    location_name=location.get("name"),
                    image_url=raw.get("image"),
                    webcast_url=raw.get("webcast_live")
                    or raw.get("vidURLs", [{}])[0].get("url")
                    if raw.get("vidURLs")
                    else None,
                    source_url=raw.get("url"),
                    flightclub_url=raw.get("flightclub_url"),
                    is_crewed=raw.get("is_crewed"),
                )
            )

        return self.repo.upsert_many(rows)

    def list_between(
        self,
        start: datetime,
        end: datetime,
    ) -> list[SpaceLaunch]:
        return self.repo.list_between(start=start, end=end)