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
from controller.controller import Controller

# TDOO Where do datafiles live? One consistent folder
# TODO jsonschema

# %%---------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
controller = Controller()
controller.setup()
controller.update()
controller.display()
