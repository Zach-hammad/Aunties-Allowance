from flask import request, jsonify, send_file
from services.calendar_utils import save_and_parse_calendar
import os

def upload_calendar_controller():
    if 'calendar' not in request.files:
        return jsonify({"error": "No calendar file uploaded"}), 400
    
    file = request.files['calendar']
    
    # Check if file is empty
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check file extension
    if not file.filename.lower().endswith('.ics'):
        return jsonify({"error": "Only .ics files are supported"}), 400
    
    try:
        busy_slots = save_and_parse_calendar(file)
        return jsonify({
            "message": "Calendar uploaded successfully", 
            "busy_slots": busy_slots
        })
    except Exception as e:
        return jsonify({"error": f"Error processing calendar: {str(e)}"}), 500

def download_calendar_controller():
    filepath = "data/weekly_plan.ics"
    
    # Check if directory exists, create if not
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        return send_file(filepath, as_attachment=True, download_name="weekly_plan.ics")
    except FileNotFoundError:
        return jsonify({"error": "No weekly plan generated yet"}), 404