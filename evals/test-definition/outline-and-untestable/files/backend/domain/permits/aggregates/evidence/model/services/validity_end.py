"""Domain service: when a report stops being valid."""

from datetime import date


def calculate_validity_end(delivered_on: date, validity_years: int) -> date:
    raise NotImplementedError
