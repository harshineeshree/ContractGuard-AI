from datetime import datetime, timedelta
from typing import Optional


def calculate_renewal_deadline(
    expiration_date: str,
    notice_period_days: str
) -> Optional[str]:
    """
    Calculates the deadline for giving renewal notice.

    Example:
    Expiration: December 31, 2026
    Notice: 60 days

    Result:
    November 1, 2026
    """

    if not expiration_date or not notice_period_days:
        return None

    try:
        # Convert the notice period into a number
        days = int(
            notice_period_days.lower()
            .replace("days", "")
            .strip()
        )

        # Convert the contract date into a Python date
        expiration = datetime.strptime(
            expiration_date,
            "%B %d, %Y"
        )

        # Calculate deadline
        deadline = expiration - timedelta(days=days)

        return deadline.strftime("%B %d, %Y")

    except (ValueError, TypeError):
        return None