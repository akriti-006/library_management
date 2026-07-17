from datetime import date


FINE_PER_DAY = 10


def calculate_fine(due_date: date, returned_on: date):
    """
    Calculate fine based on overdue days.
    """

    if returned_on <= due_date:
        return {
            "late_days": 0,
            "fine_amount": 0,
        }

    late_days = (returned_on - due_date).days

    fine = late_days * FINE_PER_DAY

    return {
        "late_days": late_days,
        "fine_amount": fine,
    }