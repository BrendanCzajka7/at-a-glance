from datetime import datetime

from pydantic import BaseModel


class NasaSpaceWeatherNotificationRead(BaseModel):
    id: int
    message_id: str
    message_type: str | None = None
    message_issue_time: datetime
    message_url: str | None = None

    title: str
    summary: str

    fetched_at: datetime

    model_config = {"from_attributes": True}