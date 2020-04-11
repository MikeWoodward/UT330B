# UT330B
Operating system independent controller for the Uni-Trend UT330B temperature and humidity logger.

What the software does
======================

The [Uni-Trend UT330B](https://www.uni-trend.com/html/product/Environmental/Environmental_Tester/UT330-USB/UT330B.html) is a battery-powered USB temperature and humidity logger. Off-the-shelf, it only comes with Windows control software. This project provides Python code to control the device from any operating system.

This project is a complete package, including software, a test script, a demo UI (written in Bokeh), and full documentation. 

.. image:: https://github.com/MikeWoodward/UT330B/blob/master/Documentation/chart.png

Acknowledgements
================

Many thanks to [Philip Gladstone](https://github.com/pjsg) for his tremendous help with this project.

Installation notes
==================

The project uses uses pyserial __version 3.01 or later__. This version uses Bokeh version 2.0.1. See the Documentation section for instructions for how to use the software.

Oddities
========

I updated this software in February 2020. For some unknown reason, the UT330B device won't accept date settings in February 2020, and won't function in February 2020. I think this is a device issue (maybe firmware?) but I can't confirm it - perhaps something to do with 2020-02. If anyone has any insight, I'd love to hear it.
