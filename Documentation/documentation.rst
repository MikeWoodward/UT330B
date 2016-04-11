=============================
How to use the UT330 software
=============================

Introduction
============

I work in an office and I thought the temperature was changing more than was comfortable through the day. Sometimes I would be cold and sometimes hot. I wanted a cheap temperature logger to monitor the temperature so I could display the temperature history as a chart. 

I looked online on `AliExpress <http://www.aliexpress.com/>`_ and found the UT330B, a USB battery powered temperature and humidity logger. It was cheap ($35) and did what I wanted. The only problem was, it only had Windows software to control it and I use a Mac. It worked via a USB port, so I thought I could figure out the commands sent over the USB port and build something myself. With great help from `Philip Gladstone <https://github.com/pjsg>`_, I did it. This project is a result of that effort.

With this software, you can control the UT330B, or other UT330 devices, from any platform that runs Python and has a USB port. In the appendices, I list some of the UT330 devices and tell you where you can buy them.

What’s in the software package?
===============================

All of the software was built on Python 2.7 using the Anaconda distribution.

UT330
-----

This is the code that provides an interface to the UT330B. It’s fully commented and PEP8 compliant. 

Test
----

This is a simple script that demonstrates all of the UT330B methods. Note that the script will delete all data on the device and do a factory reset. Please be careful using it!

UI
--

This is a small system I’ve written using Bokeh to provide a UI to the device.

Documentation
-------------

This text.

License
-------

I’m using the MIT License.

Using the UT330 object – a short tutorial
=========================================

Dependencies
------------

The UT330 object depends on the following libraries:

* datetime
* pyserial (version 3.01)
* time

If you don’t already have them, you can install them with the pip install command.

You may also have to install a device driver. If this is the case, please let me know and I’ll add details.

Connect and read the device name
--------------------------------

For any of this to work, you must connect the UT330 to a USB port on your system.

The software has been designed to work with the Python with command, just like a file object. Here’s how. ::

    from ut330 import UT330

    with UT330() as ut330:                
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"                 
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading device name ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"        
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"              
        print "Device name = {0}".format(ut330.read_device_name())

Here, the UT330 is opened and a variable (ut330) initialized. The function read_device_name is called on the ut330 object and the name is printed. You should see an output something like this.::

    ut330b

Read the offsets
----------------

The UT330B allows you to set temperature and humidity offsets, allowing you to calibrate it. Here’s how you can read the offsets. ::

    from ut330 import UT330

    with UT330() as ut330:      
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"    
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading offsets ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"     
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"     
    
    offsets = ut330.read_offsets()
    print offsets

The offsets variable is a very simple Python dict: ::

    offsets= {	'temperature offset': 0,                        
                'humidity offset': 0,                        
                'pressure offset': 0}

The UT330B does not have a pressure sensor, so the pressure offset is irrelevant.

Reading the data
----------------

The temperature, humidity, and pressure data can be read from the device using the read_data() method. Here’s an example that shows reading the data and printing the result. ::

    # Read data   
    with UT330() as ut330:           
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"     
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading data ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"   
    print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"     
    DATA = ut330.read_data()              

    if DATA != []:                  

    print  'Timestamp, Temperature (C), Relative humidity (%), Pressure (Pa)\n'   
    
    for data_line in DATA:                          
        line = "{0}, {1}, {2}, {3}\n". format(data_line['timestamp'],
                                              data_line['temperature'],
                                              data_line['humidity'],
                                              data_line['pressure'])                                                   
        print line[:-1] 

Change the configuration
------------------------

As well as read data from the UT330B, you can also change its settings. Here, I’ll just show one example, changing the configuration information.

To do this, we have to create a dict which must be defined like this: ::

    CONFIG = {'device name': 'UT330B',                       
              'sampling interval': 300,                       
              'overwrite records': False,                      
              'delay timing': 120,                       
              'delay start': True,                       
              'high temperature alarm': 40,                       
              'low temperature alarm': -10,                       
              'high humidity alarm': 95,                       
              'low humidity alarm': 10}

The UT330 code shows the valid ranges for these variables, for example, you can have at most ten characters as the device name.

Here’s how you change the configuration and check it’s changed using the write_config() and read_config methods(). ::

    with UT330() as ut330:           

        # Write config             
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"    
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Write config ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"    
        print "▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉"     
        CONFIG = {'device name': 'UT330B',                       
                  'sampling interval': 300,                       
                  'overwrite records': False,                       
                  'delay timing': 120,                       
                  'delay start': True,                       
                  'high temperature alarm': 40,                      
                  'low temperature alarm': -10,                       
                  'high humidity alarm': 95,                       
                  'low humidity alarm': 10}  
            
        ut330.write_config(CONFIG)              

        CONFIG_NEW = ut330.read_config()              

        for k, v in CONFIG.iteritems():                 
            print "{0} Old = {1} New = {2}".format(k, CONFIG[k], CONFIG_NEW[k])

What else can you do?
---------------------

The documentation for the UT330 class describes in more detail what’s available, but here’s a quick summary:

