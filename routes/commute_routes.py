from flask import Blueprint, request
from controllers.commute_controller import *

commute_bp = Blueprint('commute', __name__)

@commute_bp.route('/calculate', methods=['POST'])
def calculate_commute_cost():
    data = request.json
    return calculate_commute_cost_controller(data)
