from datetime import datetime, timedelta
import pytz

TASK_DEFAULTS = {
    "meal_prep": {"duration_minutes": 120, "preferred_start": "14:00", "preferred_end": "17:00"},
    "transit": {"duration_minutes": 30, "preferred_start": "07:00", "preferred_end": "09:00"},
    "carpool": {"duration_minutes": 30, "preferred_start": "07:00", "preferred_end": "09:00"},
}

def schedule_tasks_into_free_slots(tasks, free_slots, timezone_str):
    timezone = pytz.timezone(timezone_str)
    scheduled_tasks = []

    for task_name in tasks:
        task_info = TASK_DEFAULTS[task_name]
        task_duration = timedelta(minutes=task_info["duration_minutes"])

        for slot in free_slots:
            slot_start_dt = timezone.localize(datetime.strptime(f"{slot['day']} {slot['start']}", "%Y-%m-%d %H:%M"))
            slot_end_dt = timezone.localize(datetime.strptime(f"{slot['day']} {slot['end']}", "%Y-%m-%d %H:%M"))

            preferred_start = timezone.localize(datetime.strptime(f"{slot['day']} {task_info['preferred_start']}", "%Y-%m-%d %H:%M"))
            preferred_end = timezone.localize(datetime.strptime(f"{slot['day']} {task_info['preferred_end']}", "%Y-%m-%d %H:%M"))

            latest_start = max(slot_start_dt, preferred_start)
            earliest_end = min(slot_end_dt, preferred_end)

            if (earliest_end - latest_start) >= task_duration:
                scheduled_tasks.append({
                    "task": task_name,
                    "scheduled_day": str(latest_start.date()),
                    "start_time": latest_start.strftime("%H:%M"),
                    "end_time": (latest_start + task_duration).strftime("%H:%M")
                })

                slot["start"] = (latest_start + task_duration).strftime("%H:%M")
                break

    return scheduled_tasks
