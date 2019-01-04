#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('sha', 'q1w2e3r4')
params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

exchange_name = 'direct_logs'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
msg = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange=exchange_name, routing_key=severity, body=msg)
print(' [x] Sent {}'.format(msg))

connection.close()
