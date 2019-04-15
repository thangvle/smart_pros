import tensorflow as tf

a = tf.placeholder(tf.float32, shape =[3])
b = tf.constant([5 5 5], tf.float32)

# a is used as constant rather than placeholder
c = a + b

writer = tf.summary.FileWriter('graph/placeholders', tf.get_default_graph())
with tf.Session() as sess:
    # compute c as a + b (add in matrix)
    print(sess.run(c, {a: [1 2 3]}))    # result c = [6 7 8]
    writer.close()
    
