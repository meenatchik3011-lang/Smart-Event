
from datetime import datetime, timezone

from app.models import Event


def update_event_status(event: Event) -> None:
    """
    Update an event's status based on its start and end dates.

    Status rules:
    - UPCOMING: Current time is before the event start.
    - ONGOING: Current time is at or after the start but before the end.
    - COMPLETED: Current time is at or after the event end.
    - CANCELLED: Never change the status.
    """

    # Never change a cancelled event.
    if event.event_status == "CANCELLED":
        return

    # Use naive UTC to match the existing database datetime fields.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Check the event start date.
    if now < event.event_date:
        event.event_status = "UPCOMING"

    # Support older events that do not have an end date.
    elif event.event_end_date is None:
        event.event_status = "ONGOING"

    # Check whether the event is still in progress.
    elif now < event.event_end_date:
        event.event_status = "ONGOING"

    # The event has ended.
    else:
        event.event_status = "COMPLETED"
