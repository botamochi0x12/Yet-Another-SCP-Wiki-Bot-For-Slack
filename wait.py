"""
Util functions to wait for time to post notifications.
"""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional

TimeSeconds = float
Datetime = datetime

# offset from UTC to JST
TIMEZONE_OFFSET = (timedelta(hours=9) - timedelta(hours=0)).seconds


def wait_until(
    then: Optional[Datetime] = None,
    *,
    day=None, hour=0, minute=0, second=0,
    _how_to_know_now=None,
    _sleep=time.sleep,
    _debug=print,
) -> None:
    """Wait until a specific time point. Default to 0:00 on the next day.

    Args:
        then (Optional[Datetime], optional): Defaults to None.
        day (Optional[int], optional): Defaults to today.
        hour (int, optional): Defaults to 0.
        minute (int, optional): Defaults to 0.
        second (int, optional): Defaults to 0.
        _how_to_know_now (optional): Defaults to None.
        _sleep (optional): Defaults to time.sleep.
        _debug (optional): Defaults to print.

    >>> now = Datetime.now(tz=timezone(timedelta(hours=+9)))
    >>> wait_until(
    ...     hour=now.hour, minute=now.minute, second=now.second,
    ...     _sleep=(lambda _: None),
    ...     _how_to_know_now=(lambda: Datetime.now(tz=timezone(timedelta(hours=0)))),
    ... )
    Wait for 0.0 sec(s).
    """

    duration = compute_duration_to_tomorrow(
        then=then,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        # for debugging
        how_to_know_now=_how_to_know_now if _how_to_know_now else Datetime.now,
        )
    duration = duration - TIMEZONE_OFFSET
    _debug(f"Wait for {duration} sec(s). ")
    _sleep(duration)


def compute_duration_to_tomorrow(
    then: Optional[Datetime] = None,
    *,
    how_to_know_now=Datetime.now,
    **kwargs
) -> TimeSeconds:
    """
    >>> now = Datetime(year=2020, month=6, day=15, hour=0)

    >>> duration_to_tomorrow = compute_duration_to_tomorrow(
    ...    how_to_know_now=(lambda: now),
    ...    day=now.day, hour=1,
    ...    )

    >>> duration_to_yesterday = compute_duration_to_tomorrow(
    ...     how_to_know_now=(lambda: now),
    ...     day=(now.day-1), hour=1,
    ...     )

    >>> int(duration_to_yesterday) == int(duration_to_tomorrow)
    True
    """

    if then is None and len(kwargs) == 0:
        raise ValueError("Any of `datetime` properties should be specified.")

    now = how_to_know_now()
    if then is None:
        if kwargs["day"] is None:
            kwargs["day"] = now.day
        then: Datetime = now.replace(**kwargs)
    duration = differ_from(now=now, then=then)
    if duration < 0.0:
        duration += 24 * 60 * 60.0
    return duration


def differ_from(*, now: Datetime, then: Datetime) -> TimeSeconds:
    """
    >>> now = Datetime.now()
    >>> duration = differ_from(now=now, then=now)
    >>> int(duration)
    0

    >>> tomorrow = now.replace(day=(now.day + 1))
    >>> duration = differ_from(now=now, then=tomorrow)
    >>> int(duration)
    86400

    >>> yesterday = now.replace(day=(now.day - 1))
    >>> duration = differ_from(now=now, then=yesterday)
    >>> int(duration)
    -86400
    """
    duration = (then - now).total_seconds()
    return duration
