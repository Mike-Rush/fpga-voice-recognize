# %load mnist_int16_test.py
import input_data
import numpy as np
import tensorflow.compat.v1 as tf
import reader

print("reading data...")
batch_id, data, label = reader.get_train_data('dataset/train.tfrecord')
print("finish reading data")

sess = tf.InteractiveSession()

tf.disable_v2_behavior()


def Record_Tensor(tensor, name):
    print("Recording tensor " + name + " ...")
    f = open('./record/' + name + '.dat', 'w')
    array = tensor.eval()
    # print ("The range: ["+str(np.min(array))+":"+str(np.max(array))+"]")
    if np.size(np.shape(array)) == 1:
        Record_Array1D(array, name, f)
    else:
        if np.size(np.shape(array)) == 2:
            Record_Array2D(array, name, f)
        else:
            if np.size(np.shape(array)) == 3:
                Record_Array3D(array, name, f)
            else:
                Record_Array4D(array, name, f)
    f.close()


def Record_Array1D(array, name, f):
    print("1D")
    for i in range(np.shape(array)[0]):
        f.write(str(array[i]) + "\n")


def Record_Array2D(array, name, f):
    print("2D")
    for i in range(np.shape(array)[0]):
        for j in range(np.shape(array)[1]):
            f.write(str(array[i][j]) + "\n")


def Record_Array3D(array, name, f):
    print("3D")
    for i in range(np.shape(array)[0]):
        for j in range(np.shape(array)[1]):
            for k in range(np.shape(array)[2]):
                f.write(str(array[i][j][k]) + "\n")


def Record_Array4D(array, name, f):
    print("4D")
    for i in range(np.shape(array)[0]):
        for j in range(np.shape(array)[1]):
            for k in range(np.shape(array)[2]):
                for l in range(np.shape(array)[3]):
                    f.write(str(array[i][j][k][l]) + "\n")


with tf.name_scope('input'):
    x = tf.placeholder("float", shape=[None, 2880])
    y_ = tf.placeholder("float", shape=[None, 10])


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# First Convolutional Layer
with tf.name_scope('1st_CNN'):
    W_conv1 = weight_variable([3, 3, 1, 16])
    b_conv1 = bias_variable([16])
    x_voice = tf.reshape(x, [-1, 80, 36, 1])
    h_conv1 = tf.nn.relu(conv2d(x_voice, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

# Second Convolutional Layer
with tf.name_scope('2rd_CNN'):
    W_conv2 = weight_variable([3, 3, 16, 32])
    b_conv2 = bias_variable([32])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

# Densely Connected Layer
with tf.name_scope('Densely_NN'):
    W_fc1 = weight_variable([20 * 9 * 32, 128])
    b_fc1 = bias_variable([128])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 20 * 9 * 32])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout
with tf.name_scope('Dropout'):
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout Layer
with tf.name_scope('Softmax'):
    W_fc2 = weight_variable([128, 10])
    b_fc2 = bias_variable([10])
    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

with tf.name_scope('Loss'):
    cross_entropy = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y_conv, 1e-8, 1)))

with tf.name_scope('Train'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

with tf.name_scope('Accuracy'):
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

tf.initialize_all_variables().run()

for i in range(15000):

    if i % 20 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: data[i], y_: label[i], keep_prob: 1.0})
        print("step %d, training accuracy %g" % (i, train_accuracy))
    train_step.run(feed_dict={x: data[i], y_: label[i], keep_prob: 0.5})

Record_Tensor(W_conv1, "W_conv1")
Record_Tensor(b_conv1, "b_conv1")
Record_Tensor(W_conv2, "W_conv2")
Record_Tensor(b_conv2, "b_conv2")
Record_Tensor(W_fc1, "W_fc1")
Record_Tensor(b_fc1, "b_fc1")
Record_Tensor(W_fc2, "W_fc2")
Record_Tensor(b_fc2, "b_fc2")
sess.close()
