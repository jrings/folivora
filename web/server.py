import matplotlib

matplotlib.use("Agg")
from altair import *
import cherrypy
import pandas as pd
import numpy as np


class Main(object):
    @cherrypy.expose
    def index(self):
        df = pd.read_csv("/home/joerg/data/thermostat.csv")
        df["t_in"] = [h if np.isfinite(h) else c
                      for h, c in
                      zip(df.get("t_heat", [np.nan] * df.shape[0]), df.get("t_cool", [np.nan] * df.shape[0]))]
        D = df.copy()
        O = df.copy()
        D["type"] = "in"
        O["type"] = "out"
        D["temp"] = D["t_in"]
        O["temp"] = D["t_out"]
        df = pd.concat((D, O))
        chart = Chart(df
                      ).mark_line().encode(
            x='dt_local:T',
            y='temp:Q',
            color="type:O"
        )
        return chart.to_html()


if __name__ == '__main__':
    cherrypy.quickstart(Main())
