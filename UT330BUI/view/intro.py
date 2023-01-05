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
from bokeh.models import (Div, TabPanel)
from bokeh.layouts import column


# %%---------------------------------------------------------------------------
# Intro
# -----------------------------------------------------------------------------
class Intro():
    """Panel to introduce software."""
        
    INSTRUCTIONS = ("""This applications is a cross-platform tool for """
                    """controlling the Uni-Trend UT330B temperature """
                    """and humidity data logger. It offers the ability """
                    """to do the following:<br>"""
                    """<ul>"""
                    """<li>Read and write the device configuration, """
                    """including setting the device datetime</li>"""
                    """<li>Read temperature and humidity data from the """
                    """device, including the ability to erase data """
                    """to make space for more readings</li>"""
                    """<li>Visualize the temperature and humidity data</li>"""
                    """</ul>"""
                    """Any operations involving configuration or reading/"""
                    """erasing device data obviously requires the UT330B """
                    """device to be connected to this computer.""")

    # %%
    def __init__(self, controller):
        """Method sets up object.  First part of two-part initialization."""

        self.controller = controller

        # Shows the logo -in this case, a picture of the device
        url = 'http://localhost:5006/UT330BUI/static/UT330B.jpg'
        self.logo = \
            Div(text="""<img src="{0}" alt="div_image" """
                      """"width=""500" height="121">""".format(url), 
                width=500, height=121, sizing_mode='fixed')

        # Holds descriptive text for display.
        self.description =\
            Div(text=self.INSTRUCTIONS)
        self.layout = column(children=[self.logo,
                                       self.description],
                             sizing_mode='stretch_both')
        self.panel = TabPanel(child=self.layout, title='UT330B')

    # %%
    def setup(self):
        """Method sets up object. Second part of two-part initialization."""

        pass

    # %%
    def update(self):
        """Method updates object."""

        pass
