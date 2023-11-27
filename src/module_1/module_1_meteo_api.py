""" This is a dummy example """
# Import library
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlencode
from typing import Dict

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
def get_data_meteo_api(city: Dict[str, float]):
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": "1950-01-01",
        "end_date": "2050-12-31",
        # We consider all model
        "models": "CMCC_CM2_VHR4,FGOALS_f3_H,HiRAM_SIT_HR,MRI_AGCM3_2_S,EC_Earth3P_HR,MPI_ESM1_2_XR,NICAM16_8S",  # noqa
        "daily": VARIABLES,
    }
    # New url in the right form
    url = API_URL + urlencode(params, safe=",")
    return call_API(url)


def compute_variable_mean_and_std(data: pd.DataFrame):
    calculated_ts = data[["city", "time"]].copy()

    # Compute the mean and std of each day for each model
    for variable in VARIABLES.split(","):
        idxs = [col for col in data.columns if col.startswith(variable)]
        calculated_ts[f"{variable}_mean"] = data[idxs].mean(axis=1)
        calculated_ts[f"{variable}_std"] = data[idxs].std(axis=1)

    return calculated_ts

#Function of the code solution
def plot_timeseries(data: pd.DataFrame):
    rows = 3
    cols = 1
    fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
    axs = axs.flatten()

    data["year"] = pd.to_datetime(data["time"]).dt.year
    for k, city in enumerate(data.city.unique()):
        city_data = data.loc[data.city == city].copy()  # Create a copy of city_data
        print(city_data.head())
        for i, variable in enumerate(VARIABLES.split(",")):
            city_data[f"mid_"] = city_data[f"{variable}_mean"]
            city_data[f"upper_"] = (
                city_data[f"{variable}_mean"] + city_data[f"{variable}_std"]
            )
            city_data[f"lower_"] = (
                city_data[f"{variable}_mean"] - city_data[f"{variable}_std"]
            )

            # Plot yearly mean values
            city_data.groupby("year")["mid_"].apply("mean").plot(
                ax=axs[i], label=f"{city}", color=f"C{k}"
            )
            city_data.groupby("year")["upper_"].apply("mean").plot(
                ax=axs[i], ls="--", label="_nolegend_", color=f"C{k}"
            )
            city_data.groupby("year")["lower_"].apply("mean").plot(
                ax=axs[i], ls="--", label="_nolegend_", color=f"C{k}"
            )
            axs[i].set_title(variable)

    plt.tight_layout()
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        fancybox=True,
        shadow=True,
        ncol=5,
    )

    plt.savefig("PLOTS.png")


def main():
    # Assign the items in the list
    data_list = []
    for city, coordinates in COORDINATES.items():
        data_list.append(
            (pd.DataFrame(get_data_meteo_api(coordinates)["daily"]).assign(city=city))
        )

    data = pd.concat(data_list)
    print(data.head())

    calculated_ts = compute_variable_mean_and_std(data)
    print(calculated_ts.head())
    plot_timeseries(calculated_ts)


if __name__ == "__main__":
    main()
