import os
from ics import Calendar
from datetime import datetime, timedelta
import pytz

WORK_DAY_START = "08:00"
WORK_DAY_END = "22:00"
MIN_FREE_MINUTES = 30

def save_and_parse_calendar(file):
    save_path = os.path.join('data', 'uploaded_calendars', file.filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file.save(save_path)

    with open(save_path, 'r') as f:
        calendar = Calendar(f.read())

    busy_slots = []
    for event in calendar.events:
        busy_slots.append({
            "start": event.begin.to('utc').format('YYYY-MM-DD HH:mm'),
            "end": event.end.to('utc').format('YYYY-MM-DD HH:mm'),
            "title": event.name
        })

    return busy_slots

def find_free_time_slots(busy_slots, timezone_str):
    timezone = pytz.timezone(timezone_str)
    
    busy_by_day = {}
    for slot in busy_slots:
        start_dt = datetime.strptime(slot["start"], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.utc).astimezone(timezone)
        end_dt = datetime.strptime(slot["end"], "%Y-%m-%d %H:%M").replace(tzinfo=pytz.utc).astimezone(timezone)
        day = start_dt.date()

        if day not in busy_by_day:
            busy_by_day[day] = []
        busy_by_day[day].append((start_dt, end_dt))

    free_slots = []
    for day, slots in busy_by_day.items():
        slots.sort()

        day_start = timezone.localize(datetime.strptime(f"{day} {WORK_DAY_START}", "%Y-%m-%d %H:%M"))
        day_end = timezone.localize(datetime.strptime(f"{day} {WORK_DAY_END}", "%Y-%m-%d %H:%M"))

        if (slots[0][0] - day_start).total_seconds() / 60 >= MIN_FREE_MINUTES:
            free_slots.append({
                "day": str(day),
                "start": WORK_DAY_START,
                "end": slots[0][0].strftime("%H:%M")
            })

        for i in range(len(slots) - 1):
            gap_start = slots[i][1]
            gap_end = slots[i+1][0]
            if (gap_end - gap_start).total_seconds() / 60 >= MIN_FREE_MINUTES:
                free_slots.append({
                    "day": str(day),
                    "start": gap_start.strftime("%H:%M"),
                    "end": gap_end.strftime("%H:%M")
                })

        if (day_end - slots[-1][1]).total_seconds() / 60 >= MIN_FREE_MINUTES:
            free_slots.append({
                "day": str(day),
                "start": slots[-1][1].strftime("%H:%M"),
                "end": WORK_DAY_END
            })

    return free_slots
