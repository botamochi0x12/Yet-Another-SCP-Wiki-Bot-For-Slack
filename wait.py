"""
Util functions to wait for time to post notifications.
"""

import logging
import time
from collections.abc import Callable
from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

JST = ZoneInfo("Asia/Tokyo")


def wait_until(
    then: datetime | None = None,
    *,
    day: int | None = None,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    _how_to_know_now: Callable[[], datetime] | None = None,
    _sleep: Callable[[float], None] = time.sleep,
    _debug: Callable[[str], None] = lambda msg: logger.debug(msg),
) -> None:
    """Wait until a specific time point. Default to 0:00 on the next day."""
    duration = compute_duration_to_tomorrow(
        then=then,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        how_to_know_now=(
            _how_to_know_now if _how_to_know_now else lambda: datetime.now(tz=JST)
        ),
    )
    _debug(f"Wait for {duration} sec(s).")
    _sleep(duration)


def compute_duration_to_tomorrow(
    then: datetime | None = None,
    *,
    how_to_know_now: Callable[[], datetime] = lambda: datetime.now(tz=JST),
    **kwargs: int | None,
) -> float:
    if then is None and len(kwargs) == 0:
        raise ValueError("Any of `datetime` properties should be specified.")

    now = how_to_know_now()
    if then is None:
        if kwargs.get("day") is None:
            kwargs["day"] = now.day
        then = now.replace(**kwargs)
    duration = differ_from(now=now, then=then)
    if duration < 0.0:
        duration += 24 * 60 * 60.0
    return duration


def differ_from(*, now: datetime, then: datetime) -> float:
    return (then - now).total_seconds()
