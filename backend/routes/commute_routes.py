from flask import Blueprint, request
from controllers.commute_controller import *
from auth.auth import requires_auth

commute_bp = Blueprint('commute', __name__)

@commute_bp.route('/calculate', methods=['POST'])
@requires_auth
def calculate_commute_cost():
    data = request.json
    return calculate_commute_cost_controller(data)
