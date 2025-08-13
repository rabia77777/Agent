from datetime import datetime, timedelta, timezone
from typing import Tuple


def is_driver_hos_compliant(driver: dict, additional_drive_hours: float) -> Tuple[bool, str]:
    """Return (ok, reason)."""
    now = datetime.now(timezone.utc)

    status = driver.get("status", "available")
    if status not in ("available", "on_duty"):
        return False, f"driver status {status} not eligible"

    hours_driven_today = float(driver.get("hours_driven_today", 0.0))
    if hours_driven_today + additional_drive_hours > 11.0:
        return False, "exceeds 11 hours driving limit"

    on_duty_start = driver.get("on_duty_start")
    if on_duty_start is not None:
        if isinstance(on_duty_start, str):
            try:
                on_duty_start = datetime.fromisoformat(on_duty_start)
            except Exception:
                on_duty_start = None
    if on_duty_start is not None:
        if on_duty_start.tzinfo is None:
            on_duty_start = on_duty_start.replace(tzinfo=timezone.utc)
        on_duty_elapsed = now - on_duty_start
        if on_duty_elapsed > timedelta(hours=14):
            return False, "exceeds 14-hour on-duty window"

    last_break_start = driver.get("last_break_start")
    if last_break_start is not None:
        if isinstance(last_break_start, str):
            try:
                last_break_start = datetime.fromisoformat(last_break_start)
            except Exception:
                last_break_start = None
    if hours_driven_today >= 8.0:
        if last_break_start is None:
            return False, "30-minute break required after 8 hours driving"
        if last_break_start.tzinfo is None:
            last_break_start = last_break_start.replace(tzinfo=timezone.utc)
        if now - last_break_start < timedelta(minutes=30):
            return False, "30-minute break not satisfied"

    return True, "ok"