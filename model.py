import tensorflow as tf
import numpy as np
import matplotlib
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split

# importing EMG data
filename = "EMG_label_data_muscle1.csv"
data = pd.read_csv(filename)

# turn time and voltage to 1D array
data.columns = ["time_stamp", "voltage", "time", "label"]
time = data["time"].values
voltage = data["voltage"].values
labels = data["label"].values
print("Time")
print(time)
print("voltage")
print(voltage)
print("label")
print(labels)

train_data, test_data = train_test_split(data, train_size=0.8)
print("train_data")
print(train_data)
print("test_data")
print(test_data)


"""
TODO

- Initialize variable for time and voltage as 1D array
- Initialize Weight function
- Create loss function and optimizer (SGD)
- tf.session
"""
