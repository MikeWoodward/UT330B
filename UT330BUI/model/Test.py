# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:11:25 2016

@author: mwoodward
"""

# =============================================================================
# Imports
# =============================================================================
import datetime
from UT330 import UT330

# =============================================================================
# Helper functions
# =============================================================================
def device_name(ut330):
    """Read the device name"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading device name ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("Device name = {0}".format(ut330.read_device_name()))
    print()

def device_config(ut330):
    """Get the device configuration"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading config info ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

    CONFIG = ut330.read_config()

    # Write the config data to file and screen
    CONFIG_FILE = 'UT330_config_{0}.csv'. \
                  format(CONFIG['timestamp'].strftime("%Y%m%d_%H%M%S"))

    with open(CONFIG_FILE, 'w') as config_file:

        for key, value in CONFIG.items():
            config_file.write("{0}, {1}\n".format(key, value))
            print("{0} = {1}".format(key, value))
    
    print()
    
def device_offsets(ut330):
    """Read offsets"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading offsets ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

    OFFSETS = ut330.read_offsets()

    # Write the data to file

    OFFSETS_FILE = 'UT330_offset.csv'
    with open(OFFSETS_FILE, 'w') as offsets_file:

        for key, value in OFFSETS.items():
            offsets_file.write("{0}, {1}\n".format(key, value))
            print("{0} = {1}".format(key, value))

    print()    

def device_readdata(ut330):
    """Read data"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Reading data ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

    DATA = ut330.read_data()

    if DATA != []:

        TIMESTAMP = DATA[0]['Timestamp']

        # Write the data to file

        DATA_FILE = 'UT330_data_{0}.csv'.\
                    format(TIMESTAMP.strftime("%Y%m%d_%H%M%S"))

        with open(DATA_FILE, 'w') as data_file:

            HEADER = 'Timestamp,Temperature (C),' \
                     'Relative humidity (%),' \
                     'Pressure (Pa)\n'

            data_file.write(HEADER)

            print(HEADER[:-1])

            for data_line in DATA:

                line = "{0}, {1}, {2}, {3}\n". \
                       format(data_line['Timestamp'],
                              data_line['Temperature (C)'],
                              data_line['Relative humidity (%)'],
                              data_line['Pressure (Pa)'])

                data_file.write(line)

                print(line[:-1])

        print() 
 
def device_writeoffsets(ut330):
    """Write offsets"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Write offsets ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

    OFFSETS = {'temperature offset': 0,
               'humidity offset': 0,
               'pressure offset': 0}

    ut330.write_offsets(OFFSETS)

    OFFSETS = ut330.read_offsets()

    OFFSETS_FILE = 'UT330_offset.csv'

    for key, value in OFFSETS.items():
        print("{0} = {1}".format(key, value))

    print()    
    
def device_writeconfig(ut330):
    """Write config"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Write config ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

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

    for k, v in CONFIG.items():
        print("{0} Old = {1} New = {2}".format(k, CONFIG[k],
                                               CONFIG_NEW[k]))

    print()   
    
def device_writedatetime(ut330):
    """Write data and time"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Write date time ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    NOW = datetime.datetime.now()

    ut330.write_datetime(NOW)
    
def device_restorefactory(ut330):
    """Restore factory settings"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Restore factory ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    ut330.restore_factory()   
    
def device_deletedata(ut330):
    """Delete the data"""
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ Delete data ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")
    print("▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉")

    ut330.delete_data()    
# =============================================================================
# Main
# =============================================================================
try:
    
    # Open the device
    with UT330() as ut330:
        
        device_name(ut330)
        device_config(ut330)
        device_offsets(ut330)
        device_readdata(ut330)
        device_writedatetime(ut330)
#        device_writeoffsets(ut330)
#        device_writeconfig(ut330)
#        device_restorefactory(ut330)
#        device_deletedata(ut330)

except IOError as error:

    print(error)
    
except Exception as error:

    print(error)
