from datetime import date, timedelta


def next_workday(day: date) -> date:
    """The next day that is not a Saturday or Sunday."""
    day += timedelta(days=1)
    while day.weekday() >= 5:
        day += timedelta(days=1)
    return day
