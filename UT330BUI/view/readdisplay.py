#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 15:54:55 05-Jan-2020

Author: Mike Woodward

This code is licensed under the MIT license
"""


# %%---------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from bokeh.models import (Div, FileInput, TabPanel)
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, LinearAxis, Range1d

import pandas as pd
from io import BytesIO
import base64

# %%---------------------------------------------------------------------------
# ReadDisplay
# -----------------------------------------------------------------------------
class ReadDisplay():
    """Reads data saved to file into the system and displays it."""

    # %%
    def __init__(self, controller):
        """Method sets up object.  First part of two-part initialization."""

        self.controller = controller

        # Header for section to get file
        self.file_header =\
            Div(text="""<span style='font-weight:bold'>"""
                     """Choose the file to display</span>""",
                     sizing_mode='stretch_width')

        # Selects the data file to read into the system
        self.select_file = FileInput(accept=".csv",
                                     sizing_mode='stretch_width')
        
        # Shows summary and status for data read in.
        self.status = Div(text="""No file connected""",
                          sizing_mode='stretch_width')

        # Chart to show temperature and/or humidity.
        self.temphumidity = figure(x_axis_type='datetime',
                                   title="Humidity & temperature by datetime",
                                   x_axis_label='Datetime',
                                   y_axis_label='Temperature (C)')

        df = pd.DataFrame(
            {'Timestamp': [pd.to_datetime('4/12/2016  8:15:33 AM')],
             'Temperature (C)': [25.0],
             'Relative humidity (%)': [40.0]})

        self.cds = ColumnDataSource(df)

        self.temphumidity.line(x='Timestamp',
                               y='Temperature (C)',
                               line_color='red',
                               legend_label='Temperature (C)',
                               line_width=2,
                               line_alpha=0.5,
                               source=self.cds)

        self.temphumidity.extra_y_ranges = \
            {"humidity": Range1d(start=0, end=100)}

        self.temphumidity.add_layout(
            LinearAxis(y_range_name="humidity",
                       axis_label='Humidity (%)'), 'right')

        self.temphumidity.line(x='Timestamp',
                               y='Relative humidity (%)',
                               legend_label='Relative humidity (%)',
                               line_color='blue',
                               line_width=2,
                               line_alpha=0.5,
                               source=self.cds,
                               y_range_name="humidity")

        self.temphumidity.legend.click_policy = "hide"

        self.temphumidity.title.text_font_size = '20px'
        self.temphumidity.xaxis.axis_label_text_font_size = '15px'
        self.temphumidity.xaxis.major_label_text_font_size = '15px'
        self.temphumidity.yaxis.axis_label_text_font_size = '15px'
        self.temphumidity.yaxis.major_label_text_font_size = '15px'

        # Layout
        self.layout = row(
            children=[column(children=[self.file_header,
                                       self.select_file,
                                       self.status],
                             sizing_mode='fixed',
                             width=250, height=80),
                      column(self.temphumidity, sizing_mode='stretch_both')],
            sizing_mode='stretch_both')
        self.panel = TabPanel(child=self.layout, title='Read & display')

    # %%
    def setup(self):
        """Method sets up object. Second part of two-part initialization."""

        self.select_file.on_change("value", self.callback_select_file)

    # %%
    def update(self):
        """Method updates object."""

        pass

    # %%
    def callback_select_file(self, attrname, old, new):
        """Callback method for select file"""

        self.status.text = 'Reading in the data file....'

        # Convert the data to a Pandas dataframe
        convert = BytesIO(base64.b64decode(self.select_file.value))
        df = pd.read_csv(convert)

        # Check the Pandas dataframe has the correct fields
        if set(df.columns) != set(['Timestamp',
                                   'Temperature (C)',
                                   'Relative humidity (%)',
                                   'Pressure (Pa)']):
            self.status.text = ("""The file {0} has the columns {1} """
                                """when it should have the columns {2} """
                                .format(self.select_file.filename,
                                        set(df.columns),
                                        set(['Timestamp',
                                             'Temperature (C)',
                                             'Relative humidity (%)',
                                             'Pressure (Pa)'])))
            return

        # Make sure the data types are correct
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        self.cds.data = {'Timestamp': df['Timestamp'],
                         'Temperature (C)': df['Temperature (C)'],
                         'Relative humidity (%)': df['Relative humidity (%)']}

        self.status.text = 'Read in the data file correctly.'
