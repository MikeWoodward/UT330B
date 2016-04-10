# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:51:20 2016

@author: mwoodward
"""

from bokeh.models import HBox, VBox
from bokeh.models.widgets import Button, Panel, TextInput
from UT330 import UT330


class Offsets_Panel(object):

    def __init__(self, ut330):

        self.ut330 = ut330

        self.t_current = TextInput(title="Temperature current")
        self.h_current = TextInput(title="Humidity current")
        self.p_current = TextInput(title="Pressure current")

        self.t_offset = TextInput(title="Temperature offset")
        self.h_offset = TextInput(title="Humidity offset")
        self.p_offset = TextInput(title="Pressure offset")

        self.read_offsets = Button(label='Read offsets')
        self.write_offsets = Button(label='Write offsets')

    def _layout_(self):
        return VBox(HBox(self.t_current, self.t_offset, width=500),
                    HBox(self.h_current, self.h_offset, width=500),
                    HBox(self.p_current, self.p_offset, width=500),
                    HBox(self.read_offsets, self.write_offsets, width=500))

    def panel(self):

        return Panel(child=self._layout_(), title="Offsets")

    def _read_(self):

        offsets = self.ut330.read_offsets()

        self.t_current.value = str(offsets['temperature'])
        self.h_current.value = str(offsets['humidity'])
        self.p_current.value = str(offsets['pressure'])

        self.t_offset.value = str(offsets['temperature offset'])
        self.h_offset.value = str(offsets['humidity offset'])
        self.p_offset.value = str(offsets['pressure offset'])

    def _write_(self):

        offsets = {'temperature offset': float(self.t_offset.value),
                   'humidity offset': float(self.h_offset.value),
                   'pressure offset': float(self.p_offset.value)}

        self.ut330.write_offsets(offsets)

    def callbacks(self):

        self.read_offsets.on_click(self._read_)
        self.write_offsets.on_click(self._write_)

    def device_read(self):

        self._read_()
