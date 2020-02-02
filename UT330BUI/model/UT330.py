#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides a cross-platform Python interface for the UNI-T 330A/B/C temperature,
humidity, and pressure data loggers.

This code controls a UNI-T 330 A/B/C device via a cross-platform Python script.
The device accepts commands and provides responses. I’ve decoded all the
commands and responses and put them into this script. There are a few bytes in
both the commands and responses that I couldn’t figure out. If you know what
they are, please add them.

My device is a UNI-T 330B which only has temperature and humidity. The commands
for this device have placeholders for pressure, which I’ve added to my code,
but of course, I can’t check the pressure readings are correct.

Created on Wed Mar  2 18:10:21 2016

@author: Mike Woodward
"""

# =============================================================================
# Imports
# =============================================================================
import datetime
import time
import serial.tools.list_ports


# =============================================================================
# Module info
# =============================================================================
__author__ = "Mike Woodward"
__copyright__ = "2016 Michael Vincent Woodward"
__credits__ = "Philip Gladstone"
__license__ = "MIT"


# =============================================================================
# Function decorators
# =============================================================================
def buffer_safety(func):

    """There can be timing errors where a read takes place when the buffer
    is either partially written or not written at all. These errors can be
    removed by a short pause of 10ms. This function decorator makes sure
    there's at least 10ms between calls."""

    def buffer_protection(self, argument=None):

        # If we're less than 10ms since the last call, wait 10ms
        if datetime.datetime.now() - self.last_op_time \
           < datetime.timedelta(0, 0, 10000):
            time.sleep(0.01)

        # Read functions have no arguments, write functions have one
        if argument is None:

            data = func(self)

        else:

            data = func(self, argument)

        # We don't know how long the operation took, so use the current time
        # as the last op time
        self.last_op_time = datetime.datetime.now()

        return data

    return buffer_protection

# =============================================================================
# Functions
# =============================================================================
TABLE = (
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040)


def modbusCRC(data):

    """Returns the Modbus CRC as two bytes. Be careful of the order."""

    # If the contnets of the data list are not all integers, this function
    # will have problems. Future action is to check all elements are ints

    crc = 0xFFFF

    for number in data:
        crc = (crc >> 8) ^ TABLE[(crc ^ number) & 0xFF]

    MSB = crc >> 8  # Most Significant Byte
    LSB = crc & 255  # Least Significant Byte

    return MSB, LSB


