# this code will write serial input to arduino to control the LED

import serial, time
import pickle
import re
import pandas as pd
import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt

arduino = serial.Serial('/dev/ttyACM0',115200,timeout=1)

time.sleep(1)
filename = "EMG_svm_pickle.pkl"
svm_clf = pickle.load(open(filename, 'rb'))
count = 0

df = pd.DataFrame()
while 1:
    raw_input = arduino.readline()
    decoded_input = raw_input.decode()



    print()


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
