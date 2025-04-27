from flask import Blueprint, request
from controllers.finance_controller import create_link_token_controller, exchange_token_controller, get_transactions_controller
from auth.auth import requires_auth

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/create-link-token', methods=['GET'])
@requires_auth
def create_link_token():
    return create_link_token_controller()

@finance_bp.route('/exchange-token', methods=['POST'])
@requires_auth
def exchange_token():
    public_token = request.json.get('public_token')
    return exchange_token_controller(public_token)

@finance_bp.route('/transactions', methods=['GET'])
@requires_auth
def get_transactions_route():
    return get_transactions_controller()