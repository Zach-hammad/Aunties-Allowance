# gas_utils.py
import requests

def fetch_gas_price(city, api_key):
    # Call CollectAPI to get gas prices
    url = "https://api.collectapi.com/gasPrice/allUsaPrice"
    headers = {
        'content-type': "application/json",
        'authorization': api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    for result in data['result']:
        if city.lower() in result['name'].lower():
            return float(result['gasoline'])  # Assuming gasoline type
    return None

def fetch_vehicle_mpg(make, model, year):
    # Fetch vehicle MPG from OpenDataSoft API
    url = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=all-vehicles-model&q={make}+{model}&refine.year={year}"
    response = requests.get(url)
    data = response.json()

    if data['nhits'] > 0:
        record = data['records'][0]['fields']
        return record.get('comb08') or record.get('city08')  # Combined or City MPG
    return None

def calculate_weekly_gas_cost(distance_per_day, commute_days, mpg, gas_price):
    # Estimate weekly gas spending
    total_miles = distance_per_day * 2 * commute_days
    gallons_needed = total_miles / mpg
    total_gas_cost = gallons_needed * gas_price
    return total_gas_cost
