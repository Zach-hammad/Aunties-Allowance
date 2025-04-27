from flask import Blueprint
from controllers.user_controller import *
from auth.auth import requires_auth

user_bp = Blueprint('user', __name__)

@user_bp.route('/setup', methods=['POST'])
@requires_auth
def setup_user():
    return setup_user_controller()
