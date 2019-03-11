import tensorflow as tf
import numpy as np
import matplotlib
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split

# importing EMG data
filename = "EMG_raw_data_muscle1.csv"
data = pd.read_csv(filename)

# turn time and voltage to 1D array
data.columns = ["time","voltage"]
time = data["time"].values
voltage = data["voltage"].values
print("Time")
print(time)
print("voltage")
print(voltage)

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


class ConvNet(object):
    def __init__(self):
	self.learing_rate = 0.001		# set up learning rate
	self.batch_size = 128			# split up data in 1 epoch
	self.keep_prob = tf.constant(0.75)	# probablity
	self.gstep = tf.Variable(0, dtype=tf.int32, 
				trainable=False, name='global_step')
	self.n_classes = 10
	self.skip_step = 20
	self.n_test = 10000
	self.training = False

    def get_data(self):
	with tf.name_scope('data'):
            	# need to have label with the train_data and test_data
	    	# create iterator
		train_data = tf.data.Dataset.from_tensor_slices(train)

