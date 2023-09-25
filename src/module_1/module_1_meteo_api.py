""" This is a dummy example """
# Import library
import requests
import json
import time
import numpy as np
import matplotlib.pyplot as plt

# Define variables
API_URL = "https://climate-api.open-meteo.com/v1/climate?"

COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
}

VARIABLES = "temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean"
MODELS = "CMCC_CM2_VHR4,FGOALS_f3_H,HiRAM_SIT_HR,MRI_AGCM3_2_S,EC_Earth3P_HR,MPI_ESM1_2_XR,NICAM16_8S"


# Create functions
def call_API(url):
    cooloff = 1
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            r = requests.get(url)
            r.raise_for_status()  # HTTP ERRORS
            print("Good connection")

        except requests.exceptions.ConnectionError as e:
            print("Connection error:", e)

            if attempt < max_attempts - 1:
                print(f"Trying in {cooloff} seconds")
                time.sleep(cooloff)
                cooloff *= 2  # double the cooloff time on each iteration
                attempt += 1
                continue
            else:
                raise

        except requests.exceptions.HTTPError as e:
            print("Error HTTP:", e)
            if attempt < max_attempts - 1:
                print(f"Trying in {cooloff} seconds")
                time.sleep(cooloff)
                cooloff *= 2
                attempt += 1
            else:
                raise

        return r.json()
# Obtain data from a city from the API
def get_data_meteo_api(city, start_date, end_date):
    coordinates = COORDINATES.get(city)

    if coordinates:
        lat = coordinates["latitude"]
        long = coordinates["longitude"]

        # New request to the API
        url = f"{API_URL}latitude={lat}&longitude={long}&start_date={start_date}&end_date={end_date}&models={MODELS}&daily={VARIABLES}"
        return call_API(url)
    else:
        print("Coordinate error")
        return None

"""
def compute_average(data):
    return np.mean(data)


def compute_dispersion(data):
    return np.std(data)
"""
"""
# It is not working
def plot_results(
    city,
    temperature_average,
    temperature_dispersion,
    precipitation_average,
    precipitation_dispersion,
    soil_moisture_average,
    soil_moisture_dispersion,
):
    variables = ["T", "P", "H"]
    # Create figure and axes
    fig, gp = plt.subplots()
    x = range(len(variables))
"""

def main():
    start_date = "1951-01-01"
    end_date = "1951-12-31"
    # models = "CMCC_CM2_VHR4"

    # Go through each city in the COORDINATES list and call the function to take each data.
    for city in COORDINATES.keys():
        city_data = get_data_meteo_api(city, start_date, end_date)
        print(city_data.keys())
        daily_data = city_data["daily"]
        print(f"Datos para la ciudad de {city}:")
        print(daily_data)
        # print(city_data)
       # print("Dates of: " + city + " " + str(city_data))

        # I have errors in this part of the code because I can´t axcess to this variables (KeyError: 'temperature_2m_mean')
        #I need to check later the next code lines, It is commented because of that. I am checking some things
        """
        temperature_average = compute_average(temperature_data)
        temperature_dispersion = compute_dispersion(precipitation_data)

        precipitation_average = compute_average(precipitation_data)
        precipitation_dispersion = compute_dispersion(precipitation_data)

        soil_moisture_average = compute_average(soil_moisture_data)
        soil_moisture_dispersion = compute_dispersion(soil_moisture_data)

        print(
            "Dates of:"
            + city
            + "\nTemperature - average: "
            + temperature_average
            + "- Dispersión: "
            + temperature_dispersion
        )
        print(
            "Precipitation - average:"
            + precipitation_average
            + "- Dispersión: "
            + precipitation_dispersion
        )
        print(
            "Soil moisture - average: "
            + soil_moisture_average
            + "- Dispersión: "
            + soil_moisture_dispersion
        )
        print("\n")
    # plot_results(city, temperature_average, temperature_dispersion, precipitation_average, precipitation_dispersion, soil_moisture_average, soil_moisture_dispersion)
"""

if __name__ == "__main__":
    main()
