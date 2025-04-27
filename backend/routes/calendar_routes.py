from flask import Blueprint, request, send_file
from controllers.calendar_controller import upload_calendar_controller, download_calendar_controller
from auth.auth import requires_auth

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar/upload', methods=['POST'])
@requires_auth
def upload_calendar():
    return upload_calendar_controller()

@calendar_bp.route('/calendar/download', methods=['GET'])
@requires_auth
def download_calendar():
    return download_calendar_controller()
