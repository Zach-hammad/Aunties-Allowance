# scripts/test_schedule_tasks.py


from services.scheduler_utils import schedule_tasks_into_free_slots

tasks = ["meal_prep", "transit", "carpool"]

free_slots = [
    {"day": "2025-04-26", "start": "08:00", "end": "09:30"},
    {"day": "2025-04-26", "start": "14:00", "end": "18:00"},
    {"day": "2025-04-27", "start": "07:00", "end": "09:00"}
]

scheduled = schedule_tasks_into_free_slots(tasks, free_slots)

print("\n=== Scheduled Tasks ===")
for task in scheduled:
    print(f"{task['task']} on {task['scheduled_day']} from {task['start_time']} to {task['end_time']}")
