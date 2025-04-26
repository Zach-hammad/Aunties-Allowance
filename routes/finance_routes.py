from flask import Blueprint, request
from controllers.finance_controller import create_link_token_controller, exchange_token_controller, get_transactions_controller

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/create-link-token', methods=['GET'])
def create_link_token():
    return create_link_token_controller()

@finance_bp.route('/exchange-token', methods=['POST'])
def exchange_token():
    public_token = request.json.get('public_token')
    return exchange_token_controller(public_token)

@finance_bp.route('/transactions', methods=['GET'])
def get_transactions_route():
    return get_transactions_controller()