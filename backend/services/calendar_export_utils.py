from ics import Calendar, Event
from datetime import datetime
import pytz

def export_schedule_to_ics(scheduled_tasks, timezone_str, filename="weekly_plan.ics"):
    calendar = Calendar()
    timezone = pytz.timezone(timezone_str)

    for task in scheduled_tasks:
        event = Event()
        event.name = task['task'].replace("_", " ").title()

        start_dt = timezone.localize(datetime.strptime(f"{task['scheduled_day']} {task['start_time']}", "%Y-%m-%d %H:%M"))
        end_dt = timezone.localize(datetime.strptime(f"{task['scheduled_day']} {task['end_time']}", "%Y-%m-%d %H:%M"))

        event.begin = start_dt
        event.end = end_dt
        event.description = "Scheduled by SavingSpree"

        calendar.events.add(event)

    with open(f"data/{filename}", "w") as f:
        f.writelines(calendar)

    return f"data/{filename}"
