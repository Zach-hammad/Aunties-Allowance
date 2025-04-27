from services.finance_utils import create_link_token, exchange_public_token
from config import PLAID_CLIENT
from flask import jsonify

def create_link_token_controller():
    # Correct: Pass the client, get the token
    token = create_link_token(PLAID_CLIENT)
    return jsonify({"link_token": token})

def exchange_token_controller(public_token):
    access_token = exchange_public_token(PLAID_CLIENT, public_token)
    return jsonify({"access_token": access_token})

from services.finance_utils import fetch_transactions

def get_transactions_controller():
    transactions = fetch_transactions()
    return jsonify({"transactions": transactions})

