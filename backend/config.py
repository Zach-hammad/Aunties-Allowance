# config.py
import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api

load_dotenv()

# Env vars
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Google and Gas APIs
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
COLLECTAPI_KEY = os.getenv("COLLECTAPI_KEY")

# Plaid Client Setup
plaid_configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENV == "sandbox" else plaid.Environment.Production,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)
plaid_api_client = plaid.ApiClient(plaid_configuration)
PLAID_CLIENT = plaid_api.PlaidApi(plaid_api_client)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_IDENTIFIER = os.getenv("API_IDENTIFIER")
ALGORITHMS = os.getenv("ALGORITHMS").split(",")