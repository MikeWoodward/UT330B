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
from bokeh.io import curdoc
from bokeh.models import Tabs
from model.UT330 import UT330
from view.intro import Intro
from view.readdisplay import ReadDisplay
from view.settings import Settings
from view.readsave import ReadSave


# %%---------------------------------------------------------------------------
# Controller
# -----------------------------------------------------------------------------
class Controller():
    """The Controller class is part of the model-view-controller architecture.
    Links views and Model and controls interaction between them."""

    # %%
    def __init__(self):
        """Method initializes object. First part of two-part initialization.
        The initialization done here should be low risk - we need the GUI to
        be built before we can show error messages."""

        self.status = "UT330B not connected."
        self.connected = False
        self.device_data = None
        self.device_config = None
        self.device_offsets = None

        self.UT330B = UT330()

        # Instantiate each of the tabs.
        intro = Intro(self)
        readdisplay = ReadDisplay(self)
        settings = Settings(self)
        readsave = ReadSave(self)

        self.panels = [intro,
                       readdisplay,
                       settings,
                       readsave]

        # Create tabs, note the order here is the display order.
        self.tabs = Tabs(tabs=[p.panel for p in self.panels])

    # %%
    def setup(self):
        """Method sets up object. Second part of two-part initialization."""
        for panel in self.panels:
            panel.setup()

    # %%
    def update(self):
        """Method updates object."""
        for panel in self.panels:
            panel.update()

    # %%
    def display(self):
        """Displays the visualization. Calls the Bokeh methods to make the
        application start. Note the server actually renders the GUI in the
        browser.
        Returns:
        None"""
        curdoc().add_root(self.tabs)
        curdoc().title = 'UT330BUI'

    # %%
    # Device level actions
    # --------------------

    # %%
    def connect(self):
        """Connects to UT330B device."""
        
        if self.connected:
            self.status = ("Cannot connect to UT330B because "
                           "the UT330B is already connected.")
            self.update()
            return

        try:
            self.UT330B.connect()
            self.status = "Successful connection to UT330B."
            self.connected = True
        except IOError as error:
            self.status = error.__str__()
            self.connected = False

        # Update all panels
        self.update()


    # %%
    def disconnect(self):
        """Disconnects from UT330B device."""
        
        if not self.connected:
            self.status = ("Cannot disconnect UT330B because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.UT330B.disconnect()
            self.status = "Disconnected from UT330B."
            self.connected = False
        except IOError as error:
            self.status = error.__str__()

        self.update()


    # %%
    def erase(self):
        """Erases data from UT330B device."""
        
        if not self.connected:
            self.status = ("Cannot erase UT330B data because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.UT330B.delete_data()
            self.status = "Data erased from UT330B."
            self.device_data = None
        except IOError as error:
            self.status = error.__str__()

        self.update()

    # %%
    def read_data(self):
        """Reads data from UT330B device."""

        if not self.connected:
            self.status = ("Cannot read UT330B data because the UT330B is "
                           "not connected.")
            self.update()
            return

        self.status = ("Reading UT330B data. This may take some time "
                       "if there's a lot of data...")
        self.update()
        
        curdoc().add_next_tick_callback(self.read_data_2)

    def read_data_2(self):
        try:
            self.device_data = self.UT330B.read_data()
            self.status = "Data read from UT330B."

            if len(self.device_data) == 0:
                self.status = "No data to read on device."

        except IOError as error:
            self.status = error.__str__()

        self.update()

    # %%
    def read_config(self):
        """Reads config from UT330B device."""
        
        if not self.connected:
            self.status = ("Cannot read UT330B configuration because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.device_config = self.UT330B.read_config()
            self.status = "Configuration read from UT330B."

            if len(self.device_config) == 0:
                self.status = "No config data read from device."

        except IOError as error:
            self.status = error.__str__()

        self.update()

    # %%
    def write_config(self, config):

        """Writes config data to UT330B device."""

        if not self.connected:
            self.status = ("Cannot write UT330B configuration because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.UT330B.write_config(config)
            self.status = "Configuration written to UT330B. "
            self.UT330B.write_datetime(config['timestamp'])
            self.status += "Datetime written to UT330B."
        except IOError as error:
            self.status = error.__str__()          
        except ValueError as error:
            self.status = error.__str__()            

        self.update()

    # %%
    def read_offsets(self):
        """Reads offsets from UT330B device."""

        if not self.connected:
            self.status = ("Cannot read UT330B offsets because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.device_offsets = self.UT330B.read_offsets()
            self.status = "Offsets read from UT330B."

            if len(self.device_offsets) == 0:
                self.status = "No offset data read from device."

        except IOError as error:
            self.status = error.__str__()

        self.update()

    # %%
    def write_offsets(self, offsets):

        """Writes config data to UT330B device."""
        
        if not self.connected:
            self.status = ("Cannot write UT330B offsets because "
                           "the UT330B is not connected.")
            self.update()
            return

        try:
            self.UT330B.write_offsets(offsets)
            self.status = "Configuration written to UT330B. "
        except IOError as error:
            self.status = error.__str__()
        except ValueError as error:
            self.status = error.__str__()
            
        self.update()
        
