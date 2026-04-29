# backend/app/schemas/app_event.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    level: str
    source: str
    event_type: str
    message: str
    details: str | None = None
    created_at: datetime