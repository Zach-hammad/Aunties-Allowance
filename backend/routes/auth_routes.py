from flask import Blueprint
from controllers.auth_controller import *
from auth.auth import requires_auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@requires_auth
def signup():
    return signup_controller()

@auth_bp.route('/login', methods=['POST'])
@requires_auth
def login():
    return login_controller()
