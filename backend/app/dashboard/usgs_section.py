from datetime import datetime, timedelta

from app.schemas.usgs_dashboard import UsgsEarthquakeCard, UsgsSection
from app.services.usgs_earthquake_service import UsgsEarthquakeService


class UsgsDashboardSection:
    def __init__(self, db):
        self.earthquake_service = UsgsEarthquakeService(db)

    def build(self, now: datetime) -> UsgsSection:
        since = now - timedelta(hours=24)

        earthquakes = self.earthquake_service.list_since(since=since)

        largest = _max_by(
            earthquakes,
            key=lambda item: item.magnitude if item.magnitude is not None else -1,
        )

        most_significant = _max_by(
            earthquakes,
            key=lambda item: item.significance
            if item.significance is not None
            else -1,
        )

        tsunami_events = [
            item for item in earthquakes
            if item.tsunami == 1
        ]

        alert_events = [
            item for item in earthquakes
            if item.alert is not None
        ]

        return UsgsSection(
            largest_today=(
                UsgsEarthquakeCard.model_validate(largest)
                if largest
                else None
            ),
            most_significant_today=(
                UsgsEarthquakeCard.model_validate(most_significant)
                if most_significant
                else None
            ),
            tsunami_events_today=[
                UsgsEarthquakeCard.model_validate(item)
                for item in tsunami_events
            ],
            alert_events_today=[
                UsgsEarthquakeCard.model_validate(item)
                for item in alert_events
            ],
        )


def _max_by(items, key):
    if not items:
        return None

    return max(items, key=key)