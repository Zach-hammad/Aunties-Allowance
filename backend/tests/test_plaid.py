import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
client_id = os.getenv("PLAID_CLIENT_ID")
secret = os.getenv("PLAID_SECRET")
environment = os.getenv("PLAID_ENV", "sandbox")

# Configure the Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': client_id,
        'secret': secret,
    }
)

# Create an API client
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import time

# Create a link token request
request = LinkTokenCreateRequest(
    products=[Products("transactions")],
    client_name="Your App Name",
    country_codes=[CountryCode('US')],
    language='en',
    user=LinkTokenCreateRequestUser(
        client_user_id=str(time.time())
    )
)

# Create the link token
response = client.link_token_create(request)
print("Link Token:", response['link_token'])
