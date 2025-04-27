# maps_utils.py
import googlemaps

def get_commute_distance_and_time(home, work, api_key):
    gmaps = googlemaps.Client(key=api_key)
    matrix = gmaps.distance_matrix(origins=[home], destinations=[work], mode="driving")

    distance_meters = matrix['rows'][0]['elements'][0]['distance']['value']
    duration_seconds = matrix['rows'][0]['elements'][0]['duration']['value']

    distance_miles = distance_meters / 1609.34  # meters to miles
    duration_minutes = duration_seconds / 60    # seconds to minutes

    return distance_miles, duration_minutes
