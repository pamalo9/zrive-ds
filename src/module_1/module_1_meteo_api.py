""" This is a dummy example """
# Import library
import requests
import json
import time

# Define variables
API_URL = "https://climate-api.open-meteo.com/v1/climate?"

COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
}

VARIABLES = "temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean"

# Create functions
def call_API_aux(url):
    r = requests.get(url)

# Check the connections
    if r.status_code == 200:
        print("Connection without errors") 
        return r.json()  # correct connection

    else:
        print("Number Error: " + str(r.status_code) + "\nType: " + r.text)  # Error explanation

# Check rate limit error and make cool off(Wait 3 seconds)
    for _ in range(3):
        if r.status_code == 429:
            print("ERROR: " + str(r.status_code) + " \nType: Max rate limit, you need to wait a bit ")
            time.sleep(10)
        continue

# Obtain data from a city from the API
def get_data_meteo_api(city, start_date, end_date, temporal_res):
    coordinates = COORDINATES.get(city)

    if coordinates:
        lat = coordinates["latitude"]
        long = coordinates["longitude"]
        #New request to the API
        url = f"{API_URL}latitude={lat}&longitude={long}&temporal_resolution={temporal_res}&variables={VARIABLES}&start_date={start_date}&end_date={end_date}"
        return call_API_aux(url)
    
    else:
        print("Coordinate error")
        return None


    

def compute():
    return None


def plot_results():
    return None


def main():

# raise NotImplementedError
    temporal_res = "year"
    start_date = "1950-01-01"
    end_date = "2050-12-31"

# Go through each city in the COORDINATES list and call the function to take each data.
    for city in COORDINATES.keys():
        city_data = get_data_meteo_api(city, start_date, end_date, temporal_res)
        print("Dates of: " + city + " "+ str(city_data))


if __name__ == "__main__":
    main()
