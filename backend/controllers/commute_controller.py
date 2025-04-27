from services.gas_utils import calculate_weekly_gas_cost
from services.maps_utils import get_commute_distance_and_time
from services.gas_utils import fetch_vehicle_mpg, fetch_gas_price
from config import GOOGLE_MAPS_API_KEY, COLLECTAPI_KEY
from flask import jsonify

def calculate_commute_cost_controller(data):
    home = data.get('home')
    work = data.get('work')
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    commute_days = data.get('commute_days', 5)

    distance, _ = get_commute_distance_and_time(home, work, GOOGLE_MAPS_API_KEY)
    mpg = fetch_vehicle_mpg(make, model, year)
    gas_price = fetch_gas_price(home.split(",")[-2].strip(), COLLECTAPI_KEY)  # Rough city grab
    weekly_cost = calculate_weekly_gas_cost(distance, commute_days, mpg, gas_price)

    return jsonify({"weekly_commute_cost": weekly_cost})
