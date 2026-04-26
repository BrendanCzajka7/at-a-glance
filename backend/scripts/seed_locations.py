from app.core.db import Base, SessionLocal, engine
from app.models.location import Location
from app.models.weather_forecast import WeatherForecast
from app.services.location_service import LocationService


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        service = LocationService(db)

        service.create_location(
            key="okaloosa_island",
            name="Okaloosa Island, FL",
            latitude=30.3914,
            longitude=-86.5932,
            timezone="America/Chicago",
        )

        service.create_location(
            key="chicago",
            name="Chicago, IL",
            latitude=41.8781,
            longitude=-87.6298,
            timezone="America/Chicago",
        )

        print("Seeded locations.")
    finally:
        db.close()


if __name__ == "__main__":
    main()