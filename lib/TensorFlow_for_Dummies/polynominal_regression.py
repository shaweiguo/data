'''
    Demonstrates how an application can monitor sessions with session hooks
    ax3+bx2+cx+d
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

# Random input values
N = 40
x = tf.random_normal([N])
a_real = tf.truncated_normal([N], mean=2.0)
b_real = tf.truncated_normal([N], mean=-2.0)
c_real = tf.truncated_normal([N], mean=-1.0)
d_real = tf.truncated_normal([N], mean=1.0)
y = a_real * tf.pow(x, 3) + b_real * tf.pow(x, 2) + c_real * x + d_real

# Variables
a = tf.Variable(tf.random_normal([]))
b = tf.Variable(tf.random_normal([]))
c = tf.Variable(tf.random_normal([]))
d = tf.Variable(tf.random_normal([]))

# Compute model and loss
model = a * tf.pow(x, 3) + b * tf.pow(x, 2) + c * x + d
loss = tf.reduce_mean(tf.pow(model - y, 2))

# Create optimizer
learn_rate = 0.01
num_epochs = 400
num_batches = N
optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)

# Initialize variables
init = tf.global_variables_initializer()

# Launch session
with tf.Session() as sess:
    sess.run(init)

    # Perform training
    for epoch in range(num_epochs):
        for batch in range(num_batches):
            sess.run(optimizer)

    # Display results
    print('a = ', sess.run(a))
    print('b = ', sess.run(b))
    print('c = ', sess.run(c))
    print('d = ', sess.run(d))

# #多项式回归
# import numpy as np
# import tensorflow as tf
# import matplotlib.pyplot as plt
#
# n_observation=100
# xs=np.linspace(-3,3,n_observation)
# ys=np.sin(xs)+np.random.uniform(-0.5,0.5,n_observation)
# plt.scatter(xs,ys)
# plt.show()
#
# X=tf.placeholder(tf.float32,name="X")
# Y=tf.placeholder(tf.float32,name="Y")
#
# W=tf.Variable(tf.random_uniform([1]),name="weights")
# b=tf.Variable(tf.random_uniform([1]),name="bias")
#
# Y_pred=tf.add(tf.multiply(X,W),b)
#
# W_2=tf.Variable(tf.random_uniform([1]),name="weights_2")
# Y_pred=tf.add(tf.multiply(tf.pow(X,2),W_2),Y_pred)
# W_3=tf.Variable(tf.random_uniform([1]),name="weights_3")
# Y_pred=tf.add(tf.multiply(tf.pow(X,2),W_3),Y_pred)
#
# sample_num=xs.shape[0]
# loss=tf.reduce_sum(tf.pow(Y_pred-Y,2))/sample_num
#
# learning_rate=0.01
# optimizer=tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
#
# init=tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#
#     writer=tf.summary.FileWriter('./graphs/polynomial_reg',sess.graph)
#
#     for i in range(1000):
#         total_loss=0
#         for x,y in zip(xs,ys):
#             _,l=sess.run([optimizer,loss],feed_dict={X:x,Y:y})
#             total_loss+=l
#         if i%20 ==0:
#             print ('epoch {0}: {1}'.format(i,total_loss/sample_num))
#
#     writer.close()
#
#     W, W_2, W_3, b=sess.run([W, W_2, W_3, b])
#     print(W, W_2, W_3, b)
#
#     print ("W:" + str(W[0]))
#     # print(W, b)
#
#     print ("W:" + str(W[0]))
#     print ("W_2:" + str(W_2[0]))
#     print ("W_3:" + str(W_3[0]))
#     print ("b:" + str(b[0]))
#
#     plt.plot(xs,ys,'bo',label='real_data')
#     plt.plot(xs,xs*W+np.power(xs,2)*W_2+np.power(xs,3)*W_3+b,'r',label='Predicted data')
#     plt.legend()
#     plt.show()
