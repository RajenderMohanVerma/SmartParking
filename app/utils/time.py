from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


try:
    INDIA_TZ = ZoneInfo("Asia/Kolkata")
except ZoneInfoNotFoundError:
    # India has no daylight-saving changes, so this fallback is equivalent.
    INDIA_TZ = timezone(timedelta(hours=5, minutes=30), name="IST")


def as_utc(value):
    """Normalize stored or incoming timestamps to timezone-aware UTC."""
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def to_india(value):
    """Convert a stored UTC timestamp to India Standard Time for display."""
    normalized = as_utc(value)
    return normalized.astimezone(INDIA_TZ) if normalized else None


def format_india(value, fmt):
    local_value = to_india(value)
    return local_value.strftime(fmt) if local_value else ""


def india_day_bounds_utc(day_value):
    """Return an IST calendar day's inclusive start and exclusive next-day UTC."""
    start_local = datetime.combine(day_value, time.min, tzinfo=INDIA_TZ)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def india_date_range_utc(start_date: date | None, end_date: date | None):
    start = (
        datetime.combine(start_date, time.min, tzinfo=INDIA_TZ).astimezone(timezone.utc)
        if start_date
        else None
    )
    end = (
        datetime.combine(end_date, time.min, tzinfo=INDIA_TZ).astimezone(timezone.utc)
        + timedelta(days=1)
        if end_date
        else None
    )
    return start, end
