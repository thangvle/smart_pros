# this code will write serial input to arduino to control the LED

import serial, time
import pickle
import re
import pandas as pd
import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt

# initialize arduino object and port
#arduino_reader = serial.Serial('/dev/ttyACM0',115200,timeout=1)
arduino_reader = serial.Serial('/dev/cu.usbmodem14502',115200,timeout=1)
arduino_command = serial.Serial('/dev/cu.usbmodem14101', 115200, timeout=1) 
#arduino_command = serial.Serial('dev/ttyACM1',115200, timeout=1)
# load svm model
filename = "/Users/nhok2303/Desktop/github/smart_pros/hand_jupyter_notebook/emg_svm_model.pkl"
emg_model = pickle.load(open(filename, 'rb'))


# initialize a list to hold data

df = pd.DataFrame(columns=['x', 'y','z','muscle1','muscle2','muscle3'])
raw_input = arduino_reader.readline()  # read input from arduino
time.sleep(1)   # skip the first few bad data

while(1):
    raw_input = arduino_reader.readline()      # actual arduino reading

    input_decoded = raw_input.decode()  # decode raw data to string
    # converting string to float
    data = np.array([x for x in input_decoded.rstrip().split("\t")], dtype=np.float32)

    # attach the data to the dataframe
    # does the dataframe change when append new data?
    
    df = df.append(pd.Series([data[0], data[1], data[2], data[3], data[4], data[5]], index=df.columns), ignore_index=True)
    #print(df.tail(1))
    mode = emg_model.predict(df.tail(1))
    #print(mode)
    if(mode == "hold"):
        arduino_command.write(b'H')
    if(mode == "grip"):
        arduino_command.write(b'G')
    if(mode == "rest"):
        arduino_command.write(b'R')



'''
for i in range(5):
    arduino.write(b'H')
    time.sleep(1)
    arduino.write(b'L')
    time.sleep(1)
# export to csv. Comment t variables. Maximum is 2048 his code out if not need to
'''
'''
        y_pred = svm_clf.predict(df)
        print(y_pred)
        for i in y_pred:
            if i == 'rest':
                arduino.write(b'R')
            elif i == 'active':
                arduino.write(b'A')

'''


#df = pd.DataFrame()

#plt.plot(cleandata)
#plt.show()



'''
while(input != None):
    raw_input = arduino.readline()
    #print((input))
    # read digit only input from arduino
    input_decoded = input.decode()
    input_formatted = input_decoded.rstrip()

    #flt = float(input_formatted)
    #print(input_decoded)
    #print(flt)
    #print(digit_array.shape)
    #print(digit_array.shape)

    #data_array = np.append(data_array, [digit_array], axis=0)
arduino.close()
'''
#plt.plot(digit_array)
#plt.show()
    #print(data_array)
    #for line in data:
    #    print(line)
    #create dataframe from data_array
    #df = pd.DataFrame()
#print()

    #df.head(10)

    #svm_clf.predict(digit)
