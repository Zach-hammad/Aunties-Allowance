from flask import request, jsonify
from services.tasks_utils import generate_task_schedule
from services.calendar_export_utils import export_schedule_to_ics
import pytz


DEFAULT_TIMEZONE = "America/New_York"
def suggest_tasks_controller():
    busy_slots = request.json.get("busy_slots", [])
    user_behavior = request.json.get("user_behavior")
    timezone = request.json.get("timezone", DEFAULT_TIMEZONE)

    if not busy_slots or not user_behavior or not timezone:
        return jsonify({"error": "Missing data"}), 400

    # 🛡️ Validate timezone
    if timezone not in pytz.all_timezones:
        return jsonify({"error": f"Invalid timezone: {timezone}"}), 400

    schedule = generate_task_schedule(busy_slots, user_behavior, timezone)

    ics_filepath = export_schedule_to_ics(schedule, timezone)

    return jsonify({
        "scheduled_tasks": schedule,
        "ics_file_path": ics_filepath
    })
