import os
from dotenv import load_dotenv
import googlemaps

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

origins = ["Philadelphia, PA"]
destinations = ["New York, NY"]

matrix = gmaps.distance_matrix(origins, destinations, mode="driving")

distance_text = matrix['rows'][0]['elements'][0]['distance']['text']
duration_text = matrix['rows'][0]['elements'][0]['duration']['text']

print(f"Distance: {distance_text}")
print(f"Duration: {duration_text}")
