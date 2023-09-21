""" This is a dummy example """
# Import library
import requests
import json

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
    data = requests.get(API)
    if data.status_code == 200:
        data = data.json()
        print("data")

    else:
        print("ERROR")

    return None


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