* Write the date and time
* Read and write the offsets
* Read and write the configuration
* Delete the data
* Do a factory reset on the device

The UT330 UI
============

Background
----------

I wanted some way of displaying a chart and updating configuration settings using a UI. I could have done this with JavaScript and linked to Python, but I wanted to try out the Bokeh visualization package. I got something up and running, so I thought I would include it here.

To try this code, you’ll need to install the Bokeh project. To do this, type: ::

    pip install bokeh

Starting the UI
---------------

The Bokeh application here uses the Bokeh server to provide a web interface. To run the application, you’ll need to start the Bokeh server. From a console, type in: ::

    bokeh serve

Once the server starts, you should see something like this in the console window.

Running the UI
--------------

To run the UI, run the file UI.py. This should start a browser and you should see something like this.


The UT330 object
================

Methods
------

Disconnect
``````````

**Description:** Disconnects the UT330 device.

**Return value:** No return value.

read_data
`````````

**Description:** Reads the temperature, humidity, and pressure data off the UT330B.

**Return value:** Returns a data structure containing the timestamped temperature, humidity, and pressure data. Here's an example of the data returned: ::

 blah {}

delete_data
```````````

**Description:** Deletes the temperature, humidity, and pressure data from the UT330.

**Return value:** No return value.

read_config
```````````

**Description:**

**Return value:**

write_config
````````````

**Description:**

**Return value:**

write_date_time
```````````````

**Description:**

**Return value:**

read_offsets
````````````

**Description:**

**Return value:**

write_offsets
`````````````

**Description:**

**Return value:**

restore_factory
```````````````

**Description:** Restores the factory settings.

**Return value:** No return value

read_device_name
````````````````

**Description:** This returns the device name stripped of all leading and trailing blanks. The maximum device name length is 10 characters. 

**Return value:** Returns the device name.

Attributes
----------

None of the attributes are designed for use outside of the object. Use them at your own risk.

Functions
---------

Modbus
``````

This calculates a two byte Modbus CRC value. Be careful of the byte ordering when using the values. The UT330 puts the least significant byte first.

Avoiding timing issues – decorators
-----------------------------------

By experiment, I found issues with sending commands and reading the responses very quickly. For example, I found that executing two consecutive read_offsets gave a zero buffer for the second read_offsets. Again by experimentation, I found a delay of 0.01s (10ms) between device commands removed the problem. 

However, we don’t need the delay all of the time. If it’s been more than 10ms since the last command, there’s no point adding a delay.

I implemented this conditional delay using Python’s method decorators. This is the function ??? that appears as the method decorator @????


Appendix
========

Limitations
-----------

I couldn’t find a reliable way to uniquely identify the UT330 device, so I used the pid and vid. This might not uniquely identify the device and it’s possible that other USB devices report the same values. I’m open to suggestions for uniquely identifying the device.

I couldn’t identify the use of all bytes in the responses. For example, when reading the XXX, I don’t know what bytes YYYY are. If anyone knows, please let me know.

The UT330B and variants
-----------------------

The UT330B is a battery powered temperature and humidity logger manufactured by Uni-Trend (uni-trend.com), a Chinese company based in Hong Kong. There are several variants of this device on the market:
* UT330 A – temperature only
* UT330 B – temperature and humidity (my device)
* UT330 C – temperature, humidity, and pressure

The device is powered by a ½ AA lithium battery (please note: this is not an AA battery). This is a little hard to find and costs around $10, though you can get cheaper versions online for less. Some of the vendors on AliExpress sell the UT330 including a battery, though they charge a little more.

Where to buy it
---------------

I’ve seen this device (UT330B) on several websites worldwide. The cheapest place to buy it is from `AliExpress <http://www.aliexpress.com/>`_ where it costs around $35 (including shipping from China) depending on which vendor you buy from. I’ve seen the same device on Amazon in the US for around $70 and I’ve seen it on a specialist electronic supplier’s UK website for £70.

How the I found the commands and data
-------------------------------------

I did this with a great deal of help from `Philip Gladstone <https://github.com/pjsg/>`_.

We set up a Windows machine and installed the UT330 software. We also installed USB monitoring software. This monitoring software displayed all of the data exchanged between the UT330B device and the UT330 software.

We then used the UT330 software to send commands to the UT330 device, for example, clicking on the factory reset button, synching the time etc.

By going through all of the options on the software were able to capture every command and every response as a series of bytes. By changing values, we were able to figure out the format of commands and the responses. For example, we figured out that every command and response started ab cd (in hex) and ended with a two byte CRC. For the offsets, we changed the offset values and examined the bytes on the send command, we then read in the offsets again to see the same values on the receive side. In this way we were able to figure out what each of the commands and responses were.

We were able to find out how multi-byte values and negative values are handled by freezing the UT330 and heating it. It turns out the device uses two’s complement and least significant byte first.

Unfortunately, there were some bytes that I couldn’t figure out a meaning for. I’ve commented these in the code.

By capturing many commands and responses, and by trail and error on the Internet, I found the CRC was a Modbus CRC.
