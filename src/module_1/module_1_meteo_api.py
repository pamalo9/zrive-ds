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
def call_API_aux(API):
    #Call the api
    r = requests.get(API_URL)
    #Check the connections
    if r.status_code == 200:
        print("Connected to the API")  #correct connection
    else:
        print("Number Error: " + str(r.status_code) + "\nType: " + r.text) #Error number and explanation
    
    #Check rate limit error and make cool off
    for _ in range(3):
        if r.status_code == 429:
            print("ERROR: " + str(r.status_code) + " \nType: Max rate limit, you need to wait a bit ")
            time.sleep(10)
        continue

def get_data_meteo_api(city):
    return None


def compute():
    return None

def plot_results():
    return None


def main():
    call_API_aux(API_URL)
    # raise NotImplementedError
    
    

if __name__ == "__main__":
    main()
