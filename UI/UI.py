#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:20:49 2017

@author: mikewoodward

This should probably be broken up into seperate objects, one for each
tab. The connect and discionnect buttions are similar, so they should
all probably map to the same functions.

"""

# =============================================================================
# Imports
# =============================================================================
from bokeh.client import push_session
from bokeh.document import Document
from bokeh.layouts import column, layout, row, widgetbox
from bokeh.models import ColumnDataSource, LinearAxis, Range1d
from bokeh.models.widgets import (Button, CheckboxGroup, Div,
                                  Panel, Select,
                                  Tabs, TextInput)
from bokeh.plotting import figure

import datetime

import glob
from math import ceil
import os.path
import pandas as pd

import sys
sys.path.insert(0, r'..')
from UT330.UT330 import UT330


# =============================================================================
# class Display
# =============================================================================
class Display(object):

    def __init__(self):

        self.page_width = 1200  # The width of the display in the browser
        self.page_height = 620  # The height of the display

        # The temperature and humidity data used by default and if the
        # user selects none in the read file menu
        self.default_data = \
            pd.DataFrame.from_dict({
                   'Timestamp': ['2018-07-01 08:00:00', '2018-07-01 08:00:01',
                                 '2018-07-02 08:00:00', '2018-07-03 08:00:00',
                                 '2018-07-03 08:00:01', '2018-07-04 08:00:00',
                                 '2018-07-04 08:00:01', '2018-07-04 08:00:02',
                                 '2018-07-05 08:00:00', '2018-07-06 08:00:00',
                                 '2018-07-06 08:00:01'],
                   'Temperature (C)': [0, 20.0, 15.0, 20.0, 10.0, 10.0, 20.0,
                                       10.0, 15.0, 10.0, 40.0],
                   'Relative humidity (%)': [0.0, 36.0, 31.0, 36.0, 26.0, 26.0,
                                             36.0, 26.0, 31.0, 25.0, 40.0],
                   'Pressure (Pa)': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

        self.default_data['Timestamp'] = \
            pd.to_datetime(self.default_data['Timestamp'])

        # We start with the default data
        self.data = self.default_data
        self.source = ColumnDataSource(data=self.data)

        # UT330 device
        self.ut330 = UT330()

        # Whether the UT330 device is connected or not.
        self.device_connected = False

        # Text used in dropdown menu if no file selected
        self.data_file_none = "No data file selected"

        # The Bokeh display is tabbed
        self.tabs = Tabs(tabs=[self.intro_tab(),
                               self.read_file_tab(),
                               self.h_t_tab(),
                               self.config_tab(),
                               self.offset_tab(),
                               self.time_tab(),
                               self.device_data_tab()])

    # Intro tab
    # =========
    def intro_tab(self):

        """Intro tab - explains the application"""

        html = ("<h1>UT330 UI</h1>"
                "<p>"
                "This UI controls a UT330 device from any operating "
                "system. It displays the temperature and humidity from "
                "pre-existing data files downloaded from a UT330 and it "
                "enables new data files to be read from a UT330 device "
                "connected to the computer. For full details of how the "
                "software works (and for licensing), read the "
                "<a href='https://github.com/MikeWoodward/UT330B'>"
                "Github page</a>."
                "</p>"
                "<p>"
                "Mike Woodward, 2017"
                "</p>")

        intro_text = Div(text=html,
                         width=self.page_width,
                         height=self.page_height)

        return Panel(child=widgetbox(intro_text), title="UT330 UI")

    # Read tab
    # ========
    def file_changed(self, attrname, old, new):

        """Helper functions for read_tab - called when user selects new
        data file to display """

        if new == self.data_file_none:
            self.data = self.default_data
        else:
            self.data = pd.read_csv(new, parse_dates=['Timestamp'])

        self.h_t_update()

    def scan_folder(self):

        """Helper function for scanning the data files folder"""

        pattern = os.path.join('Data', 'UT330_data_*.csv')
        files = glob.glob(pattern)

        length = len(files)

        if 0 == length:
            status_text = ("<strong>Error!</strong> There are no data "
                           "files in the Data folder. ")
        else:
            status_text = ("There are {0} file(s) in the "
                           "'Data' folder. ").format(length)

        status_text += ("Click <strong>Rescan folder</strong> to rescan the "
                        "data folder.")

        # Ensure we have a 'None' option and that it's the default
        files.insert(0, self.data_file_none)

        # Update the control
        self.file_select.options = files
        self.file_select.value = files[0]

        self.file_status.text = status_text

    def read_file_tab(self):

        """Lets the user choose a data file to read"""

        # Drop down list
        self.file_select = Select(name='Data files',
                                  value='',
                                  options=[],
                                  title='Data files')
        # Status text
        self.file_status = Div(text='', width=self.page_width)

        # Update the file_select and file_status controls with scan data
        self.scan_folder()

        # This line is here deliberately. The scan_folder would trigger
        # the on-change function and we don't want that first time around.
        self.file_select.on_change('value', self.file_changed)

        # Re-scan button
        file_rescan = Button(label="Rescan folder", button_type="success")
        file_rescan.on_click(self.scan_folder)

        # Layout
        c = column(self.file_select,
                   self.file_status,
                   file_rescan)

        return Panel(child=c, title="Read from file")

    # Config tab
    # ==========
    def config_read(self):

        """Reads config data to disk"""

        if not self.device_connected:
            self.config_status.text = ("Cannot read the UT330 device "
                                       "config data "
                                       "because no UT330 device connected.")
            return

        # Get the config data
        if self.config_connected():
            # The device has been read OK
            self.config_device_read = True
        else:
            self.config_device_read = False

    def config_write(self):

        """Writes config data to disk"""

        # Some error checking
        if not self.device_connected:
            self.config_status.text = ("Cannot write the UT330 config data "
                                       "to disk "
                                       "because there is no UT330 device "
                                       "connected.")
            return

        if not self.config_device_read:
            self.config_status.text = ("You must read the UT330 configuration "
                                       "before before "
                                       "writng different configuration data.")
            return

        try:
            # Get the config data
            config = {'device name': self.config_device_name.value,
                      'sampling interval': int(self.config_sampling.value),
                      'overwrite records':
                          self.config_overwrite_records.value == 'True',
                      'delay timing': int(self.config_delay.value),
                      'delay start': self.config_delay_start.value == 'Delay',
                      'high temperature alarm': int(self.config_t_high.value),
                      'low temperature alarm': int(self.config_t_low.value),
                      'high humidity alarm': int(self.config_h_high.value),
                      'low humidity alarm': int(self.config_h_low.value)}

        # Write it
            self.ut330.write_config(config)
            self.config_status.text = ("Wrote configuration data to UT3330 "
                                       "device.")
        except ValueError as error:
            self.config_status.text = error.args[0]
        except:
            self.config_status.text = "Error in config_write function."

    def config_connect(self):

        """Attempts to connect to device"""

        # Look to see if the device already connected
        if self.device_connected:
            self.config_status.text = ("Cannot connect the UT330 device "
                                       "because the UT330 device is already "
                                       "connected.")
            return

        # Now try and connect
        try:
            self.ut330.connect()
            self.config_status.text = ("Connected to the UT330 device.")
            self.device_connected = True
            return
        except IOError as error:
            self.config_status.text = error.args[0]
            self.device_connected = False
            return

    def config_disconnect(self):

        """Attempts to disconnect from device"""

        if not self.device_connected:
            self.config_status.text = ("Cannot disconnect the UT330 device "
                                       "because no UT330 device connected.")
            return

        # Now try and disconnect
        try:
            self.ut330.disconnect()
            self.config_status.text = "Disconnected the UT330 device."
            self.config_device_read = False
            self.device_connected = False
            return
        except IOError as error:
            self.config_status.text = error.args[0]
            return

    def config_not_connected(self):

        """UT330 not connected - so update config controls appropriately"""
        self.config_status.text = "UT330 device not connected."

        self.config_device_name.value = "No device"
        self.config_device_time.value = "No device"
        self.config_computer_time.value = "No device"
        self.config_t_high.value = "No device"
        self.config_t_low.value = "No device"
        self.config_h_high.value = "No device"
        self.config_h_low.value = "No device"
        self.config_p_high.value = "No device"
        self.config_p_low.value = "No device"
        self.config_sampling.value = "No device"
        self.config_delay.value = "No device"
        self.config_power.value = "No device"
        self.config_readings.value = "No device"

    def config_connected(self):

        """UT330 connected - so update config controls appropriately"""

        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            config = self.ut330.read_config()

            self.config_status.text = "UT330 device connected."

            # Populate the widgets
            self.config_device_name.value = config['device name']
            self.config_device_time.value = config['timestamp'].strftime(
                    "%Y-%m-%d %H:%M:%S")
            self.config_computer_time.value = now
            self.config_t_high.value = str(config['high temperature alarm'])
            self.config_t_low.value = str(config['low temperature alarm'])
            self.config_h_high.value = str(config['high humidity alarm'])
            self.config_h_low.value = str(config['low humidity alarm'])
            self.config_p_high.value = 'None'
            self.config_p_low.value = 'None'
            self.config_sampling.value = str(config['sampling interval'])

            self.config_overwrite_records.value = \
                'True' if config['overwrite records'] else 'False'
            self.config_delay_start.value = \
                'Delay' if config['delay start'] else 'No delay'
            self.config_delay.value = str(config['delay timing'])

            self.config_power.value = str(config['battery power'])
            self.config_readings.value = \
                "{0} of {1}".format(config['readings count'],
                                    config['readings limit'])

            return True
        except:
            self.config_status.text = "Exception raised in config_connected."
            return False

    def config_tab(self):

        """Reading/writing device configuration"""

        # True if the config device data has been read, false otherwise
        self.config_device_read = False

        # Device connectivity
        # ===================
        config_conn_head = Div(text="<strong>Connectivity</strong>")
        self.config_status = Div(text="", width=self.page_width)
        config_connect = Button(label='Connect to UT330',
                                button_type="success")
        config_read = Button(label='Read config', button_type="success")
        config_write = Button(label='Write config', button_type="success")
        config_disconnect = Button(label='Disconnect from UT330',
                                   button_type="success")

        config_connect.on_click(self.config_connect)
        config_read.on_click(self.config_read)
        config_write.on_click(self.config_write)
        config_disconnect.on_click(self.config_disconnect)

        # Show the configuration data
        # ===========================
        # Set up the widgets
        config_device_head = Div(text="<strong>Configuration</strong>")
        self.config_device_name = TextInput(title="Device name")
        self.config_device_time = TextInput(title="Device time")
        self.config_computer_time = TextInput(title="Computer time")
        self.config_t_high = TextInput(title="High temperature alarm (C)")
        self.config_t_low = TextInput(title="Low temperature alarm (C)")
        self.config_h_high = TextInput(title="High humidity alarm (%RH)")
        self.config_h_low = TextInput(title="Low humidity alarm (%RH)")
        self.config_p_high = TextInput(title="High pressure alarm")
        self.config_p_low = TextInput(title="Low pressure alarm")
        self.config_sampling = TextInput(title="Sampling interval (s)")
        self.config_overwrite_records = Select(title="Overwrite records",
                                               options=['False', 'True'])
        self.config_delay_start = Select(title="Delay start",
                                         options=['No delay', 'Delay'])
        self.config_delay = TextInput(title="Delay (s)")

        # Status data
        # ===========
        config_status_head = Div(text="<strong>Status</strong>")
        self.config_power = TextInput(title="Battery power (%)")
        self.config_readings = TextInput(title="Readings")

        # Disable user input for these widgets
        self.config_power.disabled = True
        self.config_readings.disabled = True

        # Values to widgets
        # =================
        if self.device_connected:
            self.config_connected()
        else:
            self.config_not_connected()

        # Set up the display
        layout = column(row(config_conn_head),
                        row(self.config_status),
                        row(config_connect,
                            config_read,
                            config_write,
                            config_disconnect),
                        row(config_device_head),
                        row(self.config_device_name,
                            self.config_device_time,
                            self.config_computer_time),
                        row(self.config_t_low,
                            self.config_h_low,
                            self.config_p_low),
                        row(self.config_t_high,
                            self.config_h_high,
                            self.config_p_high),
                        row(self.config_sampling),
                        row(self.config_overwrite_records,
                            self.config_delay_start,
                            self.config_delay),
                        row(config_status_head),
                        row(self.config_power, self.config_readings))

        return Panel(child=layout,
                     title="Read/write configuration")

    # Offset tab
    # ==========

    def offset_connect(self):

        """Connect the UT330 device"""

        # Look to see if the device already connected
        if self.device_connected:
            self.offset_status.text = ("Cannot connect the UT330 device "
                                       "because the UT330 device is already "
                                       "connected.")
            return

        # Now try and connect
        try:
            self.ut330.connect()
            self.offset_status.text = ("Connected to the UT330 device.")
            self.device_connected = True
        except IOError as error:
            self.offset_status.text = error.args[0]
            self.device_connected = False
        except:
            self.offset_status.text = "Exception raised in offset_connect."
            self.device_connected = False

    def offset_disconnect(self):

        """Disconnect the UT330 device"""

        if not self.device_connected:
            self.offset_status.text = ("Cannot disconnect the UT330 device "
                                       "because no UT330 device connected.")
            return

        # Now try and disconnect
        try:
            self.ut330.disconnect()
            self.offset_status.text = "Disconnected the UT330 device."
            self.offset_device_read = False
            self.device_connected = False
        except IOError as error:
            self.offset_status.text = error.args[0]
        except:
            self.offset_status.text = "Exception raised in offset_disconnect."

    def offset_read(self):

        """Reads offset data to disk"""

        if not self.device_connected:
            self.offset_status.text = ("Cannot read the UT330 device "
                                       "offset data "
                                       "because no UT330 device connected.")
            return

        # Get the config data
        if self.offset_connected():
            # The device has been read OK
            self.offset_device_read = True
        else:
            self.offset_device_read = False

    def offset_write(self):

        """Writes offset data to disk"""

        if not self.device_connected:
            self.offset_status.text = ("Cannot write the UT330 offset data "
                                       "to disk "
                                       "because there is no UT330 device "
                                       "connected.")
            return

        if not self.offset_device_read:
            self.offset_status.text = ("You must read the UT330 offset "
                                       "before before "
                                       "writng different offset data.")
            return

        try:
            # Get the offset data
            offset = {'temperature offset': float(self.offset_t.value),
                      'humidity offset': float(self.offset_h.value),
                      'pressure offset': float(self.offset_p.value)}

            # Write it
            self.ut330.write_offsets(offset)
            self.offset_status.text = ("Wrote offset data to UT3330 "
                                       "device.")
        except ValueError as error:
            self.offset_status.text = error.args[0]
        except:
            self.offset_status.text = "Exception in offset_write function."

    def offset_not_connected(self):

        """UT330 not connected - so update offset controls appropriately"""
        self.config_status.text = "UT330 device not connected."

        self.offset_t_current.value = "No device"
        self.offset_h_current.value = "No device"
        self.offset_p_current.value = "No device"
        self.offset_t.value = "No device"
        self.offset_h.value = "No device"
        self.offset_p.value = "No device"

    def offset_connected(self):

        """UT330  connected - so update offset controls appropriately"""

        try:
            self.config_status.text = ("UT330 device connected and offsets "
                                       "read.")

            offsets = self.ut330.read_offsets()

            self.offset_t_current.value = str(offsets['temperature'])
            self.offset_h_current.value = str(offsets['humidity'])
            self.offset_p_current.value = str(offsets['pressure'])
            self.offset_t.value = str(offsets['temperature offset'])
            self.offset_h.value = str(offsets['humidity offset'])
            self.offset_p.value = str(offsets['pressure offset'])
            return True
        except:
            self.config_status.text = "UT330 device not connected."
            return False

    def offset_tab(self):

        """Reading/writing device offsets"""

        # True if the offset device data has been read, false otherwise
        self.offset_device_read = False

        offset_status_h = Div(text="<strong>Status</strong>")
        self.offset_status = Div(text="", width=self.page_width)

        # Connect to device button
        # ========================
        offset_controls_h = Div(text="<strong>Device controls</strong>")
        offset_connect = Button(label='Connect to UT330',
                                button_type="success")
        offset_read = Button(label='Read offset', button_type="success")
        offset_write = Button(label='Write offset', button_type="success")
        offset_disconnect = Button(label='Disconnect from UT330',
                                   button_type="success")

        offset_connect.on_click(self.offset_connect)
        offset_read.on_click(self.offset_read)
        offset_write.on_click(self.offset_write)
        offset_disconnect.on_click(self.offset_disconnect)

        # Offsets
        # =======
        offset_offsets_h = Div(text="<strong>Offsets</strong>")
        self.offset_t_current = TextInput(title="Temperature current")
        self.offset_h_current = TextInput(title="Humidity current")
        self.offset_p_current = TextInput(title="Pressure current")

        self.offset_t = TextInput(title="Temperature offset")
        self.offset_h = TextInput(title="Humidity offset")
        self.offset_p = TextInput(title="Pressure offset")

        # Values to widgets
        # =================
        if self.device_connected:
            self.offset_connected()
        else:
            self.offset_not_connected()

        if self.device_connected:
            self.offset_status.text = ('UT330 device connected. The Read, '
                                       'Write, and Disconnect buttons '
                                       'will work.')
        else:
            self.offset_status.text = ('UT330 device is <strong>NOT</strong> '
                                       'connected. The '
                                       'Read, Write, and Disconnect buttons '
                                       'will <strong>not work</strong>. '
                                       'Click the '
                                       'Connect button if the UT330 is '
                                       'connected on a USB port.')
        # Layout
        # ======
        l = layout([[offset_status_h],
                    [self.offset_status],
                    [offset_controls_h],
                    [offset_connect,
                     offset_read,
                     offset_write,
                     offset_disconnect],
                    [offset_offsets_h],
                    [self.offset_t_current,
                     self.offset_h_current,
                     self.offset_p_current],
                    [self.offset_t,
                     self.offset_h,
                     self.offset_p]],
                   width=self.page_width)

        return Panel(child=l,
                     title="Read/write offset")

    # Data tab
    # ========
    def data_connect(self):

        """Connects to the device"""

        if self.device_connected:
            self.data_status.text = ("Cannot connect the UT330 device "
                                     "because UT330 device already connected.")
            return

        # Now try and connect
        try:
            self.ut330.connect()
            self.data_status.text = "Connected to the UT330 device."
            self.device_connected = True
        except IOError as error:
            self.data_status.text = error.args[0]
            self.device_connected = False
        except:
            self.data_status.text = "Exception raised in data_connect."
            self.device_connected = False

    def data_disconnect(self):

        """Disconnects from the device"""

        if not self.device_connected:
            self.data_status.text = ("Cannot disconnect the UT330 device "
                                     "because no UT330 device connected.")
            return

        # Now try and disconnect
        try:
            self.ut330.disconnect()
            self.data_status.text = "Disconnected the UT330 device."
            self.device_connected = False
        except IOError as error:
            self.data_status.text = error.args[0]
        except:
            self.data_status.text = "Exception raised in data_disconnect."

    def data_read(self):

        """Reads data from device"""

        if not self.device_connected:
            self.data_status.text = ("Cannot read the UT330 device "
                                     "because no UT330 device connected.")
            return

        try:
            self.data_status.text = "Reading in data from UT330..."
            data = self.ut330.read_data()
            count = len(data)

            if 0 == count:
                self.data_status.text = "No data to read on device."
                return

            self.data = pd.DataFrame(data)
            self.h_t_update()
            self.data_status.text = \
                "{0} lines of data read in from UT330.".format(count)
        except:
            self.data_status.text = "Exception in data_read."

    def data_write(self):

        """Writes data to disk"""

        if not self.device_connected:
            self.data_status.text = ("Cannot write the UT330 device data "
                                     "to disk "
                                     "because there is no UT330 device "
                                     "connected.")
            return

        try:
            data = self.ut330.read_data()
            self.data = pd.DataFrame(data)
            self.h_t_update()

            timestamp = data[0]['Timestamp']
            data_file = \
                os.path.join('Data',
                             'UT330_data_{0}.csv'.
                             format(timestamp.strftime("%Y%m%d_%H%M%S")))
            self.data.to_csv(data_file)

            self.data_status.text = "Wrote data to file {0}.".format(data_file)
        except:
            self.data_status.text = "Exception in data_write."

    def data_erase(self):

        """Erases device data"""

        if not self.device_connected:
            self.data_status.text = ("Cannot erase the UT330 device data "
                                     "because no UT330 device connected.")
            return

        try:
            self.ut330.delete_data()
            self.data_status.text = "UT330 data erased."
        except:
            self.data_status.text = "Exception in data_erase."

    def device_data_tab(self):

        """Reading device data"""
        self.data_status = Div(text="", width=self.page_width)

        data_connect = Button(label='Connect to UT330',
                              button_type="success")
        data_read = Button(label='Read data',
                           button_type="success")
        data_write = Button(label='Write data to disk',
                            button_type="success")
        data_erase = Button(label='Erase data',
                            button_type="success")
        data_disconnect = Button(label='Disconnect from UT330',
                                 button_type="success")

        data_connect.on_click(self.data_connect)
        data_read.on_click(self.data_read)
        data_write.on_click(self.data_write)
        data_erase.on_click(self.data_erase)
        data_disconnect.on_click(self.data_disconnect)

        if self.device_connected:
            self.data_status.text = ('UT330 device connected. The Read, '
                                     'Write, Erase, and Disconnect buttons '
                                     'will work.')
        else:
            self.data_status.text = ('UT330 device is <strong>NOT</strong> '
                                     'connected. The '
                                     'Read, Write, Erase, and Disconnect '
                                     'buttons will <strong>not work</strong>. '
                                     'Press the '
                                     'Connect button if the UT330 is '
                                     'connected on a USB port.')

        # Layout
        l = layout([[self.data_status],
                    [data_connect, data_disconnect],
                    [data_read, data_write, data_erase]],
                   width=self.page_width)

        return Panel(child=l,
                     title="Read from device")

    # Humidity and temperature
    # ========================
    # Helper function to update the Humidity and Temperature chart
    def h_t_update(self):

        """Updates Humidity/Temperature chart"""

        self.source.data = {'Timestamp': self.data['Timestamp'],
                            'Temperature (C)': self.data['Temperature (C)'],
                            'Relative humidity (%)':
                                self.data['Relative humidity (%)'],
                            'Pressure (Pa)': self.data['Pressure (Pa)']}

        # Reset the y axis ranges for temperature and humidity
        ymin = round(self.data['Temperature (C)'].min() - 2)
        ymax = ceil(self.data['Temperature (C)'].max() + 2)
        self.h_t_fig.y_range.start = ymin
        self.h_t_fig.y_range.end = ymax

        ymin = round(self.data['Relative humidity (%)'].min() - 2)
        ymax = ceil(self.data['Relative humidity (%)'].max() + 2)
        self.h_t_fig.extra_y_ranges['humidity'].start = ymin
        self.h_t_fig.extra_y_ranges['humidity'].end = ymax

    def h_t_lines_changed(self, active):

        """Helper function for h_t_tab - turns lines on and off"""

        for index in range(len(self.h_t_line)):

            self.h_t_line[index].visible = index in active

    def h_t_tab(self):

        """Plots the humidity and temperature"""

        self.h_t_fig = figure(plot_width=int(self.page_width*0.9),
                              plot_height=self.page_height,
                              title="Temperature and humidity",
                              toolbar_location="above",
                              x_axis_type="datetime")

        self.h_t_fig.xaxis.axis_label = "Timestamp"
        self.h_t_fig.yaxis.axis_label = "Temperature (C)"

        # Ranges need to be defined here - causes update issues if this
        # doesn't happen here
        self.h_t_fig.y_range = Range1d(start=0, end=100)
        self.h_t_fig.extra_y_ranges = {'humidity': Range1d(start=0,
                                                           end=100)}

        self.h_t_fig.add_layout(LinearAxis(y_range_name='humidity',
                                           axis_label="Relative humidity (%)"),
                                'right')

        # Add the lines
        self.h_t_line = 2*[None]

        # Plot the humidity/pressure
        self.h_t_line[0] = self.h_t_fig.line(x='Timestamp',
                                             y='Temperature (C)',
                                             source=self.source,
                                             color="blue",
                                             legend="Temperature",
                                             line_width=2)

        self.h_t_line[1] = self.h_t_fig.line(x="Timestamp",
                                             y="Relative humidity (%)",
                                             source=self.source,
                                             y_range_name="humidity",
                                             color="green",
                                             legend="Humidity",
                                             line_width=2)

        # Update the data and the plot ranges
        self.h_t_update()

        # Checkboxes to show lines
        resp_b = [0, 1]
        h_t_check_head = Div(text="Responses")
        h_t_check = CheckboxGroup(labels=["Temperature", "Humidity"],
                                  active=resp_b,
                                  name="Lines")

        h_t_check.on_click(self.h_t_lines_changed)

        # Lay out the page
        w = widgetbox(h_t_check_head,
                      h_t_check,
                      width=int(self.page_width*0.1))

        l = row(w, self.h_t_fig)

        return Panel(child=l, title="Temperature and humidity")

    # Time tab
    #  =======
    def time_connect(self):

        """Connects to the device"""

        if self.device_connected:
            self.time_status.text = ("Cannot connect the UT330 device "
                                     "because UT330 device already connected.")
            return

        # Now try and connect
        try:
            self.ut330.connect()
            self.time_status.text = "Connected to the UT330 device."
            self.device_connected = True
        except IOError as error:
            self.time_status.text = error.args[0]
            self.device_connected = False
        except:
            self.time_status.text = "Exception raised in data_connect."
            self.device_connected = False

    def time_disconnect(self):

        """Disconnects from the device"""

        if not self.device_connected:
            self.time_status.text = ("Cannot disconnect the UT330 device "
                                     "because no UT330 device connected.")
            return

        # Now try and disconnect
        try:
            self.ut330.disconnect()
            self.time_status.text = "Disconnected the UT330 device."
            self.device_connected = False
        except IOError as error:
            self.time_status.text = error.args[0]
        except:
            self.time_status.text = "Exception raised in data_disconnect."

    def time_get(self):

        """Gets the time on the device."""

        if not self.device_connected:
            self.time_status.text = ("Cannot get time from the UT330 device "
                                     "because no UT330 device connected.")
            return

        try:
            before = datetime.datetime.now()

            config = self.ut330.read_config()
            device = config['timestamp']
            after = datetime.datetime.now()
            self.time_compare.text = "Date/time on computer before "\
                                     "device call: {0}<br>"\
                                     "Date/time from device: {1}<br>" \
                                     "Date/time on computer after "\
                                     "device call: {2}".format(before,
                                                               device,
                                                               after)

            self.time_status.text = "Got the UT330 date and time."
        except:
            self.time_status.text = "Exception in time_get."

    def time_set(self):

        """Sets the time on the device."""

        if not self.device_connected:
            self.time_status.text = ("Cannot set time from the UT330 device "
                                     "because no UT330 device connected.")
            return

        try:
            now = datetime.datetime.now()
            self.ut330.write_date_time(now)
            self.time_status.text = ("Set the UT330 date and time from the "
                                     "computer.")
        except:
            self.time_status.text = "Exception in time_set."

    def time_tab(self):

        """The date and time setting and getting tab"""

        self.time_status = Div(text="", width=self.page_width)

        time_connect = Button(label='Connect to UT330',
                              button_type="success")

        time_disconnect = Button(label='Disconnect from UT330',
                                 button_type="success")

        time_get = Button(label='Get UT330 date and time',
                          button_type="success")

        self.time_compare = Div(text="", width=self.page_width)

        time_set = Button(label='Set the UT330 date and time',
                          button_type="success")

        time_connect.on_click(self.time_connect)
        time_disconnect.on_click(self.time_disconnect)
        time_get.on_click(self.time_get)
        time_set.on_click(self.time_set)

        l = layout([self.time_status],
                   [time_connect, time_disconnect],
                   [time_get, self.time_compare],
                   [time_set])

        return Panel(child=l, title="Date and time setting")

    def go(self):

        """Displays the application"""

        document = Document()
        document.title = "UT330 UI"
        document.add_root(self.tabs)
        session = push_session(document)
        session.show()

        session.loop_until_closed()

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':

    display = Display()

    display.go()
