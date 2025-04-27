import requests

vehicle_make = "Toyota"
vehicle_model = "Corolla"
year = "2020"

url = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=all-vehicles-model&q={vehicle_make}+{vehicle_model}&refine.year={year}"

response = requests.get(url)
data = response.json()

if data["nhits"] > 0:
    record = data["records"][0]["fields"]
    print(f"{year} {vehicle_make} {vehicle_model}")
    print(f"City MPG: {record.get('city08', 'N/A')}")
    print(f"Highway MPG: {record.get('highway08', 'N/A')}")
else:
    print("No data found for the specified vehicle.")
