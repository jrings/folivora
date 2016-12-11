import glob

import matplotlib

matplotlib.use("Agg")
import bokeh.plotting as plt
from bokeh.embed import file_html
from bokeh.resources import CDN
import cherrypy
import pandas as pd
import numpy as np


class Main(object):
    @cherrypy.expose
    def index(self):
        df = pd.concat([pd.read_csv(fname) for fname in glob.glob("/home/joerg/data/thermostat*.csv")])
        df["dt_local"] = pd.to_datetime(df.dt_local)
        D = df.copy()
        O = df.copy()
        S = df.copy()
        D["type"] = "in"
        O["type"] = "out"
        S["type"] = "setpoint"
        O["temp"] = O["t_out"]
        S["temp"] = [h if np.isfinite(h) else c for c, h in zip(S.get("t_cool", [np.nan] * S.shape[0]),
                                                                S.get("t_heat", [np.nan] * S.shape[0]))]

        df = pd.concat((D, O, S))
        p = plt.figure(
            tools="pan,box_zoom,reset,save",
            x_axis_label='Datetime', y_axis_label='Temperature',
            x_axis_type="datetime",
            plot_width=1000, plot_height=600,
            y_range=(0, df.temp.max() + 10)
        )
        p.line(D.dt_local, D.temp, color="orange")
        p.line(O.dt_local, O.temp, color="darkgreen")
        p.line(S.dt_local, S.temp, color="hotpink")

        return file_html(p, CDN, "my plot")


if __name__ == '__main__':
    cherrypy.quickstart(Main())
