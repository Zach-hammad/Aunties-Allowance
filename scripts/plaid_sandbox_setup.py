# scripts/plaid_sandbox_setup.py

import requests
import os
import json
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")

def create_sandbox_public_token():
    """Create a sandbox public_token"""
    url = "https://sandbox.plaid.com/sandbox/public_token/create"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "client_id": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "institution_id": "ins_109508",  # Sandbox Chase Bank
        "initial_products": ["transactions"]
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    public_token = response.json().get("public_token")
    print(f"[SUCCESS] Public Token Created: {public_token}")
    return public_token

def exchange_public_token(public_token):
    """Exchange public_token for access_token"""
    url = "https://sandbox.plaid.com/item/public_token/exchange"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "client_id": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "public_token": public_token
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    print(f"[SUCCESS] Access Token Retrieved: {access_token}")
    return access_token

def save_access_token(access_token):
    """Save access_token to local file"""
    with open("scripts/access_token.json", "w") as f:
        json.dump({"access_token": access_token}, f, indent=4)
    print(f"[SUCCESS] Access Token saved to scripts/access_token.json")


  

def get_transactions(access_token, retries=5, delay_seconds=10):
    """Fetch fake transactions with retries"""
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
        "options": {"count": 5}
    }

    for attempt in range(retries):
        response = requests.post(url, json=body, headers=headers)
        data = response.json()

        if "transactions" in data:
            print("\n=== Recent Transactions ===")
            for txn in data["transactions"]:
                print(f"{txn['date']} - {txn['name']} - ${txn['amount']}")
            print("============================")
            return

        elif data.get("error_code") == "PRODUCT_NOT_READY":
            print(f"[WAIT] Product not ready yet. Retry {attempt+1}/{retries} after {delay_seconds} seconds...")
            time.sleep(delay_seconds)
        else:
            print(f"[ERROR] Unexpected error: {data}")
            break

    print("[FAILED] Transactions not ready after retries.")

if __name__ == "__main__":
    try:
        public_token = create_sandbox_public_token()
        access_token = exchange_public_token(public_token)
        save_access_token(access_token)
        get_transactions(access_token)
    except Exception as e:
        print(f"[ERROR] {e}")
