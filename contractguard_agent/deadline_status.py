from datetime import datetime
from typing import Optional


def get_deadline_status(
    deadline_date: str,
    warning_days: int = 30
) -> Optional[str]:
    """
    Determines the status of a contract renewal deadline.

    Status:
    - PASSED
    - URGENT
    - UPCOMING
    - SAFE
    """

    if not deadline_date:
        return None

    try:
        deadline = datetime.strptime(
            deadline_date,
            "%B %d, %Y"
        ).date()

        today = datetime.today().date()

        days_remaining = (deadline - today).days

        if days_remaining < 0:
            return "PASSED"

        if days_remaining <= 7:
            return "URGENT"

        if days_remaining <= warning_days:
            return "UPCOMING"

        return "SAFE"

    except (ValueError, TypeError):
        return None