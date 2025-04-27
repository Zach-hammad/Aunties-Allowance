from flask import Blueprint, request
from controllers.tasks_controller import suggest_tasks_controller
from auth.auth import requires_auth

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/suggest', methods=['POST'])
@requires_auth
def suggest_tasks():
    return suggest_tasks_controller()
