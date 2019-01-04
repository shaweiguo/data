#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('us', 5672, '/', credentials)
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
