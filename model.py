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
def conv_relu(inputs, filters, k_size, stride, padding, scope_name):

    # method that does convolution + relu on inputs

    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        in_channels = inputs.shape[-1]
        kernel = tf.get_variable('kernel',
                                [k_size, k_size, in_channels, filters],
                                initializer=tf.truncated_normal_initializer())
        biases = tf.get_variable('biases',
                                [filters],
                                initializer=tf.random_normal_initializer())
        conv = tf.nn.conv1d(inputs, kernel, strides=[1, stride, stride, 1], padding=padding)
    return tf.nn.relu(conv + biases, name=scope.name)

def maxpool(inputs, ksize, stride, padding='VALID', scope_name='pool'):
    '''A method that does max pooling on inputs'''
    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        pool = tf.nn.max_pool(inputs,
                            ksize=[1, ksize, ksize, 1],
                            strides=[1, stride, stride, 1],
                            padding=padding)
    return pool

def fully_connected(inputs, out_dim, scope_name='fc'):
    # A fully connected linear layer on inputs

    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        in_dim = inputs.shape[-1]
        w = tf.get_variable('weights', [in_dim, out_dim],
                            initializer=tf.truncated_normal_initializer())
        b = tf.get_variable('biases', [out_dim],
                            initializer=tf.constant_initializer(0.0))
        out = tf.matmul(inputs, w) + b
    return out


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
       	    # create dataset
       		   train_data = tf.data.Dataset.from_tensor_slices(train)
               train_data = train_data.shuffle(10000)
               train_data = train_data.batch(batch_size)

               test_data = tf.data.Dataset.from_tensor_slices(test)
               test_data = test_data.batch(batch_size)

               # creating iterator
               iterator = tf.data.Iterator.from_structure(train_data.output_types
                                                           train_data.output_shapes)
               # reshape array here if needed

               # Initializer for train and test Dataset
               self.train_init = iterator.make_initializer(train_data)
               self.test_init = iterator.make_initializer(test_data)

    def
