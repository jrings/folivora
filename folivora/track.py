import datetime
import os
import time

import api
import clize
import pandas as pd


def main(url, target_fname="/tmp/thermostat_tracker.csv", delay=60):
    """

    :param url: URL for the thermostat API
    :param target_fname: Tracker filename, where data is saved
    :param delay: Time delay [s] between polls of the thermostat state
    """
    if delay < 60:
        raise ValueError("Polling delay must be 60 seconds or more")
    if os.path.exists(target_fname):
        df = pd.read_csv(target_fname)
    else:
        df = None
    while True:
        J = api.get_state(url)
        ts = J.pop("time")
        now = datetime.datetime.now()
        dt = datetime.datetime(
            year=now.year, month=now.month, day=ts["day"], hour=ts["hour"], minute=ts["minute"], second=0)
        J["local_datetime"] = dt

        if df is None:
            df = pd.DataFrame([J])
        else:
            df = pd.concat((df, pd.DataFrame([J])))
        df.to_csv(target_fname, index=False)
        time.sleep(delay)


if __name__ == "__main__":
    clize.run(main)