# =============================================================================
# class UT330
# =============================================================================
class UT330():

    """Provides an object-based interface to the UT330.

    Here are the commands I know about
    # 0x10 - set configuration info
    # 0x11 - read configuration info
    # 0x12 - synch time
    # 0x16 - set offsets
    # 0x17 - read offsets
    # 0x18 - delete data
    # 0x19 - read data
    # 0x20 - factory reset
    # 0x51 - get device name
    """

    # %%
    def __init__(self):

        # The time of the last function call. Set to min initially because
        # there hasn't been a last call when the software starts.
        self.last_op_time = datetime.datetime.min

        # The PySerial object
        self._ut330 = None

        # Input and output buffer object
        self._buffer = None

        # Index to the position of the current element being processed
        self._index = 0

        # Time to wait before timing out
        self._read_timeout = 5
        self._write_timeout = 5

    # %%
    def __del__(self):

        self.disconnect()

    # %%
    def connect(self):

        """Connects to the device or raises an error"""

        # Get the port the device is connected to
        # ---------------------------------------
        port = None

        # Get all the serial ports
        port_list = serial.tools.list_ports.comports()
        serial.tools.list_ports.comports

        # Now find which port has our device
        for trial in port_list:

            # I'm not sure this is specific enough for general use. It may
            # give a false report if another device using the same controller
            # is connected. However, I can't find a more specific check.
            if trial.vid == 4292 and trial.pid == 60000:
                port = trial

        if port is None:
            raise IOError('Error! The UT330 device was not detected on any '
                          'USB port.')

        # Attempt a connection to the port
        # --------------------------------
        self._ut330 = serial.Serial(port=port.device,
                                    baudrate=115200,
                                    timeout=self._read_timeout,
                                    write_timeout=self._write_timeout)

        # Check that the serial port is open
        # ----------------------------------
        if not self._ut330.isOpen():
            raise IOError('Error! The UT330 is not open on the serial port.')

    # %%
    def __enter__(self):

        """Function to make this class work with Python's with statement"""

        self.connect()

        return self

    # %%
    def __exit__(self, type_ex, value_ex, traceback_ex):

        """Function to make this class work with Python's with statement"""

        self.disconnect()

    # %%
    def _read_buffer(self, byte_count):

        """Reads the contents of the buffer and returns it as an integer list.
        """

        # If the page_size is set much larger than this number we tend
        # to get problems with partially filled buffers
        page_size = 32768

        self._buffer = []

        # Read in data in as large chuncks as possible to speed up reading.
        # Read in the largest possible chunks first.
        for i in range(int(byte_count/page_size)):
            self._buffer += self._ut330.read(page_size)

        # Now read in the smallest chunk.
        self._buffer += self._ut330.read(byte_count % page_size)

    # %%
    def _write_buffer(self):

        """Writes the command string to the buffer"""

        bytes_written = self._ut330.write(bytearray(self._buffer))

        if bytes_written != len(self._buffer):
            raise ValueError('Error! _write_buffer: not all command bytes '
                             'written')

    # %%
    def _get_datetime(self):

        """Returns the date and time as a timestamp"""

        timestamp = datetime.datetime(2000 + self._buffer[self._index],
                                      self._buffer[self._index + 1],
                                      self._buffer[self._index + 2],
                                      self._buffer[self._index + 3],
                                      self._buffer[self._index + 4],
                                      self._buffer[self._index + 5])
        return timestamp

    # %%
    def _get_temperature(self):

        """Returns the temperature from the device buffer data - including
        negative temperatures"""

        # Look to see if the temperature's negative - using two's complement
        # to represent negative numbers
        if self._buffer[self._index + 1] >= 128:
            temperature = -float(256*(self._buffer[self._index + 1] ^ 0xff) +
                                 (self._buffer[self._index] ^ 0xff) + 1)/10
        # Temperature is positive
        else:
            temperature = float(256*self._buffer[self._index + 1] +
                                self._buffer[self._index])/10

        return temperature

    # %%
    def _get_name(self):

        """Retrieves the device name from the buffer data"""

        temp = self._buffer[self._index: self._index + 10]

        return ''.join(chr(entry) for entry in temp).strip()

    # %%
    def disconnect(self):

        """Disconnect the device"""

        if self._ut330 is not None:
            self._ut330.close()

    # %%
    @buffer_safety
    def read_data(self):

        """Downloads the device buffer data (temperature, humidity, pressure),
        and decodes it"""

        # We split this function into a header and data part to speed up
        # reading. Reading the header tells us how much data there is in the
        # data part

        # The read data command
        self._buffer = [0xab, 0xcd, 0x03, 0x19, 0x70, 0xc5]

        # Write the command
        self._write_buffer()

        # Read the header
        # ---------------
        # Now get the header data from the buffer
        self._read_buffer(8)

        # Check that some data has actually been returned
        if len(self._buffer) == 0:
            print("Warning! Empty buffer returned by device")
            return []

        # Get the length of data in the buffer
        length = (self._buffer[4] + 256*self._buffer[5] +
                  256*256*self._buffer[6] + 256*256*256*self._buffer[7])

        # Check that there's actually some data on the device - 22 is the
        # minimum buffer length if there's actually data
        if length < 22:

            # Need to read the CRC code and so clear the buffer before
            # returning - gives an error later if this isn't done.
            self._read_buffer(2)

            print("Warning! No temperature/humidity/pressure data on the " \
                  "device")
            return []

        # Now get the data
        # ----------------
        self._read_buffer(length)

        self._index = 0  # This is the offset of the first data item

        # The output data structure
        data = []

        # Loop over every set of readings
        while self._index < length - 2:

            timestamp = self._get_datetime()

            self._index += 6

            temperature = self._get_temperature()

            self._index += 2

            humidity = float(self._buffer[self._index] +
                             256*self._buffer[self._index + 1])/10
            pressure = float(self._buffer[self._index + 2] +
                             256*self._buffer[self._index + 2])/10

            self._index += 4

            data.append({'Timestamp': timestamp,
                         'Temperature (C)': temperature,
                         'Relative humidity (%)': humidity,
                         'Pressure (Pa)': pressure})

        return data

    # %%
    @buffer_safety
    def delete_data(self):

        """Deletes the temperature, humidity, and pressure data from the
        device"""

        # The delete command
        self._buffer = [0xab, 0xcd, 0x03, 0x18, 0xb1, 0x05]

        self._buffer[5], self._buffer[4] = modbusCRC(self._buffer[0:4])

        # Write the command
        self._write_buffer()

        # Now get the response data from the buffer
        self._read_buffer(7)

        # Check the return code shows the data was correctly deleted
        if [171, 205, 4, 24, 0, 116, 181] != self._buffer:
            raise IOError("Error! Delete data returned error code.")

    # %%
    @buffer_safety
    def read_config(self):

        """Read the configuration data from the device, saves it to disk"""

        # Send the read info command to the device
        self._buffer = [0xab, 0xcd, 0x03, 0x11, 0x71, 0x03]

        # Write the command
        self._write_buffer()

        # Now get the data from the buffer. We know the returned length will
        # be 46.
        self._read_buffer(46)

        # Now, interpret the data in the buffer
        config = {}

        # Get the device name
        self._index = 4
        config['device name'] = self._get_name()

        # I don't know what bytes 15 to 19 are

        config['sampling interval'] = (256*256*self._buffer[22] +
                                       256*self._buffer[21] +
                                       self._buffer[20])

        config['readings count'] = 256*self._buffer[24] + self._buffer[23]
        config['readings limit'] = 256*self._buffer[26] + self._buffer[25]

        config['battery power'] = self._buffer[27]

        config['overwrite records'] = bool(self._buffer[28])
        config['delay start'] = bool(self._buffer[29])

        config['delay timing'] = (256*256*self._buffer[32] +
                                  256*self._buffer[31] +
                                  self._buffer[30])

        # I don't know what byte 33 is

        # It's possible the high temp alarm could be negative
        if self._buffer[34] < 128:
            config['high temperature alarm'] = self._buffer[34]
        else:
            config['high temperature alarm'] = -256 + self._buffer[34]

        # It's possible the low temperature alarm could be positive
        if self._buffer[35] >= 128:
            config['low temperature alarm'] = -256 + self._buffer[35]
        else:
            config['low temperature alarm'] = self._buffer[35]

        config['high humidity alarm'] = self._buffer[36]
        config['low humidity alarm'] = self._buffer[37]

        self._index = 38
        config['timestamp'] = self._get_datetime()

        return config

    # %%
    @buffer_safety
    def write_config(self, config):

        """Sets the configuration information on the device"""

        # The command to send, note we'll be overriding some bytes
        self._buffer = [0xab, 0xcd, 0x1a, 0x10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Check config parameters
        # -----------------------
        if len(config['device name']) > 10:
            raise ValueError('Error! device name {0} is {1} characters when '
                             'it can be a maximum of 10'.
                             format(config['device name'],
                                    len(config['device name'])))

        if len(config['device name']) == 0:
            raise ValueError('Error! device name is length zero, it needs '
                             'to be more than zero characters')

        if config['sampling interval'] < 0 or \
           config['sampling interval'] > 86400:
            raise ValueError('Error! sampling interval is {0} but it must be '
                             'between 0 and 86400'.
                             format(config['sampling interval']))

        if config['delay timing'] < 0 or config['delay timing'] > 604800:
            raise ValueError('Error! delay timing is {0} but it must be '
                             'between 0 and 604800'.
                             format(config['delay timing']))

        # Prepare the data for writing
        # ----------------------------

        # Add the device name - pad to 10 characters with spaces
        for idx, val in enumerate(config['device name'][0:10].rjust(10, ' ')):
            self._buffer[4 + idx] = ord(val)

        # Add the sampling interval
        self._buffer[14] = config['sampling interval'] & 0xff
        self._buffer[15] = (config['sampling interval'] & 0x00ff00) >> 8
        self._buffer[16] = (config['sampling interval'] & 0xff0000) >> 16

        self._buffer[17] = int(config['overwrite records'])
        self._buffer[18] = int(config['delay start'])

        # Delay timing
        self._buffer[19] = config['delay timing'] & 0xff
        self._buffer[20] = (config['delay timing'] & 0x00ff00) >> 8
        self._buffer[21] = (config['delay timing'] & 0xff0000) >> 16

        self._buffer[22] = 0  # I don't know what this byte is

        if config['high temperature alarm'] >= 0:
            self._buffer[23] = config['high temperature alarm']
        else:
            self._buffer[23] = 256 + config['high temperature alarm']

        if config['low temperature alarm'] < 0:
            self._buffer[24] = 256 + config['low temperature alarm']
        else:
            self._buffer[24] = config['low temperature alarm']

        self._buffer[25] = config['high humidity alarm']
        self._buffer[26] = config['low humidity alarm']

        # Add the CRC bytes
        self._buffer[28], self._buffer[27] = modbusCRC(self._buffer[0:27])

        # Write the buffer
        self._write_buffer()

        # Now get the response data from the buffer
        self._read_buffer(7)

        # Check the return code shows the data was correctly written
        if [171, 205, 4, 16, 0, 115, 117] != self._buffer:
            raise IOError("Error! Config writing returned error code.")

    # %%
    @buffer_safety
    def write_datetime(self, timestamp):

        """Syncs the time to the timestamp"""

        # The command to send, note we'll be overriding some bytes
        self._buffer = [0xab, 0xcd, 0x09, 0x12, 0, 0, 0, 0, 0, 0, 0, 0]

        self._buffer[4] = timestamp.year - 2000
        self._buffer[5] = timestamp.month
        self._buffer[6] = timestamp.day
        self._buffer[7] = timestamp.hour
        self._buffer[8] = timestamp.minute
        self._buffer[9] = timestamp.second

        # Add the CRC bytes
        self._buffer[11], self._buffer[10] = modbusCRC(self._buffer[0:10])

        self._write_buffer()

        # Now get the response data from the buffer
        self._read_buffer(7)

        # Check the return code shows the data was correctly written
        if [171, 205, 4, 18, 0, 114, 21] != self._buffer:
            raise IOError("Error! Writing datetime returned error code.")

    # %%
    @buffer_safety
    def read_offsets(self):

        """Reads the temperature, humidity, pressure offset"""
        self._buffer = [0xab, 0xcd, 0x03, 0x17, 0xF1, 0x01]

        self._write_buffer()

        # Now get the response data from the buffer. The returned buffer length
        # is known to be 18.
        self._read_buffer(18)

        # Decode the data

        offsets = {}

        self._index = 4
        offsets['temperature'] = self._get_temperature()

        if self._buffer[6] < 128:
            offsets['temperature offset'] = float(self._buffer[6]) / 10
        else:
            offsets['temperature offset'] = float(self._buffer[6] - 256) / 10

        offsets['humidity'] = float(256*self._buffer[8] + self._buffer[7]) / 10

        if self._buffer[9] < 128:
            offsets['humidity offset'] = float(self._buffer[9]) / 10
        else:
            offsets['humidity offset'] = float(self._buffer[9] - 256) / 10

        offsets['pressure'] = float(256*self._buffer[11] + self._buffer[10])/10

        if self._buffer[12] < 128:
            offsets['pressure offset'] = float(self._buffer[12]) / 10
        else:
            offsets['pressure offset'] = float(self._buffer[12] - 256) / 10

        # I don't know what bytes 13, 14, and 15 are

        return offsets

    # %%
    @buffer_safety
    def write_offsets(self, offsets):

        """Set the device offsets for temperature, humidity, pressure"""

        # Check for errors in parameters
        if offsets['temperature offset'] > 6.1 or \
           offsets['temperature offset'] < -6:
            raise ValueError('Error! The temperature offset is {0} when it '
                             'must be between -6 and 6.1 C'.
                             format(offsets['temperature offset']))

        if offsets['humidity offset'] > 6.1 or offsets['humidity offset'] < -6:
            raise ValueError('Error! The humidity offset is {0} when it must '
                             'be between -6% and 6.1%'.
                             format(offsets['humidity offset']))

        if offsets['pressure offset'] > 6.1 or offsets['pressure offset'] < -6:
            raise ValueError('Error! The pressure offset is {0} when it must '
                             'be between -6hpa and 6.1hpa'.
                             format(offsets['pressure offset']))

        # The command to send, note we'll be overriding some bytes
        self._buffer = [0xab, 0xcd, 0x06, 0x16, 0, 0, 0, 0, 0]

        if offsets['temperature offset'] < 0:
            self._buffer[4] = 256 - int(offsets['temperature offset']*10)
        else:
            self._buffer[4] = int(offsets['temperature offset']*10)

        if offsets['humidity offset'] < 0:
            self._buffer[5] = 256 - int(offsets['humidity offset']*10)
        else:
            self._buffer[5] = int(offsets['humidity offset']*10)

        if offsets['pressure offset'] < 0:
            self._buffer[6] = 256 - int(offsets['pressure offset']*10)
        else:
            self._buffer[6] = int(offsets['pressure offset']*10)

        # Add the CRC bytes
        self._buffer[8], self._buffer[7] = modbusCRC(self._buffer[0:7])

        self._write_buffer()

        # Now get the response data from the buffer
        self._read_buffer(7)

        # Check the return code shows the data was correctly written
        if [171, 205, 4, 22, 0, 112, 213] != self._buffer:
            raise IOError("Error! Offset writing returned error code.")

    # %%
    @buffer_safety
    def restore_factory(self):

        """This command is given as a factory reset in the Windows software"""

        self._buffer = [0xab, 0xcd, 0x03, 0x20, 0xb0, 0xd7]

        self._write_buffer()

        # Now get the data from the buffer
        self._read_buffer(7)

        # Check the return code shows the data was correctly written
        if [171, 205, 4, 32, 0, 103, 117] != self._buffer:
            raise IOError("Error! Restore factory returned an error code.")

    # %%
    @buffer_safety
    def read_device_name(self):

        """Returns the device name"""

        self._buffer = [0xab, 0xcd, 0x03, 0x51, 0x70, 0xF3]

        self._write_buffer()

        # Now get the response data from the buffer, we know the length is
        # fixed to 16 bytes
        self._read_buffer(16)

        self._index = 4

        return self._get_name()
