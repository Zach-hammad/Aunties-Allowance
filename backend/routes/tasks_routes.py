from flask import Blueprint, request
from controllers.tasks_controller import suggest_tasks_controller
from auth.auth import requires_auth
import logging

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/suggest', methods=['POST'])
def suggest_tasks():
    logging.debug("📥 /tasks/suggest endpoint hit")
    logging.debug(f"Request data: {request.json}")
    return suggest_tasks_controller()
