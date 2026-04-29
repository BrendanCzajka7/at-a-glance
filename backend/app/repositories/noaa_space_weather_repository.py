from app.models.noaa_space_weather_report import NoaaSpaceWeatherReport


class NoaaSpaceWeatherRepository:
    def __init__(self, db):
        self.db = db

    def create(self, report: NoaaSpaceWeatherReport) -> NoaaSpaceWeatherReport:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_latest(self) -> NoaaSpaceWeatherReport | None:
        return (
            self.db.query(NoaaSpaceWeatherReport)
            .order_by(NoaaSpaceWeatherReport.fetched_at.desc())
            .first()
        )