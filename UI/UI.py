# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:51:20 2016

@author: mwoodward
"""
from bokeh.client import push_session
from bokeh.models.widgets import Tabs
from bokeh.plotting import curdoc

from Chart_Panel import Chart_Panel
from Config_Panel import Config_Panel
from Offsets_Panel import Offsets_Panel

from UT330 import UT330


ut330 = UT330()

# Setup the config panel
config = Config_Panel(ut330)
config.callbacks()
config.device_read()

# Setup the offsets panel
offsets = Offsets_Panel(ut330)
offsets.callbacks()
offsets.device_read()

# Set up the charts panel
chart = Chart_Panel(ut330)
chart.callbacks()

# Build the tabs
tabs = Tabs(tabs=[config.panel(), offsets.panel(), chart.panel()])

# Set up the document
doc = curdoc()
doc.clear()  # Clear what's already there, if anything
doc.title = "UT330"  # Change the title
doc.add_root(tabs)  # Add our figure

# open a session to keep our local document in sync with server
session = push_session(doc)
session.show()  # open the document in a browser

# Do the device read here to improve application performance
chart.device_read()

session.loop_until_closed()  # run forever
