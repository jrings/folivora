import datetime
import os
import time

import api
import clize
import numpy as np
import pandas as pd
import pywapi
from sigtools.modifiers import autokwoargs


def poll_current_weather(zip_):
    if isinstance(zip_, int):
        zip_ = str(zip_)
    weather = pywapi.get_weather_from_weather_com(zip_, units="imperial")
    
    return weather["current_conditions"]


@autokwoargs
def main(url, zip_, target_fname="/tmp/thermostat_tracker.csv", delay=60):
    """

    :param url: URL for the thermostat API
    :param target_fname: Tracker filename, where data is saved
    :param delay: Time delay [s] between polls of the thermostat state
    :param zip_: Zip code of thermostat - to add weather data
    """
    if delay < 60:
        raise ValueError("Polling delay must be 60 seconds or more")
    if os.path.exists(target_fname):
        df = pd.read_csv(target_fname)
    else:
        df = None
    while True:
        J = get_current_state(url, zip_)
        df = _append_to_dataframe(J, df)

        df.to_csv(target_fname, index=False)
        time.sleep(delay)


def get_current_state(url, zip):
    J = api.get_state(url)
    ts = J.pop("time")
    now = datetime.datetime.now()
    dt = datetime.datetime(
        year=now.year, month=now.month, day=now.day, hour=ts["hour"], minute=ts["minute"], second=0)
    utcnow = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    J["dt_local"] = dt
    J["read_dt_utc"] = utcnow
    W = poll_current_weather(zip)
    J["t_out"] = W["temperature"]
    J["weather"] = W["text"]
    J["humidity"] = W["humidity"]
    return J


def _append_to_dataframe(J, df):
    if df is None:
        df = pd.DataFrame([J])
    else:
        if not set(df.columns) == set(list(J.keys())):
            # New keys?
            new_columns = [c for c in J if c not in df.columns]
            for col in new_columns:
                df[col] = np.nan
        df = pd.concat((df, pd.DataFrame([J])))
    return df.drop_duplicates("dt_local")


if __name__ == "__main__":
    clize.run(main)
