from datetime import datetime
from zoneinfo import ZoneInfo


def now_for_timezone(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name)).replace(tzinfo=None)