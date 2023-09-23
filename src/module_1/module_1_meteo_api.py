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
def call_API_aux(url): 
    r = requests.get(url)

    # Check the connections
    if r.status_code == 200:
        print("Connection without errors")
        return r.json()  # correct connection

    else:
        print(
            "Number Error: " + str(r.status_code) + "\nType: " + r.text
        )  # Error explanation

    # Check rate limit error and make cool off(Wait 3 seconds)
    for _ in range(3):
        if r.status_code == 429:
            print(
                "ERROR: "
                + str(r.status_code)
                + " \nType: Max rate limit, you need to wait a bit "
            )
            time.sleep(10)
            r = requests.get(url)
        continue
    return None


# Obtain data from a city from the API
def get_data_meteo_api(city, start_date, end_date, temporal_resolution):
    coordinates = COORDINATES.get(city)

    if coordinates:
        lat = coordinates["latitude"]
        long = coordinates["longitude"]

        # New request to the API
        url = f"{API_URL}latitude={lat}&longitude={long}&start_date={start_date}&end_date={end_date}&models={MODELS}&temporal_resolution={temporal_resolution}&daily={VARIABLES}"
        return call_API_aux(url)
    else:
        print("Coordinate error")
        return None


def compute_average(data):
    return np.mean(data)


def compute_dispersion(data):
    return np.std(data)


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


def main():
    # raise NotImplementedError
    temporal_resolution = "year"
    start_date = "1950-01-01"
    end_date = "1951-12-31"
    # models = "CMCC_CM2_VHR4"

    # Go through each city in the COORDINATES list and call the function to take each data.
    for city in COORDINATES.keys():
        city_data = get_data_meteo_api(city, start_date, end_date, temporal_resolution)

        # print(city_data)
        print("Dates of: " + city + " " + str(city_data))

        # I have errors in this part of the code because I can´t axcess to this variables (KeyError: 'temperature_2m_mean')
        temperature_data = city_data["temperature_2m_mean"]
        precipitation_data = city_data["precipitation_sum"]
        soil_moisture_data = city_data["soil_moisture_0_to_10cm_mean"]

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


if __name__ == "__main__":
    main()
