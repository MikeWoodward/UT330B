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
import datetime
from bokeh.models import (Button, Div, TabPanel, Select, TextInput)
from bokeh.layouts import column, row


# %%---------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
class Settings():
    """UT330B settings."""

    # %%
    def __init__(self, controller):
        """Method sets up object.  First part of two-part initialization."""

        self.controller = controller

        #An approximation for how long it takes to write the time to the
        # device
        # TODO explain what this is
        self.time_offset = datetime.timedelta(seconds=0)

        # Heading for connectivity section.
        self.connectivity =\
            Div(text="""<span style='font-weight:bold'>Connectivity</span>""")
        # Tells the user the current status of the UT330B connection.
        self.connect_status = Div(text=self.controller.status)
        # Connect to the UT330B device.
        self.connect_ut330b =\
            Button(label="""Connect to UT330B""", button_type="""success""")
        # Reads in the UT330B configuration
        self.read_config =\
            Button(label="""Read UT330B configuration""",
                   button_type="""success""")
        # Writes the UT330B configuration
        self.write_config =\
            Button(label="""Write UT330B configation""",
                   button_type="""success""")
        # Disconnects from the UT330B device.
        self.disconnect =\
            Button(label="""Disconnect from UT330B""",
                   button_type="""success""")
        # Heading for configuration section
        self.configuration =\
            Div(text="""<span style='font-weight:bold'>Configuration</span>""")
        # The device name
        self.device_name =\
            TextInput(title="""Device name""",
                      value="""No device""",
                      max_width=300)
        # Temperature that triggers low temperature alarm.
        self.low_temp_alarm =\
            TextInput(title="""Low temperature alarm (C)""",
                      value="""No device""")
        # Humidity that triggers low humidity alarm.
        self.low_humid_alarm =\
            TextInput(title="""Low humidity alarm (%RH)""",
                      value="""No device""")
        # Pressure that triggers low pressure alarm.
        self.low_press_alarm =\
            TextInput(title="""Low pressure alarm""", value="""No device""")
        # Temperature that triggers high temperature alarm.
        self.hi_temp_alarm =\
            TextInput(title="""High temperature alarm (C)""",
                      value="""No device""")
        # Humidity that triggers high humidity alarm.
        self.hi_humid_alarm =\
            TextInput(title="""High humidity alarm (%RH)""",
                      value="""No device""")
        # Pressure that triggers high pressure alarm.
        self.hi_press_alarm =\
            TextInput(title="""Low pressure alarm""", value="""No device""")
        # The sampling interval in seconds.
        self.sample_interval =\
            TextInput(title="""Sampling interval (s)""",
                      value="""No device""")
        # Overwrite records
        self.overwrite =\
            Select(options=['False', 'True'], title="""Overwrite records""")
        # Whether or not to delay recording start
        self.delay_start =\
            Select(options=['No delay', 'Delay'], title="""Delay start""")
        # The start delay in seconds.
        self.delay_s = TextInput(title="""Delay (s)""", value="""No device""")
        # Reads in the UT330B offsets
        self.read_offsets =\
            Button(label="""Read UT330B offsets""",
                   button_type="""success""")
        # Writes the UT330B offsets
        self.write_offsets =\
            Button(label="""Write UT330B offsets""",
                   button_type="""success""")
        # The battery power %.
        self.battery_power =\
            TextInput(title="""Battery power (%)""",
                      disabled=True,
                      value="""No device""")
        # The number of readings.
        self.readings_count =\
            TextInput(title="""Readings count""",
                      disabled=True,
                      value="""No device""")
        # Heading for date time section
        self.datetime_head =\
            Div(text="""<span style='font-weight:bold'>"""
                     """Set UT330B date and time</span>""")
        # The device time
        self.device_time = TextInput(title="""Device time""",
                                     value="""No device""",
                                     disabled=True)
        # The computer time
        self.computer_time = TextInput(title="""Computer time""",
                                       value="""No device""",
                                       disabled=True)
        # Heading for offsets section
        self.offsets =\
            Div(text="""<span style='font-weight:bold'>Offsets</span>""")
        # The current temperature (C).
        self.current_temp =\
            TextInput(title="""Current temperature (C)""",
                      disabled=True,
                      value="""No device""")
        # The current humidity (%RH).
        self.current_humid =\
            TextInput(title="""Current humidity (%RH)""",
                      disabled=True,
                      value="""No device""")
        # The current pressure.
        self.current_press =\
            TextInput(title="""Current pressure""",
                      disabled=True,
                      value="""No device""")
        # The temperature offset (C).
        self.temp_offset =\
            TextInput(title="""Temperature offset (C)""",
                      value="""No device""")
        # The humidity offset (%RH).
        self.humidity_offset =\
            TextInput(title="""Humidity offset (%RH)""",
                      value="""No device""")
        # The pressure offset.
        self.pressure_offset =\
            TextInput(title="""Pressure offset""", value="""No device""")

        # Layout
        self.layout = column(children=[self.connectivity,
                                       self.connect_status,
                                       row(self.connect_ut330b,
                                           self.disconnect),
                                       self.configuration,
                                       self.device_name,
                                       row(self.low_temp_alarm,
                                           self.low_humid_alarm,
                                           self.low_press_alarm),
                                       row(self.hi_temp_alarm,
                                           self.hi_humid_alarm,
                                           self.hi_press_alarm),
                                       row(self.sample_interval,
                                           self.overwrite),
                                       row(self.delay_start,
                                           self.delay_s),

                                       row(self.battery_power,
                                           self.readings_count),
                                       self.datetime_head,
                                       row(self.device_time,
                                           self.computer_time),

                                       row(self.read_config,
                                           self.write_config),

                                       self.offsets,
                                       row(self.current_temp,
                                           self.current_humid,
                                           self.current_press),
                                       row(self.temp_offset,
                                           self.humidity_offset,
                                           self.pressure_offset),
                                       row(self.read_offsets,
                                           self.write_offsets)
                                       ],
                             sizing_mode='stretch_both')
        self.panel = TabPanel(child=self.layout, title='Settings')

    # %%
    def setup(self):
        """Method sets up object. Second part of two-part initialization."""

        self.connect_ut330b.on_click(self.callback_connect_ut330b)
        self.disconnect.on_click(self.callback_disconnect)

        self.read_config.on_click(self.callback_read_config)
        self.write_config.on_click(self.callback_write_config)

        self.read_offsets.on_click(self.callback_read_offsets)
        self.write_offsets.on_click(self.callback_write_offsets)

    # %%
    def update(self):
        """Method updates object."""

        self.connect_status.text = self.controller.status

    # %%
    def callback_connect_ut330b(self):
        """Callback method for Connect UT330B"""

        self.controller.connect()

    # %%
    def callback_read_config(self):
        """Callback method for Read config"""

        before = datetime.datetime.now()
        self.controller.read_config()
        after = datetime.datetime.now()
        config = self.controller.device_config
        if not config:
            return

        self.time_offset = after - before

        # Likely computer time hen UT330B time sample was done
        computer_time = before + (after - before)/2

        self.sample_interval.value = str(config['sampling interval'])
        self.readings_count.value = "{0} / {1}".format(
            config['readings count'], config['readings limit'])
        self.battery_power.value = str(config['battery power'])
        self.device_name.value = config['device name']
        self.device_time.value = \
            config['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        self.computer_time.value = \
            computer_time.strftime("%Y-%m-%d %H:%M:%S")
        self.overwrite.value = \
            'True' if config['overwrite records'] else 'False'
        self.delay_start.value = \
            'Delay' if config['delay start'] else 'No delay'
        self.delay_s.value = str(config['delay timing'])
        self.hi_temp_alarm.value = str(config['high temperature alarm'])
        self.low_temp_alarm.value = str(config['low temperature alarm'])
        self.hi_humid_alarm.value = str(config['high humidity alarm'])
        self.low_humid_alarm.value = str(config['low humidity alarm'])
        self.hi_press_alarm.value = 'None'
        self.low_press_alarm.value = 'None'

    # %%
    def callback_write_config(self):
        """Callback method for Write config"""

        set_time = datetime.datetime.now() + self.time_offset

        try:
            config = {'device name': self.device_name.value,
                      'sampling interval': int(self.sample_interval.value),
                      'overwrite records':
                          self.overwrite.value == 'True',
                      'delay timing': int(self.delay_s.value),
                      'delay start': self.delay_start.value == 'Delay',
                      'high temperature alarm': int(self.hi_temp_alarm.value),
                      'low temperature alarm': int(self.low_temp_alarm.value),
                      'high humidity alarm': int(self.hi_humid_alarm.value),
                      'low humidity alarm': int(self.low_humid_alarm.value),
                      'timestamp': set_time}
            self.controller.write_config(config)                
        except ValueError as e:
            self.connect_status.text = ("Error! Cannot write this "
                                        "configuration data to the device. "
                                        "This may be because the UT330B is "
                                        "not connected.")
            return

    # %%
    def callback_read_offsets(self):
        """Callback method for read offsets"""

        self.controller.read_offsets()
        offsets = self.controller.device_offsets    
        if not offsets:
            return

        self.current_temp.value = str(offsets['temperature'])
        self.current_humid.value = str(offsets['humidity'])
        self.current_press.value = str(offsets['pressure'])

        self.temp_offset.value = str(offsets['temperature offset'])
        self.humidity_offset.value = str(offsets['humidity offset'])
        self.pressure_offset.value = str(offsets['pressure offset'])

    # %%
    def callback_write_offsets(self):
        """Callback method for write offsets"""
        
        try:
            offsets = {'temperature offset': float(self.temp_offset.value),
                       'humidity offset': float(self.humidity_offset.value),
                       'pressure offset': float(self.pressure_offset.value)} 
            self.controller.write_offsets(offsets)
        except ValueError as e:
            self.connect_status.text = ("Error! Cannot write this "
                                        "offset data to the device. "
                                        "This may be because the UT330B is "
                                        "not connected.")

    # %%
    def callback_disconnect(self):
        """Callback method for Disconnect"""

        self.controller.disconnect()
