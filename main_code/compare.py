# this code will write serial input from arduino 1 into python, show the code, then tell Arduino 2 to blink LED 

import serial, time
import pickle
import re
import pandas as pd
import numpy as np

AnalogAddress = '/dev/cu.usbmodem14502'; # port of analog source
CommandAddress = '/dev/cu.usbmodem14101';  # port to send digital commands

arduino1 = serial.Serial(AnalogAddress,115200,timeout=1)
arduino2 = serial.Serial(CommandAddress,115200,timeout=1)

# initialize a list to hold data

df = pd.DataFrame(columns=['x', 'y','z','muscle1','muscle2','muscle3'])

while True:
    raw_input = arduino1.readline()  # read input from arduino
    input_decoded = raw_input.decode()  # decode raw data to string
    data = np.array([x for x in input_decoded.rstrip().split("\t")], dtype=np.float32) # remove \t and do what?
    df = df.append(pd.Series([data[0], data[1], data[2], data[3], data[4], data[5]], index=df.columns), ignore_index=True) #  make a table and bring it into proper format
    lastrow = df.tail(1) # save most current analog signals to process

    iddleAnalog=[0,0,0,0,0,0]
    Train1Analog=[1,0,0,0,0,0]
    Train2Analog=[0,1,0,0,0,0]
    ActivationAnalog=[0,0,1,0,0,0]
    
    if (lastrow == iddleAnalog) :
                  # don't  show anything here
        arduino2.write(b'L')       
    if (lastrow == Train1Analog) :
        arduino2.write(b'H')
                  #  label train mode 1 here for ML
    if (lastrow == Train2Analog) :
        arduino2.write(b'L')
        time.sleep(1)
        arduino2.write(b'H')
                  # label train mode 2 here for ML
    if (lastrow == ActivationAnalog) :
                  # Start ML prediction here
        # turn led on
        arduino2.write(b'H')
        time.sleep(1) # delay 1 sec
        # turn led off  
        arduino2.write(b'L')
        time.sleep(1)
