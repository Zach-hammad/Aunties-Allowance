import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.collectapi.com/gasPrice/allUsaPrice"

headers = {
    'content-type': "application/json",
    'authorization': os.getenv('COLLECTAPI_KEY')
}

response = requests.get(url, headers=headers)
data = response.json()

if data["success"]:
    prices = data["result"]
    print("Sample Gas Prices in the US:")
    for price in prices[:3]:  # First three states
        print(f"{price['name']} - Regular: ${price['gasoline']}, Diesel: ${price['diesel']}")
else:
    print("API request failed:", data)
