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
print(data)
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
#   create train_voltage, train_labels, test_voltage, test_labels
train_voltage = train_data["voltage"].values
train_labels = train_data["label"].values
test_voltage = test_data["voltage"].values
test_labels = test_data["label"].values

#   added trained and tested voltage and labels to tuples
train = (train_voltage, train_labels)
test = (test_voltage, test_labels)


"""
TODO
- Current data shape: (300, 4). Shape on a single line: (1,4)
- Figure out the size of the inputs (tf.shape?)
- Figure out and change the size of the kernel (filters)
- figure out the batch size of the inputs (lens()?)
- Change max_pool, fully_connected if need be
- look at train one epoch
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
	self.batch_size = 300			# split up data in 1 epoch
	self.keep_prob = tf.constant(0.75)	# probablity
	self.gstep = tf.Variable(0, dtype=tf.int32,
				trainable=False, name='global_step')
	self.n_classes = 10
	self.skip_step = 20
	self.n_test = 10000
	self.training = False

    def get_data(self):
        with tf.name_scope('data'):
            #   read EMG data. Return two tuples of numpy array of
            #   ((train_voltage, train_labels), (test_voltage, test_labels))

               # need to have label with the train_data and test_data
       	       # create dataset

       		   training_data = tf.data.Dataset.from_tensor_slices(train)
               training_data = training_data.shuffle(10000)
               training_data = training_data.batch(batch_size)

               testing_data = tf.data.Dataset.from_tensor_slices(test)
               testing_data = test_data.batch(batch_size)

               # creating iterator
               iterator = tf.data.Iterator.from_structure(training_data.output_types, training_data.output_shapes)
               voltage, label = iterator.get_next()

               # reshape array here if needed

               # Initializer for train and test Dataset
               self.train_init = iterator.make_initializer(training_data)
               self.test_init = iterator.make_initializer(testing_data)

    def inference(self):
         conv1 = conv_relu(inputs=self.voltage,
                        filters=32,
                        k_size=5,
                        stride=1,
                        padding='SAME',
                        scope_name='conv1')
        pool1 = maxpool(conv1, 2, 2, 'VALID', 'pool1')

        fc = fully_connected(pool1, 1024, 'fc')
        dropout = tf.nn.dropout(tf.nn.relu(fc), self.keep_prob, name='relu_dropout')
        self.logits = fully_connected(dropout, self.n_classes, 'logits')

    def loss(self):
        '''
        define loss function
        use softmax cross entropy with logits as the loss function
        compute mean cross entropy, softmax is applied internally
        '''
        #
        with tf.name_scope('loss'):
            entropy = tf.nn.softmax_cross_entropy_with_logits(labels=self.label, logits=self.logits)
            self.loss = tf.reduce_mean(entropy, name='loss')

    def optimize(self):
        '''
        Define training op
        using Adam Gradient Descent to minimize cost
        '''
        self.opt = tf.train.AdamOptimizer(self.lr).minimize(self.loss,
                                                global_step=self.gstep)

    def summary(self):
        '''
        Create summaries to write on TensorBoard
        '''
        with tf.name_scope('summaries'):
            tf.summary.scalar('loss', self.loss)
            tf.summary.scalar('accuracy', self.accuracy)
            tf.summary.histogram('histogram loss', self.loss)
            self.summary_op = tf.summary.merge_all()

    def eval(self):
        '''
        Count the number of right predictions in a batch
        '''
        with tf.name_scope('predict'):
            preds = tf.nn.softmax(self.logits)
            correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(self.label, 1))
            self.accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32))

    def build(self):
        '''
        Build the computation graph
        '''
        self.get_data()
        self.inference()
        self.loss()
        self.optimize()
        self.eval()
        self.summary()

    def train_one_epoch(self, sess, saver, init, writer, epoch, step):
        start_time = time.time()
        sess.run(init)
        self.training = True
        total_loss = 0
        n_batches = 0
        try:
            while True:
                _, l, summaries = sess.run([self.opt, self.loss, self.summary_op])
                writer.add_summary(summaries, global_step=step)
                if (step + 1) % self.skip_step == 0:
                    print('Loss at step {0}: {1}'.format(step, l))
                step += 1
                total_loss += l
                n_batches += 1
        except tf.errors.OutOfRangeError:
            pass
        saver.save(sess, 'checkpoints/convnet_mnist/mnist-convnet', step)
        print('Average loss at epoch {0}: {1}'.format(epoch, total_loss/n_batches))
        print('Took: {0} seconds'.format(time.time() - start_time))
        return step

    def eval_once(self, sess, init, writer, epoch, step):
        start_time = time.time()
        sess.run(init)
        self.training = False
        total_correct_preds = 0
        try:
            while True:
                accuracy_batch, summaries = sess.run([self.accuracy, self.summary_op])
                writer.add_summary(summaries, global_step=step)
                total_correct_preds += accuracy_batch
        except tf.errors.OutOfRangeError:
            pass

        print('Accuracy at epoch {0}: {1} '.format(epoch, total_correct_preds/self.n_test))
        print('Took: {0} seconds'.format(time.time() - start_time))

    def train(self, n_epochs):
        '''
        The train function alternates between training one epoch and evaluating
        '''
        utils.safe_mkdir('checkpoints')
        utils.safe_mkdir('checkpoints/convnet_mnist')
        writer = tf.summary.FileWriter('./graphs/convnet', tf.get_default_graph())

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(os.path.dirname('checkpoints/convnet_mnist/checkpoint'))
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)

            step = self.gstep.eval()

            for epoch in range(n_epochs):
                step = self.train_one_epoch(sess, saver, self.train_init, writer, epoch, step)
                self.eval_once(sess, self.test_init, writer, epoch, step)
        writer.close()

if __name__ == '__main__':
    model = ConvNet()
    model.build()
    model.train(n_epochs=30)
