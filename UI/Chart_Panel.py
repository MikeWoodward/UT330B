# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:51:20 2016

@author: mwoodward
"""
from bokeh.models import ColumnDataSource, HBox, LinearAxis, Range1d, VBox
from bokeh.models.widgets import Button, Panel
from bokeh.plotting import figure
import pandas as pd
from UT330 import UT330


class Chart_Panel(object):

    def __init__(self, ut330):

        self.ut330 = ut330

        self.source = ColumnDataSource(data=dict(ts=[], t=[], h=[]))

        self.plot = figure(x_axis_type="datetime")
        self.plot.title = "Temperature and humidity vs. time"

        self.plot.line(x="ts",
                       y="t",
                       source=self.source,
                       color="blue",
                       legend="Temperature",
                       line_width=2)

        self.plot.xaxis.axis_label = "Timestamp"
        self.plot.yaxis.axis_label = "Temperature (C)"

        self.plot.extra_y_ranges = {"humidity": Range1d(0, 100)}

        self.plot.line(x="ts",
                       y="h",
                       source=self.source,
                       y_range_name="humidity",
                       color="green",
                       legend="Humidity",
                       line_width=2)

        self.plot.add_layout(LinearAxis(y_range_name="humidity",
                                        axis_label="Relative humidity (%)"),
                             'right')

        self.read = Button(label='Read data')
        self.delete = Button(label='Delete data')

    def _layout_(self):

        return VBox(HBox(self.read, self.delete), self.plot)

    def panel(self):

        return Panel(child=self._layout_(), title="Chart")

    def device_delete(self):

        self.ut330.delete_data()

    def device_read(self):

        self.data = self.ut330.read_data()

        df = pd.DataFrame(self.data)

        self.source.data = dict(ts=df['timestamp'],
                                t=df['temperature'],
                                h=df['humidity'])

        ymin = 10*int(df['temperature'].min()/10)
        ymax = 10*int((10+df['temperature'].max())/10)
        self.plot.y_range = Range1d(ymin, ymax)

        ymin = 10*int(df['humidity'].min()/10)
        ymax = 10*int((10+df['humidity'].max())/10)
        self.plot.extra_y_ranges = {"humidity": Range1d(ymin, ymax)}

    def callbacks(self):

        self.read.on_click(self.device_read)
        self.delete.on_click(self.device_delete)
