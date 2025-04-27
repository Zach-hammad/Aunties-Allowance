from flask import request, jsonify, send_file
from services.calendar_utils import save_and_parse_calendar

def upload_calendar_controller():
    if 'calendar' not in request.files:
        return jsonify({"error": "No calendar file uploaded"}), 400

    file = request.files['calendar']
    busy_slots = save_and_parse_calendar(file)
    return jsonify({"message": "Calendar uploaded successfully", "busy_slots": busy_slots})

def download_calendar_controller():
    filepath = "data/weekly_plan.ics"  # default filename we save schedules as
    try:
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "No weekly plan generated yet"}), 404
