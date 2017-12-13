import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
sound_names = ["air conditioner","car horn","children playing","dog bark","drilling","engine idling",
               "gun shot","jackhammer","siren","street music","DJI Phantom1-Phantom2"]
sound_data = np.load('./urban_sound.npz')
X_data = sound_data['X']
y_data = sound_data['y']
print(X_data.shape, y_data.shape)
from sklearn.model_selection import train_test_split
X_sub, X_test, y_sub, y_test = train_test_split(X_data, y_data, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_sub, y_sub, test_size=0.2)
len(X_train), len(X_val), len(X_test), len(y_train), len(y_val), len(y_test)
print(X_train.shape, y_train.shape)
training_epochs = 6000
n_dim = 193
n_classes = 11
n_hidden_units_one = 363
n_hidden_units_two = 242
n_hidden_units_three = 121
learning_rate = 0.1
sd = 1 / np.sqrt(n_dim)
X = tf.placeholder(tf.float32,[None,n_dim])
Y = tf.placeholder(tf.float32,[None,n_classes])

with tf.name_scope("layer1") as scope:
    W_1 = tf.Variable(tf.random_normal([n_dim, n_hidden_units_one], mean=0, stddev=sd), name="weight1")
    b_1 = tf.Variable(tf.random_normal([n_hidden_units_one], mean=0, stddev=sd), name="bias1")
    h_1 = tf.nn.sigmoid(tf.matmul(X, W_1) + b_1)

    w1_hist = tf.summary.histogram("weights1", W_1)
    b1_hist = tf.summary.histogram("biases1", b_1)
    layer1_hist = tf.summary.histogram("layer1", h_1)

with tf.name_scope("layer2") as scope:
    W_2 = tf.Variable(tf.random_normal([n_hidden_units_one, n_hidden_units_two], mean=0, stddev=sd), name="weight2")
    b_2 = tf.Variable(tf.random_normal([n_hidden_units_two], mean=0, stddev=sd), name="bias2")
    h_2 = tf.nn.tanh(tf.matmul(h_1, W_2) + b_2)

    w2_hist = tf.summary.histogram("weights2", W_2)
    b2_hist = tf.summary.histogram("biases2", b_2)
    layer2_hist = tf.summary.histogram("layer2", h_2)

with tf.name_scope("layer3") as scope:
    W_3 = tf.Variable(tf.random_normal([n_hidden_units_two, n_hidden_units_three], mean=0, stddev=sd), name="weight3")
    b_3 = tf.Variable(tf.random_normal([n_hidden_units_three], mean=0, stddev=sd), name="bias3")
    h_3 = tf.nn.sigmoid(tf.matmul(h_2, W_3) + b_3)

    w3_hist = tf.summary.histogram("weights3", W_3)
    b3_hist = tf.summary.histogram("biases3", b_3)
    layer3_hist = tf.summary.histogram("layer3", h_3)

with tf.name_scope("layerOut") as scope:
    W = tf.Variable(tf.random_normal([n_hidden_units_three, n_classes], mean=0, stddev=sd), name="w")
    b = tf.Variable(tf.random_normal([n_classes], mean = 0, stddev=sd), name="b")
    y_ = tf.nn.softmax(tf.matmul(h_3, W) + b)

    wo_hist = tf.summary.histogram("weightsOut", W)
    bo_hist = tf.summary.histogram("biasesOut", b)
    y_softmax = tf.summary.histogram("layerOut", y_)

init = tf.initialize_all_variables()
with tf.name_scope("cost") as scope:
    cost_function = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(y_), reduction_indices=[1]))
    cost_summ = tf.summary.scalar("cost", cost_function)

with tf.name_scope("train") as scope:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

correct_prediction = tf.equal(tf.argmax(y_,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
accuracy_summ = tf.summary.scalar("accuracy", accuracy)

saver = tf.train.Saver()
cost_history = np.empty(shape=[1], dtype=float)

with tf.Session() as sess:
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("./logs/trainer")
    writer.add_graph(sess.graph)  # Show the graph
    sess.run(init)
    for epoch in range(training_epochs):
        summary,_, cost = sess.run([merged_summary,optimizer, cost_function], feed_dict={X: X_sub, Y: y_sub})
        writer.add_summary(summary, global_step=epoch)
        cost_history = np.append(cost_history, cost)

    acc = round(sess.run(accuracy, feed_dict={X: X_test, Y: y_test}), 3)
    print('Validation accuracy: ' + str(acc))
    saver.save(sess, "./model_494.ckpt")

fig = plt.figure(figsize=(10, 8))
fig.suptitle('Test accuracy: ' + str(acc), fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_title('validation data:20% test data:20%')
ax.set_xlabel('Iterations')
ax.set_ylabel('Cost')
plt.plot(cost_history)
plt.axis([0, training_epochs, 0, np.max(cost_history)])

plt.savefig('./accuracy.png')
plt.show()


