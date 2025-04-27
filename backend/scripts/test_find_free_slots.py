# scripts/test_find_free_slots.py

from services.calendar_utils import find_free_time_slots

# Example busy slots you can pretend were parsed from an .ics
busy_slots = [
    {"start": "2025-04-26 10:00", "end": "2025-04-26 11:00", "title": "Meeting A"},
    {"start": "2025-04-26 14:00", "end": "2025-04-26 15:00", "title": "Meeting B"},
    {"start": "2025-04-26 16:30", "end": "2025-04-26 17:30", "title": "Call with client"}
]

# Run the free time finding function
free_slots = find_free_time_slots(busy_slots)

# Print the results
print("\n=== Free Time Slots ===")
for slot in free_slots:
    print(f"{slot['day']} - {slot['start']} to {slot['end']}")
