from datetime import datetime

from wait import JST, compute_duration_to_tomorrow, differ_from, wait_until


def test_differ_from_same_time() -> None:
    now = datetime(2024, 1, 15, 10, 0, 0, tzinfo=JST)
    assert differ_from(now=now, then=now) == 0.0


def test_differ_from_one_day() -> None:
    now = datetime(2024, 1, 15, 10, 0, 0, tzinfo=JST)
    tomorrow = datetime(2024, 1, 16, 10, 0, 0, tzinfo=JST)
    assert differ_from(now=now, then=tomorrow) == 86400.0


def test_compute_duration_same_hour() -> None:
    now = datetime(2024, 1, 15, 10, 0, 0, tzinfo=JST)
    duration = compute_duration_to_tomorrow(
        how_to_know_now=lambda: now,
        day=now.day,
        hour=10,
        minute=0,
        second=0,
    )
    assert int(duration) == 0


def test_wait_until_calls_sleep(mocker) -> None:  # type: ignore[no-untyped-def]
    sleep_mock = mocker.Mock()
    now = datetime(2024, 1, 15, 9, 0, 0, tzinfo=JST)
    wait_until(
        hour=10,
        _how_to_know_now=lambda: now,
        _sleep=sleep_mock,
    )
    sleep_mock.assert_called_once()
    assert sleep_mock.call_args[0][0] >= 0.0


def test_wait_until_no_negative_sleep(mocker) -> None:  # type: ignore[no-untyped-def]
    sleep_mock = mocker.Mock()
    now = datetime(2024, 1, 15, 11, 0, 0, tzinfo=JST)  # past 10:00
    wait_until(
        hour=10,
        _how_to_know_now=lambda: now,
        _sleep=sleep_mock,
    )
    assert sleep_mock.call_args[0][0] >= 0.0
