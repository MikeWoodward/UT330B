# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:51:20 2016

@author: mwoodward
"""
import datetime
from bokeh.models import HBox, VBox
from bokeh.models.widgets import Button, Panel, Select, TextInput
from UT330 import UT330


class Config_Panel(object):

    def __init__(self, ut330):

        self.ut330 = ut330

        self.device_name = TextInput(title="Device name")

        self.device_time = TextInput(title="Device time")
        self.computer_time = TextInput(title="Computer time")

        self.t_high = TextInput(title="High temperature alarm (C)")
        self.t_low = TextInput(title="Low temperature alarm (C)")
        self.h_high = TextInput(title="High humidity alarm (%RH)")
        self.h_low = TextInput(title="Low humidity alarm (%RH)")
        self.p_high = TextInput(title="High pressure alarm")
        self.p_low = TextInput(title="Low pressure alarm")

        self.sampling = TextInput(title="Sampling interval (s)")
        self.overwrite_records = Select(title="Overwrite records",
                                        options=['False', 'True'])

        self.delay_start = Select(title="Delay start",
                                  options=['No delay', 'Delay'])
        self.delay = TextInput(title="Delay (s)")

        self.power = TextInput(title="Battery power (%)")
        self.readings = TextInput(title="Readings")

        self.read_config = Button(label='Read config')
        self.write_config = Button(label='Write config')

    def _layout_(self):

        return VBox(HBox(self.device_name,
                         self.device_time,
                         self.computer_time,
                         width=700),
                    HBox(self.t_low,
                         self.h_low,
                         self.p_low,
                         width=700),
                    HBox(self.t_high,
                         self.h_high,
                         self.p_high,
                         width=700),
                    HBox(self.sampling, width=700),
                    HBox(self.overwrite_records,
                         self.delay_start,
                         self.delay,
                         width=700),
                    HBox(self.power,
                         self.readings,
                         width=700),
                    HBox(self.read_config,
                         self.write_config,
                         width=700))

    def panel(self):

        return Panel(child=self._layout_(), title="Configuration")

    def callbacks(self):

        self.read_config.on_click(self._read_)
        self.write_config.on_click(self._write_)

    def device_read(self):

        self._read_()

    def _read_(self):

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config = self.ut330.read_config()

        self.device_name.value = config['device name']
        self.device_time.value = config['timestamp'].strftime("%Y-%m-%d "
                                                              "%H:%M:%S")
        self.computer_time.value = now
        self.t_high.value = str(config['high temperature alarm'])
        self.t_low.value = str(config['low temperature alarm'])
        self.h_high.value = str(config['high humidity alarm'])
        self.h_low.value = str(config['low humidity alarm'])
        self.p_high.value = 'None'
        self.p_low.value = 'None'
        self.sampling.value = str(config['sampling interval'])
        self.overwrite_records.value = 'True' if config['overwrite records'] \
                                       else 'False'
        self.delay_start.value = 'Delay' if config['delay start'] \
                                 else 'No delay'
        self.delay.value = str(config['delay timing'])
        self.power.value = str(config['battery power'])
        self.readings.value = "{0}/{1}".format(config['readings count'],
                                               config['readings limit'])

    def _write_(self):

        config = {'device name': self.device_name.value,
                  'sampling interval': int(self.sampling.value),
                  'overwrite records': self.overwrite_records.value == 'True',
                  'delay timing': int(self.delay.value),
                  'delay start': self.delay_start.value == 'Delay',
                  'high temperature alarm': int(self.t_high.value),
                  'low temperature alarm': int(self.t_low.value),
                  'high humidity alarm': int(self.h_high.value),
                  'low humidity alarm': int(self.h_low.value)}

        self.ut330.write_config(config)
