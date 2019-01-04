''' Demonstrates how an application can monitor sessions with session hooks '''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

# Random input values
N = 40
x = tf.random_normal([N])
m_real = tf.truncated_normal([N], mean=2.0)
b_real = tf.truncated_normal([N], mean=3.0)
y = m_real * x + b_real

# Variables
m = tf.Variable(tf.random_normal([]))
b = tf.Variable(tf.random_normal([]))

# Compute model and loss
model = tf.add(tf.multiply(x, m), b)
loss = tf.reduce_mean(tf.pow(model - y, 2))

# Create optimizer
learn_rate = 0.1
num_epochs = 200
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
    print('m = ', sess.run(m))
    print('b = ', sess.run(b))

# #线性回归
# import numpy as  np
# import tensorflow as tf
# import matplotlib.pyplot as plt
#
# n_observations=100
# xs=np.linspace(-3,3,n_observations)
# ys=np.sin(xs)+np.random.uniform(-0.5,0.5,n_observations)
# plt.scatter(xs,ys)
# plt.show()
#
# X=tf.placeholder(tf.float32,name='X')
# Y=tf.placeholder(tf.float32,name='Y')
#
# # just state these two parameters
# W=tf.Variable(tf.random_normal([1]),name='weight')
# b=tf.Variable(tf.random_normal([1]),name='bias')
#
# Y_pred=tf.add(tf.multiply(X,W),b,name="y_pred")
#
# loss=tf.square(Y-Y_pred,name='loss')
#
# learning_rate=0.01
# optimizer=tf.train.ProximalGradientDescentOptimizer(learning_rate).minimize(loss)
#
# n_samples=xs.shape[0]
#
# # inititalize these parameters.Only after this step, the para will have value
# init=tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#     writer=tf.summary.FileWriter('./graphs/linear_reg',sess.graph)
#
#     for i in range(50):
#         total_loss=0
#         for x,y in zip(xs,ys):
#             _,l=sess.run([optimizer,loss],feed_dict={X:x,Y:y})
#             total_loss+=l
#
#         if i%5 ==0:
#             print('Epoch:{0}: {1}'.format(l,total_loss/n_samples) )
#
#     writer.close();
#     # need run, and then  you can get the content of w and b
#     W,b=sess.run([W,b])
#     print(W,b)
#
#     print ("W:"+str(W[0]))
#     print ("b:"+str(b[0]))
#
#     plt.plot(xs,ys,'bo',label='Real data')
#     plt.plot(xs,xs*W+b,'r',label='Predicted data')
#     plt.legend()
#     plt.show()
