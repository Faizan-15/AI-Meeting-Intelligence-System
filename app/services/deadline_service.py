from datetime import date, datetime, timedelta
import calendar


def normalize_deadline(deadline: str, meeting_date: date):
    if not deadline:
        return None

    text = deadline.lower().strip()

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    # Exact weekday
    if text in weekdays:
        target_day = weekdays[text]
        days_ahead = (target_day - meeting_date.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        return (meeting_date + timedelta(days=days_ahead)).isoformat()

    # Next weekday
    if text.startswith("next "):
        next_day = text.replace("next ", "").strip()

        if next_day in weekdays:
            target_day = weekdays[next_day]
            days_ahead = (target_day - meeting_date.weekday()) % 7

            if days_ahead == 0:
                days_ahead = 7

            return (meeting_date + timedelta(days=days_ahead)).isoformat()

    # Tomorrow
    if text == "tomorrow":
        return (meeting_date + timedelta(days=1)).isoformat()

    # End of month
    if text in ["end of month", "end of the month"]:
        last_day = calendar.monthrange(
            meeting_date.year,
            meeting_date.month
        )[1]

        return date(
            meeting_date.year,
            meeting_date.month,
            last_day
        ).isoformat()

    # Explicit date such as "September 10"
    for fmt in ("%B %d", "%b %d"):
        try:
            parsed_date = datetime.strptime(deadline, fmt)

            return date(
                meeting_date.year,
                parsed_date.month,
                parsed_date.day
            ).isoformat()

        except ValueError:
            continue

    return None