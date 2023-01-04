#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 15:25:51 05-Jan-2020

Author: Mike Woodward

This code is licensed under the MIT license
"""


# %%---------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
from bokeh.models import (Button, Div, TabPanel)
from bokeh.layouts import column, row
import pandas as pd


# %%---------------------------------------------------------------------------
# ReadSave
# -----------------------------------------------------------------------------
class ReadSave():
    """Reads temperature and humidity data from the 330B and saves the data to
    disk."""

    INSTRUCTIONS = ("""To use this tab, press the buttons in the """
                    """following order: <br>"""
                    """<ol>"""
                    """    <li>"""
                    """    Connect to UT330B - this button makes the """
                    """    connection to the device"""
                    """    </li>"""
                    """    <li>"""
                    """    Read UT330B data - this button reads the """
                    """    temperature and humidity data from the device"""
                    """    </li>"""
                    """    <li>"""
                    """    Write to disk - this button writes the """
                    """    temperature and humidity data read from the """
                    """    device to disk, the file name is the most """
                    """    recent date and time in the data"""
                    """    </li>"""
                    """    <li>"""
                    """    Erase UT330B data - this button erases the """
                    """    temperature and humidity data from the device """
                    """    which makes room for more data."""
                    """    </li>"""
                    """    <li>"""
                    """    Disconnect from UT330B - this button breaks the """
                    """    connection to the device"""
                    """    </li>"""
                    """</ol>""")

    # %%
    def __init__(self, controller):
        """Method sets up object.  First part of two-part initialization."""

        self.controller = controller

        # Instructions header
        self.instructions_header =\
            Div(text="""<span style='font-weight:bold'>"""
                     """How to use this tab</span>""")
        # Provides instructions on how to use the tab.
        self.instructions = Div(text=self.INSTRUCTIONS)
        # Widgets header
        self.widgets_header =\
            Div(text="""<span style='font-weight:bold'>"""
                     """Read, save, erase controls</span>""")
        # Connects to the UT330B device
        self.connect =\
            Button(label="""Connect to UT330B""", button_type="""success""")
        # Reads in the data from the UT330B device
        self.read_ut330b =\
            Button(label="""Read UT330B data""", button_type="""success""")
        # Writes temperature and humidity data to disk.
        self.write_to_disk =\
            Button(label="""Write to disk""", button_type="""success""")
        # Removes all UT33)B temperature and humidity data from device.
        self.erase_data =\
            Button(label="""Erase UT330B data""", button_type="""success""")
        # Disconnects from the UT330B device.
        self.disconnect =\
            Button(label="""Disconnect from UT330B""",
                   button_type="""success""")
        # Status header
        self.status_header =\
            Div(text="""<span style='font-weight:bold'>"""
                     """Connection status</span>""")
        # Status information on UT330B.
        self.status = Div(text=self.controller.status)
        # Layout widget and figures
        self.layout =\
            column(children=[self.instructions_header,
                             self.instructions,
                             self.status_header,
                             self.status,   
                             self.widgets_header,
                             row(self.connect, self.read_ut330b,
                                 self.write_to_disk, self.erase_data,
                                 self.disconnect)],
                   sizing_mode="stretch_both")
        self.panel = TabPanel(child=self.layout,
                           title='Read & save')

    # %%
    def setup(self):
        """Method sets up object. Second part of two-part initialization."""

        self.connect.on_click(self.callback_connect)
        self.read_ut330b.on_click(self.callback_read_ut330b)
        self.write_to_disk.on_click(self.callback_write_to_disk)
        self.erase_data.on_click(self.callback_erase_data)
        self.disconnect.on_click(self.callback_disconnect)

    # %%
    def update(self):
        """Method updates object."""
        self.status.text = self.controller.status

    # %%
    def callback_connect(self):
        """Callback method for Connect"""
        self.controller.connect()

    # %%
    def callback_read_ut330b(self):
        """Callback method for Read UT330B"""
        self.controller.read_data()

    # %%
    def callback_write_to_disk(self):
        """Callback method for Write to disk"""

        df = pd.DataFrame(self.controller.device_data)

        if df.empty:
            self.status.text = ("Can't write data to UT330B because "
                                "there's no data to write.")
            return

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        time_str = df['Timestamp'].max().strftime("%Y%m%d_%H%M%S")

        # Check folder exists, if not, create it        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.dirname(dir_path)
        folder = os.path.join(dir_path, 'data')
        if not os.path.isdir(folder):
            os.mkdir(folder)

        data_file = \
            os.path.join(folder,
                         'UT330_data_{0}.csv'.format(time_str))

        df.to_csv(data_file, index=False)

        self.status.text = "Wrote data to file {0}.".format(data_file)

    # %%
    def callback_erase_data(self):
        """Callback method for Erase data"""
        self.controller.erase()

    # %%
    def callback_disconnect(self):
        """Callback method for Disconnect"""
        self.controller.disconnect()
