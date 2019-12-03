# this code will write serial input from arduino into python and show the code

import serial, time
import pickle
import re
import pandas as pd
import numpy as np

arduino1 = serial.Serial('/dev/cu.usbmodem14501',115200,timeout=1)

# time.sleep(1)

# initialize a list to hold data

df = pd.DataFrame(columns=['x', 'y','z','muscle1','muscle2','muscle3'])
raw_input = arduino1.readline()  # read input from arduino

for i in range(0,10):
    raw_input = arduino1.readline()      # actual arduino reading
##    if (raw_input == '') :
##        print('expected noon')
##    else :
    print(raw_input)
#    input_decoded = raw_input.decode()  # decode raw data to string
            # converting string to float
        
##    data = np.array([x for x in input_decoded.rstrip().split("\t")], dtype=np.float32)
##
##            # attach the data to the dataframe
##            # does the dataframe change when append new data?
##
##        df = df.append(pd.Series([data[0], data[1], data[2], data[3], data[4], data[5]], index=df.columns), ignore_index=True)
##        lastrow = df.tail(1)
##        cond = [500, 500, 500, 500, 500, 500]
##        if (all(lastrow<cond) == 'true') :
##            arduino.write(b'H') #tell Arduino to turn it on
##        else :
##            arduino.write(b'L') #tell Arduino to turn it off
##        
# let's print out some value here to confirm we got the right data


## SECTION BELOW IS FOR LED
    # initialize board. Must close serial monitor before running code
#arduino = serial.Serial('/dev/cu.usbmodem14401', 115200, timeout=1) # Serial(port_name, baudrate, timeout=1)

arduino2 = serial.Serial('/dev/cu.usbmodem14101', 115200, timeout=1) 
while True:
    # turn led on
    arduino2.write(b'H')
    time.sleep(1) # delay 1 sec
    # turn led off  
    arduino2.write(b'L')
    time.sleep(1)

