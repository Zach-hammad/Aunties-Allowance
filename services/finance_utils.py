# finance_utils.py
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import time

def create_link_token(client):
    request = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="AuntiesAllowanceApp",
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(
            client_user_id=str(int(time.time()))
        )
    )
    response = client.link_token_create(request)
    return response['link_token']

def exchange_public_token(client, public_token):
    request = {"public_token": public_token}
    response = client.item_public_token_exchange(request)
    return response['access_token']

def fetch_recent_transactions(client, access_token, days_back=14):
    # Fetch transactions over the last `days_back` days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options={"count": 100}
    )
    response = client.transactions_get(request)
    return response['transactions']

def calculate_food_spending(transactions):
    # Sum all grocery / dining / food-related transactions
    food_keywords = ["restaurant", "grocery", "cafe", "dining", "food"]
    total = 0
    for txn in transactions:
        if any(keyword in txn['name'].lower() for keyword in food_keywords):
            total += txn['amount']
    return total

import json
import requests
from datetime import datetime, timedelta
from config import PLAID_CLIENT_ID, PLAID_SECRET

def fetch_transactions():
    # Load access_token from saved file
    with open("scripts/access_token.json", "r") as f:
        data = json.load(f)
    access_token = data["access_token"]

    url = "https://sandbox.plaid.com/transactions/get"
    headers = {
        "Content-Type": "application/json"
    }
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    body = {
        "client_id": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "access_token": access_token,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "options": {"count": 10}
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    transactions = response.json().get("transactions", [])

    return transactions
