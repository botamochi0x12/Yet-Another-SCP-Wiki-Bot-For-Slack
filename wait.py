"""
Util functions to wait for time to post notifications.
"""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional

TimeSeconds = float
Datetime = datetime


def _get_now() -> Datetime:
    """Get the current time in JST

    Returns:
        Datetime: datetime in JST
    """
    jst = timezone(timedelta(hours=+9))
    now = Datetime.now(tz=jst)
    return now


def wait_until(
    then: Optional[Datetime] = None,
    *,
    day=None, hour=0, minute=0, second=0,
    _how_to_know_now=_get_now,
    _sleep=time.sleep,
    _debug=print,
    ) -> None:
    """Wait until a specific time point. Default to 0:00 on the next day.

    Args:
        then (Optional[Datetime], optional): [description]. Defaults to None.
        day (Optional[int], optional): [description]. Defaults to today.
        hour (int, optional): [description]. Defaults to 0.
        minute (int, optional): [description]. Defaults to 0.
        second (int, optional): [description]. Defaults to 0.
        _how_to_know_now (optional): [description]. Defaults to _get_now.
        _sleep (optional): [description]. Defaults to time.sleep.
        _debug (optional): [description]. Defaults to print.

    >>> now = datetime.now()
    >>> wait_until(hour=now.hour, minute=now.minute, second=now.second)
    Wait for 0.0 sec(s).
    """

    duration = then if then is not None else compute_duration_to_tomorrow(
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        # for debugging
        how_to_know_now=_how_to_know_now,
        )
    _debug(f"Wait for {duration} sec(s). ")
    _sleep(duration)


def compute_duration_to_tomorrow(
    *,
    how_to_know_now=_get_now,
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

    if len(kwargs) == 0:
        raise ValueError("Any of `datetime` properties should be specified.")

    now = how_to_know_now()
    if kwargs["day"] is None:
        kwargs["day"] = now.day
    then = now.replace(**kwargs)
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
