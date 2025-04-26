from flask import Blueprint
from controllers.auth_controller import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    return signup_controller()

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_controller()
