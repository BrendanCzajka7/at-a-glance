from dataclasses import dataclass


@dataclass(frozen=True)
class LocationConfig:
    key: str
    name: str
    latitude: float
    longitude: float
    timezone: str


LOCATIONS = {
    "okaloosa_island": LocationConfig(
        key="okaloosa_island",
        name="Okaloosa Island, FL",
        latitude=30.3914,
        longitude=-86.5932,
        timezone="America/Chicago",
    ),
    "chicago": LocationConfig(
        key="chicago",
        name="Chicago, IL",
        latitude=41.8781,
        longitude=-87.6298,
        timezone="America/Chicago",
    ),
}


def get_location(location_key: str) -> LocationConfig:
    try:
        return LOCATIONS[location_key]
    except KeyError:
        raise ValueError(f"Unknown location_key: {location_key}")