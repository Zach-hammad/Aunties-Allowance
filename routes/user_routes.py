from flask import Blueprint
from controllers.user_controller import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/setup', methods=['POST'])
def setup_user():
    return setup_user_controller()
