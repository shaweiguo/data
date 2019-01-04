#!/usr/bin/env python
import pika
import random

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_name = 'hello'

channel.queue_declare(queue=queue_name)

num = random.randint(1, 1000)
msg = 'Hello world:{}'.format(str(num))

channel.basic_publish(exchange='', routing_key=queue_name, body=msg)
print(' [x] Sent {}'.format(msg))

connection.close()
