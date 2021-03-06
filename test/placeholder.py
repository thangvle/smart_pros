import tensorflow as tf

a = tf.placeholder(tf.float32, shape =[3])
b = tf.constant([5, 5, 5], tf.float32)

# a is used as constant rather than placeholder
c = a + b

writer = tf.summary.FileWriter('graph/placeholders', tf.get_default_graph())
with tf.Session() as sess:
    # compute c as a + b (add in matrix)
    print(sess.run(c, {a: [1, 2, 3]}))    # result c = [6 7 8]
    writer.close()

a = tf.add(2, 5) # a =7
b = tf.multiply(a, 3) # b = a * 3 = 21
writer2 = tf.summary.FileWriter('graph/feed_dict', tf.get_default_graph())
with tf.Session() as sess:
    print(sess.run(b)) # compute b
    print(sess.run(b, feed_dict = {a:15})) # set a = 15, compute b 
