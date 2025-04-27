from flask import Blueprint, request, jsonify, send_file
from icalendar import Calendar, Event
from io import BytesIO
from datetime import datetime
import logging

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar/upload', methods=['POST'])
def upload_calendar():
    logging.debug("📥 /calendar/upload endpoint hit")

    # Check if a file is included in the request
    if 'file' not in request.files:
        logging.error("❌ No file part in the request")
        return jsonify({"error": "No calendar file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error("❌ No selected file")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Parse the .ics file
        calendar = Calendar.from_ical(file.read())
        events = []
        for component in calendar.walk():
            if component.name == "VEVENT":
                event = {
                    "summary": component.get("SUMMARY"),
                    "start": component.get("DTSTART").dt.isoformat(),
                    "end": component.get("DTEND").dt.isoformat(),
                }
                events.append(event)

        logging.debug(f"✅ Parsed events: {events}")
        return jsonify({"events": events}), 200
    except Exception as e:
        logging.error(f"❌ Error processing .ics file: {e}")
        return jsonify({"error": "Failed to process .ics file"}), 500

@calendar_bp.route('/calendar/download', methods=['GET'])
def download_calendar():
    logging.debug("📤 /calendar/download endpoint hit")

    try:
        # Create a new calendar
        calendar = Calendar()
        calendar.add('prodid', '-//Aunties Allowance//EN')
        calendar.add('version', '2.0')

        # Example tasks or events (replace with actual data)
        tasks = [
            {"summary": "Task 1", "start": "2025-04-27T10:00:00", "end": "2025-04-27T11:00:00"},
            {"summary": "Task 2", "start": "2025-04-27T14:00:00", "end": "2025-04-27T15:00:00"},
        ]

        # Add events to the calendar
        for task in tasks:
            event = Event()
            event.add('summary', task['summary'])
            event.add('dtstart', datetime.fromisoformat(task['start']))
            event.add('dtend', datetime.fromisoformat(task['end']))
            calendar.add_component(event)

        # Write the calendar to a file-like object
        ics_file = BytesIO()
        ics_file.write(calendar.to_ical())
        ics_file.seek(0)

        logging.debug("✅ Calendar file generated successfully")
        return send_file(
            ics_file,
            mimetype='text/calendar',
            as_attachment=True,
            download_name='calendar.ics'
        )
    except Exception as e:
        logging.error(f"❌ Error generating calendar file: {e}")
        return jsonify({"error": "Failed to generate calendar file"}), 500