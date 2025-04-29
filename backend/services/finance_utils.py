# services/finance_utils.py

import time
import json
import requests
from datetime import datetime, timedelta

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest     # ← IMPORT THIS

from config import PLAID_CLIENT_ID, PLAID_SECRET

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
    response = client.item_public_token_exchange({
        "public_token": public_token
    })
    return response['access_token']

def fetch_recent_transactions(client, access_token, days_back=14):
    from datetime import datetime, timedelta
    from plaid.model.transactions_get_request import TransactionsGetRequest

    end_date   = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    req = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options={"count": 500}
    )
    res = client.transactions_get(req)
    # 🔑 Convert each model to dict
    return [txn.to_dict() for txn in res['transactions']]


def calculate_food_spending(transactions):
    # Sum all grocery / dining / food-related transactions
    food_keywords = ["restaurant", "grocery", "cafe", "dining", "food"]
    total = 0
    for txn in transactions:
        if any(k in txn['name'].lower() for k in food_keywords):
            total += txn['amount']
    return total

def fetch_transactions():
    # (existing sandbox REST call)
    with open("scripts/access_token.json", "r") as f:
        data = json.load(f)
    access_token = data["access_token"]

    url = "https://sandbox.plaid.com/transactions/get"
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

    resp = requests.post(url, json=body, headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    return resp.json().get("transactions", [])
